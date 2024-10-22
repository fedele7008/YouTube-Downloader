"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QScreen, QCursor, QFontDatabase

def center_widget_on_screen(widget: QWidget, screen: QScreen | None = None):
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
    active_screen = QApplication.screenAt(QCursor.pos()) if screen is None else screen
    if active_screen is None:
        active_screen = QApplication.primaryScreen()
    center_point = QScreen.availableGeometry(active_screen).center()
    frame_geometry = widget.frameGeometry()
    frame_geometry.moveCenter(center_point)
    widget.move(frame_geometry.topLeft())

def get_default_system_font() -> str:
    """
    Retrieves the default system font family.

    This function returns the name of the default system font family used for general text.
    It requires an active QApplication instance to function properly.

    Returns:
        str: The name of the default system font family.

    Raises:
        RuntimeError: If no QApplication instance is found.

    Note:
        This function should be called after a QApplication instance has been created.
    """
    if not QApplication.instance():
        raise RuntimeError("QApplication instance not found")
    
    return QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont).family()
