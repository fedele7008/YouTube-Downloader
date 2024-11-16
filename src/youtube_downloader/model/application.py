"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os

from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtWidgets import QApplication

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.data.types.locale import Locale
from youtube_downloader.data.loaders.config_loader import ConfigKeys
from youtube_downloader.data.types.log_levels import LogLevel

class YouTubeDownloaderModel(QObject):
    locale_changed = Signal(Locale)
    theme_changed = Signal(str)
    debug_mode_changed = Signal(bool)
    debug_level_changed = Signal(str)
    font_changed = Signal(str)
    font_size_changed = Signal(int)
    default_download_path_changed = Signal(str)
    last_download_path_changed = Signal(str)
    load_last_download_path_changed = Signal(bool)
    
    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager):
        super().__init__()
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager
        self.clipboard = QApplication.clipboard()

    def get_ffmpeg_location(self) -> str:
        return self.resource_manager.binary_loader.get_ffmpeg_location()

    def get_theme_list(self) -> list[str]:
        return self.resource_manager.style_loader.get_all_available_themes()
    
    def get_locale_list(self) -> list[Locale]:
        return self.resource_manager.locale_loader.get_all_available_locales()
    
    def get_font_list(self) -> list[str]:
        return self.resource_manager.font_loader.get_all_available_font_families()

    def get_theme(self) -> str:
        return self.resource_manager.style_loader.get_config_theme()
    
    def get_locale(self) -> Locale:
        return self.resource_manager.locale_loader.get_config_locale()
    
    def get_debug_mode(self) -> bool:
        return self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_DEBUG_MODE)
    
    def get_debug_level(self) -> str:
        return self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_DEBUG_LEVEL)
    
    def get_font(self) -> str:
        return self.resource_manager.font_loader.get_config_font()
    
    def get_font_size(self) -> int:
        return self.resource_manager.font_loader.get_config_font_size()
    
    def get_default_download_path(self) -> str:
        return self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_STANDARD_DOWNLOAD_PATH).replace("\\", "/")
    
    def get_last_download_path(self) -> str:
        return self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_LAST_DOWNLOAD_PATH).replace("\\", "/")
    
    def get_load_last_download_path(self) -> bool:
        return self.resource_manager.config_loader.get_config(ConfigKeys.SETTINGS_LOAD_LAST_DOWNLOAD_PATH)

    def validate_path(self, path: str) -> bool:
        if not os.path.isdir(path):
            return False
        elif not os.access(path, os.W_OK):
            return False
        return True

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

    @Slot()
    def set_debug_mode(self, debug_mode: bool) -> None:
        if debug_mode != self.get_debug_mode():
            self.resource_manager.config_loader.save_config_key(ConfigKeys.SETTINGS_DEBUG_MODE, debug_mode)
            self.debug_mode_changed.emit(debug_mode)
            self.logger.info(f"Debug mode toggled to: {debug_mode}")

    @Slot()
    def set_debug_level(self, debug_level: str) -> None:
        if debug_level != self.get_debug_level():
            if not LogLevel.validate_str(debug_level):
                err_str = f"Invalid debug level: {debug_level}. Aborting the change."
                self.logger.error(err_str)
                raise ValueError(err_str)
            self.resource_manager.config_loader.save_config_key(ConfigKeys.SETTINGS_DEBUG_LEVEL, debug_level)
            self.debug_level_changed.emit(debug_level)
            self.logger.info(f"Debug level changed to: {debug_level}")

    @Slot()
    def set_font(self, font: str) -> None:
        if font != self.get_font():
            self.resource_manager.font_loader.change_config_font(font)
            self.font_changed.emit(font)
            self.logger.info(f"Font changed to: {font}")
            
    @Slot()
    def set_font_size(self, font_size: int) -> None:
        if font_size != self.get_font_size():
            self.resource_manager.font_loader.set_config_font_size(font_size)
            self.font_size_changed.emit(font_size)
            self.logger.info(f"Font size changed to: {font_size}")
            
    @Slot()
    def set_default_download_path(self, default_download_path: str, quite: bool = True) -> None:
        if default_download_path != self.get_default_download_path():
            if not self.validate_path(default_download_path):
                err_str = f"Invalid default download path: {default_download_path}. Aborting the change."
                self.logger.error(err_str)
                raise ValueError(err_str)
            self.resource_manager.config_loader.save_config_key(ConfigKeys.SETTINGS_STANDARD_DOWNLOAD_PATH, default_download_path)
            if not quite:
                self.default_download_path_changed.emit(default_download_path)
            self.logger.info(f"Default download path changed to: {default_download_path}")

    @Slot()
    def set_last_download_path(self, last_download_path: str, quite: bool = True) -> None:
        if last_download_path != self.get_last_download_path():
            if not self.validate_path(last_download_path):
                err_str = f"Invalid last download path: {last_download_path}. Aborting the change."
                self.logger.error(err_str)
                raise ValueError(err_str)
            self.resource_manager.config_loader.save_config_key(ConfigKeys.SETTINGS_LAST_DOWNLOAD_PATH, last_download_path)
            if not quite:
                self.last_download_path_changed.emit(last_download_path)
            self.logger.info(f"Last download path changed to: {last_download_path}")

    @Slot()
    def set_load_last_download_path(self, load_last_download_path: bool) -> None:
        if load_last_download_path != self.get_load_last_download_path():
            self.resource_manager.config_loader.save_config_key(ConfigKeys.SETTINGS_LOAD_LAST_DOWNLOAD_PATH, load_last_download_path)
            self.load_last_download_path_changed.emit(load_last_download_path)
            self.logger.info(f"Load last download path toggled to: {load_last_download_path}")

    def invoke_current_locale_changed(self) -> None:
        self.locale_changed.emit(self.get_locale())

    def invoke_current_theme_changed(self) -> None:
        self.theme_changed.emit(self.get_theme())

    def invoke_current_debug_mode_changed(self) -> None:
        self.debug_mode_changed.emit(self.get_debug_mode())

    def invoke_current_debug_level_changed(self) -> None:
        self.debug_level_changed.emit(self.get_debug_level())

    def invoke_current_font_changed(self) -> None:
        self.font_changed.emit(self.get_font())

    def invoke_current_font_size_changed(self) -> None:
        self.font_size_changed.emit(self.get_font_size())

    def invoke_current_default_download_path_changed(self) -> None:
        self.default_download_path_changed.emit(self.get_default_download_path())

    def invoke_current_last_download_path_changed(self) -> None:
        self.last_download_path_changed.emit(self.get_last_download_path())

    def invoke_current_load_last_download_path_changed(self) -> None:
        self.load_last_download_path_changed.emit(self.get_load_last_download_path())

    theme = Property(str, get_theme, set_theme, notify=theme_changed)
    locale = Property(Locale, get_locale, set_locale, notify=locale_changed)
    debug_mode = Property(bool, get_debug_mode, set_debug_mode, notify=debug_mode_changed)
    debug_level = Property(str, get_debug_level, set_debug_level, notify=debug_level_changed)
    font = Property(str, get_font, set_font, notify=font_changed)
    font_size = Property(int, get_font_size, set_font_size, notify=font_size_changed)
    default_download_path = Property(str, get_default_download_path, set_default_download_path, notify=default_download_path_changed)
    last_download_path = Property(str, get_last_download_path, set_last_download_path, notify=last_download_path_changed)
    load_last_download_path = Property(bool, get_load_last_download_path, set_load_last_download_path, notify=load_last_download_path_changed)
