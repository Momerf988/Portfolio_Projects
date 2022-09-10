# ********** IMPORTS ********** #


import tkinter as tk
import tkinter.ttk as ttk
import sys

# **********  DATA   ********** #


stdout_ori = sys.stdout
stderr_ori = sys.stderr


# **********  STDO   ********** #


class LogTextArea():
    def __init__(self, text_area):
        super().__init__()
        self.text_area = text_area
        return

    def write(self, str):
        self.text_area.insert(tk.END, str)
        return


# **********  GUI    ********** #


class GUI:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.log_text = None
        self.draw_gui()
        sys.stdout = LogTextArea(self.log_text)
        print('hello')
        return

    def draw_gui(self):
        self.log_text = tk.Text(self.root)
        self.log_text.grid(row=0, column=0)
        return


root = tk.Tk()
gui  = GUI(root)
root.mainloop()