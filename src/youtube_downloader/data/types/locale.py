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
    SEARCH_PANE_URL_LABEL = "url-label"
    SEARCH_PANE_URL_INPUT_PLACEHOLDER = "url-input-placeholder"
    SEARCH_PANE_DEST_LABEL = "download-path-label"
    SEARCH_PANE_BROWSE_BUTTON = "browse-button"
    SEARCH_PANE_BROWSE_DIALOG_TITLE = "browse-dialog-title"
    SEARCH_PANE_SEARCH_BUTTON = "search-button"
    SEARCH_PANE_INPUT_ERROR_MESSAGE_EMPTY_DEST = "input-error-message-empty-dest"
    SEARCH_PANE_INPUT_ERROR_MESSAGE_DEST_DIR_NOT_EXIST = "input-error-message-dest-dir-not-exist"
    SEARCH_PANE_INPUT_ERROR_MESSAGE_DEST_DIR_NOT_WRITABLE = "input-error-message-dest-dir-not-writable"
    OK_BUTTON_TEXT = "ok-button-text"
    SEARCH_PANE_INPUT_ERROR_PROMPT_TITLE = "input-error-prompt-title"
    SEARCH_PANE_INPUT_ERROR_PROMPT_MESSAGE_EMPTY_URL = "input-error-prompt-message-empty-url"
    SEARCH_PANE_INPUT_ERROR_PROMPT_MESSAGE_INVALID_VIDEO = "input-error-prompt-message-invalid-video"
    ABOUT_DIALOG_TITLE = "about-dialog-title"
    CLOSE_BUTTON_TEXT = "close-button-text"
    ABOUT_DIALOG_DESCRIPTION = "about-dialog-description"
    LICENSE_DIALOG_TITLE = "license-dialog-title"
    SETTINGS_DIALOG_TITLE = "settings-dialog-title"
    SETTINGS_DIALOG_RESTORE_BUTTON = "settings-restore-button"
    SETTINGS_DIALOG_CANCEL_BUTTON = "settings-cancel-button"
    SETTINGS_DIALOG_APPLY_BUTTON = "settings-apply-button"
    SETTINGS_DIALOG_SAVE_BUTTON = "settings-save-button"
    SETTINGS_DIALOG_LIST = "settings-dialog-list"
    SETTINGS_GENERAL_LOCALE_TITLE = "settings-general-locale-title"
    SETTINGS_GENERAL_LOCALE_LANGUAGE_LABEL = "settings-general-locale-language-label"
    SETTINGS_GENERAL_DOWNLOAD_TITLE = "settings-general-download-title"
    SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_LABEL = "settings-general-download-default-download-path-label"
    SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_BROWSE_BUTTON = "settings-general-download-default-download-path-browse-button"
    SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_BROWSE_DIALOG_TITLE = "settings-general-download-default-download-path-browse-dialog-title"
    SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_ERROR_NOT_SET = "settings-general-download-default-download-path-error-not-set"
    SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_ERROR_NOT_EXIST = "settings-general-download-default-download-path-error-not-exist"
    SETTINGS_GENERAL_DOWNLOAD_DEFAULT_DOWNLOAD_PATH_ERROR_NOT_WRITABLE = "settings-general-download-default-download-path-error-not-writable"
    SETTINGS_GENERAL_DOWNLOAD_LOAD_LAST_DOWNLOAD_PATH_LABEL = "settings-general-download-load-last-download-path-label"
