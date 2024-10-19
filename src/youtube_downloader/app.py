"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys, logging, os

from PySide6.QtWidgets import QApplication

from youtube_downloader.util.path import get_log_path
from youtube_downloader.model.application import YouTubeDownloaderApp
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.controller.main_window_controller import MainWindowController
from youtube_downloader.data.log_manager import LogManager
from youtube_downloader.data.log_handlers.console_handler import ConsoleHandler
from youtube_downloader.data.log_handlers.log_file_handler import LogFileHandler
from youtube_downloader.data.log_handlers.gui_handler import QtHandler

class App:
    def __init__(self):
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
        self.log_manager = LogManager("youtube_downloader", logging.DEBUG)
        self.logger = self.log_manager.get_logger()

        self.console_log_handler = ConsoleHandler()
        self.log_file_handler = LogFileHandler(os.path.join(get_log_path(), "service.log"))
        self.qt_log_handler = QtHandler()
        self.handlers = [self.console_log_handler, self.log_file_handler, self.qt_log_handler]

        for handler in self.handlers:
            self.log_manager.add_handler(handler)

        self.app_model = YouTubeDownloaderApp()
        self.app_window = MainWindow()
        self.app_window_controller = MainWindowController(self.app_window, self.app_model)
        self.app_window_controller.show()
        self.logger.info("YouTube Downloader Service started")

    def show(self):
        self.app_window_controller.show()

    def hide(self):
        self.app_window_controller.hide()
        
    def close(self):
        self.app_window_controller.close()
