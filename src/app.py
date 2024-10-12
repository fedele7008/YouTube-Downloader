import sys, os, json, configparser, subprocess

from enum import Enum
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QSizePolicy, QFileDialog, QMessageBox, 
                             QStackedLayout, QTabWidget, QTableWidget, QHeaderView, QTableWidgetItem,
                             QFrame)
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QFontDatabase, QMovie, QDesktopServices, QPixmap, QImage


def get_resource_path():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources"))


def get_default_download_dir_path():
    return str(os.path.join(Path.home(), "Downloads"))


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024*1024:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024*1024*1024:
        return f"{size_bytes/(1024*1024):.2f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.2f} GB"

class Locale(Enum):
    ko_KR = 1
    en_US = 2
    
    @classmethod
    def parse_string(cls, string_value):
        try:
            return cls[string_value]
        except KeyError:
            raise ValueError(f"{string_value} is not a valid {cls.__name__}")

    def to_string(self):
        return self.name
    
    @classmethod
    def get_default(cls):
        return cls.en_US
    
    @classmethod
    def validate(cls, string_value):
        try:
            cls.parse_string(string_value)
            return True
        except ValueError:
            return False

    
class Theme(Enum):
    light = 1
    dark = 2
    
    @classmethod
    def parse_string(cls, string_value):
        try:
            return cls[string_value]
        except KeyError:
            raise ValueError(f"{string_value} is not a valid {cls.__name__}")

    def to_string(self):
        return self.name
    
    @classmethod
    def get_default(cls):
        return cls.light
    
    @classmethod
    def validate(cls, string_value):
        try:
            cls.parse_string(string_value)
            return True
        except ValueError:
            return False
        

class Font():
    registered_font_families = set()
    
    @classmethod
    def get_default(cls):
        return QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont).family()
    
    @classmethod
    def register_font(cls, font_path: str):
        # validate if font_path exists
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")
        
        # validate if font_path is a valid font file
        if not font_path.endswith(".ttf"):
            raise TypeError(f"Invalid font file: {font_path}")
        
        # register font
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            raise RuntimeError(f"Failed to register font file: {font_path}")
        cls.registered_font_families.add(QFontDatabase.applicationFontFamilies(font_id)[0])

        print(f"Registered font file [ID: {font_id}]: {font_path}")

    @classmethod
    def register_font_dir(cls, font_dir_path: str):
        # validate if font_dir_path exists
        if not os.path.exists(font_dir_path):
            raise FileNotFoundError(f"Font directory not found: {font_dir_path}")
        
        # validate if font_dir_path is a directory
        if not os.path.isdir(font_dir_path):
            raise TypeError(f"Invalid font directory: {font_dir_path}")
        
        font_files = [os.path.join(font_dir_path, f) for f in os.listdir(font_dir_path) if f.endswith(".ttf")]
        fonts_found = 0
        for font_file in font_files:
            try:
                cls.register_font(font_file)
                fonts_found += 1
            except Exception as e:
                print(f"Failed to register font file '{font_file}': {e}")
        
        print(f"Registered {fonts_found} font files from '{font_dir_path}'")

    @classmethod
    def validate_font_family(cls, font_family: str):
        # validate if font_family is registered explicitly or in the system font
        return font_family in QFontDatabase.families()


class UrlInput(QLineEdit):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.selectAll()


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
    

