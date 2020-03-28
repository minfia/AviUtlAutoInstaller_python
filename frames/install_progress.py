# -*- coding: utf-8 -*-


import tkinter as tk
import tkinter.ttk as ttk


class InstallProgressWidget(tk.Frame):
    def __init__(self, master=None, bg="white"):
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
        self.set_filename("progress")
        self.set_filedlsize("x")
        self.set_filesize("y")
        self.update_filelabel()
        ttk.Style().configure("InstallPB.TLabel", background=bg)
        self.label = ttk.Label(frame, textvariable=self.file_text, style="InstallPB.TLabel")
        self.label.grid(row=row, column=column, sticky="W")

    def create_progressbar(self, frame, row, column):
        self.progress_value.set(0)
        self.progress_bar = ttk.Progressbar(frame, length=200, variable=self.progress_value, mode="determinate")
        self.progress_bar.grid(row=row, column=column, sticky=(tk.W, tk.E), padx=4)
        self.columnconfigure(column, weight=1)

    def set_filename(self, name):
        self.filename_text.set(name)
        self.update_filelabel()

    def set_filesize(self, size):
        self.filesize_text.set(size)
        self.update_filelabel()

    def set_filedlsize(self, size):
        self.filedlsize_text.set(size)
        self.update_filelabel()

    def update_filelabel(self):
        self.file_text.set(self.filename_text.get()+": "+self.filedlsize_text.get()+"/"+self.filesize_text.get())

    def setup_progress(self, name, totalsize):
        self.progress_value.set(0)
        self.progress_bar.configure(maximum=int(totalsize))
        self.progress_bar.update()
        self.set_filename(name)
        self.set_filedlsize("0")
        self.set_filesize(totalsize)

    def update_progress(self, value):
        self.progress_value.set(value)
        self.set_filedlsize(value)
        self.progress_bar.update()

    def hide_frame(self):
        self.widget_frame.pack_forget()

    def show_frame(self):
        self.widget_frame.pack(anchor="w", fill="both")

