# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime
import os
from json import load as json_load
# Internal modules
from main_config import *
#from main import main_window

class WinViewProj(Toplevel):
    def __init__(self, master=None, ev=None, project_dict=None):
        Toplevel.__init__(self, master)
        self.title(get_name("win_view_proj"))
        self.focus_force()
        self.geometry("+200+200")
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.resizable(False, True)

        self.tree = ttk.Treeview(master=self, columns='name start finish keywords d')
        self.tree.heading('#0', text=get_name('projects'))
        self.tree.heading('name', text=get_name('name'))
        self.tree.column('start', width=110)
        self.tree.heading('start', text=get_name('start'))
        self.tree.column('finish', width=110)
        self.tree.heading('finish', text=get_name('finish'))
        self.tree.heading('keywords', text=get_name('keywords'))

        self.projects = []
        self.selected_proj = None
        for root, dirs, files in os.walk(projects_dir):
            if project_file in files:
                self.projects.append(os.path.join(root, project_file))

        print(len(self.projects))
        for i in range(0, len(self.projects)):
            self.tree.insert('', 'end', i + 1, text=os.path.split(os.path.split(self.projects[i])[0])[1])

            with open(self.projects[i], encoding='utf-8') as f:
                pd = json_load(f)

            self.tree.set(i + 1, 'name', pd['name'])
            self.tree.set(i + 1, 'start', ' '.join((pd['timeslot']['start']['date'], pd['timeslot']['start']['time'])))
            self.tree.set(i + 1, 'finish', ' '.join((pd['timeslot']['finish']['date'], pd['timeslot']['finish']['time'])))
            self.tree.set(i + 1, 'keywords', ' '.join(pd['keywords']))

        self.tree.pack(fill=Y, expand=1)
        self.tree.bind('<Double-Button-1>', self.handle_choose_proj)

    def handle_choose_proj(self, ev=None):
        self.selected_proj = self.projects[int(self.tree.focus()) - 1]
        self.destroy()
        #main_window.update_project()
