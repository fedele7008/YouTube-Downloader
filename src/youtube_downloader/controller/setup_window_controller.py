"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import Slot

from youtube_downloader.controller.main_window_controller import MainWindowController
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.setup_window import SetupWindow
from youtube_downloader.data.types.locale import Locale, LocaleKeys
from youtube_downloader.util.decorator import block_signal
from youtube_downloader.util.gui import center_widget_on_screen

class SetupWindowController():
    def __init__(self,
                 log_manager: LogManager | None,
                 resource_manager: ResourceManager,
                 view: SetupWindow,
                 model: YouTubeDownloaderModel,
                 main_controller: MainWindowController):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.view: SetupWindow = view
        self.model: YouTubeDownloaderModel = model
        self.main_controller: MainWindowController = main_controller

        self.config_ui()
        self.bind_model()
        self.refresh_ui()

    def config_ui(self):
        icon = self.resource_manager.media_loader.get_icon()
        self.view.setWindowIcon(icon)

    def bind_model(self):
        self.model.theme_changed.connect(self.on_theme_changed)
        self.view.setup_config_theme_selector.textActivated.connect(self.on_theme_selected)
        self.model.locale_changed.connect(self.on_locale_changed)
        self.view.setup_config_language_selector.textActivated.connect(self.on_locale_selected)
        self.view.setup_start_button.clicked.connect(self.on_start_button_clicked)
        
    def refresh_ui(self):
        locale_list = self.model.get_locale_list()
        self.view.setup_config_language_selector.addItems([locale.to_str() for locale in locale_list])
        
        theme_list = self.model.get_theme_list()
        self.view.setup_config_theme_selector.addItems(theme_list)

        self.model.invoke_current_theme_changed()
        self.model.invoke_current_locale_changed()

    @Slot()
    @block_signal(lambda self: self.view)
    def on_theme_changed(self, theme: str) -> None:
        theme_str = self.resource_manager.style_loader.get_style()
        self.view.setStyleSheet(theme_str)
        self.view.setup_config_theme_selector.setCurrentText(self.model.get_theme())
        
    @Slot()
    @block_signal(lambda self: self.view)
    def on_locale_changed(self, locale: Locale) -> None:
        locale_map = self.resource_manager.locale_loader.get_locale(locale)["components"]
        self.view.setWindowTitle(locale_map[LocaleKeys.SETUP_WINDOW_TITLE])
        self.view.setup_welcome_label.setText(locale_map[LocaleKeys.SETUP_WINDOW_WELCOME_LABEL])
        self.view.setup_config_language_label.setText(locale_map[LocaleKeys.SETUP_WINDOW_LANGUAGE_LABEL])
        self.view.setup_config_theme_label.setText(locale_map[LocaleKeys.SETUP_WINDOW_THEME_LABEL])
        self.view.setup_start_button.setText(locale_map[LocaleKeys.SETUP_WINDOW_START_BUTTON])
        self.view.setup_config_language_selector.setCurrentText(self.model.get_locale().to_str())

    @Slot()
    def on_theme_selected(self, theme: str) -> None:
        self.model.set_theme(theme)

    @Slot()
    def on_locale_selected(self, locale: str) -> None:
        locale_enum = Locale.parse_str(locale)
        self.model.set_locale(locale_enum)

    @Slot()
    def on_start_button_clicked(self) -> None:
        self.main_controller.show()
        center_widget_on_screen(self.main_controller.view, self.view.screen())
        self.close()

    def show(self):
        self.view.show()
        self.view.raise_()

    def hide(self):
        self.view.hide()

    def close(self):
        self.view.close()
