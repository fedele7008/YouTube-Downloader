"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, sys

from PySide6.QtWidgets import QSplashScreen, QProgressBar, QLabel, QApplication
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from youtube_downloader.util.path import get_media_path, get_icon_path
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
        self.setFixedSize(splash_image.size())
        # Disable the interaction with the splash screen
        self.setEnabled(False)
        center_widget_on_screen(self)

        self.progress_bar = QProgressBar(self)
        progress_bar_height = 8
        self.progress_bar.setGeometry(0, height - progress_bar_height, width, progress_bar_height)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                  stop:0 #2D32B3, stop:1 #B32DFF);
                border-top-right-radius: 2px;
                border-bottom-right-radius: 2px;
            }
        """)
        self.progress_bar.setMaximum(50000)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.message_label = QLabel(self)
        self.message_label.setStyleSheet("""
            color: #F5F5F5;
            background-color: transparent;
            font-family: 'Verdana';
        """)
        self.message_label.resize(190, 20)
        self.message_label.move(width - self.message_label.width() - 10, height - self.message_label.height() - 10)
        self.message_label.setAlignment(Qt.AlignRight)
        self.message_label.setText("Starting...")

        self.app_logo_label = QLabel(self)
        logo_pixmap = QPixmap(os.path.join(get_icon_path(), "YoutubeDownloader.png"))
        if logo_pixmap.isNull():
            raise Exception("Failed to load app logo")
        
        logo_size = 64
        logo_pixmap = logo_pixmap.scaled(logo_size, logo_size, Qt.KeepAspectRatio)
        
        self.app_logo_label.setPixmap(logo_pixmap)
        self.app_logo_label.resize(logo_size, logo_size)        
        self.app_logo_label.move(10, 10)
        self.app_logo_label.raise_()

        self.app_title_label = QLabel(self, text=self.app.applicationName())
        self.app_title_label.setStyleSheet("color: #ea6654;")
        self.app_title_label.setFont(QFont('Verdana', 28, QFont.Bold))
        self.app_title_label.adjustSize()
        self.app_title_label.move(10 + logo_size + 10, 14)
        self.app_title_label.raise_()

        self.app_version_label = QLabel(self, text=self.app.applicationVersion())
        self.app_version_label.setStyleSheet("color: #929cc4;")
        self.app_version_label.setFont(QFont('Verdana', 14))
        self.app_version_label.adjustSize()
        self.app_version_label.move(self.app_title_label.x(), self.app_title_label.y() + self.app_title_label.height())
        self.app_version_label.raise_()

        self.app.processEvents()

        self.animation = None

    def update_progress(self, percentage: float, message: str, min_duration_ms: int, callback = None, *args):
        start_value = self.progress_bar.value()
        end_value = int(percentage / 100 * self.progress_bar.maximum())
        half_duration = min_duration_ms // 2

        def update_message(value):
            current_percentage = value / self.progress_bar.maximum() * 100
            self.message_label.setText(f"{message}...{current_percentage:.0f}%")
            self.app.processEvents()

        update_message(start_value)

        # First half animation
        first_half_animation = QPropertyAnimation(self.progress_bar, b"value")
        first_half_animation.setDuration(half_duration)
        first_half_animation.setStartValue(start_value)
        first_half_animation.setEndValue((start_value + end_value) // 2)
        first_half_animation.valueChanged.connect(update_message)
        first_half_animation.setEasingCurve(QEasingCurve.InCubic)
        first_half_animation.start()
        self.app.processEvents()
        
        # Wait for the first half animation to finish
        while first_half_animation.state() == QPropertyAnimation.Running:
            self.app.processEvents()

        # Run callback
        result = None
        if callback:
            result = callback(*args)

        # Second half animation
        second_half_animation = QPropertyAnimation(self.progress_bar, b"value")
        second_half_animation.setDuration(half_duration)
        second_half_animation.setStartValue(self.progress_bar.value())
        second_half_animation.setEndValue(end_value)
        second_half_animation.valueChanged.connect(update_message)
        second_half_animation.setEasingCurve(QEasingCurve.OutCubic)
        second_half_animation.start()
        self.app.processEvents()

        # Wait for the second half animation to finish
        while second_half_animation.state() == QPropertyAnimation.Running:
            self.app.processEvents()

        # Set final message
        update_message(end_value)

        return result
