"""Draws the app icon (src/testudines/assets/icon.png, 1024px) with Qt. No external art.

A turtle (Testudines is the scientific name for turtles) under the moon, on a rounded square.
"""
import math
import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QBrush, QColor, QGuiApplication, QImage, QLinearGradient, QPainter, QPainterPath,
                           QPen, QPolygonF, QRadialGradient)

app = QGuiApplication([])
N = 1024
img = QImage(N, N, QImage.Format.Format_ARGB32)
img.fill(Qt.GlobalColor.transparent)
p = QPainter(img)
p.setRenderHint(QPainter.RenderHint.Antialiasing)

# background: a night-sky rounded square
m = 64
tile = QPainterPath()
tile.addRoundedRect(QRectF(m, m, N - 2 * m, N - 2 * m), 200, 200)
g = QLinearGradient(0, m, 0, N - m)
g.setColorAt(0, QColor("#16233f"))
g.setColorAt(1, QColor("#1f4f6b"))
p.fillPath(tile, g)
p.setClipPath(tile)

# the moon, and a few stars
p.setPen(Qt.PenStyle.NoPen)
p.setBrush(QColor("#f1efe2"))
p.drawEllipse(QPointF(250, 250), 78, 78)
p.setBrush(QColor(255, 255, 255, 170))
for x, y, r in ((520, 180, 5), (690, 260, 4), (830, 170, 6), (420, 330, 3), (880, 380, 4), (610, 120, 3)):
    p.drawEllipse(QPointF(x, y), r, r)

# ground
ground = QPainterPath()
ground.addRect(QRectF(0, 800, N, N))
p.fillPath(ground, QColor("#2c6b45"))

ink = QColor("#123528")
skin = QColor("#8fcf74")


def leg(x: float, y: float, w: float, h: float, angle: float) -> None:
    p.save()
    p.translate(x, y)
    p.rotate(angle)
    p.setBrush(skin)
    p.setPen(QPen(ink, 14))
    p.drawRoundedRect(QRectF(-w / 2, 0, w, h), w / 2.2, w / 2.2)
    p.restore()


# legs behind the shell, then the head and tail
leg(330, 690, 92, 130, 12)
leg(700, 690, 92, 130, -12)
leg(440, 700, 86, 118, 4)
leg(600, 700, 86, 118, -4)
p.setBrush(skin)
p.setPen(QPen(ink, 14))
p.drawPolygon(QPolygonF([QPointF(250, 640), QPointF(170, 700), QPointF(262, 690)]))  # tail
p.drawEllipse(QRectF(730, 470, 200, 160))                                           # head
p.setBrush(ink)
p.setPen(Qt.PenStyle.NoPen)
p.drawEllipse(QPointF(858, 530), 15, 15)                                             # eye
p.setPen(QPen(ink, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
p.drawArc(QRectF(830, 560, 70, 34), 200 * 16, 120 * 16)                              # smile

# the shell: a dome with a hexagon pattern
shell = QPainterPath()
shell.moveTo(220, 700)
shell.cubicTo(220, 340, 820, 340, 820, 700)
shell.closeSubpath()
sg = QRadialGradient(QPointF(470, 470), 420)
sg.setColorAt(0, QColor("#f2b84b"))
sg.setColorAt(1, QColor("#c9782a"))
p.setBrush(QBrush(sg))
p.setPen(QPen(ink, 16))
p.drawPath(shell)
p.save()
p.setClipPath(shell)
p.setBrush(Qt.BrushStyle.NoBrush)
p.setPen(QPen(QColor("#8a4b17"), 12))
r = 74
for row in range(-1, 5):
    for col in range(-1, 7):
        cx = 240 + col * r * 1.75 + (row % 2) * r * 0.875
        cy = 430 + row * r * 1.5
        hexagon = QPolygonF([QPointF(cx + r * math.cos(math.radians(60 * k + 30)),
                                     cy + r * math.sin(math.radians(60 * k + 30))) for k in range(6)])
        p.drawPolygon(hexagon)
p.restore()
p.setPen(QPen(ink, 16))
p.setBrush(Qt.BrushStyle.NoBrush)
p.drawPath(shell)
rim = QPainterPath()
rim.addRoundedRect(QRectF(200, 680, 640, 46), 23, 23)
p.setBrush(QColor("#e6a243"))
p.drawPath(rim)
p.end()

out = Path(__file__).resolve().parent.parent / "src" / "testudines" / "assets" / "icon.png"
out.parent.mkdir(parents=True, exist_ok=True)
img.save(str(out))
print("wrote", out)
