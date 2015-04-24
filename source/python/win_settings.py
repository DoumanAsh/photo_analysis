# -*- coding: utf-8 -*-
# External modules
import json
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
# Internal modules
from main_config import *


class WinSettings(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.geometry("+200+200")
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.title(get_name("win_settings"))
        self.focus_force()

        # Declare elements
        # ==============================================================================================================
        self.frame_photo_an = ttk.LabelFrame(master=self, text=get_name("frame_photo_an"))

        self.frame_preview_size = ttk.Frame(master=self.frame_photo_an)
        self.lbl_preview_size = ttk.Label(master=self.frame_preview_size, text=get_name("lbl_preview_size"))
        self.scale_preview_size = ttk.Scale(master=self.frame_preview_size,
                                            from_=min_preview_size,
                                            to=max_preview_size,
                                            value=settings['photo_an']['preview_size'],
                                            command=self.scale_preview_size_change)

        self.lbl_preview_size_value = ttk.Label(master=self.frame_preview_size, text=self.scale_preview_size.get())

        self.frame_analysis_type = ttk.LabelFrame(master=self.frame_photo_an,
                                                  text=get_name("frame_analysis_type"))
        self.ch_btn_geo_an_value = StringVar()
        self.ch_btn_geo_an_value.set(settings['photo_an']['geo_an'])
        self.ch_btn_geo_an = ttk.Checkbutton(master=self.frame_analysis_type,
                                             text=get_name("ch_btn_geo_an"),
                                             variable=self.ch_btn_geo_an_value,
                                             onvalue='True',
                                             offvalue='False')

        self.ch_btn_obj_detect_an_value = StringVar()
        self.ch_btn_obj_detect_an_value.set(settings['photo_an']['obj_detect_an'])
        self.ch_btn_obj_detect_an = ttk.Checkbutton(master=self.frame_analysis_type,
                                                    text=get_name("ch_btn_obj_detect_an"),
                                                    variable=self.ch_btn_obj_detect_an_value,
                                                    onvalue='True',
                                                    offvalue='False')

        # ==============================================================================================================
        self.frame_buttons = ttk.Frame(master=self)
        self.btn_save = ttk.Button(master=self.frame_buttons, text=get_name("btn_save"))
        self.btn_save.bind('<ButtonRelease-1>', self.save_settings)
        self.btn_cancel = ttk.Button(master=self.frame_buttons, text=get_name("btn_cancel"))
        self.btn_cancel.bind('<ButtonRelease-1>', self.close)

        ################################################################################################################
        # Locate elements
        self.frame_photo_an.pack(fill=X)
        self.frame_preview_size.pack(fill=X)
        self.lbl_preview_size.pack(side=LEFT)
        self.scale_preview_size.pack(side=LEFT)
        self.lbl_preview_size_value.pack(side=LEFT)
        self.frame_analysis_type.pack(fill=X)
        self.ch_btn_geo_an.pack(side=LEFT)
        self.ch_btn_obj_detect_an.pack(side=LEFT)
        self.frame_buttons.pack(fill=X)
        self.btn_save.pack(side=LEFT)
        self.btn_cancel.pack(side=LEFT)

    def save_settings(self, ev=None):
        settings['photo_an']['preview_size'] = (int(self.scale_preview_size.get() / 10) * 10)
        settings['photo_an']['geo_an'] = self.ch_btn_geo_an_value.get()
        settings['photo_an']['obj_detect_an'] = self.ch_btn_obj_detect_an_value.get()
        with open(settings_json, 'w', encoding='utf-8') as f:
            json.dump(settings, f)
        self.destroy()

    def close(self, ev=None):
        self.destroy()

    def scale_preview_size_change(self, ev=None):
        self.lbl_preview_size_value.config(text=str(int(self.scale_preview_size.get() / 10) * 10))
