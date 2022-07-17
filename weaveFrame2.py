try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from serialCom import move_row

weave2_width = 1600
weave2_height = 800
block_size = 20
buffer = 3

class WeaveFrame2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(weave2_width) + "x" + str(weave2_height)

        label = tk.Label(self, text="Draw your pattern", font=controller.title_font)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button_weave = tk.Button(self, text="Next row", command=self.weave_row)
        self.pattern_row = 0
        self.highlight = None

        # Make a canvas for the pattern
        self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer)* self.controller.pat_len2,
                                        width=(block_size + buffer)* self.controller.num_motors+buffer)
        self.pattern_canvas.bind('<Button-1>', self.onPatternClick)
        populate_matrix(self.pattern_canvas, self.controller.pat_len2, self.controller.num_motors, "blue")
        self.pattern = np.zeros((self.controller.pat_len2, self.controller.num_motors))

        # Make a tie up matrix canvas
        self.tie_up_canvas = tk.Canvas(self, height=(block_size + buffer)* self.controller.num_frames,
                                        width=(block_size + buffer)* self.controller.num_motors+buffer)
        populate_matrix(self.tie_up_canvas, self.controller.num_frames, self.controller.num_motors, "green")

        # Make a frame canvas
        self.frame_canvas = tk.Canvas(self, height=(block_size + buffer)* self.controller.num_frames,
                                       width=(block_size + buffer)* self.controller.num_frames+buffer)
        populate_matrix(self.frame_canvas, self.controller.num_frames, self.controller.num_frames, "orange")

        # Make a treadling canvas
        self.treadling_canvas = tk.Canvas(self, height=(block_size + buffer)* self.controller.pat_len2,
                                      width=(block_size + buffer)* self.controller.num_frames+buffer)
        populate_matrix(self.treadling_canvas, self.controller.pat_len2, self.controller.num_frames, "purple")

        #Position everything on screen
        self.tie_up_canvas.grid(row=1, column=1)
        self.pattern_canvas.grid(row=2, column=1)
        self.frame_canvas.grid(row=1, column=2)
        self.treadling_canvas.grid(row=2, column=2)
        button.grid(row=3, column =1, columnspan=2)
        label.grid(row=0, column=1, columnspan=2)
        button_weave.grid(row=2, column=0)

    def weave_row(self):
        self.pattern_row += 1
        if self.pattern_row >= self.controller.pat_len2:
            self.pattern_row = 0
        self.pattern_canvas.delete(self.highlight)
        self.highlight = self.pattern_canvas.create_rectangle(buffer, self.pattern_row * (block_size + buffer),
                                             self.controller.num_motors * (block_size + buffer) + buffer/2,
                                             (self.pattern_row-1) * (block_size + buffer)+buffer,
                                             width=buffer, outline="green")
        move_row(self.pattern[self.pattern_row-1])


    def onPatternClick(self, event=None):
        col = int(event.x / (block_size + buffer))
        row = int(event.y / (block_size + buffer))
        if (event.x <= ((col + 1) * (block_size + buffer) - buffer)) and \
                (event.y <= ((row + 1) * (block_size + buffer) - buffer)):
            self.pattern[row][col] = not self.pattern[row][col]
        fill = "blue"
        if self.pattern[row][col]:
            fill = "red"
        x = col * block_size + (col + 1) * buffer
        y = row * block_size + (row + 1) * buffer
        self.pattern_canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=fill)

def populate_matrix(canvas, rows, cols, color):
    for row in range(rows):
        for column in range(cols):
            x = column * block_size + (column + 1) * buffer
            y = row * block_size + (row + 1) * buffer
            canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color)