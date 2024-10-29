"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import platform

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction

from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.util.decorator import block_signal
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.data.types.locale import Locale, LocaleKeys
from youtube_downloader.view.settings_dialog import SettingsDialog
from youtube_downloader.view.about_dialog import AboutDialog
from youtube_downloader.view.license_dialog import LicenseDialog

class MainWindowController():
    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager, view: MainWindow, model: YouTubeDownloaderModel):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.view: MainWindow = view
        self.model: YouTubeDownloaderModel = model

        self.config_ui()
        self.bind_model()
        self.refresh_ui()

    def config_ui(self):
        main_icon = self.resource_manager.media_loader.get_icon()
        self.view.setWindowIcon(main_icon)

        self.settings_action = QAction(self.view)
        self.settings_action.setShortcut("Ctrl+P")
        self.settings_action.triggered.connect(self.open_settings_dialog)
        self.view.settings_menu.addAction(self.settings_action)

        self.quit_action = QAction(self.view)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)
        self.view.actions_menu.addAction(self.quit_action)

        self.about_action = QAction(self.view)
        self.about_action.triggered.connect(self.open_about_dialog)
        self.view.help_menu.addAction(self.about_action)
        
        self.license_action = QAction(self.view)
        self.license_action.triggered.connect(self.open_license_dialog)
        self.view.help_menu.addAction(self.license_action)
    
    def bind_model(self):
        self.model.theme_changed.connect(self.on_theme_changed)
        self.model.locale_changed.connect(self.on_locale_changed)

    def refresh_ui(self):
        self.model.invoke_current_theme_changed()
        self.model.invoke_current_locale_changed()
        
    @Slot()
    @block_signal(lambda self: self.view)
    def on_theme_changed(self, theme: str) -> None:
        theme_str = self.resource_manager.style_loader.get_style()
        self.view.setStyleSheet(theme_str)

    @Slot()
    @block_signal(lambda self: self.view)
    def on_locale_changed(self, locale: Locale) -> None:
        locale_map = self.resource_manager.locale_loader.get_locale(locale)["components"]
        self.view.setWindowTitle(locale_map[LocaleKeys.APP_NAME])

        # Set menu titles
        self.view.settings_menu.setTitle(locale_map[LocaleKeys.APP_MENU_SETTINGS_TITLE])
        self.view.actions_menu.setTitle(locale_map[LocaleKeys.APP_MENU_ACTIONS_TITLE])
        self.view.help_menu.setTitle(locale_map[LocaleKeys.APP_MENU_HELP_TITLE])

        # Set menu action titles
        if platform.system() == "Darwin":
            self.settings_action.setText("Settings")
        else:
            self.settings_action.setText(locale_map[LocaleKeys.APP_MENU_SETTINGS_GENERAL_TITLE])

        self.quit_action.setText(locale_map[LocaleKeys.APP_MENU_ACTIONS_QUIT_TITLE])
        self.about_action.setText(locale_map[LocaleKeys.APP_MENU_HELP_ABOUT_TITLE])
        self.license_action.setText(locale_map[LocaleKeys.APP_MENU_HELP_LICENSE_TITLE])

        # Set menu action status tips
        self.settings_action.setStatusTip(locale_map[LocaleKeys.APP_MENU_SETTINGS_GENERAL_STATUS_TIP])
        self.quit_action.setStatusTip(locale_map[LocaleKeys.APP_MENU_ACTIONS_QUIT_STATUS_TIP])
        self.about_action.setStatusTip(locale_map[LocaleKeys.APP_MENU_HELP_ABOUT_STATUS_TIP])
        self.license_action.setStatusTip(locale_map[LocaleKeys.APP_MENU_HELP_LICENSE_STATUS_TIP])
    
    @Slot()
    def open_settings_dialog(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec()

    @Slot()
    def open_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

    @Slot()
    def open_license_dialog(self):
        license_dialog = LicenseDialog()
        license_dialog.exec()

    def show(self):
        self.view.show()
        self.view.raise_()
        
    def hide(self):
        self.view.hide()

    def close(self):
        self.view.close()
