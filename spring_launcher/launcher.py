#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    logging.basicConfig(filename='launcher.log', level=logging.INFO, filemode='w')
    logging.info("Started logging...")

    from gui import GUI
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
