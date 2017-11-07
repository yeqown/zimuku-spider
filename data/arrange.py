"""
    choose some file into differrent folder and do special shell
    # Author: yeqiang 
    # Date: 2017-10-26
"""

import glob
import os
import fnmatch
import shutil
import sys
import os.path as path

include_file_perfix = ["*.rar", "*.zip", "*.srt"]

rar_folder = path.abspath("./rar")
zip_folder = path.abspath("./zip")
srt_folder = path.abspath("./srt")

curdir = path.curdir


def check_mkdir():
    if not path.exists(rar_folder):
        os.mkdir(rar_folder)
    if not path.exists(zip_folder):
        os.mkdir(zip_folder)
    if not path.exists(srt_folder):
        os.mkdir(srt_folder)


def move_file(file_or_files, new_dir):
    if isinstance(file_or_files, list):
        for file in file_or_files:
            filename = file.split('/')[-1]
            shutil.move(file, path.join(new_dir, filename))
    else:
        shutil.move(file_or_files, path.join(new_dir, file_or_files))


def scan(in_path):
    zip_files = []
    rar_files = []
    srt_files = []

    for dirpath, dirname, filenames in os.walk(in_path):
        for filename in fnmatch.filter(filenames, "*.zip"):
            zip_files.append(path.join(dirpath, filename))

        for filename in fnmatch.filter(filenames, "*.rar"):
            rar_files.append(path.join(dirpath, filename))

        for filename in fnmatch.filter(filenames, "*.srt"):
            srt_files.append(path.join(dirpath, filename))

    move_file(zip_files, path.join(curdir, "zip/"))
    print("Move zip files [{}]".format(len(zip_files)))
    move_file(rar_files, path.join(curdir, "rar/"))
    print("Move rar files [{}]".format(len(rar_files)))
    move_file(srt_files, path.join(curdir, "srt/"))
    print("Move srt files [{}]".format(len(srt_files)))

if __name__ == "__main__":
    check_mkdir()
    scan(in_path=path.join(curdir, "download_corpus"))
