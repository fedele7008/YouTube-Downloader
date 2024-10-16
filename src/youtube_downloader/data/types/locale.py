"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from youtube_downloader.data.abstracts.enum import BaseEnum

class Locale(BaseEnum):
    ko_KR = 1
    en_US = 2

    @classmethod
    def get_default(cls):
        return cls.en_US

if __name__ == "__main__":
    # Test cases for Locale methods
    print("Testing Locale methods:")

    # Test validate_str method
    print("\nTesting validate_str method:")
    print(f"Is 'ko_KR' valid? {Locale.validate_str('ko_KR')}")
    print(f"Is 'en_US' valid? {Locale.validate_str('en_US')}")
    print(f"Is 'fr_FR' valid? {Locale.validate_str('fr_FR')}")

    # Test parse_str method
    print("\nTesting parse_str method:")
    try:
        ko_locale = Locale.parse_str('ko_KR')
        print(f"Parsed 'ko_KR': {ko_locale}")
    except ValueError as e:
        print(f"Error parsing 'ko_KR': {e}")

    try:
        en_locale = Locale.parse_str('en_US')
        print(f"Parsed 'en_US': {en_locale}")
    except ValueError as e:
        print(f"Error parsing 'en_US': {e}")

    try:
        invalid_locale = Locale.parse_str('fr_FR')
        print(f"Parsed 'fr_FR': {invalid_locale}")
    except ValueError as e:
        print(f"Error parsing 'fr_FR': {e}")

    # Test to_str method
    print("\nTesting to_str method:")
    ko_locale = Locale.ko_KR
    en_locale = Locale.en_US
    print(f"ko_KR to string: {ko_locale.to_str()}")
    print(f"en_US to string: {en_locale.to_str()}")
    print(f"All members str: {Locale.get_all_members_str()}")
    print(f"All members: {Locale.get_all_members()}")

