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
import sys

class TestGUI(unittest.TestCase):

    @patch('youtube_downloader.util.gui.subprocess.run')
    def test_get_default_system_font(self, mock_run):
        # Setup mock
        mock_result = MagicMock()
        mock_result.stdout = "Arial\n"
        mock_run.return_value = mock_result

        # Call the function
        result = get_default_system_font()

        # Assert the result
        self.assertEqual(result, "Arial")

        # Verify subprocess.run was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0][0], sys.executable)
        self.assertEqual(args[0][1], '-c')
        self.assertIn('QApplication', args[0][2])
        self.assertIn('QFontDatabase', args[0][2])
        self.assertEqual(kwargs['capture_output'], True)
        self.assertEqual(kwargs['text'], True)

if __name__ == "__main__":
    pytest.main([__file__])
