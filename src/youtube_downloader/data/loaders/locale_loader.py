"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, json

from youtube_downloader.data.types.locale import Locale
from youtube_downloader.data.loaders.config_loader import ConfigLoader, ConfigKeys
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.util.path import get_locale_path

class LocaleLoader():
    def __init__(self, config_loader: ConfigLoader, log_manager: LogManager | None = None):
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.config_loader = config_loader
        config_locale = self.config_loader.get_config(key=ConfigKeys.SETTINGS_LOCALE)
        if Locale.validate_str(config_locale):
            self.config_locale = Locale.parse_str(config_locale)
        else:
            self.logger.warning(f"Invalid locale: {config_locale}. Using default locale: {Locale.get_default()}")
            self.config_locale = Locale.get_default()
            self.config_loader.save_config_key(key=ConfigKeys.SETTINGS_LOCALE, value=self.config_locale.to_str())
        self.locales = {}
        self.load_locales()
        self.logger.info(f"Locales available: {[x.to_str() for x in self.get_all_available_locales()]}")
        self.logger.debug(f"Locale Loader initialized with config locale: {self.config_locale}")

    def load_locales(self):
        locale_path = get_locale_path()
        locale_files = {}
        available_locales: list[Locale] = Locale.get_all_members()
        for locale in available_locales:
            file_name = f"{locale.to_str()}.json"
            file_path = os.path.join(locale_path, file_name)
            if os.path.exists(file_path):
                locale_files[locale] = file_path
            else:
                err_str = f"Locale file not found: {file_path}"
                self.logger.error(err_str)
                raise FileNotFoundError(err_str)
            
        for locale, file_path in locale_files.items():
            with open(file_path, "r", encoding="utf-8") as f:
                locale_data = json.load(f)
                self.locales[locale] = locale_data
                self.logger.debug(f"Loaded locale: {file_path}")

    def get_locale(self, locale: Locale) -> dict:
        return self.locales[locale]
    
    def get_all_available_locales(self) -> list[Locale]:
        return list(self.locales.keys())
    
    def get_config_locale(self) -> Locale:
        return self.config_locale
    
    def set_config_locale(self, locale: Locale) -> None:
        if self.config_locale != locale:
            self.config_locale = locale
            self.config_loader.save_config_key(key=ConfigKeys.SETTINGS_LOCALE, value=self.config_locale.to_str())
