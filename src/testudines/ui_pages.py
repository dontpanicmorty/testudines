"""Pages of the desktop app. Each page is a QWidget built from the Service layer."""
from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QShortcut, QKeySequence
from PySide6.QtWidgets import (QButtonGroup, QDialog, QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                               QMessageBox, QPlainTextEdit, QPushButton, QScrollArea, QSplitter,
                               QTabWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from . import runner
from .ui_widgets import CHECK_KEYS, RUN_KEYS, CodeEditor, MarkdownView, build_content, is_dark, mono_font, run_async


def heading(text: str, size: int = 22) -> QLabel:
    l = QLabel(text)
    f = l.font()
    f.setPointSize(size)
    f.setBold(True)
    l.setFont(f)
    l.setWordWrap(True)
    return l


def muted(text: str) -> QLabel:
    l = QLabel(text)
    l.setWordWrap(True)
    l.setStyleSheet("color:#8a919c")
    return l


def scrolled(inner: QWidget, max_width: int | None = 860) -> QScrollArea:
    """Centre content in a scroll area with a readable max width."""
    host = QWidget()
    row = QHBoxLayout(host)
    row.setContentsMargins(32, 24, 32, 40)
    row.addStretch(1)
    if max_width:
        inner.setMaximumWidth(max_width)
    row.addWidget(inner, 100)
    row.addStretch(1)
    sa = QScrollArea()
    sa.setWidgetResizable(True)
    sa.setFrameShape(QFrame.Shape.NoFrame)
    sa.setWidget(host)
    return sa


def card() -> tuple[QFrame, QVBoxLayout]:
    f = QFrame()
    f.setFrameShape(QFrame.Shape.StyledPanel)
    l = QVBoxLayout(f)
    l.setContentsMargins(14, 10, 14, 12)
    return f, l


class Page(QWidget):
    def __init__(self, win) -> None:
        super().__init__()
        self.win, self.svc = win, win.svc
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)

    def set_body(self, w: QWidget) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        self.root.addWidget(w)


# ----------------------------------------------------------------------- Today
class Heatmap(QWidget):
    def __init__(self, activity: dict[str, int]) -> None:
        super().__init__()
        self.activity = activity
        self.setFixedSize(12 * 15 + 4, 7 * 15 + 4)

    def paintEvent(self, e) -> None:
        p = QPainter(self)
        today = date.today()
        start = today - timedelta(days=today.weekday() + 7 * 11)
        dark = is_dark()
        for w in range(12):
            for d in range(7):
                day = start + timedelta(days=w * 7 + d)
                if day > today:
                    continue
                n = self.activity.get(day.isoformat(), 0)
                c = QColor("#6c9cff" if dark else "#2f5fd0")
                c.setAlpha(0 if not n else 90 if n < 3 else 170 if n < 6 else 255)
                base = QColor("#2a2f38" if dark else "#dedbd3")
                p.setBrush(base)
                p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(QRectF(w * 15 + 2, d * 15 + 2, 12, 12), 2, 2)
                p.setBrush(c)
                p.drawRoundedRect(QRectF(w * 15 + 2, d * 15 + 2, 12, 12), 2, 2)


