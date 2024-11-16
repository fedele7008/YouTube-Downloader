"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

This is a simple Youtube video downloading GUI application using pyside6 and yt-dlp.

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys

from youtube_downloader.app import YouTubeDownloader

if __name__ == "__main__":
    app = YouTubeDownloader()
    sys.exit(app.get_application().exec())
