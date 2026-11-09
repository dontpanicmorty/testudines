"""The SQL section's screens: where to start (the home screen) and working an exercise."""
from __future__ import annotations

import json
import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QFileDialog, QFrame, QGridLayout, QHBoxLayout,
                               QHeaderView, QLabel, QListWidget, QListWidgetItem, QMessageBox,
                               QPlainTextEdit, QProgressBar, QPushButton, QScrollArea, QSpinBox, QSplitter,
                               QStackedLayout, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from . import sql_grader
from .sql_content import DIFFICULTIES
from .ui_pages import card, heading, muted, scrolled
from .ui_widgets import CHECK_KEYS, RUN_KEYS, CodeEditor, MarkdownView, mono_font, run_async

MODE_NAMES = {"track": "Guided Track", "practice": "Practice Session", "randomizer": "Randomizer"}


SHOW_ROWS = 1_000  # rows put in a results table; more would slow the window for no benefit


def fill_table(table: QTableWidget, columns: list[str], rows: list[tuple]) -> None:
    rows = rows[:SHOW_ROWS]
    table.clear()
    table.setColumnCount(len(columns))
    table.setRowCount(len(rows))
    table.setHorizontalHeaderLabels(columns)
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            item = QTableWidgetItem("NULL" if v is None else sql_grader.normalize(v))
            if v is None:
                item.setForeground(Qt.GlobalColor.gray)
            table.setItem(r, c, item)
    table.resizeColumnsToContents()


def data_table() -> QTableWidget:
    t = QTableWidget()
    t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    t.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)
    t.verticalHeader().setVisible(False)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    t.setFont(mono_font(12))
    t.setAlternatingRowColors(True)
    return t


def clock(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


class SqlHomePage(QWidget):
    """Choose what to work on: the guided track, a Practice Session, quick difficulty, or the Randomizer."""

    def __init__(self, win) -> None:
        super().__init__()
        self.win = win
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)

    @property
    def sql(self):
        return self.win.sql

    def refresh(self) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        w = QWidget()
        v = QVBoxLayout(w)
        v.setSpacing(12)
        v.addWidget(heading("SQL"))
        v.addWidget(muted(f"{len(self.sql.idx.all)} exercises graded by a real database engine (DuckDB) on this "
                          "computer. Any correct query passes, not just one exact answer."))

        # guided track
        done, total = self.sql.track_done()
        f, l = card()
        l.addWidget(heading("Guided Track", 15))
        l.addWidget(QLabel(f"{len(self.sql.idx.lessons)} lessons, {total} exercises, easy to hard, in order."))
        bar = QProgressBar()
        bar.setRange(0, total)
        bar.setValue(done)
        bar.setFormat(f"{done} / {total} complete")
        l.addWidget(bar)
        b = QPushButton("Continue the track" if done or self.sql.db.state_get("last_track") else "Start the track")
        b.setDefault(True)
        b.clicked.connect(lambda: self.win.sql_start("track"))
        l.addWidget(b, 0, Qt.AlignmentFlag.AlignLeft)
        v.addWidget(f)

        # practice session
        f, l = card()
        l.addWidget(heading("Practice Session", 15))
        l.addWidget(QLabel("Choose difficulties and how many, from all exercises."))
        row = QHBoxLayout()
        self.diff_boxes = {}
        for d in DIFFICULTIES:
            box = QCheckBox(d.capitalize())
            box.setChecked(True)
            box.toggled.connect(self._pool_changed)
            self.diff_boxes[d] = box
            row.addWidget(box)
        row.addSpacing(16)
        row.addWidget(QLabel("How many:"))
        self.count = QSpinBox()
        self.count.setRange(1, len(self.sql.idx.all))
        self.count.setValue(10)
        row.addWidget(self.count)
        row.addStretch(1)
        l.addLayout(row)
        self.pool_label = muted("")
        l.addWidget(self.pool_label)
        row = QHBoxLayout()
        self.start_btn = QPushButton("Start session")
        self.start_btn.clicked.connect(self._start_practice)
        row.addWidget(self.start_btn)
        saved = self.sql.saved("practice")
        if saved:
            r = QPushButton(f"Resume session ({len(saved['queue'])} exercises)")
            r.clicked.connect(lambda: self.win.sql_resume("practice"))
            row.addWidget(r)
        row.addStretch(1)
        l.addLayout(row)
        quick = QHBoxLayout()
        quick.addWidget(QLabel("Or every exercise of one difficulty:"))
        for d in DIFFICULTIES:
            q = QPushButton(d.capitalize())
            q.clicked.connect(lambda _=False, d=d: self.win.sql_start("practice", [d], None))
            quick.addWidget(q)
        quick.addStretch(1)
        l.addLayout(quick)
        v.addWidget(f)
        self._pool_changed()

        # randomizer
        f, l = card()
        l.addWidget(heading("Randomizer", 15))
        l.addWidget(QLabel("A random set from all exercises, with difficulty hidden and the exercise list out of sight."))
        row = QHBoxLayout()
        row.addWidget(QLabel("How many:"))
        self.rcount = QSpinBox()
        self.rcount.setRange(1, len(self.sql.idx.all))
        self.rcount.setValue(10)
        row.addWidget(self.rcount)
        go = QPushButton("Start randomizer")
        go.clicked.connect(lambda: self.win.sql_start("randomizer", None, self.rcount.value()))
        row.addWidget(go)
        saved = self.sql.saved("randomizer")
        if saved:
            r = QPushButton(f"Resume randomizer ({len(saved['queue'])} exercises)")
            r.clicked.connect(lambda: self.win.sql_resume("randomizer"))
            row.addWidget(r)
        row.addStretch(1)
        l.addLayout(row)
        v.addWidget(f)

        # progress file
        f, l = card()
        l.addWidget(heading("Progress", 15))
        l.addWidget(QLabel("Save your SQL progress to a file, or load one (a SQL Dojo export works too)."))
        row = QHBoxLayout()
        ex = QPushButton("Export…")
        ex.clicked.connect(self.win.sql_export)
        im = QPushButton("Import…")
        im.clicked.connect(self.win.sql_import)
        row.addWidget(ex)
        row.addWidget(im)
        row.addStretch(1)
        l.addLayout(row)
        v.addWidget(f)
        v.addStretch(1)
        self.root.addWidget(scrolled(w))

    def _diffs(self) -> list[str]:
        return [d for d, box in self.diff_boxes.items() if box.isChecked()]

    def _pool_changed(self) -> None:
        n = len(self.sql.pool(self._diffs()))
        self.count.setMaximum(max(1, n))
        self.pool_label.setText(f"{n} exercise(s) match this selection." if n else "No exercises match this selection.")
        self.start_btn.setEnabled(n > 0)

    def _start_practice(self) -> None:
        self.win.sql_start("practice", self._diffs(), self.count.value())


