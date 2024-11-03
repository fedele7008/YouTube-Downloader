"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os
from typing import Any
import requests

from PySide6.QtWidgets import QWidget, QStackedLayout, QLabel, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtGui import QImage, QPixmap, QPainter, QEnterEvent, QMouseEvent, QCursor

from youtube_downloader.util.path import get_media_path

class ResizableImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_original = None
        self.overlay_pixmap = None
        self.mouse_over = False
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setMinimumSize(0, 0)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def setPixmap(self, pixmap):
        """Store the original pixmap and trigger repaint."""
        self.pixmap_original = pixmap
        self.update()

    def setOverlayPixmap(self, pixmap):
        """Set the overlay pixmap (e.g., play button)."""
        self.overlay_pixmap = pixmap

    def enterEvent(self, event):
        """Handle mouse entering the widget."""
        self.mouse_over = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leaving the widget."""
        self.mouse_over = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """Custom paint event to handle aspect-ratio scaling and overlay."""
        if self.pixmap_original:
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.black)
            scaled_pixmap = self.pixmap_original.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            if self.mouse_over and self.overlay_pixmap:
                smaller_side = min(scaled_pixmap.width(), scaled_pixmap.height())
                overlay_size = QSize(smaller_side // 4, smaller_side // 4)
                overlay_scaled_pixmap = self.overlay_pixmap.scaled(
                    overlay_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                overlay_x = x + (scaled_pixmap.width() - overlay_scaled_pixmap.width()) // 2
                overlay_y = y + (scaled_pixmap.height() - overlay_scaled_pixmap.height()) // 2
                painter.drawPixmap(overlay_x, overlay_y, overlay_scaled_pixmap)
        else:
            super().paintEvent(event)

class VideoWidget(QWidget):
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html style="width: 100%; height: 100%; margin: 0; padding: 0">
        <body style="overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0">
            {content}
        </body>
    </html>
    """

    def __init__(self, video_url_or_id: str, thumbnail_url: str | None = None, controls: bool = True, autoplay: bool = True, parent: QWidget | None = None, **kwargs: Any):
        super().__init__(parent)
        self.autoplay = autoplay

        url_or_id = video_url_or_id.strip()
        if "watch?v=" in url_or_id:
            url_start = url_or_id.split("watch?v=")[1]
            self.video_id = url_start[:url_start.find("&") if "&" in url_start else len(url_start)]
        elif "youtu.be/" in url_or_id:
            url_start = url_or_id.split("youtu.be/")[1]
            self.video_id = url_start[:url_start.find("?") if "?" in url_start else len(url_start)]
        elif "embed/" in url_or_id:
            url_start = url_or_id.split("embed/")[1]
            self.video_id = url_start[:url_start.find("?") if "?" in url_start else len(url_start)]
        else:
            self.video_id = url_or_id

        self.video_url = f"https://www.youtube.com/embed/{self.video_id}"
        self.video_options = [
            f"autoplay={1 if autoplay else 0}",
            f"controls={1 if controls else 0}",
            "fs=0",
            "iv_load_policy=3",
            "enablejsapi=1",
            "origin=https://www.youtube.com"
        ]
        self.iframe_tag = f'<iframe id="player" width="100%" height="100%" src="{self.video_url}?{"&".join(self.video_options)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>'
        self.html_str = VideoWidget.HTML_TEMPLATE.format(content=self.iframe_tag, video_id=self.video_id)

        self.main_layout = QStackedLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.web_view = QWebEngineView()
        self.web_view.show()

        self.main_layout.addWidget(self.web_view)

        self.settings = self.web_view.settings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        
        self.set_thumbnail(thumbnail_url)
        self.main_layout.addWidget(self.thumbnail_label)
        self.main_layout.setCurrentWidget(self.thumbnail_label)

    def enterEvent(self, event: QEnterEvent) -> None:
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        return super().leaveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.main_layout.setCurrentWidget(self.web_view)
        self.web_view.setHtml(self.html_str)
        return super().mousePressEvent(event)

    def create_thumbnail(self, image_data: bytes, overlay: str | None = None) -> QLabel:
        image = QImage()
        image.loadFromData(image_data)
        pixmap = QPixmap.fromImage(image)
        label = ResizableImageLabel()
        label.setPixmap(pixmap)
        if overlay is not None:
            overlay_image_path = os.path.join(get_media_path(), overlay)
            overlay_pixmap = QPixmap(overlay_image_path)
            label.setOverlayPixmap(overlay_pixmap)
        return label

    def set_thumbnail(self, thumbnail_url: str | None) -> None:
        if thumbnail_url:
            res = requests.get(thumbnail_url)
            if res.status_code == 200:
                self.thumbnail_label = self.create_thumbnail(res.content, overlay="play_button.png")
                return
        
        default_image_path = os.path.join(get_media_path(), "sample.png")
        with open(default_image_path, "rb") as f:
            self.thumbnail_label = self.create_thumbnail(f.read())
