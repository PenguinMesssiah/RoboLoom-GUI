try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from serialCom import move_row

weave1_width = 1500
weave1_height = 800
block_size = 25
buffer = 1
color0 = "white"
color1 = "black"
color0_text = "black"
color1_text = "white"



class FileFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(weave1_width) + "x" + str(weave1_height)
        self.pat_text = []
        self.pattern = []
        self.rows = 0
        self.cols = 0

        label = tk.Label(self, text="Load your pattern (csv) and see the cloth properties", font=controller.title_font)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        load_button = tk.Button(self, text="Load File", command=lambda: self.show_file())
        fall_apart_button = tk.Button(self, text="Single Cloth?",
                                      command=lambda: calc_integrity(self.pattern, self.rows, self.cols, self.num_cloths))
        weave_factor_button = tk.Button(self, text="Weave Factor?",
                                        command=lambda: calc_weave_factor(self.pattern, self.rows, self.cols, self.pat_canvas, self.m1, self.m2))

        message = "G:\Shared drives\SHRED Lab\ActiveStudentsResearchFolders\SamSpeer_ResearchFolder\Projects\RoboLoom\Weaving Patterns\star_trek_pattern.csv"

        self.text_box = tk.Text(
            self,
            height=3,
            width=100,
            wrap='word'
        )
        self.text_box.insert('end', message)

        # Make a canvas for the pattern
        max_x = 41*block_size + 41*buffer
        pat_width = max_x
        pat_height = 800
        self.pat_canvas = tk.Canvas(self, bg='#FFFFFF', width=pat_width, height=pat_height, scrollregion=(0, 0, max_x, 80*block_size))
        hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hbar.config(command=self.pat_canvas.xview)
        vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vbar.config(command=self.pat_canvas.yview)
        self.pat_canvas.config(width=pat_width, height=pat_height)
        self.pat_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.num_cloths = tk.Label(self, text="? cloths")
        self.m1 = tk.Label(self, text="M1 = ?")
        self.m2 = tk.Label(self, text="M2 = ?")

        label.grid(row=0, column=0, columnspan=3)
        button.grid(row=1, column=0, columnspan=3)
        self.text_box.grid(row=2, column=1, columnspan=2)
        load_button.grid(row=2, column=0)

        hbar.grid(row=8, column=1, sticky=tk.EW)
        vbar.grid(row=3, column=2, sticky=tk.NS, rowspan=5)
        self.pat_canvas.grid(row=3, column=1, rowspan=5)
        fall_apart_button.grid(row=3, column=0)
        weave_factor_button.grid(row=5, column=0)
        self.num_cloths.grid(row=4, column=0)
        self.m1.grid(row=6, column=0)
        self.m2.grid(row=7, column=0)

    def show_file(self):
        print("Hi")
        file = self.text_box.get("1.0","end-1c")
        self.pattern = np.genfromtxt(file, delimiter=',', dtype=int)
        self.cols = len(self.pattern[0])
        self.rows = len(self.pattern)

        self.pat_canvas.delete("all")
        self.m1.config(text="M1 = ?")
        self.m2.config(text="M2 = ?")
        self.num_cloths.config(text="? cloths")

        text = []
        for row in range(self.rows):
            text_row = []
            for column in range(self.cols):
                x = column * block_size + (column + 1) * buffer +block_size+2*buffer
                y = row * block_size + (row + 1) * buffer + block_size+2*buffer
                color = color1
                color_text = color1_text
                if self.pattern[row,column] == 0:
                    color = color0
                    color_text = color0_text
                self.pat_canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="")
                text_row.append(self.pat_canvas.create_text(x + block_size / 2, y + block_size / 2,
                                                            text=str(self.pattern[row,column]), fill=color_text,
                                                   font=('Helvetica 15 bold')))
            text.append(text_row)
        self.pat_text = text

