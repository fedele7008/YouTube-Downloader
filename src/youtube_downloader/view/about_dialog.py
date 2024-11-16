"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy, 
                               QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

import youtube_downloader
from youtube_downloader.util.gui import center_widget_on_screen
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.data.types.locale import LocaleKeys

class AboutDialog(QDialog):
    def __init__(self, parent: QWidget, log_manager: LogManager | None, resource_manager: ResourceManager, model: YouTubeDownloaderModel, **kwargs: Any):
        super().__init__(parent)
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.model: YouTubeDownloaderModel = model

        self.locale_map = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"]
        self.setWindowTitle(self.locale_map[LocaleKeys.ABOUT_DIALOG_TITLE])
        self.setGeometry(0, 0, 400, 280)
        center_widget_on_screen(self, kwargs.get("screen", None))
        self.setObjectName("about-dialog")

        self.main_layout = QVBoxLayout()

        self.app_name_label = QLabel(self.locale_map[LocaleKeys.APP_NAME])
        self.app_name_label.setObjectName("about-dialog-app-name-label")
        
        self.app_version_label = QLabel(youtube_downloader.__version__)
        self.app_version_label.setObjectName("about-dialog-app-version-label")

        self.description_label = QLabel(self.locale_map[LocaleKeys.ABOUT_DIALOG_DESCRIPTION])
        self.description_label.setOpenExternalLinks(True)
        self.description_label.setTextFormat(Qt.TextFormat.RichText)
        self.description_label.setWordWrap(True)
        self.description_label.setObjectName("about-dialog-description-label")

        center_layout = QHBoxLayout()
        self.close_button = QPushButton(self.locale_map[LocaleKeys.CLOSE_BUTTON_TEXT])
        self.close_button.clicked.connect(self.close)
        self.close_button.setObjectName("about-dialog-close-button")
        self.close_button.setProperty("class", "neutral")
        self.close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        center_layout.addStretch()
        center_layout.addWidget(self.close_button)

        self.main_layout.addWidget(self.app_name_label)
        self.main_layout.addWidget(self.app_version_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addStretch()
        self.main_layout.addLayout(center_layout)

        self.close_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        self.app_name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.app_version_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.main_layout)
