"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class SearchPane(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.url_label = QLabel()
        self.url_input = QLineEdit()
        self.dest_label = QLabel()
        self.dest_input = QLineEdit()
        self.browse_button = QPushButton()
        self.input_error_label = QLabel()
        self.search_button = QPushButton()
        self.main_layout.addWidget(self.url_label, 0, 0)
        self.main_layout.addWidget(self.url_input, 0, 1, 1, 2)
        self.main_layout.addWidget(self.dest_label, 1, 0)
        self.main_layout.addWidget(self.dest_input, 1, 1)
        self.main_layout.addWidget(self.browse_button, 1, 2)
        self.main_layout.addWidget(self.input_error_label, 2, 1, 1, 2)
        self.main_layout.addWidget(self.search_button, 0, 3, 2, 1)

    def init_style(self):
        self.url_label.setProperty("class", "input-label")
        self.dest_label.setProperty("class", "input-label")
        self.browse_button.setProperty("class", "neutral")
        self.search_button.setProperty("class", "primary")
        self.url_input.setProperty("class", "input-field")
        self.dest_input.setProperty("class", "input-field")

        self.url_label.setObjectName("search-pane-url-label")
        self.url_input.setObjectName("search-pane-url-input")
        self.dest_label.setObjectName("search-pane-dest-label")
        self.dest_input.setObjectName("search-pane-dest-input")
        self.browse_button.setObjectName("search-pane-browse-button")
        self.input_error_label.setObjectName("search-pane-input-error-label")
        self.search_button.setObjectName("search-pane-search-button")

        self.input_error_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.url_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.dest_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.url_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dest_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.input_error_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.url_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.dest_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(6)
        self.main_layout.setRowStretch(3, 1)
