"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import pytest

from youtube_downloader.util import converter

def test_byte_to_display():
    assert converter.byte_to_display(500) == "500 B"
    assert converter.byte_to_display(1024) == "1.00 KB"
    assert converter.byte_to_display(1536) == "1.50 KB"
    assert converter.byte_to_display(1048576) == "1.00 MB"
    assert converter.byte_to_display(1572864) == "1.50 MB"
    assert converter.byte_to_display(1073741824) == "1.00 GB"
    assert converter.byte_to_display(1610612736) == "1.50 GB"

def test_byte_to_display_large_numbers():
    assert converter.byte_to_display(10737418240) == "10.00 GB"
    assert converter.byte_to_display(1099511627776) == "1024.00 GB"

def test_byte_to_display_small_numbers():
    assert converter.byte_to_display(1) == "1 B"
    assert converter.byte_to_display(10) == "10 B"
    assert converter.byte_to_display(100) == "100 B"

def test_byte_to_display_zero():
    assert converter.byte_to_display(0) == "0 B"

def test_byte_to_display_negative():
    with pytest.raises(ValueError):
        converter.byte_to_display(-1)
