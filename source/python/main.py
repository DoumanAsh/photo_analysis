# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import ttk
# Internal modules
from main_config import *
from win_main import WinMain


class Settings():
    def __init__(self, test=None):
        self.test = test

root = Tk()
root.geometry("300x300+100+100")
style = ttk.Style()
style.theme_use('clam')
style.configure(style=".", background=main_bg, foreground=main_fg)
style.configure(style="TLabelframe", padding=3)
style.configure(style="TButton", background=btn_bg, foreground=btn_fg)
root.config(background=main_bg)
root.title(get_name("win_main"))
main_window = WinMain(root)

root.mainloop()