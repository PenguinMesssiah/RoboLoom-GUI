try:
    import tkinter as tk  # python 3
    from tkinter import ttk # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from constants import *
from serialCom import move_frame, init_frames

mathMode_width   = 1400
mathMode_height  = 1000


class MathMode_Page1(tk.Frame):

    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      self.parent     = parent
      self.geo        = str(mathMode_width) + "x" + str(mathMode_height)

      # Make this changeable later?
      self.rows    = 25
      self.columns = 20 

      #Create Labels
      label       = tk.Label(self, text="Interactive Math Mode", font=controller.title_font)
      label_x     = tk.Label(self, text="X", font=controller.title_font)
      label_equal = tk.Label(self, text="=", font=controller.title_font)

      self.pat_row   = 0
      self.highlight = None

      # make and populate the canvases
      # Make a canvas for the pattern
      self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                      width=(block_size + buffer) * self.controller.num_motors + buffer)
      self.pattern_text, self.pattern_rects = populate_matrix(self.pattern_canvas, self.rows,
                                          self.controller.num_motors, pattern_0_color, pattern_1_color)
      self.pattern = np.zeros((self.rows, self.controller.num_motors), dtype=int)

      # Make a treadling canvas
      self.make_treadling_canvas()
      
      # Make a tieup canvas
      self.make_tieup_canvas()

      #TODO: Create method: self.make_intermediate_canvas()
      #TODO: Second Math Page for Multiplication of Threading w/ Intermediate Matrix
      
      # Make a threading matrix canvas
      #self.make_threading_canvas()

      #Make the intermediate matrix

      #Placing Objects
      label.place(relx=0.5, rely=0.01, anchor=tk.CENTER)
      label_x.place(relx=0.175, rely=0.3)
      label_equal.place(relx=0.4, rely=0.3)

      self.treadling_canvas.place(relx=0.05, rely=0.025)
      self.tieup_canvas.place(relx=0.25, rely=0.25)

      self.threading_canvas.place(relx=0.05, rely=0.6)
      #self.pattern_canvas.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

    def onMatClick(self, canvas, matrix, text, event, color0, color1, rects):
        col = int(event.x / (block_size + buffer))
        row = int(event.y / (block_size + buffer))
        if (event.x <= ((col + 1) * (block_size + buffer) - buffer)) and \
                (event.y <= ((row + 1) * (block_size + buffer) - buffer)):
            matrix[row][col] = not matrix[row][col]
        x = col * block_size + (col + 1) * buffer
        y = row * block_size + (row + 1) * buffer
        if matrix[row][col] == 1:
            text_color = color0
            back_color = color1
        else:
            text_color = color1
            back_color = color0
        canvas.delete(rects[row][col])
        rects[row][col] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color)
        canvas.delete(text[row][col])
        text[row][col] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(matrix[row][col]),
                                            fill=text_color, font='Helvetica 15')
        self.pattern = update_pattern(self.pattern_canvas, self.pattern_text, self.pattern, self.threading,
                                      self.tie_up, self.treadling, self.pattern_rects)

    def make_threading_canvas(self):
        self.threading_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                          width=(block_size + buffer) * self.controller.num_motors + buffer)
        self.threading_text, self.threading_rects = populate_matrix(self.threading_canvas, self.controller.num_frames,
                                                                    self.controller.num_motors, threading_0_color,
                                                                    threading_1_color)
        self.threading = np.zeros((self.controller.num_frames, self.controller.num_motors), dtype=int)
        self.threading_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.threading_canvas, matrix=self.threading,
                                          text=self.threading_text, rects=self.threading_rects:
                                   self.onMatClick(canvas, matrix, text, event, threading_0_color,
                                                   threading_1_color, rects))

    def make_tieup_canvas(self):
        self.tieup_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                      width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                              self.controller.num_pedals, tie_up_0_color,
                                                              tie_up_1_color)
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)
        self.tieup_canvas.bind('<Button-1>',
                               lambda event, canvas=self.tieup_canvas, matrix=self.tie_up,
                                      text=self.tie_up_text, rects=self.tie_up_rects:
                               self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))

    def make_treadling_canvas(self):
        self.treadling_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                          width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.treadling_text, self.treadling_rects = populate_matrix(self.treadling_canvas, self.rows,
                                                                    self.controller.num_pedals, treadling_0_color,
                                                                    treadling_1_color)
        self.treadling = np.zeros((self.rows, self.controller.num_pedals), dtype=int)
        self.treadling_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.treadling_canvas, matrix=self.treadling,
                                          text=self.treadling_text, rects=self.treadling_rects:
                                   self.onMatClick(canvas, matrix, text, event, treadling_0_color,
                                                   treadling_1_color, rects))

def populate_matrix(canvas, rows, cols, color_background, color_text):
    text = []
    rects = []
    for row in range(rows):
        text_row = []
        rects_row = []
        for column in range(cols):
            x = column * block_size + (column + 1) * buffer
            y = row * block_size + (row + 1) * buffer
            rects_row.append(canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color_background))
            text_row.append(canvas.create_text(x + block_size / 2, y + block_size / 2, text="0", fill=color_text,
                                               font=('Helvetica 15')))
        text.append(text_row)
        rects.append(rects_row)
    return text, rects


def update_pattern(canvas, text, pattern, threading, tie_up, treadling, rects):
    a = np.matmul(treadling, np.transpose(tie_up))
    pattern = np.matmul(a, threading)

    for i in range(np.shape(pattern)[0]):
        for j in range(np.shape(pattern)[1]):
            x = j * block_size + (j + 1) * buffer
            y = i * block_size + (i + 1) * buffer
            canvas.delete(text[i][j])
            canvas.delete((rects[i][j]))
            if pattern[i][j] == 1:
                text_color = pattern_0_color
                back_color = pattern_1_color
            else:
                text_color = pattern_1_color
                back_color = pattern_0_color
            rects[i][j] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color)
            text[i][j] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(pattern[i][j]),
                                            fill=text_color, font='Helvetica 15')
    return pattern