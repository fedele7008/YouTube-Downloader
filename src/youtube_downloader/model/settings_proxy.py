"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import QObject

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.data.types.locale import Locale

class SettingsProxyModel(QObject):
    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager, service_model: YouTubeDownloaderModel):
        super().__init__()
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager
        self.service_model: YouTubeDownloaderModel = service_model

        self.pull_settings()

    def pull_settings(self) -> None:
        self.proxy_locale: Locale = self.service_model.get_locale()
        self.proxy_locale_list: list[Locale] = self.service_model.get_locale_list()
        self.proxy_theme: str = self.service_model.get_theme()
        self.proxy_theme_list: list[str] = self.service_model.get_theme_list()
        self.proxy_debug_mode: bool = self.service_model.get_debug_mode()
        self.proxy_debug_level: str = self.service_model.get_debug_level()
        self.proxy_font: str = self.service_model.get_font()
        self.proxy_font_size: int = self.service_model.get_font_size()
        self.proxy_font_list: list[str] = self.service_model.get_font_list()
        self.proxy_default_download_path: str = self.service_model.get_default_download_path()
        self.proxy_load_last_download_path: bool = self.service_model.get_load_last_download_path()

        self.snapshot_locale: Locale = self.proxy_locale
        self.snapshot_theme: str = self.proxy_theme
        self.snapshot_debug_mode: bool = self.proxy_debug_mode
        self.snapshot_debug_level: str = self.proxy_debug_level
        self.snapshot_font: str = self.proxy_font
        self.snapshot_font_size: int = self.proxy_font_size
        self.snapshot_default_download_path: str = self.proxy_default_download_path
        self.snapshot_load_last_download_path: bool = self.proxy_load_last_download_path

    def push_settings(self) -> None:
        config_changed = 0
        failed = 0
        if self.proxy_locale != self.service_model.get_locale():
            try:
                self.service_model.set_locale(self.proxy_locale)
            except:
                self.service_model.set_locale(self.snapshot_locale)
                self.proxy_locale = self.snapshot_locale
                failed += 1
            config_changed += 1
        if self.proxy_theme != self.service_model.get_theme():
            try:
                self.service_model.set_theme(self.proxy_theme)
            except:
                self.service_model.set_theme(self.snapshot_theme)
                self.proxy_theme = self.snapshot_theme
                failed += 1
            config_changed += 1
        if self.proxy_debug_mode != self.service_model.get_debug_mode():
            try:
                self.service_model.set_debug_mode(self.proxy_debug_mode)
            except:
                self.service_model.set_debug_mode(self.snapshot_debug_mode)
                self.proxy_debug_mode = self.snapshot_debug_mode
                failed += 1
            config_changed += 1
        if self.proxy_debug_level != self.service_model.get_debug_level():
            try:
                self.service_model.set_debug_level(self.proxy_debug_level)
            except:
                self.service_model.set_debug_level(self.snapshot_debug_level)
                self.proxy_debug_level = self.snapshot_debug_level
                failed += 1
            config_changed += 1
        if self.proxy_font != self.service_model.get_font():
            try:
                self.service_model.set_font(self.proxy_font)
            except:
                self.service_model.set_font(self.snapshot_font)
                self.proxy_font = self.snapshot_font
                failed += 1
            config_changed += 1
        if self.proxy_font_size != self.service_model.get_font_size():
            try:
                self.service_model.set_font_size(self.proxy_font_size)
            except:
                self.service_model.set_font_size(self.snapshot_font_size)
                self.proxy_font_size = self.snapshot_font_size
                failed += 1
            config_changed += 1
        if self.proxy_load_last_download_path != self.service_model.get_load_last_download_path():
            try:
                self.service_model.set_load_last_download_path(self.proxy_load_last_download_path)
            except:
                self.service_model.set_load_last_download_path(self.snapshot_load_last_download_path)
                self.proxy_load_last_download_path = self.snapshot_load_last_download_path
                failed += 1
            config_changed += 1
        if self.proxy_default_download_path != self.service_model.get_default_download_path():
            try:
                self.service_model.set_default_download_path(self.proxy_default_download_path, quite=False)
            except:
                self.service_model.set_default_download_path(self.snapshot_default_download_path, quite=False)
                self.proxy_default_download_path = self.snapshot_default_download_path
                failed += 1
            config_changed += 1

        self.logger.info(f"Saved {config_changed} settings.")
        if failed > 0:
            self.logger.warning(f"Failed to save {failed} settings.")

    def restore(self) -> None:
        config_restored = 0
        if self.snapshot_locale != self.service_model.get_locale():
            self.service_model.set_locale(self.snapshot_locale)
            config_restored += 1
        if self.snapshot_theme != self.service_model.get_theme():
            self.service_model.set_theme(self.snapshot_theme)
            config_restored += 1
        if self.snapshot_debug_mode != self.service_model.get_debug_mode():
            self.service_model.set_debug_mode(self.snapshot_debug_mode)
            config_restored += 1
        if self.snapshot_debug_level != self.service_model.get_debug_level():
            self.service_model.set_debug_level(self.snapshot_debug_level)
            config_restored += 1
        if self.snapshot_font != self.service_model.get_font():
            self.service_model.set_font(self.snapshot_font)
            config_restored += 1
        if self.snapshot_font_size != self.service_model.get_font_size():
            self.service_model.set_font_size(self.snapshot_font_size)
            config_restored += 1
        if self.snapshot_load_last_download_path != self.service_model.get_load_last_download_path():
            self.service_model.set_load_last_download_path(self.snapshot_load_last_download_path)
            config_restored += 1
        if self.snapshot_default_download_path != self.service_model.get_default_download_path():
            self.service_model.set_default_download_path(self.snapshot_default_download_path)
            config_restored += 1
        self.logger.info(f"Restored {config_restored} settings")

    def is_dirty_proxy(self) -> bool:
        if self.proxy_locale != self.service_model.get_locale():
            return True
        if self.proxy_theme != self.service_model.get_theme():
            return True
        if self.proxy_debug_mode != self.service_model.get_debug_mode():
            return True
        if self.proxy_debug_level != self.service_model.get_debug_level():
            return True
        if self.proxy_font != self.service_model.get_font():
            return True
        if self.proxy_font_size != self.service_model.get_font_size():
            return True
        if self.proxy_default_download_path != self.service_model.get_default_download_path():
            return True
        if self.proxy_load_last_download_path != self.service_model.get_load_last_download_path():
            return True
        return False
