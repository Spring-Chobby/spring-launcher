from subprocess import Popen
import os

from PyQt5.QtCore import QObject, pyqtSignal

from spring_platform import SpringPlatform

class EngineLauncher(QObject):
    lobbyClosed = pyqtSignal(name='lobbyClosed')
    WRITE_FOLDER = os.getcwd() + "/data"

    def StartLauncher(self, ver_string, extraArgs=None):
        args = ["./data/engine/" + ver_string + "/" + SpringPlatform.SPRING_BIN,
            "--write-dir", self.WRITE_FOLDER]
        if extraArgs is not None:
             args = args + extraArgs
        p = Popen(args)
        p.wait()
        self.lobbyClosed.emit()

    def GetGameEngineVersion(self):
        return ""

        #TODO: Fix this abomination!
        _sync = unitsync.Unitsync("C:/Users/tzaeru/Documents/SpringLauncher/data/engine/103.0.1-1222-g37dc534 develop/unitsync.dll")
        print(_sync.GetSpringVersion())
        #print(_sync.SetSpringConfigString("write-dir", os.getcwd() + "/data")))
        #print(_sync.SetSpringConfigString("SpringData", os.getcwd() + "/data"))
        _sync.Init(True, 1)
        print(_sync.SetSpringConfigFile("C:/Users/tzaeru/Documents/SpringLauncher/data/engine/103.0.1-1222-g37dc534 develop/springsettins.cfg"))

        print("COUNT:" + str(_sync.GetDataDirectoryCount()))
        print("IT IS: " + str(_sync.GetDataDirectory(1)))
        print("MODS: " + str(_sync.GetPrimaryModCount()))
        #print("Count: " + str(_sync.GetPrimaryModCount()))
        #print(_sync.AddAllArchives("Chobby"))
        #print(_sync.GetPrimaryModCount())
