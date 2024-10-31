"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QShortcut, QKeySequence

from youtube_downloader.util.decorator import block_signal
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.model.settings_proxy import SettingsProxyModel
from youtube_downloader.view.settings_dialog import SettingsDialog
from youtube_downloader.data.types.locale import Locale, LocaleKeys

class SettingsDialogController():
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

        self.config_ui()
        self.bind_model()
        self.refresh_ui()
        self.reset_config_ui()
        self.register_shortcuts()
        self.update_buttons()

    def config_ui(self):
        locale_map = self.resource_manager.locale_loader.get_locale(self.model.get_locale())["components"]
        self.view.settings_list.addItems(locale_map[LocaleKeys.SETTINGS_DIALOG_LIST])

        self.view.restore_button.clicked.connect(self.on_restore_button_clicked)
        self.view.cancel_button.clicked.connect(self.on_cancel_button_clicked)
        self.view.apply_button.clicked.connect(self.on_apply_button_clicked)
        self.view.save_button.clicked.connect(self.on_save_button_clicked)
        self.view.settings_list.currentRowChanged.connect(self.on_settings_group_changed)
        self.view.settings_pane_general.locale_section.language_input.textActivated.connect(self.on_general_locale_language_changed)
        self.view.settings_pane_general.download_section.default_download_path_input.textChanged.connect(self.on_general_download_default_download_path_changed)
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.stateChanged.connect(self.on_general_download_load_last_download_path_changed)
        
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

    def reset_config_ui(self):
        self.view.settings_pane_general.locale_section.language_input.clear()
        self.view.settings_pane_general.locale_section.language_input.addItems(self.language_list)
        locale_snapshot = self.locale_to_lang_map[self.settings_proxy.snapshot_locale]
        self.view.settings_pane_general.locale_section.language_input.setCurrentText(locale_snapshot)
        self.on_general_locale_language_changed(locale_snapshot)

        self.view.settings_pane_general.download_section.default_download_path_input.setText(self.settings_proxy.snapshot_default_download_path)
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.setChecked(self.settings_proxy.snapshot_load_last_download_path)

    def refresh_config_ui(self):
        self.view.settings_pane_general.locale_section.language_input.clear()
        self.view.settings_pane_general.locale_section.language_input.addItems(self.language_list)
        locale = self.locale_to_lang_map[self.settings_proxy.proxy_locale]
        self.view.settings_pane_general.locale_section.language_input.setCurrentText(locale)
        self.on_general_locale_language_changed(locale)

        self.view.settings_pane_general.download_section.default_download_path_input.setText(self.settings_proxy.proxy_default_download_path)
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.setChecked(self.settings_proxy.proxy_load_last_download_path)

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
        self.view.settings_pane_general.download_section.load_last_download_path_checkbox.setText(locale_map[LocaleKeys.SETTINGS_GENERAL_DOWNLOAD_LOAD_LAST_DOWNLOAD_PATH_LABEL])

    @Slot()
    def on_general_locale_language_changed(self, language: str) -> None:
        locale: Locale = self.lang_to_locale_map[language]
        self.settings_proxy.proxy_locale = locale
        self.update_buttons()

    @Slot()
    def on_general_download_default_download_path_changed(self, path: str) -> None:
        self.settings_proxy.proxy_default_download_path = path
        self.update_buttons()

    @Slot()
    def on_general_download_load_last_download_path_changed(self, state: Qt.CheckState) -> None:
        is_checked = state == Qt.CheckState.Checked
        self.settings_proxy.proxy_load_last_download_path = is_checked
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

    @Slot(int)
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

    def exec(self):
        self.view.exec()
