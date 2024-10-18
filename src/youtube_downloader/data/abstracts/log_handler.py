"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import logging

from abc import ABC

from youtube_downloader.data.log_handlers.common import DEFAULT_DATETIME_FORMAT

class LogHandler(logging.Handler, ABC):
    """
    An abstract base class for custom log handlers.

    This class extends the functionality of logging.Handler and provides additional
    methods for setting log formats and levels.
    """

    def set_format(self, fmt: str, datefmt: str = DEFAULT_DATETIME_FORMAT):
        """
        Set the format for log messages.

        Args:
            fmt (str): The format string for log messages.
            datefmt (str, optional): The date/time format string. Defaults to DEFAULT_DATETIME_FORMAT.
        """
        self.setFormatter(logging.Formatter(fmt, datefmt))

    def set_formatter(self, formatter: logging.Formatter):
        """
        Set the formatter for the log handler.

        Args:
            formatter (logging.Formatter): The formatter to use for log messages.
        """
        self.setFormatter(formatter)

    def set_log_level(self, log_level):
        """
        Set the logging level for this handler.

        Args:
            log_level: The logging level to set (e.g., logging.INFO, logging.DEBUG).
        """
        self.setLevel(log_level)
