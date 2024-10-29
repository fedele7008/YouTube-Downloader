"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os
from enum import Enum

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QCursor

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.search_pane import SearchPane
from youtube_downloader.data.types.locale import Locale, LocaleKeys
from youtube_downloader.util.decorator import block_signal
from youtube_downloader.util.path import get_system_download_path
from youtube_downloader.data.loaders.config_loader import ConfigKeys

class SearchPaneController():
    class ErrorType(Enum):
        EMPTY_DEST = 0
        DEST_DIR_NOT_EXIST = 1
        DEST_DIR_NOT_WRITABLE = 2

    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager, view: SearchPane, model: YouTubeDownloaderModel):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.view: SearchPane = view
        self.model: YouTubeDownloaderModel = model

        self.config_ui()
        self.bind_model()
        self.refresh_ui()

    def config_ui(self):
        self.dialog_title = str()
        
        if self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_LOAD_LAST_DOWNLOAD_PATH):
            self.view.dest_input.setText(self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_LAST_DOWNLOAD_PATH))
        else:
            self.view.dest_input.setText(self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_STANDARD_DOWNLOAD_PATH))

        self.view.browse_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.view.search_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def bind_model(self):
        self.model.locale_changed.connect(self.on_locale_changed)
        self.view.dest_input.textChanged.connect(self.on_dest_input_changed)
        self.view.browse_button.clicked.connect(self.on_browse_button_clicked)
        self.view.search_button.clicked.connect(self.on_search_button_clicked)
        self.view.url_input.returnPressed.connect(self.on_search_button_clicked)

    def refresh_ui(self):
        self.model.invoke_current_locale_changed()
        self.on_dest_input_changed()

    @Slot()
    @block_signal(lambda self: self.view)
    def on_locale_changed(self, locale: Locale) -> None:
        locale_map = self.resource_manager.locale_loader.get_locale(locale)["components"]
        self.view.url_label.setText(locale_map[LocaleKeys.SEARCH_PANE_URL_LABEL])
        self.view.url_input.setPlaceholderText(locale_map[LocaleKeys.SEARCH_PANE_URL_INPUT_PLACEHOLDER])
        self.view.dest_label.setText(locale_map[LocaleKeys.SEARCH_PANE_DEST_LABEL])
        self.view.browse_button.setText(locale_map[LocaleKeys.SEARCH_PANE_BROWSE_BUTTON])
        self.view.search_button.setText(locale_map[LocaleKeys.SEARCH_PANE_SEARCH_BUTTON])
        self.dialog_title = locale_map[LocaleKeys.SEARCH_PANE_BROWSE_DIALOG_TITLE]

    @Slot()
    def on_dest_input_changed(self) -> None:
        error_type: SearchPaneController.ErrorType | None = None
        if not self.view.dest_input.text():
            error_type = self.ErrorType.EMPTY_DEST
        elif not os.path.isdir(self.view.dest_input.text()):
            error_type = self.ErrorType.DEST_DIR_NOT_EXIST
        elif not os.access(self.view.dest_input.text(), os.W_OK):
            error_type = self.ErrorType.DEST_DIR_NOT_WRITABLE
        self.view.search_button.setEnabled(error_type is None)
        self.show_error_label(error_type)

        if error_type is None and self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_LOAD_LAST_DOWNLOAD_PATH):
            self.resource_manager.config_loader.save_config_key(ConfigKeys.SETTINGS_LAST_DOWNLOAD_PATH, self.view.dest_input.text())

    @Slot()
    def on_browse_button_clicked(self) -> None:
        browse_dir = self.view.dest_input.text()
        if not os.path.isdir(browse_dir) or not os.access(browse_dir, os.W_OK):
            browse_dir = get_system_download_path()
        dest_dir = QFileDialog.getExistingDirectory(self.view, self.dialog_title, browse_dir)
        if dest_dir:
            self.view.dest_input.setText(dest_dir)

    @Slot()
    def on_search_button_clicked(self) -> None:
        self.logger.info("Search button clicked")
        pass

    def show_error_label(self, error_type: ErrorType | None) -> None:
        if error_type is None:
            self.view.input_error_label.hide()
            return
        
        match error_type:
            case self.ErrorType.EMPTY_DEST:
                self.view.input_error_label.setText(self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_INPUT_ERROR_MESSAGE_EMPTY_DEST])
            case self.ErrorType.DEST_DIR_NOT_EXIST:
                self.view.input_error_label.setText(self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_INPUT_ERROR_MESSAGE_DEST_DIR_NOT_EXIST])
            case self.ErrorType.DEST_DIR_NOT_WRITABLE:
                self.view.input_error_label.setText(self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_INPUT_ERROR_MESSAGE_DEST_DIR_NOT_WRITABLE])
        self.view.input_error_label.show()
