"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QGridLayout, QComboBox, 
                               QPushButton, QComboBox, QSizePolicy, QHBoxLayout, QSpacerItem)
from youtube_downloader.util.gui import center_widget_on_screen
from PySide6.QtCore import Qt

class SetupWindow(QMainWindow):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.setGeometry(0, 0, 400, 300)
        center_widget_on_screen(self, kwargs.get("screen", None))
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_widget = QWidget()
        self.setup_main_layout = QVBoxLayout()
        self.setup_main_widget.setLayout(self.setup_main_layout)
        self.setCentralWidget(self.setup_main_widget)

        self.setup_welcome_label = QLabel()
        self.setup_welcome_label.setObjectName("setup-welcome-label")

        self.setup_config_widget = QWidget()
        self.setup_config_layout = QGridLayout()
        self.setup_config_widget.setLayout(self.setup_config_layout)

        self.setup_config_language_label = QLabel()
        self.setup_config_language_label.setObjectName("setup-config-language-label")
        self.setup_config_language_label.setProperty("class", "input-label")
        self.setup_config_language_selector = QComboBox()
        self.setup_config_language_selector.setObjectName("setup-config-language-selector")
        self.setup_config_theme_label = QLabel()
        self.setup_config_theme_label.setObjectName("setup-config-theme-label")
        self.setup_config_theme_label.setProperty("class", "input-label")
        self.setup_config_theme_selector = QComboBox()
        self.setup_config_theme_selector.setObjectName("setup-config-theme-selector")

        self.setup_config_layout.addWidget(self.setup_config_language_label, 0, 0)
        self.setup_config_layout.addWidget(self.setup_config_language_selector, 0, 1)
        self.setup_config_layout.addWidget(self.setup_config_theme_label, 1, 0)
        self.setup_config_layout.addWidget(self.setup_config_theme_selector, 1, 1)

        spacer_item = QSpacerItem(60, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.setup_config_layout.addItem(spacer_item, 0, 2, 2, 1)

        self.footer_container = QWidget()
        self.footer_layout = QHBoxLayout()
        self.footer_container.setLayout(self.footer_layout)

        self.setup_start_button = QPushButton()
        self.setup_start_button.setObjectName("setup-start-button")
        self.setup_start_button.setProperty("class", "primary")

        self.footer_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.footer_layout.addWidget(self.setup_start_button)
        self.footer_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.setup_main_layout.addWidget(self.setup_welcome_label)
        self.setup_main_layout.addWidget(self.setup_config_widget)
        self.setup_main_layout.addWidget(self.footer_container)

        self.setup_welcome_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setup_config_language_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setup_config_theme_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.footer_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.setup_start_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.setup_welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setup_config_language_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setup_config_theme_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.setup_config_layout.setContentsMargins(0, 5, 0, 5)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)

        self.setup_main_layout.setSpacing(5)
        self.setup_config_layout.setSpacing(15)
