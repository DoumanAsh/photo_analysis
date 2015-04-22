# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
# Internal modules
from main_config import *
from win_photo_an import WinPhotoAn
from win_epp import WinEpp
from win_settings import WinSettings


class App():
    def __init__(self, master=None):
        self.master = master
        self.win_epp = None
        self.win_settings = None
        self.win_photo_an = None
        self.win_view_projects = None

        # Menu
        self.menubar = Menu(master)
        self.master.config(menu=self.menubar)

        # Main menu
        self.menu_file = Menu(self.menubar, tearoff=0)
        self.menu_file.add_command(label=get_name("cmd_settings"),
                                   command=self.cmd_settings)
        self.menu_file.add_separator()
        self.menu_file.add_command(label=get_name("cmd_exit"), command=root.quit)
        self.menubar.add_cascade(label=get_name("menu_main"),
                                 menu=self.menu_file)

        # Projects menu
        self.menu_project = Menu(self.menubar, tearoff=0)
        self.menu_project.add_command(label=get_name("cmd_create_project"),
                                      command=self.cmd_create_project)
        self.menu_project.add_command(label=get_name("cmd_view_projects"),
                                      command=self.cmd_view_projects)
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

    def cmd_settings(self, ev=None):
        # Create window from class and save pointer
        self.win_settings = WinSettings(master=self.master)
        # Bind handler on destroying to clean up self class
        self.win_settings.bind("<Destroy>", self.handle_destroy_win_settings)

    def handle_destroy_win_settings(self, ev=None):
        # Unbind to avoid multiple calls
        self.win_settings.unbind("<Destroy>")
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
        # Unbind to avoid multiple calls
        self.win_epp.unbind("<Destroy>")
        # Unset pointer
        self.win_epp = None

    def cmd_view_projects(self):
        pass

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
        # Unbind to avoid multiple calls
        self.win_photo_an.unbind("<Destroy>")
        # Unset pointer
        self.win_photo_an = None

    @staticmethod
    def cmd_help():
        messagebox.showinfo(get_name("win_help"), get_name("text_help"))

    @staticmethod
    def cmd_about():
        messagebox.showinfo(get_name("win_about"), get_name("text_about"))


root = Tk()
root.geometry("300x300")
s = ttk.Style()
s.theme_use('clam')
s.configure(style=".", background=main_bg, foreground=main_fg)
root.config(background=main_bg)
root.title(get_name("win_main"))
app = App(root)

root.mainloop()