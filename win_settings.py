# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
# Internal modules
from main_config import *


class WinSettings(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.config(background=main_bg)
        self.title(get_name("win_settings"))
        self.focus_force()
