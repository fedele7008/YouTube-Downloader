"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys, logging, os

from PySide6.QtWidgets import QApplication

from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.util.path import get_log_path
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.view.splash_window import SplashScreen
from youtube_downloader.controller.main_window_controller import MainWindowController
from youtube_downloader.data.log_manager import LogManager
from youtube_downloader.data.log_handlers.console_handler import ConsoleHandler
from youtube_downloader.data.log_handlers.log_file_handler import LogFileHandler
from youtube_downloader.data.log_handlers.gui_handler import QtHandler

class YouTubeDownloader:
    def __init__(self):
        # Create QApplication instance safely
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

        # Initialize splash screen
        self.splash_screen = SplashScreen()
        self.splash_screen.show()
        self.screen = self.splash_screen.screen()

        # Initialize log manager
        self.log_manager = LogManager("youtube_downloader", logging.DEBUG)
        self.logger = self.log_manager.get_logger()

        self.console_log_handler = ConsoleHandler()
        self.log_file_handler = LogFileHandler(os.path.join(get_log_path(), "service.log"))
        self.qt_log_handler = QtHandler()
        self.handlers = [self.console_log_handler, self.log_file_handler, self.qt_log_handler]

        for handler in self.handlers:
            self.log_manager.add_handler(handler)

        # Initialize resource manager
        self.resource_manager = ResourceManager(self.log_manager, self.splash_screen.update_progress)

        # Initialize application model
        self.app_model = YouTubeDownloaderModel()

        # Initialize application view
        self.app_window = MainWindow(screen=self.screen)

        # Initialize application controller - viewmodel
        self.app_window_controller = MainWindowController(self.app_window, self.app_model)

        # Close splash screen
        self.splash_screen.close()

        # Start application
        self.app_window_controller.show()
        self.logger.info("YouTube Downloader Service started")

    def show(self):
        self.app_window_controller.show()

    def hide(self):
        self.app_window_controller.hide()
        
    def close(self):
        self.app_window_controller.close()

    def get_application(self) -> QApplication:
        return self.app
