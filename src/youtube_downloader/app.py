"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys

from PySide6.QtWidgets import QApplication
from youtube_downloader.model.application import YouTubeDownloaderApp
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.controller.main_window_controller import MainWindowController

class App:
    def __init__(self):
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
        self.youtube_downloader_model = YouTubeDownloaderApp()
        self.main_window = MainWindow()
        self.main_window_controller = MainWindowController(self.main_window, self.youtube_downloader_model)
        self.main_window_controller.show()

    def show(self):
        self.main_window_controller.show()

    def hide(self):
        self.main_window_controller.hide()
        
    def close(self):
        self.main_window_controller.close()
