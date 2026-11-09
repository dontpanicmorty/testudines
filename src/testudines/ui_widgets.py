"""Reusable native Qt widgets: code editor, markdown view, runnable code blocks."""
from __future__ import annotations

import re
import sys
from typing import Callable

from PySide6.QtCore import QObject, QRect, QRunnable, QSize, Qt, QThreadPool, Signal
from PySide6.QtGui import (QColor, QFont, QFontDatabase, QFontMetrics, QKeyEvent, QPainter,
                           QSyntaxHighlighter, QTextCharFormat, QTextFormat)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPlainTextEdit, QPushButton,
                               QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

from . import runner

# The Run and Check shortcuts, as each platform writes them (the editor accepts Cmd or Ctrl)
RUN_KEYS, CHECK_KEYS = ("⌘↵", "⇧⌘↵") if sys.platform == "darwin" else ("Ctrl+Enter", "Ctrl+Shift+Enter")


def is_dark() -> bool:
    return QApplication.palette().window().color().lightness() < 128


def mono_font(size: int = 13) -> QFont:
    f = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
    f.setPointSize(size)
    return f


# ---------------------------------------------------------------- background work
class _Signals(QObject):
    done = Signal(object)


class _Job(QRunnable):
    def __init__(self, fn: Callable, *a) -> None:
        super().__init__()
        self.fn, self.a, self.signals = fn, a, _Signals()

    def run(self) -> None:
        try:
            res = self.fn(*self.a)
        except Exception as e:  # surface, never crash the UI thread
            res = {"ok": False, "passed": False, "output": f"Internal error: {e}"}
        self.signals.done.emit(res)


_live: set = set()


def run_async(fn: Callable, cb: Callable, *a) -> None:
    job = _Job(fn, *a)
    _live.add(job)

    def finish(res):
        _live.discard(job)
        cb(res)

    job.signals.done.connect(finish)
    QThreadPool.globalInstance().start(job)


# ---------------------------------------------------------------- syntax highlighting
KEYWORDS = ("and as assert async await break class continue def del elif else except finally for from "
            "global if import in is lambda nonlocal not or pass raise return try while with yield "
            "match case").split()
CONSTS = ["True", "False", "None"]
BUILTINS = ("print len range int float str bool list dict set tuple sum min max sorted enumerate zip map "
            "filter any all abs round open isinstance type repr input reversed next iter super object "
            "Exception ValueError TypeError KeyError IndexError").split()


class PyHighlighter(QSyntaxHighlighter):
    def __init__(self, doc) -> None:
        super().__init__(doc)
        d = is_dark()
        col = dict(kw="#ff7ab2" if d else "#b4237b", const="#d0a8ff" if d else "#6f42c1",
                   builtin="#6bdfff" if d else "#0a7a99", string="#fc6a5d" if d else "#b3361c",
                   comment="#7f8c98" if d else "#6a737d", number="#d9c97c" if d else "#946800",
                   defn="#67b7a4" if d else "#1a6fb5", deco="#ffa14f" if d else "#b35900")

        def fmt(c: str, bold=False, italic=False) -> QTextCharFormat:
            f = QTextCharFormat()
            f.setForeground(QColor(c))
            if bold:
                f.setFontWeight(QFont.Weight.Bold)
            f.setFontItalic(italic)
            return f

        self.rules = [
            (re.compile(r"\b(" + "|".join(BUILTINS) + r")\b"), fmt(col["builtin"])),
            (re.compile(r"\b(" + "|".join(KEYWORDS) + r")\b"), fmt(col["kw"], bold=True)),
            (re.compile(r"\b(" + "|".join(CONSTS) + r")\b"), fmt(col["const"])),
            (re.compile(r"\b\d+(\.\d+)?([eE][+-]?\d+)?\b"), fmt(col["number"])),
            (re.compile(r"(?<=\bdef )\w+|(?<=\bclass )\w+"), fmt(col["defn"], bold=True)),
            (re.compile(r"^\s*@[\w.]+"), fmt(col["deco"])),
        ]
        self.f_str, self.f_com = fmt(col["string"]), fmt(col["comment"], italic=True)
        self.str_re = re.compile(r"""[rbfRBF]{0,2}("[^"\\\n]*(\\.[^"\\\n]*)*"|'[^'\\\n]*(\\.[^'\\\n]*)*')""")
        self.com_re = re.compile(r"#[^\n]*")

    def highlightBlock(self, text: str) -> None:
        for rx, f in self.rules:
            for m in rx.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), f)
        for m in self.str_re.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.f_str)
        # triple-quoted strings (state 1 = ''' , 2 = """)
        state = self.previousBlockState()
        pos = 0
        cur = state if state in (1, 2) else 0
        while pos < len(text):
            if cur:
                q = '"""' if cur == 2 else "'''"
                end = text.find(q, pos)
                if end < 0:
                    self.setFormat(pos, len(text) - pos, self.f_str)
                    pos = len(text)
                else:
                    self.setFormat(pos, end + 3 - pos, self.f_str)
                    pos, cur = end + 3, 0
            else:
                a, b = text.find('"""', pos), text.find("'''", pos)
                cands = [(i, c) for i, c in ((a, 2), (b, 1)) if i >= 0]
                if not cands:
                    break
                i, c = min(cands)
                before = text[:i]
                if "#" in before:  # triple quote inside a comment
                    break
                cur, pos = c, i + 3
                self.setFormat(i, 3, self.f_str)
        self.setCurrentBlockState(cur)
        for m in self.com_re.finditer(text):
            if self.format(m.start()) != self.f_str:
                self.setFormat(m.start(), m.end() - m.start(), self.f_com)


