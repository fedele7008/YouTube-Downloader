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

class LocaleKeys:
    APP_NAME = "app-title"
    APP_MENU_SETTINGS_TITLE = "app-menu-settings-title"
    APP_MENU_SETTINGS_GENERAL_TITLE = "app-menu-settings-general-title"
    APP_MENU_SETTINGS_GENERAL_STATUS_TIP = "app-menu-settings-general-status-tip"
    APP_MENU_ACTIONS_TITLE = "app-menu-actions-title"
    APP_MENU_ACTIONS_QUIT_TITLE = "app-menu-actions-quit-title"
    APP_MENU_ACTIONS_QUIT_STATUS_TIP = "app-menu-actions-quit-status-tip"
    APP_MENU_HELP_TITLE = "app-menu-help-title"
    APP_MENU_HELP_ABOUT_TITLE = "app-menu-help-about-title"
    APP_MENU_HELP_ABOUT_STATUS_TIP = "app-menu-help-about-status-tip"
    APP_MENU_HELP_LICENSE_TITLE = "app-menu-help-license-title"
    APP_MENU_HELP_LICENSE_STATUS_TIP = "app-menu-help-license-status-tip"
    SETUP_WINDOW_TITLE = "setup-window-title"
    SETUP_WINDOW_WELCOME_LABEL = "setup-window-welcome-label"
    SETUP_WINDOW_LANGUAGE_LABEL = "setup-window-language-label"
    SETUP_WINDOW_THEME_LABEL = "setup-window-theme-label"
    SETUP_WINDOW_START_BUTTON = "setup-window-start-button"
