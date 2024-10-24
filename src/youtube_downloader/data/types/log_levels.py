"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import logging

from youtube_downloader.data.abstracts.enum import BaseEnum

class LogLevel(BaseEnum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    @classmethod
    def get_default(cls):
        return cls.INFO

    @classmethod
    def map_to_logging_enum(cls, log_level):
        # map from LogLevel enum to logging enum
        mapping = {
            cls.NOTSET: logging.NOTSET,
            cls.DEBUG: logging.DEBUG,
            cls.INFO: logging.INFO,
            cls.WARNING: logging.WARNING,
            cls.ERROR: logging.ERROR,
            cls.CRITICAL: logging.CRITICAL
        }
        return mapping[log_level]
    
    @classmethod
    def map_to_str(cls, log_level: int):
        # map from logging enum to LogLevel enum string
        mapping = {
            logging.NOTSET: cls.NOTSET,
            logging.DEBUG: cls.DEBUG,
            logging.INFO: cls.INFO,
            logging.WARNING: cls.WARNING,
            logging.ERROR: cls.ERROR,
            logging.CRITICAL: cls.CRITICAL
        }
        return mapping[log_level].to_str()
