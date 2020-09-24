# -*- coding: utf-8 -*-


import dataclasses
from enum import auto
from enum import Enum


# ダウンロードファイルタイプ
class DownloadFileType(Enum):
    TOOL = auto()
    MAIN = auto()
    PLUGIN = auto()
    SCRIPT = auto()
    ENCODER = auto()

# ダウンロードファイルに関するクラス
@dataclasses.dataclass
class DownloadFile:
    download_file_type: DownloadFileType
    file_name: str
    url: str
    priority: int = 1
    dl_enable: bool = False
    result: bool = False
    install_file: list = None
    script_collect_dir_name: str = ""

# インストール先ルートディレクトリパス
install_dir = ""
# AviUtlのディレクトリパス
aviutl_dir = "AviUtl"
# ダウンロードファイルの一時ディレクトリパス
dl_temp_dir = "{0}\\DL_TEMP".format(aviutl_dir)
# 7z展開先ディレクトリパス
sv_dir = "C:\\AviUtlAutoInstaller_7z"
# プラグインディレクトリパス
plugins_dir = "{0}\\plugins".format(aviutl_dir)
# スクリプトディレクトリパス
script_dir = "{0}\\script".format(plugins_dir)
# 画像ディレクトリパス
figure_dir = "{0}\\figure".format(plugins_dir)
# バックアップディレクトリパス
backup_dir = "{0}\\backup_files".format(aviutl_dir)
# ダウンロードファイルのバックアップの有効化
backup_enable = False
# ダウンロードするファイルリスト
download_list = []


download_list.append(DownloadFile(download_file_type=DownloadFileType.TOOL ,dl_enable=True, file_name="7z.msi", url="https://ja.osdn.net/frs/redir.php?m=jaist&f=sevenzip%2F70468%2F7z1806.msi", priority=0))
download_list.append(DownloadFile(download_file_type=DownloadFileType.MAIN, dl_enable=True, file_name="aviutl110.zip", url="http://spring-fragrance.mints.ne.jp/aviutl/aviutl110.zip", priority=0))
download_list.append(DownloadFile(download_file_type=DownloadFileType.PLUGIN, dl_enable=True, file_name="exedit92.zip", url="http://spring-fragrance.mints.ne.jp/aviutl/exedit92.zip", priority=0, install_file=["exedit*.*", "lua*.*"]))


# 追加プラグイン&スクリプト
download_list.append(DownloadFile(download_file_type=DownloadFileType.PLUGIN, dl_enable=True, file_name="L-SMASH_Works_r940_plugins.zip", url="https://pop.4-bit.jp/bin/l-smash/L-SMASH_Works_r940_plugins.zip", install_file=["*.au*"]))
download_list.append(DownloadFile(download_file_type=DownloadFileType.PLUGIN, dl_enable=True, file_name="auls_outputpng.zip", url="http://auls.client.jp/plugin/auls_outputpng.zip", install_file=["*.auf"]))
download_list.append(DownloadFile(download_file_type=DownloadFileType.PLUGIN, dl_enable=True, file_name="psdtoolkit_v0.2beta48.zip", url="https://github.com/oov/aviutl_psdtoolkit/releases/download/v0.2beta48/psdtoolkit_v0.2beta48.zip"))
download_list.append(DownloadFile(download_file_type=DownloadFileType.SCRIPT, dl_enable=True, file_name="WindShk.zip", url="https://tim3.web.fc2.com/script/WindShk.zip", script_collect_dir_name="ティム氏", install_file=["*.anm"]))
download_list.append(DownloadFile(download_file_type=DownloadFileType.SCRIPT, dl_enable=True, file_name="InkV2.zip", url="https://tim3.web.fc2.com/script/InkV2.zip", script_collect_dir_name="ティム氏", install_file=["*.obj"]))
download_list.append(DownloadFile(download_file_type=DownloadFileType.SCRIPT, dl_enable=True, file_name="Framing.zip", url="https://tim3.web.fc2.com/script/Framing.zip", script_collect_dir_name="ティム氏", install_file=["*.dll", "*.anm"]))
download_list.append(DownloadFile(download_file_type=DownloadFileType.SCRIPT, dl_enable=True, file_name="ReelRot.zip", url="https://tim3.web.fc2.com/script/ReelRot.zip", script_collect_dir_name="ティム氏", install_file=["*.anm"]))
download_list.append(DownloadFile(download_file_type=DownloadFileType.SCRIPT, dl_enable=True, file_name="VanishP2_V2.zip", url="https://tim3.web.fc2.com/script/VanishP2_V2.zip", script_collect_dir_name="ティム氏", install_file=["*.anm"]))
download_list.append(DownloadFile(download_file_type=DownloadFileType.SCRIPT, dl_enable=True, file_name="LinHal.zip", url="https://tim3.web.fc2.com/script/LinHal.zip", script_collect_dir_name="ティム氏", install_file=["*.anm"]))


def install_dir_reflection(inst_dir):
    """インストールに必要なディレクトリ構成を反映する
    Parameters
    ----------
    inst_dir : string
        インストール先のルートディレクトリパス
    """
    global install_dir, aviutl_dir, dl_temp_dir, plugins_dir, script_dir, figure_dir, backup_dir
    install_dir = inst_dir
    aviutl_dir = install_dir + "\\AviUtl"
    dl_temp_dir = "{0}\\DL_TEMP".format(aviutl_dir)
    plugins_dir = "{0}\\plugins".format(aviutl_dir)
    script_dir = "{0}\\script".format(plugins_dir)
    figure_dir = "{0}\\figure".format(plugins_dir)
    backup_dir = "{0}\\backup_files".format(aviutl_dir)

def install_encoder_reflection(enc_list):
    """エンコーダの選択状態を反映する
    Parameters
    ----------
    enc_list : list
        boolのリスト
    """
    global download_list
    download_list.append(DownloadFile(download_file_type=DownloadFileType.ENCODER, dl_enable=enc_list[0], file_name="x264guiEx_2.65v2.zip", url="https://dl.dropboxusercontent.com/sh/q6afzrpcrl8nsda/AAAsdMuegINAP07jSPVDOXRka/x264guiEx_2.65v2.zip", priority=0))
    download_list.append(DownloadFile(download_file_type=DownloadFileType.ENCODER, dl_enable=enc_list[1], file_name="QSVEnc_4.07.7z", url="https://drive.google.com/uc?id=1M8G9gfRes7JhX-xGCNW9OwIbzTgXRuX6", priority=0))
    download_list.append(DownloadFile(download_file_type=DownloadFileType.ENCODER, dl_enable=enc_list[2], file_name="NVEnc_5.15.7z", url="https://drive.google.com/uc?id=1E8OZMftN6FynswbWFVHOTzfdCT47ebbT", priority=0))
    download_list.append(DownloadFile(download_file_type=DownloadFileType.ENCODER, dl_enable=enc_list[3], file_name="VCEEnc_6.04.7z", url="https://drive.google.com/uc?id=1Ab6QkSeJvVEuUvqUIHHl7JaZl-Fo5xO4", priority=0))

def main():
    pass

if __name__ == "__main__":
    main()

