"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import pytest, logging
import os

from youtube_downloader.data.log_manager import LogManager, get_null_logger

@pytest.fixture(scope="function")
def log_manager():
    manager = LogManager("test_logger")
    yield manager
    manager.clear_handlers()

@pytest.fixture(scope="function")
def temp_log_file():
    log_file = "test_temp.log"
    yield log_file
    if os.path.exists(log_file):
        os.remove(log_file)

def test_init(log_manager):
    assert log_manager.logger.name == "test_logger"
    assert log_manager.logger.level == logging.INFO

def test_get_logger(log_manager):
    assert isinstance(log_manager.get_logger(), logging.Logger)

def test_add_and_remove_handler(log_manager):
    handler = logging.StreamHandler()
    handler.name = "test_handler"
    log_manager.add_handler(handler)
    assert handler in log_manager.get_handlers()
    
    log_manager.remove_handler(handler)
    assert handler not in log_manager.get_handlers()

def test_remove_handler_by_name(log_manager):
    handler = logging.StreamHandler()
    handler.name = "test_handler"
    log_manager.add_handler(handler)
    
    log_manager.remove_handler_by_name("test_handler")
    assert handler not in log_manager.get_handlers()

def test_clear_handlers(log_manager, temp_log_file):
    handler1 = logging.StreamHandler()
    handler2 = logging.FileHandler(temp_log_file)
    log_manager.add_handler(handler1)
    log_manager.add_handler(handler2)
    
    log_manager.clear_handlers()
    assert len(log_manager.get_handlers()) == 0

def test_set_log_level(log_manager):
    log_manager.set_log_level(logging.DEBUG)
    assert log_manager.logger.level == logging.DEBUG

def test_set_handler_log_level(log_manager):
    handler = logging.StreamHandler()
    handler.name = "test_handler"
    log_manager.add_handler(handler)
    
    log_manager.set_handler_log_level("test_handler", logging.ERROR)
    assert log_manager.get_handler("test_handler").level == logging.ERROR

def test_get_handler(log_manager):
    handler = logging.StreamHandler()
    handler.name = "test_handler"
    log_manager.add_handler(handler)
    print(log_manager.get_handler("test_handler"))
    print(handler)
    assert log_manager.get_handler("test_handler") == handler

def test_get_handlers_name(log_manager, temp_log_file):
    handler1 = logging.StreamHandler()
    handler1.name = "handler1"
    handler2 = logging.FileHandler(temp_log_file)
    handler2.name = "handler2"
    log_manager.add_handler(handler1)
    log_manager.add_handler(handler2)
    
    assert set(log_manager.get_handlers_name()) == {"handler1", "handler2"}

def test_get_handlers_filter(log_manager, temp_log_file):
    stream_handler = logging.StreamHandler()
    file_handler1 = logging.FileHandler(temp_log_file)
    file_handler2 = logging.FileHandler(temp_log_file + ".2")
    log_manager.add_handler(stream_handler)
    log_manager.add_handler(file_handler1)
    log_manager.add_handler(file_handler2)

    assert len(log_manager.get_handlers_filter(logging.StreamHandler)) == 1
    assert len(log_manager.get_handlers_filter(logging.FileHandler)) == 2

    # Clean up the additional log file
    if os.path.exists(temp_log_file + ".2"):
        os.remove(temp_log_file + ".2")

def test_get_null_logger():
    null_logger = get_null_logger()
    null_logger.info("test")
    assert isinstance(null_logger, logging.Logger)
    assert null_logger.name == "silent_logger"
    assert len(null_logger.handlers) == 1
    assert isinstance(null_logger.handlers[0], logging.NullHandler)

if __name__ == "__main__":
    pytest.main([__file__])
