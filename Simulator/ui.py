# ****************************** Imports ****************************** #

import matlab.engine
import math
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, S, E, W
import sys

from random import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matlab.engine

eng = matlab.engine.start_matlab('-noFigureWindows')
eng.addpath(r'./mlab', nargout=0)
eng.addpath(r'./mlab/labs', nargout=0)
eng.addpath(r'./mlab/helper', nargout=0)

from constants import *
from helper_functions import *
from labs.lab1 import Lab1
from labs.lab2 import Lab2
from labs.lab3 import Lab3
from labs.lab4 import Lab4
from labs.lab5 import Lab5
from labs.lab6 import Lab6
from labs.lab7 import Lab7
from labs.lab8 import Lab8
from labs.extended import Extended

# Create a custom logger
logger = logging.getLogger(__name__)


# Tk Variables

root = tk.Tk()
root.title("GUI")
root.minsize(1000, 700)

waveform_type = tk.StringVar()
waveform_type.set(list(waveform_types)[0])

waveform_type_jam = tk.StringVar()
waveform_type_jam.set(list(waveform_types)[0])

operation_mode = tk.IntVar()
operation_mode.set(OperationModes.URAD.value)


# ****************************** Helper Functions ****************************** #


def write_common_parameters():
    # Radar
    eng.workspace['c'] = c
    eng.workspace['fc'] = fc.get()
    eng.workspace['wavelength'] = wavelength.get()
    eng.workspace['range_max'] = range_max.get()
    eng.workspace['ts'] = pow(10, round(math.log10(ts.get())))
    eng.workspace['range_res'] = range_res.get()
    eng.workspace['bw'] = bw.get()
    eng.workspace['speed_max'] = speed_max.get()
    eng.workspace['speed_res'] = speed_res.get()
    eng.workspace['num_of_sweeps'] = num_of_sweeps.get()
    eng.workspace['waveform_type'] = waveform_types[waveform_type.get()]
    eng.workspace['jammer_enabled'] = False;
    eng.workspace['clutter_enabled'] = False;
    return


def set_default_values(_fc, _range_max, _bw, _speed_max, _waveform_type):
    fc.set(_fc)
    range_max.set(_range_max)
    bw.set(_bw)
    speed_max.set(_speed_max)
    waveform_type.set(_waveform_type)



# ****************************** Callbacks ****************************** #


def change_operation_mode(mode):
    if mode == OperationModes.URAD:
        operation_mode.set(OperationModes.URAD.value)
        ext_container.grid_forget()
        tabControl.grid(row=0, column=1, padx=(DEFAULT_PADDING), pady=(
            DEFAULT_PADDING), ipadx=(DEFAULT_PADDING), ipady=(DEFAULT_PADDING), sticky=(N, S, E, W))
    elif mode == OperationModes.Extended:
        operation_mode.set(OperationModes.Extended.value)
        tabControl.grid_forget()
        ext_container.grid(row=0, column=1,padx=(DEFAULT_PADDING), pady=(
            DEFAULT_PADDING), ipadx=(DEFAULT_PADDING), ipady=(DEFAULT_PADDING), sticky=(N, S, E, W))
    print(mode)


def runSimulation():
    eng.clear_workspace(nargout=0)
    write_common_parameters()
    if operation_mode.get() == OperationModes.Extended:
        run_extended()
    else:
        run_lab()


# ****************************** Matlab Calls ****************************** #


def run_extended():
    extended.simulate()

def run_lab():
    
    global tabControl
    labName = tabControl.tab(tabControl.select(), "text")

    if labName == 'Lab 1':
        lab1.simulate()
    if labName == 'Lab 2':
        lab2.simulate()
    if labName == 'Lab 3':
        lab3.simulate()
    if labName == 'Lab 4':
        lab4.simulate()
    if labName == 'Lab 5':
        lab5.simulate()
    if labName == 'Lab 6':
        lab6.simulate()
    if labName == 'Lab 7':
        lab7.simulate()
    if labName == 'Lab 8':
        lab8.simulate()


# ****************************** Widgets ****************************** #


