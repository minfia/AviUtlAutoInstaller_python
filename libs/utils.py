# -*- coding: utf-8 -*-

from os.path import expanduser
from os.path import isdir
import glob
import subprocess
import shutil
import time

def run_aviutl(aviutl_path, kill=False):
    """AviUtlを実行する
    Parameters
    ----------
    aviutl_path : str
        AviUtlのあるフルパス
    kill : bool
        実行後、プロセスを殺す
    """
    proc = subprocess.Popen(aviutl_path, shell = False)
    if kill:
        time.sleep(3)
        proc.kill()

def get_user_temp_dir():
    return "{0}\\AppData\\Local\\Temp".format(expanduser("~"))

def main():
    pass

if __name__ == '__main__':
    main()

