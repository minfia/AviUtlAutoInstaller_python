# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk


class InstallDirWidget(tk.Frame):
    def __init__(self, master=None, bg="white"):
        """コンストラクタ
        各ウィジェットの生成をする
        Parameters
        ----------
        bg : RGB or string
        """
        super().__init__(master)
        self.widget_frame = self
        self.widget_frame.configure(bg=bg, relief="raised", height=0)
        self.widget_frame.pack(anchor="nw", fill="x", pady=8)
        self.install_dir = tk.StringVar()
        self.cb_boolean = tk.BooleanVar()
        self.create_label(frame=self.widget_frame, row=1, column=1, bg=bg)
        self.create_install_dir_entry(frame=self.widget_frame, row=2, column=1)
        self.create_dialog_button(frame=self.widget_frame, row=2, column=2, bg=bg)
        self.create_remove_checkbutton(frame=self.widget_frame, row=3, column=1, bg=bg)

    def create_label(self, frame, row, column, bg):
        """ラベル生成
        Parameters
        ----------
        frame : Frame
            表示する親フレーム
        row : int
            表示する位置
        column : int
            表示する位置
        bg : RGB or string
            背景色
        """
        self.label = tk.Label(self, text="インストール先を選択してください", bg=bg)
        self.label.grid(row=row, column=column, sticky="W", padx=4)

    def create_install_dir_entry(self, frame, row, column):
        """入力欄生成
        Parameters
        ----------
        frame : Frame
            表示する親フレーム
        row : int
            表示する位置
        column : int
            表示する位置
        """
        self.install_dir_entry = ttk.Entry(self, width=72, textvariable=self.install_dir)
        self.install_dir_entry.grid(row=row, column=column, sticky=(tk.W, tk.E), padx=4)
        self.columnconfigure(column, weight=1)

    def create_dialog_button(self, frame, row, column, bg):
        """ボタン生成
        Parameters
        ----------
        frame : Frame
            表示する親フレーム
        row : int
            表示する位置
        column : int
            表示する位置
        bg : RGB or string
            背景色
        """
        ttk.Style().configure("InstallBT.TButton", background=bg)
        self.select_dir_button = ttk.Button(self, text="...", width=8, style="InstallBT.TButton", command=self.dir_select_dialog)
        self.select_dir_button.grid(row=row, column=column, sticky="W", padx=4)

    def create_remove_checkbutton(self, frame, row, column, bg):
        """チェックボタン生成
        Parameters
        ----------
        frame : Frame
            表示する親フレーム
        row : int
            表示する位置
        column : int
            表示する位置
        bg : RGB or string
            背景色
        """
        self.cb_boolean.set(False)
        ttk.Style().configure("RemoveCB.TCheckbutton", background=bg)
        self.remove_checkbutton = ttk.Checkbutton(self, text="AviUtlやプラグインの圧縮ファイルを削除しない", style="RemoveCB.TCheckbutton", variable=self.cb_boolean)
        self.remove_checkbutton.grid(row=row, column=column, sticky="W", padx=4)

    def dir_select_dialog(self):
        """ディレクトリ選択ダイアログを表示する
        選択されたディレクトリを入力欄に表示する
        """
        self.dir_path = tk.filedialog.askdirectory(title="インストール先を選択してください")
        if self.dir_path != "":
            self.install_dir.set(self.dir_path)

    def get_install_path(self):
        """インストールパスを取得する
        Returns
        -------
        string
            インストールパス
        """
        return self.install_dir.get()

    def get_keep_dl_file(self):
        """保存の有無を取得する
        Returns
        -------
        bool
            True    保存する
            False   保存しない
        """
        return self.cb_boolean.get()

