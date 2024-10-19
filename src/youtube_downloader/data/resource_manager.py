"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from youtube_downloader.data.loaders.config_loader import ConfigLoader
from youtube_downloader.data.loaders.binary_loader import BinaryLoader
from youtube_downloader.data.log_manager import LogManager, get_null_logger

class ResourceManager():
    def __init__(self, log_manager: LogManager | None = None):
        self.logger = log_manager.get_logger() if log_manager else get_null_logger()
        self.config_loader = ConfigLoader(log_manager)
        if not self.config_loader.check_config():
            self.config_loader.create_default_config(override=True)
        self.config = self.config_loader.get_config()
        
        self.binary_loader = BinaryLoader(log_manager)
        self.logger.info("Resource manager service started")
