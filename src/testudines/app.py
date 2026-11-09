"""Native desktop shell: who's practicing, the SQL and Python sections, navigation, page stack."""
from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QButtonGroup, QDialog, QHBoxLayout, QLabel, QLineEdit,
                               QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton,
                               QStackedWidget, QVBoxLayout, QWidget)

from . import users
from .content import Index
from .paths import ASSETS_DIR
from .service import Service
from .sql_content import SqlIndex
from .sql_pages import SqlExercisePage, SqlHomePage, export_progress, import_progress
from .sql_service import SqlService
from .ui_pages import (ExercisePage, LessonPage, MapPage, ReferencePage, ReviewPage, ScratchPage,
                       TodayPage)

APP_NAME = "Testudines"
SECTIONS = ("sql", "python")
NAV = {"sql": ["Home", "Exercise"],
       "python": ["Today", "Curriculum", "Review", "Scratchpad", "Reference"]}


class UserDialog(QDialog):
    """Who's practicing? Pick a name, or add a new one. Each person's progress is kept separately."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Who's practicing?")
        self.setMinimumWidth(380)
        self.chosen: str | None = None
        v = QVBoxLayout(self)
        title = QLabel("Who's practicing?")
        f = title.font()
        f.setPointSize(18)
        f.setBold(True)
        title.setFont(f)
        v.addWidget(title)
        for name in users.users():
            b = QPushButton(name)
            b.clicked.connect(lambda _=False, n=name: self._pick(n))
            v.addWidget(b)
        row = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("New name")
        self.name.returnPressed.connect(self._add)
        add = QPushButton("Add")
        add.clicked.connect(self._add)
        row.addWidget(self.name, 1)
        row.addWidget(add)
        v.addLayout(row)

    def _pick(self, name: str) -> None:
        self.chosen = name
        self.accept()

    def _add(self) -> None:
        try:
            self._pick(users.add(self.name.text()))
        except ValueError as exc:
            QMessageBox.warning(self, "Who's practicing?", str(exc))


class MainWindow(QMainWindow):
    def __init__(self, user: str, py_index: Index | None = None, sql_index: SqlIndex | None = None) -> None:
        super().__init__()
        self.py_index = py_index or Index()
        self.sql_index = sql_index or SqlIndex()
        self.setWindowTitle(APP_NAME)
        self.resize(1360, 880)
        self.setMinimumSize(1000, 680)
        self.section = users.settings().get("section", "sql")
        if self.section not in SECTIONS:
            self.section = "sql"

        # sidebar: app name, who's practicing, the two sections, that section's pages
        side = QWidget()
        side.setFixedWidth(200)
        sl = QVBoxLayout(side)
        sl.setContentsMargins(0, 8, 0, 0)
        title = QLabel(APP_NAME)
        f = title.font()
        f.setPointSize(19)
        f.setBold(True)
        title.setFont(f)
        title.setContentsMargins(18, 6, 0, 0)
        sl.addWidget(title)
        who = QHBoxLayout()
        who.setContentsMargins(18, 0, 10, 4)
        self.user_label = QLabel("")
        self.user_label.setStyleSheet("color:#8a919c")
        switch = QPushButton("Switch user")
        switch.setFlat(True)
        switch.setStyleSheet("color:#8a919c;text-decoration:underline")
        switch.clicked.connect(self.switch_user)
        who.addWidget(self.user_label, 1)
        who.addWidget(switch)
        sl.addLayout(who)
        tabs = QHBoxLayout()
        tabs.setContentsMargins(12, 4, 12, 6)
        self.section_buttons = QButtonGroup(self)
        for name in SECTIONS:
            b = QPushButton("SQL" if name == "sql" else "Python")
            b.setCheckable(True)
            b.clicked.connect(lambda _=False, n=name: self.set_section(n))
            self.section_buttons.addButton(b)
            tabs.addWidget(b)
            setattr(self, f"{name}_button", b)
        sl.addLayout(tabs)
        self.side = QListWidget()
        self.side.setStyleSheet("QListWidget{font-size:15px;border:none;padding-top:4px}"
                                "QListWidget::item{padding:9px 14px;border-radius:8px;margin:1px 8px}"
                                "QListWidget::item:selected{background:palette(highlight);color:palette(highlighted-text)}")
        self.side.currentRowChanged.connect(self._nav)
        self.foot = QLabel("")
        self.foot.setStyleSheet("color:#8a919c;padding:10px 16px")
        sl.addWidget(self.side, 1)
        sl.addWidget(self.foot)

        self.stack = QStackedWidget()
        root = QWidget()
        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        h.addWidget(side)
        h.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        for i in range(5):
            a = QAction(f"page {i + 1}", self)
            a.setShortcut(QKeySequence(f"Ctrl+{i + 1}"))
            a.triggered.connect(lambda _=False, i=i: self.side.setCurrentRow(i) if i < self.side.count() else None)
            self.addAction(a)
        self.set_user(user)

    # ---- who's practicing
    def set_user(self, name: str) -> None:
        """Open a user's progress and rebuild every page on it."""
        self.user = name
        self.user_dir = users.folder(name)
        users.save_setting("last_user", name)
        self.db = users.open_db(name)
        self.svc = Service(self.db, self.py_index)
        self.sql = SqlService(self.db, self.sql_index)
        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()
        self.today, self.map = TodayPage(self), MapPage(self)
        self.lesson, self.exercise = LessonPage(self), ExercisePage(self)
        self.review, self.scratch, self.ref = ReviewPage(self), ScratchPage(self), ReferencePage(self)
        self.sql_home, self.sql_exercise = SqlHomePage(self), SqlExercisePage(self)
        for p in (self.today, self.map, self.lesson, self.exercise, self.review, self.scratch, self.ref,
                  self.sql_home, self.sql_exercise):
            self.stack.addWidget(p)
        self.user_label.setText(name)
        self.set_section(self.section)

    def switch_user(self) -> None:
        self.sql_exercise._save()
        dlg = UserDialog(self)
        if dlg.exec() and dlg.chosen:
            self.set_user(dlg.chosen)

    # ---- sections and navigation
    def set_section(self, section: str) -> None:
        self.section = section
        users.save_setting("section", section)
        getattr(self, f"{section}_button").setChecked(True)
        self.side.blockSignals(True)
        self.side.clear()
        for n in NAV[section]:
            self.side.addItem(QListWidgetItem(n))
        self.side.blockSignals(False)
        if section == "sql":
            self.go_sql_home()
        else:
            self.go_today()

    def _nav(self, row: int) -> None:
        if row < 0:
            return
        if self.section == "sql":
            (self.go_sql_home if row == 0 else self.go_sql_exercise)()
        else:
            {0: self.go_today, 1: self.go_map, 2: self.go_review, 3: self.go_scratch, 4: self.go_reference}[row]()

    def _select(self, row: int | None) -> None:
        self.side.blockSignals(True)
        if row is None:
            self.side.clearSelection()
            self.side.setCurrentRow(-1)
        else:
            self.side.setCurrentRow(row)
        self.side.blockSignals(False)

    # SQL
    def go_sql_home(self):
        self.sql_exercise._save()
        self._select(0); self.sql_home.refresh(); self.stack.setCurrentWidget(self.sql_home); self.refresh_side()

    def go_sql_exercise(self):
        if self.sql_exercise.session is None:
            self.sql_start("track")
            return
        self._select(1); self.stack.setCurrentWidget(self.sql_exercise)

    def sql_start(self, mode: str, difficulties=None, count=None) -> None:
        try:
            session = self.sql.start(mode, difficulties, count)
        except ValueError as exc:
            QMessageBox.information(self, APP_NAME, str(exc))
            return
        self._open_sql(session)

    def sql_resume(self, mode: str) -> None:
        session = self.sql.saved(mode)
        if session:
            self._open_sql(session)

    def _open_sql(self, session: dict) -> None:
        self._select(1)
        self.sql_exercise.open_session(session)
        self.stack.setCurrentWidget(self.sql_exercise)

    def sql_export(self) -> None:
        export_progress(self, self.sql)

    def sql_import(self) -> None:
        if import_progress(self, self.sql) is not None:
            self.go_sql_home()

    # Python
    def go_today(self):
        self._select(0); self.today.refresh(); self.stack.setCurrentWidget(self.today); self.refresh_side()

    def go_map(self):
        self._select(1); self.map.refresh(); self.stack.setCurrentWidget(self.map)

    def go_review(self):
        self._select(2); self.review.start(); self.stack.setCurrentWidget(self.review)

    def go_scratch(self):
        self._select(3); self.stack.setCurrentWidget(self.scratch)

    def go_reference(self):
        self._select(4); self.ref.refresh(); self.stack.setCurrentWidget(self.ref)

    def go_lesson(self, lid: str):
        self._select(1); self.lesson.show_lesson(lid); self.stack.setCurrentWidget(self.lesson)

    def go_exercise(self, eid: str, redo: bool = False):
        self._select(1); self.exercise.show_exercise(eid, redo); self.stack.setCurrentWidget(self.exercise)

    def refresh_side(self) -> None:
        if self.section == "python":
            t = self.svc.today()
            due = t["cards_due"] + t["redo_due"]
            self.side.item(2).setText(f"Review  ({due})" if due else "Review")
            self.foot.setText(f"🔥 {t['streak']}-day streak")
        else:
            done, total = self.sql.track_done()
            self.foot.setText(f"Track {done}/{total}  ·  🔥 {self.db.streak()}-day streak")
            self.foot.setWordWrap(True)

    def closeEvent(self, e) -> None:
        self.sql_exercise._save()
        super().closeEvent(e)


def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")
    icon = ASSETS_DIR / "icon.png"
    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))
    user = users.last_user()
    if user is None:
        dlg = UserDialog()
        if not dlg.exec() or not dlg.chosen:
            return 0
        user = dlg.chosen
    win = MainWindow(user)
    win.show()
    return app.exec()
