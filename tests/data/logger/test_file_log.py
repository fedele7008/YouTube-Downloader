"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, pytest, logging
import shutil

from youtube_downloader.data.log_handlers.log_file_handler import LogFileHandler
from youtube_downloader.data.log_handlers.common import DEFAULT_FORMAT

@pytest.fixture
def log_file_handler(tmp_path):
    log_file = tmp_path / "test.log"
    handler = LogFileHandler(filename=str(log_file))
    yield handler
    # Clean up
    handler.close()
    if os.path.exists(log_file):
        os.remove(log_file)

def test_log_file_handler_initialization(log_file_handler):
    assert isinstance(log_file_handler, LogFileHandler)
    assert log_file_handler.name == "log_file_handler"
    assert log_file_handler.mode == "a"
    assert log_file_handler.maxBytes == 10 * 1024 * 1024
    assert log_file_handler.backupCount == 5

def test_log_file_handler_format(log_file_handler):
    assert log_file_handler.formatter._fmt == DEFAULT_FORMAT

def test_log_file_handler_logging(log_file_handler, tmp_path):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_file_handler)

    test_message = "Test log message"
    logger.info(test_message)

    log_file = tmp_path / "test.log"
    assert os.path.exists(log_file)
    
    with open(log_file, "r") as f:
        log_content = f.read()
        assert test_message in log_content
    
    # Clean up
    logger.removeHandler(log_file_handler)
    log_file_handler.close()
    if os.path.exists(log_file):
        os.remove(log_file)

def test_log_file_handler_rotation(tmp_path):
    log_file = tmp_path / "rotation_test.log"
    handler = LogFileHandler(filename=str(log_file), maxBytes=100, backupCount=3)
    
    logger = logging.getLogger("rotation_test_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Write enough logs to trigger rotation
    for i in range(10):
        logger.info("A" * 20)  # Each log is about 20 bytes

    assert os.path.exists(log_file)
    assert os.path.exists(f"{log_file}.1")
    assert os.path.exists(f"{log_file}.2")
    assert os.path.exists(f"{log_file}.3")
    assert not os.path.exists(f"{log_file}.4")  # Should not exist due to backupCount=3

    # Clean up
    logger.removeHandler(handler)
    handler.close()
    for file in [log_file] + [f"{log_file}.{i}" for i in range(1, 4)]:
        if os.path.exists(file):
            os.remove(file)
