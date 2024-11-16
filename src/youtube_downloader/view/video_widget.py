"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os
from typing import Any

from PySide6.QtWidgets import QWidget, QStackedLayout, QLabel, QProgressBar, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QHideEvent, QImage, QPixmap, QEnterEvent, QMouseEvent, QCloseEvent

from youtube_downloader.util.path import get_media_path
from youtube_downloader.view.resizable_image import ResizeableImage
from youtube_downloader.util.request import get_request

class VideoWidget(QWidget):
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html style="width: 100%; height: 100%; margin: 0; padding: 0">
        <body style="overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0">
            {content}
        </body>
    </html>
    """

    def __init__(self, video_url_or_id: str | None = None, thumbnail_url: str | None = None, controls: bool = True, autoplay: bool = True, parent: QWidget | None = None, **kwargs: Any):
        super().__init__(parent)
        self.autoplay = autoplay
        self.controls = controls
        self.autoplay = autoplay
        self.video_ready = False

        self.main_layout = QStackedLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        if video_url_or_id:
            self.set_video(video_url_or_id)
        else:
            self.web_view = QWidget()
            self.main_layout.addWidget(self.web_view)
        self.set_thumbnail(thumbnail_url)
        self.main_layout.setCurrentWidget(self.thumbnail_label)

    def set_video(self, video_url_or_id: str):
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
            f"autoplay={1 if self.autoplay else 0}",
            f"controls={1 if self.controls else 0}",
            "fs=0",
            "iv_load_policy=3",
            "enablejsapi=1",
            "origin=https://www.youtube.com"
        ]
        self.iframe_tag = f'<iframe id="player" width="100%" height="100%" src="{self.video_url}?{"&".join(self.video_options)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>'
        self.html_str = VideoWidget.HTML_TEMPLATE.format(content=self.iframe_tag, video_id=self.video_id)

        self.web_view = QWidget()
        self.web_view_layout = QVBoxLayout()
        self.web_view_layout.setContentsMargins(0, 0, 0, 0)
        self.web_view_layout.setSpacing(0)
        self.web_view.setLayout(self.web_view_layout)

        self.web_view_content = QWebEngineView()
        self.settings = self.web_view_content.settings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)

        self.first_load = True
        self.web_view_content.setHtml(self.html_str)
        self.web_view_content.stop()
        self.web_view_content.show()
        self.web_view_layout.addWidget(self.web_view_content)

        self.main_layout.addWidget(self.web_view)

        self.timeout = 10000
        self.timer_bar = QProgressBar(self)
        self.timer_bar.setFixedHeight(5)
        self.timer_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                  stop:0 #2D32B3, stop:1 #B32DFF);
            }
        """)
        self.timer_bar.setMaximum(1000)
        self.timer_bar.setValue(self.timer_bar.maximum())
        self.timer_bar.setTextVisible(False)
        self.timer_bar.hide()
        self.timer_bar_animation = None
        self.web_view_layout.addWidget(self.timer_bar)
        self.video_ready = True

    def create_thumbnail(self, image_data: bytes, overlay: str | None = None) -> QLabel:
        thumbnail_image = QImage()
        thumbnail_image.loadFromData(image_data)
        thumbnail_pixmap = QPixmap.fromImage(thumbnail_image)
        thumbnail_widget = ResizeableImage(pixmap=thumbnail_pixmap, fill_color=Qt.GlobalColor.black, hover_scale=1/4)
        if overlay is not None:
            overlay_image_path = os.path.join(get_media_path(), overlay)
            overlay_pixmap = QPixmap(overlay_image_path)
            thumbnail_widget.setHoverPixmap(overlay_pixmap)
        return thumbnail_widget

    def set_thumbnail(self, thumbnail_url: str | None) -> None:
        image = get_request(thumbnail_url)
        if not image:
            default_image_path = os.path.join(get_media_path(), "default_thumbnail.jpg")
            with open(default_image_path, "rb") as f:
                self.thumbnail_label = self.create_thumbnail(f.read())
                self.main_layout.addWidget(self.thumbnail_label)
                self.main_layout.setCurrentWidget(self.thumbnail_label)
            return
        
        self.thumbnail_label = self.create_thumbnail(image.content, overlay="play_button.png")
        self.main_layout.addWidget(self.thumbnail_label)
        self.main_layout.setCurrentWidget(self.thumbnail_label)

    def on_timer_start(self) -> None:
        self.timer_bar_animation = QPropertyAnimation(self.timer_bar, b"value")
        self.timer_bar_animation.setDuration(self.timeout)
        self.timer_bar_animation.setStartValue(self.timer_bar.maximum())
        self.timer_bar_animation.setEndValue(0)
        self.timer_bar_animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.timer_bar_animation.finished.connect(self.on_timer_timeout)
        self.timer_bar_animation.start()
        self.timer_bar.setValue(self.timer_bar.maximum())
        self.timer_bar.show()

    def on_timer_stop(self) -> None:
        if self.timer_bar_animation:
            self.timer_bar_animation.stop()
            self.timer_bar_animation = None
        self.timer_bar.hide()

    def on_timer_timeout(self) -> None:
        self.main_layout.setCurrentWidget(self.thumbnail_label)
        self.web_view_content.setHtml("")
        self.on_timer_stop()

    def enterEvent(self, event: QEnterEvent) -> None:
        if self.main_layout.currentWidget() == self.web_view:
            self.on_timer_stop()
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        if self.main_layout.currentWidget() == self.web_view:
            self.on_timer_start()
        return super().leaveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.video_ready:
            return super().mousePressEvent(event)

        self.main_layout.setCurrentWidget(self.web_view)
        if self.first_load:
            self.web_view_content.reload()
            self.first_load = False
        else:
            self.web_view_content.setHtml(self.html_str)
        return super().mousePressEvent(event)

    def widget_cleanup(self) -> None:
        self.on_timer_stop()
        self.on_timer_timeout()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.widget_cleanup()
        self.web_view_content.stop()
        self.web_view_content.deleteLater()
        return super().closeEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.widget_cleanup()
        return super().hideEvent(event)
