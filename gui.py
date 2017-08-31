import json
from threading import Thread
import os

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QMainWindow, QSizePolicy, QGraphicsDropShadowEffect, QProgressBar
from PyQt5.QtCore import QCoreApplication, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QColor, QFontDatabase

from spring_downloader import Downloader
from spring_launcher import Launcher

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        fontPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font/Audiowide-Regular.ttf')
        print(fontPath)
        font_id = QFontDatabase.addApplicationFont(fontPath)
        print("FontID", font_id)
        families = QFontDatabase.applicationFontFamilies(font_id)
        print("Font Families", families)
        font = QFont("Audiowide")
        self.setFont(font)

        qbtn = QPushButton('Download Engine', self)
        qbtn.clicked.connect(self.OnBtnClick)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(20, 145)
        qbtn.setFont(font)

        self.status = QLabel('Status label', self)
        self.status.resize(qbtn.sizeHint())
        self.status.setText("...")
        self.status.setContentsMargins(0,0,0,0);
        self.status.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.status.move(190, 150)
        self.status.setFont(font)
        #self.status.setStyleSheet("border: 1px solid black;");
        dse = QGraphicsDropShadowEffect(self)
        dse.setBlurRadius(10)
        dse.setColor(QColor("#FFEEEE"))
        dse.setOffset(4,4)
        self.status.setGraphicsEffect(dse)

        self.pbDownload = QProgressBar(self)
        self.pbDownload.setGeometry(30, 40, 400, 25)
        self.step = 0

        self.setGeometry(300, 300, 550, 250)
        self.setStyleSheet("QMainWindow {border-image: url(data/background.jpg) 0 0 0 0 stretch stretch;}")
        self.setObjectName("Window")
        self.setWindowTitle('Chobby Launcher')
        self.show()

        self.dl = Downloader()
        self.dl.downloadStarted.connect(self.OnDownloadStarted)
        self.dl.downloadFinished.connect(self.OnDownloadFinished)
        self.dl.downloadFailed.connect(self.OnDownloadFailed)
        self.dl.downloadProgress.connect(self.OnDownloadProgress)
        self.launcher = Launcher()

    @pyqtSlot(str, str)
    def OnDownloadStarted(self, name, type):
        self.status.setText("Downloading: " + name)
        self.status.adjustSize()

    @pyqtSlot()
    def OnDownloadFinished(self):
        self.status.setText("Finished.")
        self.status.adjustSize()

    @pyqtSlot()
    def OnDownloadFailed(self):
        self.status.setText("Failed to download: " + name)
        self.status.adjustSize()

    @pyqtSlot(int, int)
    def OnDownloadProgress(self, current, total):
        self.pbDownload.setValue(current / total * 100)

    def OnBtnClick(self):
        thread = Thread(target = self.dl.DownloadEngine, args = (self.launcher.GetGameEngineVersion(), ))
        thread.start()
