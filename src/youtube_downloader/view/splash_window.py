"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, time

from PySide6.QtWidgets import QSplashScreen, QProgressBar, QLabel, QApplication
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer

from youtube_downloader.util.path import get_media_path
from youtube_downloader.util.gui import center_widget_on_screen

class SplashScreen(QSplashScreen):
    def __init__(self):
        # Create QApplication instance safely
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

        splash_image = QPixmap(os.path.join(get_media_path(), "splash.jpg"))
        if splash_image.isNull():
            raise Exception("Failed to load splash image")
        width = 640
        height = width * splash_image.height() / splash_image.width()
        splash_image = splash_image.scaled(width, height, Qt.KeepAspectRatio)
        super().__init__(splash_image)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # Disable the interaction with the splash screen
        self.setEnabled(False)
        center_widget_on_screen(self)

        self.progress_bar = QProgressBar(self)
        progress_bar_height = 5
        self.progress_bar.setGeometry(0, height - progress_bar_height, width, progress_bar_height)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #30B32D;
                border-top-right-radius: 2px;
                border-bottom-right-radius: 2px;
            }
        """)
        self.progress_bar.setMaximum(1000)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.message_label = QLabel(self)
        self.message_label.setStyleSheet("""
            color: #F5F5F5;
            background-color: transparent;
        """)
        self.message_label.resize(190, 20)
        self.message_label.move(width - self.message_label.width() - 10, height - self.message_label.height() - 10)
        self.message_label.setAlignment(Qt.AlignRight)
        self.message_label.setText("Starting...")
        self.app.processEvents()

    def update_progress(self, value: int, message: str, sleep_time: float = 0.2) -> None:
        if value > self.progress_bar.maximum():
            value = self.progress_bar.maximum()
        elif value < 0:
            value = 0
        self.progress_bar.setValue(value)
        self.message_label.setText(message)
        self.repaint()
        self.app.processEvents()
        time.sleep(sleep_time)

    def close(self):
        super().close()
