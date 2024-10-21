"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import logging, threading
from typing import Callable

from PySide6.QtCore import QObject, Signal

from youtube_downloader.data.abstracts.log_handler import LogHandler
from youtube_downloader.data.log_handlers.common import BRIEF_FORMAT, BRIEF_DATETIME_FORMAT

class QtHandler(LogHandler):
    """
    A custom logging handler for Qt-based GUI applications.

    This class extends LogHandler to provide logging capabilities that integrate
    with Qt's signal-slot mechanism, allowing log messages to be displayed in GUI elements.

    This handler stores all log messages from the moment it is added to the logger.
    This feature ensures that any new GUI component connected to the QtHandler
    will have access to the complete history of log messages, maintaining
    consistency across the application's interface.

    Attributes:
        name (str): The name of the handler, set to "qt_handler".
        buffer (list): A list to store log messages before the GUI is ready.
        buffer_lock (threading.Lock): A lock to ensure thread-safe access to the buffer.
        gui_ready (bool): A flag indicating whether the GUI is ready to receive log messages.
        signal_emitter (SignalEmitter): An instance of SignalEmitter to emit log messages as signals.

    Usage example:
    ```
        from PySide6.QtWidgets import QApplication, QTextEdit
        from youtube_downloader.data.log_handlers.gui_handler import QtHandler

        app = QApplication()
        text_edit = QTextEdit()
        
        qt_handler = QtHandler()
        qt_handler.bind_signal(text_edit.append)
        
        logger = logging.getLogger()
        logger.addHandler(qt_handler)
        
        logger.info("This message will appear in the QTextEdit")
    ```
    """
    
    class SignalEmitter(QObject):
        """
        A nested class to emit log messages as Qt signals.

        This class is used to avoid duplicate overriding of the emit method in logging.Handler.

        Attributes:
            log_signal (Signal): A Qt signal that emits log messages as strings.
        """
        log_signal: Signal = Signal(str)

    def __init__(self):
        """
        Initialize the QtHandler.

        Sets up the log format, initializes the buffer, and creates a SignalEmitter instance.
        """
        logging.Handler.__init__(self)
        self.set_format(BRIEF_FORMAT, BRIEF_DATETIME_FORMAT)
        self.name = "qt_handler"
        self.buffer = []
        self.buffer_lock = threading.Lock()
        self.gui_ready = False
        self.signal_emitter = self.SignalEmitter()

    def emit(self, record: logging.LogRecord):
        """
        Emit a log record.

        If the GUI is ready, the log message is emitted as a signal. Also,
        it is added to the buffer.

        Args:
            record (logging.LogRecord): The log record to emit.
        """
        msg = self.format(record)
        with self.buffer_lock:
            self.buffer.append((self.level, msg))
            if self.gui_ready:
                self.signal_emitter.log_signal.emit(msg)

    def bind_signal(self, slot_function: Callable):
        """
        Bind the log signal to a slot function and emit buffered messages.

        This method should be called when the GUI is ready to receive log messages.

        Args:
            slot_function (Callable): The function to call when a log message is emitted.
        """
        with self.buffer_lock:
            temporary_update_signal_emitter = self.SignalEmitter()
            self.signal_emitter.log_signal.connect(slot_function)
            temporary_update_signal_emitter.log_signal.connect(slot_function)
            self.gui_ready = True
            for level, msg in self.buffer:
                if level >= self.level:
                    temporary_update_signal_emitter.log_signal.emit(msg)
