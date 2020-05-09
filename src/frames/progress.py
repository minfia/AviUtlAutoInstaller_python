# -*- coding: utf-8 -*-


import tkinter as tk
import tkinter.ttk as ttk


class InstallProgressWidget(tk.Frame):
    def __init__(self, master=None, bg="white"):
        """コンストラクタ
        各ウィジェットの生成をする
        Parameters
        ----------
        bg : RGB or string
            背景色
        """
        super().__init__(master)
        self.widget_frame = self
        self.widget_frame.configure(bg=bg)
        self.widget_frame.pack(anchor="w", fill="both")
        self.filename_text = tk.StringVar()
        self.filedlsize_text = tk.StringVar()
        self.filesize_text = tk.StringVar()
        self.file_text = tk.StringVar()
        self.progress_value = tk.IntVar()

        self.create_progress_label(frame=self.widget_frame, row=1, column=1, bg=bg)
        self.create_progressbar(frame=self.widget_frame, row=2, column=1)

    def create_progress_label(self, frame, row, column, bg):
        """処理表示ラベルの生成
        Parameters
        ----------
        frame : Frame
            表示するフレーム
        row : int
            表示する位置(行)
        column : int
            表示する位置(列)
        bg : RGB or string
            背景色
        """
        self.set_filename("progress")
        self.set_filedlsize("x")
        self.set_filesize("y")
        self.update_filelabel()
        ttk.Style().configure("InstallPB.TLabel", background=bg)
        self.label = ttk.Label(frame, textvariable=self.file_text, style="InstallPB.TLabel")
        self.label.grid(row=row, column=column, sticky="W")

    def create_progressbar(self, frame, row, column):
        """プログレスバーの生成
        Parameters
        ----------
        frame : Frame
            表示するフレーム
        row : int
            表示する位置(行)
        column : int
            表示する位置(列)
        """
        self.progress_value.set(0)
        self.progress_bar = ttk.Progressbar(frame, length=200, variable=self.progress_value, mode="determinate")
        self.progress_bar.grid(row=row, column=column, sticky=(tk.W, tk.E), padx=4)
        self.columnconfigure(column, weight=1)

    def __get_mode(self):
        """プログレスバーのモードを文字列で返す
        Returns
        -------
            mode    : モード
        """
        obj = self.progress_bar.cget("mode")
        mode = ""
        if type(obj) is str:
            mode = obj
        else:
            mode = obj.string
        return mode

    def set_indeterminate(self):
        """プログレスバーを不確定的に設定
        """
        self.progress_bar.configure(maximum=10)
        mode = self.__get_mode()
        if not mode == "indeterminate":
            self.progress_bar.configure(mode = "indeterminate")
            self.progress_bar.start()

    def set_determinate(self):
        """プログレスバーを確定的に変更
        """
        mode = self.__get_mode()
        if not mode == "determinate":
            self.progress_bar.stop()
            self.progress_bar.configure(mode = "determinate")

    def set_filename(self, name):
        """ラベルに表示するファイル名をセットする
        Parameters
        ----------
        name : string
            ファイル名
        """
        self.filename_text.set(name)
        self.update_filelabel()

    def set_filesize(self, size):
        """ラベルに表示するファイルサイズをセットする
        Parameters
        ----------
        size : int
            ファイルサイズj
        """
        self.filesize_text.set(size)
        self.update_filelabel()

    def set_filedlsize(self, size):
        """ラベルに表示するダウンロード済みサイズをセットする
        Parameters
        ----------
        size : int
            ダウンロード済みサイズ
        """
        self.filedlsize_text.set(size)
        self.update_filelabel()

    def update_filelabel(self):
        """ラベルを更新する
        """
        self.file_text.set(self.filename_text.get()+": "+self.filedlsize_text.get()+"/"+self.filesize_text.get())

    def setup_progress(self, name, totalsize):
        """ラベルとプログレスバーを初期化する
        Parameters
        ----------
        name : string
            ファイル名
        totalsize : int
            ファイルサイズ
        """
        self.progress_value.set(0)
        if self.__get_mode() == "determinate":
            self.progress_bar.configure(maximum=int(totalsize))
        self.progress_bar.update()
        self.set_filename(name)
        self.set_filedlsize("0")
        self.set_filesize(totalsize)

    def update_progress(self, value):
        """プログレスバーを更新する
        Parameters
        ----------
        value : int
            ダウンロード済みファイルサイズ
        """
        if self.__get_mode() == "determinate":
            self.progress_value.set(value)
            self.set_filedlsize(value)
        self.progress_bar.update()

    def hide_frame(self):
        """InstallProgressWidgetを非表示にする
        """
        self.widget_frame.pack_forget()

    def show_frame(self):
        """InstallProgressWidgetを表示する
        """
        self.widget_frame.pack(anchor="w", fill="both")

