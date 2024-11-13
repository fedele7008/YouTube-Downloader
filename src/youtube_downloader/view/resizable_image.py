"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QColor, QCursor
from PySide6.QtCore import Qt, QSize

class ResizeableImage(QLabel):
    def __init__(self, parent=None, pixmap: QPixmap = None, fill_color: QColor = Qt.GlobalColor.black, hover_pixmap: QPixmap = None, hover_scale: float = 1.0):
        super().__init__(parent)
        self.base_pixmap = pixmap
        self.fill_color = fill_color
        self.hover_pixmap = hover_pixmap
        self.hover_scale = hover_scale
        self.mouse_over = False
        self.setAlignment(Qt.AlignCenter)
        self.setPixmap(pixmap)
        self.setMinimumSize(0, 0)
        if hover_pixmap:
            self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def setPixmap(self, pixmap: QPixmap) -> None:
        self.base_pixmap = pixmap
        self.update()

    def setFillColor(self, color: QColor) -> None:
        self.fill_color = color
        self.update()

    def setHoverPixmap(self, pixmap: QPixmap) -> None:
        self.hover_pixmap = pixmap
        self.update()

    def setHoverScale(self, scale: float) -> None:
        self.hover_scale = scale
        self.update()

    def enterEvent(self, event) -> None:
        self.mouse_over = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.mouse_over = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event) -> None:
        if not self.base_pixmap:
            super().paintEvent(event)
            return
        
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.fill_color)
        scaled_pixmap = self.base_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        x = (self.width() - scaled_pixmap.width()) // 2
        y = (self.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)

        if self.mouse_over and self.hover_pixmap:
            smaller_edge = min(scaled_pixmap.width(), scaled_pixmap.height())
            hover_size = QSize(smaller_edge * self.hover_scale, smaller_edge * self.hover_scale)
            hover_scaled_pixmap = self.hover_pixmap.scaled(hover_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            hover_x = x + (scaled_pixmap.width() - hover_scaled_pixmap.width()) // 2
            hover_y = y + (scaled_pixmap.height() - hover_scaled_pixmap.height()) // 2
            painter.drawPixmap(hover_x, hover_y, hover_scaled_pixmap)
