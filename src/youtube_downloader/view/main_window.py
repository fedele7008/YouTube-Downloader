"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from youtube_downloader.util.gui import center_widget_on_screen

class MainWindow(QMainWindow):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.setGeometry(0, 0, 900, 600)
        center_widget_on_screen(self, kwargs.get("screen", None))
        self.init_ui()
        
    def init_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
