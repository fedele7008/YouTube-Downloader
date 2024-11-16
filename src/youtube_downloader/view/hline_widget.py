"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QFrame, QSizePolicy

class HLineWidget(QFrame):
    def __init__(self, height: int = 2):
        super().__init__()
        self.setObjectName("hline")
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
