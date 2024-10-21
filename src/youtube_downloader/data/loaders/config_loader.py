"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, json

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.util.path import get_config_path, get_system_download_path
from youtube_downloader.util.gui import get_default_system_font
from youtube_downloader.data.types.locale import Locale
from youtube_downloader.data.loaders.common import DEFAULT_THEME_NAME
from youtube_downloader.data.log_handlers.gui_handler import QtHandler
from youtube_downloader.data.abstracts.log_handler import LogHandler
from youtube_downloader.data.types.log_levels import LogLevel
import youtube_downloader

"""
Configuration structure:

The configuration file is located at %appdata%/config directory for the project.
Under the appdata directory, there is a settings.json file that contains
the user configuration for the application.

The configuration looks like this:
{
    "version": "2.1.0",
    "settings": {
        "locale": "en_US",
        "theme": "{theme_name}",
        "debug_mode": false,
        "debug_level": "DEBUG",
        "font": "{font_name}",
        "font_size": 12,
        "standard_download_path": "{path}",
        "last_download_path": "{path}",
        "load_last_download_path": true,
    }
}

Note that settings schema may change by the application version, hence there
may be a migration process required when the application version is updated.
"""

class ConfigKeys:
    VERSION = "version"
    SETTINGS = "settings"
    SETTINGS_LOCALE = "locale"
    SETTINGS_THEME = "theme"
    SETTINGS_DEBUG_MODE = "debug_mode"
    SETTINGS_DEBUG_LEVEL = "debug_level"
    SETTINGS_FONT = "font"
    SETTINGS_FONT_SIZE = "font_size"
    SETTINGS_STANDARD_DOWNLOAD_PATH = "standard_download_path"
    SETTINGS_LAST_DOWNLOAD_PATH = "last_download_path"
    SETTINGS_LOAD_LAST_DOWNLOAD_PATH = "load_last_download_path"

