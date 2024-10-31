"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, 
                               QComboBox, QSizePolicy, QLineEdit, QCheckBox)
from PySide6.QtCore import Qt

from youtube_downloader.view.hline_widget import HLineWidget

class SettingsGeneralPane(QWidget):
    class LocaleSection(QWidget):
        def __init__(self):
            super().__init__()

            ### ROOT ###
            root_layout = QVBoxLayout()
            self.setLayout(root_layout)

            ### ROOT > TITLE ###
            title_layout = QHBoxLayout()
            self.title_label = QLabel()
            title_layout.addWidget(self.title_label)
            title_layout.addWidget(HLineWidget(3))
            root_layout.addLayout(title_layout)

            ### ROOT > CONTENT ###
            content_widget = QWidget()
            content_layout = QVBoxLayout()
            content_widget.setLayout(content_layout)
            root_layout.addWidget(content_widget)

            ### ROOT > CONTENT > CONFIG:LANGUAGE ###
            language_widget = QWidget()
            language_layout = QHBoxLayout()
            language_widget.setLayout(language_layout)
            self.language_label = QLabel()
            self.language_input = QComboBox()
            language_layout.addWidget(self.language_label)
            language_layout.addWidget(self.language_input)
            language_layout.addStretch()
            content_layout.addWidget(language_widget)

            ### STYLE: Content margins ###
            root_layout.setContentsMargins(0, 0, 0, 0)
            language_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setContentsMargins(20, 0, 0, 0)

            ### STYLE: Size policy ###
            self.language_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self.language_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            ### STYLE: Property ###
            self.title_label.setProperty("class", "settings-section-title")
            self.language_label.setProperty("class", "input-label")
            self.language_input.setProperty("class", "combo-box")

            ### STYLE: Object name ###
            self.title_label.setObjectName("settings-general-locale-title")
            self.language_label.setObjectName("settings-general-locale-language-label")
            self.language_input.setObjectName("settings-general-locale-language-input")
    
    class DownloadSection(QWidget):
        def __init__(self):
            super().__init__()

            ### ROOT ###
            root_layout = QVBoxLayout()
            self.setLayout(root_layout)

            ### ROOT > TITLE ###
            title_layout = QHBoxLayout()
            self.title_label = QLabel()
            title_layout.addWidget(self.title_label)
            title_layout.addWidget(HLineWidget(3))
            root_layout.addLayout(title_layout)

            ### ROOT > CONTENT ###
            content_widget = QWidget()
            content_layout = QVBoxLayout()
            content_widget.setLayout(content_layout)
            root_layout.addWidget(content_widget)

            ### ROOT > CONTENT > CONFIG:DEFAULT-DOWNLOAD-PATH ###
            default_download_path_widget = QWidget()
            default_download_path_layout = QVBoxLayout()
            default_download_path_widget.setLayout(default_download_path_layout)
            self.default_download_path_label = QLabel()
            self.default_download_path_input = QLineEdit()
            default_download_path_layout.addWidget(self.default_download_path_label)
            default_download_path_layout.addWidget(self.default_download_path_input)
            content_layout.addWidget(default_download_path_widget)

            ### ROOT > CONTENT > CONFIG:LOAD-LAST-DOWNLOAD-PATH ###
            self.load_last_download_path_checkbox = QCheckBox()
            content_layout.addWidget(self.load_last_download_path_checkbox)

            ### STYLE: Content margins ###
            root_layout.setContentsMargins(0, 0, 0, 0)
            default_download_path_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setContentsMargins(20, 0, 0, 0)

            ### STYLE: Spacing ###
            default_download_path_layout.setSpacing(4)

            ### STYLE: Property ###
            self.title_label.setProperty("class", "settings-section-title")

            ### STYLE: Object name ###
            self.title_label.setObjectName("settings-general-download-title")
            self.default_download_path_label.setObjectName("settings-general-download-default-download-path-label")
            self.default_download_path_input.setObjectName("settings-general-download-default-download-path-input")
            self.load_last_download_path_checkbox.setObjectName("settings-general-download-load-last-download-path-checkbox")

    def __init__(self):
        super().__init__()
        self.init_sections()
        self.init_ui()
        self.init_style()

    def init_sections(self):
        self.sections = []
        self.locale_section = SettingsGeneralPane.LocaleSection()
        self.download_section = SettingsGeneralPane.DownloadSection()
        self.sections.append(self.locale_section)
        self.sections.append(self.download_section)

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
        self.main_layout.addStretch()

    def init_style(self):
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.main_widget.setProperty("class", "settings-content")
