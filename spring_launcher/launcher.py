#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--temp")
parser.add_argument("--current")

def main():
    FORMAT = '%(asctime)s %(levelname)s:%(message)s'
    logging.basicConfig(filename='launcher.log', level=logging.INFO, filemode='w', format=FORMAT)
    logging.info("Started logging...")

    args = parser.parse_args()
    if args.temp and args.current:
        TEMP_DIR = args.temp
        CURR_DIR = args.current

        logging.info("Step 5. Delete files in current")
        import os
        import shutil
        for file_name in os.listdir(CURR_DIR):
            file_path = os.path.join(CURR_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        logging.info("Step 6. Move Temp Path files to current")
        for file_name in os.listdir(TEMP_DIR):
            src_path = os.path.join(TEMP_DIR, file_name)
            dst_path = os.path.join(CURR_DIR, file_name)
            shutil.move(src_path, dst_path)

        executable = os.path.join(CURR_DIR, sys.argv[0])
        #os.execl(executable, executable, os.path.basename(executable))
        import psutil
        try:
            p = psutil.Process(os.getpid())
            for handler in p.get_open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            logging.error(e)
        os.execl(executable, executable)
        # 7. Launch current/launcher and resume normal operations

    import gui
    gui.start()

if __name__ == '__main__':
    main()
