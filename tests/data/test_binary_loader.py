"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from youtube_downloader.data.loaders.binary_loader import BinaryLoader


def test_singleton_instance():
    """
    Test that BinaryLoader is a singleton.
    """
    instance1 = BinaryLoader()
    instance2 = BinaryLoader()
    assert instance1 is instance2, "BinaryLoader is not a singleton."

def test_reload_ffmpeg():
    """
    Test the reload_ffmpeg method.
    """
    loader = BinaryLoader()
    result = loader.reload_ffmpeg()
    assert result is True, "Failed to reload and validate ffmpeg binary."
    assert hasattr(loader, 'ffmpeg_version'), "ffmpeg_version attribute not set."

def test_validate_ffmpeg():
    """
    Test the validate_ffmpeg method.
    """
    loader = BinaryLoader()
    loader.load_ffmpeg()  # Ensure ffmpeg_exe is set
    version = loader.validate_ffmpeg()
    assert version is not None, "Failed to validate ffmpeg binary."
    assert isinstance(version, str), "ffmpeg version is not a string."

def test_load_ffmpeg():
    """
    Test the load_ffmpeg method.
    """
    loader = BinaryLoader()
    loader.load_ffmpeg()
    assert hasattr(loader, 'ffmpeg_exe'), "ffmpeg_exe attribute not set."
    assert isinstance(loader.ffmpeg_exe, str), "ffmpeg_exe is not a string."
