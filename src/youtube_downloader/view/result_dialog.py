"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QWidget)

from youtube_downloader.util.gui import center_widget_on_screen
from youtube_downloader.view.video_widget import VideoWidget

class ResultDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, **kwargs: Any):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 600)
        center_widget_on_screen(self, kwargs.get("screen", None))

        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        self.video_widget = VideoWidget(parent=self)
        self.main_layout.addWidget(self.video_widget)

        self.setLayout(self.main_layout)

    def init_style(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
