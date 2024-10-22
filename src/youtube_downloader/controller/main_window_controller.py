"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QPixmap

from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.util.decorator import block_signal
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager

class MainWindowController():
    def __init__(self, log_manager: LogManager, resource_manager: ResourceManager, view: MainWindow, model: YouTubeDownloaderModel):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager
        self.view: MainWindow = view
        self.model: YouTubeDownloaderModel = model
        self.config_ui()
        self.bind_model()
        self.refresh_ui()

    def config_ui(self):
        icon = self.resource_manager.media_loader.get_icon()
        self.view.setWindowIcon(icon)
    
    def bind_model(self):
        self.model.app_name_changed.connect(self.on_app_name_changed)
        self.view.windowTitleChanged.connect(self.model.set_app_name)

    @Slot()
    @block_signal(lambda self: self.view)
    def on_app_name_changed(self, name):
        self.view.setWindowTitle(name)
        
    def refresh_ui(self):
        self.model.invoke_current_app_name_changed()
        
    def show(self):
        self.view.show()
        self.view.raise_()
        
    def hide(self):
        self.view.hide()

    def close(self):
        self.view.close()
