# -*- coding: utf-8 -*-


import ctypes
import os
from os.path import exists
import shutil
import sys
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

# 自作モジュール
import frames.install_dir as instdir
import frames.enc_select as encsel
import frames.progress as prog
import modules.download_progress as dlprog
import modules.install_progress as instprog
import libs.install_config as instconf
import libs.utils


# アプリバージョン
APP_VERSION = "0.1.4"

# ウィジェットのインスタンス格納変数
install_pre_widget = None
encoder_sel_widget = None

# フレームのインスタンス格納変数
preparation_frame = None
progress_frame = None

# ボタンのインスタンス格納変数
install_button = None
cancel_button = None

def create_main_frame(main_window):
    """メインウィンドウ用のフレーム
    Parameters
    ----------
    main_window : TK
        メインウィンドウ
    """
    main_frame = tk.Frame(main_window, bg="white")
    main_frame.pack(fill="both", expand=1)

    create_install_preparation_frame(frame=main_frame)
    create_install_progress_frame(frame=main_frame)
    progress_frame.pack_forget()

    create_buttons_version_frame(frame=main_frame)

def create_install_preparation_frame(frame, bg="white"):
    """インストール準備用フレーム
    Parameters
    ----------
    frame : Frame
        表示する親フレーム
    bg : RGB or string
        背景色
    """
    global preparation_frame
    preparation_frame = tk.Frame(frame, bg=bg)
    preparation_frame.pack(fill="both")

    # インストール先選択
    global install_pre_widget
    install_pre_widget = instdir.InstallDirWidget(preparation_frame, install_init_dir="{0}\\".format(os.getcwd()), bg=bg)
    # エンコーダ選択
    global encoder_sel_widget
    encoder_sel_widget = encsel.EncoderSelectWidget(preparation_frame, bg=bg)

def create_install_progress_frame(frame, bg="white"):
    """インストール実行用フレーム
    Parameters
    ----------
    frame : Frame
        表示する親フレーム
    bg : RGB or string
        背景色
    """
    global progress_frame
    progress_frame = tk.Frame(frame, bg=bg)
    progress_frame.pack(fill="both")

    global install_progress_widget
    install_progress_widget = prog.InstallProgressWidget(progress_frame, bg=bg)

def create_buttons_version_frame(frame, bg="white"):
    """インストール/キャンセルボタン、バージョンラベルの生成
    Parameters
    ----------
    frame : Frame
        表示する親フレーム
    bg : RGB or string
        背景色
    """
    button_status_list = [["キャンセル"  ,  cancel_button_command   ],
                          ["インストール",  install_button_command  ]]
    buttons_frame = tk.Frame(frame, width=200, bg=bg)
    buttons_frame.pack(anchor="e", side="bottom", fill="x")
    button_style = ttk.Style()
    button_style.configure("BTsFrame.TButton", background=bg)

    version_label = tk.Label(buttons_frame, text="ver. {0}".format(APP_VERSION), bg=bg)
    version_label.pack(anchor="w", side="left", padx=4)

    global install_button
    global cancel_button
    install_button = ttk.Button(buttons_frame, text="インストール", style="BTsFrame.TButton", command=install_button_command)
    cancel_button = ttk.Button(buttons_frame, text="キャンセル", style="BTsFrame.TButton", command=cancel_button_command)
    cancel_button.pack(anchor="e", side="right", padx=4, pady=4)
    install_button.pack(anchor="e", side="right", padx=4, pady=4)

