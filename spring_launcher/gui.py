import json
from threading import Thread
import os
import logging
import sys
import shutil
import copy

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QMainWindow, QSizePolicy, QGraphicsDropShadowEffect, QProgressBar
from PyQt5.QtCore import QCoreApplication, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QColor, QFontDatabase

from spring_downloader import SpringDownloader
from engine_launcher import EngineLauncher
from launcher_config import LauncherConfig
from spring_connector import SpringConnector

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = LauncherConfig()
        if self.config.local_connection is not None:
            logging.info("Local connection available at {}:{}".format(
                                      self.config.local_connection["host"],
                                      self.config.local_connection["port"]))
            self.sc = SpringConnector(self.config.local_connection["host"],
                                      self.config.local_connection["port"])
    #         self.sc.register("CompileMap", self.compileMap)
            self.sc_thread = Thread(target = self.sc.listen)
            self.sc_thread.start()
        self.initUI()

    def closeEvent(self, _):
        os._exit(1)

    def initUI(self):
        fontPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font/Audiowide-Regular.ttf')
        font_id = QFontDatabase.addApplicationFont(fontPath)
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont("Audiowide")
        self.setFont(font)

        self.btnAction = QPushButton('Download Engine', self)
        self.btnAction.clicked.connect(self.OnBtnClick)
        self.btnAction.resize(self.btnAction.sizeHint())
        self.btnAction.move(20, 145)
        self.btnAction.setFont(font)

        self.lblStatus = QLabel('Status label', self)
        self.lblStatus.resize(self.btnAction.sizeHint())
        self.lblStatus.setText("")
        self.lblStatus.setContentsMargins(0,0,0,0);
        self.lblStatus.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.lblStatus.move(190, 150)
        self.lblStatus.setFont(font)
        #self.lblStatus.setStyleSheet("border: 1px solid black;");
        dse = QGraphicsDropShadowEffect(self)
        dse.setBlurRadius(10)
        dse.setColor(QColor("#FFEEEE"))
        dse.setOffset(4,4)
        self.lblStatus.setGraphicsEffect(dse)

        self.pbDownload = QProgressBar(self)
        self.pbDownload.setGeometry(30, 40, 400, 25)
        self.step = 0

        self.setGeometry(300, 300, 550, 250)
        self.setStyleSheet("QMainWindow {border-image: url(data/background.jpg) 0 0 0 0 stretch stretch;}")
        self.setObjectName("Window")
        self.setWindowTitle(self.config.game_title)
        self.show()

        self.dl = SpringDownloader()
        self.dl.downloadStarted.connect(self.OnDownloadStarted)
        self.dl.downloadFinished.connect(self.OnDownloadFinished)
        self.dl.downloadFailed.connect(self.OnDownloadFailed)
        self.dl.downloadProgress.connect(self.OnDownloadProgress)
        self.launcher = EngineLauncher()
        self.launcher.lobbyClosed.connect(self.OnLobbyClosed)

        self.games = copy.deepcopy(self.config.games)
        self.maps = copy.deepcopy(self.config.maps)
        self.engines = copy.deepcopy(self.config.engines)

        if self.engines and len(self.engines) > 0:
            self.launcher.VERSION_STRING = self.engines[0]

        self.actions = ["autoupdate", "packages", "start"]
        if self.config.no_downloads:
            self.actions = ["start"]
        self.DisplayNextAction()
        if self.config.auto_download:
            self.btnAction.setEnabled(False)
            self.MaybeNextStep()

    def DisplayNextAction(self):
        if len(self.actions) == 0:
            return

        nextAction = self.actions[0]
        if nextAction == "packages":
            self.btnAction.setText("Download")
            self.btnAction.resize(self.btnAction.sizeHint())
        elif nextAction == "autoupdate":
            self.btnAction.setText("Self-update")
        elif nextAction == "start":
            self.btnAction.setText("Launch")

    def MaybeNextStep(self):
        self.currentAction = None
        if len(self.actions) == 0:
            self.btnAction.setEnabled(True)
            return

        self.DisplayNextAction()
        self.currentAction = self.actions[0]
        self.actions = self.actions[1:]
        logging.info("Action: {}".format(self.currentAction))
        self.btnAction.setEnabled(False)

        if self.currentAction == "autoupdate":
            logging.info("Checking for autoupdate")
            self.btnAction.setText("Checking for self-updates...")
            thread = Thread(target = self.dl.SelfUpdate, args = (self.config.launcher_game_id,))
            thread.start()
        elif self.currentAction == "packages":
            if len(self.games) != 0:
                self.actions = ["packages"] + self.actions
                game = self.games[0]
                self.games = self.games[1:]
                thread = Thread(target = self.dl.DownloadGame, args = (game,))
                thread.start()
            elif len(self.maps) != 0:
                self.actions = ["packages"] + self.actions
                _map = self.maps[0]
                self.maps = self.maps[1:]
                thread = Thread(target = self.dl.DownloadMap, args = (_map,))
                thread.start()
            elif len(self.engines) != 0:
                self.actions = ["packages"] + self.actions
                engine = self.engines[0]
                self.engines = self.engines[1:]
                thread = Thread(target = self.dl.DownloadEngine, args = (engine,))
                thread.start()
            else:
                if len(self.actions) > 0 and self.actions[0] == "start" and not self.config.auto_start:
                    self.currentAction = None
                    self.btnAction.setEnabled(True)
                    self.DisplayNextAction()
                else:
                    self.MaybeNextStep()
        elif self.currentAction == "start":
            required_files = ["config.json", "springsettings.cfg"]
            for f in required_files:
                if not os.path.exists(os.path.join(self.dl.FOLDER, f)):
                    shutil.copy(f, os.path.join(self.dl.FOLDER, f))

            extraArgs = None
            if self.config.start_args:
                extraArgs = self.config.start_args
            thread = Thread(target = self.launcher.StartLauncher, args = (self.config.engines[0], extraArgs))
            thread.start()
            self.hide()
            # NOTE: This **might** be needed for Windows; test!
            # if platform.name.is_windows():
            #     self.hidden = True
            #     self.setWindowFlags(Qt.ToolTip)
            self.MaybeNextStep()

    @pyqtSlot(str, str)
    def OnDownloadStarted(self, name, type):
        self.lblStatus.setText("Downloading: " + name)
        self.lblStatus.adjustSize()

    @pyqtSlot()
    def OnDownloadFinished(self):
        self.lblStatus.setText("Download finished.")
        self.lblStatus.adjustSize()
        self.MaybeNextStep()

    @pyqtSlot(str)
    def OnDownloadFailed(self, msg):
        self.lblStatus.setText(msg)
        self.lblStatus.adjustSize()

    @pyqtSlot(int, int)
    def OnDownloadProgress(self, current, total):
        self.pbDownload.setValue(current / total * 100)

    @pyqtSlot()
    def OnLobbyClosed(self):
        sys.exit(0)

    def OnBtnClick(self):
        self.MaybeNextStep()

def start():
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
