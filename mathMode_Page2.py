try:
    import tkinter as tk  # python 3
    from tkinter import ttk # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from constants import *

mathMode_width   = 1000
mathMode_height  = 400


class MathMode_Page2(tk.Frame):

    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      self.parent     = parent
      self.geo        = str(mathMode_width) + "x" + str(mathMode_height)

      #Create Labels & buttons
      label       = tk.Label(self, text="Mini Math Mode", font=controller.title_font)
      label_x     = tk.Label(self, text="X", font=controller.title_font)
      label_equal = tk.Label(self, text="=", font=controller.title_font)

      label_tr    = tk.Label(self, text="Treadling (Tr)", font=controller.title_font)
      label_p     = tk.Label(self, text="Product (P)", font=controller.title_font)  
      label_d     = tk.Label(self, text="Drawdown (D)", font=controller.title_font)

      button_back   = tk.Button(self, text="Back", command=lambda: controller.show_frame("MathMode_Page1"))
      button_return = tk.Button(self, text="Return", command=lambda: controller.show_frame("WeaveFrame1"))

      self.pat_row   = 0
      self.highlight = None
      
      #TODO: Set Minimum Page Dimensions
      #TODO: Find way to import product matrix

      #Placing Objects
      label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
      label_x.place(relx=0.275, rely=0.325, anchor=tk.W)
      label_equal.place(relx=0.575, rely=0.325, anchor=tk.E)
      label_tr.place(relx=0.05,rely=0.2)
      label_p.place(relx=0.3,rely=0.2)
      label_d.place(relx=0.6,rely=0.2)

      button_back.place(relx=0.45, rely= 0.1)
      button_return.place(relx=0.525, rely=0.1)
    
    def init_page(self):
      self.pattern = np.zeros((NUM_ROWS_DIS, NUM_MOTORS_DIS), dtype=int)
      
      self.make_treadling_canvas()
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
      self.pattern = update_pattern(self.pattern_canvas, self.pattern_text, self.pattern,
                                    self.treadling, self.product_matrix, self.pattern_rects)
    
    def make_product_canvas(self):
      mathMode_frame     = self.controller.get_page("MathMode_Page1")
      old_product_canvas = mathMode_frame.product_canvas
      old_product_matrix = mathMode_frame.product_matrix
      dynamic_y          = (block_size + buffer) * self.controller.num_pedals

      self.product_canvas = tk.Canvas(self, height=dynamic_y, width=(block_size + buffer) * NUM_MOTORS_DIS + buffer)
      self.product_text, self.product_rects = populate_matrix(self.product_canvas, self.controller.num_pedals,
                                                              NUM_MOTORS_DIS, product_0_color, product_1_color)
      self.product_matrix = old_product_matrix
      
      update_newCanvas_wOldCanvas(old_product_canvas, self.product_canvas)
      """
      self.product_canvas.bind('<Button-1>',
                              lambda event, canvas=self.product_canvas, matrix=self.product_matrix,
                                    text=self.product_text, rects=self.product_rects:
                              self.onMatClick(canvas, matrix, text, event, product_0_color, product_1_color, rects))
      """
      product_dim       = str(self.controller.num_pedals) + " x " + str(NUM_MOTORS_DIS) 
      self.label_product_dim = tk.Label(self, text=product_dim, font=self.controller.title_font) 
      
      self.product_canvas.place(relx=0.3, rely=0.3)
      self.label_product_dim.place(relx=0.3, y=dynamic_y+150)
    
    def make_treadling_canvas(self):
      dynamic_y = (block_size + buffer) * NUM_ROWS_DIS
      
      self.treadling_canvas = tk.Canvas(self, height=dynamic_y,
                                        width=(block_size + buffer) * self.controller.num_pedals + buffer)
      self.treadling_text, self.treadling_rects = populate_matrix(self.treadling_canvas, NUM_ROWS_DIS,
                                                                  self.controller.num_pedals, treadling_0_color,
                                                                  treadling_1_color)
      self.treadling = np.zeros((NUM_ROWS_DIS, self.controller.num_pedals), dtype=int)
      self.treadling_canvas.bind('<Button-1>',
                                  lambda event, canvas=self.treadling_canvas, matrix=self.treadling,
                                        text=self.treadling_text, rects=self.treadling_rects:
                                  self.onMatClick(canvas, matrix, text, event, treadling_0_color,
                                                  treadling_1_color, rects))
      treadling_dim       = str(NUM_ROWS_DIS) + " x " + str(self.controller.num_pedals) 
      self.label_treading_dim  = tk.Label(self, text=treadling_dim, font=self.controller.title_font) 
      
      self.treadling_canvas.place(relx=0.05, rely=0.3)
      self.label_treading_dim.place(relx=0.05, y=dynamic_y+150)

    def make_pattern_canvas(self):
      # Make a canvas for the pattern
      dynamic_y = (block_size + buffer) * NUM_ROWS_DIS

      self.pattern_canvas = tk.Canvas(self, height=dynamic_y, width=(block_size + buffer) * NUM_MOTORS_DIS + buffer)
      self.pattern_text, self.pattern_rects = populate_matrix(self.pattern_canvas, NUM_ROWS_DIS,
                                          NUM_MOTORS_DIS, pattern_0_color, pattern_1_color)
      self.pattern = np.zeros((NUM_ROWS_DIS, NUM_MOTORS_DIS), dtype=int)

      pattern_dim       = str(NUM_ROWS_DIS) + " x " + str(NUM_MOTORS_DIS) 
      self.label_pattern_dim = tk.Label(self, text=pattern_dim, font=self.controller.title_font)
      
      self.pattern_canvas.place(relx=0.6, rely=0.3)
      self.label_pattern_dim.place(relx=0.6, y=dynamic_y+150)
    
    def destroyPage(self):
      self.pattern_canvas.destroy()
      self.treadling_canvas.destroy()
      self.product_canvas.destroy()
      self.label_treading_dim.destroy()
      self.label_product_dim.destroy()
      self.label_pattern_dim.destroy()

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

def update_pattern(canvas, text, pattern, treadling, product, rects):
    #Passing the TieUp as the Transpose
    pattern = np.matmul(treadling, product)

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