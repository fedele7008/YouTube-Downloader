"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import unittest, pytest
from unittest.mock import patch, MagicMock
from youtube_downloader.util.gui import get_default_system_font

class TestGUI(unittest.TestCase):

    @patch('youtube_downloader.util.gui.QApplication')
    @patch('youtube_downloader.util.gui.QFontDatabase')
    def test_get_default_system_font(self, mock_QFontDatabase, mock_QApplication):
        # Setup mocks
        mock_QApplication.instance.return_value = True
        mock_font = MagicMock()
        mock_font.family.return_value = "Arial"
        mock_QFontDatabase.systemFont.return_value = mock_font

        # Call the function
        result = get_default_system_font()

        # Assert the result
        self.assertEqual(result, "Arial")

        # Verify QFontDatabase.systemFont was called correctly
        mock_QFontDatabase.systemFont.assert_called_once_with(mock_QFontDatabase.SystemFont.GeneralFont)

    @patch('youtube_downloader.util.gui.QApplication')
    def test_get_default_system_font_no_qapp(self, mock_QApplication):
        # Setup mock to simulate no QApplication instance
        mock_QApplication.instance.return_value = None

        # Assert that RuntimeError is raised
        with self.assertRaises(RuntimeError):
            get_default_system_font()

if __name__ == "__main__":
    pytest.main([__file__])
