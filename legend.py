import os
import sys
from tkinter import Toplevel, Message


def open_legend(root):
    window = Toplevel(root)

    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(script_dir, 'legend.txt')

    with open(file_path, 'r') as legend_file:
        legend = legend_file.read()

    Message(window, text=legend, font='Consolas', padx=10, pady=10).pack()
