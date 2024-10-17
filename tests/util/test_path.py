"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import pytest, os

from youtube_downloader.util import path

@pytest.fixture
def tmp_path(tmp_path):
    return tmp_path

def test_get_package_root():
    root = path.get_package_root()
    assert os.path.isdir(root)
    assert os.path.exists(root)

def test_get_external_path():
    external_path = path.get_external_path()
    assert os.path.isdir(external_path)
    assert external_path.endswith("external")

def test_get_resource_path():
    resource_path = path.get_resource_path()
    assert os.path.isdir(resource_path)
    assert resource_path.endswith("resources")

def test_get_system_download_path():
    download_path = path.get_system_download_path()
    assert os.path.isdir(download_path)
    assert download_path.endswith("Downloads")

def test_get_font_path():
    font_path = path.get_font_path()
    assert os.path.isdir(font_path)
    assert font_path.endswith(os.path.join("resources", "fonts"))

def test_get_icon_path():
    icon_path = path.get_icon_path()
    assert os.path.isdir(icon_path)
    assert icon_path.endswith(os.path.join("resources", "icon"))

def test_get_locale_path():
    locale_path = path.get_locale_path()
    assert os.path.isdir(locale_path)
    assert locale_path.endswith(os.path.join("resources", "locale"))

def test_get_media_path():
    media_path = path.get_media_path()
    assert os.path.isdir(media_path)
    assert media_path.endswith(os.path.join("resources", "media"))

def test_get_style_path():
    style_path = path.get_style_path()
    assert os.path.isdir(style_path)
    assert style_path.endswith(os.path.join("resources", "style"))

def test_recursive_find(tmp_path):
    # Create a temporary directory structure
    dir1 = tmp_path / "dir1"
    dir2 = dir1 / "dir2"
    dir2.mkdir(parents=True)
    
    # Create some test files
    (dir1 / "file1.txt").touch()
    (dir1 / "file2.py").touch()
    (dir2 / "file3.py").touch()
    (dir2 / "file4.txt").touch()
    
    # Test recursive_find
    py_files = path.recursive_find(str(tmp_path), "py")
    assert len(py_files) == 2
    assert str(dir1 / "file2.py") in py_files
    assert str(dir2 / "file3.py") in py_files
    
    txt_files = path.recursive_find(str(tmp_path), "txt")
    assert len(txt_files) == 2
    assert str(dir1 / "file1.txt") in txt_files
    assert str(dir2 / "file4.txt") in txt_files

def test_recursive_find_complex(tmp_path):
    # Create a more complex temporary directory structure
    dir1 = tmp_path / "dir1"
    dir2 = dir1 / "dir2"
    dir3 = dir2 / "dir3"
    dir4 = dir3 / "dir4"
    dir4.mkdir(parents=True)
    
    # Create test files with various extensions and depths
    (tmp_path / "root.txt").touch()
    (dir1 / "file1.py").touch()
    (dir1 / "file2.txt").touch()
    (dir2 / "file3.py").touch()
    (dir2 / "file4.jpg").touch()
    (dir3 / "file5.py").touch()
    (dir3 / "file6.txt").touch()
    (dir4 / "file7.py").touch()
    (dir4 / "file8.txt").touch()
    (dir4 / "file9.jpg").touch()
    
    # Test recursive_find with different extensions and depths
    py_files = path.recursive_find(str(tmp_path), "py")
    assert len(py_files) == 4
    assert str(dir1 / "file1.py") in py_files
    assert str(dir2 / "file3.py") in py_files
    assert str(dir3 / "file5.py") in py_files
    assert str(dir4 / "file7.py") in py_files
    
    txt_files = path.recursive_find(str(tmp_path), "txt")
    assert len(txt_files) == 4
    assert str(tmp_path / "root.txt") in txt_files
    assert str(dir1 / "file2.txt") in txt_files
    assert str(dir3 / "file6.txt") in txt_files
    assert str(dir4 / "file8.txt") in txt_files
    
    jpg_files = path.recursive_find(str(tmp_path), "jpg")
    assert len(jpg_files) == 2
    assert str(dir2 / "file4.jpg") in jpg_files
    assert str(dir4 / "file9.jpg") in jpg_files
    
    # Test recursive_find with non-existent extension
    non_existent = path.recursive_find(str(tmp_path), "non")
    assert len(non_existent) == 0
    
    # Test recursive_find from a subdirectory
    sub_py_files = path.recursive_find(str(dir2), "py")
    assert len(sub_py_files) == 3
    assert str(dir2 / "file3.py") in sub_py_files
    assert str(dir3 / "file5.py") in sub_py_files
    assert str(dir4 / "file7.py") in sub_py_files