class YouTubeDownloader(QMainWindow):
    fonts_registered = False
    min_font_size = 8
    max_font_size = 32

    def __init__(self, **kwargs):
        super().__init__()
        
        self.parse_args(kwargs)
        
        with open(os.path.join(get_resource_path(), "config", "locale.json"), "r") as locale_file:
            self.locale_data = json.load(locale_file)
            
        self.component_text = self.locale_data[self.config["settings"]["locale"].to_string()]["components"]

        self.setWindowTitle(self.component_text["app-title"])
        self.setGeometry(100, 100, 900, 600)
        self.apply_style()
        self.init_ui()
    
    def register_fonts(self):
        if YouTubeDownloader.fonts_registered is True:
            return
        font_dir = os.path.join(get_resource_path(), "fonts")
        Font.register_font_dir(font_dir)
        YouTubeDownloader.fonts_registered = True
        print(f"Available font families: {Font.registered_font_families}")
        
    def load_config(self):
        if YouTubeDownloader.fonts_registered is False:
            self.register_fonts()

        self.config = {
            "settings": {
                "locale": Locale.get_default(),
                "theme": Theme.get_default(),
                "font": Font.get_default(),
                "font-size": 12
            }
        }
        
        config = configparser.ConfigParser()
        config_file_list = config.read(os.path.join(get_resource_path(), "config", "config.ini"))
        if len(config_file_list) == 0:
            print(f"Failed to read config file. Use default config instead:\n{self.config}", file=sys.stderr)
            return

        if not config.has_section("settings"):
            print(f"No 'settings' section found in the config file. Use default config instead:\n{self.config}", file=sys.stderr)
            return
        
        if config.has_option("settings", "locale"):
            try:
                self.config["settings"]["locale"] = Locale.parse_string(config.get("settings", "locale"))
            except ValueError:
                print(f"Invalid locale value '{config.get('settings', 'locale')}'. Use default config['settings']['locale']: '{self.config['settings']['locale']}'", file=sys.stderr)
        else:
            print(f"No 'locale' option found in the 'settings' section. Use default config['settings']['locale']: '{self.config['settings']['locale']}'", file=sys.stderr)

        if config.has_option("settings", "theme"):
            try:
                self.config["settings"]["theme"] = Theme.parse_string(config.get("settings", "theme"))
            except:
                print(f"Invalid theme value '{config.get('settings', 'theme')}'. Use default config['settings']['theme']: '{self.config['settings']['theme']}'", file=sys.stderr)
        else:
            print(f"No 'theme' option found in the 'settings' section. Use default config['settings']['theme']: '{self.config['settings']['theme']}'", file=sys.stderr)
            
        if config.has_option("settings", "font"):
            font_str = config.get("settings", "font")
            if Font.validate_font_family(font_str):
                self.config["settings"]["font"] = QFontDatabase.families()[QFontDatabase.families().index(font_str)]
            else:
                print(f"Invalid font value '{font_str}'. Use default config['settings']['font']: '{self.config['settings']['font']}'", file=sys.stderr)
        else:
            print(f"No 'font' option found in the 'settings' section. Use default config['settings']['font']: '{self.config['settings']['font']}'", file=sys.stderr)
            
        if config.has_option("settings", "font-size"):
            try:
                font_size = int(config.get("settings", "font-size"))
                if font_size < YouTubeDownloader.min_font_size or font_size > YouTubeDownloader.max_font_size:
                    print(f"Invalid font size-value '{font_size}'. Use default config['settings']['font-size']: '{self.config['settings']['font-size']}'", file=sys.stderr)
                else:
                    self.config["settings"]["font-size"] = font_size
            except ValueError:
                print(f"Invalid font size-value '{config.get('settings', 'font-size')}'. Use default config['settings']['font-size']: '{self.config['settings']['font-size']}'", file=sys.stderr)

    def load_ffmpeg(self):
        dependency_path = os.path.join(get_resource_path(),
                                       "dependencies",
                                       "macos" if sys.platform == "darwin" else "windows")
        self.ffmpeg_path = os.path.join(dependency_path, "ffmpeg" if sys.platform == "darwin" else "ffmpeg.exe")
        
        # Test if ffmpeg is available
        if not os.path.isfile(self.ffmpeg_path):
            raise ImportError(f"ffmpeg not found at '{self.ffmpeg_path}'. Please make sure to install FFmpeg before running the application.")
        
    def parse_args(self, kwargs):
        if not hasattr(self, "config"):
            self.load_config()
            self.load_ffmpeg()
        
        for key, value in kwargs.items():
            match key:
                case "locale":
                    try:
                        if type(value) is str:
                            locale = Locale.parse_string(value)
                        elif type(value) is Locale:
                            locale = value
                        else:
                            raise TypeError("Invalid argument type for locale")
                        self.config["settings"]["locale"] = locale
                    except ValueError:
                        print(f"Invalid locale value '{value}'. Use fallback config['settings']['locale']: '{self.config['settings']['locale']}'", file=sys.stderr)
                case "theme":
                    try:
                        if type(value) is str:
                            theme = Theme.parse_string(value)
                        elif type(value) is Theme:
                            theme = value
                        else:
                            raise TypeError("Invalid argument type for theme")
                        self.config["settings"]["theme"] = theme
                    except ValueError:
                        print(f"Invalid theme value '{value}'. Use fallback config['settings']['theme']: '{self.config['settings']['theme']}'", file=sys.stderr)
                case "font":
                    if type(value) is not str:
                        raise TypeError("Invalid argument type for font")
                    if Font.validate_font_family(value):
                        self.config["settings"]["font"] = QFontDatabase.families()[QFontDatabase.families().index(value)]
                    else:
                        print(f"Invalid font value '{value}'. Use fallback config['settings']['font']: '{self.config['settings']['font']}'", file=sys.stderr)
                case "font_size":
                    if type(value) is not int:
                        raise TypeError("Invalid argument type for font-size")
                    if value < YouTubeDownloader.min_font_size or value > YouTubeDownloader.max_font_size:
                        print(f"Invalid font size value '{value}'. Use fallback config['settings']['font-size']: '{self.config['settings']['font-size']}'", file=sys.stderr)
                    else:
                        self.config["settings"]["font-size"] = value
        
    def apply_style(self):
        style_paths = []
        
        global_style_file_path = os.path.join(get_resource_path(), "style", "global.qss")
        style_paths.append(global_style_file_path)
        
        match self.config["settings"]["theme"]:
            case Theme.light:
                theme_file = "light-theme.qss"
            case Theme.dark:
                theme_file = "dark-theme.qss"
            case _:
                raise ValueError("Invalid theme")
        
        theme_file_path = os.path.join(get_resource_path(), "style", theme_file)
        style_paths.append(theme_file_path)
        
        font = self.config["settings"]["font"]
        font_size = self.config["settings"]["font-size"]
        style = f"""
        * {{
            font-family: "{font}";
            font-size: {font_size}px;
        }}
        QLabel[class="error-label"] {{
            font-size: {font_size-2}px;
        }}
        """
        for stylesheet in style_paths:
            with open(stylesheet, "r") as style_file:
                style += style_file.read() + "\n"
                
        self.setStyleSheet(style)
        
    def get_asset(self, asset_file_name):
        asset_path = os.path.join(get_resource_path(), "assets", asset_file_name)
        
        if not os.path.isfile(asset_path):
            raise FileNotFoundError(f"Asset file '{asset_file_name}' not found")
        
        return asset_path
    
    def open_video_url(self):
        # [DEBUG-START]
        self.video_url = "https://www.youtube.com/"
        # [DEBUG-END]
        if hasattr(self, "video_url") and self.video_url:
            QDesktopServices.openUrl(QUrl(self.video_url))
            
    def open_channel_url(self):
        # [DEBUG-START]
        self.channel_url = "https://www.youtube.com/"
        # [DEBUG-END]
        if hasattr(self, "channel_url") and self.channel_url:
            QDesktopServices.openUrl(QUrl(self.channel_url))
        
    def init_ui(self):
        # Configure main widget
        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        
        # Configure input layout
        self.input_layout = QGridLayout()
        self.url_label = QLabel(self.component_text["url-label"])
        self.url_label.setProperty("class", "input-label")
        self.url_input = UrlInput()
        self.url_input.setPlaceholderText(self.component_text["url-input-placeholder"])
        self.dest_label = QLabel(self.component_text["download-path-label"])
        self.dest_label.setProperty("class", "input-label")
        self.dest_input = QLineEdit()
        self.dest_input.setText(get_default_download_dir_path())
        self.input_error_label = QLabel("Test error message")
        self.input_error_label.hide()
        self.input_error_label.setProperty("class", "error-label")
        self.input_error_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.browse_button = QPushButton(self.component_text["browse-button"])
        self.search_button = QPushButton(self.component_text["search-button"])
        self.search_button.setObjectName("search-button")
        self.search_button.setProperty("class", "primary")
        self.search_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        self.url_input.returnPressed.connect(self.handle_search_button_click)
        self.dest_input.textChanged.connect(self.handle_dest_input_changed)
        self.search_button.clicked.connect(self.handle_search_button_click)
        self.browse_button.clicked.connect(self.handle_browse_button_click)

        self.input_layout.addWidget(self.url_label, 0, 0)
        self.input_layout.addWidget(self.url_input, 0, 1, 1, 2)
        self.input_layout.addWidget(self.dest_label, 1, 0)
        self.input_layout.addWidget(self.dest_input, 1, 1)
        self.input_layout.addWidget(self.browse_button, 1, 2)
        self.input_layout.addWidget(self.search_button, 0, 3, 2, 1)
        self.input_layout.addWidget(self.input_error_label, 2, 1, 1, 2)
        self.input_layout.setSpacing(7)
        
        self.main_layout.addLayout(self.input_layout)
        
        # Configure video layout
        self.video_widget = QWidget()
        self.video_widget.setMaximumHeight(600)
        self.video_layout = QStackedLayout(self.video_widget)
        self.video_content_widget = QWidget()
        self.video_content_widget.setProperty("class", "video-content")
        self.video_loading_widget = QWidget()
        self.video_loading_widget.setProperty("class", "video-content")
        self.video_content_layout = QVBoxLayout(self.video_content_widget)
        self.video_content_layout.setSpacing(10)
        self.video_loading_layout = QVBoxLayout(self.video_loading_widget)
        self.video_loading_layout.setSpacing(20)
        
        # Configure video loading widget
        self.loading_widget = QLabel()
        self.loading_widget.setObjectName("loading-widget")
        self.loading_movie = QMovie(self.get_asset("loading.gif"))
        if self.loading_movie.isValid():
            self.loading_movie.setScaledSize(QSize(50, 50))
            self.loading_widget.setMovie(self.loading_movie)
            self.loading_movie.start()
        else:
            print(f"Failed to load loading animation", file=sys.stderr)

        self.loading_label = QLabel(self.component_text["loading-label"])
        self.loading_label.setObjectName("loading-label")
        self.video_loading_layout.addWidget(self.loading_widget)
        self.video_loading_layout.addWidget(self.loading_label)
        
        # Configure video content widget
        self.video_info_widget = QWidget()
        self.video_info_widget.setMaximumHeight(120)
        self.video_info_layout = QHBoxLayout(self.video_info_widget)
        self.video_info_layout.setContentsMargins(0,0,0,0)
        
        # Configure video thumbnail widget
        self.thumbnail_widget = ClickableLabel()
        self.thumbnail_widget.setMaximumHeight(self.video_info_widget.maximumHeight())
        self.thumbnail_widget.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.thumbnail_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.thumbnail_widget.clicked.connect(self.open_video_url)
        self.thumbnail_widget.setProperty("class", "thumbnail-widget")

        # [DEBUG-START]
        image = QImage(self.get_asset("sample.png"))
        default_pixmap = QPixmap.fromImage(image).scaledToHeight(self.thumbnail_widget.height())
        self.thumbnail_widget.setPixmap(default_pixmap)
        # [DEBUG-END]
        
        # Configure video info
        self.video_info_text_widget = QWidget()
        self.video_info_text_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.video_info_text_layout = QVBoxLayout(self.video_info_text_widget)
        self.video_info_text_layout.setContentsMargins(0,0,0,0)
        self.video_info_text_layout.setSpacing(4)
        
        self.video_info_text_title = ClickableLabel()
        self.video_info_text_title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.video_info_text_title.clicked.connect(self.open_video_url)
        self.video_info_text_title.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.video_info_text_channel = ClickableLabel()
        self.video_info_text_channel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.video_info_text_channel.clicked.connect(self.open_channel_url)
        self.video_info_text_channel.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.video_info_text_stretch = QWidget()
        self.video_info_text_stretch.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.video_info_text_length = QLabel()

        # [DEBUG-START]
        self.video_info_text_title.setText("Test Video Title")
        self.video_info_text_channel.setText("Test Channel")
        self.video_info_text_length.setText("Test Duration")
        # [DEBUG-END]
        
        self.video_info_text_layout.addWidget(self.video_info_text_title)
        self.video_info_text_layout.addWidget(self.video_info_text_channel)
        self.video_info_text_layout.addWidget(self.video_info_text_stretch)
        self.video_info_text_layout.addWidget(self.video_info_text_length)

        self.video_info_layout.addWidget(self.thumbnail_widget)
        self.video_info_layout.addWidget(self.video_info_text_widget)

        self.download_tab_widget = QTabWidget()
        self.video_download_tab = QWidget()
        self.video_download_tab_layout = QVBoxLayout(self.video_download_tab)
        self.audio_download_tab = QWidget()
        self.audio_download_tab_layout = QVBoxLayout(self.audio_download_tab)
        self.download_tab_widget.addTab(self.video_download_tab, self.component_text["video-download-tab"])
        self.download_tab_widget.addTab(self.audio_download_tab, self.component_text["audio-download-tab"])
        
        # Configure video download tab
        self.video_table_widget = QTableWidget()
        self.video_table_widget.setColumnCount(4)
        self.video_table_widget.setHorizontalHeaderLabels(self.component_text["video-download-table-header"])
        header = self.video_table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.video_table_widget.horizontalHeader().setSectionsClickable(False)
        self.video_table_widget.setAutoScroll(False)
        self.video_table_widget.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.video_table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.video_table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.video_table_widget.verticalHeader().setSectionsClickable(False)
        self.video_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.video_table_widget.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_table_widget.setShowGrid(False)
        self.video_table_widget.setCornerButtonEnabled(False)

        # [DEBUG-START] Add dummy rows for the table -- start 
        self.video_table_widget.setRowCount(10)
        for row in range(self.video_table_widget.rowCount()):
            for col in range(self.video_table_widget.columnCount()):
                item = QTableWidgetItem(f"Row {row+1}, Column {col+1} content")
                self.video_table_widget.setItem(row, col, item)
        # [DEBUG-END] Add dummy rows for the table -- end 

        self.video_download_tab_layout.addWidget(self.video_table_widget)
        
        # Configure video download tab
        self.audio_table_widget = QTableWidget()
        self.audio_table_widget.setColumnCount(4)
        self.audio_table_widget.setHorizontalHeaderLabels(self.component_text["video-download-table-header"])
        header = self.audio_table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.audio_table_widget.horizontalHeader().setSectionsClickable(False)
        self.audio_table_widget.setAutoScroll(False)
        self.audio_table_widget.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.audio_table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.audio_table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.audio_table_widget.verticalHeader().setSectionsClickable(False)
        self.audio_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.audio_table_widget.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_table_widget.setShowGrid(False)
        self.audio_table_widget.setCornerButtonEnabled(False)   

        self.audio_download_tab_layout.addWidget(self.audio_table_widget)
        
        # Continuation of video content configuration...
        self.video_content_layout.addWidget(self.video_info_widget)
        self.video_content_line_separator = QWidget()
        self.video_content_line_separator.setProperty("class", "hline")
        self.video_content_line_separator.setFixedHeight(2)
        self.video_content_line_separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.video_content_layout.addWidget(self.video_content_line_separator)
        self.video_content_layout.addWidget(self.download_tab_widget)

        self.video_layout.addWidget(self.video_content_widget)
        self.video_layout.addWidget(self.video_loading_widget)
        self.video_layout.setCurrentWidget(self.video_content_widget)

        self.main_layout.addWidget(self.video_widget)
        
        # Configure 
        self.download_status_table = QTableWidget()
        self.download_status_table.setColumnCount(7)
        self.download_status_table.setHorizontalHeaderLabels(self.component_text["video-download-status-table-header"])
        self.download_status_table.horizontalHeader().setSectionsClickable(False)
        self.download_status_table.setAutoScroll(False)
        self.download_status_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.download_status_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.download_status_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.download_status_table.verticalHeader().setSectionsClickable(False)
        self.download_status_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.download_status_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_status_table.setShowGrid(False)
        self.download_status_table.setCornerButtonEnabled(False)
        header = self.download_status_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.main_layout.addWidget(self.download_status_table)
        
        # [DEBUG-START] Add dummy rows for the table -- start 
        self.download_status_table.setRowCount(10)
        for row in range(self.download_status_table.rowCount()):
            for col in range(self.download_status_table.columnCount()):
                item = QTableWidgetItem(f"Row {row+1}, Column {col+1} content")
                self.download_status_table.setItem(row, col, item)
        # [DEBUG-END] Add dummy rows for the table -- end 
        
    def handle_dest_input_changed(self):
        enable_search_button = True
        if not self.dest_input.text():
            enable_search_button = False
            self.input_error_label.setText(self.component_text["input-error-message-empty-dest"])
        elif not os.path.isdir(self.dest_input.text()):
            enable_search_button = False
            self.input_error_label.setText(self.component_text["input-error-message-dest-dir-not-exist"])
        elif not os.access(self.dest_input.text(), os.W_OK):
            enable_search_button = False
            self.input_error_label.setText(self.component_text["input-error-message-dest-dir-not-writable"])
        
        self.search_button.setEnabled(enable_search_button)
        if enable_search_button:
            self.input_error_label.hide()
        else:
            self.input_error_label.show()

    def handle_search_button_click(self):
        if not self.search_button.isEnabled():
            return
        
        if not self.url_input.text():
            self.prompt_error_message(self.component_text["input-error-prompt-title"], self.component_text["input-error-prompt-message-empty-url"])
            return
        
        if True:
            self.prompt_error_message(self.component_text["input-error-prompt-title"], self.component_text["input-error-prompt-message-invalid-video"])
            return

    def handle_browse_button_click(self):
        download_dest_dir = self.dest_input.text()
        browse_dir = download_dest_dir
        if not os.path.isdir(browse_dir) or not os.access(browse_dir, os.W_OK):
            browse_dir = get_default_download_dir_path()
        destination_directory = QFileDialog.getExistingDirectory(self, self.component_text["browse-dialog-title"], browse_dir)
        if destination_directory:
            self.dest_input.setText(destination_directory)

    def prompt_error_message(self, title: str, message: str, informative_message: str = None):
        error_dialog = QMessageBox(self)
        error_dialog.setProperty("class", "error-dialog")
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        if informative_message:
            error_dialog.setInformativeText(informative_message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        okay_button = error_dialog.button(QMessageBox.StandardButton.Ok)
        okay_button.setText(self.component_text["ok-button-text"])
        error_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader(locale=Locale.en_US, theme=Theme.light)
    window.show()
    sys.exit(app.exec())