SQL_KEYWORDS = ("select from where and or not in is null like ilike between exists as on join inner left right "
                "full outer cross natural using group by order having limit offset distinct all any union intersect "
                "except with recursive case when then else end cast create replace view table insert into values "
                "update set delete drop alter primary key references default over partition window rows range "
                "unbounded preceding following current filter qualify asc desc nulls first last true false").split()
SQL_FUNCTIONS = ("count sum avg min max coalesce nullif greatest least round floor ceil abs length lower upper trim "
                 "substring substr replace concat string_agg row_number rank dense_rank ntile lag lead first_value "
                 "last_value date_trunc date_part extract strftime strptime now current_date").split()


class SqlHighlighter(QSyntaxHighlighter):
    """Keywords, functions, strings, numbers and -- comments, in the same colours as Python code."""

    def __init__(self, doc) -> None:
        super().__init__(doc)
        d = is_dark()

        def fmt(c: str, bold=False, italic=False) -> QTextCharFormat:
            f = QTextCharFormat()
            f.setForeground(QColor(c))
            if bold:
                f.setFontWeight(QFont.Weight.Bold)
            f.setFontItalic(italic)
            return f

        self.rules = [
            (re.compile(r"(?i)\b(" + "|".join(SQL_FUNCTIONS) + r")(?=\s*\()"), fmt("#6bdfff" if d else "#0a7a99")),
            (re.compile(r"(?i)\b(" + "|".join(SQL_KEYWORDS) + r")\b"), fmt("#ff7ab2" if d else "#b4237b", bold=True)),
            (re.compile(r"\b\d+(\.\d+)?\b"), fmt("#d9c97c" if d else "#946800")),
            (re.compile(r"'(?:[^']|'')*'"), fmt("#fc6a5d" if d else "#b3361c")),
            (re.compile(r"--[^\n]*"), fmt("#7f8c98" if d else "#6a737d", italic=True)),
        ]

    def highlightBlock(self, text: str) -> None:
        for rx, f in self.rules:
            for m in rx.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), f)


# ---------------------------------------------------------------- code editor
class _LineNumbers(QWidget):
    def __init__(self, ed: "CodeEditor") -> None:
        super().__init__(ed)
        self.ed = ed

    def sizeHint(self) -> QSize:
        return QSize(self.ed.line_number_width(), 0)

    def paintEvent(self, e) -> None:
        self.ed.paint_numbers(e)


