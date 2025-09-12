import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://google.com"))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SWAN Browser")
        self.setGeometry(100, 100, 1200, 800)

        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_urlbar)
        self.setCentralWidget(self.tabs)

        
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        
        back_btn = QAction("←", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        nav_bar.addAction(back_btn)

        
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        nav_bar.addAction(forward_btn)

        
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        nav_bar.addAction(reload_btn)

        
        home_btn = QAction("=", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl("https://google.com"), "New Tab"))
        nav_bar.addAction(new_tab_btn)

        
        self.add_new_tab(QUrl("https://google.com"), "Home")

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://google.com")

        browser = Browser()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda q, browser=browser: self.update_tab_title(browser, q))

    def update_tab_title(self, browser, q):
        i = self.tabs.indexOf(browser)
        if i != -1:
            self.tabs.setTabText(i, browser.page().title())

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def current_browser(self):
        return self.tabs.currentWidget()

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("https://google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://", "https://"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_urlbar(self, i):
        browser = self.current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())
            browser.urlChanged.connect(lambda q, browser=browser: self.url_bar.setText(q.toString()))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
