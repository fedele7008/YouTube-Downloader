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
    def __init__(self, parent: QWidget | None = None, result_data: dict | None = None, **kwargs: Any):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 600)
        center_widget_on_screen(self, kwargs.get("screen", None))
        
        self.result_data = result_data
        if self.result_data is None:
            raise ValueError("Result data is not provided")
        self.video_id = self.result_data.get("id", None)
        if self.video_id is None:
            raise ValueError("Result data does not contain 'id'")
        self.thumbnail_url = self.result_data.get("thumbnail", None)

        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        self.result_widget = VideoWidget(self.video_id, self.thumbnail_url, parent=self)
        self.main_layout.addWidget(self.result_widget)

        self.label = QLabel(self.result_data.get("title", "No title"))
        self.main_layout.addWidget(self.label)

        self.setLayout(self.main_layout)

    def init_style(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
