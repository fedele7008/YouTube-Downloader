"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys, logging, os

from PySide6.QtWidgets import QApplication

import youtube_downloader
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
from youtube_downloader.view.setup_window import SetupWindow
from youtube_downloader.controller.setup_window_controller import SetupWindowController

class YouTubeDownloader:
    def __init__(self):
        # Create QApplication instance safely
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
        self.app.setApplicationName("YouTube Downloader")
        self.app.setApplicationVersion(f"{youtube_downloader.__version__}")
        self.app.setStyle('Fusion')

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
        self.app_model = YouTubeDownloaderModel(self.log_manager, self.resource_manager)

        # Initialize application view
        self.app_window = MainWindow(screen=self.screen)

        # Initialize application controller - viewmodel
        self.app_window_controller = MainWindowController(self.log_manager, self.resource_manager, self.app_window, self.app_model)

        # Close splash screen
        self.splash_screen.close()

        if self.resource_manager.is_first_load():
            # Show setup screen for the first time
            self.logger.info("First config load detected, showing setup screen")
            
            self.setup_window = SetupWindow(screen=self.screen)
            self.setup_window_controller = SetupWindowController(self.log_manager, self.resource_manager, self.setup_window, self.app_model, self.app_window_controller)
            self.setup_window_controller.show()
        else:
            # Start application normally
            self.app_window_controller.show()

        self.app.setWindowIcon(self.resource_manager.media_loader.get_icon())
        self.logger.info("YouTube Downloader Service started")

    def show(self):
        self.app_window_controller.show()

    def hide(self):
        self.app_window_controller.hide()
        
    def close(self):
        self.app_window_controller.close()

    def get_application(self) -> QApplication:
        return self.app
