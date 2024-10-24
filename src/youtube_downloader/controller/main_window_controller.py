"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import Slot

from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.util.decorator import block_signal
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.data.types.locale import Locale, LocaleKeys

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
        icon = self.resource_manager.media_loader.get_icon()
        self.view.setWindowIcon(icon)
    
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

    def show(self):
        self.view.show()
        self.view.raise_()
        
    def hide(self):
        self.view.hide()

    def close(self):
        self.view.close()
