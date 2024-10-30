"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import Slot
from PySide6.QtGui import QShortcut, QKeySequence

from youtube_downloader.util.decorator import block_signal
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.settings_dialog import SettingsDialog
from youtube_downloader.data.types.locale import Locale, LocaleKeys

class SettingsDialogController():
    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager, view: SettingsDialog, model: YouTubeDownloaderModel):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.view: SettingsDialog = view
        self.model: YouTubeDownloaderModel = model

        self.config_ui()
        self.bind_model()
        self.refresh_ui()
        self.register_shortcuts()

    def config_ui(self):
        locale_map = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"]
        self.view.settings_list.addItems(locale_map[LocaleKeys.SETTINGS_DIALOG_LIST])

        self.view.restore_button.clicked.connect(self.on_restore_button_clicked)
        self.view.cancel_button.clicked.connect(self.on_cancel_button_clicked)
        self.view.apply_button.clicked.connect(self.on_apply_button_clicked)
        self.view.save_button.clicked.connect(self.on_save_button_clicked)
        self.view.settings_list.currentRowChanged.connect(self.on_settings_group_changed)
        
        self.view.settings_list.setCurrentRow(0)

    def bind_model(self):
        self.model.locale_changed.connect(self.on_locale_changed)

    def refresh_ui(self):
        self.model.invoke_current_locale_changed()

    def register_shortcuts(self):
        cancel_shortcut = QShortcut(QKeySequence("Esc"), self.view)
        cancel_shortcut.activated.connect(self.on_cancel_button_clicked)

        save_shortcut = QShortcut(QKeySequence("Return"), self.view)
        save_shortcut.activated.connect(self.on_save_button_clicked)

    @Slot()
    @block_signal(lambda self: self.view)
    def on_locale_changed(self, locale: Locale) -> None:
        locale_map = self.resource_manager.locale_loader.get_locale(locale)["components"]
        for i in range(self.view.settings_list.count()):
            self.view.settings_list.item(i).setText(locale_map[LocaleKeys.SETTINGS_DIALOG_LIST][i])

    @Slot()
    def on_restore_button_clicked(self) -> None:
        self.logger.info("Restore button clicked")

    @Slot()
    def on_cancel_button_clicked(self) -> None:
        self.logger.info("Cancel button clicked")
        self.view.close()

    @Slot()
    def on_apply_button_clicked(self) -> None:
        self.logger.info("Apply button clicked")

    @Slot()
    def on_save_button_clicked(self) -> None:
        self.logger.info("Save button clicked")
        self.view.close()

    @Slot(int)
    def on_settings_group_changed(self, index: int) -> None:
        self.logger.info(f"Settings group changed: {index}")

    def exec(self):
        self.view.exec()
