"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import pytest, os, json

from unittest.mock import patch, MagicMock
from youtube_downloader.data.loaders.config_loader import ConfigLoader
import youtube_downloader

@pytest.fixture
def mock_config_path(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    yield config_dir
    # Clean up: remove the config directory after the test
    for file in config_dir.iterdir():
        file.unlink()
    config_dir.rmdir()

@pytest.fixture
def config_loader(mock_config_path):
    with patch('youtube_downloader.data.loaders.config_loader.get_config_path', return_value=str(mock_config_path)):
        loader = ConfigLoader()
        yield loader
        # Clean up: remove the config file if it exists
        if os.path.exists(loader.config_path):
            os.remove(loader.config_path)

def test_init(mock_config_path, config_loader):
    assert config_loader.config_path == os.path.join(str(mock_config_path), "settings.json")
    assert os.path.exists(mock_config_path)

def test_check_config(config_loader):
    assert not config_loader.check_config()
    
    with open(config_loader.config_path, 'w') as f:
        json.dump({}, f)
    
    assert config_loader.check_config()

def test_create_default_config(config_loader):
    # Test creating when file doesn't exist
    config_loader.create_default_config()
    assert os.path.exists(config_loader.config_path)
    
    # Test not overriding when file exists
    with open(config_loader.config_path, 'w') as f:
        json.dump({"test": "data"}, f)
    
    config_loader.create_default_config()
    with open(config_loader.config_path, 'r') as f:
        assert json.load(f) == {"test": "data"}
    
    # Test overriding when file exists
    config_loader.create_default_config(override=True)
    with open(config_loader.config_path, 'r') as f:
        assert json.load(f) != {"test": "data"}

def test_get_config(config_loader):
    # Test when file doesn't exist
    with pytest.raises(FileNotFoundError):
        config_loader.get_config()
    
    # Test successful fetch
    test_config = {
        "version": youtube_downloader.__version__,
        "settings": {"test": "data"}
    }
    with open(config_loader.config_path, 'w') as f:
        json.dump(test_config, f)
    
    assert config_loader.get_config() == {"test": "data"}
    
    # Test version mismatch
    test_config["version"] = "0.0.0"
    with open(config_loader.config_path, 'w') as f:
        json.dump(test_config, f)
    
    with patch('youtube_downloader.data.loaders.config_loader.DEFAULT_CONFIG', {"settings": {"default": "config"}}):
        assert config_loader.get_config() == {"default": "config"}

if __name__ == "__main__":
    pytest.main([__file__])
