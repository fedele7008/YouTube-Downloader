"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import logging, pytest

from youtube_downloader.data.abstracts.log_handler import LogHandler

class ConcreteLogHandler(LogHandler):
    def emit(self, record):
        pass

def test_log_handler_initialization():
    handler = ConcreteLogHandler()
    assert isinstance(handler, LogHandler)
    assert isinstance(handler, logging.Handler)

def test_log_handler_set_format():
    handler = ConcreteLogHandler()
    test_format = "!%(message)s"
    handler.set_format(test_format)
    assert isinstance(handler.formatter, logging.Formatter)
    assert handler.formatter._fmt == test_format

def test_log_handler_set_formatter():
    handler = ConcreteLogHandler()
    test_formatter = logging.Formatter("!%(message)s")
    handler.set_formatter(test_formatter)
    assert handler.formatter == test_formatter

def test_log_handler_set_log_level():
    handler = ConcreteLogHandler()
    handler.set_log_level(logging.WARNING)
    assert handler.level == logging.WARNING

if __name__ == "__main__":
    pytest.main([__file__])
