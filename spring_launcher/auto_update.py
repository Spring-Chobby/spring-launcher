import platform
import os
import logging
import json

import requests
from requests.compat import urljoin, quote_plus

# TODO: Properly use mirrors and load them from a file (which is also synced)
mirrors = ["http://tzaeru.com:4445/"]

platformToDir = {
    "Linux": "linux",
    "Darwin": "mac",
    "Windows": "windows"
}

platformDir = platformToDir[platform.system()]

def try_get(resource):
    #quoted = quote_plus(resource)
    for m in mirrors:
        url = urljoin(m, resource)
        r = requests.get(url)
        return r

def download_file(url, path):
    logging.info("Download file: {} from URL: {}".format(path, url))
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs

    mirror = mirrors[0]
    url = mirror + "download?path=" + url
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def synchronize():
    res = try_get("files/")
    meta = res.json()
    for file, checksum in meta["spring-launcher-dist"].items():
        checksum = checksum["checksum"]
        parts = file.split("/")

        if parts[0] != platformDir:
            continue

        path = os.sep.join(parts[1:])

        download_url = "spring-launcher-dist/" + file
        if os.path.exists(path):
            local_checksum = calc_file_checksum(path)
            if checksum != local_checksum:
                logging.info("Different file: {}".format(path))
                download_file(download_url, path)
        else:
            logging.info("Missing file: {}".format(path))
            download_file(download_url, path)


# TODO: separate module

from sys import argv
from hashlib import sha1
from io import BytesIO

class githash(object):
    def __init__(self):
        self.buf = BytesIO()

    def update(self, data):
        self.buf.write(data)

    def hexdigest(self):
        data = self.buf.getvalue()
        h = sha1()
        h.update(("blob %u\0" % len(data)).encode())
        #h.update()
        h.update(data)

        return h.hexdigest()

def githash_data(data):
    h = githash()
    h.update(data)
    return h.hexdigest()

def githash_fileobj(fileobj):
    return githash_data(fileobj.read())

def calc_file_checksum(path):
    fileobj = open(path, "rb")
    return githash_fileobj(fileobj)
