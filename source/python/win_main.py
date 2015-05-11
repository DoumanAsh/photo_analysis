# -*- coding: utf-8 -*-
# External modules
from shutil import rmtree as delete_folder
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


class SimpleMsg(Toplevel):
    def __init__(self, title='', message=''):
        bg = '#333'
        self.s = ttk.Style()
        self.s.configure('SimpleMsg.TLabelframe', padding=0)
        self.s.configure('SimpleMsg.TLabel', background='white')

        Toplevel.__init__(self, background=bg)
        self.geometry("+250+125")
        self.config(background=bg,
                    padx=2,
                    pady=2)
        self.focus_force()
        self.overrideredirect(True)
        self.frame = ttk.LabelFrame(master=self, text=title, style='SimpleMsg.TLabelframe')
        self.lbl = Text(master=self.frame,
                        bg='white',
                        font=("Cambria", 12),
                        borderwidth=0,
                        wrap=WORD,
                        height=len(message.splitlines()) + 4,
                        width=50)
        self.lbl.insert(1.0, message)
        self.lbl.tag_configure("center", justify='center')
        self.lbl.tag_add("center", 1.0, 8.0)
        self.lbl.configure(state="disabled", relief=FLAT)
        self.btn = ttk.Button(master=self.frame, text="Ok")
        self.btn.bind("<ButtonRelease-1>", lambda _: self.destroy())
        self.bind("<Escape>", lambda _: self.destroy())
        self.bind("<Return>", lambda _: self.destroy())
        self.bind("<FocusOut>", lambda _: self.focus_force())
        self.frame.pack(fill=BOTH)
        self.lbl.pack(fill=BOTH)
        self.btn.pack()


