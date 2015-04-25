from tkinter import ttk
from tkinter import *
import json
root = Tk()
with open('json/osm_types_and_classes.json', encoding='utf-8') as f:
    osm_types_and_classes = json.load(f)
def test(t):
    print(tree.focus())
    print(tree.parent(tree.focus()))
    print('O-ya-ya ' + str(t))
    pass
tree = ttk.Treeview(root, columns='keywords')
tree.heading('keywords', text='keywords')
tree.heading('#0', text='Types and classes')
for osm_type in list(sorted(osm_types_and_classes.keys())):
    tree.insert('', 'end', osm_type, text=osm_type)
    tree.set(osm_type, 'keywords', "test")
    for osm_class in list(sorted(osm_types_and_classes[osm_type].keys())):
        tree.insert(osm_type, 'end', osm_class, text=osm_class)
        #tree.set(osm_class, 'keywords', str(', '.join(osm_types_and_classes[osm_type][osm_class])))

tree.bind('<Double-Button-1>', lambda t: tree.focus())
tree.pack()
root.mainloop()
