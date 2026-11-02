"""Draws the app icon (assets/icon.png, 1024px) with Qt. No external art."""
import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QGuiApplication, QImage, QLinearGradient, QPainter, QPainterPath

app = QGuiApplication([])
N = 1024
img = QImage(N, N, QImage.Format.Format_ARGB32)
img.fill(Qt.GlobalColor.transparent)
p = QPainter(img)
p.setRenderHint(QPainter.RenderHint.Antialiasing)
p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
m = 64
rect = QRectF(m, m, N - 2 * m, N - 2 * m)
path = QPainterPath()
path.addRoundedRect(rect, 200, 200)
g = QLinearGradient(0, 0, N, N)
g.setColorAt(0, QColor("#1c2b4a"))
g.setColorAt(1, QColor("#2f5fd0"))
p.fillPath(path, g)
f = QFont("Helvetica Neue", 1)
f.setPixelSize(470)
f.setWeight(QFont.Weight.Black)
p.setFont(f)
p.setPen(QColor("#ffffff"))
p.drawText(QRectF(0, 150, N, 560), Qt.AlignmentFlag.AlignCenter, "Py")
bar = QPainterPath()
bar.addRoundedRect(QRectF(300, 720, 424, 44), 22, 22)
p.fillPath(bar, QColor("#ffd24a"))
p.end()
out = Path(__file__).resolve().parent.parent / "src" / "pydojo" / "assets" / "icon.png"
out.parent.mkdir(parents=True, exist_ok=True)
img.save(str(out))
print("wrote", out)
