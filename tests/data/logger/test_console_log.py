"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys, logging, pytest
from io import StringIO, TextIOWrapper

from youtube_downloader.data.log_handlers.console_handler import ConsoleHandler
from youtube_downloader.data.log_handlers.common import DEFAULT_FORMAT

def test_console_handler_initialization():
    handler = ConsoleHandler()
    assert isinstance(handler, ConsoleHandler)

def test_console_handler_custom_stream():
    custom_stream = StringIO()
    handler = ConsoleHandler(stream=custom_stream)
    assert handler.stream == custom_stream

def test_console_handler_format():
    handler = ConsoleHandler()
    assert isinstance(handler.formatter, logging.Formatter)
    assert handler.formatter._fmt == DEFAULT_FORMAT

def test_console_handler_emit():
    custom_stream = StringIO()
    handler = ConsoleHandler(stream=custom_stream)
    logger = logging.getLogger("test_logger")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    test_message = "Test log message"
    logger.info(test_message)

    log_output = custom_stream.getvalue().strip()
    assert test_message in log_output

def test_console_handler_set_format():
    handler = ConsoleHandler()
    new_format = "!%(message)s"
    handler.set_format(new_format)
    assert handler.formatter._fmt == new_format

def test_console_handler_set_formatter():
    handler = ConsoleHandler()
    new_formatter = logging.Formatter("!%(message)s")
    handler.set_formatter(new_formatter)
    assert handler.formatter == new_formatter

def test_console_handler_set_log_level():
    handler = ConsoleHandler()
    handler.set_log_level(logging.ERROR)
    assert handler.level == logging.ERROR

if __name__ == "__main__":
    pytest.main([__file__])
