import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTabWidget, QFileDialog, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QGridLayout,
                             QMessageBox, QStackedWidget, QDialogButtonBox, QSizePolicy)
from PyQt6.QtCore import Qt, QThread, QRunnable, QThreadPool, pyqtSignal, pyqtSlot, QObject, QSize, QUrl
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIcon, QMovie, QImage, QFont, QDesktopServices
import yt_dlp
import shutil
import requests
from io import BytesIO
import threading
import re

def get_video_formats(url, ffmpeg_path):
    ydl_opts = {
        'ffmpeg_location': ffmpeg_path
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract video information without downloading
        info_dict = ydl.extract_info(url, download=False)
        return info_dict

class SearchWorker(QRunnable):
    def __init__(self, url, ffmpeg_path):
        super().__init__()
        self.url = url
        self.ffmpeg_path = ffmpeg_path
        self.signals = WorkerSignals()

    def run(self):
        try:
            video_formats = get_video_formats(self.url, self.ffmpeg_path)
            self.signals.result.emit(video_formats)
        except Exception as e:
            self.signals.error.emit(str(e))

class WorkerSignals(QObject):
    result = pyqtSignal(object)
    error = pyqtSignal(str)

class DownloadWorkerSignals(QObject):
    progress = pyqtSignal(int, float, str, bool, bool)  # row, progress percentage, remaining time, is_merged_format, is_video
    finished = pyqtSignal(int)  # row
    error = pyqtSignal(int, str)  # row, error message

class DownloadWorker(QRunnable):
    def __init__(self, row, url, format, output_path, video_title):
        super().__init__()
        self.row = row
        self.url = url
        self.format = format
        self.output_path = output_path
        self.video_title = video_title
        self.signals = DownloadWorkerSignals()
        self.is_cancelled = threading.Event()
        self.ydl = None
        self.full_path = None
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.merging = False
        self.is_merged_format = self.check_if_merged_format(format)
        self.is_video_download = True
        self.max_progress = 0

    def check_if_merged_format(self, format):
        return 'acodec' in format and format['acodec'] != 'none' and \
               'vcodec' in format and format['vcodec'] != 'none'

    @staticmethod
    def generate_unique_filename(base_name, ext, output_path):
            file_name = f"{base_name}.{ext}"
            counter = 1
            while os.path.exists(os.path.join(output_path, file_name)):
                file_name = f"{base_name}_{counter}.{ext}"
                counter += 1
            return file_name

    def run(self):
        safe_title = self.video_title.replace(' ', '_')
        resolution = self.format.get('height', None)
        ext = self.format.get('ext', 'mp4')
        if resolution is None:
            resolution = "Unknown_resolution"
        else:
            resolution = f"{resolution}p"
        base_name = f"{safe_title}_{resolution}"
        file_name = self.generate_unique_filename(base_name, ext, self.output_path)
        full_path = os.path.join(self.output_path, file_name)
        self.full_path = full_path

        # 기존 파일 삭제
        if os.path.exists(self.full_path):
            try:
                os.remove(self.full_path)
                print(f"Deleted existing file: {self.full_path}")
            except Exception as e:
                print(f"Error deleting existing file: {e}")

        ydl_opts = {
            'format': self.format.get('format_id', 'bestvideo')+'+bestaudio/best',
            'outtmpl': full_path,
            'progress_hooks': [self.progress_hook],
            'merge_output_format': ext,
            'retries': 10,  # 재시도 횟수 증가
            'fragment_retries': 10,  # 프래그먼트 다운로드 재시도 횟수
            'skip_unavailable_fragments': True,  # 사용 불가능한 프래그먼트 건너뛰기
            'keepvideo': False,  # 병합 후 원본 파일 삭제
            'overwrites': True,  # 기존 파일 덮어쓰기
            'postprocessor_hooks': [self.postprocessor_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.ydl = ydl
                info = ydl.extract_info(self.url, download=False)
                self.total_bytes = info.get('filesize') or info.get('filesize_approx', 0)
                if not self.is_cancelled.is_set():
                    ydl.download([self.url])
            if not self.is_cancelled.is_set():
                self.signals.finished.emit(self.row)
        except Exception as e:
            if not self.is_cancelled.is_set():
                self.signals.error.emit(self.row, str(e))
        finally:
            # 다운로드 완료 또는 취소 후 부분 다운로드 파일 삭제
            self.cleanup_temp_files()

    def cancel(self):
        self.is_cancelled.set()
        if self.ydl:
            self.ydl.params['outtmpl'] = os.devnull  # 출력을 무시합니다

    def progress_hook(self, d):
        if self.is_cancelled.is_set():
            raise Exception("Download cancelled")
        if d['status'] == 'downloading':
            self.downloaded_bytes = d.get('downloaded_bytes', 0)
            if self.total_bytes > 0:
                progress = (self.downloaded_bytes / self.total_bytes) * 100
            else:
                progress = 0

            if progress < self.max_progress and not self.is_merged_format:
                self.is_video_download = False
            self.max_progress = max(self.max_progress, progress)

            speed = d.get('speed', 0)
            if speed:
                eta = (self.total_bytes - self.downloaded_bytes) / speed
            else:
                eta = 0

            print(f"Emitting progress: {progress:.2f}%, Is Merged Format: {self.is_merged_format}, Is Video: {self.is_video_download}")
            self.signals.progress.emit(self.row, progress, self.format_time(eta), self.is_merged_format, self.is_video_download)

    def postprocessor_hook(self, d):
        if d['status'] == 'started':
            self.merging = True
            self.signals.progress.emit(self.row, 99, "Merging...", self.is_merged_format, self.is_video_download)
        elif d['status'] == 'finished':
            self.merging = False
            self.signals.progress.emit(self.row, 100, "Complete", self.is_merged_format, self.is_video_download)

    @staticmethod
    def format_time(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02.0f}:{m:02.0f}:{s:02.0f}"

    def cleanup_temp_files(self):
        if self.full_path:
            base_path, extension = os.path.splitext(self.full_path)
            base_name = os.path.basename(base_path)
            dir_path = os.path.dirname(self.full_path)

            # Pattern to match temporary files
            pattern = rf"{re.escape(base_name)}\.f\d+{re.escape(extension)}"

            for file_name in os.listdir(dir_path):
                if re.match(pattern, file_name):
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting temporary file {file_path}: {e}")

            # Pattern to match temporary files
            pattern = rf"{re.escape(base_name)}\.f\d+{re.escape(extension)}\.part"

            for file_name in os.listdir(dir_path):
                if re.match(pattern, file_name):
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting temporary file {file_path}: {e}")

            # Check for and delete .part file
            part_file = f"{self.full_path}.part"
            if os.path.exists(part_file):
                try:
                    os.remove(part_file)
                except Exception as e:
                    print(f"Error deleting partial file {part_file}: {e}")

class SelectAllLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.selectAll()

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("유튜브 다운로더")
        self.setGeometry(100, 100, 1200, 800)

        self.apply_global_style()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        # 입력 필드 그리드 레이아웃
        input_layout = QGridLayout()
        url_label = QLabel("영상 링크:")
        url_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.url_input = SelectAllLineEdit()
        self.url_input.setPlaceholderText("YouTube 비디오 URL을 입력하세요")
        input_layout.addWidget(url_label, 0, 0)
        input_layout.addWidget(self.url_input, 0, 1, 1, 2)

        dest_label = QLabel("다운로드 경로:")
        dest_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.dest_input = QLineEdit()
        self.dest_input.setText(self.get_default_download_directory())
        browse_button = QPushButton("폴더 변경")
        browse_button.clicked.connect(self.browse_folder)
        input_layout.addWidget(dest_label, 1, 0)
        input_layout.addWidget(self.dest_input, 1, 1)
        input_layout.addWidget(browse_button, 1, 2)

        self.main_layout.addLayout(input_layout)

        # 검색 버튼
        self.search_button = QPushButton("검색")
        self.search_button.clicked.connect(self.search_video)
        self.main_layout.addWidget(self.search_button)

        # 탭 위젯
        self.tab_widget = QTabWidget()
        self.video_tab = QWidget()
        # self.audio_tab = QWidget() # Feature for version 2.1
        self.tab_widget.addTab(self.video_tab, "동영상")
        # self.tab_widget.addTab(self.audio_tab, "오디오") # Feature for version 2.1

        # 비디오 탭 내용
        video_layout = QVBoxLayout(self.video_tab)
        
        # 스택 위젯 생성
        self.video_stack = QStackedWidget()
        video_layout.addWidget(self.video_stack)

        # 비디오 정보와 테이블을 포함할 컨테이너 위젯
        self.video_content_widget = QWidget()
        self.video_content_layout = QVBoxLayout(self.video_content_widget)
        self.video_content_layout.setSpacing(10)
        self.video_content_layout.setContentsMargins(10, 10, 10, 10)
        
        # 비디오 정보 컨테이너
        self.video_info_widget = QWidget()
        self.video_info_layout = QHBoxLayout(self.video_info_widget)
        self.video_info_layout.setContentsMargins(0, 0, 0, 0)  # 내부 마진 제거
        
        # 썸네일 레이블
        self.thumbnail_label = ClickableLabel()
        self.thumbnail_label.setFixedSize(120, 90)  # 16:9 비율
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.clicked.connect(self.open_video_url)
        self.video_info_layout.addWidget(self.thumbnail_label)
        
        # 비디오 정보를 담을 수직 레이아웃
        video_text_layout = QVBoxLayout()
        video_text_layout.setSpacing(0)  # 위젯 사이의 간격을 0으로 설정
        video_text_layout.setContentsMargins(5, 0, 0, 0)  # 왼쪽에만 약간의 마진 추가
        
        # 비디오 제목 레이블
        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        font = self.title_label.font()
        font.setPointSize(font.pointSize() + 6)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        video_text_layout.addWidget(self.title_label)
        
        # 채널 이 레이블
        self.channel_label = QLabel()
        self.channel_label.setContentsMargins(0, 0, 0, 0)
        self.channel_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        video_text_layout.addWidget(self.channel_label)
        
        # 비디오 길이 레이블
        self.duration_label = QLabel()
        self.duration_label.setStyleSheet("color: gray;")
        self.duration_label.setContentsMargins(0, 0, 0, 0)
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        video_text_layout.addWidget(self.duration_label)
        
        # 수직 레이아웃을 메인 레이아웃에 추가
        self.video_info_layout.addLayout(video_text_layout, 1)  # 1 stretch factor
        
        self.video_content_layout.addWidget(self.video_info_widget)

        # 초기에 비디오 정보 위젯 숨기기
        self.video_info_widget.hide()

        # 비디오 테이블
        self.video_table = QTableWidget()
        self.video_table.setColumnCount(4)
        self.video_table.setHorizontalHeaderLabels(["화질", "포멧", "파일 크기", "다운로드"])
        self.video_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.video_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.video_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.video_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.video_table.verticalHeader().setVisible(False)
        self.video_table.setContentsMargins(0, 0, 0, 0)
        self.video_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #CCCCCC;
                background-color: white;
                margin-top: 0px;  /* 상단 마진 제거 */
            }
            QTableWidget::item {
                padding: 5px;
                border-right: 1px solid #CCCCCC;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                padding: 5px;
                border: none;
                border-right: 1px solid #CCCCCC;
                border-bottom: 1px solid #CCCCCC;
            }
        """)

        self.video_content_layout.addWidget(self.video_table)

        # 스택 위젯에 컨텐츠 추가
        self.video_stack.addWidget(self.video_content_widget)

        # 로딩 위젯 생성
        self.loading_widget = QLabel()
        self.loading_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gif_path = os.path.join(os.path.dirname(__file__), 'assets', 'loading.gif')
        self.loading_movie = QMovie(gif_path)
        if self.loading_movie.isValid():
            self.loading_movie.setScaledSize(QSize(50, 50))
            self.loading_widget.setMovie(self.loading_movie)
        else:
            print(f"Error: Could not load the GIF file at {gif_path}")
        self.video_stack.addWidget(self.loading_widget)

        # 스레드풀 초기화
        self.threadpool = QThreadPool()

        self.ffmpeg_path = self.get_ffmpeg_path()

        self.download_workers = {}
        self.worker_count = 0

        self.video_title = ""
        self.downloading_items = set()  # (video_title, format_id) 튜플을 저

        # 새로운 레이아웃 생성
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.tab_widget)
        self.setup_download_list()
        content_layout.addWidget(self.download_list)
        self.main_layout.addLayout(content_layout)

        self.apply_widget_styles()

    def apply_global_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QLabel, QLineEdit, QTableWidget, QListWidget, QTableWidget::item {
                color: #333333;
            }
            QLineEdit, QTableWidget, QListWidget {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QProgressBar {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                text-align: center;
                background-color: #F0F0F0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #333333;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
            }
            QTableWidget {
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                color: #333333;
                padding: 5px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E0E0E0;
            }
        """)

    def apply_widget_styles(self):
        # 비디오 테이블 스타일
        self.video_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #CCCCCC;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-right: 1px solid #CCCCCC;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                padding: 5px;
                border: none;
                border-right: 1px solid #CCCCCC;
                border-bottom: 1px solid #CCCCCC;
            }
        """)

        # 다운로드 목록 테이블 스타일
        self.download_list.setStyleSheet("""
            QTableWidget {
                border: 1px solid #CCCCCC;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-right: 1px solid #CCCCCC;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                padding: 5px;
                border: none;
                border-right: 1px solid #CCCCCC;
                border-bottom: 1px solid #CCCCCC;
            }
            QProgressBar {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                text-align: center;
                background-color: #F0F0F0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
            QTableCornerButton::section {
                background-color: #E0E0E0;
                border: none;
            }
        """)

    def get_default_download_directory(self):
        if sys.platform == "win32":
            return str(Path.home() / "Downloads")
        elif sys.platform == "darwin":  # macOS
            return str(Path.home() / "Downloads")
        else:  # Linux or other Unix-like systems
            return str(Path.home() / "Downloads")

    def browse_folder(self):
        current_dir = self.dest_input.text()
        if not os.path.isdir(current_dir):
            current_dir = self.get_default_download_directory()
        
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder", current_dir)
        if folder:
            self.dest_input.setText(folder)

    def search_video(self):
        # 다운로드 경로 검증
        dest_path = self.dest_input.text()
        if not os.path.exists(dest_path) or not os.access(dest_path, os.W_OK):
            self.show_error_message("경로 오류", "유효하지 않거나 접근할 수 없는 다운로드 경로입니다.")
            return

        # YouTube 링크 검증
        video_url = self.url_input.text().strip()
        if not video_url:
            self.show_error_message("입력 오류", "YouTube 비디오 URL을 입력해주세요.")
            return

        # UI 업데이트
        self.search_button.setEnabled(False)
        self.video_stack.setCurrentWidget(self.loading_widget)
        self.loading_movie.start()

        # 검색 시작 시 비디오 정보 초기화
        self.clear_video_info()

        # 워커 생성 및 실행
        worker = SearchWorker(video_url, self.ffmpeg_path)
        worker.signals.result.connect(self.search_complete)
        worker.signals.error.connect(self.search_error)
        self.threadpool.start(worker)

    def clear_video_info(self):
        """비디오 정보를 초기화하고 숨깁니다."""
        self.thumbnail_label.clear()
        self.title_label.clear()
        self.channel_label.clear()
        self.duration_label.clear()
        self.video_info_widget.hide()
        self.video_table.setRowCount(0)

    def search_complete(self, info):
        self.loading_movie.stop()
        self.video_stack.setCurrentWidget(self.video_content_widget)
        self.search_button.setEnabled(True)
        self.populate_video_info(info)
        self.populate_video_table(info)

    def search_error(self, error_msg):
        self.loading_movie.stop()
        self.video_stack.setCurrentWidget(self.video_content_widget)
        self.search_button.setEnabled(True)
        self.clear_video_info()  # 에러 발생 시 비디오 정보 초기화

        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setWindowTitle("오류")
        error_box.setText("비디오 정보를 가져오는 데 실패했습니다.")
        error_box.setInformativeText(f"오류 메시지: {error_msg}")
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # 오류 메시지 박스의 스타일 설정
        error_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;
            }
            QMessageBox QLabel {
                color: #000000;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # 버튼 스타일 직접 설정
        button = error_box.button(QMessageBox.StandardButton.Ok)
        if button:
            button.setStyleSheet("""
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
            """)

        error_box.exec()

    def populate_video_info(self, info):
        thumbnail_url = info.get('thumbnail')
        title = info.get('title', 'Unknown Title')
        channel = info.get('channel', '')
        channel_url = info.get('channel_url', '')
        duration = info.get('duration')
        self.video_url = info.get('webpage_url', '')  # 클래스 속성으로 저장

        self.video_title = title  # 클래스 속성으로 저장
        self.title_label.setText(f"제: {title}")

        if thumbnail_url:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                image = QImage()
                image.loadFromData(response.content)
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
                self.thumbnail_label.setPixmap(scaled_pixmap)
                self.thumbnail_label.setFixedSize(scaled_pixmap.size())
                self.thumbnail_label.setCursor(Qt.CursorShape.PointingHandCursor)
                self.thumbnail_label.show()
            else:
                self.thumbnail_label.hide()
        else:
            self.thumbnail_label.hide()

        if title:
            self.title_label.setText(f'<a href="{self.video_url}" style="color: black; text-decoration: none;">{title}</a>')
            self.title_label.setOpenExternalLinks(True)
            self.title_label.show()
        else:
            self.title_label.hide()

        if channel:
            self.channel_label.setText(f'<a href="{channel_url}" style="color: black; text-decoration: none;">{channel}</a>')
            self.channel_label.setOpenExternalLinks(True)
            self.channel_label.show()
        else:
            self.channel_label.hide()

        if duration:
            duration_str = self.format_duration(duration)
            self.duration_label.setText(f"길이: {duration_str}")
            self.duration_label.show()
        else:
            self.duration_label.hide()

        # 썸네일, 제목, 채널, 또는 길이 중 하나라도 있으면 비디오 정보 위젯을 표시
        if thumbnail_url or title or channel or duration:
            self.video_info_widget.show()
        else:
            self.video_info_widget.hide()

    def format_duration(self, seconds):
        """초를 HH:MM:SS 형식으로 변환합니다."""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    def populate_video_table(self, info):
        self.video_table.setRowCount(0)
        self.video_title = info.get('title', 'Unknown Title')
        self.thumbnail_url = info.get('thumbnail')  # 썸네일 URL 저장
        
        # 모든 포맷을 해상도별로 그룹화
        formats_by_resolution_format = {}
        for format in info['formats']:
            height = format.get('height')
            ext = format.get('ext', 'Unknown')
            if height is not None and ext != 'mhtml':
                key = (ext, height)
                if key not in formats_by_resolution_format:
                    formats_by_resolution_format[key] = []
                formats_by_resolution_format[key].append(format)
        
        # 각 해상도 및 포맷별로 최고 품질(파일 크기가 가장 큰) 포맷 선택
        sorted_formats = sorted(formats_by_resolution_format.items(), key=lambda x: (x[0][0] != 'mp4', x[0][0], -x[0][1]))
        for (ext, height), formats in sorted_formats:
            best_format = max(formats, key=lambda f: f.get('filesize', 0) or 0)
            
            row_position = self.video_table.rowCount()
            self.video_table.insertRow(row_position)
            
            # 해상도
            resolution = f"{height}p"
            self.video_table.setItem(row_position, 0, QTableWidgetItem(resolution))
            
            # 포맷
            self.video_table.setItem(row_position, 1, QTableWidgetItem(ext))
            
            # 파일 크기
            filesize = best_format.get('filesize')
            if filesize:
                filesize_str = self.format_size(filesize)
            else:
                filesize_str = 'Unknown'
            self.video_table.setItem(row_position, 2, QTableWidgetItem(filesize_str))
            # 다운로드 버튼
            download_btn = QPushButton("다운로드")
            format_id = best_format['format_id']
            download_btn.clicked.connect(lambda _, f=best_format: self.download_video(f))
            
            # 이미 다운로드 중인 아이템이면 버튼 비활성화
            if (self.video_title, format_id) in self.downloading_items:
                download_btn.setEnabled(False)
                download_btn.setText("다운로드 중")
                download_btn.setStyleSheet("""
                    background-color: #CCCCCC; 
                    color: #666666;
                    border-radius: 4px;
                    padding: 5px 10px;
                    margin: 2px;
                """)
            else:
                download_btn.setStyleSheet("""
                    background-color: #4CAF50; 
                    color: white;
                    border-radius: 4px;
                    padding: 5px 10px;
                    margin: 2px;
                """)
            
            download_btn.setProperty('format_id', format_id)
            self.video_table.setCellWidget(row_position, 3, download_btn)

        # 각 행의 높이를 40픽셀로 설정
        for i in range(self.video_table.rowCount()):
            self.video_table.setRowHeight(i, 40)

    def format_size(self, size_bytes):
        # 바이트를 적���한 단위로 변환
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes/(1024*1024):.2f} MB"
        else:
            return f"{size_bytes/(1024*1024*1024):.2f} GB"

    def update_download_button(self, format_id):
        for row in range(self.video_table.rowCount()):
            download_btn = self.video_table.cellWidget(row, 3)
            if isinstance(download_btn, QPushButton) and download_btn.property('format_id') == format_id:
                if (self.video_title, format_id) in self.downloading_items:
                    download_btn.setEnabled(False)
                    download_btn.setText("다운로드 중")
                    download_btn.setStyleSheet("""
                        background-color: #CCCCCC; 
                        color: #666666;
                        border-radius: 4px;
                        padding: 5px 10px;
                        margin: 2px;
                    """)
                else:
                    download_btn.setEnabled(True)
                    download_btn.setText("다운로드")
                    download_btn.setStyleSheet("""
                        background-color: #4CAF50; 
                        color: white;
                        border-radius: 4px;
                        padding: 5px 10px;
                        margin: 2px;
                    """)
                break

    def download_video(self, format):
        if not hasattr(self, 'video_title') or not self.video_title:
            self.video_title = "Unknown Title"
        
        format_id = format['format_id']
        download_item = (self.video_title, format_id)
        if download_item in self.downloading_items:
            return  # 이미 다운로드 중인 아이템이면 무시
        
        self.downloading_items.add(download_item)
        self.update_download_button(format_id)  # 버튼 상태 업데이트
        
        row = self.download_list.rowCount()
        self.download_list.insertRow(row)
        
        self.add_download_item(row, format)
        
        worker = DownloadWorker(row, self.url_input.text(), format, 
                                self.dest_input.text(), self.video_title)
        worker.signals.progress.connect(self.update_download_progress)
        worker.signals.finished.connect(lambda r: self.download_finished(r, download_item))
        worker.signals.error.connect(lambda r, e: self.download_error(r, e, download_item))
        
        self.download_workers[row] = worker
        self.threadpool.start(worker)

    def add_download_item(self, row, format):
        # 썸네일
        thumb_label = QLabel()
        if hasattr(self, 'thumbnail_url') and self.thumbnail_url:
            try:
                response = requests.get(self.thumbnail_url)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    thumb_label.setPixmap(pixmap.scaled(70, 50, Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    self.set_default_thumbnail(thumb_label)
            except Exception as e:
                print(f"Error loading thumbnail: {e}")
                self.set_default_thumbnail(thumb_label)
        else:
            self.set_default_thumbnail(thumb_label)
        
        thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_list.setCellWidget(row, 0, thumb_label)

        # 비디오 이름
        self.download_list.setItem(row, 1, QTableWidgetItem(self.video_title))

        # 해상도
        self.download_list.setItem(row, 2, QTableWidgetItem(format.get('format_note', 'N/A')))

        # 파일 크기
        size = format.get('filesize') or format.get('filesize_approx')
        size_str = self.format_size(size) if size else "N/A"
        self.download_list.setItem(row, 3, QTableWidgetItem(size_str))

        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.addWidget(progress_bar)
        progress_layout.setContentsMargins(5, 0, 5, 0)
        self.download_list.setCellWidget(row, 4, progress_widget)

        # Set initial color based on whether it's a merged format
        is_merged_format = self.check_if_merged_format(format)
        self.set_progress_bar_color(progress_bar, is_merged_format, True)

        # 남은 시간
        self.download_list.setItem(row, 5, QTableWidgetItem(""))

        # 상태 (취소 버튼)
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(2, 2, 2, 2)
        status_layout.setSpacing(2)
        
        status_label = QLabel("대기 중")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.hide()  # 초기에는 숨김
        
        cancel_button = QPushButton("취소")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4136;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FF7166;
            }
        """)
        cancel_button.clicked.connect(lambda: self.cancel_download(row))
        cancel_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(cancel_button)
        
        self.download_list.setCellWidget(row, 6, status_widget)

        self.download_list.setRowHeight(row, 50)

    def set_default_thumbnail(self, label):
        default_pixmap = QPixmap(70, 50)
        default_pixmap.fill(Qt.GlobalColor.lightGray)
        label.setPixmap(default_pixmap)

    def set_progress_bar_color(self, progress_bar, is_merged_format, is_video):
        if is_merged_format:
            color = "#4CAF50"  # Green color for merged format
            print("Setting progress bar color to Green (Merged Format)")
        elif is_video:
            color = "#2196F3"  # Blue color for video download
            print("Setting progress bar color to Blue (Video Download)")
        else:
            color = "#4CAF50"  # Green color for audio download
            print("Setting progress bar color to Green (Audio Download)")
        
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                text-align: center;
                background-color: #F0F0F0;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)
        progress_bar.repaint()

    def update_download_progress(self, row, progress, time_left, is_merged_format, is_video):
        try:
            progress_widget = self.download_list.cellWidget(row, 4)
            if progress_widget:
                progress_bar = progress_widget.findChild(QProgressBar)
                if progress_bar:
                    progress_bar.setValue(int(progress))
                    self.set_progress_bar_color(progress_bar, is_merged_format, is_video)
                    print(f"Updated progress bar. Value: {int(progress)}, Is Merged Format: {is_merged_format}, Is Video: {is_video}")
            
            time_item = self.download_list.item(row, 5)
            if time_item:
                time_item.setText(time_left)
            
            # Update status
            status_widget = self.download_list.cellWidget(row, 6)
            if status_widget:
                status_label = status_widget.findChild(QLabel)
                cancel_button = status_widget.findChild(QPushButton)
                if status_label:
                    if time_left == "Merging...":
                        status_label.setText("병합중")
                        status_label.show()
                        if cancel_button:
                            cancel_button.hide()
                    elif time_left == "Complete":
                        status_label.setText("완료됨")
                        status_label.show()
                        if cancel_button:
                            cancel_button.hide()
                    else:
                        status_label.hide()
                        if cancel_button:
                            cancel_button.show()
        except Exception as e:
            print(f"Error in update_download_progress: {e}")

    def download_finished(self, row, download_item):
        status_widget = self.download_list.cellWidget(row, 6)
        if status_widget:
            status_label = status_widget.findChild(QLabel)
            cancel_button = status_widget.findChild(QPushButton)
            if status_label:
                status_label.setText("다운로드 완료")
                status_label.show()
            if cancel_button:
                cancel_button.hide()
        del self.download_workers[row]
        self.downloading_items.remove(download_item)
        self.update_download_button(download_item[1])

    def download_error(self, row, error_msg, download_item):
        status_widget = self.download_list.cellWidget(row, 6)
        if status_widget:
            status_label = status_widget.findChild(QLabel)
            cancel_button = status_widget.findChild(QPushButton)
            if status_label:
                status_label.setText("오류 발생")
                status_label.show()
            if cancel_button:
                cancel_button.hide()
        self.show_error_message("다운로드 오류", error_msg)
        del self.download_workers[row]
        self.downloading_items.remove(download_item)
        self.update_download_button(download_item[1])

    def cancel_download(self, row):
        if row in self.download_workers:
            worker = self.download_workers[row]
            worker.cancel()
            
            # 다운로드 중이던 파일 삭제
            if hasattr(worker, 'full_path') and os.path.exists(worker.full_path):
                try:
                    os.remove(worker.full_path)
                    print(f"Deleted file: {worker.full_path}")
                except Exception as e:
                    print(f"Error deleting file: {e}")

            # 부분 다운로드 파일 삭제
            partial_path = worker.full_path + '.part'
            if os.path.exists(partial_path):
                try:
                    os.remove(partial_path)
                    print(f"Deleted partial file: {partial_path}")
                except Exception as e:
                    print(f"Error deleting partial file: {e}")

            status_widget = self.download_list.cellWidget(row, 6)
            if status_widget:
                status_label = status_widget.findChild(QLabel)
                cancel_button = status_widget.findChild(QPushButton)
                if status_label:
                    status_label.setText("취소됨")
                    status_label.show()
                if cancel_button:
                    cancel_button.hide()
            del self.download_workers[row]
            for item in self.downloading_items:
                if item[1] == worker.format['format_id']:
                    self.downloading_items.remove(item)
                    self.update_download_button(item[1])
                    break

            # 프로그레스 바를 0으로 리셋
            progress_widget = self.download_list.cellWidget(row, 4)
            if progress_widget:
                progress_bar = progress_widget.findChild(QProgressBar)
                if progress_bar:
                    progress_bar.setValue(0)
            
            # 남은 시간을 초기화
            time_item = self.download_list.item(row, 5)
            if time_item:
                time_item.setText("")

    def setup_download_list(self):
        self.download_list = QTableWidget()
        self.download_list.setColumnCount(7)
        self.download_list.setHorizontalHeaderLabels(["썸네일", "비디오 이름", "해상도", "파일 크기", "진행률", "남은 시간", "상태"])
        
        # Make the table non-selectable
        self.download_list.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.download_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.download_list.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        header = self.download_list.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        
        self.download_list.setColumnWidth(0, 90)  # 썸네일
        self.download_list.setColumnWidth(3, 100)  # 파일 크기
        self.download_list.setColumnWidth(5, 80)  # 남은 시간
        self.download_list.setColumnWidth(6, 100)  # 상태 (너비를 늘림)

        # Apply stylesheet to make it visually consistent with the video table
        self.download_list.setStyleSheet("""
            QTableWidget {
                border: 1px solid #CCCCCC;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-right: 1px solid #CCCCCC;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                padding: 5px;
                border: none;
                border-right: 1px solid #CCCCCC;
                border-bottom: 1px solid #CCCCCC;
            }
        """)

    def get_ffmpeg_path(self):
        # 시스템에 설치된 ffmpeg 찾기
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            return ffmpeg_path
        
        # 시스템에서 찾지 못한 경우, 기존 로직 사용
        if getattr(sys, 'frozen', False):
            # PyInstaller로 패키징 경우
            return os.path.join(sys._MEIPASS, 'ffmpeg')
        else:
            # 개발 환경에서 실행되는 경우
            return os.path.join(os.path.dirname(__file__), 'ffmpeg')

    def show_error_message(self, title, message):
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # 오류 메시지 박스의 스타일 설정
        error_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;
            }
            QMessageBox QLabel {
                color: #000000;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # 버튼 스타일 직접 설정
        button = error_box.button(QMessageBox.StandardButton.Ok)
        if button:
            button.setStyleSheet("""
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
            """)

        error_box.exec()

    def open_video_url(self):
        if hasattr(self, 'video_url') and self.video_url:
            QDesktopServices.openUrl(QUrl(self.video_url))

    def check_if_merged_format(self, format):
        return 'acodec' in format and format['acodec'] != 'none' and \
               'vcodec' in format and format['vcodec'] != 'none'

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())