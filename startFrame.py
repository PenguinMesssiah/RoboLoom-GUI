try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

start_width = 500
start_height = 500

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(start_width) + "x" + str(start_height)

        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Calibrate Loom", command=lambda: controller.show_frame("CalFrame"))
        button2 = tk.Button(self, text="Weave (Matrix Controlled)",
                            command=lambda: controller.show_frame("WeaveFrame1"))
        button3 = tk.Button(self, text="Weave (Pattern Controlled)",
                            command=lambda: controller.show_frame("WeaveFrame2"))
        button1.pack()
        button2.pack()
        button3.pack()