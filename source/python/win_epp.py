# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
# Internal modules
from main_config import *


class WinEpp(Toplevel):
    def __init__(self, master=None, ev=None, project_dict=None):

        Toplevel.__init__(self, master)
        self.title(get_name("win_epp"))
        self.focus_force()
        self.geometry("+200+200")
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.resizable(FALSE, FALSE)

        self.frame_proj_name = ttk.Frame(master=self)
        self.lbl_proj_name = ttk.Label(master=self.frame_proj_name,
                                       text=get_name("lbl_proj_name"))
        self.entry_proj_name = ttk.Entry(master=self.frame_proj_name, width=50)

        # Project timeslot (start/finish)
        self.frame_timeslot = ttk.LabelFrame(master=self,
                                             text=get_name("frame_timeslot"))
        self.lbl_start = ttk.Label(master=self.frame_timeslot,
                                   text=get_name("lbl_start"))
        self.lbl_start_date = ttk.Label(master=self.frame_timeslot,
                                        text=get_name("lbl_date"))
        self.entry_start_date = ttk.Entry(master=self.frame_timeslot)

        self.lbl_start_time = ttk.Label(master=self.frame_timeslot,
                                        text=get_name("lbl_time"))
        self.entry_start_time = ttk.Entry(master=self.frame_timeslot)

        self.lbl_finish = ttk.Label(master=self.frame_timeslot,
                                    text=get_name("lbl_finish"))
        self.lbl_finish_date = ttk.Label(master=self.frame_timeslot,
                                         text=get_name("lbl_date"))
        self.entry_finish_date = ttk.Entry(master=self.frame_timeslot)

        self.lbl_finish_time = ttk.Label(master=self.frame_timeslot,
                                         text=get_name("lbl_time"))
        self.entry_finish_time = ttk.Entry(master=self.frame_timeslot)
        #################################

        self.frame_buttons = ttk.Frame(master=self)
        self.btn_save = ttk.Button(master=self.frame_buttons, text=get_name("btn_save"))
        self.btn_save.bind('<ButtonRelease-1>', self.save_project)
        self.btn_cancel = ttk.Button(master=self.frame_buttons, text=get_name("btn_cancel"))
        self.btn_cancel.bind('<ButtonRelease-1>', self.close)

        self.frame_big_texts = ttk.Frame(master=self)
        self.frame_keywords = ttk.LabelFrame(master=self.frame_big_texts,
                                             text=get_name("frame_keywords"))
        self.txt_keywords = Text(master=self.frame_keywords,
                                 width=15,
                                 heigh=10,
                                 wrap='word')
        self.frame_description = ttk.LabelFrame(master=self.frame_big_texts,
                                                text=get_name("frame_description"))
        self.txt_description = Text(master=self.frame_description,
                                    width=37,
                                    heigh=10,
                                    wrap='word')

        # Fill existing values if we have project dictionary
        if project_dict:
            self.entry_proj_name.insert(0, project_dict["name"])
            self.entry_start_date.insert(0, project_dict["timeslot"]["start"]["date"])
            self.entry_start_time.insert(0, project_dict["timeslot"]["start"]["time"])

        # Locate elements
        self.frame_proj_name.pack(fill=X)
        self.lbl_proj_name.pack(side=LEFT)
        self.entry_proj_name.pack(side=LEFT)
        self.frame_timeslot.pack(fill=X)
        self.lbl_start.grid(row=0, column=0)
        self.lbl_start_date.grid(row=0, column=1)
        self.entry_start_date.grid(row=0, column=2)
        self.lbl_start_time.grid(row=0, column=3)
        self.entry_start_time.grid(row=0, column=4)
        self.lbl_finish.grid(row=1, column=0)
        self.lbl_finish_date.grid(row=1, column=1)
        self.entry_finish_date.grid(row=1, column=2)
        self.lbl_finish_time.grid(row=1, column=3)
        self.entry_finish_time.grid(row=1, column=4)
        self.frame_big_texts.pack(fill=BOTH)
        self.frame_keywords.pack(side=LEFT)
        self.txt_keywords.pack()
        self.frame_description.pack(side=LEFT)
        self.txt_description.pack()
        self.frame_buttons.pack(fill=X)
        self.btn_save.pack(side=LEFT)
        self.btn_cancel.pack(side=LEFT)

    def save_project(self, ev=None):
        proj_dict = {
            "name": self.entry_proj_name.get(),
            "timeslot": {
                "start": {
                    "date": self.entry_start_date.get(),
                    "time": self.entry_start_time.get()
                },
                "finish": {
                    "date": self.entry_finish_date.get(),
                    "time": self.entry_finish_time.get()
                }
            }
        }
        print(proj_dict)

    def close(self, ev=None):
        self.destroy()