class TodayPage(Page):
    def refresh(self) -> None:
        t = self.svc.today()
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(heading("Today"))
        v.addWidget(muted("Three parts: recall what you've learned, rebuild something from memory, "
                          "then learn one new thing. 30–45 minutes."))

        def row(title: str, body: str, buttons: list[tuple[str, callable, bool]]) -> None:
            f, l = card()
            h = QHBoxLayout()
            col = QVBoxLayout()
            col.addWidget(heading(title, 15))
            b = QLabel(body)
            b.setWordWrap(True)
            col.addWidget(b)
            h.addLayout(col, 1)
            for text, fn, primary in buttons:
                btn = QPushButton(text)
                if primary:
                    btn.setDefault(True)
                btn.clicked.connect(fn)
                h.addWidget(btn)
            l.addLayout(h)
            v.addWidget(f)

        row("1 · Recall", f"{t['cards_due']} card(s) due · {t['cards_total']} in rotation" if t["cards_due"]
            else f"Nothing due · {t['cards_total']} cards in rotation",
            [("Start review", lambda: self.win.go_review(), bool(t["cards_due"]))])
        redo = t["redo"]
        row("2 · Rebuild from memory",
            ", ".join(r["title"] for r in redo) if redo else
            "No exercises due for a cold redo yet. They return 1, 3, 7, 16 days after you first solve them.",
            [(f"Redo: {r['title'][:24]}", (lambda rid=r["id"]: self.win.go_exercise(rid, redo=True)), True)
             for r in redo])
        if t["resume_lesson"]:
            row("3 · New material", "You have unfinished exercises in a lesson you started.",
                [("Continue", lambda: self.win.go_lesson(t["resume_lesson"]), True)])
        elif t["next_lesson"]:
            row("3 · New material", f"{t['path_title']} · next: {t['next_title']}",
                [("Start", lambda: self.win.go_lesson(t["next_lesson"]), True),
                 ("Change path", lambda: self.win.go_map(), False)])
        else:
            row("3 · New material", f"You've finished {t['path_title']}. Pick another path on the Curriculum page.",
                [("Change path", lambda: self.win.go_map(), False)])
        v.addWidget(heading("Last 12 weeks", 15))
        v.addWidget(Heatmap(t["activity"]))
        v.addWidget(muted(f"{t['streak']}-day streak. 25 focused minutes a day beats a weekend binge."))
        v.addStretch(1)
        self.set_body(scrolled(w))


# ----------------------------------------------------------------- Curriculum
class MapPage(Page):
    def refresh(self) -> None:
        c = self.svc.curriculum()
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(heading("Curriculum"))
        paths = self.svc.paths()
        if len(paths) > 1:
            # one button per learning path; the chosen one drives Today's new material
            row = QHBoxLayout()
            self.path_group = QButtonGroup(self)
            for p in paths:
                b = QPushButton(f"{p['title']}   ({p['done']}/{p['lessons']})")
                b.setCheckable(True)
                b.setChecked(p["id"] == c["path"])
                b.setToolTip(p["summary"])
                b.clicked.connect(lambda _=False, pid=p["id"]: self._choose_path(pid))
                self.path_group.addButton(b)
                row.addWidget(b)
            row.addStretch(1)
            v.addLayout(row)
        if c["path_summary"]:
            summary = QLabel(c["path_summary"])
            summary.setWordWrap(True)
            v.addWidget(summary)
        v.addWidget(muted("Work top to bottom. Double-click a lesson to open it. "
                          "✓ complete · ◐ started · ○ not started"))
        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        tree.setIndentation(18)
        stage_items: dict[str, QTreeWidgetItem] = {}
        for m in c["modules"]:
            si = stage_items.get(m["stage"])
            if si is None:
                si = QTreeWidgetItem(tree, [m["stage"].upper()])
                f = si.font(0)
                f.setBold(True)
                si.setFont(0, f)
                si.setFlags(Qt.ItemFlag.ItemIsEnabled)
                stage_items[m["stage"]] = si
            done = sum(l["done"] for l in m["lessons"])
            mi = QTreeWidgetItem(si, [f"{m['title']}   ({done}/{len(m['lessons'])})"])
            mi.setToolTip(0, m["summary"])
            mf = mi.font(0)
            mf.setBold(True)
            mi.setFont(0, mf)
            for l in m["lessons"]:
                mark = "✓" if l["done"] else "◐" if l["read"] else "○"
                li = QTreeWidgetItem(mi, [f"{mark}  {l['title']}   ·  {l['minutes']} min  ·  "
                                          f"{l['exercises_done']}/{l['exercises']} exercises"])
                li.setData(0, Qt.ItemDataRole.UserRole, l["id"])
        tree.expandAll()
        tree.itemActivated.connect(self._open)
        tree.itemDoubleClicked.connect(self._open)
        v.addWidget(tree, 1)
        v.setContentsMargins(32, 24, 32, 24)
        self.set_body(w)

    def _open(self, item: QTreeWidgetItem, *_):
        lid = item.data(0, Qt.ItemDataRole.UserRole)
        if lid:
            self.win.go_lesson(lid)

    def _choose_path(self, pid: str) -> None:
        self.svc.set_path(pid)
        self.refresh()


