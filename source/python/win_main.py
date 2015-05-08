# -*- coding: utf-8 -*-
# External modules
from shutil import rmtree as delete_folder
from re import compile as re_compile
from os import path as os_path
from os import walk as os_walk
from os import listdir
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox, font
from tkinter import ttk
# Internal modules
from main_config import *
from win_photo_an import WinPhotoAn
from win_epp import WinEpp
from win_settings import WinSettings
from win_view_proj import WinViewProj
import exiftool as et


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

        self.frame_welcome = None
        self.frame_project = None
        self.create_frame_welcome()

    def create_frame_welcome(self):
        self.frame_welcome = ttk.Frame(master=self.master)
        self.frame_default_controls = ttk.Frame(master=self.frame_welcome)

        self.btn_open_proj = ttk.Button(master=self.frame_default_controls, text=get_name("cmd_open_project"))
        self.btn_create_proj = ttk.Button(master=self.frame_default_controls, text=get_name("cmd_create_project"))
        self.btn_view_proj = ttk.Button(master=self.frame_default_controls, text=get_name("cmd_view_proj"))
        self.btn_save_photo = ttk.Button(master=self.frame_default_controls, text=get_name("cmd_save_photo"))
        self.btn_analyse_photo = ttk.Button(master=self.frame_default_controls, text=get_name("cmd_analyse_photo"))

        self.btn_open_proj.bind('<ButtonRelease-1>', lambda _: self.cmd_open_project())
        self.btn_create_proj.bind('<ButtonRelease-1>', lambda _: self.cmd_create_project())
        self.btn_view_proj.bind('<ButtonRelease-1>', lambda _: self.cmd_view_proj())
        self.btn_save_photo.bind('<ButtonRelease-1>', lambda _: self.cmd_save_photo())
        self.btn_analyse_photo.bind('<ButtonRelease-1>', lambda _: self.cmd_analyse_photo())

        self.lbl_welcome1 = ttk.Label(master=self.frame_welcome,
                                      text=get_name("welcome_text1"),
                                      justify=CENTER,
                                      padding=10,
                                      font=["Segoe Print", 16])


        self.lbl_welcome2 = ttk.Label(master=self.frame_welcome,
                                      text=get_name("welcome_text2"),
                                      justify=CENTER,
                                      padding=10,
                                      font=["Segoe Print", 12])

        self.frame_welcome.pack(fill=BOTH)
        self.lbl_welcome1.grid(row=0, column=0)
        self.lbl_welcome2.grid(row=1, column=0)
        self.frame_default_controls.grid(rowspan=2, row=0, column=1)
        self.btn_open_proj.pack(fill=X)
        self.btn_create_proj.pack(fill=X)
        self.btn_view_proj.pack(fill=X)
        self.btn_save_photo.pack(fill=X)
        self.btn_analyse_photo.pack(fill=X)

    def project_selected(self):
        if self.frame_welcome is not None:
            self.frame_welcome.destroy()
            self.frame_welcome = None

        self.menu_project.entryconfig(1, state=ACTIVE)

        with open(self.project_file, encoding='utf-8') as f:
            self.project_dict = json_load(f)

        if self.frame_project is not None:
            self.frame_project.destroy()


        self.frame_project = ttk.Frame(master=self.master)

        self.frame_proj_info = ttk.LabelFrame(master=self.frame_project, text=get_name("frame_proj_info"))

        text = '''{0}:\t"{1}"

{2}:\t{3}\t{4}
{5}:\t{6}\t{7}

{8}:
{9}

{10}:
{11}'''.format(get_name('name'),
               self.project_dict['name'],
               get_name('start'),
               self.project_dict['timeslot']['start']['time'],
               self.project_dict['timeslot']['start']['date'],
               get_name('finish'),
               self.project_dict['timeslot']['finish']['time'],
               self.project_dict['timeslot']['finish']['date'],
               get_name('keywords'),
               self.project_dict['keywords'] if self.project_dict['keywords'] else get_name("empty"),
               get_name('description'),
               self.project_dict['description'] if self.project_dict['description'].strip() else get_name("empty"))

        self.lbl_proj_info = ttk.Label(master=self.frame_proj_info,
                                       justify=LEFT,
                                       wraplength=450,
                                       text=text)

        self.frame_proj_controls = ttk.LabelFrame(master=self.frame_project, text=get_name("frame_proj_controls"))
        self.btn_analyze_photo = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_analyze_photo"))
        self.btn_edit = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_edit"))
        self.btn_close_proj = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_close_proj"))
        self.btn_delete_proj = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_delete_proj"))
        self.btn_refresh = ttk.Button(master=self.frame_proj_controls, text=get_name("btn_refresh"))

        self.btn_analyze_photo.bind('<ButtonRelease-1>', self.analyze_photo_from_project)
        self.btn_edit.bind('<ButtonRelease-1>', self.edit_project)
        self.btn_close_proj.bind('<ButtonRelease-1>', lambda _: self.cmd_close_project())
        self.btn_delete_proj.bind('<ButtonRelease-1>', lambda _: self.delete_proj())
        self.btn_refresh.bind('<ButtonRelease-1>', self.refresh)

        self.frame_proj_stat = ttk.LabelFrame(master=self.frame_project, text=get_name("frame_proj_stat"))

        proj_path = os_path.split(self.project_file)[0]
        folders = next(os_walk(proj_path))[1]

        if folders:
            self.tree_folders = ttk.Treeview(master=self.frame_proj_stat,
                                             columns=('Files', 'Nested folders'),
                                             height=len(folders),
                                             selectmode=NONE)
            self.tree_folders.column('#0', stretch=False)
            self.tree_folders.heading('#0', text=get_name('folder'))
            self.tree_folders.column('Files', stretch=False)
            self.tree_folders.heading('Files', text=get_name('files'))
            self.tree_folders.column('Nested folders', stretch=False)
            self.tree_folders.heading('Nested folders', text=get_name('nested_folders'))

            for ix, folder in enumerate(folders, start=1):
                self.tree_folders.insert('', 'end', ix, text=folder)
                self.tree_folders.set(ix, 'Files', len(next(os_walk(os_path.join(proj_path, folder)))[2]))
                self.tree_folders.set(ix, 'Nested folders', len(next(os_walk(os_path.join(proj_path, folder)))[1]))

        else:
            self.lbl_no_st_empty_prj = ttk.Label(master=self.frame_proj_stat, text=get_name("lbl_no_st_empty_prj"))

        self.frame_project.pack(fill=BOTH)
        self.frame_proj_info.grid(row=0, column=0, columnspan=4, sticky=W + E + N + S)
        self.lbl_proj_info.pack(fill=X)
        self.frame_proj_controls.grid(row=0, column=4, sticky=W + E + N + S)
        self.btn_analyze_photo.pack(fill=X)
        self.btn_edit.pack(fill=X)
        self.btn_close_proj.pack(fill=X)
        self.btn_delete_proj.pack(fill=X)
        self.btn_refresh.pack(fill=X)
        self.frame_proj_stat.grid(row=1, column=0, columnspan=5, sticky=W + E + N + S)
        if folders:
            self.tree_folders.pack()
        else:
            self.lbl_no_st_empty_prj.pack(fill=X)

    def analyze_photo_from_project(self, _=None):
        # TODO: show warning to user
        if self.win_photo_an:
            self.win_photo_an.destroy()

        try:
            # Create window from class and save pointer
            self.win_photo_an = WinPhotoAn(master=self.master,
                                           path=os_path.split(self.project_file)[0],
                                           project_keywords=self.project_dict["keywords"])

        # This exception will be raised if user chooses a project without photo
        except ValueError:
            messagebox.showerror(parent=self.master,
                                 title=get_name("title_error_no_photo_in_project"),
                                 message=get_name("text_error_no_photo_in_project"))
            return

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

    def delete_proj(self, _=None):
        if messagebox.askyesno(parent=self.master, title=get_name("ask_conf_del_proj_title"), message=get_name("ask_conf_del_proj_text")):
            delete_folder(path=os_path.split(self.project_file)[0])
            self.cmd_close_project()

    def refresh(self, _=None):
        self.project_selected()

    def cmd_open_project(self):
        fn = filedialog.askopenfilename(parent=self.master,
                                        title=get_name("ask_project_file"),
                                        filetypes=[(get_name("photo_projects"),
                                                    "*.json")],
                                        initialdir=settings["projects_dir"])
        if fn:
            self.project_file = fn
            self.project_selected()

    def cmd_close_project(self):
        self.project_dict = None
        self.project_file = None
        self.menu_project.entryconfig(1, state=DISABLED)
        if self.frame_project is not None:
            self.frame_project.destroy()
            self.frame_project = None
            self.create_frame_welcome()

    def cmd_settings(self, _=None):
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
        dir_with_photo = filedialog.askdirectory(parent=self.master, title=get_name("dia_save_photo"), initialdir='/')
        if not dir_with_photo:
            return

        # Regex to replace string.replace('-', ' ').replace('_', ' ')
        re_replace = re_compile("[-_]")
        # Get list of files to save
        photos_for_saving_with_date = {}
        photos_for_saving_without_date = []
        for root, _, files in os_walk(dir_with_photo):
            for file in files:
                if os_path.splitext(file)[-1].lower() in supported_image_ext:
                    possible_dt = ''
                    # Try to get date/time from filename
                    for name_part in re_replace.sub(os_path.splitext(file)[0], " ").split():
                        # Collect all numeric parts of filename
                        if name_part.isnumeric():
                            possible_dt = '{0}:{1}'.format(possible_dt, name_part)
                    try:
                        # Try to convert collected numeric parts into datetime object
                        dt = datetime.strptime(possible_dt, ':%Y:%m:%d:%H:%M:%S')
                    # If date/time were not found in filename
                    except ValueError:
                        try:
                            # Try to find date/time in metadata
                            possible_dt = et.get_data_from_image(os_path.join(root, file),
                                                                 "-EXIF:DateTimeOriginal")["EXIF"]["DateTimeOriginal"]
                            dt = datetime.strptime(possible_dt, '%Y:%m:%d %H:%M:%S')
                        # If date/time were not found in metadata too
                        except KeyError:
                            photos_for_saving_without_date.append(os_path.join(root, file))
                            continue
                    photos_for_saving_with_date[dt.strftime('%Y-%m-%d %H:%M:%S')] = [os_path.join(root, file), None]

        # Get max and min dates from files which are going to be saved
        sorted_photo_dt = sorted(photos_for_saving_with_date)
        min_date = datetime.strptime(sorted_photo_dt[0].split()[0], '%Y-%m-%d')
        max_date = datetime.strptime(sorted_photo_dt[-1].split()[0], '%Y-%m-%d')

        # Collect projects which are between min and max dates
        proposed_projects = []
        for d in listdir(settings["projects_dir"]):
            dates = str(d.split('_')[0])
            if len(dates) > 11:
                prj_start = datetime.strptime(dates[:10], '%Y-%m-%d')
                prj_finish = datetime.strptime(dates[11:], '%Y-%m-%d')
            else:
                prj_start = datetime.strptime(dates, '%Y-%m-%d')
                prj_finish = prj_start
            if prj_start >= min_date and prj_finish <= max_date:
                proposed_projects.append(os_path.join(settings["projects_dir"], d, project_file))

        # Connect photo and project basing on date/time
        for project in proposed_projects:
            with open(project, encoding='utf-8') as _f:
                pd = json_load(_f)

            # Parse project timeslot
            prj_start = '{0} {1}'.format(pd["timeslot"]["start"]["date"], pd["timeslot"]["start"]["time"])
            prj_start = datetime.strptime(prj_start, "%d.%m.%Y %H:%M")
            prj_finish = '{0} {1}'.format(pd["timeslot"]["finish"]["date"], pd["timeslot"]["finish"]["time"])
            prj_finish = datetime.strptime(prj_finish, "%d.%m.%Y %H:%M")

            for key in photos_for_saving_with_date:
                # Skip photo, if project is already assigned to this photo
                if photos_for_saving_with_date[key][1] is not None:
                    continue

                dt = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
                if prj_start <= dt <= prj_finish:  # If photo date/time in project timeslot
                    photos_for_saving_with_date[key][1] = os_path.split(project)[0]

    def cmd_analyse_photo(self):
        # If pointer is defined just switch focus to the window
        if self.win_photo_an:
            self.win_photo_an.focus_force()
            return

        # Create window from class and save pointer
        path = filedialog.askdirectory(title=get_name("ask_dir_photo_an"))
        if path:
            try:
                # Create window from class and save pointer
                self.win_photo_an = WinPhotoAn(master=self.master, path=path)

            # This exception will be raised if user chooses folder without photo
            # and rejects suggestion to choose another folder
            except ValueError:
                return

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

