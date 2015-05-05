# -*- coding: utf-8 -*-
# External modules
import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
# Internal modules
from main_config import *
from win_photo_an import WinPhotoAn
from win_epp import WinEpp
from win_settings import WinSettings
from win_view_proj import WinViewProj


class WinMain():
    def __init__(self, master=None):
        self.master = master

        self.is_project_under_edition = False

        # Initialize pointers to child windows with empty values
        self.win_epp = None
        self.win_settings = None
        self.win_photo_an = None
        self.win_view_proj = None

        self.project_file = None
        self.project_dict = None

        # Menu
        self.menubar = Menu(master)
        self.master.config(menu=self.menubar)

        # Projects menu
        self.menu_project = Menu(self.menubar, tearoff=0)
        self.menu_project.add_command(label=get_name("cmd_open_project"),
                                      command=self.cmd_open_project)

        self.menu_project.add_command(label=get_name("cmd_close_project"),
                                      command=self.cmd_close_project, state=DISABLED)
        self.menu_project.add_command(label=get_name("cmd_create_project"),
                                      command=self.cmd_create_project)
        self.menu_project.add_command(label=get_name("cmd_view_proj"),
                                      command=self.cmd_view_proj)
        self.menu_project.add_separator()

        self.menu_project.add_command(label=get_name("cmd_settings"),
                                      command=self.cmd_settings)
        self.menu_project.add_separator()
        self.menu_project.add_command(label=get_name("cmd_exit"), command=self.master.quit)

        self.menubar.add_cascade(label=get_name("menu_project"),
                                 menu=self.menu_project)

        # Common operations
        self.menu_common_op = Menu(self.menubar, tearoff=0)
        self.menu_common_op.add_command(label=get_name("cmd_save_photo"),
                                        command=self.cmd_save_photo)
        self.menu_common_op.add_command(label=get_name("cmd_analyse_photo"),
                                        command=self.cmd_analyse_photo)
        self.menubar.add_cascade(label=get_name("menu_common_op"),
                                 menu=self.menu_common_op)

        # Help
        self.menu_help = Menu(self.menubar, tearoff=0)
        self.menu_help.add_command(label=get_name("cmd_help"),
                                   command=self.cmd_help)
        self.menu_help.add_separator()
        self.menu_help.add_command(label=get_name("cmd_about"),
                                   command=self.cmd_about)
        self.menubar.add_cascade(label=get_name("menu_help"),
                                 menu=self.menu_help)

        self.frame_proj_info = None
        self.lbl_name = None
        self.lbl_start = None
        self.lbl_finish = None
        self.lbl_keywords = None
        self.lbl_description = None
        self.frame_proj_controls = None
        self.btn_analyze_photo = None
        self.btn_edit = None
        self.btn_get_stat = None
        self.btn_close_proj = None

    def project_selected(self):
        self.menu_project.entryconfig(1, state=ACTIVE)

        with open(self.project_file, encoding='utf-8') as f:
            self.project_dict = json_load(f)

        if self.frame_proj_info is not None:
            self.frame_proj_info.destroy()

        self.frame_proj_info = ttk.LabelFrame(master=self.master, text=get_name("frame_proj_info"))
        self.lbl_name = ttk.Label(master=self.frame_proj_info,
                                  justify=LEFT,
                                  text='{0}: {1}'.format(get_name('name'),
                                                         self.project_dict['name']))
        self.lbl_start = ttk.Label(master=self.frame_proj_info,
                                   justify=LEFT,
                                   text='{0}: {1} {2}'.format(get_name('start'),
                                                              self.project_dict['timeslot']['start']['time'],
                                                              self.project_dict['timeslot']['start']['date']))

        self.lbl_finish = ttk.Label(master=self.frame_proj_info,
                                    justify=LEFT,
                                    text='{0}: {1} {2}'.format(get_name('finish'),
                                                               self.project_dict['timeslot']['finish']['time'],
                                                               self.project_dict['timeslot']['finish']['date']))
        self.lbl_keywords = ttk.Label(master=self.frame_proj_info,
                                      justify=LEFT,
                                      wraplength=450,
                                      text='{0}:\n{1}'.format(get_name('keywords'),
                                                             self.project_dict['keywords']))
        self.lbl_description = ttk.Label(master=self.frame_proj_info,
                                         justify=LEFT,
                                         wraplength=450,
                                         text='{0}:\n{1}'.format(get_name('description'),
                                                                 self.project_dict['description']))

        if self.frame_proj_controls is not None:
            self.frame_proj_controls.destroy()

        self.frame_proj_controls = ttk.LabelFrame(master=self.master, text=get_name("frame_proj_controls"))
        self.btn_analyze_photo = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_analyze_photo"))
        self.btn_edit = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_edit"))
        self.btn_get_stat = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_get_stat"))
        self.btn_close_proj = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_close_proj"))

        self.btn_analyze_photo.bind('<ButtonRelease-1>', self.analyze_photo_from_project)
        self.btn_edit.bind('<ButtonRelease-1>', self.edit_project)
        self.btn_get_stat.bind('<ButtonRelease-1>', self.get_project_stat)
        self.btn_close_proj.bind('<ButtonRelease-1>', lambda _: self.cmd_close_project())

        self.frame_proj_info.pack(side=LEFT, fill=BOTH)
        self.lbl_name.pack(fill=X)
        self.lbl_start.pack(fill=X)
        self.lbl_finish.pack(fill=X)
        self.lbl_keywords.pack(fill=X)
        self.lbl_description.pack(fill=X)
        self.frame_proj_controls.pack(side=LEFT, fill=BOTH)
        self.btn_analyze_photo.pack(fill=X)
        self.btn_edit.pack(fill=X)
        self.btn_get_stat.pack(fill=X)
        self.btn_close_proj.pack(fill=X)

    def analyze_photo_from_project(self, _=None):
        # TODO: show warning to user
        if self.win_photo_an:
            self.win_photo_an.destroy()

        # Create window from class and save pointer
        self.win_photo_an = WinPhotoAn(master=self.master, path=os.path.split(self.project_file)[0])
        # Bind handler on destroying to clean up self class
        self.win_photo_an.bind("<Destroy>", self.handle_destroy_win_photo_an)

    def edit_project(self, _=None):
        # TODO: show warning to user
        if self.win_epp:
            self.win_epp.destroy()

        self.is_project_under_edition = True

        # Create window from class and save pointer
        self.win_epp = WinEpp(master=self.master, project_dict=self.project_dict)
        # Bind handler on destroying to clean up self class
        self.win_epp.bind("<Destroy>", self.handle_destroy_win_epp)

    def get_project_stat(self, _=None):
        pass

    def cmd_open_project(self):
        # If pointer is defined just switch focus to the window
        if self.win_photo_an:
            self.win_photo_an.focus_force()
            return

        fn = filedialog.askopenfilename(title=get_name("ask_dir_photo_an"),
                                        filetypes=[(get_name("photo_projects"),
                                                    "*.json")],
                                        initialdir=projects_dir)
        if not fn:
            return

        self.project_file = fn
        self.project_selected()

    def cmd_close_project(self):
        self.project_dict = None
        self.project_file = None
        self.menu_project.entryconfig(1, state=DISABLED)
        if self.frame_proj_info is not None:
            self.frame_proj_info.destroy()
        if self.frame_proj_controls is not None:
            self.frame_proj_controls.destroy()

    def cmd_settings(self, ev=None):
        # Create window from class and save pointer
        self.win_settings = WinSettings(master=self.master)
        # Bind handler on destroying to clean up self class
        self.win_settings.bind("<Destroy>", self.handle_destroy_win_settings)

    def handle_destroy_win_settings(self, ev=None):
        # Handle only destroying of main window
        if ev.widget != self.win_epp:
            return

        # Unset pointer
        self.win_settings = None

    def cmd_create_project(self):
        # If pointer is defined just switch focus to the window
        if self.win_epp:
            self.win_epp.focus_force()
            return

        # Create window from class and save pointer
        self.win_epp = WinEpp(master=self.master)
        # Bind handler on destroying to clean up self class
        self.win_epp.bind("<Destroy>", self.handle_destroy_win_epp)

    def handle_destroy_win_epp(self, ev=None):
        # Handle only destroying of main window
        if ev.widget != self.win_epp:
            return

        if self.is_project_under_edition:
            self.is_project_under_edition = False
            if self.win_epp.project_file is not None:
                self.project_file = self.win_epp.project_file
                self.project_dict = None
            self.project_selected()

        # Unset pointer
        self.win_epp = None

    def cmd_view_proj(self):
        if self.win_view_proj:
            self.win_view_proj.focus_force()
            return
        # Create window from class and save pointer
        self.win_view_proj = WinViewProj(master=self.master)
        # Bind handler on destroying to clean up self class
        self.win_view_proj.bind("<Destroy>", self.handle_destroy_win_view_proj)

    def handle_destroy_win_view_proj(self, ev=None):
        # Handle only destroying of main window
        if ev.widget != self.win_view_proj:
            return

        if self.win_view_proj.selected_proj is not None:
            self.project_file = self.win_view_proj.selected_proj
            self.project_selected()

        # Unset pointer
        self.win_view_proj = None

    def cmd_save_photo(self):
        pass

    def cmd_analyse_photo(self):
        # If pointer is defined just switch focus to the window
        if self.win_photo_an:
            self.win_photo_an.focus_force()
            return

        # Create window from class and save pointer
        path = filedialog.askdirectory(title=get_name("ask_dir_photo_an"))
        if path:
            self.win_photo_an = WinPhotoAn(master=self.master, path=path)
            # Bind handler on destroying to clean up self class
            self.win_photo_an.bind("<Destroy>", self.handle_destroy_win_photo_an)

    def handle_destroy_win_photo_an(self, ev=None):
        # Handle only destroying of main window
        if ev.widget != self.win_photo_an:
            return

        # Unset pointer
        self.win_photo_an = None

    @staticmethod
    def cmd_help():
        messagebox.showinfo(get_name("win_help"), get_name("text_help"))

    @staticmethod
    def cmd_about():
        messagebox.showinfo(get_name("win_about"), get_name("text_about"))

