from subprocess import Popen
import os

from PyQt5.QtCore import QObject, pyqtSignal

from spring_platform import Platform

class Launcher(QObject):
    lobbyClosed = pyqtSignal(name='lobbyClosed')

    def StartChobby(self, ver_string):
        p = Popen(["./data/engine/" + ver_string + "/" + Platform.SPRING_BIN,
            "--write-dir",
            os.getcwd() + "/data",
            "--menu",
            "rapid://chobby:test"])
        p.wait()
        self.lobbyClosed.emit()

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
    launcher = Launcher()
    launcher.StartChobby(launcher.GetGameEngineVersion())

if __name__ == "__main__":
    test()
