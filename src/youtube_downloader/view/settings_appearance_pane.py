"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, 
                               QComboBox, QSizePolicy, QSpinBox, QPushButton, QTextEdit,
                               QFrame)
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt

from youtube_downloader.view.hline_widget import HLineWidget

class SettingsAppearancePane(QWidget):
    class StyleSection(QWidget):
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

            ### ROOT > CONTENT > CONFIG:THEME ###
            theme_widget = QWidget()
            theme_layout = QVBoxLayout()
            theme_widget.setLayout(theme_layout)
            content_layout.addWidget(theme_widget)
            theme_select_widget = QWidget()
            theme_select_layout = QHBoxLayout()
            theme_select_widget.setLayout(theme_select_layout)
            theme_layout.addWidget(theme_select_widget)
            self.theme_label = QLabel()
            self.theme_input = QComboBox()
            theme_select_layout.addWidget(self.theme_label)
            theme_select_layout.addWidget(self.theme_input)
            theme_select_layout.addStretch()
            theme_import_widget = QWidget()
            theme_import_layout = QHBoxLayout()
            theme_import_widget.setLayout(theme_import_layout)
            theme_layout.addWidget(theme_import_widget)
            self.theme_import = QPushButton()
            theme_import_layout.addWidget(self.theme_import)
            theme_import_layout.addStretch()
            theme_layout.addStretch()

            ### ROOT > CONTENT > CONFIG:THEME-PREVIEW ###
            config_section_widget = QWidget()
            config_section_layout = QVBoxLayout()
            config_section_widget.setLayout(config_section_layout)
            content_layout.addWidget(config_section_widget)
            self.preview_label = QLabel()
            config_section_layout.addWidget(self.preview_label)
            preview_widget_wrapper_widget = QWidget()
            preview_widget_wrapper_layout = QHBoxLayout()
            preview_widget_wrapper_widget.setLayout(preview_widget_wrapper_layout)
            config_section_layout.addWidget(preview_widget_wrapper_widget)
            self.preview_widget = QFrame()
            preview_layout = QHBoxLayout()
            self.preview_widget.setLayout(preview_layout)
            preview_widget_wrapper_layout.addWidget(self.preview_widget)
            self.primary_color = QFrame()
            preview_layout.addWidget(self.primary_color)
            self.secondary_color = QFrame()
            preview_layout.addWidget(self.secondary_color)
            self.accent_color = QFrame()
            preview_layout.addWidget(self.accent_color)
            self.neutral_color = QFrame()
            preview_layout.addWidget(self.neutral_color)
            self.foreground_color = QFrame()
            preview_layout.addWidget(self.foreground_color)
            self.disabled_color = QFrame()
            preview_layout.addWidget(self.disabled_color)
            self.field_color = QFrame()
            preview_layout.addWidget(self.field_color)
            preview_layout.addStretch()
            preview_widget_wrapper_layout.addStretch(5)
            config_section_layout.addStretch()

            ### STYLE: Property ###
            self.theme_import.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            preview_height = 30
            inner_padding = 10
            self.preview_widget.setFixedHeight(preview_height)
            self.primary_color.setFixedSize(preview_height - inner_padding, preview_height - inner_padding)
            self.secondary_color.setFixedSize(preview_height - inner_padding, preview_height - inner_padding)
            self.accent_color.setFixedSize(preview_height - inner_padding, preview_height - inner_padding)
            self.neutral_color.setFixedSize(preview_height - inner_padding, preview_height - inner_padding)
            self.foreground_color.setFixedSize(preview_height - inner_padding, preview_height - inner_padding)
            self.disabled_color.setFixedSize(preview_height - inner_padding, preview_height - inner_padding)
            self.field_color.setFixedSize(preview_height - inner_padding, preview_height - inner_padding)
            self.primary_color.setToolTip("Primary")
            self.secondary_color.setToolTip("Secondary")
            self.accent_color.setToolTip("Accent")
            self.neutral_color.setToolTip("Neutral")
            self.foreground_color.setToolTip("Foreground")
            self.disabled_color.setToolTip("Disabled")
            self.field_color.setToolTip("Field")
            self.primary_color.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            self.secondary_color.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            self.accent_color.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            self.neutral_color.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            self.foreground_color.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            self.disabled_color.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            self.field_color.setCursor(QCursor(Qt.CursorShape.CrossCursor))

            ### STYLE: Content margins ###
            root_layout.setContentsMargins(0, 0, 0, 0)
            theme_layout.setContentsMargins(0, 0, 0, 0)
            theme_select_layout.setContentsMargins(0, 0, 0, 0)
            theme_import_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setContentsMargins(30, 0, 0, 0)
            config_section_layout.setContentsMargins(0, 0, 0, 0)
            preview_widget_wrapper_layout.setContentsMargins(0, 0, 0, 0)
            preview_layout.setContentsMargins(inner_padding//2, 0, inner_padding//2, 0)

            ### STYLE: Spacing ###
            root_layout.setSpacing(8)
            theme_layout.setSpacing(8)
            content_layout.setSpacing(12)
            preview_layout.setSpacing(inner_padding//2)
            config_section_layout.setSpacing(6)

            ### STYLE: Size policy ###
            self.theme_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self.theme_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            self.theme_import.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self.preview_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

            ### STYLE: Property ###
            self.title_label.setProperty("class", "settings-section-title")
            self.theme_input.setProperty("class", "combo-box")
            self.theme_import.setProperty("class", "neutral")
            self.preview_widget.setProperty("class", "theme-preview-frame")
            self.primary_color.setProperty("class", "theme-preview-color")
            self.secondary_color.setProperty("class", "theme-preview-color")
            self.accent_color.setProperty("class", "theme-preview-color")
            self.neutral_color.setProperty("class", "theme-preview-color")
            self.foreground_color.setProperty("class", "theme-preview-color")
            self.disabled_color.setProperty("class", "theme-preview-color")
            self.field_color.setProperty("class", "theme-preview-color")

            ### STYLE: Object name ###
            self.title_label.setObjectName("settings-appearance-style-title")
            self.theme_label.setObjectName("settings-appearance-style-theme-label")
            self.theme_input.setObjectName("settings-appearance-style-theme-input")
            self.theme_import.setObjectName("settings-appearance-style-theme-import")
            self.preview_label.setObjectName("settings-appearance-style-preview-label")
            self.preview_widget.setObjectName("settings-appearance-style-preview-widget")
            self.primary_color.setObjectName("settings-appearance-style-primary-color")
            self.secondary_color.setObjectName("settings-appearance-style-secondary-color")
            self.accent_color.setObjectName("settings-appearance-style-accent-color")
            self.neutral_color.setObjectName("settings-appearance-style-neutral-color")
            self.foreground_color.setObjectName("settings-appearance-style-foreground-color")
            self.disabled_color.setObjectName("settings-appearance-style-disabled-color")
            self.field_color.setObjectName("settings-appearance-style-field-color")

    class FontSection(QWidget):
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

            ### ROOT > CONTENT > CONFIG:FONT ###
            font_widget = QWidget()
            font_layout = QHBoxLayout()
            font_widget.setLayout(font_layout)
            content_layout.addWidget(font_widget)
            self.font_label = QLabel()
            self.font_input = QComboBox()
            font_layout.addWidget(self.font_label)
            font_layout.addWidget(self.font_input)
            font_layout.addStretch()

            ### ROOT > CONTENT > CONFIG:FONT-SIZE ###
            font_size_widget = QWidget()
            font_size_layout = QHBoxLayout()
            font_size_widget.setLayout(font_size_layout)
            content_layout.addWidget(font_size_widget)
            self.font_size_label = QLabel()
            self.font_size_input = QSpinBox()
            font_size_layout.addWidget(self.font_size_label)
            font_size_layout.addWidget(self.font_size_input)
            font_size_layout.addStretch()

            ### ROOT > CONTENT > CONFIG:FONT-PREVIEW ###
            self.font_preview_widget = QTextEdit()
            self.font_preview_widget.setReadOnly(True)
            content_layout.addWidget(self.font_preview_widget)

            ### STYLE: Content margins ###
            root_layout.setContentsMargins(0, 0, 0, 0)
            font_layout.setContentsMargins(0, 0, 0, 0)
            font_size_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setContentsMargins(30, 0, 0, 0)

            ### STYLE: Spacing ###
            root_layout.setSpacing(8)
            font_layout.setSpacing(4)
            font_size_layout.setSpacing(4)
            content_layout.setSpacing(12)

            ### STYLE: Size policy ###
            self.font_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self.font_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            self.font_size_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self.font_size_input.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self.font_preview_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            ### STYLE: Property ###
            self.title_label.setProperty("class", "settings-section-title")
            self.font_input.setProperty("class", "combo-box")
            self.font_size_input.setProperty("class", "spin-box")

            ### STYLE: Object name ###
            self.title_label.setObjectName("settings-appearance-fonts-title")
            self.font_label.setObjectName("settings-appearance-fonts-font-label")
            self.font_input.setObjectName("settings-appearance-fonts-font-input")
            self.font_size_label.setObjectName("settings-appearance-fonts-font-size-label")
            self.font_size_input.setObjectName("settings-appearance-fonts-font-size-input")
            self.font_preview_widget.setObjectName("settings-appearance-fonts-font-preview")


    def __init__(self):
        super().__init__()
        self.init_sections()
        self.init_ui()
        self.init_style()

    def init_sections(self):
        self.sections = []
        self.style_section = SettingsAppearancePane.StyleSection()
        self.font_section = SettingsAppearancePane.FontSection()
        self.sections.append(self.style_section)
        self.sections.append(self.font_section)

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
        self.main_layout.setSpacing(20)
        self.main_widget.setProperty("class", "settings-content")
