# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import frames.install_dir as instdir
import frames.enc_select as encsel
import frames.install_progress as instprog

install_pre_widget = None
encoder_sel_widget = None

preparation_frame = None
progress_frame = None

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

    create_buttons_frame(frame=main_frame)

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
    install_progress_widget = instprog.InstallProgressWidget(progress_frame, bg=bg)

def create_buttons_frame(frame, bg="white"):
    """インストール/キャンセルボタンの生成
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
    buttons_frame.pack(anchor="e", side="bottom")
    button_style = ttk.Style()
    button_style.configure("BTsFrame.TButton", background=bg)

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
    inst_dir = install_pre_widget.get_install_path()
    if inst_dir == "":
        messagebox.showinfo(title="確認", message="インストール先を選択してください")
        return

    # インストール可能かチェック
    access_message = None
    try:
        os.mkdir("{0}AviUtl".format(inst_dir))
    except FileExistsError:
        access_message = "すでにAviUtlディレクトリが存在してします"
    except FileNotFoundError:
        access_message = "インストール先のディレクトリが存在しません\n{0}".format(inst_dir)
    except PermissionError:
        access_message = "インストール先に書き込み権限がありません\n{0}".format(inst_dir)
    except Exception as e:
        access_message = str(e)

    if access_message:
        messagebox.showerror(title="エラー", message=access_message)
        return

    if messagebox.askquestion(title="確認", message="{0}AviUtl\nにインストールを開始しますか？".format(inst_dir)) == "yes":
        global install_button
        install_button.configure(state="disabled")
        preparation_frame.pack_forget()
        progress_frame.pack(fill="both")
    else:
        os.rmdir("{0}AviUtl".format(inst_dir))

def cancel_button_command():
    """キャンセルボタン
    """
    close_event()

def close_event():
    """終了イベント
    """
    if messagebox.askquestion(title="終了", message="インストールをキャンセルしますか？") == "yes":
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

    create_main_frame(root)

    root.mainloop()


if __name__ == '__main__':
    main()

