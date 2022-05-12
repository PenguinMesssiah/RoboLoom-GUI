try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

weave1_width = 1600
weave1_height = 800
block_size = 20
buffer = 3

class WeaveFrame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(weave1_width) + "x" + str(weave1_height)

        label = tk.Label(self, text="Change the matrices", font=controller.title_font)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))

        #make and populate the canvases
        # Make a canvas for the pattern
        self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.pat_len2,
                                        width=(block_size + buffer) * self.controller.num_motors + buffer)
        populate_matrix(self.pattern_canvas, self.controller.pat_len2, self.controller.num_motors, "blue")

        # Make a tie up matrix canvas
        self.tie_up_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                       width=(block_size + buffer) * self.controller.num_motors + buffer)
        populate_matrix(self.tie_up_canvas, self.controller.num_frames, self.controller.num_motors, "green")

        # Make a frame canvas
        self.frame_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                      width=(block_size + buffer) * self.controller.num_frames + buffer)
        populate_matrix(self.frame_canvas, self.controller.num_frames, self.controller.num_frames, "orange")

        # Make a treadling canvas
        self.treadling_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.pat_len2,
                                          width=(block_size + buffer) * self.controller.num_frames + buffer)
        populate_matrix(self.treadling_canvas, self.controller.pat_len2, self.controller.num_frames, "purple")

        

        # Position things in frame
        self.tie_up_canvas.grid(row=0, column=1)
        self.pattern_canvas.grid(row=1, column=1)
        self.frame_canvas.grid(row=0, column=2)
        self.treadling_canvas.grid(row=1, column=2)
        button.grid(row=2, column=1, columnspan=2)
        label.grid(row=0, column=1, columnspan=2)

def populate_matrix(canvas, rows, cols, color):
    for row in range(rows):
        for column in range(cols):
            x = column * block_size + (column + 1) * buffer
            y = row * block_size + (row + 1) * buffer
            canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color)