# --------------------------------------------------------------------- Lesson
class LessonPage(Page):
    def show_lesson(self, lid: str) -> None:
        l = self.svc.lesson(lid)
        self.lid, self.marked = lid, lid in self.svc.db.lessons_read()
        w = QWidget()
        v = QVBoxLayout(w)
        back = QPushButton("← Curriculum")
        back.setFlat(True)
        back.clicked.connect(self.win.go_map)
        back.setStyleSheet("text-align:left;color:#8a919c")
        v.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
        v.addWidget(muted(f"{l['minutes']} min · {len(l['exercises'])} exercises · {l['cards']} review cards"))
        v.addWidget(build_content(l["body"], runnable=True))
        v.addWidget(heading("Practice", 17))
        for e in l["exercises"]:
            b = QPushButton(f"{'✓' if e['passed'] else '○'}   {e['title']}      "
                            f"{'●' * e['difficulty']}{'○' * (3 - e['difficulty'])}")
            b.setStyleSheet("text-align:left;padding:10px 14px")
            b.clicked.connect(lambda _=False, eid=e["id"]: self.win.go_exercise(eid))
            v.addWidget(b)
        if not l["exercises"]:
            v.addWidget(muted("No exercises in this lesson."))
        nav = QHBoxLayout()
        self.mark = QPushButton("✓ Read — added to review" if self.marked else "Mark as read and add cards to review")
        self.mark.setEnabled(not self.marked)
        self.mark.clicked.connect(self._mark)
        nav.addWidget(self.mark)
        nav.addStretch(1)
        if l["prev"]:
            p = QPushButton("← Previous")
            p.clicked.connect(lambda: self.win.go_lesson(l["prev"]))
            nav.addWidget(p)
        if l["next"]:
            n = QPushButton("Next →")
            n.clicked.connect(lambda: self.win.go_lesson(l["next"]))
            nav.addWidget(n)
        v.addLayout(nav)
        v.addStretch(1)
        sa = scrolled(w)
        # auto-mark as read once the learner has scrolled through most of the lesson
        sb = sa.verticalScrollBar()
        sb.valueChanged.connect(lambda val: val > 0.85 * max(1, sb.maximum()) and self._mark())
        self.set_body(sa)

    def _mark(self) -> None:
        if self.marked:
            return
        self.marked = True
        self.svc.read_lesson(self.lid)
        self.mark.setText("✓ Read — added to review")
        self.mark.setEnabled(False)
        self.win.refresh_side()


