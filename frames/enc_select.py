# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk


class EncoderSelectWidget(tk.Frame):
    def __init__(self, master=None, bg="white"):
        """コンストラクタ
        各ウィジェットの生成をする
        Parameters
        ----------
        bg : RGB or string
        """
        super().__init__(master)
        self.widget_frame = self
        self.widget_frame.configure(bg=bg)
        self.widget_frame.pack(anchor="nw", fill="x", pady=8)
        self.x264_enc_boolean = tk.BooleanVar()
        self.qsv_enc_boolean = tk.BooleanVar()
        self.nvenc_boolean = tk.BooleanVar()
        self.vceenc_boolean = tk.BooleanVar()
        self.create_encoder_label(frame=self.widget_frame, bg=bg)
        self.create_encoder_checkbutton(frame=self.widget_frame, bg=bg)

    def create_encoder_label(self, frame, bg):
        """ラベルを生成
        Patameters
        ----------
        frame : Frame
            表示する親フレーム
        bg : RGB or string
            背景色
        """
        ttk.Style().configure("EncL.TLabel", background=bg)
        self.select_label = ttk.Label(frame, text="インストールするエンコーダ", style="EncL.TLabel")
        self.select_label.pack(anchor="w", padx=4)

    def create_encoder_checkbutton(self, frame, bg):
        """エンコーダーの選択チェックボタンを生成
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
        self.checkbutton_status_list = [["x264guiEx",   self.x264_enc_boolean,  1,  "disabled"  ],
                                        ["QSV"      ,   self.qsv_enc_boolean ,  0,  "enabled"   ],
                                        ["NVEnc"    ,   self.nvenc_boolean   ,  0,  "enabled"   ],
                                        ["VCEEnc"   ,   self.vceenc_boolean  ,  0,  "enabled"   ]]
        ttk.Style().configure("EncCB.TCheckbutton", background=bg)
        for i in range(len(self.checkbutton_status_list)):
            ttk.Checkbutton(self, text=self.checkbutton_status_list[i][0], style="EncCB.TCheckbutton", state=self.checkbutton_status_list[i][3],
                            variable=self.checkbutton_status_list[i][1]).pack(side="left", padx=4)
            self.checkbutton_status_list[i][1].set(self.checkbutton_status_list[i][2])

    def get_enc_type_list(self):
        enc_list = [self.x264_enc_boolean.get(), self.qsv_enc_boolean.get(), self.nvenc_boolean.get(), self.vceenc_boolean.get()]
        return enc_list

