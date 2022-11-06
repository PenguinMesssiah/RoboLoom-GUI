import numpy as np
from serialCom import move_row, move_frame

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

start_width = 500
start_height = 500

class ResetFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(start_width) + "x" + str(start_height)

        label = tk.Label(self, text="Reset RoboLoom", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Move all motors down", command=lambda: self.all_down())

        button1.pack()

    def all_down(self):
        move_row(np.zeros((self.controller.num_motors)))
        move_frame(np.zeros((self.controller.num_frames), dtype='int'))
