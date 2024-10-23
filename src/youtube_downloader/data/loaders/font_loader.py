"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, logging

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from youtube_downloader.util.gui import get_default_system_font
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.loaders.config_loader import ConfigLoader, ConfigKeys
from youtube_downloader.util.path import get_font_path, recursive_find

PREFERRED_FONT_FAMILY = "NanumGothic"

class FontLoader():
    def __init__(self, config_loader: ConfigLoader, log_manager: LogManager | None = None):
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.config_loader = config_loader
        self.config_font = self.config_loader.get_config(key=ConfigKeys.SETTINGS_FONT)
        self.registered_font_families = set()
        
        # Assert QApplication is running
        if not QApplication.instance():
            err_str = "QApplication is not running, cannot initialize FontLoader"
            self.logger.error(err_str)
            raise RuntimeError(err_str)
        
        self.register_font_recursive()
        self.logger.debug(f"{len(self.get_all_available_font_families())} font families available")

        if not self.validate_font_family(self.config_font):
            self.logger.warning(f"Invalid font family: {self.config_font}. Using default system font: {get_default_system_font()}")
            self.change_config_font(get_default_system_font())

        if self.config_loader.get_is_first_load():
            if self.validate_font_family(PREFERRED_FONT_FAMILY):
                self.change_config_font(PREFERRED_FONT_FAMILY)
        self.logger.debug(f"Font Loader initialized with config font: {self.config_font}")

    def register_font(self, font_path: str):
        if not os.path.exists(font_path):
            err_str = f"Font file not found: {font_path}"
            self.logger.error(err_str)
            raise FileNotFoundError(err_str)
        
        if not font_path.endswith(".ttf") and not font_path.endswith(".otf"):
            err_str = f"Invalid font file: {font_path} (only .ttf and .otf are supported)"
            self.logger.error(err_str)
            raise TypeError(err_str)
        
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            err_str = f"Failed to register font file: {font_path}"
            self.logger.error(err_str)
            raise RuntimeError(err_str)
    
        self.registered_font_families.add(QFontDatabase.applicationFontFamilies(font_id)[0])

        self.logger.log(logging.NOTSET, f"Registered font file [ID: {font_id}]: {font_path}")

    def register_font_recursive(self):
        font_dir = get_font_path()
        if not os.path.exists(font_dir):
            err_str = f"Font directory not found: {font_dir}"
            self.logger.error(err_str)
            raise FileNotFoundError(err_str)
        
        if not os.path.isdir(font_dir):
            err_str = f"Invalid font directory: {font_dir}"
            self.logger.error(err_str)
            raise TypeError(err_str)
        
        font_files = recursive_find(font_dir, "ttf") + recursive_find(font_dir, "otf")
        for font_file in font_files:
            try:
                self.register_font(font_file)
            except Exception as e:
                self.logger.error(f"Failed to register font file: {font_file}. Error: {e}")

        self.logger.debug(f"Registered {len(self.registered_font_families)} font files")

    def validate_font_family(self, font_family: str) -> bool:
        return font_family in QFontDatabase.families()

    def get_all_available_font_families(self) -> list[str]:
        return QFontDatabase.families()

    def change_config_font(self, font_family: str) -> None:
        if self.validate_font_family(font_family):
            self.config_font = font_family
            self.config_loader.save_config_key(ConfigKeys.SETTINGS_FONT, font_family)
            self.logger.info(f"Changed config font to: {font_family}")
        else:
            err_str = f"Invalid font family: {font_family}"
            self.logger.error(err_str)
            raise ValueError(err_str)
