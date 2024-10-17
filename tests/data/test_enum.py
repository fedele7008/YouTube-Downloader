"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import pytest

from youtube_downloader.data.types.locale import Locale

def test_validate_str():
    assert Locale.validate_str('ko_KR') == True
    assert Locale.validate_str('en_US') == True
    assert Locale.validate_str('xx_XX') == False  # Gibberish locale
    assert Locale.validate_str('') == False
    assert Locale.validate_str('invalid_format') == False
    assert Locale.validate_str('ko-KR') == False  # Wrong separator

def test_parse_str():
    assert Locale.parse_str('ko_KR') == Locale.ko_KR
    assert Locale.parse_str('en_US') == Locale.en_US
    
    with pytest.raises(ValueError):
        Locale.parse_str('xx_XX')  # Gibberish locale
    
    with pytest.raises(ValueError):
        Locale.parse_str('')
    
    with pytest.raises(ValueError):
        Locale.parse_str('invalid_format')

def test_to_str():
    assert Locale.ko_KR.to_str() == 'ko_KR'
    assert Locale.en_US.to_str() == 'en_US'

def test_get_all_members_str():
    all_members_str = Locale.get_all_members_str()
    assert isinstance(all_members_str, list)
    assert 'ko_KR' in all_members_str
    assert 'en_US' in all_members_str
    assert 'xx_XX' not in all_members_str  # Gibberish locale should not be present

def test_get_all_members():
    all_members = Locale.get_all_members()
    assert isinstance(all_members, list)
    assert Locale.ko_KR in all_members
    assert Locale.en_US in all_members
    assert 'xx_XX' not in all_members  # Gibberish locale should not be present