# ------------------------------------------------------------------- Exercise
class ExercisePage(Page):
    def show_exercise(self, eid: str, redo: bool = False) -> None:
        e = self.svc.exercise(eid)
        self.eid, self.e, self.redo = eid, e, redo
        self.files = dict(e["starter"] if redo else e["files"])
        self.hint_n = 0
        split = QSplitter(Qt.Orientation.Horizontal)

        # left: prompt + help
        left = QWidget()
        lv = QVBoxLayout(left)
        back = QPushButton("← Lesson")
        back.setFlat(True)
        back.setStyleSheet("text-align:left;color:#8a919c")
        back.clicked.connect(lambda: self.win.go_lesson(e["lesson"]))
        lv.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
        lv.addWidget(heading(("↻ Redo: " if redo else "") + e["title"] + ("   ✓ solved" if e["passed"] else ""), 18))
        lv.addWidget(MarkdownView(e["prompt"]))
        row = QHBoxLayout()
        self.hint_btn = QPushButton(f"Hint ({e['n_hints']})")
        self.hint_btn.setEnabled(e["n_hints"] > 0)
        self.hint_btn.clicked.connect(self._hint)
        sol = QPushButton("Show solution")
        sol.clicked.connect(self._solution)
        rs = QPushButton("Reset")
        rs.clicked.connect(self._reset)
        for b in (self.hint_btn, sol, rs):
            row.addWidget(b)
        row.addStretch(1)
        lv.addLayout(row)
        self.hints_box = QVBoxLayout()
        lv.addLayout(self.hints_box)
        lv.addStretch(1)
        lsa = QScrollArea()
        lsa.setWidgetResizable(True)
        lsa.setFrameShape(QFrame.Shape.NoFrame)
        lsa.setWidget(left)

        # right: editors + output
        right = QWidget()
        rv = QVBoxLayout(right)
        self.tabs = QTabWidget()
        self.editors: dict[str, CodeEditor] = {}
        for name, text in self.files.items():
            ed = CodeEditor(text)
            ed.submit.connect(self.run)
            ed.check.connect(self.check)
            ed.textChanged.connect(self._changed)
            self.editors[name] = ed
            self.tabs.addTab(ed, name)
        self.tabs.tabBar().setVisible(len(self.files) > 1)
        self.tabs.setCurrentIndex(list(self.files).index(e["main"]) if e["main"] in self.files else 0)
        rv.addWidget(self.tabs, 3)
        bar = QHBoxLayout()
        self.run_btn = QPushButton(f"▶ Run   {RUN_KEYS}")
        self.check_btn = QPushButton(f"✓ Check   {CHECK_KEYS}")
        self.check_btn.setDefault(True)
        self.run_btn.clicked.connect(self.run)
        self.check_btn.clicked.connect(self.check)
        self.status = QLabel("")
        bar.addWidget(self.run_btn)
        bar.addWidget(self.check_btn)
        bar.addWidget(self.status, 1)
        rv.addLayout(bar)
        self.banner = QLabel("")
        self.banner.setWordWrap(True)
        self.banner.setVisible(False)
        rv.addWidget(self.banner)
        self.out = QPlainTextEdit()
        self.out.setReadOnly(True)
        self.out.setFont(mono_font(12))
        self.out.setPlaceholderText("Output appears here.")
        rv.addWidget(self.out, 2)

        split.addWidget(lsa)
        split.addWidget(right)
        split.setSizes([420, 760])
        split.setChildrenCollapsible(False)
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self._save)
        host = QWidget()
        hl = QVBoxLayout(host)
        hl.setContentsMargins(16, 12, 16, 12)
        hl.addWidget(split)
        self.set_body(host)

    def _collect(self) -> dict[str, str]:
        return {n: ed.toPlainText() for n, ed in self.editors.items()}

    def _changed(self) -> None:
        if not self.redo:
            self.save_timer.start(800)

    def _save(self) -> None:
        self.svc.db.save_files(self.eid, self._collect())

    def _busy(self, on: bool, msg: str = "") -> None:
        self.run_btn.setEnabled(not on)
        self.check_btn.setEnabled(not on)
        self.status.setText(msg)

    def _show(self, text: str, ok: bool) -> None:
        self.out.setPlainText(text or "(no output)")
        self.out.setStyleSheet("border-left:3px solid " + ("#4cc27f" if ok else "#ef7a7a"))

    def run(self) -> None:
        if not self.run_btn.isEnabled():  # already running (the shortcut keys bypass a greyed-out button)
            return
        self._busy(True, "running…")
        files = self._collect()
        if not self.redo:
            self.svc.db.save_files(self.eid, files)
        ex = self.svc.idx.exercises[self.eid]
        run_async(runner.run_main, self._ran, {**ex.tests(), **files}, ex.main, ex.timeout,
                  ex.memory_mb or None)

    def _ran(self, res: dict) -> None:
        self._busy(False)
        self.banner.setVisible(False)
        self._show(res["output"], res["ok"])

    def check(self) -> None:
        if not self.run_btn.isEnabled():  # already running (the shortcut keys bypass a greyed-out button)
            return
        self._busy(True, "checking…")
        files = self._collect()
        run_async(self.svc.run_check, self._checked, self.eid, files, self.redo)

    def _checked(self, res: dict) -> None:
        self._busy(False)
        ok = res["passed"]
        self._show(res["output"], ok)
        self.banner.setVisible(True)
        if ok:
            self.banner.setText("✓ All checks pass. " + ("Scheduled further out." if self.redo
                                                           else "This returns for a cold redo tomorrow."))
            self.banner.setStyleSheet("background:#1f8a4c33;border:1px solid #1f8a4c;border-radius:6px;padding:8px")
        else:
            n = res.get("n_failed") or 0
            self.banner.setText(f"{n or 'Some'} check(s) failing. Read the first error carefully.")
            self.banner.setStyleSheet("background:#c23b3b2a;border:1px solid #c23b3b;border-radius:6px;padding:8px")
        self.win.refresh_side()

    def _hint(self) -> None:
        r = self.svc.hint(self.eid, self.hint_n)
        f, l = card()
        l.addWidget(QLabel(f"<b>Hint {self.hint_n + 1}</b>"))
        t = QLabel(r["hint"])
        t.setWordWrap(True)
        l.addWidget(t)
        self.hints_box.addWidget(f)
        if self.hint_n < self.e["n_hints"] - 1:
            self.hint_n += 1
        else:
            self.hint_btn.setEnabled(False)

    def _solution(self) -> None:
        box = QMessageBox(self)
        box.setWindowTitle("Show solution?")
        box.setText("Try one more time first?")
        box.setInformativeText("Seeing the solution is fine, but you'll learn more by struggling a little.")
        keep = box.addButton("Keep trying", QMessageBox.ButtonRole.RejectRole)
        show = box.addButton("Show solution", QMessageBox.ButtonRole.AcceptRole)
        box.exec()
        if box.clickedButton() is not show:
            return
        sol = self.svc.solution(self.eid)["files"]
        dlg = QDialog(self)
        dlg.setWindowTitle("Reference solution")
        dlg.resize(760, 520)
        v = QVBoxLayout(dlg)
        tabs = QTabWidget()
        for n, t in sol.items():
            tabs.addTab(CodeEditor(t, readonly=True), n)
        v.addWidget(tabs)
        dlg.exec()

    def _reset(self) -> None:
        if QMessageBox.question(self, "Reset", "Discard your code and restore the starter?") \
                != QMessageBox.StandardButton.Yes:
            return
        files = self.svc.reset(self.eid)["files"]
        for n, t in files.items():
            if n in self.editors:
                self.editors[n].setPlainText(t)


