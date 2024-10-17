"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, platform, subprocess

import youtube_downloader.util.path as path

class BinaryLoader():
    """
    A singleton class responsible for loading and validating the ffmpeg binary.

    This class ensures that only one instance of the ffmpeg loader exists, 
    and provides methods to load and validate the ffmpeg executable based 
    on the current platform. It supports macOS and Windows platforms.

    Attributes:
        ffmpeg_version (str): The version of the loaded ffmpeg binary.
        ffmpeg_exe (str): The path to the loaded ffmpeg executable.

    Methods:
        reload_ffmpeg() -> bool:
            Loads and validates the ffmpeg binary, returning True if successful.
        
        validate_ffmpeg() -> str | None:
            Validates the loaded ffmpeg binary and returns its version if valid.
        
        load_ffmpeg():
            Loads the ffmpeg executable path based on the current platform.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the BinaryLoader class is created.

        Returns:
            BinaryLoader: The singleton instance of the BinaryLoader class.
        """
        if cls._instance is None:
            cls._instance = super(BinaryLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """
        Initializes the BinaryLoader instance and reloads the ffmpeg binary.
        """
        self.reload_ffmpeg()

    def reload_ffmpeg(self) -> bool:
        """
        Loads and validates the ffmpeg binary.

        Returns:
            bool: True if the ffmpeg binary is successfully loaded and validated, False otherwise.
        """
        self.load_ffmpeg()
        ffmpeg_version = self.validate_ffmpeg()
        if ffmpeg_version is None:
            return False
        self.ffmpeg_version = ffmpeg_version
        return True

    def validate_ffmpeg(self) -> str | None:
        """
        Validates the loaded ffmpeg binary.

        Returns:
            str | None: The version of the ffmpeg binary if valid, None otherwise.
        """
        if not hasattr(self, "ffmpeg_exe"):
            # ffmpeg not loaded yet
            return None
        
        result = subprocess.run([self.ffmpeg_exe, "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            return None
        ffmpeg_version = result.stdout.split("\n")[0].split(" ")[2]
        return ffmpeg_version

    def load_ffmpeg(self):
        """
        Loads the ffmpeg executable path based on the current platform.

        Raises:
            NotImplementedError: If the platform is not supported.
        """
        match platform.system():
            case "Darwin":
                ffmpeg_exe_name = "ffmpeg"
            case "Windows":
                ffmpeg_exe_name = "ffmpeg.exe"
            case _:
                raise NotImplementedError(f"Unsupported platform: {platform.system()}")

        self.ffmpeg_exe = os.path.abspath(os.path.join(path.get_external_path(), "ffmpeg", "bin", ffmpeg_exe_name))