# Window Root Style
s=ttk.Style()
# s.theme_use('classic')
s.configure('heading.TLabel', font=FONT_HEADING)
s.configure('output.TLabelframe', background='white')

# Variables for mlab script
fc = tk.DoubleVar(root, 24.005e9)
wavelength = tk.DoubleVar(root, c / fc.get())
range_max = tk.DoubleVar(root, 100)
ts = tk.DoubleVar(root, 6 * range2time(range_max.get()))
range_res = tk.DoubleVar(root, 2.5)
bw = tk.DoubleVar(root, range2bw(range_res.get()))
speed_max = tk.DoubleVar(root, 270 * 1000 / 3600)
speed_res = tk.DoubleVar(root, 2.5)
num_of_sweeps = tk.DoubleVar(root, 16)


# On change text

def upd_txt(var, val):
    try:
        var.set(val)
    except:
        pass
    return
    
fc.trace_add(
    "write", lambda a, b, d:
     upd_txt(wavelength,c / fc.get()))
range_max.trace_add(
    "write", lambda a, b, c:
     upd_txt(ts,6 * range2time(range_max.get())))
bw.trace_add(
    "write", lambda a, b, c:
     upd_txt(range_res,bw2range(bw.get())))


write_common_parameters()

# Matplotlib
plt.rcParams.update({'font.size': 8, 'font.weight':  'bold'})

# ***** Frames

tabControl = ttk.Notebook(root, width=512)
controlFrame = ttk.Frame(root, width=128, height=512)
extendedFrame = ttk.Frame(root, width=512, height=512)

# Add frame here
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)
tab7 = ttk.Frame(tabControl)
tab8 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Lab 1')
tabControl.add(tab2, text='Lab 2')
tabControl.add(tab3, text='Lab 3')
tabControl.add(tab4, text='Lab 4')
tabControl.add(tab5, text='Lab 5')
tabControl.add(tab6, text='Lab 6')
tabControl.add(tab7, text='Lab 7')
tabControl.add(tab8, text='Lab 8')

sframe = ScrollableFrame(tab1)
sframe.pack(expand=True, fill=tk.BOTH)
tab1 = sframe.scrollable_frame

sframe = ScrollableFrame(tab2)
sframe.pack(expand=True, fill=tk.BOTH)
tab2 = sframe.scrollable_frame

sframe = ScrollableFrame(tab3)
sframe.pack(expand=True, fill=tk.BOTH)
tab3 = sframe.scrollable_frame

sframe = ScrollableFrame(tab4)
sframe.pack(expand=True, fill=tk.BOTH)
tab4 = sframe.scrollable_frame

sframe = ScrollableFrame(tab5)
sframe.pack(expand=True, fill=tk.BOTH)
tab5 = sframe.scrollable_frame

sframe = ScrollableFrame(tab6)
sframe.pack(expand=True, fill=tk.BOTH)
tab6 = sframe.scrollable_frame

sframe = ScrollableFrame(tab7)
sframe.pack(expand=True, fill=tk.BOTH)
tab7 = sframe.scrollable_frame

sframe = ScrollableFrame(tab8)
sframe.pack(expand=True, fill=tk.BOTH)
tab8 = sframe.scrollable_frame


# lab1 = Lab1(tab1, eng)
# lab1.draw_gui()

# lab2 = Lab2(tab2, eng)
# lab2.draw_gui()

# lab3 = Lab3(tab3, eng)
# lab3.draw_gui()

# lab4 = Lab4(tab4, eng)
# lab4.draw_gui()

# lab5 = Lab5(tab5, eng)
# lab5.draw_gui()

# lab6 = Lab6(tab6, eng)
# lab6.draw_gui()

# lab7 = Lab7(tab7, eng)
# lab7.draw_gui()

# lab8 = Lab8(tab8, eng)
# lab8.draw_gui()

ext_container = extendedFrame
sframe = ScrollableFrame(extendedFrame)
sframe.pack(expand=True, fill=tk.BOTH)
extendedFrame = sframe.scrollable_frame

