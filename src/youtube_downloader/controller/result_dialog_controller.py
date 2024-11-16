"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.resource_manager import ResourceManager
from youtube_downloader.model.application import YouTubeDownloaderModel
from youtube_downloader.view.result_dialog import ResultDialog

class ResultDialogController():
    def __init__(self, log_manager: LogManager | None, resource_manager: ResourceManager, view: ResultDialog, model: YouTubeDownloaderModel, video_data: dict):
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.resource_manager: ResourceManager = resource_manager

        self.view: ResultDialog = view
        self.model: YouTubeDownloaderModel = model
        self.video_data: dict = video_data

        if self.video_data is None:
            raise ValueError("Result data is not provided")
        self.video_id = self.video_data.get("id", None)
        if self.video_id is None:
            raise ValueError("Result data does not contain 'id'")
        self.thumbnail_url = self.video_data.get("thumbnail", None)

        self.config_ui()

    def config_ui(self):
        self.view.video_widget.set_thumbnail(self.thumbnail_url)
        self.view.video_widget.set_video(self.video_id)

    def exec(self):
        self.view.exec()
