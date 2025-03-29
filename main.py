import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QLineEdit,
    QPushButton, QVBoxLayout, QWidget, QComboBox,
    QHBoxLayout, QLabel, QFileDialog, QProgressBar,
    QMenu, QInputDialog, QFrame, QSizePolicy
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, QThreadPool, QRunnable
from PyQt6.QtGui import QIcon, QPalette, QColor, QAction  # QAction moved here
from concurrent.futures import ThreadPoolExecutor
import threading

class SearchWorker(QRunnable):
    def __init__(self, url, callback):
        super().__init__()
        self.url = url
        self.callback = callback

    def run(self):
        self.callback(self.url)

class MultiSearchBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HyperSearch Browser")
        self.setGeometry(100, 100, 1400, 900)

        # Modern UI Theme
        self.setStyleSheet("""
            QMainWindow {background: #1e1e2f; color: #ffffff;}
            QToolBar {background: #2d2d44; border: none; padding: 10px;}
            QComboBox {background: #3b3b58; border: 1px solid #5b5b7b; 
                      border-radius: 5px; padding: 8px; color: #ffffff;}
            QComboBox::drop-down {border-left: 1px solid #5b5b7b;}
            QLineEdit {background: #3b3b58; border: 1px solid #5b5b7b; 
                      border-radius: 5px; padding: 8px; color: #ffffff;}
            QPushButton {background: #007bff; border: none; border-radius: 5px; 
                        padding: 8px 20px; color: #ffffff; font-weight: bold;}
            QPushButton:hover {background: #0056b3;}
            QTabWidget {background: #252537;}
            QTabBar::tab {background: #3b3b58; color: #ffffff; padding: 10px; 
                         border-top-left-radius: 5px; border-top-right-radius: 5px;}
            QTabBar::tab:selected {background: #007bff;}
            QLabel {color: #ffffff;}
            QProgressBar {border: 1px solid #5b5b7b; border-radius: 5px; 
                         background: #3b3b58; color: #ffffff;}
            QProgressBar::chunk {background: #007bff;}
        """)

        # Thread pool for optimization
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(10)

        # Define all_engines first
        self.all_engines = {
            "Text": {
                "Google": "https://www.google.com/search?q={}", "Bing": "https://www.bing.com/search?q={}",
                "Yahoo": "https://search.yahoo.com/search?p={}", "DuckDuckGo": "https://duckduckgo.com/?q={}",
                "Yandex": "https://yandex.com/search/?text={}", "Baidu": "https://www.baidu.com/s?wd={}",
                "Ask": "https://www.ask.com/web?q={}", "AOL": "https://search.aol.com/aol/search?q={}",
                "Ecosia": "https://www.ecosia.org/search?q={}", "Startpage": "https://www.startpage.com/sp/search?query={}",
                "Qwant": "https://www.qwant.com/?q={}", "Swisscows": "https://swisscows.com/web?query={}"
            },
            "Image": {
                "Google Images": "https://www.google.com/search?tbm=isch&q={}", "Bing Images": "https://www.bing.com/images/search?q={}",
                "Yandex Images": "https://yandex.com/images/search?text={}", "TinEye": "https://tineye.com/search?url={}",
                "Pinterest": "https://www.pinterest.com/search/pins/?q={}", "Flickr": "https://www.flickr.com/search/?text={}",
                "Shutterstock": "https://www.shutterstock.com/search?searchterm={}", "Getty Images": "https://www.gettyimages.com/photos/{}",
                "Unsplash": "https://unsplash.com/s/photos/{}", "Pixabay": "https://pixabay.com/images/search/{}", 
                "Pexels": "https://www.pexels.com/search/{}", "Openverse": "https://openverse.org/search/?q={}"
            },
            "File": {
                "Google Files": "https://www.google.com/search?q=filetype:pdf site:*.edu | site:*.org -inurl:(signup | login) {}",
                "IndexOf": "https://www.google.com/search?q=inurl:(index.of | dir) {}", "FilePursuit": "https://filepursuit.com/pursuit?q={}",
                "DocSearch": "https://www.google.com/search?q=filetype:doc | filetype:docx -inurl:(signup | login) {}", 
                "PDF Drive": "https://www.pdfdrive.com/search?q={}", "Scribd": "https://www.scribd.com/search?query={}",
                "SlideShare": "https://www.slideshare.net/search/slideshow?searchfrom=header&q={}", "Z-Library": "https://z-lib.is/s/?q={}",
                "GetIntoPC": "https://getintopc.com/?s={}", "Archive": "https://archive.org/search.php?query={}", 
                "4Shared": "https://www.4shared.com/web/q/search?q={}", "MediaFire": "https://www.mediafire.com/search/?q={}"
            },
            "Audio": {
                "SoundCloud": "https://soundcloud.com/search?q={}", "YouTube": "https://www.youtube.com/results?search_query={}",
                "Spotify": "https://open.spotify.com/search/{}", "Jamendo": "https://www.jamendo.com/search?qs=q={}",
                "FreeMusicArchive": "https://freemusicarchive.org/search/?search-genre={}", "Bandcamp": "https://bandcamp.com/search?q={}",
                "Last.fm": "https://www.last.fm/search?q={}", "Mixcloud": "https://www.mixcloud.com/search/?q={}",
                "ReverbNation": "https://www.reverbnation.com/main/search?q={}", "Audiomack": "https://audiomack.com/search?q={}", 
                "CCMixter": "http://ccmixter.org/search?search_text={}", "SoundClick": "https://www.soundclick.com/search/default.cfm?searchterm={}"
            },
            "Code": {
                "GitHub": "https://github.com/search?q={}", "GitLab": "https://gitlab.com/search?search={}",
                "BitBucket": "https://bitbucket.org/repo/all?name={}", "StackOverflow": "https://stackoverflow.com/search?q={}",
                "CodePen": "https://codepen.io/search/pens?q={}", "SourceForge": "https://sourceforge.net/directory/?q={}",
                "Gist": "https://gist.github.com/search?q={}", "Pastebin": "https://pastebin.com/search?q={}",
                "CodeProject": "https://www.codeproject.com/search.aspx?q={}", "Reddit Programming": "https://www.reddit.com/r/programming/search?q={}",
                "HackerRank": "https://www.hackerrank.com/community?q={}", "LeetCode": "https://leetcode.com/problemset/all/?search={}"
            },
            "AI": {
                "Grok": "https://x.ai/grok?q={}", "Perplexity": "https://www.perplexity.ai/?q={}",
                "You.com": "https://you.com/search?q={}", "ChatGPT": "https://chat.openai.com/?q={}",
                "HuggingFace": "https://huggingface.co/models?search={}", "WolframAlpha": "https://www.wolframalpha.com/input/?i={}",
                "Kagi": "https://kagi.com/search?q={}", "Andi": "https://andisearch.com/?q={}",
                "Writesonic": "https://writesonic.com/?s={}", "Jasper": "https://www.jasper.ai/?q={}", 
                "Claude": "https://anthropic.com/claude?q={}", "Bard": "https://bard.google.com/?q={}"
            },
            "Maps": {
                "Google Maps": "https://www.google.com/maps/search/{}", "OpenStreetMap": "https://www.openstreetmap.org/search?query={}",
                "Bing Maps": "https://www.bing.com/maps?q={}", "MapQuest": "https://www.mapquest.com/search/results?query={}",
                "Waze": "https://www.waze.com/live-map/?q={}", "Here WeGo": "https://wego.here.com/search/{}", 
                "Apple Maps": "https://maps.apple.com/?q={}", "Yandex Maps": "https://yandex.com/maps/?text={}",
                "Mapbox": "https://www.mapbox.com/search/?q={}", "TomTom": "https://www.tomtom.com/en_us/search/?q={}", 
                "2GIS": "https://2gis.com/search/{}", "What3Words": "https://what3words.com/{}"
            },
            "Trends": {
                "Google Trends": "https://trends.google.com/trends/explore?q={}", "Twitter Trends": "https://twitter.com/search?q={}",
                "Reddit Trends": "https://www.reddit.com/search/?q={}&sort=hot", "YouTube Trends": "https://www.youtube.com/results?search_query={}&sp=CAM%253D",
                "TikTok Trends": "https://www.tiktok.com/search?q={}", "Instagram Trends": "https://www.instagram.com/explore/tags/{}", 
                "Pinterest Trends": "https://trends.pinterest.com/?q={}", "BuzzSumo": "https://app.buzzsumo.com/research/content?type=articles&q={}",
                "Ahrefs": "https://app.ahrefs.com/keywords-explorer/google/us/all?keywords={}", "SEMRush": "https://www.semrush.com/analytics/keywordoverview/?q={}", 
                "TrendHunter": "https://www.trendhunter.com/search?q={}", "Exploding Topics": "https://explodingtopics.com/search?term={}"
            }
        }

        # Settings (now after all_engines is defined)
        self.settings_file = "search_settings.json"
        self.load_settings()

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Search bar frame
        self.search_frame = QFrame()
        self.search_frame.setFixedHeight(80)
        self.search_layout = QHBoxLayout(self.search_frame)
        self.search_layout.setSpacing(10)
        self.search_layout.setContentsMargins(20, 10, 20, 10)

        # Search type
        self.search_type = QComboBox()
        self.search_type.addItems(["Text", "Image", "File", "Audio", "Code", "AI", "Maps", "Trends"])
        self.search_type.currentTextChanged.connect(self.update_ui)
        self.search_layout.addWidget(QLabel("Type:"))
        self.search_layout.addWidget(self.search_type)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter query or upload file...")
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_layout.addWidget(self.search_input)

        # Upload button
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setVisible(False)
        self.search_layout.addWidget(self.upload_btn)

        # Search button
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.perform_search)
        self.search_layout.addWidget(self.search_btn)

        # Settings button
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.settings_btn.customContextMenuRequested.connect(self.show_settings_menu)
        self.search_layout.addWidget(self.settings_btn)

        self.main_layout.addWidget(self.search_frame)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.main_layout.addWidget(self.progress)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tabs)

        self.update_active_engines()
        self.uploaded_file = None
        self.active_loads = 0
        self.lock = threading.Lock()

    def load_settings(self):
        default_settings = {cat: list(engines.keys()) for cat, engines in self.all_engines.items()}
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.active_engines = json.load(f)
        else:
            self.active_engines = default_settings
        self.save_settings()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.active_engines, f)

    def update_active_engines(self):
        self.search_engines = {
            cat: {name: url for name, url in engines.items() if name in self.active_engines.get(cat, [])}
            for cat, engines in self.all_engines.items()
        }

    def show_settings_menu(self, pos):
        menu = QMenu(self)
        search_type = self.search_type.currentText()
        engines = self.all_engines[search_type]
        
        for engine in engines:
            action = QAction(engine, self, checkable=True)
            action.setChecked(engine in self.active_engines[search_type])
            action.triggered.connect(lambda checked, e=engine: self.toggle_engine(search_type, e, checked))
            menu.addAction(action)
        
        menu.addSeparator()
        add_action = QAction("Add Custom Engine", self)
        add_action.triggered.connect(lambda: self.add_custom_engine(search_type))
        menu.addAction(add_action)
        
        menu.exec(self.settings_btn.mapToGlobal(pos))

    def toggle_engine(self, category, engine, checked):
        with self.lock:
            if checked and engine not in self.active_engines[category]:
                self.active_engines[category].append(engine)
            elif not checked and engine in self.active_engines[category]:
                self.active_engines[category].remove(engine)
            self.update_active_engines()
            self.save_settings()

    def add_custom_engine(self, category):
        name, ok1 = QInputDialog.getText(self, "Add Engine", "Engine Name:")
        if not ok1 or not name:
            return
        url, ok2 = QInputDialog.getText(self, "Add Engine", "Search URL (use {} for query):")
        if not ok2 or not url:
            return
        self.all_engines[category][name] = url
        self.active_engines[category].append(name)
        self.update_active_engines()
        self.save_settings()

    def update_ui(self):
        search_type = self.search_type.currentText()
        self.upload_btn.setVisible(search_type in ["Image", "File", "Audio"])
        self.search_input.setPlaceholderText(
            "Enter query or upload file..." if search_type not in ["Image", "File", "Audio"]
            else "Upload file or enter query..."
        )

    def upload_file(self):
        search_type = self.search_type.currentText()
        file_types = {
            "Image": "Images (*.png *.jpg *.jpeg *.gif *.bmp)",
            "File": "Documents (*.pdf *.doc *.docx *.txt)",
            "Audio": "Audio Files (*.mp3 *.wav *.ogg)"
        }
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", file_types[search_type]
        )
        if file_path:
            self.uploaded_file = file_path
            self.search_input.setText(os.path.basename(file_path))

    def perform_search(self):
        query = self.search_input.text().strip()
        search_type = self.search_type.currentText()
        
        # Don't proceed if no query or file when required
        if not query and not self.uploaded_file and search_type not in ["Trends"]:
            return

        # Reset UI state
        self.tabs.clear()
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate progress
        
        # Get active search engines for current type
        engines = self.search_engines.get(search_type, {})
        if not engines:
            self.progress.setVisible(False)
            return

        # Handle uploaded file case
        if search_type in ["Image", "File", "Audio"] and self.uploaded_file:
            file_name = os.path.basename(self.uploaded_file)
            query = f"{query} {file_name}" if query else file_name

        # Set up loading tracking
        self.active_loads = len(engines)
        if self.active_loads == 0:
            self.progress.setVisible(False)
            return

        # Launch searches
        for engine_name, base_url in engines.items():
            try:
                formatted_query = query.replace(" ", "+") if query else ""
                url = base_url.format(formatted_query)
                worker = SearchWorker(url, lambda u, n=engine_name: self.load_tab(u, n))
                self.threadpool.start(worker)
            except Exception as e:
                print(f"Error formatting URL for {engine_name}: {e}")
                self.active_loads -= 1

        # Clear uploaded file after search
        self.uploaded_file = None
        self.search_input.clear()  # Optional: clear input after search

    def load_tab(self, url, engine_name):
        try:
            web_view = QWebEngineView()
            web_view.loadFinished.connect(lambda ok: self.check_loading_finished())
            with self.lock:
                tab_index = self.tabs.addTab(web_view, engine_name)
                self.tabs.setTabToolTip(tab_index, url)  # Optional: show URL on hover
            web_view.load(QUrl(url))
        except Exception as e:
            print(f"Error loading tab {engine_name}: {e}")
            self.check_loading_finished()

    def check_loading_finished(self):
        with self.lock:
            self.active_loads -= 1
            if self.active_loads <= 0:
                self.active_loads = 0  # Prevent negative count
                self.progress.setVisible(False)
                QApplication.processEvents()  # Ensure UI updates

    def close_tab(self, index):
        if self.tabs.count() > 0:
            self.tabs.removeTab(index)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e2f"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
    app.setPalette(palette)
    
    browser = MultiSearchBrowser()
    browser.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
