try:
    import tkinter as tk  # python 3
    from tkinter import ttk # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from serialCom import move_frame, init_frames

weave1_width   = 1400
weave1_height  = 1000
console_height = 100
block_size = 20
buffer = 2

tie_up_0_color = "#022b75"
tie_up_1_color = "#80a2e0"

threading_0_color = "#3d026e"
threading_1_color = "#c1abde"

treadling_0_color = "#034a01"
treadling_1_color = "#98c997"

pattern_0_color = "white"
pattern_1_color = "black"
instr_message = 'Welcome! Change the number of shafts and pedals for your shaft loom setup. \
Then change the matrices by clicking on the boxes. Once your pattern is complete, \
weave using the \'Next Row\' and \'Previous Row\' buttons.'


class WeaveFrame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent     = parent
        self.geo        = str(weave1_width) + "x" + str(weave1_height)

        # Make this changeable later?
        self.rows    = 25
        self.columns = 20 
        self.side_nav_state = False

        #Defining the Set X for Tie-Up & Treadling
        dynamic_x = (block_size + buffer) * self.controller.num_motors + buffer

        #Create Title
        label = tk.Label(self, text="Shaft Loom Weaving", font=controller.title_font)
        
        #Adding Console
        self.make_console(dynamic_x)

        #Create Buttons
        button            = tk.Button(self, text="Return Home", command=lambda: controller.show_frame("StartPage"))
        button_weave      = tk.Button(self, text="Next Row", command=lambda: self.weave_row(True))
        button_weave_back = tk.Button(self, text="Previous Row", command=lambda: self.weave_row(False))
        side_nav_button   = tk.Button(self, text="Toggle Side Menu", command=lambda: toggle_side_nav(self))

        #Adding Side Navigation Panel
        self.make_side_nav_menu()

        self.pat_row   = 0
        self.highlight = None

        # make and populate the canvases
        # Make a canvas for the pattern
        self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                        width=(block_size + buffer) * self.controller.num_motors + buffer)
        self.pattern_text, self.pattern_rects = populate_matrix(self.pattern_canvas, self.rows,
                                            self.controller.num_motors, pattern_0_color, pattern_1_color)
        self.pattern = np.zeros((self.rows, self.controller.num_motors), dtype=int)

        # Make a tie up matrix canvas
        self.make_threading_canvas()

        # Make a tieup canvas
        self.make_tieup_canvas()

        # Make a treadling canvas
        self.make_treadling_canvas()

        # make buttons for num frames and num pedals
        self.make_pedal_frame_buttons()

        #Placing Objects
        label.place(relx=0.3, rely=0.01, anchor=tk.CENTER)
        button.place(relx=0.36, rely=0.15, anchor=tk.NW)

        self.button_frames.place(x=150, rely=0.15, anchor=tk.N)
        self.text_box_frames.place(x=210, rely=0.15, anchor=tk.N)
        self.button_pedals.place(x=dynamic_x+100, rely=0.15)
        self.text_box_pedals.place(x=dynamic_x+200, rely=0.15)
        button_weave.place(relx=0.25, rely= 0.15)
        button_weave_back.place(relx=0.3, rely= 0.15)
        side_nav_button.place(relx=0.17, rely= 0.15)

        self.threading_canvas.place(relx=0.05, rely=0.20)
        self.tieup_canvas.place(x=dynamic_x+100, rely=0.20)
        self.pattern_canvas.place(relx=0.05, rely=0.3)
        self.treadling_canvas.place(x=dynamic_x+100, rely=0.3)

        #Place Side Nav
        self.side_nav_frame.place(relx=1, rely=0.02, anchor=tk.NE)
        self.notebook.place(relx=0.5, rely=0, anchor=tk.N)

        #Display Console
        self.console_frame.place(relx=0.05, rely=0.03, anchor=tk.NW)
        self.console_text.pack(side=tk.LEFT)

    def make_console(self, dynamic_x):
        self.console_frame     = tk.LabelFrame(self, height=console_height, width=dynamic_x+140,  
                                           bg="#d2d7d3", text="Console Log", relief=tk.RAISED)
        self.console_frame.pack_propagate(False)
        self.console_text      = tk.Listbox(self.console_frame, height=console_height,
                                         width=dynamic_x+140,  font='Terminal 10')
        self.console_text.insert(tk.END, instr_message)
    
    def make_side_nav_menu(self):
        #TODO: Show Side Nav Menu on Top of Weaving Draft
        self.side_nav_frame = tk.Frame(self, width=75, height=weave1_height*.8, 
                            background="#50c878", relief= tk.GROOVE, borderwidth=5)
        
        #Adding Notebook for Side Nav
        self.notebook = ttk.Notebook(self.side_nav_frame)
        #tab1 = tk.Frame(notebook, width= , height= )
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        self.tab4 = tk.Frame(self.notebook)

    def make_pedal_frame_buttons(self):
        self.button_frames   = tk.Button(self, text="Set # of Shafts", command=self.set_frames)
        self.button_pedals   = tk.Button(self, text="Set # of Pedals", command=self.set_pedals)
        self.text_box_frames = tk.Text(self, height=1, width=2, wrap='word')
        self.text_box_frames.insert('end', self.controller.num_frames)
        self.text_box_pedals = tk.Text(self, height=1, width=2, wrap='word')
        self.text_box_pedals.insert('end', self.controller.num_pedals)

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

    def weave_row(self, forward):
        if forward:
            self.pat_row += 1
        else:
            self.pat_row -= 1
        if self.pat_row > self.rows:
            self.pat_row = 1
        elif self.pat_row <= 0:
            self.pat_row = self.rows
        self.pattern_canvas.delete(self.highlight)
        x0 = buffer
        y0 = (self.pat_row - 1) * (block_size + buffer) + buffer
        x1 = (self.controller.num_motors) * (block_size + buffer) + buffer / 2
        y1 = y0 + block_size + buffer / 2
        self.highlight = self.pattern_canvas.create_rectangle(x0, y0, x1, y1, width=buffer * 2, outline="green")
        # CHANGE THIS TO MOVE FRAME with the frame from treadling*tie up
        # Send a list of frames
        # Frames starts as a list of 0s. Where treadling is 1, get tieup column, or col with frames, send that

        #Find where treadling is 1
        pedals_pressed = np.where(self.treadling[self.pat_row - 1]==1)[0]
        print(pedals_pressed)
        frames = np.zeros((self.controller.num_frames), dtype='int')
        for pedal in pedals_pressed:
            print(pedal)
            print(frames)
            print(np.resize(self.tie_up[:, pedal], (self.controller.num_frames)))
            frames = np.bitwise_or(frames, self.tie_up[:, pedal])
            print(frames)

        move_frame(frames)

    def set_frames(self):
        oldHeight = (block_size + buffer) * self.controller.num_frames

        self.controller.num_frames = int(self.text_box_frames.get("1.0", "end-1c"))
        init_frames(self.controller.num_frames)

        newHeight= (block_size + buffer) * self.controller.num_frames

        # resize the threading, return everything to zeros
        self.threading_canvas.delete("all")
        self.threading_canvas.config(width=(block_size + buffer) * self.controller.num_motors + buffer,
                                     height=(block_size + buffer) * self.controller.num_frames)
        self.threading_text, self.threading_rects = populate_matrix(self.threading_canvas, self.controller.num_frames,
                                                                    self.controller.num_motors, threading_0_color,
                                                                    threading_1_color)
        self.threading = np.zeros((self.controller.num_frames, self.controller.num_motors), dtype=int)

        #resize the tie-up, return everything to zeros
        self.tieup_canvas.delete("all")
        self.tieup_canvas.config(height=(block_size + buffer) * self.controller.num_frames,
                                      width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                              self.controller.num_pedals, tie_up_0_color,
                                                              tie_up_1_color)
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)

        #rebind buttons with new thing
        self.threading_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.threading_canvas, matrix=self.threading,
                                          text=self.threading_text, rects=self.threading_rects:
                                   self.onMatClick(canvas, matrix, text, event, threading_0_color,
                                                   threading_1_color, rects))
        self.tieup_canvas.bind('<Button-1>',
                               lambda event, canvas=self.tieup_canvas, matrix=self.tie_up,
                                      text=self.tie_up_text, rects=self.tie_up_rects:
                               self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))
        
        #Resize Pattern & Treadling Canvas
        rel_diff        = abs(newHeight-oldHeight)/weave1_height
        new_base_height = 0.22 + self.threading_canvas.winfo_height()/weave1_height
        dynamic_x = (block_size + buffer) * self.controller.num_motors + buffer

        if newHeight>oldHeight:
            self.pattern_canvas.place(relx=0.05, rely=new_base_height  + rel_diff)
            self.treadling_canvas.place(x=dynamic_x+100, rely=new_base_height + rel_diff)
        elif newHeight != oldHeight:
            self.pattern_canvas.place(relx=0.05, rely=new_base_height - rel_diff)
            self.treadling_canvas.place(x=dynamic_x+100, rely=new_base_height - rel_diff) 

        print("FRAMES")

    def set_pedals(self):
        self.controller.num_pedals = int(self.text_box_pedals.get("1.0", "end-1c"))
        # remake the tie_up and treadling canvas

        self.tieup_canvas.delete("all")
        self.tieup_canvas.config(height=(block_size + buffer) * self.controller.num_frames,
                                 width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                              self.controller.num_pedals, tie_up_0_color,
                                                              tie_up_1_color)
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)


        self.treadling_canvas.delete("all")
        self.treadling_canvas.config(height=(block_size + buffer) * self.rows,
                                          width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.treadling_text, self.treadling_rects = populate_matrix(self.treadling_canvas, self.rows,
                                                                    self.controller.num_pedals, treadling_0_color,
                                                                    treadling_1_color)
        self.treadling = np.zeros((self.rows, self.controller.num_pedals), dtype=int)

        # rebind buttons with new thing
        self.tieup_canvas.bind('<Button-1>',
                               lambda event, canvas=self.tieup_canvas, matrix=self.tie_up,
                                      text=self.tie_up_text, rects=self.tie_up_rects:
                               self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))
        self.treadling_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.treadling_canvas, matrix=self.treadling,
                                          text=self.treadling_text, rects=self.treadling_rects:
                                   self.onMatClick(canvas, matrix, text, event, treadling_0_color,
                                                   treadling_1_color, rects))
        print("PEDALS")

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

def toggle_side_nav(self):
    self.side_nav_state = bool(not(self.side_nav_state))

    if self.side_nav_state ==  True:
        self.notebook.add(self.tab1, text="Weaving Terminology")
        self.notebook.add(self.tab2, text="Weacing Draft Legend")
        self.notebook.add(self.tab3, text="Culturally Significant Patterns")
        self.notebook.add(self.tab4, text="Linear Algebra Review")
        self.side_nav_frame.place(relx=1, rely=0.05, anchor=tk.NE, width=800)
    else:
        for x in range(0,4,1):
            self.notebook.hide(x)
        
        self.side_nav_frame.place(relx=1, rely=0.05, anchor=tk.NE, width=75)