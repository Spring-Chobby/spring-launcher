#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

This program creates a quit
button. When we press the button,
the application terminates. 

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication
import json
from subprocess import call, Popen
import os
from unitsync import unitsync
from gui import GUI
import wrapper

#DownloadGame()
#DownloadEngine(GetGameEngineVersion())
#DownloadChobby()
#DownloadGame()
#StartChobby(GetGameEngineVersion())     
        
if __name__ == '__main__':
    
    json_data = None

    with open('config.json') as data_file:
    	json_data = json.load(data_file)

    print(json_data["game_name"])

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

    ## Some commands:
    # PR: pr-downloader --download-engine "103.0.1-1222-g37dc534 develop"
    # PR: pr-downloader ba:stable
    # PR: pr-downloader ba:test
    # pyinstaller: pyinstaller --windowed main.py --paths "C:\Program Files (x86)\Python35-32\Lib\site-packages\PyQt5\Qt\bin"  --onefile
    # spring & chobby:
    # spring.exe --write-dir "C:\Users\tzaeru\Documents\Balanced-Annihilation-Chobby-Installer\data" --menu "Chobby $VERSION"