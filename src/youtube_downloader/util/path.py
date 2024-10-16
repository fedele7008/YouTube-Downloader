"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import sys, os, pathlib, importlib.resources

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
        with importlib.resources.path("youtube_downloader", "__init__.py") as path:
            return os.path.dirname(path)


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