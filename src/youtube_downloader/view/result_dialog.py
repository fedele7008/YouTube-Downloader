"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from youtube_downloader.util.gui import center_widget_on_screen
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QWidget)

class ResultPane(QDialog):
    def __init__(self, parent: QWidget, **kwargs: Any):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 600)
        center_widget_on_screen(self, kwargs.get("screen", None))
        
        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(QLabel("TEST"))

    def init_style(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
