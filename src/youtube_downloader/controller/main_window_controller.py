"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import platform

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QShortcut, QKeySequence

from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.util.decorator import block_signal
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.data.types.locale import Locale, LocaleKeys
from youtube_downloader.view.settings_dialog import SettingsDialog
from youtube_downloader.view.about_dialog import AboutDialog
from youtube_downloader.view.license_dialog import LicenseDialog
from youtube_downloader.data.log_handlers.gui_handler import QtHandler
from youtube_downloader.data.loaders.config_loader import ConfigKeys
from youtube_downloader.controller.search_pane_controller import SearchPaneController
from youtube_downloader.controller.settings_dialog_controller import SettingsDialogController

class MainWindowController():
    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager, view: MainWindow, model: YouTubeDownloaderModel):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.view: MainWindow = view
        self.model: YouTubeDownloaderModel = model

        self.search_pane_controller: SearchPaneController = SearchPaneController(self.log_manager, self.resource_manager, self.view.search_pane, self.model)

        self.config_ui()
        self.bind_model()
        self.refresh_ui()
        self.register_shortcuts()

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
        self.model.debug_mode_changed.connect(self.on_debug_mode_changed)
        self.model.debug_level_changed.connect(self.on_debug_level_changed)

        gui_log_level = self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_DEBUG_LEVEL)
        gui_handlers: list[QtHandler] = self.log_manager.get_handlers_filter(QtHandler)
        for handler in gui_handlers:
            handler.set_log_level(gui_log_level)
            handler.bind_signal(self.view.log_widget.append)

    def refresh_ui(self):
        self.model.invoke_current_theme_changed()
        self.model.invoke_current_locale_changed()
        self.model.invoke_current_debug_mode_changed()
        self.model.invoke_current_debug_level_changed()
        
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
        if platform.system() == "Darwin":
            self.view.help_menu.setTitle("Help")
        else:
            self.view.help_menu.setTitle(locale_map[LocaleKeys.APP_MENU_HELP_TITLE])

        # Set menu action titles
        if platform.system() == "Darwin":
            self.settings_action.setText("Settings")
            self.quit_action.setText("Quit")
            self.about_action.setText("About")
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
    @block_signal(lambda self: self.view)
    def on_debug_mode_changed(self, debug_mode: bool) -> None:
        self.view.log_widget.setVisible(debug_mode)

    @Slot()
    @block_signal(lambda self: self.view)
    def on_debug_level_changed(self, debug_level: str) -> None:
        self.view.log_widget.clear()
        gui_handlers: list[QtHandler] = self.log_manager.get_handlers_filter(QtHandler)
        for handler in gui_handlers:
            handler.set_log_level(debug_level)
            handler.emit_buffered_messages()

    @Slot()
    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self.view, screen=self.view.screen())
        settings_dialog_controller = SettingsDialogController(self.log_manager, self.resource_manager, settings_dialog, self.model)
        settings_dialog_controller.exec()

    @Slot()
    def open_about_dialog(self):
        about_dialog = AboutDialog(self.view, self.log_manager, self.resource_manager, self.model, screen=self.view.screen())
        about_dialog.exec()

    @Slot()
    def open_license_dialog(self):
        license_dialog = LicenseDialog(self.view, self.log_manager, self.resource_manager, self.model, screen=self.view.screen())
        license_dialog.exec()

    def show(self):
        self.view.show()
        self.view.raise_()
        
    def hide(self):
        self.view.hide()

    def close(self):
        self.view.close()

    def register_shortcuts(self):
        refresh_shortcut = QShortcut(QKeySequence("Ctrl+R"), self.view)
        refresh_shortcut.activated.connect(self.debug_refresh_ui)

    def debug_refresh_ui(self):
        self.logger.debug("UI refreshed")
        self.resource_manager.style_loader.reload_global_style()
        self.refresh_ui()
