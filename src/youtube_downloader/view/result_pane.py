"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ResultPane(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.video_info_widget = QWidget()
        self.video_info_layout = QVBoxLayout()
        self.video_info_widget.setLayout(self.video_info_layout)
        self.main_layout.addWidget(self.video_info_widget)

        self.video_info_layout.addWidget(QLabel("TEST"))

    def init_style(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
