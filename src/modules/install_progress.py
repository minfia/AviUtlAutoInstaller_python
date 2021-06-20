# -*- coding: utf-8 -*-


import glob
import subprocess
import shutil
import os
from os.path import basename
from os.path import exists
from os.path import splitext
from os.path import isdir
import libs.inifile_config as iniconf
import libs.install_config as instconf
import libs.utils


# ローカル変数
__sv_cmd = ""
__install_stop = False

def install_start(progress_instance, download_file_list):
    """インストール開始・表示の更新を行う
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
        -1  : 失敗
    """
    result = 0
    process_max = 0
    process_complete_count = 0
    progress_instance.set_determinate()
    for item in download_file_list:
        if (item.dl_enable) and (item.result) and (not item.download_file_type == instconf.DownloadFileType.TOOL):
            process_max += 1
    result = __extract_7zip()
    if not result == 0:
        return -1
    progress_instance.setup_progress("unzip... ", process_max)

    for item in download_file_list:
        if __install_stop:
            return 1
        if (not item.dl_enable) or (item.download_file_type == instconf.DownloadFileType.TOOL):
            continue
        result = __unzip_file(item)
        if not result == 0:
            return -1
        process_complete_count += 1
        progress_instance.update_progress(process_complete_count)

    # AviUtlの設定ファイルを編集(v1.10準拠)
    # 最大画像サイズ (1920x1080 -> 2560x1560)
    # キャッシュサイズ (256 -> 512)
    # 再生ウィンドウをメインウィンドウに表示する (無効 -> 有効)
    # 編集ファイルが閉じられるときに確認ダイアログを表示する (無効 -> 有効)
    # 拡張編集の設定 (無効 -> 有効)
    param_list = ["width=2560", "height=1560", "frame=320000", "sharecache=512",\
                  "moveA=5", "moveB=30", "moveC=899", "moveD=8991", "saveunitsize=4096", "compprofile=1", "plugincache=1",\
                  "startframe=1", "shiftselect=1", "yuy2mode=0", "movieplaymain=1", "vfplugin=1", "yuy2limit=0", "editresume=0", "fpsnoconvert=0",\
                  "tempconfig=0", "load30fps=0", "loadfpsadjust=0", "overwritecheck=0", "dragdropdialog=0", "openprojectaup=1", "closedialog=1",\
                  "projectonfig=0", "windowsnap=0", "dragdropactive=1", "trackbarclick=1", "defaultsavefile=%p", "finishsound=",\
                  "resizelist=1920x1080,1280x720,640x480,352x240,320x240",\
                  "fpslist=*,30000/1001,24000/1001,60000/1001,60,50,30,25,24,20,15,12,10,8,6,5,4,3,2,1",\
                  "sse=1", "sse2=1"]
    iniconf.add_param("{0}\\aviutl.ini".format(instconf.aviutl_dir), "[system]", param_list)
    iniconf.update_param("{0}\\aviutl.ini".format(instconf.aviutl_dir), "[拡張編集]", "disp", 1)

    return result

def __extract_7zip():
    """7zipの展開
    Returns
    -------
        0   : 成功
        -1  : 失敗
    """
    msi_path = "{0}\\7z.msi".format(instconf.dl_temp_dir)
    target_path = "targetdir={0}".format(instconf.sv_dir)
    print("msi_path: {0}".format(msi_path))
    print("target_path: {0}".format(target_path))
    proc = subprocess.run(["msiexec.exe", "/a", msi_path, target_path, "/qn"])
    result = proc.returncode
    global __sv_cmd
    __sv_cmd = "{0}\\Files\\7-Zip\\7z.exe".format(instconf.sv_dir)

    return result

