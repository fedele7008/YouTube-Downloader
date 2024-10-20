"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from youtube_downloader.data.loaders.config_loader import ConfigLoader
from youtube_downloader.data.loaders.binary_loader import BinaryLoader
from youtube_downloader.data.loaders.font_loader import FontLoader
from youtube_downloader.data.loaders.style_loader import StyleLoader
from youtube_downloader.data.log_manager import LogManager, get_null_logger

class ResourceManager():
    def __init__(self, log_manager: LogManager | None = None):
        # Set logger
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()

        # Initialize binary loader
        self.binary_loader = BinaryLoader(self.log_manager)

        # Initialize config loader
        self.config_loader = ConfigLoader(self.log_manager)
        if not self.config_loader.check_config():
            self.config_loader.create_default_config(override=True)
        
        # Initialize font loader
        self.font_loader = FontLoader(self.config_loader, self.log_manager)

        # Initialize style loader
        self.style_loader = StyleLoader(self.config_loader, self.log_manager)

        self.logger.info("Resource manager service started")