def calc_weave_factor(pattern, rows, cols, pat_canvas, m1_label, m2_label):
    print("Weave Factor")
    if pattern == []:
        return
    horz_padded = np.append(pattern, np.reshape(pattern[:, 0], (rows, 1)), axis=1)
    horz_diff = np.absolute(np.diff(horz_padded, axis=1))

    vert_padded = np.append(pattern, np.reshape(pattern[0, :], (1, cols)), axis=0)
    vert_diff = np.absolute(np.diff(vert_padded, axis=0))

    # Sum
    horz_sum = np.sum(horz_diff)
    horz_sums_vec = np.sum(horz_diff, axis=1) / cols
    m1 = rows ** 2 / horz_sum
    print(m1)

    vert_sum = np.sum(vert_diff)
    vert_sums_vec = np.sum(vert_diff, axis=0)/rows
    m2 = cols ** 2 / vert_sum
    print(m2)

    m1_label.config(text="M1 = "+str(m1)[0:3])
    m2_label.config(text="M2 = " + str(m2)[0:3])

    for row in range(rows):
        y = row * block_size + (row + 1) * buffer
        y = y + block_size + 2*buffer
        r = str(hex(int(255)))[2:]
        g = str(hex(int((horz_sums_vec[row])*255)))[2:]
        b = str(hex(int((horz_sums_vec[row])*255)))[2:]
        if len(g) == 1:
            g = "0"+g
        if len(b) == 1:
            b = "0"+b
        color = "#" + r+g+b
        pat_canvas.create_rectangle(buffer, y, block_size + buffer, y + block_size, fill=color, outline="")
    for col in range(cols):
        x = col * block_size + (col + 1) * buffer
        x = x + block_size + 2 * buffer
        r = str(hex(int(255)))[2:]
        g = str(hex(int((vert_sums_vec[col]) * 255)))[2:]
        b = str(hex(int((vert_sums_vec[col]) * 255)))[2:]
        if len(g) == 1:
            g = "0"+g
        if len(b) == 1:
            b = "0"+b
        color = "#" + str(r+g+b)
        pat_canvas.create_rectangle(x, buffer, x + block_size, block_size + buffer, fill=color, outline="")

def calc_integrity(pattern, rows, cols, label):
    print("Number of cloths goes here")
    # Go through each combination of rows and columns to break them into sets and see if they'd fall apart
    fall_apart = False


    for c1 in range(cols):
        if fall_apart:
            break
        # Check individual col 1
        c1_1s = np.argwhere(pattern[:, c1] == 1)[:, 0]
        rows_c1_1s = [x for x in c1_1s]

        leftover = np.delete(pattern, rows_c1_1s, 0)
        leftover = np.delete(leftover, [c1], 1)

        # see if any of remaining cols sum to 0, this would be the b set
        leftover_sum = np.sum(leftover, axis=0)
        b_set = np.argwhere(leftover_sum == 0)[:, 0]

        # if the b set is not empty, check pattern at the rows_1s in the non b set or c1 or c2 columns
        # if these are all ones, it falls apart
        if len(b_set) > 0:
            rows_not_1 = [y for y in range(rows) if y not in rows_c1_1s]
            potential_a_cols = np.delete(pattern, rows_not_1, 0)
            potential_a_cols = np.delete(potential_a_cols, [c1], 1)
            potential_a_cols = np.delete(potential_a_cols, b_set, 1)
            if not np.size(potential_a_cols) == 0:
                if len(np.unique(potential_a_cols)) <= 1 and potential_a_cols[0, 0]:
                    fall_apart = True
                    # print("Fabric will fall apart")
                    # find the a cols
                    # print("A set rows and cols")
                    # print(rows_not_1)
            else:
                fall_apart = True
                # print("Fabric will fall apart")
                # find the a cols
                # print("A set rows and cols")
                # print(rows_not_1)
        for c2 in range(c1 + 1, cols):
            if fall_apart:
                break
            # Check all pairs
            c2_1s = np.argwhere(pattern[:, c2] == 1)[:, 0]
            rows_1s = [x for x in rows_c1_1s if x in c2_1s]
            # remove rows that are both ones and cols that are c1 and c2
            leftover = np.delete(pattern, rows_1s, 0)
            leftover = np.delete(leftover, [c1, c2], 1)

            # see if any of remaining cols sum to 0, this would be the b set
            leftover_sum = np.sum(leftover, axis=0)
            b_set = np.argwhere(leftover_sum == 0)[:, 0]

            # if the b set is not empty, check pattern at the rows_1s in the non b set or c1 or c2 columns
            # if these are all ones, it falls apart
            if len(b_set) > 0:
                rows_not_1 = [y for y in range(rows) if y not in rows_1s]
                potential_a_cols = np.delete(pattern, rows_not_1, 0)
                potential_a_cols = np.delete(potential_a_cols, [c1, c2], 1)
                potential_a_cols = np.delete(potential_a_cols, b_set, 1)
                if not np.size(potential_a_cols) == 0:
                    if len(np.unique(potential_a_cols)) <= 1 and potential_a_cols[0, 0]:
                        fall_apart = True
                        # print("Fabric will fall apart")
                        # find the a cols
                        # print("A set rows and cols")
                        # print(rows_not_1)
                else:
                    fall_apart = True
                    # print("Fabric will fall apart")
                    # find the a cols
                    # print("A set rows and cols")
                    # print(rows_not_1)
    if not fall_apart:
        print("Fabric will not fall apart")
        label.config(text="1 cloth")
    else:
        print("Fabric will fall apart")
        label.config(text="2 cloths")