extended = Extended(extendedFrame, eng)
extended.draw_gui()

change_operation_mode(OperationModes.URAD)

root.config(bg='#f4f6f6')
root.grid_columnconfigure(0, weight=0, minsize=1)
root.grid_columnconfigure(1, weight=1, minsize=1)
root.grid_rowconfigure(0, weight=1, minsize=500)
root.grid_rowconfigure(1, weight=0, minsize=70)

controlFrame.grid(row=0, column=0, rowspan=2, padx=(DEFAULT_PADDING, 0), pady=(DEFAULT_PADDING), sticky=(N, S, E, W))
tabControl.grid(row=0, column=1, padx=(DEFAULT_PADDING), pady=(DEFAULT_PADDING), ipadx=(DEFAULT_PADDING), ipady=(DEFAULT_PADDING), sticky=(N, S, E, W))

# Logger Frame

loggerFrame = ttk.Frame(root, width=320, height=70)
loggerFrame.grid(row=1, column=1, padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING), ipadx=(DEFAULT_PADDING), ipady=(DEFAULT_PADDING), sticky=(N, S, E, W))
loggerFrame.columnconfigure(0, weight=1)
loggerFrame.rowconfigure(0, weight=0)
loggerFrame.rowconfigure(1, weight=1)

labelHeading = ttk.Label(loggerFrame, wraplength=320, anchor='nw', justify=tk.LEFT, text="Log Window", style='heading.TLabel')
labelHeading.grid(row=0, column=0, sticky="w", padx=2*DEFAULT_PADDING, pady=(DEFAULT_PADDING,DEFAULT_PADDING))

text_area = tk.Text(loggerFrame)
text_area.grid(row=1, column=0, sticky=(N, S, E, W), padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING))

sys.stdout = LogTextArea(text_area)
sys.stderr = LogTextArea(text_area)

# ***** Control Frame ***** #


labelTitle = ttk.Label(controlFrame, text='Radar Lab App')
labelTitle.config(font=("Sans", 32))
labelTitle.grid(row=0, column=0, pady=32)


# Configure Radar


labelFrameConfig = ttk.LabelFrame(controlFrame, text='Input Parameters')
labelFrameConfig.grid(row=1, column=0, padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING), sticky="ew")

labelFC = ttk.Label(labelFrameConfig, text='Operating frequency (Hz)')
entryFC = ttk.Entry(labelFrameConfig, textvariable=fc)
labelFC.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING, pady=(DEFAULT_PADDING,0))
entryFC.grid(row=0, column=1, sticky="ew", padx=DEFAULT_PADDING, pady=(DEFAULT_PADDING,0))

labelRangeMax = ttk.Label(labelFrameConfig, text='Maximum Range (m)')
entryRangeMax = ttk.Entry(labelFrameConfig, textvariable=range_max)
labelRangeMax.grid(row=2, column=0, sticky="w", padx=DEFAULT_PADDING)
entryRangeMax.grid(row=2, column=1, sticky="ew", padx=DEFAULT_PADDING)


labelRangeRes = ttk.Label(labelFrameConfig, text='Bandwidth (Hz)')
entryRangeRes = ttk.Entry(labelFrameConfig, textvariable=bw)
labelRangeRes.grid(row=5, column=0, sticky="w", padx=DEFAULT_PADDING)
entryRangeRes.grid(row=5, column=1, sticky="ew", padx=DEFAULT_PADDING)

labelSpeedMax = ttk.Label(labelFrameConfig, text='Maximum Speed (m/s)')
entrySpeedMax = ttk.Entry(labelFrameConfig, textvariable=speed_max)
labelSpeedMax.grid(row=6, column=0, sticky="w", padx=DEFAULT_PADDING)
entrySpeedMax.grid(row=6, column=1, sticky="ew", padx=DEFAULT_PADDING)

labelWT = ttk.Label(labelFrameConfig, text='Waveform type')
entryWT = ttk.OptionMenu(labelFrameConfig, waveform_type,list(waveform_types)[0], *waveform_types)
labelWT.grid(row=7, column=0, sticky="w", padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING))
entryWT.grid(row=7, column=1, sticky="ew", padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING))

