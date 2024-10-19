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
        self.logger = log_manager.get_logger() if log_manager else get_null_logger()
        self.config_file = "settings.json"
        self.config_path = os.path.join(get_config_path(), self.config_file)
        if not os.path.exists(get_config_path()):
            os.makedirs(get_config_path())
        self.DEFAULT_CONFIG = {
            "version": f"{youtube_downloader.__version__}",
            "settings": {
                "locale": Locale.get_default().to_str(),
                "theme": "system_light",
                "debug_mode": False,
                "debug_level": "DEBUG",
                "font": get_default_system_font(),
                "font_size": 12,
                "standard_download_path": get_system_download_path(),
                "last_download_path": get_system_download_path(),
                "load_last_download_path": True,
            }
        }
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

    def get_config(self) -> dict:
        """
        Retrieve the current configuration.

        This method reads the configuration file and returns its contents as a dictionary.
        If the configuration file version doesn't match the current application version,
        it returns the default configuration.

        Returns:
            dict: The current configuration settings.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        if not self.check_config():
            err_str = f"Config file does not exist: {self.config_path}"
            self.logger.error(err_str)
            raise FileNotFoundError(err_str)
        
        with open(self.config_path, "r") as f:
            data = json.load(f)

        if data["version"] != youtube_downloader.__version__:
            self.logger.warning(f"Config file version mismatch: config version is {data['version']} where current version is {youtube_downloader.__version__}. Getting default config.")
            return self.DEFAULT_CONFIG["settings"]
        
        return data["settings"]
