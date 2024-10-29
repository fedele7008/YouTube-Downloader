"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import Any

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QMenuBar, QSplitter, 
                               QFrame, QTextEdit, QVBoxLayout)
from PySide6.QtCore import Qt

from youtube_downloader.util.gui import center_widget_on_screen
from youtube_downloader.view.search_pane import SearchPane
from youtube_downloader.view.result_pane import ResultPane
from youtube_downloader.view.status_pane import StatusPane

class MainWindow(QMainWindow):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.setGeometry(0, 0, 900, 600)
        center_widget_on_screen(self, kwargs.get("screen", None))
        self.init_ui()
        self.init_style()
        
    def init_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        self.settings_menu = self.menu_bar.addMenu(str())
        self.actions_menu = self.menu_bar.addMenu(str())
        self.help_menu = self.menu_bar.addMenu(str())

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.content_widget = QFrame()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        self.search_pane = SearchPane()
        self.result_pane = ResultPane()
        self.status_pane = StatusPane()

        self.content_layout.addWidget(self.search_pane)
        self.content_layout.addWidget(self.result_pane)
        self.content_layout.addWidget(self.status_pane)

        self.log_widget = QTextEdit()

        self.splitter.addWidget(self.content_widget)
        self.splitter.addWidget(self.log_widget)
        self.main_layout.addWidget(self.splitter)

    def init_style(self):
        self.menu_bar.setObjectName("main-menu-bar")
        self.content_widget.setObjectName("content-widget")
        self.log_widget.setObjectName("log-widget")

        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(10)

        self.log_widget.setReadOnly(True)
        self.log_widget.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
