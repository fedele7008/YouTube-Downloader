"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os
from enum import Enum

from PySide6.QtCore import Slot, Qt, QRegularExpression, QThreadPool
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QCursor

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.search_pane import SearchPane
from youtube_downloader.data.types.locale import Locale, LocaleKeys
from youtube_downloader.util.decorator import block_signal
from youtube_downloader.util.path import get_system_download_path
from youtube_downloader.view.error_dialog import ErrorDialog
from youtube_downloader.view.result_dialog import ResultDialog
from youtube_downloader.controller.result_dialog_controller import ResultDialogController
from youtube_downloader.worker.search_worker import SearchWorker

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

        self.quick_paste_search = False
        self.search_in_progress = False

        self.config_ui()
        self.bind_model()
        self.refresh_ui()

    def config_ui(self):
        self.dialog_title = str()
        
        if self.model.get_load_last_download_path():
            self.view.dest_input.setText(self.model.get_last_download_path())
        else:
            self.view.dest_input.setText(self.model.get_default_download_path())

        self.view.browse_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.view.search_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def bind_model(self):
        self.model.locale_changed.connect(self.on_locale_changed)
        self.model.default_download_path_changed.connect(self.on_default_download_path_changed)
        self.view.dest_input.textChanged.connect(self.on_dest_input_changed)
        self.view.browse_button.clicked.connect(self.on_browse_button_clicked)
        self.view.search_button.clicked.connect(self.on_search_button_clicked)
        self.view.url_input.returnPressed.connect(self.on_search_button_clicked)
        self.model.clipboard.dataChanged.connect(self.on_clipboard_changed)

    def refresh_ui(self):
        self.model.invoke_current_locale_changed()
        self.on_dest_input_changed()

    @Slot()
    @block_signal(lambda self: self.view)
    def on_locale_changed(self, locale: Locale) -> None:
        locale_map = self.resource_manager.locale_loader.get_locale(locale)["components"]
        self.view.url_label.setText(locale_map[LocaleKeys.SEARCH_PANE_URL_LABEL])
        self.update_url_input_placeholder()
        self.view.dest_label.setText(locale_map[LocaleKeys.SEARCH_PANE_DEST_LABEL])
        self.view.browse_button.setText(locale_map[LocaleKeys.SEARCH_PANE_BROWSE_BUTTON])
        self.view.search_button.setText(locale_map[LocaleKeys.SEARCH_PANE_SEARCH_BUTTON])
        self.dialog_title = locale_map[LocaleKeys.SEARCH_PANE_BROWSE_DIALOG_TITLE]
        self.on_dest_input_changed()

    @Slot()
    def on_default_download_path_changed(self, default_download_path: str) -> None:
        if not self.model.get_load_last_download_path():
            self.view.dest_input.setText(default_download_path)

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

        if error_type is None:
            self.model.set_last_download_path(self.view.dest_input.text(), quite=True)

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
        if not self.view.search_button.isEnabled():
            return
        
        if self.search_in_progress:
            return
        
        self.search_text = self.view.url_input.text().strip()

        if not self.search_text:
            if self.quick_paste_search:
                self.search_text = self.model.clipboard.text().strip()
            else:
                title = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_INPUT_ERROR_PROMPT_TITLE]
                message = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_INPUT_ERROR_PROMPT_MESSAGE_EMPTY_URL]
                self.logger.error(f"Searching for video with empty URL: {self.search_text}")
                ErrorDialog.prompt(self.view, title, message)
                return

        self.logger.info(f"Searching for video with URL: {self.search_text}")
        self.search_in_progress = True
        self.view.search_button.setEnabled(False)

        cache = self.resource_manager.cache_loader.get(self.search_text)
        if cache:
            self.on_search_worker_success(cache)
            return

        self.search_worker = SearchWorker(self.log_manager, self.model, self.search_text)
        self.search_worker.signals.success.connect(self.on_search_worker_success)
        self.search_worker.signals.error.connect(self.on_search_worker_error)
        QThreadPool.globalInstance().start(self.search_worker)

    @Slot(dict)
    def on_search_worker_success(self, video_data: dict) -> None:
        self.logger.debug(f"Search worker success: {video_data.get('title', 'No title')}")
        self.resource_manager.cache_loader.add(self.search_text, video_data)
        try:
            self.result_dialog = ResultDialog(parent=self.view, screen=self.view.screen())
            self.result_dialog_controller = ResultDialogController(self.log_manager, self.resource_manager, self.result_dialog, self.model, video_data)
            self.result_dialog_controller.exec()
        except Exception as e:
            self.logger.error(f"Error displaying result dialog: {e}")
        self.search_in_progress = False
        self.view.search_button.setEnabled(True)

    @Slot(Exception)
    def on_search_worker_error(self, e: Exception) -> None:
        self.logger.error(f"Search worker error: {e}")
        title = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_INPUT_ERROR_PROMPT_TITLE]
        message = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_INPUT_ERROR_PROMPT_MESSAGE_INVALID_VIDEO]
        ErrorDialog.prompt(self.view, title, message)
        self.search_in_progress = False
        self.view.search_button.setEnabled(True)

    @Slot()
    def on_clipboard_changed(self):
        self.update_url_input_placeholder()

    def update_url_input_placeholder(self):
        clipboard_text = self.model.clipboard.text().strip()
        if clipboard_text:
            pattern = QRegularExpression(r"^(https:\/\/youtu\.be\/|https:\/\/www\.youtube\.com\/watch\?v=.+).*")
            match = pattern.match(clipboard_text)
            if match.hasMatch():
                self.view.url_input.setPlaceholderText(clipboard_text)
                self.quick_paste_search = True
                return
        self.view.url_input.setPlaceholderText(self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SEARCH_PANE_URL_INPUT_PLACEHOLDER])
        self.quick_paste_search = False

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
