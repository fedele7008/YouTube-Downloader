"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt

from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.data.types.locale import LocaleKeys
from youtube_downloader.data.loaders.config_loader import ConfigKeys

class ErrorDialog(QMessageBox):
    def __init__(self, parent: QWidget, title: str, message: str, informative_message: str | None = None):
        super().__init__(parent)
        self.setObjectName("error-dialog")
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)
        if informative_message:
            self.setInformativeText(informative_message)
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.okay_button = QPushButton(self)
        self.okay_button.setObjectName("error-dialog-okay-button")
        self.okay_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if hasattr(parent, "resource_manager") and isinstance(parent.resource_manager, ResourceManager):
            locale = parent.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_LOCALE)
            self.okay_button.setText(parent.resource_manager.locale_loader.get_locale(locale)["components"][LocaleKeys.OK_BUTTON_TEXT])
        else:
            self.okay_button.setText("OK")
        self.addButton(self.okay_button, QMessageBox.ButtonRole.AcceptRole)
        self.exec()

    @classmethod
    def prompt(cls, parent: QWidget, title: str, message: str, informative_message: str | None = None) -> None:
        cls(parent, title, message, informative_message)
