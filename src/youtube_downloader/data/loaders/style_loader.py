"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, re, shutil, textwrap
from typing import Self

import youtube_downloader
from youtube_downloader.data.loaders.config_loader import ConfigLoader, ConfigKeys
from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.util.path import get_style_path, get_resource_theme_path, get_theme_path, flat_find
from youtube_downloader.data.loaders.common import DEFAULT_THEME_NAME

class Theme():
    THEME_INFO_HEADER = "[THEME INFO]"
    THEME_VARIABLES_HEADER = "[THEME VARIABLES]"
    THEME_COLORS_HEADER = "[THEME COLORS]"
    THEME_ADDITIONAL_STYLES_HEADER = "[ADDITIONAL STYLES]"

    SEPARATOR = ":"

    class ThemeInfoKeys():
        NAME = "name"
        AUTHOR = "author"
        VERSION = "version"

    class ThemeColorsKeys():
        BACKGROUND_COLOR = "background-color"
        FOREGROUND_COLOR = "foreground-color"
        LIGHT_BORDER_COLOR = "light-border-color"
        FIELD_BACKGROUND_COLOR = "field-background-color"
        PRIMARY_COLOR = "primary-color"
        PRIMARY_HOVER_COLOR = "primary-hover-color"
        PRIMARY_PRESSED_COLOR = "primary-pressed-color"
        SECONDARY_COLOR = "secondary-color"
        SECONDARY_HOVER_COLOR = "secondary-hover-color"
        SECONDARY_PRESSED_COLOR = "secondary-pressed-color"
        ERROROUS_COLOR = "errorous-color"
        ERROROUS_HOVER_COLOR = "errorous-hover-color"
        ERROROUS_PRESSED_COLOR = "errorous-pressed-color"
        WARNING_COLOR = "warning-color"
        WARNING_HOVER_COLOR = "warning-hover-color"
        WARNING_PRESSED_COLOR = "warning-pressed-color"

    def __init__(self, theme_path: str, theme_name: str, theme_info: dict, theme_colors: dict | None = None, theme_styles: str | None = None, log_manager: LogManager | None = None):
        self.logger = log_manager.get_logger() if log_manager else get_null_logger()
        self.theme_path = theme_path
        self.theme_name = theme_name
        self.theme_info = theme_info
        self.theme_colors = theme_colors
        self.theme_styles = theme_styles

    @classmethod
    def parse_theme_file(cls, theme_file: str, log_manager: LogManager | None = None) -> Self:
        logger = log_manager.get_logger() if log_manager else get_null_logger()

        # Verify if theme file exists
        if not os.path.exists(theme_file):
            err_str = f"Theme file does not exist: {theme_file}"
            logger.error(err_str)
            raise FileNotFoundError(err_str)
        
        # Verify if theme file is valid
        if not theme_file.endswith(".theme"):
            err_str = f"Theme file is invalid: {theme_file}"
            logger.error(err_str)
            raise ValueError(err_str)
        
        with open(theme_file, "r") as file:
            data = file.read()

        # Remove any string that starts with "//" to end of the line
        data = re.sub(r"//.*", "", data)
        # Strip any trailing white spaces but not leading white spaces for each line
        data = "\n".join([line.rstrip() for line in data.split("\n")])
        # Remove any empty lines
        data = "\n".join([line for line in data.split("\n") if line.strip()])

        theme_info_header_index = data.find(cls.THEME_INFO_HEADER)
        if theme_info_header_index == -1:
            err_str = f"Theme file is missing {cls.THEME_INFO_HEADER}: {theme_file}"
            logger.error(err_str)
            raise ValueError(err_str)
        
        theme_variables_header_index = data.find(cls.THEME_VARIABLES_HEADER)
        if theme_variables_header_index == -1:
            err_str = f"Theme file is missing {cls.THEME_VARIABLES_HEADER}: {theme_file}"
            logger.error(err_str)
            raise ValueError(err_str)
        
        theme_colors_header_index = data.find(cls.THEME_COLORS_HEADER)
        if theme_colors_header_index == -1:
            err_str = f"Theme file is missing {cls.THEME_COLORS_HEADER}: {theme_file}"
            logger.error(err_str)
            raise ValueError(err_str)
        
        theme_additional_styles_header_index = data.find(cls.THEME_ADDITIONAL_STYLES_HEADER)
        if theme_additional_styles_header_index == -1:
            err_str = f"Theme file is missing {cls.THEME_ADDITIONAL_STYLES_HEADER}: {theme_file}"
            logger.error(err_str)
            raise ValueError(err_str)
        
        # Extract theme file components
        theme_info_str = data[theme_info_header_index+len(cls.THEME_INFO_HEADER):theme_variables_header_index].strip()
        theme_variables_str = data[theme_variables_header_index+len(cls.THEME_VARIABLES_HEADER):theme_colors_header_index].strip()
        theme_colors_str = data[theme_colors_header_index+len(cls.THEME_COLORS_HEADER):theme_additional_styles_header_index].strip()
        theme_additional_styles = data[theme_additional_styles_header_index+len(cls.THEME_ADDITIONAL_STYLES_HEADER):].strip()

        # Extract theme info
        theme_info = {}
        for line in theme_info_str.split("\n"):
            split_index = line.find(cls.SEPARATOR)
            if split_index == -1:
                logger.warn(f"Theme file {theme_file} detected invalid theme info format: {line}. Ignoring it.")
                continue
            key = line[:split_index].strip()
            value = line[split_index+1:].strip()
            theme_info[key] = value

        # Assert that theme info contains all required keys
        ThemeInfoKeysList = [value for attr, value in vars(cls.ThemeInfoKeys).items() if not attr.startswith('__')]
        for key in ThemeInfoKeysList:
            if key not in theme_info:
                err_str = f"Theme file {theme_file} is missing required theme info: {key}."
                logger.error(err_str)
                raise ValueError(err_str)

        # Extract theme colors
        theme_colors = {}
        for line in theme_colors_str.split("\n"):
            if not line.strip():
                continue
            split_index = line.find(cls.SEPARATOR)
            if split_index == -1:
                err_str = f"Theme file {theme_file} detected invalid theme colors format: {line}."
                logger.error(err_str)
                raise ValueError(err_str)
            key = line[:split_index].strip()
            value = line[split_index+1:].strip()
            theme_colors[key] = value

        # Assert that theme colors contains all required keys
        ThemeColorKeysList = [value for attr, value in vars(cls.ThemeColorsKeys).items() if not attr.startswith('__')]
        for key in ThemeColorKeysList:
            if key not in theme_colors:
                err_str = f"Theme file {theme_file} is missing required theme colors: {key}."
                logger.error(err_str)
                raise ValueError(err_str)
            
        # Assert that theme_colors contains extraneous keys
        for key in theme_colors.keys():
            if key not in ThemeColorKeysList:
                err_str = f"Theme file {theme_file} contains extraneous theme colors: {key}."
                logger.error(err_str)
                raise ValueError(err_str)

        # Extract theme variables
        theme_variables = {}
        for line in theme_variables_str.split("\n"):
            if not line.strip():
                continue
            split_index = line.find(cls.SEPARATOR)
            if split_index == -1:
                logger.warn(f"Theme file {theme_file} detected invalid theme variables format: {line}. Ignoring it.")
                continue
            key = line[:split_index].strip()
            value = line[split_index+1:].strip()
            theme_variables[key] = value

        # Assert that theme variables does not contain any key of theme_colors
        for key in theme_variables.keys():
            if key in theme_colors:
                err_str = f"Theme file {theme_file} contains theme variables that conflict with theme colors: {key}."
                logger.error(err_str)
                raise ValueError(err_str)
            
        # Apply theme variable to its own values (in order)
        for key, value in theme_variables.items():
            for target_key, target_value in theme_variables.items():
                if key == target_key:
                    continue # Skip applying self to self
                theme_variables[target_key] = target_value.replace(f"${{{key}}}", value)
            
        # Apply theme variables to theme_colors's values
        for key, value in theme_variables.items():
            for color_key, color_value in theme_colors.items():
                theme_colors[color_key] = color_value.replace(f"${{{key}}}", value)

        # Apply theme variables to theme_additional_styles
        for key, value in theme_variables.items():
            theme_additional_styles = theme_additional_styles.replace(f"${{{key}}}", value)

        # Apply theme colors to theme_additional_styles
        for key, value in theme_colors.items():
            theme_additional_styles = theme_additional_styles.replace(f"${{{key}}}", value)

        return cls(theme_file, theme_info[cls.ThemeInfoKeys.NAME], theme_info, theme_colors, theme_additional_styles, log_manager)


