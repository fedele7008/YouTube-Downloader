"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QScreen, QCursor

def center_widget_on_screen(widget: QWidget):
    """
    Centers the given widget on the primary screen.

    This function calculates the center point of the primary screen's available geometry
    and moves the widget to that center position.

    Args:
        widget (QWidget): The widget to be centered on the screen.

    Note:
        This function assumes that a QApplication instance has been created
        and that a primary screen is available.
    """
    screen = QApplication.screenAt(QCursor.pos())
    centerPoint = QScreen.availableGeometry(screen).center()
    fg = widget.frameGeometry()
    fg.moveCenter(centerPoint)
    widget.move(fg.topLeft())
