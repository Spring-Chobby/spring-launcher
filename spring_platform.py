import sys
import platform

class Platform(object):
    platformName = platform.system()
    if platformName == "Windows":
        PR_DOWNLOADER_PATH = "./bin/pr-downloader.exe"
        SPRING_BIN = "spring.exe"
    elif platformName == "Linux":
        PR_DOWNLOADER_PATH = "./bin/pr-downloader"
        SPRING_BIN = "spring"
    else:
        # FIXME: this should be printed in the GUI!
        print("Unsupported platform: {}".format(platformName))
        sys.exit(-1)
    print("Detected platform: {}".format(platformName))
