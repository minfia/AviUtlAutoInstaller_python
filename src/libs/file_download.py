# -*- coding: utf-8 -*-


import os
from enum import auto
from enum import Enum
import urllib.request


class DownloadStatus(Enum):
    NONE = auto()
    CONNECT = auto()
    CONNECTING = auto()
    FINISH = auto()
    ERROR = auto()

class FileDownload:
    def __init__(self):
        self.__openter = urllib.request.build_opener()
        self.__google_flag = False
        self.__BLOCK_SIZE = 1024
        self.__download_stop = True
        self.__download_status = DownloadStatus.NONE
        self.download_file_size = 0
        self.download_complete_size = 0

    def download(self, url, directory_path, file_name):
        """ファイルダウンロード
        Parameter
        ---------
        url : string
            ダウンロードするファイルのURL
        directory_path : string
            ダウンロード先のディレクトリパス
        file_name : string
            ダウンロードするファイル名
        Returns
        -------
            0   : 成功
            1   : 停止
            -1  : HTTPError
            -2  : URLError
            -3  : ExceptionError
        """
        self.__google_flag = False
        self.download_file_size = 0
        self.download_complete_size = 0
        if "drive.google.com" in url:
            self.__google_flag = True

        try:
            self.__b = bytes()
            self.__download_status = DownloadStatus.CONNECTING
            self.__httpres = self.__openter.open(url)
            if self.__google_flag:
                self.__download_status = DownloadStatus.CONNECT
                self.download_file_size = 1
                self.__b = self.__httpres.read()
                self.download_complete_size = 1
            else:
                self.download_file_size = int(self.__httpres.getheader('Content-Length'))
                self.__download_status = DownloadStatus.CONNECT
                if self.download_file_size < self.__BLOCK_SIZE:
                    self.__download_read_block_size = self.download_file_size
                else:
                    self.__download_read_block_size = 1024
                self.__download_stop = False
                while (not self.__download_stop) and (self.download_complete_size < self.download_file_size):
                    self.__b = self.__b + self.__httpres.read(self.__download_read_block_size)
                    self.download_complete_size += self.__download_read_block_size
                    self.__diff_size = self.download_file_size - self.download_complete_size
                    if self.__diff_size < self.__download_read_block_size:
                        self.__download_read_block_size = self.__diff_size
                if self.__download_stop:
                    self.__download_status = DownloadStatus.NONE
                    return 1
            with open("{0}/{1}".format(directory_path, file_name), "wb") as self.__fpw:
                self.__fpw.write(self.__b)
            self.__download_status = DownloadStatus.FINISH
            return 0
        except urllib.error.HTTPError as e:
            self.__download_status = DownloadStatus.ERROR
#            print("HTTP: {0}".format(e))
            return -1
        except urllib.error.URLError as e:
            self.__download_status = DownloadStatus.ERROR
#            print("URL: {0}".format(e))
            return -2
        except Exception as e:
            self.__download_status = DownloadStatus.ERROR
#            print("Ex: {0}".format(e))
            return -3
        finally:
            self.__openter.close()
            self.__httpres.close()


    def download_stop(self):
        self.__download_stop = True

    def get_download_status(self):
        return self.__download_status

