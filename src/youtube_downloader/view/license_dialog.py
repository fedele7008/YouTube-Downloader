"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from youtube_downloader import license
from youtube_downloader.util.gui import center_widget_on_screen
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.data.types.locale import LocaleKeys

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QCursor, QTextOption
from PySide6.QtCore import Qt

class LicenseDialog(QDialog):
    def __init__(self, parent: QWidget, log_manager: LogManager | None, resource_manager: ResourceManager, model: YouTubeDownloaderModel, **kwargs: Any):
        super().__init__(parent)
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.model: YouTubeDownloaderModel = model

        self.locale_map = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"]
        self.setWindowTitle(self.locale_map[LocaleKeys.LICENSE_DIALOG_TITLE])
        self.setGeometry(0, 0, 640, 400)
        center_widget_on_screen(self, kwargs.get("screen", None))
        self.setObjectName("license-dialog")

        self.main_layout = QVBoxLayout()

        license_text = license.replace("\n", "<br>")
        self.license_label = QTextEdit(license_text)
        self.license_label.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.license_label.setReadOnly(True)
        self.license_label.setObjectName("license-dialog-license-label")
        self.license_label.setProperty("class", "readonly")
        
        center_layout = QHBoxLayout()
        self.close_button = QPushButton(self.locale_map[LocaleKeys.CLOSE_BUTTON_TEXT])
        self.close_button.clicked.connect(self.close)
        self.close_button.setObjectName("license-dialog-close-button")
        self.close_button.setProperty("class", "neutral")
        self.close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        center_layout.addStretch()
        center_layout.addWidget(self.close_button)

        self.main_layout.addWidget(self.license_label)
        self.main_layout.addLayout(center_layout)

        self.close_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.license_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.license_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.main_layout)