def install_button_command():
    """インストールに遷移する
    ここでインストール可能かのチェックを行う
    また、インストールに必要なパラメータを設定する
    """
    instconf.install_dir_reflection(install_pre_widget.get_install_path())
    if instconf.install_dir == "":
        messagebox.showinfo(title="確認", message="インストール先を選択してください")
        return

    # インストール可能かチェック
    access_message = None
    try:
        os.mkdir("{0}\\aviutl_install_test_dir".format(instconf.install_dir))
    except FileNotFoundError:
        access_message = "インストール先のディレクトリが存在しません\n{0}".format(instconf.install_dir)
    except PermissionError:
        print("out")
        access_message = "インストール先に書き込み権限がありません\n{0}".format(instconf.install_dir)
    except Exception as e:
        access_message = str(e)
    finally:
        if os.path.exists("{0}\\aviutl_install_test_dir".format(instconf.install_dir)):
            os.rmdir("{0}\\aviutl_install_test_dir".format(instconf.install_dir))

    if os.path.exists(instconf.aviutl_dir):
        access_message = "すでにAviUtlディレクトリが存在してします"

    if access_message:
        messagebox.showerror(title="エラー", message=access_message)
        return

    # 各ウィジェットの設定をinstconfに反映
    instconf.backup_enable = install_pre_widget.get_keep_dl_file()
    instconf.install_encoder_reflection(encoder_sel_widget.get_enc_type_list())

    if messagebox.askquestion(title="確認", message="{0}\nにインストールを開始しますか？".format(instconf.install_dir)) == "yes":
        global install_button, cancel_button
        makedirs()
        install_button.configure(state="disabled")
        preparation_frame.pack_forget()
        progress_frame.pack(fill="both")

        # ダウンロード処理
        result = dlprog.download_start(install_progress_widget, instconf.download_list)
        if not result == 0:
            if not result == 1:
                messagebox.showerror(title="エラー", message="ファイルダウンロードでエラー")
            cleanup(error = True)
            sys.exit()

        # インストール処理
        result = instprog.install_start(install_progress_widget, instconf.download_list)
        if not result == 0:
            if not result == 1:
                messagebox.showerror(title="エラー", message="インストールに失敗しました")
            cleanup(error = True)
            sys.exit()

        if instconf.backup_enable:
            for f in instconf.download_list:
                # download_listからダウンロードしたファイルを抽出する
                if (f.download_file_type == instconf.DownloadFileType.TOOL) or ((not f.dl_enable) and (not f.result)):
                    continue
                check_file = "{0}\\{1}".format(instconf.backup_dir, f.file_name)
                if exists(check_file):
                    os.remove(check_file)
                shutil.move("{0}\\{1}".format(instconf.dl_temp_dir, f.file_name), check_file)
        cleanup()
        messagebox.showinfo(title="情報", message="インストールが完了しました")
        libs.utils.run_aviutl("{0}\\aviutl.exe".format(instconf.aviutl_dir))
        sys.exit()

def makedirs():
    try:
        os.mkdir(instconf.aviutl_dir)
        os.mkdir(instconf.dl_temp_dir)
        if not exists(instconf.sv_dir):
            os.makedirs(instconf.sv_dir)
        os.makedirs(instconf.script_dir)
        os.mkdir(instconf.figure_dir)
        if (instconf.backup_enable) and (not exists(instconf.backup_dir)):
            os.mkdir(instconf.backup_dir)

    except Exception as e:
        access_message = str(e)

def cleanup(error = False):
    if error:
        shutil.rmtree(instconf.aviutl_dir)
    else:
        shutil.rmtree(instconf.dl_temp_dir)
    shutil.rmtree(instconf.sv_dir)

def cancel_button_command():
    """キャンセルボタン
    """
    close_event()

def close_event():
    """終了イベント
    """
    if messagebox.askquestion(title="終了", message="インストールをキャンセルしますか？") == "yes":
        dlprog.download_stop()
        instprog.install_stop()
        sys.exit()

