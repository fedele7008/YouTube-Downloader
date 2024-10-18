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
    """
    A metaclass that combines EnumMeta and ABCMeta.
    
    This allows for creating abstract base classes that are also enumerations.
    """
    pass

class BaseEnum(Enum, metaclass=ABCEnumMeta):
    """
    An abstract base class for creating enhanced enumerations.
    
    This class provides additional utility methods for working with enumerations.
    """

    @classmethod
    def validate_str(cls, str_value: str) -> bool:
        """
        Validate if a string value is a valid member of the enumeration.

        Args:
            str_value (str): The string value to validate.

        Returns:
            bool: True if the string is a valid member, False otherwise.
        """
        return str_value in cls.__members__

    @classmethod
    def parse_str(cls, str_value: str):
        """
        Parse a string value into the corresponding enumeration member.

        Args:
            str_value (str): The string value to parse.

        Returns:
            The corresponding enumeration member.

        Raises:
            ValueError: If the string value is not a valid member of the enumeration.
        """
        if not cls.validate_str(str_value):
            raise ValueError(f"{str_value} is not a valid {cls.__name__}")
        return cls[str_value]

    @classmethod
    @abstractmethod
    def get_default(cls):
        """
        Get the default value for the enumeration.

        This method must be implemented by subclasses.

        Returns:
            The default enumeration member.
        """
        pass

    def to_str(self) -> str:
        """
        Convert the enumeration member to its string representation.

        Returns:
            str: The name of the enumeration member.
        """
        return self.name

    @classmethod
    def get_all_members_str(cls) -> list:
        """
        Get a list of all member names in the enumeration.

        Returns:
            list: A list of strings representing all member names.
        """
        return list(cls.__members__.keys())

    @classmethod
    def get_all_members(cls) -> list:
        """
        Get a list of all member values in the enumeration.

        Returns:
            list: A list of all enumeration member values.
        """
        return list(cls.__members__.values())