# --------------------------------------------------------------------- Review
class ReviewPage(Page):
    def start(self) -> None:
        self.cards = self.svc.today()["cards"]
        self.i = 0
        self.total = len(self.cards)
        self._draw()

    def _draw(self) -> None:
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(heading("Review"))
        if self.i >= len(self.cards):
            f, l = card()
            l.addWidget(QLabel("Session complete. ✓" if self.total else "Nothing due right now."))
            v.addWidget(f)
            b = QPushButton("Back to Today")
            b.clicked.connect(self.win.go_today)
            v.addWidget(b, 0, Qt.AlignmentFlag.AlignLeft)
            v.addStretch(1)
            self.set_body(scrolled(w))
            self.win.refresh_side()
            return
        c = self.cards[self.i]
        v.addWidget(muted(f"{self.i + 1} / {self.total} · {c['lesson_title']}"))
        qf, ql = card()
        ql.addWidget(build_content(c["q"], runnable=False))
        v.addWidget(qf)
        self.ans = QWidget()
        av = QVBoxLayout(self.ans)
        af, al = card()
        al.addWidget(build_content(c["a"], runnable=False))
        av.addWidget(af)
        row = QHBoxLayout()
        for label, g, key in (("Again  1", "again", "1"), ("Hard  2", "hard", "2"),
                              ("Good  3", "good", "3"), ("Easy  4", "easy", "4")):
            b = QPushButton(label)
            b.clicked.connect(lambda _=False, g=g: self._grade(g))
            sc = QShortcut(QKeySequence(key), self.ans)
            sc.activated.connect(lambda g=g: self._grade(g))
            row.addWidget(b)
        av.addLayout(row)
        self.ans.setVisible(False)
        v.addWidget(self.ans)
        self.show_btn = QPushButton("Show answer   (space)")
        self.show_btn.setDefault(True)
        self.show_btn.clicked.connect(self._reveal)
        sc = QShortcut(QKeySequence("Space"), w)
        sc.activated.connect(self._reveal)
        v.addWidget(self.show_btn, 0, Qt.AlignmentFlag.AlignLeft)
        v.addWidget(muted("Say or type the answer before revealing it. The effort is what makes it stick."))
        v.addStretch(1)
        self.set_body(scrolled(w))

    def _reveal(self) -> None:
        self.ans.setVisible(True)
        self.show_btn.setVisible(False)

    def _grade(self, g: str) -> None:
        if not self.ans.isVisible():
            return
        self.svc.db.srs_grade(self.cards[self.i]["item"], g)
        self.i += 1
        self._draw()


