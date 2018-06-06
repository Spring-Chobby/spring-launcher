import platform
import os
import stat
import logging
import json

import concurrent
from concurrent.futures import ThreadPoolExecutor

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

def download_files(update_list, callback):
    def dl_file(update):
        download_file(update["url"], update["path"], callback)

    with ThreadPoolExecutor(max_workers=20) as pool:
        future_to_update = {pool.submit(dl_file, update): update for update in update_list}
        for future in concurrent.futures.as_completed(future_to_update):
            update = future_to_update[future]
            try:
                _ = future.result()
            except Exception as exc:
                logging.error('%r generated an exception: %s' % (update, exc))
                raise exc

def download_file(url, path, callback):
    logging.info("Download file: {} from URL: {}".format(path, url))
    parent = os.path.dirname(path)
    if parent.strip() != "" and not os.path.exists(parent):
        logging.debug("Making subdirs because they do not exist: {}".format(parent))
        try:
            os.makedirs(parent)
        except FileExistsError as e:
            # ignore file exists error due to race conditions
            pass

    mirror = mirrors[0]
    url = mirror + "download?path=" + url
    r = requests.get(url, stream=True)
    # print(requests.head(url, stream=True).headers)
    # we probably don't need to get the content_length again
    # content_length = r.headers.get('Content-length')
    # content_length = int(content_length)

    old_permissions = None
    if os.path.exists(path):
        logging.info("Removing existing file: {}".format(path))
        old_permissions = os.stat(path).st_mode
        os.remove(path)

    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                callback(len(chunk))

    if old_permissions is not None:
        os.chmod(path, old_permissions)
    logging.info("Downloaded: {}".format(path))

def get_update_list(launcher_game_id):
    '''
    returns list of files requiring an update, as dictionaries with keys:
    relURL, path, size
    '''

    # We use the update list as a dictionary so newer paths overwrite older ones
    # This would allow games to overwrite default launcher files
    # In a way it works similar to how Spring mutators work
    update_list = {}
    existing_list = {}

    res = try_get("files/")
    meta = res.json()
    for file, checksum in meta["spring-launcher-dist"].items():
        checksum = checksum["checksum"]
        parts = file.split("/")

        if parts[0] != platformDir:
            continue

        path = os.sep.join(parts[1:])
        if path.strip() == "":
            print(file)

        download_url = "spring-launcher-dist/" + file
        if os.path.exists(path):
            local_checksum = calc_file_checksum(path)
            if checksum != local_checksum:
                update_list[path] = {
                    "url" : download_url,
                    "path" : path,
                    "size" : -1,
                }
                #logging.info("Different file: {}".format(path))
            else:
                existing_list[path] = {
                    "url" : download_url,
                    "path" : path,
                }
        else:
            #logging.info("Missing file: {}".format(path))
            update_list[path] = {
                "url" : download_url,
                "path" : path,
                "size" : -1,
            }

    res = try_get("files/{}".format(launcher_game_id))
    if res.status_code == requests.codes.ok:
        meta = res.json()
        top_key = list(meta.keys())[0]
        for path, keys in meta[top_key].items():
            download_url = keys["path"]
            checksum = keys["checksum"]

            if os.path.exists(path):
                local_checksum = calc_file_checksum(path)
                if checksum != local_checksum:
                    update_list[path] = {
                        "url" : download_url,
                        "path" : path,
                        "size" : -1,
                    }
                    #logging.info("Different file: {}".format(path))
                    if path in existing_list:
                        del existing_list[path]
                else:
                    existing_list[path] = {
                        "url" : download_url,
                        "path" : path,
                    }
            else:
                #logging.info("Missing file: {}".format(path))
                update_list[path] = {
                    "url" : download_url,
                    "path" : path,
                    "size" : -1,
                }
    update_list = list(update_list.values())

    if len(update_list) == 0:
        return update_list, existing_list

    m = mirrors[0]
    urls = [urljoin(m, "download?path=" + up["url"]) for up in update_list]

    # Get all sizes in parallel, so it doesn't fetch them forever
    def get_size(url):
        return int(requests.head(url, stream=True).headers.get("Content-length"))
    with ThreadPoolExecutor(max_workers=50) as pool:
        sizes = list(pool.map(get_size, urls))

    for i, size in enumerate(sizes):
        update_list[i]["size"] = size

    return update_list, existing_list


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
