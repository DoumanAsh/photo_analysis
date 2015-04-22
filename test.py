# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
import json
import os
from PIL import Image, ImageTk
import image_tags
import geo_tags
import people_detection


class CanvasWithImage(Canvas):
    def __init__(self, master=None, image=None, side=0):
        Canvas.__init__(self, master, height=side, width=side, bg='#222222')
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


def format_image_tags(tags):
    line = ''
    if len(tags) == 0:
        return 'not found'
    for tag in sorted(tags.keys()):
        if tag == 'keywords':
            continue
        line += '{0}: {1}\n'.format(tag, tags[tag])
    if 'keywords' in tags.keys() and len(tags['keywords']) > 0:
        line += 'Keywords:\n'
        for kw in tags['keywords']:
            line += kw
            line += '\n'
    return line


def go_to_next_img(event):
    global img_frame
    global geo_label
    global current_img

    x, y = event.x, event.y
    if x > img_frame.width / 2:
        current_img += 1
    else:
        current_img -= 1

    if current_img >= len(images):
        current_img = 0
    if current_img < 0:
        current_img = len(images) - 1

    image_full_path = os.path.join(path, images[current_img])
    img_frame.config(image=image_full_path)

    geo_label['text'] = ''
    pd_label['text'] = ''
    if check_geo_value.get():
        geo_label['text'] = 'Loading geo-info...Please wait'
        root.update()
        formatted_tags = format_image_tags(geo_tags.get_geo_tags_in_et_format(image_full_path))
        geo_label['text'] = 'Geo-info\n' \
                            '----------------\n' \
                            '{0}\n' \
                            '================\n\n'.format(formatted_tags)
    if check_pd_value.get():
        pd_label['text'] = 'Loading people detection info...Please wait'
        root.update()
        kw = people_detection.get_keywords(image_full_path)
        if len(kw) == 0:
            kw = ['not found']
        pd_label['text'] = 'People detection keywords\n' \
                           '----------------\n' \
                           '{0}\n' \
                           '================\n\n'.format('\n'.join(kw))

path = os.path.abspath('images')
images = os.listdir(path)
current_img = 0

root = Tk()

img_frame = CanvasWithImage(image=os.path.join(path, images[current_img]), side=500)
img_frame.bind('<Button-1>', go_to_next_img)
img_frame.pack(fill='both', side='left')

frame = Frame(root)
frame.pack(side='left', fill='both', expand=1)

check_geo_value = IntVar()
check_geo = Checkbutton(frame, text='Geo-info', variable=check_geo_value)
check_geo.pack(side='bottom')
check_pd_value = IntVar()
check_pd = Checkbutton(frame, text='People detection', variable=check_pd_value)
check_pd.pack(side='bottom')

geo_label = Label(frame, width=70, text='Geo-info: Initial test text')
geo_label.pack(fill='both')
pd_label = Label(frame, width=70, text='People detection info: Initial test text')
pd_label.pack(fill='both')
s = Style()
s.theme_use('clam')

# Tree
# -----------------------
'''
with open('json/osm_types_and_classes.json', encoding='utf-8') as f:
    osm_types_and_classes = json.load(f)
def test(t):
    print(tree.selection())
    print('O-ya-ya ' + str(t))
    path2 = 'D:/_test/control_set_01_02_positive/2014-08-04_13-11-51.jpg'
    img2 = ImageTk.PhotoImage(Image.open(path2))
    panel.config(image=img2)
    panel.image = img2
    pass
tree = Treeview(root, columns='keywords')
tree.heading('keywords', text='keywords')
tree.heading('#0', text='Types and classes')
for osm_type in list(sorted(osm_types_and_classes.keys())):
    tree.insert('', 'end', osm_type, text=osm_type)
    for osm_class in list(sorted(osm_types_and_classes[osm_type].keys())):
        tree.insert(osm_type, 'end', osm_class, text=osm_class)
        tree.set(osm_class, 'keywords', str(', '.join(osm_types_and_classes[osm_type][osm_class])))

tree.bind('<Double-Button-1>', test)
tree.pack()
'''
# ------------------------


root.mainloop()
