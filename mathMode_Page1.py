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

mathMode_width   = 1000
mathMode_height  = 800


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
      
      #TODO: Set Minimum Page Dimensions
      #TODO: Make Product Matrix Static
      #TODO: Add Back & Continue Buttons
      #TODO: Second Math Page for Multiplication of Threading w/ Product Matrix

      #Placing Objects
      label.place(relx=0.5, rely=0.01, anchor=tk.CENTER)
      label_x.place(relx=0.35, rely=0.45, anchor=tk.W)
      label_equal.place(relx=0.625, rely=0.45, anchor=tk.W)
      
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
        
    def make_product_canvas(self):
      self.product_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                      width=(block_size + buffer) * self.controller.num_frames + buffer)
      self.product_text, self.product_rects = populate_matrix(self.product_canvas, self.rows,
                                                              self.controller.num_frames, tie_up_0_color, tie_up_1_color)
      self.product_matrix = np.zeros((self.rows, self.controller.num_frames), dtype=int)
      self.product_canvas.bind('<Button-1>',
                              lambda event, canvas=self.product_canvas, matrix=self.product_matrix,
                                    text=self.product_text, rects=self.product_rects:
                              self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))
      
      product_dim       = str(self.rows) + " x " + str(self.controller.num_frames) 
      label_product_dim = tk.Label(self, text=product_dim, font=self.controller.title_font) 
      
      self.product_canvas.place(relx=0.7, rely=0.1)
      label_product_dim.place(relx=0.7, rely=0.8)

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
      tieup_dim       = str(self.controller.num_pedals) + " x " + str(self.controller.num_frames) 
      label_tieup_dim = tk.Label(self, text=tieup_dim, font=self.controller.title_font) 

      self.tieup_canvas.place(relx=0.4, rely=0.25)
      label_tieup_dim.place(relx=0.4, rely=0.5)

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
      treadling_dim       = str(self.rows) + " x " + str(self.controller.num_pedals) 
      label_treading_dim  = tk.Label(self, text=treadling_dim, font=self.controller.title_font) 
      
      label_treading_dim.place(relx=0.05, rely=0.8)
      self.treadling_canvas.place(relx=0.05, rely=0.1)


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