"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import Slot

from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.main_window import MainWindow
from youtube_downloader.util.decorator import block_signal

class MainWindowController():
    def __init__(self, view: MainWindow, model: YouTubeDownloaderModel):
        self.view: MainWindow = view
        self.model: YouTubeDownloaderModel = model
        self.bind_model()
        self.refresh_ui()
    
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