def main():
    root = tk.Tk()
    root.title("AviUtl Auto Installer")
    screen_width = root.winfo_screenwidth()     # モニタの横幅取得
    screen_height = root.winfo_screenheight()   # モニタの縦幅取得
    app_width = 512     # アプリの横幅
    app_height = 300    # アプリの縦幅
    # アプリを中央に表示
    root.geometry("{0}x{1}+{2}+{3}".format(app_width, app_height, int(((screen_width / 2) - (app_width / 2))), int(((screen_height / 2) - (app_height / 2)))))
    # 終了イベントを登録
    root.protocol("WM_DELETE_WINDOW", close_event)
    # ウィンドウサイズ固定
    root.resizable(0, 0)

    # アイコンの埋め込み
    ico_data = """iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEBklEQVR4nO2bS2gU
    dxzHP/+4boymm4ctIULBHmJaBR8H6UV7aUUxEPASGkx6sIciFMFLT2qR6sXHQW/F
    By1iPbQIHlTwgaD0oAVBIVAxpGkPgaVm18Tousm6I/91kuxMZmb/89idWTMfGDKv
    /39+v+/8f7//YzbExMTExMQsXoSd55qmRUoUIYS0Sdq7DEgBrUATkHBTjb7NAC+A
    tJvCoSOEaNE0bQJo1oWQIjS6sEv6m5TvF3gu/9aVAEC3EEI6cLf8pGytsoXYYXVd
    07ReYEW9CbABWEVZiDo5bsZU5g3Q0FB9mwOlNcDKclKTehMgSGQiLNZbCNjitdeq
    WwHMsV8pCdrdU7chIJ1y+9atyizmHFCitiFwMu109VPgC72rWwN0Ah/pA50Wp1Gr
    H8LOAXJEtxfYowtQc8IUYAdwbnZg4xaLkV3FGqySYFgC7AZ+BZZ4rcCc2VV6Aave
    IAwBNgHnbZwfAa4B94Fh4H9gUp+5VQWnxCInHceBAaA9qIff+u53vuzaajj39NkI
    +68c4trft5W7tvK3qToZMpWRRkw4tYBjwD4laxT5rKNrgfN/jj5gx5l+pvIvg3yU
    Mk4CDAb9sN612w3Hr2ZyDP72vSfn3cwCnco4CTDX7Jckk2w7epz1Xw/Q1OY9Gvpu
    TMDI67njoY0r+ea/f5XLn85Btgh0iAUJTSV0PCfBbUeO8fle/9HQPlEwHA9/nPRd
    5ywqvYAVSkPh9f3BRENzrmg4zrR47gWDIA8UlATw0+zLSRSMb+LFcncCfBjsYDgj
    01BNJ0PJGaMA00l3Hn1Sppds8m4ToanMGBW6Qd/03Jtk81DOtppDP89Pjv5a18TV
    rSnHR0oB2hogmzYKaRLisJXjJoaFEClN08arKsD1LSlSL4t0j+Yd73uyurF0byXa
    BPQ1wj9v3m3PdB2yxnKvKlQjR5XjskGWWoTDjXMy/zjl/SNJsqDx7eUMHZmC5fV0
    e4Jzu9qZXuo9wA83G8q6qqjqOWA6IbjY08rkioUJT56T1/w475eaJMFZR2cS847K
    /Ys7rYXxw+yyl+pWs15ANvU/vmqhKChtcj+9Mvw12ZpaMJ/stNJ+FKj5K5DdXZRY
    9KvCsQARsCFUYgEiYEOoxAJEwIZQiQVQuSmXzVTfEo/4tU1JgMeXLlTPA588/OWs
    rwqUhsI3D/wgl1XY0D/Ista26nulwOvnWR5dusCdnw76qkdpQaSe0H9NqoxTCEQ3
    8O1xbbOTANENfHv8JQQT8rPNKV1VLeJbRrc16XZFqJqM+RBtzKtdgS2JKah2VP+8
    ZOdEpw9xOx3qzevPDuSNevp/Af1DQ14PkzCYAj4Iogn7GQqfkKveITgvf+N7OoTn
    xsTExMTEvFcAbwGywfEKvFtf1gAAAABJRU5ErkJggg==
    """
    root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(data=ico_data))

    create_main_frame(root)

    # 管理者権限実行チェック
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if not is_admin == 0:
        messagebox.showerror(title="エラー", message="管理者権限では実行できません")
        sys.exit()

    root.mainloop()


if __name__ == '__main__':
    main()

