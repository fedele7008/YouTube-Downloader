"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys, logging
from typing import IO

from youtube_downloader.data.abstracts.log_handler import LogHandler
from youtube_downloader.data.log_handlers.common import DEFAULT_FORMAT

class ConsoleHandler(logging.StreamHandler, LogHandler):
    """
    A custom logging handler for console output.

    This class combines functionality from logging.StreamHandler and the custom LogHandler
    to provide console logging capabilities with additional features.

    Attributes:
        name (str): The name of the handler, set to "console_handler".
    """

    def __init__(self, stream: IO[str] = sys.stdout):
        """
        Initialize the ConsoleHandler.

        Args:
            stream (IO[str], optional): The output stream for logging. Defaults to sys.stdout.
        """
        super().__init__(stream)
        self.set_format(DEFAULT_FORMAT)
        self.name = "console_handler"
