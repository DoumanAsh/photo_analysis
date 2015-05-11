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

if __name__ == "__main__":
    root = Tk()
    root.geometry("+100+100")
    root.resizable(FALSE, FALSE)
    root.config(width=300,
                background=main_bg,
                padx=top_level_padding,
                pady=top_level_padding)
    style = ttk.Style()
    style.theme_use('xpnative')
    style.configure(style=".",
                    background=main_bg,
                    foreground=main_fg,
                    font=["Cambria", 12])
    style.configure(style="TLabelframe", padding=3)
    style.configure(style="Treeview", font=["Calibri", 10])
    style.configure(style="TButton", background=btn_bg, foreground=btn_fg)
    root.config(background=main_bg)
    root.title(get_name("win_main"))
    main_window = WinMain(root)
    root.mainloop()
