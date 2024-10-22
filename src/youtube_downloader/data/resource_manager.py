"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Callable, Any

from youtube_downloader.data.loaders.config_loader import ConfigLoader
from youtube_downloader.data.loaders.binary_loader import BinaryLoader
from youtube_downloader.data.loaders.font_loader import FontLoader
from youtube_downloader.data.loaders.style_loader import StyleLoader
from youtube_downloader.data.loaders.locale_loader import LocaleLoader
from youtube_downloader.data.loaders.media_loader import MediaLoader
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.types.locale import Locale

class ResourceManager():
    def __init__(self, log_manager: LogManager | None = None, hook: Callable[[float, str, int, Any, Any], Any] | None = None):
        # Set logger
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.progress_hook = hook
        
        # Initialize binary loader
        self.binary_loader = self.progress_hook(100 / 6, "Loading ffmpeg binary", 700, BinaryLoader, self.log_manager) if hook else BinaryLoader(self.log_manager)

        # Initialize config loader
        self.config_loader = self.progress_hook(100 / 6 * 2, f"Loading config", 300, ConfigLoader, self.log_manager) if hook else ConfigLoader(self.log_manager)

        # Initialize font loader
        self.font_loader = self.progress_hook(100 / 6 * 3, f"Loading fonts", 300, FontLoader, self.config_loader, self.log_manager) if hook else FontLoader(self.config_loader, self.log_manager)

        # Initialize style loader
        self.style_loader = self.progress_hook(100 / 6 * 4, f"Loading styles", 300, StyleLoader, self.config_loader, self.log_manager) if hook else StyleLoader(self.config_loader, self.log_manager)

        # Initialize locale loader
        self.locale_loader = self.progress_hook(100 / 6 * 5, f"Loading locales", 300, LocaleLoader, self.config_loader, self.log_manager) if hook else LocaleLoader(self.config_loader, self.log_manager)
        
        # Initialize media loader
        self.media_loader = self.progress_hook(100 / 6 * 6, f"Loading media", 700, MediaLoader, self.log_manager) if hook else MediaLoader(self.log_manager)

        if hook:
            self.progress_hook(100, "Completed", 800)

        self.logger.info("Resource manager service started")
