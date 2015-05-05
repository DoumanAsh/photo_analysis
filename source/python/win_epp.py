# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime
import os
import json
# Internal modules
from main_config import *


class WinEpp(Toplevel):
    def __init__(self, master=None, ev=None, project_dict=None):
        self.project_file = None

        Toplevel.__init__(self, master)
        self.title(get_name("win_epp"))
        self.focus_force()
        self.geometry("+200+200")
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.resizable(False, False)

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
            self.entry_finish_date.insert(0, project_dict["timeslot"]["finish"]["date"])
            self.entry_finish_time.insert(0, project_dict["timeslot"]["finish"]["time"])
            self.txt_keywords.insert('1.0', '\n'.join(project_dict["keywords"]))
            self.txt_description.insert('1.0', project_dict["description"])
        else:
            self.entry_start_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
            self.entry_start_time.insert(0, "00:00")
            self.entry_finish_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
            self.entry_finish_time.insert(0, "23:59")

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
        # Check projects directory
        if not os.path.isdir(projects_dir):
            messagebox.showerror(parent=self, title=get_name('msg_wrong_proj_dir_title'),
                                 message=get_name('msg_wrong_proj_dir_text'))

        proj_dict = dict(name=self.entry_proj_name.get(),
                         timeslot=dict(start=dict(date=self.entry_start_date.get(),
                                                  time=self.entry_start_time.get()),
                                       finish=dict(date=self.entry_finish_date.get(),
                                                   time=self.entry_finish_time.get())),
                         keywords=self.txt_keywords.get('1.0', END).replace(',', ' ').replace(';', ' ').split(),
                         description=self.txt_description.get('1.0', END))

        # Date/time checks
        # --------------------------------------------------------------------------------------------------------------
        if not self.verify_date(proj_dict["timeslot"]["start"]["date"]):
            messagebox.showerror(parent=self, title=get_name('msg_wrong_start_date_title'),
                                 message=get_name('msg_wrong_start_date_text'))
            return
        if not self.verify_date(proj_dict["timeslot"]["finish"]["date"]):
            messagebox.showerror(parent=self, title=get_name('msg_wrong_finish_date_title'),
                                 message=get_name('msg_wrong_finish_date_text'))
            return
        if not self.verify_time(proj_dict["timeslot"]["start"]["time"]):
            messagebox.showerror(parent=self, title=get_name('msg_wrong_start_time_title'),
                                 message=get_name('msg_wrong_start_time_text'))
            return
        if not self.verify_time(proj_dict["timeslot"]["finish"]["time"]):
            messagebox.showerror(parent=self, title=get_name('msg_wrong_finish_time_title'),
                                 message=get_name('msg_wrong_finish_time_text'))
            return

        datetime_start = datetime.strptime('{0} {1}'.format(proj_dict["timeslot"]["start"]["date"],
                                                            proj_dict["timeslot"]["start"]["time"]),
                                           '%d.%m.%Y %H:%M')
        datetime_finish = datetime.strptime('{0} {1}'.format(proj_dict["timeslot"]["finish"]["date"],
                                                             proj_dict["timeslot"]["finish"]["time"]),
                                            '%d.%m.%Y %H:%M')
        if datetime_finish < datetime_start:
            messagebox.showerror(parent=self, title=get_name('msg_wrong_start_finish_datetime_title'),
                                 message=get_name('msg_wrong_start_finish_datetime_text'))
            return
        # ==============================================================================================================

        splitted_start_date = proj_dict["timeslot"]["start"]["date"].split('.')
        path = '{0}-{1}-{2}'.format(splitted_start_date[2], splitted_start_date[1], splitted_start_date[0])
        if proj_dict["timeslot"]["start"]["date"] != proj_dict["timeslot"]["finish"]["date"]:
            splitted_finish_date = proj_dict["timeslot"]["finish"]["date"].split('.')
            path = '{0}-{1}-{2}-{3}'.format(path, splitted_finish_date[2], splitted_finish_date[1], splitted_finish_date[0])
        path = '{0}_{1}'.format(path, proj_dict["name"].replace(' ', '_'))

        path = os.path.normpath(os.path.join(projects_dir, path))

        # Create a new folder for project if not exist
        if os.path.isdir(path):
            rc = messagebox.askyesnocancel(parent=self,
                                           title=get_name('msg_proj_overwrite_title'),
                                           message=get_name('msg_proj_overwrite_text'))
            if rc is False:
                self.close()
                return
            if rc is None:
                return
        else:
            os.mkdir(path)

        with open(os.path.join(path, project_file), "w", encoding='utf-8') as f:
            json.dump(proj_dict, f)

        messagebox.showinfo(parent=self, title=get_name('msg_proj_saved_title'),
                            message='{0}\n{1}'.format(get_name('msg_proj_saved_text'), path))
        self.project_file = os.path.join(path, project_file)
        self.close()

    def close(self, _=None):
        self.destroy()

    @staticmethod
    def verify_date(date):
        try:
            datetime.strptime(date, '%d.%m.%Y')
            return True
        except ValueError as e:
            print(e)
            return False

    @staticmethod
    def verify_time(time):
        try:
            datetime.strptime(time, '%H:%M')
            return True
        except ValueError as e:
            print(e)
            return False