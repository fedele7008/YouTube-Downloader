"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(300, 300, 400, 200)

        # Set up dialog layout and content
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the about dialog. Show application information here."))
        
        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)