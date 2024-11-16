"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import os, json
from collections import deque
from datetime import datetime

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.data.loaders.config_loader import ConfigLoader
from youtube_downloader.util.path import get_cache_path

class SearchCacheIndexTable():
    SAVE_FILE = "search_cache_index.json"
    TABLE_SIZE = 100 # about 100 MB in size

    class Keys:
        CACHE = "cache"
        ENTRY_QUERY = "query"
        ENTRY_INDEX = "index"
        ENTRY_TIMESTAMP = "timestamp"

    def __init__(self, config_loader: ConfigLoader, log_manager: LogManager | None = None):
        self.config_loader = config_loader
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.save_file_path = os.path.join(get_cache_path(), self.SAVE_FILE)
        if not os.path.exists(get_cache_path()):
            os.makedirs(get_cache_path(), exist_ok=True)
            if not os.path.exists(get_cache_path()):
                err_str = f"Failed to create cache directory: {get_cache_path()}"
                self.logger.error(err_str)
                raise FileNotFoundError(err_str)
            
        if not self.has_save_file():
            self.create_empty_save_file()

        self.index_table: deque[dict] = self.pull_from_disk()
        while len(self.index_table) > self.TABLE_SIZE:
            self.index_table.popleft()

    def has_save_file(self) -> bool:
        if not os.path.exists(self.save_file_path):
            return False

        data = None
        with open(self.save_file_path, "r") as f:
            try:
                data = json.load(f)
            except Exception:
                return False
        
        cache_list = data.get(SearchCacheIndexTable.Keys.CACHE, None)
        if not cache_list:
            return False
        
        if not isinstance(cache_list, list):
            return False
        
        return True
    
    def create_empty_save_file(self) -> None:
        with open(self.save_file_path, "w") as f:
            json.dump({SearchCacheIndexTable.Keys.CACHE: []}, f, indent=4)
        self.logger.debug(f"Created empty search cache index file: {self.save_file_path}")

    def pull_from_disk(self) -> deque[dict]:
        if not self.has_save_file():
            self.logger.warning(f"Search cache index file not found: {self.save_file_path}")
            return deque([])
        
        with open(self.save_file_path, "r") as f:
            try:
                data = json.load(f)
                index_table = deque(data.get(SearchCacheIndexTable.Keys.CACHE, []))
            except Exception as e:
                self.logger.error(f"Failed to load search cache index: {e}")
                index_table = deque([])
        return index_table
    
    def push_to_disk(self) -> None:
        with open(self.save_file_path, "w") as f:
            json.dump({SearchCacheIndexTable.Keys.CACHE: list(self.index_table)}, f, indent=4)
        self.logger.debug(f"Saved search cache index table to {os.path.basename(self.save_file_path)}")

    def get_index(self, query: str) -> tuple[int, str] | None:
        for item in self.index_table:
            if item.get(SearchCacheIndexTable.Keys.ENTRY_QUERY) == query:
                if item != self.index_table[-1]:
                    self.index_table.remove(item)
                    self.index_table.append(item)
                    self.push_to_disk()
                index = item.get(SearchCacheIndexTable.Keys.ENTRY_INDEX)
                timestamp = item.get(SearchCacheIndexTable.Keys.ENTRY_TIMESTAMP)
                return index, timestamp
        return None
    
    def add_index(self, query: str, index: int, timestamp: str | None = None) -> None:
        if len(self.index_table) > 0 and self.index_table[-1].get(SearchCacheIndexTable.Keys.ENTRY_QUERY) == query:
            if self.index_table[-1].get(SearchCacheIndexTable.Keys.ENTRY_TIMESTAMP) != timestamp:
                item = self.index_table[-1]
                item[SearchCacheIndexTable.Keys.ENTRY_TIMESTAMP] = timestamp
                self.push_to_disk()
                return
        
        for item in self.index_table:
            if item.get(SearchCacheIndexTable.Keys.ENTRY_QUERY) == query:
                self.index_table.remove(item)
                item[SearchCacheIndexTable.Keys.ENTRY_TIMESTAMP] = timestamp
                self.index_table.append(item)
                self.push_to_disk()
                return
        
        new_index_entry = {
            SearchCacheIndexTable.Keys.ENTRY_QUERY: query,
            SearchCacheIndexTable.Keys.ENTRY_INDEX: index,
            SearchCacheIndexTable.Keys.ENTRY_TIMESTAMP: timestamp,
        }
        self.index_table.append(new_index_entry)
        while len(self.index_table) > self.TABLE_SIZE:
            self.index_table.popleft()
        self.push_to_disk()

