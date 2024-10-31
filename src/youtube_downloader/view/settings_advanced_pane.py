"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, 
                               QCheckBox, QComboBox, QSizePolicy)
from PySide6.QtCore import Qt

from youtube_downloader.view.hline_widget import HLineWidget

class SettingsAdvancedPane(QWidget):
    class DebugSection(QWidget):
        def __init__(self):
            super().__init__()

            ### ROOT ###
            root_layout = QVBoxLayout()
            self.setLayout(root_layout)

            ### ROOT > TITLE ###
            title_layout = QHBoxLayout()
            self.title_label = QLabel("Debug")
            title_layout.addWidget(self.title_label)
            title_layout.addWidget(HLineWidget(3))
            root_layout.addLayout(title_layout)

            ### ROOT > CONTENT ###
            content_widget = QWidget()
            content_layout = QVBoxLayout()
            content_widget.setLayout(content_layout)
            root_layout.addWidget(content_widget)

            ### ROOT > CONTENT > CONFIG:DEBUG-MODE ###
            self.debug_mode_checkbox = QCheckBox("Show log panel")
            content_layout.addWidget(self.debug_mode_checkbox)

            ### ROOT > CONTENT > CONFIG:DEBUG-LOG-LEVEL ###
            debug_log_level_widget = QWidget()
            debug_log_level_layout = QHBoxLayout()
            debug_log_level_widget.setLayout(debug_log_level_layout)
            content_layout.addWidget(debug_log_level_widget)
            self.debug_log_level_label = QLabel("Log Level: ")
            debug_log_level_layout.addWidget(self.debug_log_level_label)
            self.debug_log_level_input = QComboBox()
            debug_log_level_layout.addWidget(self.debug_log_level_input)
            debug_log_level_layout.addStretch()
            self.debug_log_level_input.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])

            ### STYLE: Content margins ###
            root_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setContentsMargins(30, 0, 0, 0)
            debug_log_level_layout.setContentsMargins(0, 0, 0, 0)

            ### STYLE: Spacing ###
            root_layout.setSpacing(8)
            debug_log_level_layout.setSpacing(4)
            content_layout.setSpacing(12)

            ### STYLE: Size policy ###
            self.debug_log_level_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self.debug_log_level_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            ### STYLE: Property ###
            self.title_label.setProperty("class", "settings-section-title")
            self.debug_log_level_input.setProperty("class", "combo-box")

            ### STYLE: Object name ###
            self.title_label.setObjectName("settings-advanced-debug-title")
            self.debug_log_level_label.setObjectName("settings-advanced-debug-log-level-label")
            self.debug_log_level_input.setObjectName("settings-advanced-debug-log-level-input")

    def __init__(self):
        super().__init__()
        self.init_sections()
        self.init_ui()
        self.init_style()

    def init_sections(self):
        self.sections = []
        self.debug_section = SettingsAdvancedPane.DebugSection()
        self.sections.append(self.debug_section)

    def init_ui(self):
        ### ROOT ###
        self.root_layout = QVBoxLayout()
        self.setLayout(self.root_layout)
        
        ### ROOT > MAIN ###
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.main_widget)
        self.root_layout.addWidget(self.scroll_area)

        for section in self.sections:
            self.main_layout.addWidget(section)
        self.main_layout.addStretch(10)

    def init_style(self):
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(20)
        self.main_widget.setProperty("class", "settings-content")