def __unzip_file(item):
    """圧縮ファイルを展開し、所定の場所に配置する
    Parameters
    ----------
    item : list
        DownloadFileのリスト
    Returns
    -------
        0   : 成功
        -1  : 失敗
    """
    # ファイルの解凍
    unzip_path = ""
    unzip_file_path = ""
    if item.download_file_type == instconf.DownloadFileType.MAIN:
        unzip_path = "{0}".format(instconf.aviutl_dir)
    elif (item.download_file_type == instconf.DownloadFileType.PLUGIN) or (item.download_file_type == instconf.DownloadFileType.SCRIPT):
        unzip_path = "{0}\\{1}".format(instconf.dl_temp_dir, splitext(item.file_name)[0])
    elif item.download_file_type == instconf.DownloadFileType.ENCODER:
        unzip_path = "{0}".format(libs.utils.get_user_temp_dir())

    unzip_file_path = "{0}\\{1}".format(instconf.dl_temp_dir, item.file_name)
    global __sv_cmd
    proc = subprocess.run([__sv_cmd, "x", unzip_file_path, "-aoa", "-o{0}".format(unzip_path)])
    result = proc.returncode

    if not result == 0:
        return -1

    # 解凍したファイルをタイプ分けして所定の場所に配置
    if item.download_file_type == instconf.DownloadFileType.MAIN:
        # AviUtl本体
        libs.utils.run_aviutl("{0}\\aviutl.exe".format(instconf.aviutl_dir), True)
    elif item.download_file_type == instconf.DownloadFileType.PLUGIN or item.download_file_type == instconf.DownloadFileType.SCRIPT:
        # プラグイン/スクリプト
        if "psdtoolkit" in item.file_name:
            __psdtoolkit_install(unzip_path)
            return 0
        install_dir_path = ""
        for file_type in item.install_file:
            file_path = "{0}\\**\\{1}".format(unzip_path, file_type)
            file_list = glob.glob(file_path, recursive=True)
            for f in file_list:
                if item.download_file_type == instconf.DownloadFileType.PLUGIN:
                    # プラグインのインストール
                    install_dir_path = instconf.plugins_dir
                else:
                    # スクリプトのインストール
                    script_collect_dir = "{0}\\{1}".format(instconf.script_dir, item.script_collect_dir_name)
                    if (not item.script_collect_dir_name == "") and (not isdir(script_collect_dir)):
                        # スクリプトを個別にまとめるディレクトリがない場合は作る
                        os.mkdir(script_collect_dir)
                    script_dir = instconf.script_dir if item.script_collect_dir_name == "" else script_collect_dir
                    install_dir_path = script_dir

                # 既にファイルが存在しているか確認
                check_file = "{0}\\{1}".format(install_dir_path, basename(f))
                if exists(check_file):
                    # 存在しているので一度削除
                    os.remove(check_file)
                shutil.move(f, install_dir_path)
    elif item.download_file_type == instconf.DownloadFileType.ENCODER:
        # エンコーダ
        encoder_dir = "{0}\\{1}".format(unzip_path, splitext(item.file_name)[0])
        if "x264gui" in item.file_name:
            encoder_dir = encoder_dir[:len(encoder_dir)-5]
        proc = subprocess.run(["{0}\\auo_setup.exe".format(encoder_dir), "-autorun", "-nogui", "-dir", instconf.aviutl_dir])
        shutil.rmtree(encoder_dir)
        result = proc.returncode

        if not result == 0:
            return -1

    return result

def __psdtoolkit_install(unzip_path):
    # ドキュメント関連の移動
    psddocs_dir = "{0}\\PSDToolKitの説明ファイル群".format(instconf.aviutl_dir)
    if isdir(psddocs_dir):
        shutil.rmtree(psddocs_dir)
    os.mkdir(psddocs_dir)
    shutil.move("{0}\\PSDToolKitDocs".format(unzip_path), psddocs_dir)
    shutil.move("{0}\\PSDToolKit説明書.html".format(unzip_path), psddocs_dir)
    file_list = glob.glob("{0}\\*.txt".format(unzip_path))
    for f in file_list:
        shutil.move(f, psddocs_dir)

    # プラグイン/スクリプトの移動
    install_list = os.listdir(unzip_path)
    install_list = glob.glob("{0}\\**\\*.*".format(unzip_path), recursive=True)
    for f in install_list:
        dst_file_path = "{0}".format(f.replace(unzip_path, instconf.plugins_dir))
        dst_dir_path = "{0}".format(dst_file_path.replace(basename(dst_file_path), ""))
        if exists(dst_file_path):
            # ファイルがある場合は、一度削除する
            os.remove(dst_file_path)
        if not exists(dst_dir_path):
            os.makedirs(dst_dir_path)
        shutil.move(f, "{0}".format(f.replace(unzip_path, instconf.plugins_dir)))

def install_stop():
    """インストールを停止する
    """
    __install_stop = True

def main():
    pass

if __name__ == '__main__':
    main()

