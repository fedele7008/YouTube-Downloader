"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import QObject, Property, Signal, Slot

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.data.types.locale import Locale

class YouTubeDownloaderModel(QObject):
    locale_changed = Signal(Locale)
    theme_changed = Signal(str)
    
    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager):
        super().__init__()
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

    def get_theme_list(self) -> list[str]:
        return self.resource_manager.style_loader.get_all_available_themes()
    
    def get_locale_list(self) -> list[Locale]:
        return self.resource_manager.locale_loader.get_all_available_locales()

    def get_theme(self) -> str:
        return self.resource_manager.style_loader.get_config_theme()
    
    def get_locale(self) -> Locale:
        return self.resource_manager.locale_loader.get_config_locale()
    
    @Slot()
    def set_theme(self, theme: str) -> None:
        if theme in self.get_theme_list() and theme != self.get_theme():
            self.resource_manager.style_loader.change_config_theme(theme)
            self.theme_changed.emit(theme)
            self.logger.info(f"Theme changed to: {theme}")

    @Slot()
    def set_locale(self, locale: Locale) -> None:
        if locale in self.get_locale_list() and locale != self.get_locale():
            self.resource_manager.locale_loader.set_config_locale(locale)
            self.locale_changed.emit(locale)
            self.logger.info(f"Locale changed to: {locale}")

    def invoke_current_locale_changed(self) -> None:
        self.locale_changed.emit(self.get_locale())

    def invoke_current_theme_changed(self) -> None:
        self.theme_changed.emit(self.get_theme())

    theme = Property(str, get_theme, set_theme, notify=theme_changed)
    locale = Property(Locale, get_locale, set_locale, notify=locale_changed)