# ------------------------------------------------------------------ Scratchpad
class ScratchPage(Page):
    def __init__(self, win) -> None:
        super().__init__(win)
        self.file = win.user_dir / "scratch.py"  # each user has their own scratch pad
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(32, 24, 32, 24)
        v.addWidget(heading("Scratchpad"))
        v.addWidget(muted("Free experimentation. Bundled datasets live in the folder named by "
                          "os.environ[\"DOJO_DATA\"]. Saved automatically, never graded."))
        default = ('import os\nfrom pathlib import Path\n\n'
                   'print(sorted(p.name for p in Path(os.environ["DOJO_DATA"]).iterdir()))\n')
        text = self.file.read_text() if self.file.exists() else default
        self.ed = CodeEditor(text)
        self.ed.submit.connect(self.run)
        self.ed.textChanged.connect(lambda: (self.file.parent.mkdir(parents=True, exist_ok=True),
                                             self.file.write_text(self.ed.toPlainText())))
        self.btn = QPushButton(f"▶ Run   {RUN_KEYS}")
        self.btn.clicked.connect(self.run)
        self.out = QPlainTextEdit()
        self.out.setReadOnly(True)
        self.out.setFont(mono_font(12))
        v.addWidget(self.ed, 3)
        v.addWidget(self.btn, 0, Qt.AlignmentFlag.AlignLeft)
        v.addWidget(self.out, 2)
        self.root.addWidget(w)

    def run(self) -> None:
        if not self.btn.isEnabled():  # already running
            return
        self.btn.setEnabled(False)
        run_async(runner.run_scratch, self._done, self.ed.toPlainText())

    def _done(self, res: dict) -> None:
        self.btn.setEnabled(True)
        self.out.setPlainText(res["output"] or "(no output)")
        self.out.setStyleSheet("border-left:3px solid " + ("#4cc27f" if res["ok"] else "#ef7a7a"))


# ------------------------------------------------------------------- Reference
class ReferencePage(Page):
    def refresh(self) -> None:
        sheets = self.svc.reference_list()
        split = QSplitter(Qt.Orientation.Horizontal)
        lst = QListWidget()
        lst.setMaximumWidth(260)
        for s in sheets:
            it = QListWidgetItem(s["title"])
            it.setData(Qt.ItemDataRole.UserRole, s["id"])
            lst.addItem(it)
        self.holder = QVBoxLayout()
        hw = QWidget()
        hw.setLayout(self.holder)
        self.holder.addWidget(muted("Cheat sheets that ship with the app. Pick one on the left."))
        self.holder.addStretch(1)
        lst.currentItemChanged.connect(lambda it, _: it and self._open(it.data(Qt.ItemDataRole.UserRole)))
        split.addWidget(lst)
        split.addWidget(hw)
        split.setSizes([240, 800])
        host = QWidget()
        hl = QVBoxLayout(host)
        hl.setContentsMargins(24, 20, 24, 20)
        hl.addWidget(heading("Reference"))
        hl.addWidget(split, 1)
        self.set_body(host)

    def _open(self, rid: str) -> None:
        while self.holder.count():
            it = self.holder.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        body = self.svc.reference_get(rid)["body"]
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setFrameShape(QFrame.Shape.NoFrame)
        inner = build_content(body, runnable=False)
        wrap = QWidget()
        wl = QVBoxLayout(wrap)
        wl.addWidget(inner)
        wl.addStretch(1)
        sa.setWidget(wrap)
        self.holder.addWidget(sa)