class StyleLoader():
    def __init__(self, config_loader: ConfigLoader, log_manager: LogManager | None = None):
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.config_loader = config_loader
        self.config_theme = self.config_loader.get_config(key=ConfigKeys.SETTINGS_THEME)
        self.resource_style_path = get_style_path()
        self.resource_theme_path = get_resource_theme_path()
        self.appdata_theme_path = get_theme_path()
        self.themes: dict[str, Theme] = {}
        self.global_style = ""

        # If appdata theme path does not exist, create it
        if not os.path.exists(self.appdata_theme_path):
            os.makedirs(self.appdata_theme_path)

        # Load existing theme files in appdata theme path
        for theme_file in flat_find(self.appdata_theme_path, "theme"):
            try:
                theme = Theme.parse_theme_file(theme_file, self.log_manager)
                if theme.theme_info[Theme.ThemeInfoKeys.VERSION] != youtube_downloader.__version__:
                    self.logger.warn(f"Theme file {theme.theme_name} version mismatches: {theme.theme_info[Theme.ThemeInfoKeys.VERSION]} (current app version: {youtube_downloader.__version__}). Skipping the load.")
                    continue
                if theme.theme_name in self.themes:
                    self.logger.warn(f"Theme file {theme_file} is already loaded: {theme.theme_name}")
                    continue
                self.themes[theme.theme_name] = theme
                self.logger.debug(f"Loaded theme file: {theme.theme_name}.theme")
            except Exception as e:
                self.logger.error(f"Failed to load theme file: {theme_file}. Skipping the load.")

        for theme_file in flat_find(self.resource_theme_path, "theme"):
            try:
                theme = Theme.parse_theme_file(theme_file, self.log_manager)
                if theme.theme_info[Theme.ThemeInfoKeys.VERSION] != youtube_downloader.__version__:
                    self.logger.warn(f"Theme file {theme.theme_name} version mismatches: {theme.theme_info[Theme.ThemeInfoKeys.VERSION]} (current app version: {youtube_downloader.__version__}). Skipping the load.")
                    continue
                if theme.theme_name in self.themes:
                    continue
                self.themes[theme.theme_name] = theme
                shutil.copy(theme_file, os.path.join(self.appdata_theme_path, f"{theme.theme_name}.theme"))
                self.logger.debug(f"Copied system theme file: {theme.theme_name} to {self.appdata_theme_path}")
                self.logger.debug(f"Loaded system theme file: {theme.theme_name}.theme")
            except Exception as e:
                self.logger.error(f"Failed to load system theme file: {theme_file}. Skipping the load.")

        # Check if the theme specified in config exists
        if self.config_theme not in self.themes:
            self.logger.warn(f"Theme specified in config does not exist: {self.config_theme}. Using default theme, {DEFAULT_THEME_NAME}")
            self.config_theme = DEFAULT_THEME_NAME
            self.config_loader.save_config_key(key=ConfigKeys.SETTINGS_THEME, value=self.config_theme)
            
        # Re-confirm that the theme specified in config exists
        if self.config_theme not in self.themes:
            err_str = f"Theme specified in config does not exist: {self.config_theme}"
            self.logger.error(err_str)
            raise ValueError(err_str)
        
        self.reload_global_style()
        self.logger.info(f"Themes available: {self.get_all_available_themes()}")
        self.logger.debug(f"Style Loader initialized with config theme: {self.config_theme}")

    def change_config_theme(self, theme_name: str) -> None:
        # Verify that the theme exists
        if theme_name not in self.themes:
            err_str = f"Theme does not exist: {theme_name}"
            self.logger.error(err_str)
            raise ValueError(err_str)
        
        # Change config theme
        self.config_theme = theme_name
        self.config_loader.save_config_key(key=ConfigKeys.SETTINGS_THEME, value=theme_name)
        self.logger.info(f"Changed config theme to: {theme_name}")
        self.reload_global_style()

    def reload_global_style(self):
        # Read global style from the resource style path
        with open(os.path.join(self.resource_style_path, "global.qss"), "r") as file:
            global_style_raw = file.read()
        
        if self.config_theme not in self.themes:
            err_str = f"Theme specified in config does not exist: {self.config_theme}"
            self.logger.error(err_str)
            raise ValueError(err_str)
        
        current_theme = self.themes[self.config_theme]
        for key, value in current_theme.theme_colors.items():
            global_style_raw = global_style_raw.replace(f"${{{key}}}", value)

        self.global_style = global_style_raw
        
    def get_style(self) -> str:
        # Call this method upon change of font settings or theme
        font_style = textwrap.dedent(f"""\
        * {{
            font-family: "{self.config_loader.get_config(key=ConfigKeys.SETTINGS_FONT)}";
            font-size: {self.config_loader.get_config(key=ConfigKeys.SETTINGS_FONT_SIZE)}px;
        }}
        """)
        style = f"{font_style}\n{self.global_style}\n\n/* THEME STYLES */\n\n"
        theme = self.themes[self.config_theme]
        style += theme.theme_styles

        # Replace any ${font-size} with config font size
        font_size = self.config_loader.get_config(key=ConfigKeys.SETTINGS_FONT_SIZE)
        style = re.sub(r"\${font-size}", str(font_size), style)
        # Replace any ${font-size:+n} with config font size + n where n is an integer
        # Replace any ${font-size:-n} with config font size - n where n is an integer
        def replace_font_size(match):
            operator = match.group(1)
            number = int(match.group(2))
            base_size = int(font_size)
            if operator == '+':
                return str(base_size + number)
            else:
                return str(base_size - number)
        style = re.sub(r"\${font-size:(\+|-)(\d+)}", replace_font_size, style)
        return style

    def get_all_available_themes(self) -> list[str]:
        return list(self.themes.keys())
    
    def get_config_theme(self) -> str:
        return self.config_theme
    
    def import_theme(self, theme_path: str) -> None:
        # Check if the theme file exists
        if not os.path.exists(theme_path):
            err_str = f"Theme file does not exist: {theme_path}"
            self.logger.error(err_str)
            raise FileNotFoundError(err_str)
        
        # Check if the theme file is valid
        if not theme_path.endswith(".theme"):
            err_str = f"Theme file is invalid: {theme_path}"
            self.logger.error(err_str)
            raise ValueError(err_str)
        
        theme = Theme.parse_theme_file(theme_path, self.log_manager)
        if theme.theme_info[Theme.ThemeInfoKeys.VERSION] != youtube_downloader.__version__:
            err_str = f"Theme file {theme.theme_name} version mismatches: {theme.theme_info[Theme.ThemeInfoKeys.VERSION]} (current app version: {youtube_downloader.__version__}). Aborting the load."
            self.logger.error(err_str)
            raise ValueError(err_str)
        if theme.theme_name in self.themes:
            err_str = f"Theme file {theme_path} is already loaded: {theme.theme_name}"
            self.logger.error(err_str)
            raise ValueError(err_str)
        
        # Save the theme file to appdata theme path
        shutil.copy(theme_path, os.path.join(self.appdata_theme_path, f"{theme.theme_name}.theme"))
        self.themes[theme.theme_name] = theme
        self.logger.info(f"Imported theme file: {theme.theme_name}.theme")
