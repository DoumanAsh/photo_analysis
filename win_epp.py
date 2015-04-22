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
        self.config(background=main_bg)
        self.title(get_name("win_epp"))
        self.focus_force()
        self.lbl_proj_name = ttk.Label(master=self,
                                       text=get_name("lbl_proj_name"))
        self.entry_proj_name = ttk.Entry(master=self, width=40)

        # Project timeslot (start/finish)
        self.frame_timeslot = LabelFrame(master=self,
                                         text=get_name("frame_timeslot"),
                                         background=main_bg,
                                         foreground=main_fg)
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

        self.btn_save = ttk.Button(master=self, text=get_name("btn_save"))
        self.btn_save.bind('<ButtonRelease-1>', self.save_project)
        self.btn_cancel = ttk.Button(master=self, text=get_name("btn_cancel"))
        self.btn_cancel.bind('<ButtonRelease-1>', self.close)

        self.frame_keywords = LabelFrame(master=self,
                                         text=get_name("frame_keywords"),
                                         background=main_bg,
                                         foreground=main_fg)
        self.txt_keywords = Text(master=self.frame_keywords,
                                 width=15,
                                 heigh=10,
                                 wrap='word')
        self.frame_description = LabelFrame(master=self,
                                            text=get_name("frame_description"),
                                            background=main_bg,
                                            foreground=main_fg)
        self.txt_description = Text(master=self.frame_description,
                                    width=40,
                                    heigh=10,
                                    wrap='word')

        # Fill existing values if we have project dictionary
        if project_dict:
            self.entry_proj_name.insert(0, project_dict["name"])
            self.entry_start_date.insert(0, project_dict["timeslot"]["start"]["date"])
            self.entry_start_time.insert(0, project_dict["timeslot"]["start"]["time"])

        # Locate elements
        self.lbl_proj_name.grid(row=0, column=0)
        self.entry_proj_name.grid(row=0, column=1)
        self.frame_timeslot.grid(row=1, column=0, columnspan=5)
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
        self.frame_keywords.grid(row=2, column=0)
        self.txt_keywords.pack(side='left', fill='both', expand=1)
        self.frame_description.grid(row=2, column=1)
        self.txt_description.pack(side='left', fill='both', expand=1)
        self.btn_save.grid(row=3, column=0)
        self.btn_cancel.grid(row=3, column=1)

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