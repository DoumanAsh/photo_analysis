# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import json
import os
from PIL import Image, ImageTk
import image_tags
import geo_tags
import people_detection


def Quit(ev):
    global root
    root.destroy()

def LoadFile(ev):
    dirname = filedialog.askdirectory()
    print(dirname)
    '''
    fn = tkFileDialog.Open(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', open(fn, 'rt').read())
    '''

def SaveFile(ev):
    fn = ''
    #fn = tkFileDialog.SaveAs(root, filetypes = [('*.txt files', '.txt')]).show()
    t = Toplevel()
    t.title('win2')
    if fn == '':
        return
    elif not fn.endswith(".txt"):
        fn = ".".join(fn, "txt")

    with open(fn, 'wt') as fn_fd:
        fn_fd.write(textbox.get('1.0', 'end'))

if __name__ == "__main__":
    root = Tk()
    root.title('test')

    panelFrame = Frame(root, height = 60, bg = 'gray')
    textFrame = Frame(root, height = 340, width = 600)

    panelFrame.pack(side = 'top', fill = 'x')
    textFrame.pack(side = 'bottom', fill = 'both', expand = 1)

    textbox = Text(textFrame, font='Arial 14', wrap='word')
    scrollbar = Scrollbar(textFrame)

    scrollbar['command'] = textbox.yview
    textbox['yscrollcommand'] = scrollbar.set

    textbox.pack(side = 'left', fill = 'both', expand = 1)
    scrollbar.pack(side = 'right', fill = 'y')

    loadBtn = Button(panelFrame, text = 'Load')
    saveBtn = Button(panelFrame, text = 'Save')
    quitBtn = Button(panelFrame, text = 'Quit')

    loadBtn.bind("<Button-1>", LoadFile)
    saveBtn.bind("<Button-1>", SaveFile)
    quitBtn.bind("<Button-1>", Quit)

    loadBtn.place(x = 10, y = 10, width = 40, height = 40)
    saveBtn.place(x = 60, y = 10, width = 40, height = 40)
    quitBtn.place(x = 110, y = 10, width = 40, height = 40)

    root.mainloop()
