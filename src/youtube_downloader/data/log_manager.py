"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import logging

class LogManager():
    def __init__(self, name: str, log_level = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

    def get_logger(self):
        return self.logger

    def add_handler(self, handler: logging.Handler):
        self.logger.addHandler(handler)

    def remove_handler(self, handler: logging.Handler):
        self.logger.removeHandler(handler)

    def remove_handler_by_name(self, name: str):
        for handler in self.logger.handlers:
            if handler.name == name:
                self.logger.removeHandler(handler)

    def clear_handlers(self):
        self.logger.handlers.clear()

    def set_log_level(self, log_level):
        self.logger.setLevel(log_level)

    def set_handler_log_level(self, name: str, log_level):
        for handler in self.logger.handlers:
            if handler.name == name:
                handler.setLevel(log_level)

    def get_handler(self, name: str):
        for handler in self.logger.handlers:
            if handler.name == name:
                return handler

    def get_handlers(self):
        return self.logger.handlers

    def get_handlers_name(self):
        return [handler.name for handler in self.logger.handlers]

    def get_handlers_filter(self, handler_type):
        return [handler for handler in self.logger.handlers if type(handler) == handler_type]
