"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtCore import QObject, Property, Signal, Slot

class YouTubeDownloaderModel(QObject):
    app_name_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._app_name = "YouTube Downloader"
        
    def get_app_name(self) -> str:
        return self._app_name
    
    @Slot()
    def set_app_name(self, name: str) -> None:
        if self._app_name != name:
            self._app_name = name
            self.app_name_changed.emit(name)
            
    def invoke_current_app_name_changed(self) -> None:
        self.app_name_changed.emit(self.get_app_name())

    app_name = Property(str, get_app_name, set_app_name, notify=app_name_changed)
    