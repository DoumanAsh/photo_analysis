# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime
from json import load as json_load
from os import path as os_path
from os import walk as os_walk
# Internal modules
from main_config import *
#from main import main_window


class WinViewProj(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.title(get_name("win_view_proj"))
        self.focus_force()
        self.geometry("+200+200")
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.resizable(False, True)

        self.tree = ttk.Treeview(master=self, columns='name start finish keywords')
        self.tree.heading('#0', text=get_name('project'))
        self.tree.heading('name', text=get_name('name'))
        self.tree.column('start', width=110)
        self.tree.heading('start', text=get_name('start'))
        self.tree.column('finish', width=110)
        self.tree.heading('finish', text=get_name('finish'))
        self.tree.heading('keywords', text=get_name('keywords'))

        self.projects = []
        self.selected_proj = None
        for root, _, files in os_walk(settings["projects_dir"]):
            if project_file in files:
                self.projects.append(os_path.join(root, project_file))

        for ix, proj in enumerate(self.projects, start=1):
            self.tree.insert('', 'end', ix, text=os_path.split(os_path.split(proj)[0])[1])

            with open(proj, encoding='utf-8') as f:
                pd = json_load(f)

            self.tree.set(ix, 'name', pd['name'])
            self.tree.set(ix, 'start', ' '.join((pd['timeslot']['start']['date'], pd['timeslot']['start']['time'])))
            self.tree.set(ix, 'finish', ' '.join((pd['timeslot']['finish']['date'], pd['timeslot']['finish']['time'])))
            self.tree.set(ix, 'keywords', ' '.join(pd['keywords']))

        self.tree.pack(fill=Y, expand=1)
        self.tree.bind('<Double-ButtonRelease-1>', self.handle_choose_proj)

    def handle_choose_proj(self, _=None):
        if not self.tree.focus().isnumeric():
            return
        self.selected_proj = self.projects[int(self.tree.focus()) - 1]
        self.destroy()
        #main_window.update_project()
