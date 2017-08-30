from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QMainWindow, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtCore import QCoreApplication, QTimer
from PyQt5.QtGui import QFont, QColor, QFontDatabase
import json
from threading import Thread

import wrapper

class GUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):               
        
        font_id = QFontDatabase.addApplicationFont('C:/Users/tzaeru/Documents/ChobbyWrapper/font/Audiowide-Regular.ttf')
        print(font_id)
        families = QFontDatabase.applicationFontFamilies(font_id)
        print(families)
        font = QFont("Audiowide")
        self.setFont(font)

        qbtn = QPushButton('Download Engine', self)
        qbtn.clicked.connect(self.OnDownloadEngine)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 0)
        qbtn.setFont(font)

        self.status = QLabel('Status label', self)
        self.status.resize(qbtn.sizeHint())
        self.status.setText("...")
        self.status.setContentsMargins(0,0,0,0);
        self.status.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.status.move(50, 50)
        self.status.setFont(font)
        #self.status.setStyleSheet("border: 1px solid black;");
        dse = QGraphicsDropShadowEffect(self)
        dse.setBlurRadius(10)
        dse.setColor(QColor("#FFEEEE"))
        dse.setOffset(4,4)
        self.status.setGraphicsEffect(dse)

        self.timer = QTimer()
        self.timer.timeout.connect(self.CheckStatusUpdates)
        self.timer.start(1)  # 10 times a second
        
        self.setGeometry(300, 300, 250, 150)
        self.setStyleSheet("QMainWindow {border-image: url(data/background.jpg) 0 0 0 0 stretch stretch;}")
        self.setObjectName("Window")
        self.setWindowTitle('Quit button')
        self.show()

    def OnDownloadEngine(self):
        thread = Thread(target = wrapper.DownloadEngine, args = (wrapper.GetGameEngineVersion(), ))
        thread.start()

    def CheckStatusUpdates(self):
        self.status.setText("dsa")
        self.status.setText(str(wrapper.status))
        self.status.adjustSize()