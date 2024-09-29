import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTabWidget, QFileDialog, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIcon

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("유튜브 다운로더")
        self.setGeometry(100, 100, 800, 600)

        self.apply_global_style()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 입력 필드 그리드 레이아웃
        input_layout = QGridLayout()
        url_label = QLabel("영상 링크:")
        url_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.url_input = QLineEdit()
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

        main_layout.addLayout(input_layout)

        # 검색 버튼
        self.search_button = QPushButton("검색")
        self.search_button.clicked.connect(self.search_video)
        main_layout.addWidget(self.search_button)

        # 패딩 추가
        main_layout.addSpacing(10)

        # 탭 위젯
        self.tab_widget = QTabWidget()
        self.video_tab = QWidget()
        self.audio_tab = QWidget()
        self.tab_widget.addTab(self.video_tab, "동영상")
        self.tab_widget.addTab(self.audio_tab, "오디오")
        main_layout.addWidget(self.tab_widget)

        # 비디오 탭 내용
        video_layout = QVBoxLayout(self.video_tab)
        self.video_table = QTableWidget()
        self.video_table.setColumnCount(4)
        self.video_table.setHorizontalHeaderLabels(["화질", "포멧", "파일 크기", "다운로드"])
        self.video_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.video_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.video_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.video_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.video_table.verticalHeader().setVisible(False)
        video_layout.addWidget(self.video_table)

        # 다운로드 목록 (테이블 위젯으로 변경)
        self.download_list = QTableWidget()
        self.download_list.setColumnCount(7)
        self.download_list.setHorizontalHeaderLabels([
            "썸네일", "동영상", "화질", "파일 크기", 
            "다운로드 진행 경과", "남은 시간", "상태"
        ])
        self.download_list.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.download_list.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.download_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.download_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.download_list)

        self.apply_widget_styles()

        # 더미 데이터로 다운로드 목록 채우기
        self.populate_download_list()

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
                background-color: #1E90FF;
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
        # URL 유효성 검사 및 비디오 정보 가져오기 구현
        # 예시 데이터로 테이블 채우기
        self.populate_video_table()

    def populate_video_table(self):
        self.video_table.setRowCount(3)
        resolutions = ["1080p (mp4)", "720p (mp4)", "360p (mp4)"]
        file_sizes = ["130.7 MB", "37 MB", "29 MB"]
        
        for i, (res, size) in enumerate(zip(resolutions, file_sizes)):
            resolution_item = QTableWidgetItem(res.split()[0])
            resolution_item.setFlags(resolution_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.video_table.setItem(i, 0, resolution_item)

            format_item = QTableWidgetItem(res.split()[1])
            format_item.setFlags(format_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.video_table.setItem(i, 1, format_item)

            size_item = QTableWidgetItem(size)
            size_item.setFlags(size_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.video_table.setItem(i, 2, size_item)
            
            download_btn = QPushButton("다운로드")
            download_btn.setStyleSheet("""
                background-color: #4CAF50; 
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                margin: 2px;
            """)
            download_btn.clicked.connect(lambda _, row=i: self.download_video(row))
            
            self.video_table.setCellWidget(i, 3, download_btn)
            
            # 각 행의 높이를 40픽셀로 설정
            self.video_table.setRowHeight(i, 40)

        # 테이블의 수직 헤더 (행 번호)를 숨깁니다
        self.video_table.verticalHeader().setVisible(False)

    def download_video(self, row):
        # 선택된 행의 비디오 다운로드 구현
        resolution = self.video_table.item(row, 0).text()
        format = self.video_table.item(row, 1).text()
        print(f"Downloading video: {resolution} {format}")
        # 여기에 실제 다운로드 로직을 구현하세요

    def populate_download_list(self):
        dummy_data = [
            ("thumb1.jpg", "Funny Cat Video", "1080p", "50 MB", 75, "00:30", True),
            ("thumb2.jpg", "Python Tutorial", "720p", "100 MB", 30, "02:00", False),
            ("thumb3.jpg", "Music Video", "480p", "25 MB", 100, "00:00", True),
        ]

        self.download_list.setRowCount(len(dummy_data))
        self.download_list.horizontalHeader().setVisible(True)
        self.download_list.verticalHeader().setVisible(False)  # 수직 헤더 숨기기
        
        # 왼쪽 상단 모서리 버튼 비활성화
        self.download_list.setCornerButtonEnabled(False)

        # 열 너비 조정
        header = self.download_list.horizontalHeader()
        
        # Thumbnail 열
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.download_list.setColumnWidth(0, 50)
        
        # Video Name 열 (늘어나도록 설정)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        # Resolution 열
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.download_list.setColumnWidth(2, 60)
        
        # File Size 열
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.download_list.setColumnWidth(3, 90)
        
        # Progress 열 (늘어나도록 설정)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        # Time Left 열
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.download_list.setColumnWidth(5, 60)
        
        # Status 열
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.download_list.setColumnWidth(6, 100)

        for row, (thumb, name, res, size, progress, time_left, completed) in enumerate(dummy_data):
            # Thumbnail
            thumb_label = QLabel()
            default_icon = QIcon.fromTheme("video-x-generic")  # 시스템 기본 비디오 아이콘 사용
            if default_icon.isNull():
                # 시스템 아이콘이 없는 경우 회색 사각형 생성
                default_pixmap = QPixmap(50, 50)
                default_pixmap.fill(Qt.GlobalColor.white)
            else:
                default_pixmap = default_icon.pixmap(50, 50)
            thumb_label.setPixmap(default_pixmap)
            thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.download_list.setCellWidget(row, 0, thumb_label)

            # Video Name
            self.download_list.setItem(row, 1, QTableWidgetItem(name))

            # Resolution
            self.download_list.setItem(row, 2, QTableWidgetItem(res))

            # File Size
            self.download_list.setItem(row, 3, QTableWidgetItem(size))

            # Progress Bar
            progress_bar = QProgressBar()
            progress_bar.setValue(progress)
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(15)  # 프로그레스 바의 높이를 15픽셀로 고정
            
            # 프로그레스 바를 포함할 위젯 생성
            progress_widget = QWidget()
            progress_layout = QVBoxLayout(progress_widget)
            progress_layout.addWidget(progress_bar)
            progress_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # 수직 중앙 정렬
            progress_layout.setContentsMargins(5, 0, 5, 0)  # 좌우 여백 추가
            
            self.download_list.setCellWidget(row, 4, progress_widget)

            # Time Left
            self.download_list.setItem(row, 5, QTableWidgetItem(time_left))

            # Status (Checkmark)
            status_item = QTableWidgetItem("다운로드 완료" if completed else "다운로드중...")
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.download_list.setItem(row, 6, status_item)

        # 각 행의 높이 설정
        for i in range(self.download_list.rowCount()):
            self.download_list.setRowHeight(i, 50)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())