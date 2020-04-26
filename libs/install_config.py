# -*- coding: utf-8 -*-

import dataclasses
import enum

# ダウンロードファイルタイプ
class DownloadFileType(enum.Enum):
    TOOL = enum.auto()
    MAIN = enum.auto()
    SCRIPT = enum.auto()
    PLUGIN = enum.auto()

# ダウンロードファイルに関するクラス
@dataclasses.dataclass
class DownloadFile:
    download_file_type: DownloadFileType
    file_name: str
    url: str
    priority: int = 1
    dl_enable: bool = False
    result: bool = False

# インストール先ルートディレクトリパス
install_dir = ""
# AviUtlのディレクトリパス
aviutl_dir = "AviUtl"
# ダウンロードファイルの一時ディレクトリパス
dl_temp_dir = "{0}DL_TEMP".format(aviutl_dir)
# ダウンロードファイルのバックアップの有効化
backup_enable = False
# ダウンロードするファイルリスト
download_list = []


download_list.append(DownloadFile(download_file_type = DownloadFileType.TOOL ,dl_enable = True, file_name = "7z.msi", url = "https://ja.osdn.net/frs/redir.php?m=jaist&f=sevenzip%2F70468%2F7z1806.msi", priority = 0))
download_list.append(DownloadFile(download_file_type = DownloadFileType.MAIN, dl_enable = True, file_name = "aviutl110.zip", url = "http://spring-fragrance.mints.ne.jp/aviutl/aviutl110.zip", priority = 0))
download_list.append(DownloadFile(download_file_type = DownloadFileType.PLUGIN, dl_enable = True, file_name = "exedit92.zip", url = "http://spring-fragrance.mints.ne.jp/aviutl/exedit92.zip", priority = 0))
download_list.append(DownloadFile(download_file_type = DownloadFileType.PLUGIN, dl_enable = True, file_name = "L-SMASH_Works_r940_plugins.zip", url = "https://pop.4-bit.jp/bin/l-smash/L-SMASH_Works_r940_plugins.zip"))

def install_dir_reflection(inst_dir):
    """インストールに必要なディレクトリ構成を反映する
    Parameters
    ----------
    inst_dir : string
        インストール先のルートディレクトリパス
    """
    global install_dir, aviutl_dir, dl_temp_dir
    install_dir = inst_dir
    aviutl_dir = install_dir + "\\AviUtl"
    dl_temp_dir = "{0}\\DL_TEMP".format(aviutl_dir)

def install_encoder_reflection(enc_list):
    """エンコーダの選択状態を反映する
    Parameters
    ----------
    enc_list : list
        boolのリスト
    """
    global download_list
    download_list.append(DownloadFile(download_file_type = DownloadFileType.PLUGIN, dl_enable = enc_list[0], file_name = "x264guiEx_2.64v3.7z", url = "https://drive.google.com/uc?id=15IoL3jw1J8QHkoGQvq1Jy7qkujDBZ80E", priority = 0))
    download_list.append(DownloadFile(download_file_type = DownloadFileType.PLUGIN, dl_enable = enc_list[1], file_name = "QSVEnc_4.00.7z", url = "https://drive.google.com/uc?id=1SNdOcaCXazkdgdeLas-dzF9Rb8oNGjjW", priority = 0))
    download_list.append(DownloadFile(download_file_type = DownloadFileType.PLUGIN, dl_enable = enc_list[2], file_name = "NVEnc_4.69.7z", url = "https://drive.google.com/uc?id=1iTXWXqYr1uDdJC6Va6DPCgUoRZfcARJY", priority = 0))
    download_list.append(DownloadFile(download_file_type = DownloadFileType.PLUGIN, dl_enable = enc_list[3], file_name = "VCEEnc_5.04.7z", url = "https://drive.google.com/uc?id=1_hb6NLYeymc8_o-zIOlh80Ldbr_Nih4j", priority = 0))

def main():
    pass

if __name__ == "__main__":
    main()

