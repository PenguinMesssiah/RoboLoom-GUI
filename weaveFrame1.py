try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

weave1_width = 1600
weave1_height = 800

class WeaveFrame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(weave1_width) + "x" + str(weave1_height)

        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.grid(row=0, column=0, columnspan=1)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=0, columnspan=1)