# Calculated Params

labelFrame = ttk.LabelFrame(controlFrame, text='Calculated Parameters')
labelFrame.grid(row=2, column=0, padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING), sticky="ew")


labelWavelegth = ttk.Label(labelFrame, text='Wavelength (m)')
labelWavelegth.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING, pady=(DEFAULT_PADDING,0))
entryWavelegth = ttk.Entry(labelFrame, textvariable=wavelength, state="readonly")
entryWavelegth.grid(row=0, column=1, sticky="ew", padx=DEFAULT_PADDING, pady=(DEFAULT_PADDING,0))

labelTs = ttk.Label(labelFrame, text='Sweep time (s)')
labelTs.grid(row=1, column=0, sticky="w", padx=DEFAULT_PADDING)
entryTs = ttk.Entry(labelFrame, textvariable=ts, state="readonly")
entryTs.grid(row=1, column=1, sticky="ew", padx=DEFAULT_PADDING)

labelRangeRes = ttk.Label(labelFrame, text='Range Resolution  (m)')
labelRangeRes.grid(row=2, column=0, sticky="w", padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING))
entryRangeRes = ttk.Entry(labelFrame, textvariable=range_res, state="readonly")
entryRangeRes.grid(row=2, column=1, sticky="ew", padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING))


# Configure Operation Mode


labelFrameOperationMode = ttk.LabelFrame(controlFrame, text='Operation Mode')
labelFrameOperationMode.grid(row=3, column=0, padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING), sticky="ew")

labelBasic = ttk.Label(labelFrameOperationMode, text='URAD')
labelBasic.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING, pady=(DEFAULT_PADDING,0), ipadx=24)
rbBasic = ttk.Radiobutton(labelFrameOperationMode, variable=operation_mode,value=OperationModes.URAD.value, command=lambda: change_operation_mode(OperationModes.URAD))
rbBasic.grid(row=0, column=1, sticky="ew", padx=DEFAULT_PADDING, pady=(DEFAULT_PADDING,0))

labelExtended = ttk.Label(labelFrameOperationMode, text='Extended')
labelExtended.grid(row=1, column=0, sticky="w", padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING), ipadx=24)
rbExtended = ttk.Radiobutton(labelFrameOperationMode, variable=operation_mode,value=OperationModes.Extended.value, command=lambda: change_operation_mode(OperationModes.Extended))
rbExtended.grid(row=1, column=1, sticky="ew", padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING))


# Configure Simulation Param


labelFrameSimulationParameters = ttk.LabelFrame(controlFrame, text='Simulation Parameters')
labelFrameSimulationParameters.grid(row=4, column=0, padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING), sticky="ew")

labelNSweep = ttk.Label(labelFrameSimulationParameters, text='Num Of Sweeps')
labelNSweep.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
entryNSweep = ttk.Entry(labelFrameSimulationParameters, textvariable=num_of_sweeps)
entryNSweep.grid(row=0, column=1, sticky="we", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)


# Buttons


buttonSimulate = ttk.Button(controlFrame, text="Simulate", command=runSimulation)
buttonSimulate.grid(row=5, column=0, padx=DEFAULT_PADDING, pady=0, sticky="ew",ipady=8)

frameIECont = ttk.Frame(controlFrame)
frameIECont.grid(row=6, column=0, padx=DEFAULT_PADDING, pady=(0,DEFAULT_PADDING), sticky="ew")

frameIECont.columnconfigure(0, weight=1)
frameIECont.columnconfigure(1, weight=1)

# buttonImport = ttk.Button(frameIECont, text="Import",command=lambda: print('Import'))
# buttonImport.grid(row=0, column=0, sticky=(E, W))

# buttonExport = ttk.Button(frameIECont, text="Export",command=lambda: print('Export'))
# buttonExport.grid(row=0, column=1, sticky=(E, W))


# ****************************** Main ****************************** #

if __name__ == "__main__":
    root.mainloop()
