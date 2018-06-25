import unittest
import os
import shutil

import requests

import spring_launcher
from spring_launcher import auto_update
from spring_launcher import githash

TEST_DIR = os.path.join(os.getcwd(), "test_dir")

class TestAutoDownload(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        os.makedirs(TEST_DIR)

    def tearDown(self):
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    def test_simple_download(self):
        res = auto_update.try_get("files")
        self.assertEqual(res.status_code, requests.codes.ok)

    def test_update_list(self):
        # Check if we get a list of updates for SpringBoard
        update_list, existing_list = auto_update.get_update_list(
            "sb", root_path=TEST_DIR)
        # there should be a list of files to download
        self.assertTrue(update_list)
        # using an emtpy dir so there should be no existing files
        self.assertFalse(existing_list)

        # See if download properly gets us all the files
        auto_update.download_files(update_list, root_path=TEST_DIR)
        to_download = map((lambda item: item["local_path"]), update_list)

        root_part = os.path.join(TEST_DIR, "") # appends a trailing slash if it's missing
        downloaded = []
        for dir_path, _, fnames in os.walk(TEST_DIR):
            dir_path = dir_path[len(root_part):]
            for fname in fnames:
                downloaded.append(os.path.join(dir_path, fname))

        downloaded = sorted(downloaded)
        to_download = sorted(to_download)

        self.maxDiff = None
        self.assertEquals(to_download, downloaded)

        # Verify if the downloaded file checksum matches online checksum
        to_dl_checksums = dict((item["local_path"], item["checksum"]) for item in update_list)

        dl_checksums = {}
        for dir_path, _, fnames in os.walk(TEST_DIR):
            rel_dir_path = dir_path[len(root_part):]
            for fname in fnames:
                rel_path = os.path.join(rel_dir_path, fname)
                path = os.path.join(dir_path, fname)
                dl_checksums[rel_path] = githash.calc_file_checksum(path)

        self.assertEquals(sorted(to_dl_checksums.items()),
                          sorted(dl_checksums.items()))
