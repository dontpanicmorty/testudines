"""Native desktop shell: main window, navigation sidebar, page stack."""
from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                               QMainWindow, QStackedWidget, QVBoxLayout, QWidget)

from .paths import ASSETS_DIR
from .service import Service
from .ui_pages import (ExercisePage, LessonPage, MapPage, ReferencePage, ReviewPage, ScratchPage,
                       TodayPage)

NAV = ["Today", "Curriculum", "Review", "Scratchpad", "Reference"]


class MainWindow(QMainWindow):
    def __init__(self, svc: Service) -> None:
        super().__init__()
        self.svc = svc
        self.setWindowTitle("Py Dojo")
        self.resize(1360, 880)
        self.setMinimumSize(1000, 680)

        self.side = QListWidget()
        self.side.setFixedWidth(190)
        self.side.setStyleSheet("QListWidget{font-size:15px;border:none;padding-top:10px}"
                                "QListWidget::item{padding:9px 14px;border-radius:8px;margin:1px 8px}"
                                "QListWidget::item:selected{background:palette(highlight);color:palette(highlighted-text)}")
        for n in NAV:
            self.side.addItem(QListWidgetItem(n))
        self.foot = QLabel("")
        self.foot.setStyleSheet("color:#8a919c;padding:10px 16px")
        side = QWidget()
        sl = QVBoxLayout(side)
        sl.setContentsMargins(0, 8, 0, 0)
        title = QLabel("Py Dojo")
        f = title.font()
        f.setPointSize(19)
        f.setBold(True)
        title.setFont(f)
        title.setContentsMargins(18, 6, 0, 4)
        sl.addWidget(title)
        sl.addWidget(self.side, 1)
        sl.addWidget(self.foot)

        self.stack = QStackedWidget()
        self.today, self.map = TodayPage(self), MapPage(self)
        self.lesson, self.exercise = LessonPage(self), ExercisePage(self)
        self.review, self.scratch, self.ref = ReviewPage(self), ScratchPage(self), ReferencePage(self)
        for p in (self.today, self.map, self.lesson, self.exercise, self.review, self.scratch, self.ref):
            self.stack.addWidget(p)

        root = QWidget()
        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        h.addWidget(side)
        h.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.side.currentRowChanged.connect(self._nav)

        for i, n in enumerate(NAV):
            a = QAction(n, self)
            a.setShortcut(QKeySequence(f"Ctrl+{i + 1}"))
            a.triggered.connect(lambda _=False, i=i: self.side.setCurrentRow(i))
            self.addAction(a)
        self.side.setCurrentRow(0)

    # navigation ---------------------------------------------------------
    def _nav(self, row: int) -> None:
        {0: self.go_today, 1: self.go_map, 2: self.go_review, 3: self.go_scratch, 4: self.go_reference}[row]()

    def _select(self, row: int | None) -> None:
        self.side.blockSignals(True)
        if row is None:
            self.side.clearSelection()
            self.side.setCurrentRow(-1)
        else:
            self.side.setCurrentRow(row)
        self.side.blockSignals(False)

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
        t = self.svc.today()
        due = t["cards_due"] + t["redo_due"]
        self.side.item(2).setText(f"Review  ({due})" if due else "Review")
        self.foot.setText(f"🔥 {t['streak']}-day streak")


def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Py Dojo")
    app.setStyle("Fusion")
    icon = ASSETS_DIR / "icon.png"
    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))
    win = MainWindow(Service())
    win.show()
    return app.exec()
