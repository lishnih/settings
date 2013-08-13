#!/usr/bin/env python
# coding=utf-8
# Stan 2013-05-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )
from lib.backwardcompat import *

try:
    from .lib.info import (__pkgname__, __description__, __version__)
    from .lib.dump import plain
    from .lib.settings import Settings
    from .lib.tkprop import propertyDialog
except:
    from lib.info import (__pkgname__, __description__, __version__)
    from lib.dump import plain
    from lib.settings import Settings
    from lib.tkprop import propertyDialog

import sys, os, logging


class AppUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("tkSettings")

        ### Menu ###

        self.menubar = tk.Menu(self)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(command=self.onLoadDefault, label="Load default")
        menu.add_command(command=self.onLoadFile, label="Load file")
        menu.add_separator()
        menu.add_command(command=self.quit, label="Exit")

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=menu)
        menu.add_command(command=self.onAbout, label="About")

        self.config(menu=self.menubar)

        ### Widgets ###

        # Frame with Buttons
        self.frame1 = tk.Frame(self)
        button1 = tk.Button(self.frame1, text="Settings")
        button1.pack()
        button1.bind("<Button-1>", self.onShowSettings)
        button2 = tk.Button(self.frame1, text="Save test data")
        button2.pack()
        button2.bind("<Button-1>", self.onSaveTestData)

        # Text Widget
        dFont1 = Font(family="Courier", size=9)
        self.text1 = tk.Text(self, font=dFont1)
        self.text1_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text1.yview)
        self.text1['yscrollcommand'] = self.text1_y.set
    
        # Status Widget
        self.status = tk.StringVar()
        label1 = tk.Label(self, textvariable=self.status, anchor=tk.W)
        self.setStatus()

        ### Grid widgets ###

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=120)
        self.grid_columnconfigure(1, weight=3, minsize=400)
        self.grid_columnconfigure(2)

        self.frame1.grid(row=0, column=0, sticky='nwes')
        self.text1.grid(row=0, column=1, sticky='nwes')
        self.text1_y.grid(row=0, column=2, sticky='nwes')
    
        self.grid_rowconfigure(1)
        label1.grid(row=1, column=0, columnspan=4, sticky='nwes')

        ### Initial ###

        self.onLoadDefault()

    def appendText(self, text=""):
        self.text1.insert(tk.INSERT, "{0}\n".format(plain(text)))

    def setText(self, text=""):
        self.text1.delete(1.0, tk.END)
        self.appendText(text)

    def setStatus(self, text=""):
        status = sys.executable
        if text:
            status += " :: " + text
        self.status.set(status)

    def showInfo(self):
        self.setText("System:")
        self.appendText(self.s.get_systems())
        self.appendText("Settings:")
        self.appendText(self.s.get_dict())
        self.setStatus(self.s.get_filename())

    ### From menu ###

    def onAbout(self):
        text = """tkSettings\nas part of\n{0}, version {1}\n{2}\n
Package: {3}
Python: {4}""".format(__pkgname__, __version__, __description__, __package__,
                      sys.version)
        showinfo("About", text)

    def onLoadDefault(self):
        self.s = Settings()
        self.showInfo()

    def onLoadFile(self):
        initialdir = os.path.expanduser("~")
        filename = askopenfilename(initialdir=initialdir, filetypes=[
                       ('Config files', '*.pickle'),
                       ('All files', '*.*'),
                   ])
        if filename:
            self.s = Settings(filename=filename)
            self.showInfo()

    ### From buttons ###

    def onShowSettings(self, event):
        propertyDialog(self.s.get_dict())
    
    def onSaveTestData(self, event):
        self.s.saveEnv()
        self.s.set_path('test_instance', '$')
        self.s.set_path('test_home',     '~')
        self.s.set_path('test_location', '~~',  True)
        self.s.set_path('test_app',      '~~~', True)
        self.showInfo()


def main():
    root = AppUI()
    root.update_idletasks()
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
    root.mainloop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
