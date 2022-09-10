# ****************************** Imports ****************************** #


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import N, S, E, W, BOTH
import tkinter as tk
import tkinter.ttk as ttk
from constants import *

import logging

# ****************************** Data ****************************** #


figures = []


# ****************************** Calculation Functions ****************************** #


def range2bw(RangeResolution):
    return c / (2*RangeResolution)


def bw2range(bw):
    return c / (2*bw)


def range2time(MaxRange):
    return 2*MaxRange/c


def drawSurfacePlot(container, x_data, y_data, z_data, title, x_label, y_label, z_label, width, height):

    try:
        for child in container.winfo_children():
            child.destroy()
    except NameError:
        pass
    except AttributeError:
        pass

    fig = plt.figure(figsize=(width, height))
    ax = plt.axes(projection='3d')
    ax.plot_surface(x_data, y_data, z_data, cmap='viridis', edgecolor='none')
    ax.set_title(title)
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas_wid = canvas.get_tk_widget()
    canvas_wid.pack(fill=BOTH)
    pass


def drawPPI(container, width, height, title):
    # r = np.arange(0, 2, 0.01)
    # theta = 2 * np.pi * r

    fig = plt.figure(figsize=(width, height))
    wrapped_fig = FigureWrapper(fig)
    ax = plt.subplot(111, projection='polar')
    # ax.plot(theta, r)
    # ax.set_rmax(2)
    # ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
    # ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)
    ax.set_title(title, va='bottom')
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas_wid = canvas.get_tk_widget()
    canvas_wid.pack(fill=BOTH)


# ****************************** Wrapper Classes ****************************** #


class FigureWrapper(object):
    '''Frees underlying figure when it goes out of scope.
    '''

    def __init__(self, figure):
        self._figure = figure

    def __del__(self):
        plt.close(self._figure)
        print("Figure removed")


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbary = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbarx = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        # self.scrollable_frame.bind(
        #     "<Configure>",
        #     lambda e: canvas.itemconfig(scrollable_frame, width=e.width)
        # )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        scrollbarx.pack(side="bottom", fill="x")
        scrollbary.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)


class LogTextArea():
    def __init__(self, text_area):
        super().__init__()
        self.text_area = text_area
        return

    def write(self, str):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, str)
        self.text_area.configure(state=tk.DISABLED)
        self.text_area.see(tk.END)
        return
