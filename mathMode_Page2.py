try:
    import tkinter as tk  # python 3
    from tkinter import ttk # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from constants import *

mathMode_width   = 1400
mathMode_height  = 800


class MathMode_Page2(tk.Frame):

    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      self.parent     = parent
      self.geo        = str(mathMode_width) + "x" + str(mathMode_height)

      # Make this changeable later?
      self.rows    = 25
      self.columns = 20 

      #Create Labels & buttons
      label       = tk.Label(self, text="Interactive Math Mode", font=controller.title_font)
      label_x     = tk.Label(self, text="X", font=controller.title_font)
      label_equal = tk.Label(self, text="=", font=controller.title_font)

      button_back     = tk.Button(self, text="Return", command=lambda: controller.show_frame("WeaveFrame1"))
      #button_continue = tk.Button(self, text="Continue", command=lambda: controller.show_frame("StartPage"))

      self.pat_row   = 0
      self.highlight = None
      
      #TODO: Set Minimum Page Dimensions
      #TODO: Add Back & Continue Buttons
      #TODO: Collision of Objects Checks Needed

      #Placing Objects
      label.place(relx=0.5, rely=0.01, anchor=tk.CENTER)
      label_x.place(relx=0.175, rely=0.15, anchor=tk.W)
      label_equal.place(relx=0.85, rely=0.15, anchor=tk.E)
      button_back.place(relx=0.7, rely= 0.01)
    
    def init_page(self):
      self.pattern = np.zeros((self.rows, self.controller.num_motors), dtype=int)
      self.make_threading_canvas()
      self.make_product_canvas()
      self.make_pattern_canvas()

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
      self.pattern = update_pattern(self.product_canvas, self.product_text, self.pattern,
                                    self.tie_upT, self.treadling, self.product_rects)
        
    def make_product_canvas(self):
      #Get First Math Mode Frame
      mathMode_frame     = self.controller.get_page("MathMode_Page1")
      old_product_canvas = mathMode_frame.product_canvas
      old_product_matrix = mathMode_frame.product_matrix
      
      dynamic_y = (block_size + buffer) * self.rows
      self.product_canvas = tk.Canvas(self, height=dynamic_y, width=(block_size + buffer) * self.controller.num_frames + buffer)
      self.product_text, self.product_rects = populate_matrix(self.product_canvas, self.rows,
                                                              self.controller.num_frames, product_0_color, product_1_color)
      update_newCanvas_wOldCanvas(old_product_canvas, self.product_canvas)
      self.product_matrix = old_product_matrix
      """
      self.product_canvas.bind('<Button-1>',
                              lambda event, canvas=self.product_canvas, matrix=self.product_matrix,
                                    text=self.product_text, rects=self.product_rects:
                              self.onMatClick(canvas, matrix, text, event, product_0_color, product_1_color, rects))
      """
      product_dim       = str(self.rows) + " x " + str(self.controller.num_frames) 
      label_product_dim = tk.Label(self, text=product_dim, font=self.controller.title_font) 
      
      self.product_canvas.place(relx=0.05, rely=0.1)
      label_product_dim.place(relx=0.05, y=dynamic_y+105)

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
      self.threading_canvas.place(relx=0.2, rely=0.1)

    def make_pattern_canvas(self):
      # Make a canvas for the pattern
      self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                      width=(block_size + buffer) * self.controller.num_motors + buffer)
      self.pattern_text, self.pattern_rects = populate_matrix(self.pattern_canvas, self.rows,
                                          self.controller.num_motors, pattern_0_color, pattern_1_color)
      self.pattern = np.zeros((self.rows, self.controller.num_motors), dtype=int)
      
      self.pattern_canvas.place(relx=0.2, rely=0.25)

def update_newCanvas_wOldCanvas(old_canvas, new_canvas):
    id_list = old_canvas.find_withtag('text_object')
    for id in id_list:
      print("id= ", id)
      print(old_canvas.itemcget(id,'text'))
      if old_canvas.itemcget(id,'text') == '1':   
        print('true w/ id = ', id)     
        new_canvas.itemconfig(id, text='1')

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

def update_pattern(canvas, text, pattern, tie_upT, treadling, rects):
    #Passing the TieUp as the Transpose
    pattern = np.matmul(treadling, tie_upT)

    for i in range(np.shape(pattern)[0]):
        for j in range(np.shape(pattern)[1]):
            x = j * block_size + (j + 1) * buffer
            y = i * block_size + (i + 1) * buffer
            canvas.delete(text[i][j])
            canvas.delete((rects[i][j]))
            if pattern[i][j] == 1:
                text_color = product_0_color
                back_color = product_1_color
            else:
                text_color = product_1_color
                back_color = product_0_color
            rects[i][j] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color)
            text[i][j] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(pattern[i][j]),
                                            fill=text_color, font='Helvetica 15')
    return pattern