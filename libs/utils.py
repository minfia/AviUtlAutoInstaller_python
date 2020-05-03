# -*- coding: utf-8 -*-

from os.path import expanduser
from os.path import isdir
import glob
import subprocess
import shutil

def run_aviutl(aviutl_path, kill):
    """AviUtlを実行する
    Parameters
    ----------
    aviutl_path : str
        AviUtlのあるフルパス
    kill : bool
        実行後、プロセスを殺す
    """
    subprocess.Popen(aviutl_path, shell = False)
    if kill:
        while True:
            line = ""
            proc = subprocess.Popen("tasklist", shell = True, stdout = subprocess.PIPE)
            for proc_line in proc.stdout:
                if "aviutl.exe" in str(proc_line):
                    line = str(proc_line)
                    break
            if "aviutl.exe" in line:
                break
        subprocess.run(["taskkill", "/im", "aviutl.exe"])

def get_user_temp_dir():
    return "{0}\\AppData\\Local\\Temp".format(expanduser("~"))

def main():
    pass

if __name__ == '__main__':
    main()

