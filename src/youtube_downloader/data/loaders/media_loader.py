"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.util.path import get_media_path, get_icon_path

class MediaLoader:
    def __init__(self, log_manager: LogManager | None = None):
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.media_path = get_media_path()
        self.media = {}
        self.load_media()
        self.logger.debug(f"Media Loader initialized")

    def load_media(self):
        for root, _, files in os.walk(self.media_path):
            for file in files:
                abs_file_path = os.path.join(root, file)
                key_path = os.path.join(os.path.relpath(root, self.media_path), file) if root != self.media_path else file
                self.media[key_path] = abs_file_path

    def get_media(self) -> dict[str, str]:
        return self.media
    
    def get_icon(self) -> str:
        icon_path = os.path.join(get_icon_path(), "YoutubeDownloader.jpg")
        if os.path.exists(icon_path):
            return icon_path
        else:
            err_str = f"Icon file not found at {icon_path}"
            self.logger.error(err_str)
            raise FileNotFoundError(err_str)
