"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import yt_dlp

from PySide6.QtCore import QRunnable, QObject, Signal

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.model.application import YouTubeDownloaderModel

class SearchWorkerSignals(QObject):
    success = Signal(dict)
    error = Signal(Exception)

class SearchWorker(QRunnable):
    def __init__(self, log_manager: LogManager | None, model: YouTubeDownloaderModel, url: str):
        super().__init__()
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()

        self.model: YouTubeDownloaderModel = model

        self.url: str = url
        self.signals = SearchWorkerSignals()

    def run(self) -> None:
        try:
            video_data = self.search_video()
            self.signals.success.emit(video_data)
        except Exception as e:
            self.signals.error.emit(e)

    def search_video(self) -> dict:
        ydl_opts = {
            "logger": self.logger,
            "ffmpeg_location": self.model.get_ffmpeg_location()
        }
        self.logger.debug(f"YDL opts: {ydl_opts}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            json_result = ydl.sanitize_info(info_dict)
            return json_result
        
