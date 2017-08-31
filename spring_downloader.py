from PyQt5.QtCore import QObject, pyqtSignal

import re
from subprocess import Popen, PIPE, STDOUT

from spring_platform import Platform

class Downloader(QObject):
    downloadStarted = pyqtSignal(str, str, name='downloadStarted')
    downloadFinished = pyqtSignal(name='downloadFinished')
    downloadFailed = pyqtSignal(name='downloadFailed')
    downloadProgress = pyqtSignal(int, int, name='downloadProgress')

    def __init__(self):
        super(QObject, self).__init__()

        self._InitializePatterns()

    def _InitializePatterns(self):
        self.progressPattern = re.compile("[0-9]+/[0-9]+")

    # takes line from pr-downloader
    # returns lineType, data
    # lineType is one of "info", "progress", "extract", "done"
    # data depends on lineType;
    # info-> data is a string
    # progress-> data is a tuple of (current, max)
    # extract-> data is a tuple of (dstFolder, path)
    # done-> data is None
    def _ProcessLine(self, line):
        lineType = None
        data = None

        if line.startswith("[Progress]"):
            lineType = "progress"

            progressStr = self.progressPattern.search(line).group()
            current, total = progressStr.split("/")
            current = int(current)
            total = int(total)
            data = (current, total)
        elif line.startswith("[Info]"):
            if line == "[Info] Download complete!":
                lineType = "info"
                pass
            else:
                lineType = "info"

        return lineType, data

    def _Download(self, args):
        p = Popen(args,
            stdout=PIPE,
            stderr=STDOUT,
            universal_newlines=True)
        for line in iter(p.stdout.readline, ""):
            lineType, data = self._ProcessLine(line)
            #print(line, lineType, data)
            if lineType == "progress":
                self.downloadProgress.emit(data[0], data[1])
        self.downloadFinished.emit()

    def DownloadEngine(self, ver_string):
        self.downloadStarted.emit(ver_string, "Engine")
        self._Download([Platform.PR_DOWNLOADER_PATH, '--download-engine', ver_string, '--filesystem-writepath', 'data/'])

    def DownloadGame(self):
        self.downloadStarted.emit('ba:test', "Game")
        self._Download([Platform.PR_DOWNLOADER_PATH, 'ba:test', '--filesystem-writepath', 'data/'])

    def DownloadChobby(self):
        self.downloadStarted.emit('chobby:test', "Game")
        self._Download([Platform.PR_DOWNLOADER_PATH, 'chobby:test', '--filesystem-writepath', 'data/'])

def test():
    dl = Downloader()
    dl.DownloadGame()
    dl.DownloadEngine(dl.GetGameEngineVersion())
    dl.DownloadChobby()

#test()
