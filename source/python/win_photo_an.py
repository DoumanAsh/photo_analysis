# -*- coding: utf-8 -*-
# External modules
import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
# Internal modules
from main_config import *
import geo_tags
import object_detection


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
            if side is None:
                side = self.width

            self.load_image(image=image, long_edge=side)
            self.delete(self.canvas_img_id)

            self.canvas_img_id = self.create_image(self.width / 2,
                                                   self.height / 2,
                                                   image=self.tk_img)


class WinPhotoAn(Toplevel):
    def __init__(self, master=None, path=None):
        self.photo_for_analysis = []

        Toplevel.__init__(self, master)
        self.geometry("+200+200")
        self.config(background=main_bg,
                    padx=top_level_padding,
                    pady=top_level_padding)
        self.resizable(FALSE, FALSE)
        self.focus_force()
        self.title(get_name("win_photo_an"))

        self.current_photo_ix = 0

        # Collect all photos (with allowed extensions) with paths
        for top, _, files in os.walk(path):
            for _f in files:
                if os.path.splitext(_f)[1].lower() in supported_ext_for_analysis:
                    self.photo_for_analysis.append(os.path.join(top, _f))

        if not self.photo_for_analysis:  # If no photos found
            while True:
                # Ask to choose another folder
                if messagebox.askyesno(parent=self,
                                       title=get_name('title_dia_1_photo_an'),
                                       message=get_name('text_dia_1_photo_an')):  # Ok
                    new_path = filedialog.askdirectory(parent=self, title=get_name("ask_dir_photo_an"))
                    for top, _, files in os.walk(new_path):
                        for _f in files:
                            if os.path.splitext(_f)[1].lower() in supported_ext_for_analysis:
                                self.photo_for_analysis.append(os.path.join(top, _f))
                    if self.photo_for_analysis:  # Break from the loop if now photos are found
                        break
                else:  # Cancel
                    # TODO: good (user-friendly) handling of negative response is needed
                    return

        self.canvas_with_img = CanvasWithImage(master=self,
                                               image=self.photo_for_analysis[self.current_photo_ix],
                                               side=settings['photo_an']['preview_size'])
        self.canvas_with_img.bind('<Button-1>', self.next_photo)

        self.frame_main = ttk.Frame(master=self, padding=10)
        self.frame_controls = ttk.Frame(master=self.frame_main)

        self.frame_analysis_type = ttk.LabelFrame(master=self.frame_controls,
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

        self.btn_analyze = ttk.Button(master=self.frame_controls, text=get_name("btn_analyze"))
        self.btn_analyze.bind('<ButtonRelease-1>', self.analyze)
        self.btn_save = ttk.Button(master=self.frame_controls, text=get_name("btn_save"))
        self.btn_save.bind('<ButtonRelease-1>', self.save)

        self.frame_results = ttk.Frame(master=self.frame_main, padding=5)

        self.canvas_with_img.pack(fill=BOTH, side=LEFT)
        self.frame_main.pack(fill=BOTH, side=LEFT)
        self.frame_controls.pack(fill=X)
        self.frame_analysis_type.pack()
        self.ch_btn_geo_an.pack(side=LEFT)
        self.ch_btn_obj_detect_an.pack(side=LEFT)
        self.btn_analyze.pack(side=LEFT)
        self.btn_save.pack(side=LEFT)
        self.frame_results.pack(fill=X)

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

        # Recreate frame with results to clean up previous data
        self.frame_results.destroy()
        self.frame_results = ttk.Frame(master=self.frame_main, padding=5)
        self.frame_results.pack(fill=X)

    def show_msg(self, text=''):
        bg = '#FFF8DC'
        msg_win = Toplevel(self, background=bg)
        msg_win.geometry("400x200+{0}+{1}".format(int(self.winfo_screenwidth() / 2 - 200),
                                                  int(self.winfo_screenheight() / 2 - 100)))
        msg_win.overrideredirect(True)
        ttk.Label(msg_win,
                  text=text,
                  anchor=CENTER,
                  font=("Courier New", 14),
                  background=bg).place(relx=0.5, rely=0.4, anchor=CENTER)

        ttk.Label(msg_win,
                  text=get_name("please_wait"),
                  anchor=CENTER,
                  font=("Courier New", 14),
                  background=bg).place(relx=0.5, rely=0.6, anchor=CENTER)
        self.update()
        return msg_win

    # Handlers for parent check buttons: on change of parent value set value of children the same
    # ------------------------------------------------------------------------------------------------------------------
    def ch_btn_address_handler(self):
        for var in self.ch_btn_addr_values:
            var.set(self.ch_btn_address_info_value.get())

    def ch_btn_keywords_handler(self):
        for var in self.ch_btn_kw_values:
            var.set(self.ch_btn_keywords_value.get())
    # ==================================================================================================================

    def analyze(self, ev=None):
        # Dictionary to combine results of all analysis types together
        results = {}

        if self.ch_btn_geo_an_value.get() == "True":
            msg = self.show_msg(get_name("msg_run_geo_an"))

            # Get results of geo-analysis
            results.update(geo_tags.get_geo_tags_in_iptc_format(self.photo_for_analysis[self.current_photo_ix]))

            msg.destroy()

            # Display header for address info only if we have found address (have got non-empty result)
            if results:
                self.ch_btn_address_info_value = StringVar()
                self.ch_btn_address_info_value.set(1)
                self.ch_btn_address_info = ttk.Checkbutton(master=self.frame_results,
                                                           text=get_name("address_info"),
                                                           variable=self.ch_btn_address_info_value,
                                                           command=self.ch_btn_address_handler)
                self.ch_btn_address_info.pack(fill=X, anchor=W)
                self.frame_address_info = ttk.Frame(master=self.frame_results, padding=(7, 0))
                self.frame_address_info.pack(fill=X)

        self.ch_btn_addr = []
        self.ch_btn_addr_values = []
        for name in sorted(results):
            # Skip keywords here, they will be displayed later
            if name == "keywords":
                continue
            self.ch_btn_addr_values.append(StringVar())
            self.ch_btn_addr_values[-1].set(1)
            self.ch_btn_addr.append(ttk.Checkbutton(master=self.frame_address_info,
                                                    text=results[name],
                                                    variable=self.ch_btn_addr_values[-1]))

            self.ch_btn_addr[-1].grid(row=len(self.ch_btn_addr) - 1, column=0, sticky=W)

        if self.ch_btn_obj_detect_an_value.get() == "True":
            msg = self.show_msg(get_name("msg_run_obj_detect_an"))

            # Get results of object detection
            if "keywords" in results:
                results["keywords"].extend(object_detection.get_keywords(self.photo_for_analysis[self.current_photo_ix]))
            else:
                results["keywords"] = object_detection.get_keywords(self.photo_for_analysis[self.current_photo_ix])

            msg.destroy()

        if results["keywords"]:
            self.ch_btn_keywords_value = StringVar()
            self.ch_btn_keywords_value.set(1)
            self.ch_btn_keywords = ttk.Checkbutton(master=self.frame_results,
                                                   text=get_name("keywords"),
                                                   variable=self.ch_btn_keywords_value,
                                                   command=self.ch_btn_keywords_handler)
            self.ch_btn_keywords.pack(fill=X, anchor=W)
            self.frame_keywords = ttk.Frame(master=self.frame_results, padding=(7, 0))
            self.frame_keywords.pack(fill=X)

            self.ch_btn_kw = []
            self.ch_btn_kw_values = []

            for kw in results["keywords"]:
                self.ch_btn_kw_values.append(StringVar())
                self.ch_btn_kw_values[-1].set(1)
                self.ch_btn_kw.append(ttk.Checkbutton(master=self.frame_keywords,
                                                      text=kw,
                                                      variable=self.ch_btn_kw_values[-1]))

                self.ch_btn_kw[-1].grid(row=len(self.ch_btn_kw) - 1, column=0, sticky=W)

    def save(self, ev=None):
        pass
