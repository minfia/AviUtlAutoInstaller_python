# -*- coding: utf-8 -*-

# import os
from concurrent.futures import ThreadPoolExecutor
import libs.file_download as dl
import libs.install_config as instconf

# ローカル変数
__downloader = None
__MAX_RETRY = 3

def download_start(progress_instance, download_file_list):
    """ダウンロード開始・表示の更新を行う
    Parameters
    ----------
    progress_instance : InstallProgressWidget
        InstallProgressWidgetのインスタンス
    download_file_list : list
        DownloadFileクラスのリスト
    Returns
    -------
        0   : 成功
        1   : 停止
        -1  : ダウンロード異常
    """
    result = 0
    global __downloader
    __downloader = dl.FileDownload()
    thread_pool = ThreadPoolExecutor()
    for item in download_file_list:
        if not item.dl_enable:
            continue
        for retry_count in range(-1, __MAX_RETRY, 1):
            future = thread_pool.submit(__downloader.download, item.url, instconf.dl_temp_dir, item.file_name)
            while (__downloader.download_file_size == 0) and (__downloader.get_download_status() != dl.DownloadStatus.ERROR):
                pass
            if (__downloader.get_download_status() == dl.DownloadStatus.ERROR):
                dl_result = future.result()
                continue
            progress_instance.setup_progress(item.file_name, __downloader.download_file_size)
            while (future.running()):
                progress_instance.set_filesize(__downloader.download_file_size)
                progress_instance.update_progress(__downloader.download_complete_size)
            dl_result = future.result()
            if dl_result >= 0:
                if dl_result == 0:
                    item.result = True
                break
        if dl_result == 1:
            result = 1
            break
        if (item.priority == 0) and (item.result == False):
            result = -1
            break
    thread_pool.shutdown()

    return result

def download_stop():
    """ダウンロード停止
    """
    global __downloader
    if not __downloader == None:
        __downloader.download_stop()

if __name__ == '__main__':
    main()

