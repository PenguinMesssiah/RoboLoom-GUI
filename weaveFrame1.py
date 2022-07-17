try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from serialCom import move_row

weave1_width = 800
weave1_height = 800
block_size = 25
buffer = 3

class WeaveFrame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(weave1_width) + "x" + str(weave1_height)

        label = tk.Label(self, text="Change the matrices", font=controller.title_font)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button_weave = tk.Button(self, text="Next row", command=self.weave_row)
        self.pattern_row = 0
        self.highlight = None

        #make and populate the canvases
        # Make a canvas for the pattern
        self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.pat_len2,
                                        width=(block_size + buffer) * self.controller.num_motors + buffer)
        self.pattern_text = populate_matrix(self.pattern_canvas, self.controller.pat_len2, self.controller.num_motors, "blue")
        self.pattern = np.zeros((self.controller.pat_len2, self.controller.num_motors), dtype=int)

        # Make a tie up matrix canvas
        self.threading_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                       width=(block_size + buffer) * self.controller.num_motors + buffer)
        self.threading_text = populate_matrix(self.threading_canvas, self.controller.num_frames, self.controller.num_motors, "green")
        self.threading = np.zeros((self.controller.num_frames, self.controller.num_motors), dtype=int)
        self.threading_canvas.bind('<Button-1>',
                                 lambda event, canvas=self.threading_canvas, matrix=self.threading,
                                        text = self.threading_text: self.onMatClick(canvas, matrix, text, event))


        # Make a frame canvas
        self.frame_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                      width=(block_size + buffer) * self.controller.num_frames + buffer)
        self.tie_up_text = populate_matrix(self.frame_canvas, self.controller.num_frames, self.controller.num_frames, "orange")
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_frames), dtype=int)
        self.frame_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.frame_canvas, matrix=self.tie_up,
                                          text=self.tie_up_text: self.onMatClick(canvas, matrix, text, event))

        # Make a treadling canvas
        self.treadling_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.pat_len2,
                                          width=(block_size + buffer) * self.controller.num_frames + buffer)
        self.treadling_text = populate_matrix(self.treadling_canvas, self.controller.pat_len2, self.controller.num_frames, "purple")
        self.treadling = np.zeros((self.controller.pat_len2, self.controller.num_frames), dtype=int)
        self.treadling_canvas.bind('<Button-1>',
                               lambda event, canvas=self.treadling_canvas, matrix=self.treadling,
                                      text=self.treadling_text: self.onMatClick(canvas, matrix, text, event))

        

        # Position things in frame
        self.threading_canvas.grid(row=1, column=1)
        self.pattern_canvas.grid(row=2, column=1)
        self.frame_canvas.grid(row=1, column=2)
        self.treadling_canvas.grid(row=2, column=2)
        button.grid(row=3, column=1, columnspan=2)
        label.grid(row=0, column=1, columnspan=2)
        button_weave.grid(row=2, column=0)

    def onMatClick(self, canvas, matrix, text, event):
        col = int(event.x / (block_size + buffer))
        row = int(event.y / (block_size + buffer))
        if (event.x <= ((col + 1) * (block_size + buffer) - buffer)) and \
                (event.y <= ((row + 1) * (block_size + buffer) - buffer)):
            matrix[row][col] = not matrix[row][col]
        x = col * block_size + (col + 1) * buffer
        y = row * block_size + (row + 1) * buffer
        canvas.delete(text[row][col])
        text[row][col] = canvas.create_text(x + block_size/2, y + block_size/2, text=str(matrix[row][col]),
                                            fill="black", font='Helvetica 15 bold')
        self.pattern = update_pattern(self.pattern_canvas, self.pattern_text, self.pattern, self.threading,
                                      self.tie_up, self.treadling)

    def weave_row(self):
        self.pattern_row += 1
        if self.pattern_row >= self.controller.pat_len2:
            self.pattern_row = 0
        self.pattern_canvas.delete(self.highlight)
        self.highlight = self.pattern_canvas.create_rectangle(buffer, self.pattern_row * (block_size + buffer),
                                                              self.controller.num_motors * (
                                                                          block_size + buffer) + buffer / 2,
                                                              (self.pattern_row - 1) * (
                                                                          block_size + buffer) + buffer,
                                                              width=buffer, outline="green")
        move_row(self.pattern[self.pattern_row - 1])

def populate_matrix(canvas, rows, cols, color):
    text = []
    for row in range(rows):
        text_row = []
        for column in range(cols):
            x = column * block_size + (column + 1) * buffer
            y = row * block_size + (row + 1) * buffer
            canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color)
            text_row.append(canvas.create_text(x + block_size/2, y + block_size/2, text="0", fill="black", font=('Helvetica 15 bold')))
        text.append(text_row)
    return text

def update_pattern(canvas, text, pattern, threading, tie_up, treadling):
    a = np.matmul(treadling, np.transpose(tie_up))
    pattern = np.matmul(a, threading)

    for i in range(np.shape(pattern)[0]):
        for j in range(np.shape(pattern)[1]):
            x = j * block_size + (j + 1) * buffer
            y = i * block_size + (i + 1) * buffer
            canvas.delete(text[i][j])
            text[i][j] = canvas.create_text(x + block_size/2, y + block_size/2, text=str(pattern[i][j]),
                                            fill="black", font='Helvetica 15 bold')
    return pattern