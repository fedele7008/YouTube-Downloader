"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from youtube_downloader.view.video_widget import VideoWidget

class StatusPane(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.video_widget = VideoWidget("https://www.youtube.com/watch?v=Q_i068DzFYo", thumbnail_url="https://i.ytimg.com/vi/Q_i068DzFYo/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCXGH3dsHqszXBQ47k5tPrY8tdVsg", parent=self)
        self.main_layout.addWidget(self.video_widget, 1)

    def init_style(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)


