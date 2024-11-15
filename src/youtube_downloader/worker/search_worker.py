"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import yt_dlp, multiprocessing, threading, logging, os

from PySide6.QtCore import QRunnable, QObject, Signal

from youtube_downloader.data.log_manager import LogManager, get_null_logger
from youtube_downloader.model.application import YouTubeDownloaderModel

class IPCKeys:
    STATE = "state"
    RESULT = "result"

IPC_STATE_SUCCESS = "success"
IPC_STATE_ERROR = "error"
IPC_STATE_RUNNING = "running"

IPC_RESPONSE = {
    IPCKeys.STATE: str(),
    IPCKeys.RESULT: {},
}

class PipeHandler(logging.Handler):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def emit(self, record):
        try:
            message = self.format(record)
            resp = IPC_RESPONSE.copy()
            resp[IPCKeys.STATE] = IPC_STATE_RUNNING
            resp[IPCKeys.RESULT] = {
                "log_level": record.levelname,
                "message": f"[PID: {os.getpid()}] {message}",
            }
            self.conn.send(resp)
        except Exception:
            self.handleError(record)

def search_process(url: str, ydl_opts: dict, conn) -> None:
    logger = logging.getLogger("search_worker_subprocess")
    logger.setLevel(logging.DEBUG)
    handler = PipeHandler(conn)
    logger.addHandler(handler)

    ydl_opts["logger"] = logger
    logger.debug(f"Search worker subprocess started: {url}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            json_result = ydl.sanitize_info(info_dict)
            resp = IPC_RESPONSE.copy()
            resp[IPCKeys.STATE] = IPC_STATE_SUCCESS
            resp[IPCKeys.RESULT] = json_result
            conn.send(resp)
    except Exception as e:
        resp = IPC_RESPONSE.copy()
        resp[IPCKeys.STATE] = IPC_STATE_ERROR
        resp[IPCKeys.RESULT] = e
        conn.send(resp)
    finally:
        conn.close()

class SearchWorkerSignals(QObject):
    success = Signal(dict)
    error = Signal(Exception)

class SearchWorker(QRunnable):
    def __init__(self, log_manager: LogManager | None, model: YouTubeDownloaderModel, url: str):
        super().__init__()
        self.log_manager: LogManager = log_manager
        self.logger = self.log_manager.get_logger() if self.log_manager else get_null_logger()

        self.model: YouTubeDownloaderModel = model

        self.url: str = url
        self.signals = SearchWorkerSignals()

        self.process = None
        self.cancel_flag = threading.Event()
        
    def run(self) -> None:
        try:
            self.parent_conn, self.child_conn = multiprocessing.Pipe()
            ydl_opts = {
                "ffmpeg_location": self.model.get_ffmpeg_location()
            }
            self.process = multiprocessing.Process(
                target=search_process, args=(self.url, ydl_opts, self.child_conn))
            self.logger.debug(f"Search worker controller process: {self.process}")
            self.process.start()

            while True:
                if self.cancel_flag.is_set():
                    self.logger.info("Search cancelled")
                    break
                if self.parent_conn.poll(timeout=0.1):
                    resp = self.parent_conn.recv()
                    if resp[IPCKeys.STATE] == IPC_STATE_SUCCESS:
                        self.signals.success.emit(resp[IPCKeys.RESULT])
                        break
                    elif resp[IPCKeys.STATE] == IPC_STATE_ERROR:
                        self.signals.error.emit(resp[IPCKeys.RESULT])
                        break
                    else:
                        # Log message
                        record = resp[IPCKeys.RESULT]
                        match record["log_level"]:
                            case "DEBUG":
                                self.logger.debug(record["message"])
                            case "INFO":
                                self.logger.info(record["message"])
                            case "WARNING":
                                self.logger.warning(record["message"])
                            case "ERROR":
                                self.logger.error(record["message"])
                            case _:
                                self.logger.info(record["message"])
        except Exception as e:
            self.signals.error.emit(e)
            return
        finally:
            if self.process is not None:
                if self.process.is_alive():
                    self.process.terminate()
                    self.logger.debug("Search worker process terminated")
                self.process.join()
                self.logger.debug("Search worker process joined")
                self.process = None

    def cancel(self) -> None:
        self.cancel_flag.set()