class SearchCacheDatabase():
    SAVE_FILE = "search_cache_db.json"

    class Keys:
        ENTRY = "cache"

    def __init__(self, config_loader: ConfigLoader, log_manager: LogManager | None = None):
        self.config_loader = config_loader
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()
        self.save_file_path = os.path.join(get_cache_path(), self.SAVE_FILE)
        if not os.path.exists(get_cache_path()):
            os.makedirs(get_cache_path(), exist_ok=True)
            if not os.path.exists(get_cache_path()):
                err_str = f"Failed to create cache directory: {get_cache_path()}"
                self.logger.error(err_str)
                raise FileNotFoundError(err_str)
            
        if not self.has_save_file():
            self.create_empty_save_file()

        self.cache_db: dict = self.pull_from_disk()

    def has_save_file(self) -> bool:
        if not os.path.exists(self.save_file_path):
            return False
        
        data = None
        with open(self.save_file_path, "r") as f:
            try:
                data = json.load(f)
            except Exception as e:
                return False
            
        entries = data.get(SearchCacheDatabase.Keys.ENTRY, None)
        if not entries:
            return False
        
        return True
    
    def create_empty_save_file(self) -> None:
        with open(self.save_file_path, "w") as f:
            json.dump({SearchCacheDatabase.Keys.ENTRY: {}}, f, indent=4)
        self.logger.debug(f"Created empty search cache database file: {self.save_file_path}")

    def pull_from_disk(self) -> dict:
        if not self.has_save_file():
            self.logger.warning(f"Search cache database file not found: {self.save_file_path}")
            return {}
        
        with open(self.save_file_path, "r") as f:
            try:
                data = json.load(f)
                cache_table = data.get(SearchCacheDatabase.Keys.ENTRY, {})
            except Exception as e:
                self.logger.error(f"Failed to load search cache database: {e}")
                cache_table = {}
        return cache_table

    def push_to_disk(self) -> None:
        with open(self.save_file_path, "w") as f:
            json.dump({SearchCacheDatabase.Keys.ENTRY: self.cache_db}, f, indent=4)
        self.logger.debug(f"Saved search cache database to {os.path.basename(self.save_file_path)}")

class CacheLoader():
    def __init__(self, config_loader: ConfigLoader, log_manager: LogManager | None = None):
        self.config_loader = config_loader
        self.log_manager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()

        self.index_table = SearchCacheIndexTable(config_loader, log_manager)
        self.cache_db = SearchCacheDatabase(config_loader, log_manager)

        self.sync_search_cache()

        self.logger.debug(f"Loaded search cache index table: {len(self.index_table.index_table)} entries")
        self.logger.debug(f"Loaded search cache database: {len(self.cache_db.cache_db)} entries")

    def sync_search_cache(self) -> None:
        db_keys = self.cache_db.cache_db.keys()
        remove_item_list = []
        for item in self.index_table.index_table:
            index = str(item.get(SearchCacheIndexTable.Keys.ENTRY_INDEX))
            if index not in db_keys:
                remove_item_list.append(item)
                
        for item in remove_item_list:
            self.index_table.index_table.remove(item)
            self.logger.debug(f"Sync miss: Removed index from search cache index table: {index}")

        index_keys = [str(index.get(SearchCacheIndexTable.Keys.ENTRY_INDEX)) for index in self.index_table.index_table]
        remove_item_list = []
        for key in db_keys:
            if key not in index_keys:
                remove_item_list.append(key)
        
        for item in remove_item_list:
            self.cache_db.cache_db.pop(item)
            self.logger.debug(f"Sync miss: Removed data from search cache database: {item}")

        self.index_table.push_to_disk()
        self.cache_db.push_to_disk()
        self.logger.debug(f"Synced search cache: [{os.path.basename(self.index_table.save_file_path)} <-> {os.path.basename(self.cache_db.save_file_path)}]")

    def get(self, query: str) -> dict | None:
        result = self.index_table.get_index(query)
        if result is None:
            return None
        
        index, _ = result
        return self.cache_db.cache_db.get(str(index), None)

    def add(self, query: str, data: dict) -> None:
        index = hash(query)
        self.index_table.add_index(query, index, str(datetime.now()))
        self.cache_db.cache_db[str(index)] = data

    def remove(self, query: str) -> None:
        for item in self.index_table.index_table:
            if item.get(SearchCacheIndexTable.Keys.ENTRY_QUERY) == query:
                self.index_table.remove(item)
                break

    def clear(self) -> None:
        self.index_table.index_table.clear()

    def __del__(self):
        self.sync_search_cache()
