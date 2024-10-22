"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Callable

from youtube_downloader.data.loaders.config_loader import ConfigLoader
from youtube_downloader.data.loaders.binary_loader import BinaryLoader
from youtube_downloader.data.loaders.font_loader import FontLoader
from youtube_downloader.data.loaders.style_loader import StyleLoader
from youtube_downloader.data.loaders.locale_loader import LocaleLoader
from youtube_downloader.data.loaders.media_loader import MediaLoader
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.types.locale import Locale

class ResourceManager():
    def __init__(self, log_manager: LogManager | None = None, hook: Callable[[int, str, float], None] | None = None):
        # Set logger
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()

        # Set progress hook
        self.progress_hook = hook if hook else lambda a, b, c: None

        # Initialize binary loader
        self.binary_loader = BinaryLoader(self.log_manager)
        self.progress_hook(170, f"Loading ffmpeg binary...{17}%", 0.5)

        # Initialize config loader
        self.config_loader = ConfigLoader(self.log_manager)
        self.progress_hook(340, f"Loading config...{34}%")

        # Initialize font loader
        self.font_loader = FontLoader(self.config_loader, self.log_manager)
        self.progress_hook(510, f"Loading fonts...{51}%")

        # Initialize style loader
        self.style_loader = StyleLoader(self.config_loader, self.log_manager)
        self.progress_hook(680, f"Loading styles...{68}%")

        # Initialize locale loader
        self.locale_loader = LocaleLoader(self.config_loader, self.log_manager)
        self.progress_hook(850, f"Loading locales...{85}%")
        
        # Initialize media loader
        self.media_loader = MediaLoader(self.log_manager)
        self.progress_hook(990, f"Loading media...{99}%", 0.8)

        self.progress_hook(1000, f"Completed {100}%", 0.5)

        self.logger.info("Resource manager service started")
