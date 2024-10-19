"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import logging, os
import logging.handlers

from youtube_downloader.data.abstracts.log_handler import LogHandler
from youtube_downloader.data.log_handlers.common import DEFAULT_FORMAT

class LogFileHandler(logging.handlers.RotatingFileHandler, LogHandler):
    """
    A custom logging handler for file output with rotation capabilities.

    This class combines functionality from logging.handlers.RotatingFileHandler and the custom LogHandler
    to provide file logging capabilities with log rotation and additional features.

    Attributes:
        name (str): The name of the handler, set to "log_file_handler".
    """

    def __init__(self, filename: str, mode: str = "a", maxBytes: int = 10*1024*1024, backupCount: int = 5):
        """
        Initialize the LogFileHandler.

        Args:
            filename (str): The name of the log file.
            mode (str, optional): The mode in which the file is opened. Defaults to "a" (append).
            maxBytes (int, optional): The maximum size of the log file before it gets rotated. Defaults to 10MB.
            backupCount (int, optional): The number of backup files to keep. Defaults to 5.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        super().__init__(filename, mode, maxBytes, backupCount)
        self.set_format(DEFAULT_FORMAT)
        self.name = "log_file_handler"