class SqlExercisePage(QWidget):
    """Working one exercise of the current queue."""

    def __init__(self, win) -> None:
        super().__init__()
        self.win = win
        self.session: dict | None = None
        self.eid: str | None = None
        self.paused = False
        self.module_seconds = 0.0   # this exercise, since it was opened (resets each launch)
        self.total_seconds = 0.0    # this session of the app
        self.tick_at = time.monotonic()
        self.layers = QStackedLayout(self)
        self.work = QWidget()
        self.work_layout = QVBoxLayout(self.work)
        self.work_layout.setContentsMargins(16, 10, 16, 12)
        self.layers.addWidget(self.work)
        self.layers.addWidget(self._pause_screen())
        self.ticker = QTimer(self)
        self.ticker.timeout.connect(self._tick)
        self.ticker.start(1000)
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self._save)
        QShortcut(QKeySequence("Escape"), self, activated=self.resume)

    @property
    def sql(self):
        return self.win.sql

    # ---- the queue
    def open_session(self, session: dict) -> None:
        self.session = session
        self.show_exercise(session["current"])

    def show_exercise(self, eid: str) -> None:
        if self.eid and self.eid != eid:
            self._save()
        self.eid = eid
        self.module_seconds = 0.0
        self.sql.remember(self.session, eid)
        e = self.sql.exercise(eid)
        self.e = e
        randomizer = self.session["mode"] == "randomizer"
        while self.work_layout.count():
            it = self.work_layout.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
            elif it.layout():
                self._clear(it.layout())

        # top bar: where you are, timers, pause
        top = QHBoxLayout()
        q = self.session["queue"]
        pos = q.index(eid) + 1
        label = MODE_NAMES[self.session["mode"]] + (f" — {len(q)} exercises" if self.session["mode"] != "track" else "")
        top.addWidget(QLabel(f"<b>{label}</b>   ·   {pos} of {len(q)}"))
        top.addStretch(1)
        self.timer_label = QLabel("")
        self.total_label = QLabel("")
        for lab in (self.timer_label, self.total_label):
            lab.setStyleSheet("color:#8a919c")
            top.addWidget(lab)
        self.show_timer = QPushButton("")
        self.show_timer.setFlat(True)
        self.show_timer.clicked.connect(lambda: self._toggle_setting("show_timer", True))
        self.show_total = QPushButton("")
        self.show_total.setFlat(True)
        self.show_total.clicked.connect(lambda: self._toggle_setting("show_total_timer", False))
        top.addWidget(self.show_timer)
        top.addWidget(self.show_total)
        pause = QPushButton("Pause")
        pause.clicked.connect(self.pause)
        top.addWidget(pause)
        if self.session["mode"] != "track":
            end = QPushButton("End session")
            end.clicked.connect(self._end)
            top.addWidget(end)
        home = QPushButton("Home")
        home.clicked.connect(self.win.go_sql_home)
        top.addWidget(home)
        self.work_layout.addLayout(top)
        self._timer_labels()

        split = QSplitter(Qt.Orientation.Horizontal)
        # the queue (hidden in the Randomizer, so it gives nothing away)
        self.queue_list = QListWidget()
        done = self.sql.completed()
        for i, qid in enumerate(q, 1):
            x = self.sql.idx.by_id[qid]
            item = QListWidgetItem(f"{'✓ ' if qid in done else '   '}{qid if x.track else i}  {x.title}")
            item.setData(Qt.ItemDataRole.UserRole, qid)
            self.queue_list.addItem(item)
        self.queue_list.setCurrentRow(pos - 1)
        self.queue_list.itemClicked.connect(lambda it: self.show_exercise(it.data(Qt.ItemDataRole.UserRole)))
        self.queue_list.setVisible(not randomizer)
        self.queue_list.setMinimumWidth(240)
        self.queue_list.setWordWrap(False)
        self.queue_list.setTextElideMode(Qt.TextElideMode.ElideRight)
        split.addWidget(self.queue_list)

        # the exercise: prompt, sample tables, help
        left = QWidget()
        lv = QVBoxLayout(left)
        title = e["title"] + ("   ✓ solved" if e["completed"] else "")
        lv.addWidget(heading(title, 18))
        if not randomizer:
            lv.addWidget(muted(f"{e['group']}   ·   {e['difficulty'].capitalize()}   ·   {e['concept']}"))
        lv.addWidget(MarkdownView(e["prompt"]))
        lv.addWidget(heading("Sample tables", 13))
        for t in self.sql.sample_tables(eid):
            lv.addWidget(QLabel(f"<b>{t['name']}</b>" + (f"   <span style='color:#8a919c'>showing {len(t['rows'])} "
                                                       f"of {t['total']} rows</span>" if t["total"] > len(t["rows"]) else "")))
            table = data_table()
            fill_table(table, t["columns"], t["rows"])
            table.setFixedHeight(min(260, 30 + 24 * max(1, len(t["rows"]))))
            lv.addWidget(table)
        row = QHBoxLayout()
        self.hint_btn = QPushButton("Show hint")
        self.hint_btn.setEnabled(bool(e["hint"]))
        self.hint_btn.clicked.connect(self._hint)
        self.sol_btn = QPushButton("Show solution")
        self.sol_btn.clicked.connect(self._solution)
        self.sol_btn.setEnabled(e["solution_available"])
        self.sol_btn.setToolTip("Available after 3 checks that don't pass, or once solved.")
        rs = QPushButton("Reset")
        rs.clicked.connect(self._reset)
        for b in (self.hint_btn, self.sol_btn, rs):
            row.addWidget(b)
        row.addStretch(1)
        lv.addLayout(row)
        self.help_box = QVBoxLayout()
        lv.addLayout(self.help_box)
        lv.addStretch(1)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(left)
        split.addWidget(scroll)

        # the editor and results
        right = QWidget()
        rv = QVBoxLayout(right)
        self.editor = CodeEditor(e["code"], language="sql")
        self.editor.submit.connect(self.run)
        self.editor.check.connect(self.check)
        self.editor.textChanged.connect(lambda: self.save_timer.start(800))
        rv.addWidget(self.editor, 3)
        bar = QHBoxLayout()
        self.run_btn = QPushButton(f"▶ Run   {RUN_KEYS}")
        self.check_btn = QPushButton(f"✓ Check answer   {CHECK_KEYS}")
        self.check_btn.setDefault(True)
        self.run_btn.clicked.connect(self.run)
        self.check_btn.clicked.connect(self.check)
        prev_b = QPushButton("← Previous")
        next_b = QPushButton("Next →")
        prev_b.setEnabled(pos > 1)
        next_b.setEnabled(pos < len(q))
        prev_b.clicked.connect(lambda: self._step(-1))
        next_b.clicked.connect(lambda: self._step(1))
        for b in (self.run_btn, self.check_btn):
            bar.addWidget(b)
        bar.addStretch(1)
        bar.addWidget(prev_b)
        bar.addWidget(next_b)
        rv.addLayout(bar)
        self.feedback = QLabel("")
        self.feedback.setWordWrap(True)
        self.feedback.setVisible(False)
        rv.addWidget(self.feedback)
        self.results = data_table()
        self.error = QPlainTextEdit()
        self.error.setReadOnly(True)
        self.error.setFont(mono_font(12))
        self.error.setVisible(False)
        rv.addWidget(self.results, 2)
        rv.addWidget(self.error, 2)
        self.result_note = muted("Results appear here.")
        rv.addWidget(self.result_note)
        split.addWidget(right)
        split.setSizes([270 if not randomizer else 0, 470, 600])
        split.setChildrenCollapsible(False) if not randomizer else None
        self.work_layout.addWidget(split, 1)
        self.layers.setCurrentWidget(self.work)
        self.editor.setFocus()

    def _clear(self, layout) -> None:
        while layout.count():
            it = layout.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
            elif it.layout():
                self._clear(it.layout())

    def _step(self, delta: int) -> None:
        q = self.session["queue"]
        i = q.index(self.eid) + delta
        if 0 <= i < len(q):
            self.show_exercise(q[i])

    def _end(self) -> None:
        self._save()
        self.sql.end(self.session["mode"])
        self.session = None
        self.eid = None
        self.win.go_sql_home()

    # ---- running and checking
    def _save(self) -> None:
        if self.eid and hasattr(self, "editor"):
            try:
                self.sql.save_code(self.eid, self.editor.toPlainText())
            except RuntimeError:  # the editor was already deleted
                pass

    def _busy(self, on: bool) -> None:
        self.run_btn.setEnabled(not on)
        self.check_btn.setEnabled(not on)

    def _show_result(self, result: sql_grader.Result) -> None:
        if result.error:
            self.results.setVisible(False)
            self.error.setVisible(True)
            self.error.setPlainText(result.error)
            self.result_note.setText("")
            return
        self.error.setVisible(False)
        self.results.setVisible(True)
        fill_table(self.results, result.columns, result.rows)
        n = len(result.rows)
        if result.truncated:
            note = f"More than {n:,} rows; showing the first {SHOW_ROWS:,}"
        elif n > SHOW_ROWS:
            note = f"{n:,} rows; showing the first {SHOW_ROWS:,}"
        else:
            note = f"{n} row(s)"
        self.result_note.setText(note)

    def run(self) -> None:
        if self.paused:
            return
        if not self.run_btn.isEnabled():  # already running (the shortcut keys bypass a greyed-out button)
            return
        self._save()
        self._busy(True)
        self.feedback.setVisible(False)
        run_async(self.sql.run, self._ran, self.eid, self.editor.toPlainText())

    def _ran(self, result) -> None:
        self._busy(False)
        if isinstance(result, dict):  # an internal error from run_async
            result = sql_grader.Result(error=result.get("output", "Something went wrong."))
        self._show_result(result)

    def check(self) -> None:
        if self.paused:
            return
        if not self.run_btn.isEnabled():  # already running (the shortcut keys bypass a greyed-out button)
            return
        self._busy(True)
        run_async(self.sql.check, self._checked, self.eid, self.editor.toPlainText())

    def _checked(self, res: dict) -> None:
        self._busy(False)
        if "result" not in res:
            res = {"passed": False, "result": sql_grader.Result(error=res.get("output", "")), "message": res.get("output", "")}
        self._show_result(res["result"])
        ok = res["passed"]
        self.feedback.setVisible(True)
        self.feedback.setText(res["message"])
        color = "#1f8a4c" if ok else "#c23b3b"
        self.feedback.setStyleSheet(f"background:{color}33;border:1px solid {color};border-radius:6px;padding:8px")
        self.sol_btn.setEnabled(bool(res.get("solution_available")))
        if ok:
            self.e["completed"] = True  # the clock stops the moment an answer is confirmed
            item = self.queue_list.currentItem()
            if item and not item.text().startswith("✓"):
                item.setText("✓ " + item.text()[3:])
        self.win.refresh_side()

    # ---- help
    def _hint(self) -> None:
        f, l = card()
        l.addWidget(QLabel("<b>Hint</b>"))
        t = QLabel(self.e["hint"])
        t.setWordWrap(True)
        l.addWidget(t)
        self.help_box.addWidget(f)
        self.hint_btn.setEnabled(False)

    def _solution(self) -> None:
        f, l = card()
        l.addWidget(QLabel("<b>One reference answer</b> (any query with the same result passes)"))
        ed = CodeEditor(self.sql.solution(self.eid), readonly=True, language="sql")
        ed.fit_height()
        l.addWidget(ed)
        self.help_box.addWidget(f)
        self.sol_btn.setEnabled(False)

    def _reset(self) -> None:
        if QMessageBox.question(self, "Reset", "Discard your query and restore the starter?") \
                != QMessageBox.StandardButton.Yes:
            return
        self.editor.setPlainText(self.sql.reset(self.eid))
        self.feedback.setVisible(False)

    # ---- timers and pause
    def _toggle_setting(self, key: str, default: bool) -> None:
        self.sql.set_setting(key, not self.sql.setting(key, default))
        self._timer_labels()

    def _timer_labels(self) -> None:
        if not hasattr(self, "timer_label"):
            return
        show, total = self.sql.setting("show_timer", True), self.sql.setting("show_total_timer", False)
        self.timer_label.setText(f"⏱ {clock(self.module_seconds)}" if show else "")
        self.total_label.setText(f"Σ {clock(self.total_seconds)}" if total else "")
        self.show_timer.setText("Hide timer" if show else "Show timer")
        self.show_total.setText("Hide total" if total else "Show total timer")

    def _tick(self) -> None:
        now = time.monotonic()
        step, self.tick_at = now - self.tick_at, now
        counting = (self.eid is not None and not self.paused and self.isVisible()
                    and self.window().isActiveWindow() and not self.e.get("completed", False))
        if counting:
            self.module_seconds += step
            self.total_seconds += step
        try:
            self._timer_labels()
        except RuntimeError:
            pass

    def pause(self) -> None:
        if self.eid is None:
            return
        self._save()
        self.paused = True
        self.layers.setCurrentIndex(1)

    def resume(self) -> None:
        if self.paused:
            self.paused = False
            self.tick_at = time.monotonic()
            self.layers.setCurrentWidget(self.work)

    def _pause_screen(self) -> QWidget:
        w = QWidget()
        g = QGridLayout(w)
        box = QVBoxLayout()
        box.addWidget(heading("Paused", 26), 0, Qt.AlignmentFlag.AlignHCenter)
        box.addWidget(muted("The exercise is hidden and the timer is stopped."), 0, Qt.AlignmentFlag.AlignHCenter)
        b = QPushButton("Resume   (Esc)")
        b.clicked.connect(self.resume)
        box.addWidget(b, 0, Qt.AlignmentFlag.AlignHCenter)
        g.addLayout(box, 0, 0, Qt.AlignmentFlag.AlignCenter)
        return w


def export_progress(parent, sql) -> None:
    path, _ = QFileDialog.getSaveFileName(parent, "Export SQL progress", "testudines-sql-progress.json", "JSON (*.json)")
    if path:
        with open(path, "w") as f:
            json.dump(sql.export(), f, indent=2)


def import_progress(parent, sql) -> int | None:
    path, _ = QFileDialog.getOpenFileName(parent, "Import SQL progress", "", "JSON (*.json)")
    if not path:
        return None
    if QMessageBox.question(parent, "Import progress", "Replace your current SQL progress with this file?") \
            != QMessageBox.StandardButton.Yes:
        return None
    try:
        with open(path) as f:
            n = sql.import_progress(json.load(f))
    except (OSError, ValueError) as exc:
        QMessageBox.warning(parent, "Import progress", f"Could not import that file: {exc}")
        return None
    QMessageBox.information(parent, "Import progress", f"Imported progress for {n} exercise(s).")
    return n
