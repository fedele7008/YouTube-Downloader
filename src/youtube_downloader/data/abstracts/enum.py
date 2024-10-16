"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from enum import Enum, EnumMeta
from abc import ABCMeta, abstractmethod

class ABCEnumMeta(EnumMeta, ABCMeta):
    pass

class BaseEnum(Enum, metaclass=ABCEnumMeta):
    @classmethod
    def validate_str(cls, str_value):
        return str_value in cls.__members__

    @classmethod
    def parse_str(cls, str_value):
        if not cls.validate_str(str_value):
            raise ValueError(f"{str_value} is not a valid {cls.__name__}")
        return cls[str_value]

    @classmethod
    @abstractmethod
    def get_default(cls):
        pass

    def to_str(self):
        return self.name

    @classmethod
    def get_all_members_str(cls):
        return list(cls.__members__.keys())

    @classmethod
    def get_all_members(cls):
        return list(cls.__members__.values())