class WinMain():
    def __init__(self, master=None):
        self.master = master

        self.master.bind('<Control-o>', lambda _: self.cmd_open_project())
        self.master.bind('<Control-q>', lambda _: self.cmd_close_project())
        self.master.bind('<Control-n>', lambda _: self.cmd_create_project())
        self.master.bind('<Control-v>', lambda _: self.cmd_view_proj())
        self.master.bind('<Control-c>', lambda _: self.cmd_settings())
        self.master.bind('<Control-s>', lambda _: self.cmd_save_photo())
        self.master.bind('<Control-a>', lambda _: self.cmd_analyse_photo())
        self.master.bind('<F1>', lambda _: self.cmd_help())
        self.master.bind('<Escape>', lambda _: self.master.destroy())

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
        self.menu_project.add_command(label=get_name("cmd_exit"), command=self.master.destroy)

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

        self.btn_open_proj = ttk.Button(master=self.frame_default_controls, text=get_name("btn_open_project"))
        self.btn_create_proj = ttk.Button(master=self.frame_default_controls, text=get_name("btn_create_project"))
        self.btn_view_proj = ttk.Button(master=self.frame_default_controls, text=get_name("btn_view_proj"))
        self.btn_save_photo = ttk.Button(master=self.frame_default_controls, text=get_name("btn_save_photo"))
        self.btn_analyse_photo = ttk.Button(master=self.frame_default_controls, text=get_name("btn_analyse_photo"))

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
            # Prepare table with statistics about folders and files
            # ----------------------------------------------------------------------------------------------------------
            self.tree_folders = ttk.Treeview(master=self.frame_proj_stat,
                                             columns=('files', 'nested_folders'),
                                             height=len(folders),
                                             selectmode=NONE)
            self.tree_folders.column('#0', stretch=False, width=145)
            self.tree_folders.heading('#0', text=get_name('folder'))
            self.tree_folders.column('files', stretch=False, width=145)
            self.tree_folders.heading('files', text=get_name('files'))
            self.tree_folders.column('nested_folders', stretch=False, width=190)
            self.tree_folders.heading('nested_folders', text=get_name('nested_folders'))

            for ix, folder in enumerate(folders, start=1):
                self.tree_folders.insert('', 'end', ix, text=folder)
                self.tree_folders.set(ix, 'files', len(next(os_walk(os_path.join(proj_path, folder)))[2]))
                self.tree_folders.set(ix, 'nested_folders', len(next(os_walk(os_path.join(proj_path, folder)))[1]))
            # ==========================================================================================================

            # Prepare table with statistics about photographs basing on source photographs
            # ----------------------------------------------------------------------------------------------------------
            self.tree_source = ttk.Treeview(master=self.frame_proj_stat,
                                            height=10,
                                            selectmode=NONE,
                                            columns=("xmp", "fullsize", "monitor", "web", "panorama", "layered"))

            self.scroll_tree_y = ttk.Scrollbar(master=self.frame_proj_stat, orient='vertical', command=self.tree_source.yview)
            self.tree_source.configure(yscroll=self.scroll_tree_y.set)

            source_files = []
            xmp_files = []
            xmp_files_num = 0
            fs_files_num = 0
            mon_files_num = 0
            web_files_num = 0
            pan_files_num = 0
            layered_files_num = 0

            for file in next(os_walk((os_path.join(proj_path, dir_source))))[2]:
                if os_path.splitext(file)[-1].lower() in supported_image_ext:
                    source_files.append(file)
                if os_path.splitext(file)[-1].lower() == xmp_ext:
                    xmp_files.append(file)

            for source_file in source_files:
                fn_without_ext = os_path.splitext(source_file)[0]
                self.tree_source.insert('', 'end', fn_without_ext, text=source_file)
                for file in xmp_files:
                    if os_path.splitext(file)[0] == fn_without_ext:
                        xmp_files_num += 1
                        self.tree_source.set(fn_without_ext, 'xmp', '+')
                        break

                if os_path.isdir(os_path.join(proj_path, dir_fullsize)):
                    for file in next(os_walk((os_path.join(proj_path, dir_fullsize))))[2]:
                        found_matching = dt_in_fn_regex.match(file)
                        if found_matching and found_matching.group(1) == fn_without_ext:
                            fs_files_num += 1
                            self.tree_source.set(fn_without_ext, 'fullsize', '+')
                            break

                if os_path.isdir(os_path.join(proj_path, dir_monitor)):
                    for file in next(os_walk((os_path.join(proj_path, dir_monitor))))[2]:
                        found_matching = dt_in_fn_regex.match(file)
                        if found_matching and found_matching.group(1) == fn_without_ext:
                            mon_files_num += 1
                            self.tree_source.set(fn_without_ext, 'monitor', '+')
                            break

                if os_path.isdir(os_path.join(proj_path, dir_web)):
                    for file in next(os_walk((os_path.join(proj_path, dir_web))))[2]:
                        found_matching = dt_in_fn_regex.match(file)
                        if found_matching and found_matching.group(1) == fn_without_ext:
                            web_files_num += 1
                            self.tree_source.set(fn_without_ext, 'web', '+')
                            break

                if os_path.isdir(os_path.join(proj_path, dir_panorama)):
                    for file in next(os_walk((os_path.join(proj_path, dir_panorama))))[2]:
                        found_matching = dt_in_fn_regex.match(file)
                        if found_matching and found_matching.group(1) == fn_without_ext:
                            pan_files_num += 1
                            self.tree_source.set(fn_without_ext, 'panorama', '+')
                            break

                if os_path.isdir(os_path.join(proj_path, dir_layered)):
                    for file in next(os_walk((os_path.join(proj_path, dir_layered))))[2]:
                        found_matching = dt_in_fn_regex.match(file)
                        if found_matching and found_matching.group(1) == fn_without_ext:
                            layered_files_num += 1
                            self.tree_source.set(fn_without_ext, 'layered', '+')
                            break

            text = """{13}
({14} - {0}):
{15}\t\t{16}\t{17}
XMP:\t\t{1}\t\t\t{2}%
Fullsize:\t\t{3}\t\t\t{4}%
Monitor:\t\t{5}\t\t\t{6}%
Web:\t\t{7}\t\t\t{8}%
Panorama:\t{9}\t\t\t{10}%
Layered:\t\t{11}\t\t\t{12}%""".format(len(source_files),
                                      xmp_files_num,
                                      int(xmp_files_num / len(source_files) * 100),
                                      fs_files_num,
                                      int(fs_files_num / len(source_files) * 100),
                                      mon_files_num,
                                      int(mon_files_num / len(source_files) * 100),
                                      web_files_num,
                                      int(web_files_num / len(source_files) * 100),
                                      pan_files_num,
                                      int(pan_files_num / len(source_files) * 100),
                                      layered_files_num,
                                      int(layered_files_num / len(source_files) * 100),
                                      get_name("stat_of_edited"),
                                      get_name("source_files"),
                                      get_name("type"),
                                      get_name("num_of_files"),
                                      get_name("percent_from_source"))

            self.lbl_source_stat = ttk.Label(master=self.frame_proj_stat, text=text)

            self.tree_source.heading('#0', text='Source')
            self.tree_source.heading('xmp', text='XMP')
            self.tree_source.heading('fullsize', text='FS')
            self.tree_source.heading('monitor', text='Mon')
            self.tree_source.heading('web', text='Web')
            self.tree_source.heading('panorama', text='Pan')
            self.tree_source.heading('layered', text='Lrd')

            self.tree_source.column('#0', stretch=False, width=170)
            self.tree_source.column('xmp', stretch=False, width=50)
            self.tree_source.column('fullsize', stretch=False, width=50)
            self.tree_source.column('monitor', stretch=False, width=50)
            self.tree_source.column('web', stretch=False, width=50)
            self.tree_source.column('panorama', stretch=False, width=50)
            self.tree_source.column('layered', stretch=False, width=50)

        else:
            self.lbl_no_st_empty_prj = ttk.Label(master=self.frame_proj_stat, text=get_name("lbl_no_st_empty_prj"))

        self.frame_project.pack(fill=BOTH)
        self.frame_proj_info.grid(row=0, column=0, sticky=W + E + N + S)
        self.lbl_proj_info.pack(fill=X)
        self.frame_proj_controls.grid(row=1, column=0, sticky=W + E + N + S)
        self.btn_analyze_photo.pack(fill=X)
        self.btn_edit.pack(fill=X)
        self.btn_close_proj.pack(fill=X)
        self.btn_delete_proj.pack(fill=X)
        self.btn_refresh.pack(fill=X)
        self.frame_proj_stat.grid(row=0, column=1, rowspan=2, sticky=W + E + N + S)
        if folders:
            self.tree_folders.pack()
            self.lbl_source_stat.pack(fill=X)
            self.tree_source.pack(side=LEFT)
            self.scroll_tree_y.pack(side=RIGHT, fill=Y, expand=1)
        else:
            self.lbl_no_st_empty_prj.pack(fill=X)

    @staticmethod
    def get_numeric_parts_of_fn(filename):

        found_match = regex.match(filename)
        if found_match:
            print(found_match.group(1))
        exit(0)
        print(regex.match(filename).groups())
        print(regex.search(filename))
        numeric_parts = []
        print(os_path.splitext(filename)[0])
        normalized_fn = regex.sub(os_path.splitext(filename)[0], " ")
        # Try to get date/time from filename
        for name_part in normalized_fn.split():
            # Collect all numeric parts of filename
            if name_part.isnumeric():
                numeric_parts.append(name_part)
        return numeric_parts

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

        # Get list of files to save
        photos_for_saving_with_date = {}
        photos_for_saving_without_date = []
        for root, _, files in os_walk(dir_with_photo):
            for file in files:
                if os_path.splitext(file)[-1].lower() in supported_image_ext:
                    try:
                        found_matching = dt_in_fn_regex.match(file)
                        if found_matching:
                            # Convert collected numeric parts into datetime object
                            dt = datetime.strptime(str(found_matching), '%Y-%m-%d_%H-%M-%S')
                        else:
                            raise ValueError
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
        #messagebox.showinfo(get_name("win_about"), get_name("text_about"))
        SimpleMsg(title=get_name("win_about"), message=get_name("text_about"))