class CodeEditor(QPlainTextEdit):
    submit = Signal()  # Cmd/Ctrl+Enter
    check = Signal()   # Shift+Cmd/Ctrl+Enter

    def __init__(self, text: str = "", readonly: bool = False, language: str = "python") -> None:
        super().__init__()
        self.language = language
        self.setFont(mono_font())
        self.setTabStopDistance(QFontMetrics(self.font()).horizontalAdvance(" ") * 4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setReadOnly(readonly)
        self.setPlainText(text)
        self.hl = SqlHighlighter(self.document()) if language == "sql" else PyHighlighter(self.document())
        self.numbers = _LineNumbers(self)
        self.blockCountChanged.connect(self._update_margin)
        self.updateRequest.connect(self._scroll_numbers)
        self._update_margin()

    # line numbers
    def line_number_width(self) -> int:
        digits = max(2, len(str(self.blockCount())))
        return 14 + self.fontMetrics().horizontalAdvance("9") * digits

    def _update_margin(self) -> None:
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)

    def _scroll_numbers(self, rect, dy) -> None:
        if dy:
            self.numbers.scroll(0, dy)
        else:
            self.numbers.update(0, rect.y(), self.numbers.width(), rect.height())

    def resizeEvent(self, e) -> None:
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.numbers.setGeometry(QRect(cr.left(), cr.top(), self.line_number_width(), cr.height()))

    def paint_numbers(self, event) -> None:
        p = QPainter(self.numbers)
        p.fillRect(event.rect(), self.palette().alternateBase())
        p.setPen(QColor("#7f8c98"))
        block = self.firstVisibleBlock()
        n = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                p.drawText(0, top, self.numbers.width() - 6, self.fontMetrics().height(),
                           Qt.AlignmentFlag.AlignRight, str(n + 1))
            block = block.next()
            top, bottom = bottom, bottom + round(self.blockBoundingRect(block).height())
            n += 1

    # editing behaviour
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if self.isReadOnly():
            return super().keyPressEvent(e)
        mod, key = e.modifiers(), e.key()
        ctrl = bool(mod & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier))
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if ctrl and (mod & Qt.KeyboardModifier.ShiftModifier):
                return self.check.emit()
            if ctrl:
                return self.submit.emit()
            line = self.textCursor().block().text()
            col = self.textCursor().positionInBlock()
            before = line[:col]
            indent = re.match(r"\s*", line).group()
            if self.language == "python" and before.rstrip().endswith(":"):
                indent += "    "
            super().keyPressEvent(e)
            return self.insertPlainText(indent)
        if key == Qt.Key.Key_Tab and not (mod & Qt.KeyboardModifier.ShiftModifier):
            c = self.textCursor()
            if c.hasSelection():
                return self._shift_lines(True)
            return c.insertText(" " * (4 - c.positionInBlock() % 4))
        if key == Qt.Key.Key_Backtab:
            return self._shift_lines(False)
        if key == Qt.Key.Key_Backspace and not self.textCursor().hasSelection():
            c = self.textCursor()
            before = c.block().text()[:c.positionInBlock()]
            if before and before.strip() == "" and len(before) % 4 == 0:
                for _ in range(4):
                    c.deletePreviousChar()
                return
        super().keyPressEvent(e)

    def _shift_lines(self, right: bool) -> None:
        c = self.textCursor()
        doc = self.document()
        a, b = doc.findBlock(c.selectionStart()), doc.findBlock(c.selectionEnd())
        c.beginEditBlock()
        blk = a
        while True:
            cur = self.textCursor()
            cur.setPosition(blk.position())
            if right:
                cur.insertText("    ")
            else:
                t = blk.text()
                n = min(4, len(t) - len(t.lstrip(" ")))
                for _ in range(n):
                    cur.deleteChar()
            if blk == b:
                break
            blk = blk.next()
        c.endEditBlock()

    def fit_height(self, min_lines: int = 2, max_lines: int = 28) -> None:
        n = max(min_lines, min(max_lines, self.blockCount()))
        h = self.fontMetrics().lineSpacing() * n + 18
        self.setFixedHeight(h)


