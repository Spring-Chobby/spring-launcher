import re
from subprocess import Popen, PIPE, STDOUT
import sys
import os
import platform
import stat
import shutil
import tempfile
import logging

from PyQt5.QtCore import QObject, pyqtSignal

from spring_platform import SpringPlatform
import auto_update

class SpringDownloader(QObject):
    downloadStarted = pyqtSignal(str, str, name='downloadStarted')
    downloadFinished = pyqtSignal(name='downloadFinished')
    downloadFailed = pyqtSignal(str, name='downloadFailed')
    downloadProgress = pyqtSignal(int, int, name='downloadProgress')
    FOLDER = "data"

    def __init__(self):
        super(QObject, self).__init__()

        self._InitializePatterns()

    def _InitializePatterns(self):
        self.progressPattern = re.compile("[0-9]+/[0-9]+")
        self.missingPattern = re.compile(".*no engine.*|.*no mirrors.*|.*no game found.*|.*no map found.*|.*error occured while downloading.*")

    # takes line from pr-downloader
    # returns lineType, data
    # lineType is one of "info", "progress", "failed", "extract", "done"
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
        elif line.startswith("[Error]"):
            if self.missingPattern.match(line.lower()):
                lineType = "failed"
                data = "Problem downloading: {}".format(line)
        elif line.startswith("[Info]"):
            if line == "[Info] Download complete!":
                lineType = "info"
                pass
            else:
                lineType = "info"

        return lineType, data

    def _Download(self, args):
        logging.info(" ".join(args))
        p = Popen(args, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
        for line in iter(p.stdout.readline, ""):
            logging.info(line[:-1])
            lineType, data = self._ProcessLine(line)
            if lineType == "progress":
                current, total = data[0], data[1]
                if total > 0:
                    self.downloadProgress.emit(current, total)
            elif lineType == "failed":
                self.downloadFailed.emit(data)
                p.wait()
                return
        self.downloadFinished.emit()

    def _MaybeMakeFolder(self):
        if not os.path.exists(self.FOLDER):
            os.makedirs(self.FOLDER)

    def DownloadEngine(self, ver_string):
        self._MaybeMakeFolder()
        self.downloadStarted.emit(ver_string, "Engine")
        self._Download([SpringPlatform.PR_DOWNLOADER_PATH, '--filesystem-writepath', self.FOLDER, '--download-engine', ver_string])

    def DownloadGame(self, name):
        self._MaybeMakeFolder()
        self.downloadStarted.emit(name, "Game")
        self._Download([SpringPlatform.PR_DOWNLOADER_PATH, '--filesystem-writepath', self.FOLDER, '--download-game', name])

    def DownloadMap(self, name):
        self._MaybeMakeFolder()
        self.downloadStarted.emit(name, "Map")
        self._Download([SpringPlatform.PR_DOWNLOADER_PATH, '--filesystem-writepath', self.FOLDER, '--download-map', name])

    def __mkdtemp(self):
        i = 0
        parent_dir = os.path.dirname(os.getcwd())
        while True:
            tmp_dir = os.path.join(parent_dir, "tmp_{}".format(i))
            if not os.path.exists(tmp_dir):
                try:
                    os.makedirs(tmp_dir)
                    return tmp_dir
                except OSError as e:
                    import traceback
                    logging.error(traceback.format_exc())
                    import sys
                    sys.exit(-1)
            else:
                i = i + 1

    def SelfUpdate(self, launcher_game_id):
        # determine if application is a script file or frozen exe
        if not getattr(sys, 'frozen', False):
            logging.info("Self-update only done for frozen apps.")
            self.downloadFinished.emit()
            return

        update_list, existing_list = auto_update.get_update_list(launcher_game_id)

        if len(update_list) == 0:
            logging.info("No-self update necessary.")
            return

        # Update procedure:
        # 1. Download to Temp Path
        # 2. Move data and maybe some other stuff (logs?) to Temp Path
        # 3. Copy existing to Backup Dir
        # 4. Launch Backup Dir/launcher to do final replacement
        # 5. Delete files in current
        # 6. Move Temp Path files to current
        # 7. Launch current/launcher and resume normal operations


        TMP_DIR = self.__mkdtemp()

        logging.info("Update list: ")
        for i, update in enumerate(update_list):
            update["path"] = os.path.join(TMP_DIR, update["path"])
            logging.info("{}. {} : {:.1f}kB".format(i, update["path"], update["size"] / 1024))

        self.dl_so_far = 0
        self.dl_total = sum([up["size"] for up in update_list])

        def callback(chunk_size):
            self.dl_so_far += chunk_size
            self.downloadProgress.emit(self.dl_so_far, self.dl_total)

        logging.info("Step 1. Download to Temp Path")
        logging.info("Starting self-update...")
        self.downloadStarted.emit("Updating: ", "self")
        auto_update.download_files(update_list, callback)
        logging.info("Self-update completed - restarting.")

        logging.info("Step 1.1. Copy identical existing files to Temp Path")
        logging.info("Copying existing files...")
        for existing in existing_list.values():
            logging.info("Copying: {}".format(existing["path"]))
            dest_path = os.path.join(TMP_DIR, existing["path"])
            dest_dir  = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy2(existing["path"], dest_path)

        # sometimes this could be python, but we ignore this
        # executable = sys.executable

        executable = os.path.join(TMP_DIR, sys.argv[0])

        if platform.system() == "Linux":
            logging.info("Setting proper file mode: {}".format(executable))
            os.chmod(executable, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)

        logging.info("Step 2. Move data and maybe some other stuff (logs?) to Temp Path")
        if os.path.exists("data"):
            shutil.move("data", TMP_DIR)

        curr_path = os.path.abspath(".")

        BK_DIR = self.__mkdtemp()
        logging.info("Step 3. Copy existing to backup")
        print(curr_path, BK_DIR)
        os.rmdir(BK_DIR)
        shutil.copytree(curr_path, BK_DIR)

        logging.info("Step 4. Launch Backup Dir/launcher to do final replacement")
        executable = os.path.join(BK_DIR, sys.argv[0])
        print(executable, "ARGV:", sys.argv)
        # WARNING: We don't support passing old input arguments to the new executable
        print(executable, executable, os.path.basename(executable), *["--temp", TMP_DIR, "--current", curr_path])
        #os.execl(executable, executable, os.path.basename(executable), *["--temp", TMP_DIR, "--current", curr_path])

        import psutil
        try:
            p = psutil.Process(os.getpid())
            for handler in p.get_open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            logging.error(e)


        os.execl(executable, executable, *["--temp", TMP_DIR, "--current", curr_path])

        # Set new install
        shutil.move(TMP_DIR, curr_path)

        # Preserve old install
        # shutil.move(BK_DIR, os.path.join(curr_path, TMP_DIR))

        # Remove old install
        shutil.rmtree(BK_DIR)
        executable = sys.executable

        logging.info("Restarting into: {}".format(sys.argv))
        os.chdir(curr_path)

        os.execl(executable, executable, *sys.argv)
        # This function stops the application before ever sendnig the downloadFinished signal
        return

        # self.downloadFinished.emit()
