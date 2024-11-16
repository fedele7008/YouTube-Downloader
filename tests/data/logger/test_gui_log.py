"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import pytest, logging

from PySide6.QtWidgets import QApplication, QTextEdit
from PySide6.QtTest import QTest

from youtube_downloader.data.log_handlers.gui_handler import QtHandler

@pytest.fixture(scope="module")
def qapp():
    return QApplication([])

@pytest.fixture
def qt_handler():
    return QtHandler()

@pytest.fixture
def logger(qt_handler):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(qt_handler)
    return logger

def test_qt_handler_initialization(qt_handler):
    assert qt_handler.name == "qt_handler"
    assert qt_handler.gui_ready == False
    assert len(qt_handler.buffer) == 0

def test_qt_handler_emit(qt_handler, logger):
    logger.debug("Test message")
    assert len(qt_handler.buffer) == 1
    level, msg = qt_handler.buffer[0]
    assert isinstance(level, int)
    assert "Test message" in msg

def test_qt_handler_bind_signal(qapp, qt_handler, logger):
    text_edit = QTextEdit()
    qt_handler.bind_signal(text_edit.append)
    
    assert qt_handler.gui_ready == True
    
    logger.info("Test bind signal")
    QTest.qWait(100)  # Wait for Qt to process events
    
    assert "Test bind signal" in text_edit.toPlainText()

def test_qt_handler_multiple_bindings(qapp, qt_handler, logger):
    text_edit1 = QTextEdit()
    text_edit2 = QTextEdit()
    
    qt_handler.bind_signal(text_edit1.append)
    qt_handler.bind_signal(text_edit2.append)
    
    logger.warning("Test multiple bindings")
    QTest.qWait(100)  # Wait for Qt to process events
    
    assert "Test multiple bindings" in text_edit1.toPlainText()
    assert "Test multiple bindings" in text_edit2.toPlainText()

def test_qt_handler_buffer_replay(qapp, logger):
    qt_handler = QtHandler()
    logger.addHandler(qt_handler)
    
    logger.error("Buffered message")
    
    text_edit = QTextEdit()
    qt_handler.bind_signal(text_edit.append)
    
    QTest.qWait(100)  # Wait for Qt to process events
    
    assert "Buffered message" in text_edit.toPlainText()

if __name__ == "__main__":
    pytest.main([__file__])
