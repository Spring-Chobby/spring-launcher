import platform
import os
import stat
import logging
import json
import concurrent
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.compat import urljoin, quote_plus

from .githash import calc_file_checksum

# TODO: Properly use mirrors and load them from a file (which is also synced)
mirrors = ["http://tzaeru.com:4445/"]

platformToDir = {
    "Linux": "linux",
    "Darwin": "mac",
    "Windows": "windows"
}

def try_get(resource):
    #quoted = quote_plus(resource)
    for m in mirrors:
        url = urljoin(m, resource)
        r = requests.get(url)
        return r

def download_files(update_list, callback=None, root_path=None):
    if root_path is None:
        root_path = os.getcwd()
    def dl_file(update):
        download_file(update["server_path"],
                      os.path.join(root_path, update["local_path"]),
                      checksum=update["checksum"],
                      callback=callback)

    with ThreadPoolExecutor(max_workers=20) as pool:
        future_to_update = {pool.submit(dl_file, update): update for update in update_list}
        for future in concurrent.futures.as_completed(future_to_update):
            update = future_to_update[future]
            try:
                _ = future.result()
            except Exception as exc:
                logging.error('%r generated an exception: %s' % (update, exc))
                raise exc

def download_file(url, path, checksum=None, callback=None, max_attempts=5):
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

    retry_count = 0
    while True:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    if callback is not None:
                        callback(len(chunk))
        if checksum is None or calc_file_checksum(path) == checksum:
            break
        elif retry_count >= max_attempts:
            raise Exception("Failed to download correct file: {} after {} attempts".format(url, max_attempts))
        else: # try again
            retry_count += 1
            os.remove(path)
            r = requests.get(url, stream=True)

    if old_permissions is not None:
        os.chmod(path, old_permissions)
    logging.info("Downloaded: {}".format(path))

def get_update_list(launcher_game_id, root_path=None):
    platformDir = platformToDir[platform.system()]

    # We use the update list as a dictionary so newer paths overwrite older ones
    # This would allow games to overwrite default launcher files
    # In a way it works similar to how Spring mutators work
    update_list = {}
    existing_list = {}

    if root_path is None:
        root_path = os.getcwd()

    res = try_get("files/")
    manifest = res.json()

    def _resolve_file(path, download_url, checksum):
        item = {
            "server_path": download_url,
            "local_path": path,
            "checksum": checksum,
        }
        if os.path.exists(path):
            local_checksum = calc_file_checksum(path)
            if checksum != local_checksum:
                update_list[path] = item
            else:
                if path in existing_list:
                    del existing_list[path]
                existing_list[path] = item
        else:
            update_list[path] = item

    for file, keys in manifest["spring-launcher-dist"].items():
        checksum = keys["checksum"]
        parts = file.split("/")
        if parts[0] != platformDir:
            continue

        path = os.sep.join(parts[1:])

        download_url = "spring-launcher-dist/" + file
        _resolve_file(path, download_url, checksum)

    res = try_get("files/{}".format(launcher_game_id))
    if res.status_code == requests.codes.ok:
        manifest = res.json()
        top_key = list(manifest.keys())[0]
        for path, keys in manifest[top_key].items():
            download_url = keys["path"]
            checksum = keys["checksum"]

            _resolve_file(path, download_url, checksum)
    update_list = list(update_list.values())

    if len(update_list) == 0:
        return update_list, existing_list

    m = mirrors[0]
    urls = [urljoin(m, "download?path=" + up["server_path"]) for up in update_list]

    # Get all sizes in parallel, so it doesn't fetch them forever
    def get_size(url):
        return int(requests.head(url, stream=True).headers.get("Content-length"))
    with ThreadPoolExecutor(max_workers=50) as pool:
        sizes = list(pool.map(get_size, urls))

    for i, size in enumerate(sizes):
        update_list[i]["size"] = size

    return update_list, existing_list