# ---------------------------------------------------------------- markdown
class MarkdownView(QTextBrowser):
    """Auto-height rendered markdown (no inner scrolling)."""

    def __init__(self, md: str) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setOpenLinks(False)
        self.setStyleSheet("QTextBrowser{background:transparent}")
        self.viewport().setAutoFillBackground(False)
        self.document().setDocumentMargin(2)
        d = is_dark()
        self.document().setDefaultStyleSheet(
            f"code,pre{{font-family:'{mono_font().family()}';background:{'#2a2f38' if d else '#eceae4'};}}"
            f"blockquote{{color:{'#aeb6c2' if d else '#444'};}}")
        f = self.font()
        f.setPointSize(f.pointSize() + 2)
        self.setFont(f)
        self.setMarkdown(md)
        self.document().documentLayout().documentSizeChanged.connect(self._fit)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _fit(self, size) -> None:
        self.setFixedHeight(int(size.height()) + 6)

    def resizeEvent(self, e) -> None:
        super().resizeEvent(e)
        self.document().setTextWidth(self.viewport().width())

    def wheelEvent(self, e) -> None:  # let the surrounding scroll area handle scrolling
        e.ignore()


FENCE = re.compile(r"^```(\w*)\s*$")


def split_markdown(md: str) -> list[tuple[str, str]]:
    """-> [('md', text) | ('py', code)] — runnable python blocks are split out."""
    out: list[tuple[str, str]] = []
    buf: list[str] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m:
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            body = "\n".join(lines[i + 1:j])
            if m.group(1) == "python" and "# no-run" not in body:
                if buf:
                    out.append(("md", "\n".join(buf)))
                    buf = []
                out.append(("py", body))
            else:
                buf.extend(lines[i:j + 1])
            i = j + 1
        else:
            buf.append(lines[i])
            i += 1
    if buf:
        out.append(("md", "\n".join(buf)))
    return out


class CodeBlock(QFrame):
    """An editable, runnable Python example."""

    def __init__(self, code: str) -> None:
        super().__init__()
        self.original = code
        self.setFrameShape(QFrame.Shape.StyledPanel)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(6, 6, 6, 6)
        self.ed = CodeEditor(code)
        self.ed.fit_height()
        self.ed.submit.connect(self.run)
        self.ed.textChanged.connect(self.ed.fit_height)
        bar = QHBoxLayout()
        self.btn = QPushButton("▶ Run")
        self.btn.clicked.connect(self.run)
        reset = QPushButton("Reset")
        reset.clicked.connect(lambda: self.ed.setPlainText(self.original))
        hint = QPushButton("")
        hint.setVisible(False)
        bar.addWidget(self.btn)
        bar.addWidget(reset)
        bar.addStretch(1)
        tip = QPushButton("editable")
        tip.setFlat(True)
        tip.setEnabled(False)
        bar.addWidget(tip)
        self.out = QPlainTextEdit()
        self.out.setReadOnly(True)
        self.out.setFont(mono_font(12))
        self.out.setVisible(False)
        lay.addWidget(self.ed)
        lay.addLayout(bar)
        lay.addWidget(self.out)

    def run(self) -> None:
        if not self.btn.isEnabled():  # already running
            return
        self.btn.setEnabled(False)
        run_async(runner.run_scratch, self._done, self.ed.toPlainText())

    def _done(self, res: dict) -> None:
        self.btn.setEnabled(True)
        self.out.setVisible(True)
        self.out.setPlainText(res["output"] or "(no output)")
        n = min(14, max(2, self.out.document().blockCount()))
        self.out.setFixedHeight(self.out.fontMetrics().lineSpacing() * n + 14)
        self.out.setStyleSheet("border-left:3px solid " + ("#4cc27f" if res["ok"] else "#ef7a7a"))


def build_content(md: str, runnable: bool = True) -> QWidget:
    """Render markdown into a column of native widgets."""
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(8)
    segs = split_markdown(md) if runnable else [("md", md)]
    for kind, text in segs:
        lay.addWidget(CodeBlock(text) if kind == "py" else MarkdownView(text))
    return w
