# -*- coding: utf-8 -*-
# External modules
from shutil import rmtree as delete_folder
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
        self.bind('<Return>', self.choose_proj)
        self.bind('<Delete>', self.delete_proj)
        self.bind('<Escape>', lambda _: self.destroy())
        self.title(get_name("win_view_proj"))
        self.focus_force()
        self.geometry("+200+200")
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.resizable(False, True)

        self.projects = []
        self.selected_proj = None
        self.draw_elements()

    def draw_elements(self):
        self.frame_tree = ttk.Frame(master=self)
        self.tree = ttk.Treeview(master=self.frame_tree, columns='name start finish keywords', height=20)
        self.scroll_tree_y = ttk.Scrollbar(master=self.frame_tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.scroll_tree_y.set)
        self.tree.column('#0', width=70)
        self.tree.heading('#0', text=get_name('project_num'))
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
            self.tree.insert('', 'end', ix, text=ix)

            with open(proj, encoding='utf-8') as f:
                pd = json_load(f)

            self.tree.set(ix, 'name', pd['name'])
            self.tree.set(ix, 'start', ' '.join((pd['timeslot']['start']['date'], pd['timeslot']['start']['time'])))
            self.tree.set(ix, 'finish', ' '.join((pd['timeslot']['finish']['date'], pd['timeslot']['finish']['time'])))
            self.tree.set(ix, 'keywords', ' '.join(pd['keywords']))

        self.lbl = ttk.Label(master=self,
                             text='{0}: {1}'.format(get_name("total_num_of_proj"), len(self.projects)))

        self.lbl.pack(fill=X)
        self.frame_tree.pack(fill=BOTH, expand=1)
        self.tree.pack(fill=Y, expand=1, side=LEFT)
        self.scroll_tree_y.pack(fill=Y, expand=1, side=RIGHT)
        self.tree.bind('<Double-ButtonRelease-1>', self.choose_proj)

    def choose_proj(self, _=None):
        if not self.tree.focus().isnumeric():
            return
        self.selected_proj = self.projects[int(self.tree.focus()) - 1]
        self.destroy()

    def delete_proj(self, _=None):
        if not self.tree.focus().isnumeric():
            return
        if messagebox.askyesno(parent=self, title=get_name("ask_conf_del_proj_title"), message=get_name("ask_conf_del_proj_text")):
            delete_folder(path=os_path.split(self.projects[int(self.tree.focus()) - 1])[0])
            for child in self.winfo_children():
                child.destroy()
            self.projects = []
            self.selected_proj = None
            self.draw_elements()
