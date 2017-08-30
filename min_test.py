from subprocess import call
import os

ver_string = "103.0.1-1222-g37dc534 develop"

call(['pr-downloader', '--filesystem-writepath', 'data/', '--download-engine', ver_string])
call(['pr-downloader', '--filesystem-writepath', 'data/', 'chobby:test'])
call(["data/engine/" + ver_string + "/spring.exe", "--write-dir", os.getcwd() + "/data", "--menu", "rapid://chobby:test"])

#[Info] Using filesystem-writepath: C:\Users\tzaeru\Documents\My Games\Spring