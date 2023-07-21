import numpy as np
from serialCom import move_row, move_frame

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
import serial
from PIL import Image

start_width = 500
start_height = 500
pico = None

selvedge = [[0,1],[1,0]]
idx = 0

# dictionary of list of the repeat of 12 for each pattern
patterns = {
    "plain": [[0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0]],
    "twill":[[1,0,0,0,1,0,0,0,1,0,0,0],
    [0,1,0,0,0,1,0,0,0,1,0,0],
    [0,0,1,0,0,0,1,0,0,0,1,0],
    [0,0,0,1,0,0,0,1,0,0,0,1]],
    "basket":[[1,1,0,0,1,1,0,0,1,1,0,0],
    [1,1,0,0,1,1,0,0,1,1,0,0],
    [0,0,1,1,0,0,1,1,0,0,1,1],
    [0,0,1,1,0,0,1,1,0,0,1,1]],
    "waffle":[[0,0,1,0,0,0,0,0,1,0,0,0],
    [0,1,0,1,0,0,0,1,0,1,0,0],
    [1,0,1,0,1,0,1,0,1,0,1,0],
    [0,1,1,1,0,1,0,1,1,1,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0],
    [0,1,0,1,0,0,0,1,0,1,0,0]]
}

current = None #what is the current pattern being worked on
plain_idx = 0 #what line it is on in the pattern. Should reset with new pattern
twill_idx = 0
basket_idx = 0
waffle_idx = 0

reset_row = np.tile([0, 0], 20)

class ButtonBoxFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(start_width) + "x" + str(start_height)

        label = tk.Label(self, text="Weave with the Cash Register", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.pico = serial.Serial(port="COM4", baudrate=115200, timeout=.1)

        data_pico = ""
        if pico == None:
            return
        while pico.in_waiting:
            data_pico += str(pico.readline())
        if data_pico != "":
            print(data_pico)
        if "plain" in data_pico:
            # if current != "plain":
            #     pattern_idx = 0

            pattern_row = patterns["plain"][plain_idx]
            full_row = selvedge[self.idx] + (pattern_row * 3) + selvedge[self.idx]
            Image.fromarray(np.asarray(full_row)).show()
            move_row(full_row)

            # update index
            self.plain_idx = (self.plain_idx + 1) % 2
            #  update for the next selvedge choice
            self.idx = (self.idx + 1) % 2

        elif "twill" in data_pico:
            # if current != "twill":
            #     pattern_idx = 0

            pattern_row = patterns["twill"][self.twill_idx]
            full_row = selvedge[self.idx] + (pattern_row * 3) + selvedge[self.idx]
            move_row(full_row)

            # update index
            self.twill_idx = (self.twill_idx + 1) % 4
            #  update for the next selvedge choice
            self.idx = (self.idx + 1) % 2

        elif "basket" in data_pico:
            # if current != "basket":
            #     pattern_idx = 0

            pattern_row = patterns["basket"][self.basket_idx]
            full_row = selvedge[self.idx] + (pattern_row * 3) + selvedge[self.idx]
            move_row(full_row)

            # update index
            self.basket_idx = (self.basket_idx + 1) % 4
            #  update for the next selvedge choice
            self.idx = (self.idx + 1) % 2

        elif "waffle" in data_pico:
            if current != "waffle":
                pattern_idx = 0

            pattern_row = patterns["waffle"][self.waffle_idx]
            full_row = selvedge[self.idx] + (pattern_row * 3) + selvedge[self.idx]
            move_row(full_row)

            # update index
            self.waffle_idx = (self.waffle_idx + 1) % 8
            #  update for the next selvedge choice
            self.idx = (self.idx + 1) % 2

        elif "reset" in data_pico:
            # reset indices and heddles
            self.plain_idx = 0
            self.twill_idx = 0
            self.basket_idx = 0
            self.waffle_idx = 0
            move_row(reset_row)