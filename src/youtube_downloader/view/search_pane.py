"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

class SearchPane(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        
        self.url_label = QLabel("URL")
        self.url_input = QLineEdit()
        self.dest_label = QLabel("Download Directory")
        self.dest_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.input_error_label = QLabel("Some error message")
        self.search_button = QPushButton("Search")
        self.main_layout.addWidget(self.url_label, 0, 0)
        self.main_layout.addWidget(self.url_input, 0, 1, 1, 2)
        self.main_layout.addWidget(self.dest_label, 1, 0)
        self.main_layout.addWidget(self.dest_input, 1, 1)
        self.main_layout.addWidget(self.browse_button, 1, 2)
        self.main_layout.addWidget(self.input_error_label, 2, 1, 1, 2)
        self.main_layout.addWidget(self.search_button, 0, 3, 2, 1)

    def init_style(self):
        pass
