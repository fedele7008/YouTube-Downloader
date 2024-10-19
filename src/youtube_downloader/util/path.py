"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys, os, pathlib, importlib.resources, platform

def get_package_root() -> str:
    """
    If the application is run as a bundle, return the path to the bundle.
    Otherwise, return the path to the package.

    Returns:
        str: The absolute path to the package root directory or the bundle root directory.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        package_path = importlib.resources.files("youtube_downloader")
        init_file = os.path.join(str(package_path), "__init__.py")
        return os.path.dirname(str(init_file))


def get_external_path() -> str:
    """
    Get the path to the external directory.

    Returns:
        str: The absolute path to the external directory.
    """
    return os.path.abspath(os.path.join(get_package_root(), "external"))


def get_resource_path() -> str:
    """
    Get the path to the resources directory.

    Returns:
        str: The absolute path to the resources directory.
    """
    return os.path.abspath(os.path.join(get_package_root(), "resources"))


def get_system_download_path() -> str:
    """
    Get the path to the system's download directory.

    Returns:
        str: The absolute path to the system's download directory.
    """
    return str(os.path.join(pathlib.Path.home(), "Downloads"))


def get_font_path() -> str:
    """
    Get the path to the fonts directory.

    Returns:
        str: The absolute path to the fonts directory.
    """
    return os.path.abspath(os.path.join(get_resource_path(), "fonts"))


def get_icon_path() -> str:
    """
    Get the path to the icon directory.

    Returns:
        str: The absolute path to the icon directory.
    """
    return os.path.abspath(os.path.join(get_resource_path(), "icon"))


def get_locale_path() -> str:
    """
    Get the path to the locale directory.

    Returns:
        str: The absolute path to the locale directory.
    """
    return os.path.abspath(os.path.join(get_resource_path(), "locale"))


def get_media_path() -> str:
    """
    Get the path to the media directory.

    Returns:
        str: The absolute path to the media directory.
    """
    return os.path.abspath(os.path.join(get_resource_path(), "media"))


def get_style_path() -> str:
    """
    Get the path to the style directory.

    Returns:
        str: The absolute path to the style directory.
    """
    return os.path.abspath(os.path.join(get_resource_path(), "style"))


def recursive_find(dir: str, ext: str) -> list[str]:
    """
    Recursively find files with a specific extension in a directory.

    Args:
        dir (str): The directory to search in.
        ext (str): The file extension to search for (without the dot).

    Returns:
        list[str]: A list of absolute paths to the found files.
    """
    result = []
    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith(f".{ext}"):
                result.append(os.path.join(root, file))
    return result

def get_appdata_path() -> str:
    """
    Retrieve the path to the application data directory based on the operating system.

    On macOS, it returns the path within the "Library/Application Support" directory.
    On Windows, it uses the APPDATA environment variable to determine the path.
    If the operating system is unsupported, a NotImplementedError is raised.

    Returns:
        str: The absolute path to the application data directory.

    Raises:
        EnvironmentError: If the APPDATA environment variable is not set on Windows.
        NotImplementedError: If the operating system is not supported.
    """
    current_os: str = platform.system()
    appdata_dir: str = "youtube_downloader"
    match current_os:
        case "Darwin": # MacOS
            appdata_root = os.path.join(pathlib.Path.home(), "Library", "Application Support")
        case "Windows": # Windows
            appdata_root = os.getenv("APPDATA")
            if appdata_root is None:
                raise EnvironmentError("Failed to get the application data directory. APPDATA environment variable is not set.")
        case _: # Unsupported OS
            raise NotImplementedError(f"Unsupported operating system: {current_os}")
    return os.path.join(appdata_root, appdata_dir)

def get_log_path() -> str:
    """
    Get the path to the log directory.

    Returns:
        str: The absolute path to the log directory.
    """
    return os.path.join(get_appdata_path(), "logs")
