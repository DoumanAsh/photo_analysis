# -*- coding: utf-8 -*-
# External modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
# Internal modules
from main_config import *


class CanvasWithImage(Canvas):
    def __init__(self, master=None, image=None, side=0):
        Canvas.__init__(self, master, height=side, width=side, bg=canvas_bg)
        # Init properties
        self.image_name = image
        self.width = side
        self.height = side
        self.tk_img = None
        self.width_img = None
        self.height_img = None
        self.load_image(image=image, long_edge=side)
        self.canvas_img_id = self.create_image(self.width / 2,
                                               self.height / 2,
                                               image=self.tk_img)

    def load_image(self, image=None, long_edge=None):
        pil_img = Image.open(image)

        if long_edge > 0:
            i = 0 if pil_img.size[0] > pil_img.size[1] else 1
            j = abs(i - 1)

            percent = (long_edge / float(pil_img.size[i]))
            short_edge = int((float(pil_img.size[j]) * float(percent)))

            if i:
                pil_img = pil_img.resize((short_edge, long_edge), Image.ANTIALIAS)
            else:
                pil_img = pil_img.resize((long_edge, short_edge), Image.ANTIALIAS)

        self.width_img = pil_img.size[0]
        self.height_img = pil_img.size[1]
        self.tk_img = ImageTk.PhotoImage(pil_img)

    def config(self, image=None, side=None):
        if image:
            del self.tk_img
            self.load_image(image=image, long_edge=side if side else self.width)
            self.delete(self.canvas_img_id)

            self.canvas_img_id = self.create_image(self.width / 2,
                                                   self.height / 2,
                                                   image=self.tk_img)


class WinPhotoAn(Toplevel):
    def __init__(self, master=None, path=None):
        self.photo_for_analysis = []

        # Collect all photos (with allowed extensions) with paths
        for top, dirs, files in os.walk(path):
            for _f in files:
                if os.path.splitext(_f)[1].lower() in supported_ext_for_analysis:
                    self.photo_for_analysis.append(os.path.join(top, _f))

        if not self.photo_for_analysis:  # If no photos found
            while True:
                # Ask to choose another folder
                if messagebox.askokcancel(get_name('title_dia_1_photo_an'), get_name('text_dia_1_photo_an')):  # Ok
                    new_path = filedialog.askdirectory(title=get_name("ask_dir_photo_an"))
                    for top, dirs, files in os.walk(new_path):
                        for _f in files:
                            if os.path.splitext(_f)[1].lower() in supported_ext_for_analysis:
                                self.photo_for_analysis.append(os.path.join(top, _f))
                    if self.photo_for_analysis:  # Break from the loop if now photos are found
                        break
                else:  # Cancel
                    self.destroy()

        Toplevel.__init__(self, master)
        self.geometry("{0}x{1}+200+200".format(settings['photo_an']['preview_size'] + 200,
                                               settings['photo_an']['preview_size']))
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.resizable(FALSE, FALSE)
        self.focus_force()

        self.current_photo_ix = 0
        self.canvas_with_img = CanvasWithImage(master=self,
                                               image=self.photo_for_analysis[self.current_photo_ix],
                                               side=settings['photo_an']['preview_size'])
        self.canvas_with_img.bind('<Button-1>', self.next_photo)
        self.canvas_with_img.pack(fill='both', side='left')
        self.config(background=main_bg)
        self.title(get_name("win_photo_an"))
        self.frame = Frame(master=self)
        self.frame.pack(side='right', fill='both', expand=1)
        self.label = Label(self.frame, text="test")
        self.label.pack()

    def next_photo(self, ev=None):
        x, y = ev.x, ev.y
        if x > self.canvas_with_img.width / 2:
            self.current_photo_ix += 1
        else:
            self.current_photo_ix -= 1

        if self.current_photo_ix >= len(self.photo_for_analysis):
            self.current_photo_ix = 0
        if self.current_photo_ix < 0:
            self.current_photo_ix = len(self.photo_for_analysis) - 1

        self.canvas_with_img.config(image=self.photo_for_analysis[self.current_photo_ix])
