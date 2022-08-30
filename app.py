try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

from startFrame import StartPage
from weaveFrame1 import WeaveFrame1
from calFrame import CalFrame
from weaveFrame2 import WeaveFrame2
from fileframe import FileFrame

class App(tk.Tk):

    def __init__(self, gui_args, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.bind("<Configure>", self.resize)
        self.num_motors = gui_args[0]
        self.pat_len2 = gui_args[2]
        self.num_frames = gui_args[3]

        # the container is where we'll stack a bunch of frames on top of each other,
        # then the one we want visible will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.page_names = []
        for F in (StartPage, CalFrame, WeaveFrame1, WeaveFrame2, FileFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            self.page_names.append(page_name)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        self.geometry(frame.geo)

    def resize(self, event):
        for page_name in self.page_names:
            resize_method = getattr(self.frames[page_name], "on_resize", None)
            if callable(resize_method):
                self.frames[page_name].on_resize()