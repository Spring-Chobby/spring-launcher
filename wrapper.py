from subprocess import call, Popen, PIPE, STDOUT
import sys
import json
import os
import platform
from enum import Enum

class Status(Enum):
    CHECKING_ENGINE = 0
    DOWNLOADING_ENGINE = 1
    CHECKING_GAME = 2
    DOWNLOADING_GAME = 3
    CHECKING_CHOBBY = 4
    DOWNLOADING_CHOBBY = 5
    ERROR_DOWNLOADING = 6
    LAUNCHING_CHOBBY = 7
    CHOBBY_RUNNING = 8
    FINISHED_DOWNLOAD = 9

class Downloader(object):
    def __init__(self):
        platformName = platform.system()
        if platformName == "Windows":
            self.PR_DOWNLOADER_PATH = "./bin/pr-downloader.exe"
            self.SPRING_BIN = "spring.exe"
        elif platformName == "Linux":
            self.PR_DOWNLOADER_PATH = "./bin/pr-downloader"
            self.SPRING_BIN = "spring"
        else:
            # FIXME: this should be printed in the GUI!
            print("Unsupported platform: {}".format(platformName))
            sys.exit(-1)
        print("Detected platform: {}".format(platformName))

        self.status = Status.CHECKING_ENGINE
        self.status_info = ""

    def DownloadEngine(self, ver_string):
        self.status = Status.CHECKING_ENGINE
        p = Popen([self.PR_DOWNLOADER_PATH, '--download-engine', ver_string, '--filesystem-writepath', 'data/'],
            stdout=PIPE,
            stderr=STDOUT)

        for line in iter(p.stdout.readline, b''):
            print(">>> " + line.rstrip().decode('utf-8'))

        status = Status.FINISHED_DOWNLOAD

        #DownloadGame()
        #DownloadChobby()
        self.StartChobby(self.GetGameEngineVersion())

    def DownloadGame(self):
        Popen([self.PR_DOWNLOADER_PATH, 'ba:test', '--filesystem-writepath', 'data/'])

    def DownloadChobby(self):
        p = Popen([self.PR_DOWNLOADER_PATH, 'chobby:test', '--filesystem-writepath', 'data/'],
            stdout=PIPE,
            stderr=STDOUT)

        for line in iter(p.stdout.readline, b''):
            print(">>> " + line.rstrip().decode('utf-8'))

    def StartChobby(self, ver_string):
        Popen(["data/engine/" + ver_string + "/" + self.SPRING_BIN,
            "--write-dir",
            os.getcwd() + "/data",
            "--menu",
            "rapid://chobby:test"])

    def GetGameEngineVersion(self):
        return "103.0.1-1222-g37dc534 develop"
        #TODO: Fix this abomination!
        _sync = unitsync.Unitsync("C:/Users/tzaeru/Documents/ChobbyWrapper/data/engine/103.0.1-1222-g37dc534 develop/unitsync.dll")
        print(_sync.GetSpringVersion())
        #print(_sync.SetSpringConfigString("write-dir", os.getcwd() + "/data")))
        #print(_sync.SetSpringConfigString("SpringData", os.getcwd() + "/data"))
        _sync.Init(True, 1)
        print(_sync.SetSpringConfigFile("C:/Users/tzaeru/Documents/ChobbyWrapper/data/engine/103.0.1-1222-g37dc534 develop/springsettins.cfg"))

        print("COUNT:" + str(_sync.GetDataDirectoryCount()))
        print("IT IS: " + str(_sync.GetDataDirectory(1)))
        print("MODS: " + str(_sync.GetPrimaryModCount()))
        #print("Count: " + str(_sync.GetPrimaryModCount()))
        #print(_sync.AddAllArchives("Chobby"))
        #print(_sync.GetPrimaryModCount())

def test():
    dl = Downloader()
    dl.DownloadGame()
    dl.DownloadEngine(dl.GetGameEngineVersion())
    dl.DownloadChobby()
    dl.StartChobby()

#test()

#[Info] Download complete!
#[Error] ../../tools/pr-downloader/src/FileSystem/FileSystem.cpp:601:extract(): File already exists: data/\engine\103.0.1-1222-g37dc534 develop\AI\Interfaces\Java\0.1\AIInterface.dll
#[Info] extracting (data/\engine\103.0.1-1222-g37dc534 develop\springsettings.cfg)
#[Progress] 100% [==============================] 11747350/11747350 0
#[Progress]  14% [====                          ] 14471581/103362781
