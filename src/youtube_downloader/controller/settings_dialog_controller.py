"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os
from enum import Enum

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QFileDialog

from youtube_downloader.util.decorator import block_signal
from youtube_downloader.util.path import get_system_download_path
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.model.settings_proxy import SettingsProxyModel
from youtube_downloader.view.settings_dialog import SettingsDialog
from youtube_downloader.data.types.locale import Locale, LocaleKeys
from youtube_downloader.data.types.log_levels import LogLevel

class SettingsDialogController():
    class PathErrorType(Enum):
        EMPTY_PATH = 0
        PATH_NOT_EXIST = 1
        PATH_NOT_WRITABLE = 2

    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager, view: SettingsDialog, model: YouTubeDownloaderModel):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.view: SettingsDialog = view
        self.model: YouTubeDownloaderModel = model
        self.settings_proxy: SettingsProxyModel = SettingsProxyModel(self.log_manager, self.resource_manager, self.model)

        self.lang_to_locale_map = {}
        self.locale_to_lang_map = {}
        self.language_list = [self.resource_manager.locale_loader.get_locale(locale)["name"] for locale in self.settings_proxy.proxy_locale_list]
        for language, locale in zip(self.language_list, self.settings_proxy.proxy_locale_list):
            self.lang_to_locale_map[language] = locale
            self.locale_to_lang_map[locale] = language

        self.debug_level_list = LogLevel.get_all_members_str()

        self.config_ui()
        self.bind_model()
        self.refresh_ui()
        self.reset_config_ui()
        self.update_buttons()
        self.register_shortcuts()

    def config_ui(self):
        locale_map = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"]
        self.view.settings_list.addItems(locale_map[LocaleKeys.SETTINGS_DIALOG_LIST])
        self.view.settings_list.setCurrentRow(0)

    def bind_model(self):
        self.view.restore_button.clicked.connect(self.on_restore_button_clicked)
        self.view.cancel_button.clicked.connect(self.on_cancel_button_clicked)
        self.view.apply_button.clicked.connect(self.on_apply_button_clicked)
        self.view.save_button.clicked.connect(self.on_save_button_clicked)
        self.view.settings_list.currentRowChanged.connect(self.on_settings_group_changed)
        self.view.settings_pane_general.locale_section.language_input.textActivated.connect(self.on_general_locale_language_changed)
        self.view.settings_pane_general.download_section.default_download_path_input.textChanged.connect(self.on_general_download_default_download_path_changed)
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.stateChanged.connect(self.on_general_download_load_last_download_path_changed)
        self.view.settings_pane_general.download_section.default_download_path_browse_button.clicked.connect(self.on_general_download_default_download_path_browse_button_clicked)
        self.view.settings_pane_advanced.debug_section.debug_mode_checkbox.stateChanged.connect(self.on_advanced_debug_mode_changed)
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.textActivated.connect(self.on_advanced_debug_log_level_changed)
        self.model.locale_changed.connect(self.on_locale_changed)

    def refresh_ui(self):
        self.model.invoke_current_locale_changed()

    def register_shortcuts(self):
        cancel_shortcut = QShortcut(QKeySequence("Esc"), self.view)
        cancel_shortcut.activated.connect(self.on_cancel_button_clicked)

        save_shortcut = QShortcut(QKeySequence("Return"), self.view)
        save_shortcut.activated.connect(self.on_save_button_clicked)

    def reset_config_ui(self):
        self.view.settings_pane_general.locale_section.language_input.clear()
        self.view.settings_pane_general.locale_section.language_input.addItems(self.language_list)
        locale_snapshot = self.locale_to_lang_map[self.settings_proxy.snapshot_locale]
        self.view.settings_pane_general.locale_section.language_input.setCurrentText(locale_snapshot)
        self.on_general_locale_language_changed(locale_snapshot)

        self.view.settings_pane_general.download_section.default_download_path_input.setText(self.settings_proxy.snapshot_default_download_path)
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.setChecked(self.settings_proxy.snapshot_load_last_download_path)

        self.view.settings_pane_advanced.debug_section.debug_mode_checkbox.setChecked(self.settings_proxy.snapshot_debug_mode)
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.clear()
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.addItems(self.debug_level_list)
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.setCurrentText(self.settings_proxy.snapshot_debug_level)
        self.on_advanced_debug_log_level_changed(self.settings_proxy.snapshot_debug_level)

    def refresh_config_ui(self):
        self.view.settings_pane_general.locale_section.language_input.clear()
        self.view.settings_pane_general.locale_section.language_input.addItems(self.language_list)
        locale = self.locale_to_lang_map[self.settings_proxy.proxy_locale]
        self.view.settings_pane_general.locale_section.language_input.setCurrentText(locale)
        self.on_general_locale_language_changed(locale)

        self.view.settings_pane_general.download_section.default_download_path_input.setText(self.settings_proxy.proxy_default_download_path)
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.setChecked(self.settings_proxy.proxy_load_last_download_path)

        self.view.settings_pane_advanced.debug_section.debug_mode_checkbox.setChecked(self.settings_proxy.proxy_debug_mode)
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.clear()
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.addItems(self.debug_level_list)
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.setCurrentText(self.settings_proxy.proxy_debug_level)
        self.on_advanced_debug_log_level_changed(self.settings_proxy.proxy_debug_level)

    @Slot()
    @block_signal(lambda self: self.view)
    def on_locale_changed(self, locale: Locale) -> None:
        locale_map = self.resource_manager.locale_loader.get_locale(locale)["components"]
        for i in range(self.view.settings_list.count()):
            self.view.settings_list.item(i).setText(locale_map[LocaleKeys.SETTINGS_DIALOG_LIST][i])

        self.view.restore_button.setText(locale_map[LocaleKeys.SETTINGS_DIALOG_RESTORE_BUTTON])
        self.view.cancel_button.setText(locale_map[LocaleKeys.SETTINGS_DIALOG_CANCEL_BUTTON])
        self.view.apply_button.setText(locale_map[LocaleKeys.SETTINGS_DIALOG_APPLY_BUTTON])
        self.view.save_button.setText(locale_map[LocaleKeys.SETTINGS_DIALOG_SAVE_BUTTON])

        self.view.settings_pane_general.locale_section.title_label.setText(locale_map[LocaleKeys.SETTINGS_GENERAL_LOCALE_TITLE])
        self.view.settings_pane_general.locale_section.language_label.setText(locale_map[LocaleKeys.SETTINGS_GENERAL_LOCALE_LANGUAGE_LABEL])
        self.view.settings_pane_general.download_section.title_label.setText(locale_map[LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_TITLE])
        self.view.settings_pane_general.download_section.default_download_path_label.setText(locale_map[LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_LABEL])
        self.view.settings_pane_general.download_section.default_download_path_browse_button.setText(locale_map[LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_BROWSE_BUTTON])
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.setText(locale_map[LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_LOAD_LAST_DOWNLOAD_PATH_LABEL])

        self.on_general_download_default_download_path_changed(self.settings_proxy.proxy_default_download_path)

        self.view.settings_pane_advanced.debug_section.title_label.setText(locale_map[LocaleKeys.SETTINGS_ADVANCED_DEBUG_TITLE])
        self.view.settings_pane_advanced.debug_section.debug_mode_checkbox.setText(locale_map[LocaleKeys.SETTINGS_ADVANCED_DEBUG_MODE_LABEL])
        self.view.settings_pane_advanced.debug_section.debug_log_level_label.setText(locale_map[LocaleKeys.SETTINGS_ADVANCED_DEBUG_LOG_LEVEL_LABEL])

    @Slot()
    def on_general_locale_language_changed(self, language: str) -> None:
        locale: Locale = self.lang_to_locale_map[language]
        self.settings_proxy.proxy_locale = locale
        self.update_buttons()

    @Slot()
    def on_general_download_default_download_path_changed(self, path: str) -> None:
        self.settings_proxy.proxy_default_download_path = path
        self.update_buttons()
        
        error_type: SettingsDialogController.PathErrorType | None = None
        if not path:
            error_type = self.PathErrorType.EMPTY_PATH
        elif not os.path.isdir(path):
            error_type = self.PathErrorType.PATH_NOT_EXIST
        elif not os.access(path, os.W_OK):
            error_type = self.PathErrorType.PATH_NOT_WRITABLE
        self.show_error_label(error_type)

    @Slot()
    def on_general_download_default_download_path_browse_button_clicked(self):
        browse_dir = get_system_download_path()
        browse_title = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_BROWSE_DIALOG_TITLE]
        default_download_path = QFileDialog.getExistingDirectory(self.view.settings_pane_general.download_section, browse_title, browse_dir)
        if default_download_path:
            self.view.settings_pane_general.download_section.default_download_path_input.setText(default_download_path)

    @Slot()
    def on_advanced_debug_mode_changed(self, state: Qt.CheckState) -> None:
        self.settings_proxy.proxy_debug_mode = state == Qt.CheckState.Checked.value
        self.view.settings_pane_advanced.debug_section.debug_log_level_label.setEnabled(self.settings_proxy.proxy_debug_mode)
        self.view.settings_pane_advanced.debug_section.debug_log_level_input.setEnabled(self.settings_proxy.proxy_debug_mode)
        self.update_buttons()

    @Slot()
    def on_advanced_debug_log_level_changed(self, debug_log_level: str) -> None:
        self.settings_proxy.proxy_debug_level = debug_log_level
        self.update_buttons()

    @Slot()
    def on_general_download_load_last_download_path_changed(self, state: Qt.CheckState) -> None:
        self.settings_proxy.proxy_load_last_download_path = state == Qt.CheckState.Checked.value
        self.update_buttons()

    @Slot()
    def on_restore_button_clicked(self) -> None:
        self.reset_config_ui()
        
    @Slot()
    def on_cancel_button_clicked(self) -> None:
        self.settings_proxy.restore()
        self.view.close()

    @Slot()
    def on_apply_button_clicked(self) -> None:
        self.settings_proxy.push_settings()
        self.refresh_config_ui()
        self.update_buttons()

    @Slot()
    def on_save_button_clicked(self) -> None:
        self.settings_proxy.push_settings()
        self.view.close()

    @Slot()
    def on_settings_group_changed(self, index: int) -> None:
        self.view.settings_pane.setCurrentIndex(index)

    def update_buttons(self) -> None:
        if self.settings_proxy.is_dirty_proxy():
            self.view.apply_button.setProperty("class", "neutral")
        else:
            self.view.apply_button.setProperty("class", "neutral-hollow")
        self.view.apply_button.setEnabled(self.settings_proxy.is_dirty_proxy())
        self.view.apply_button.style().unpolish(self.view.apply_button)
        self.view.apply_button.style().polish(self.view.apply_button)

    def show_error_label(self, error_type: PathErrorType | None) -> None:
        if error_type is None:
            self.view.settings_pane_general.download_section.default_download_path_error_label.hide()
            return
        
        match error_type:
            case self.PathErrorType.EMPTY_PATH:
                msg = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_ERROR_NOT_SET]
                self.view.settings_pane_general.download_section.default_download_path_error_label.setText(msg.format(path=self.settings_proxy.snapshot_default_download_path))
            case self.PathErrorType.PATH_NOT_EXIST:
                msg = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_ERROR_NOT_EXIST]
                self.view.settings_pane_general.download_section.default_download_path_error_label.setText(msg.format(path=self.settings_proxy.snapshot_default_download_path))
            case self.PathErrorType.PATH_NOT_WRITABLE:
                msg = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"][LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_ERROR_NOT_WRITABLE]
                self.view.settings_pane_general.download_section.default_download_path_error_label.setText(msg.format(path=self.settings_proxy.snapshot_default_download_path))
        self.view.settings_pane_general.download_section.default_download_path_error_label.show()


    def exec(self):
        self.view.exec()
