"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from youtube_downloader.util.gui import center_widget_on_screen
from PySide6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QSizePolicy, QListWidget, QStackedWidget)

class SettingsDialog(QDialog):
    def __init__(self, parent: QWidget, **kwargs: Any):
        super().__init__(parent)
        self.setGeometry(0, 0, 1000, 600)
        center_widget_on_screen(self, kwargs.get("screen", None))

        self.init_ui()
        self.init_style()

    def init_ui(self):
        self.dialog_layout = QVBoxLayout()

        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.settings_list = QListWidget()
        self.settings_pane = QStackedWidget()

        self.main_layout.addWidget(self.settings_list)
        self.main_layout.addWidget(self.settings_pane)

        self.footer_widget = QWidget()
        self.footer_layout = QHBoxLayout()
        self.footer_widget.setLayout(self.footer_layout)

        self.restore_button = QPushButton("Restore")
        self.cancel_button = QPushButton("Cancel")
        self.apply_button = QPushButton("Apply")
        self.save_button = QPushButton("Save")

        self.footer_layout.addWidget(self.restore_button)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.cancel_button)
        self.footer_layout.addWidget(self.apply_button)
        self.footer_layout.addWidget(self.save_button)

        self.dialog_layout.addWidget(self.main_widget)
        self.dialog_layout.addWidget(self.footer_widget)

        self.setLayout(self.dialog_layout)

    def init_style(self):
        self.restore_button.setProperty("class", "secondary")
        self.restore_button.setObjectName("settings-dialog-restore-button")
        self.cancel_button.setProperty("class", "accent")
        self.cancel_button.setObjectName("settings-dialog-cancel-button")
        self.apply_button.setProperty("class", "neutral")
        self.apply_button.setObjectName("settings-dialog-apply-button")
        self.save_button.setProperty("class", "primary")
        self.save_button.setObjectName("settings-dialog-save-button")
        self.footer_widget.setObjectName("settings-dialog-footer-widget")
        self.settings_list.setObjectName("settings-dialog-settings-list")

        self.dialog_layout.setContentsMargins(0, 0, 0, 0)
        self.dialog_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.settings_list.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.settings_pane.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