class ConfigLoader():
    """
    A class for loading and managing application configuration.

    This class handles the creation, checking, and retrieval of the application's
    configuration file. It also manages default configurations and version checks.

    Attributes:
        logger: A logger instance for logging operations.
        config_file (str): The name of the configuration file.
        config_path (str): The full path to the configuration file.
    """

    def __init__(self, log_manager: LogManager | None = None):
        """
        Initialize the ConfigLoader.

        Args:
            log_manager (LogManager | None): An optional log manager for logging operations.
        """
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.config_file = "settings.json"
        self.config_path = os.path.join(get_config_path(), self.config_file)
        if not os.path.exists(get_config_path()):
            os.makedirs(get_config_path(), exist_ok=True)
            if not os.path.exists(get_config_path()):
                err_str = f"Failed to create config directory: {get_config_path()}"
                self.logger.error(err_str)
                raise FileNotFoundError(err_str)
        self.DEFAULT_CONFIG = {
            ConfigKeys.VERSION: f"{youtube_downloader.__version__}",
            ConfigKeys.SETTINGS: {
                ConfigKeys.SETTINGS_LOCALE: Locale.get_default().to_str(),
                ConfigKeys.SETTINGS_THEME: DEFAULT_THEME_NAME,
                ConfigKeys.SETTINGS_DEBUG_MODE: False,
                ConfigKeys.SETTINGS_DEBUG_LEVEL: LogLevel.get_default().to_str(),
                ConfigKeys.SETTINGS_FONT: get_default_system_font(),
                ConfigKeys.SETTINGS_FONT_SIZE: 12,
                ConfigKeys.SETTINGS_STANDARD_DOWNLOAD_PATH: get_system_download_path(),
                ConfigKeys.SETTINGS_LAST_DOWNLOAD_PATH: get_system_download_path(),
                ConfigKeys.SETTINGS_LOAD_LAST_DOWNLOAD_PATH: True,
            }
        }

        if not self.check_config():
            self.create_default_config(override=True)
        
        log_level_str: str = self.get_config(ConfigKeys.SETTINGS_DEBUG_LEVEL)
        
        # Check if log level is valid
        if not LogLevel.validate_str(log_level_str):
            self.logger.warning(f"Invalid log level: {log_level_str}. Using default log level: {LogLevel.get_default().to_str()}")
            log_level = LogLevel.get_default()
            self.logger.debug(f"Set config log level to {log_level.to_str()}")
            self.save_config_key(ConfigKeys.SETTINGS_DEBUG_LEVEL, log_level.to_str())
        else:
            log_level = LogLevel.parse_str(log_level_str)

        if self.log_manager:
            self.set_display_log_level(log_level)
        else:
            self.logger.debug(f"Log manager not provided, skipping display log level setting")

        self.logger.debug(f"Config loader initialized with config path: {self.config_path}")
        
    def check_config(self) -> bool:
        """
        Check if the configuration file exists.

        Returns:
            bool: True if the configuration file exists, False otherwise.
        """
        return os.path.exists(self.config_path)
    
    def create_default_config(self, override: bool = False) -> None:
        """
        Create a default configuration file.

        If the configuration file already exists, this method will not overwrite it
        unless the override parameter is set to True.

        Args:
            override (bool): If True, overwrite the existing configuration file.
        """
        if self.check_config():
            if override:
                self.logger.debug(f"Overriding existing config file: {self.config_path}")
            else:
                self.logger.warning(f"Config file already exists: {self.config_path}")
                return
            
        with open(self.config_path, "w") as f:
            json.dump(self.DEFAULT_CONFIG, f, indent=4)
        self.logger.debug(f"Created default config file: {self.config_path}")

    def get_config(self, key: str | None = None):
        """
        Retrieve the current configuration or a specific configuration value.

        This method reads the configuration file and returns its contents as a dictionary.
        If a specific key is provided, it returns the value for that key.
        If the configuration file version doesn't match the current application version,
        it returns the default configuration.

        Args:
            key (str | None): The specific configuration key to retrieve. If None, returns the entire configuration.

        Returns:
            dict | Any: The entire configuration settings if no key is provided,
                        or the specific value for the given key.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            KeyError: If the specified key is not found in the configuration.
        """
        if not self.check_config():
            err_str = f"Config file does not exist: {self.config_path}"
            self.logger.error(err_str)
            raise FileNotFoundError(err_str)
        
        with open(self.config_path, "r") as f:
            data = json.load(f)

        if data[ConfigKeys.VERSION] != youtube_downloader.__version__:
            self.logger.warning(f"Config file version mismatch: config version is {data[ConfigKeys.VERSION]} where current version is {youtube_downloader.__version__}. Getting default config.")
            return self.DEFAULT_CONFIG[ConfigKeys.SETTINGS]
        
        if key:
            try:
                return data[ConfigKeys.SETTINGS][key]
            except KeyError:
                err_str = f"Config key not found: {key}"
                self.logger.error(err_str)
                raise KeyError(err_str)
        else:
            return data[ConfigKeys.SETTINGS]

    def save_config(self, config: dict) -> None:
        """
        Save the provided configuration to the config file.

        This method validates the input configuration against the default configuration,
        ensures all required keys are present and no extraneous keys exist, then saves
        the configuration to the file.

        Args:
            config (dict): The configuration dictionary to save.

        Raises:
            ValueError: If the input config is missing required keys or contains extraneous keys.

        Note:
            The saved configuration includes the current version of the application.
        """
        # Check if config is valid
        for key in self.DEFAULT_CONFIG[ConfigKeys.SETTINGS].keys():
            if key not in config:
                err_str = f"Config is missing key: {key}"
                self.logger.error(err_str)
                raise ValueError(err_str)
        
        for key in config.keys():
            if key not in self.DEFAULT_CONFIG[ConfigKeys.SETTINGS].keys():
                err_str = f"Config has extraneous key: {key}"
                self.logger.error(err_str)
                raise ValueError(err_str)
        
        # Save config
        full_config = {
            ConfigKeys.VERSION: f"{youtube_downloader.__version__}",
            ConfigKeys.SETTINGS: config
        }
        with open(self.config_path, "w") as f:
            json.dump(full_config, f, indent=4)
        self.logger.debug(f"Saved config")

    def save_config_key(self, key: str, value) -> None:
        config = self.get_config()
        config[key] = value
        self.save_config(config)

    def set_display_log_level(self, log_level: LogLevel):
        if not self.log_manager:
            self.logger.debug(f"Log manager not available, skipping display log level setting")
            return
        log_level_logging_enum: int = LogLevel.map_to_logging_enum(log_level)
        display_log_handlers: list[LogHandler] = self.log_manager.get_handlers_filter(QtHandler)
        if display_log_handlers:
            self.logger.debug(f"{len(display_log_handlers)} GUI Log Handlers found")
        for handler in display_log_handlers:
            handler.set_log_level(log_level_logging_enum)
            self.logger.debug(f"Set GUI Log Handler {handler.name} log level to {log_level.to_str()}")
