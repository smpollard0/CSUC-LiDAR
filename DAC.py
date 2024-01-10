"""
DAC.py: This is the main program for running the data acquisition software.
"""

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import capture_waveforms
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue

import serial_communication


__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

# this function is meant to collect the data coming into the DAQ NI card and plot it in the GUI
def plot_waveform(axes, the_canvas,the_toolbar, the_text_widget, sample_text_widget, sample_rate_text_widget):
    # get the sample rate and number of samples from the text boxes
    x = []
    data = []
    try:
        num_samples = int(sample_text_widget.get())
        sample_rate = int(sample_rate_text_widget.get())

        # create two processes to happen at the same time
        q = Queue()
        p1 = Process(target=capture_waveforms.collect_waveform_data, args=(num_samples, sample_rate, q,))
        p2 = Process(target=serial_communication.serial_write)
        p1.start()
        p2.start()

        x = q.get()
        data = q.get()

        # plot the data
        axes.clear() # clear current axes
        axes.plot(x,data) # plot the data
        axes.set_xlabel("Sample Number")
        axes.set_ylabel("Voltage (V)")

        the_canvas.draw() # update the plot

        the_toolbar.update() # update the toolbar

        the_text_widget.configure(state='normal')
        the_text_widget.insert(tk.END, get_date_and_time() + "\n")
        the_text_widget.configure(state='disabled')
    except:
        messagebox.showerror('Input Error','[ERROR] Invalid number of samples or sampling rate')
        the_text_widget.configure(state='normal')
        the_text_widget.insert(tk.END, get_date_and_time() + ' [ERROR]\n')
        the_text_widget.configure(state='disabled')

def get_date_and_time():
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    return "[DATE - TIME] " + dt_string

# the main of the program
if __name__ == "__main__":
    root = Tk()
    # set the default size of the window
    root.geometry("1000x1000")

    root.title("LIDAR Data Acquisition Software")

    label = Label(root, text="Data Acquisition").pack()

    # create frame for the left side to store waveform data
    left_frame = Frame(root)
    left_frame.pack(side=LEFT)

    # create the figure to put waveform data
    fig = plt.Figure(figsize = (8,8), dpi = 100)
    ax = fig.add_subplot(111)
    ax.set_xlabel("Sample Number")
    ax.set_ylabel("Voltage (V)")

    canvas = FigureCanvasTkAgg(fig, left_frame)
    toolbar = NavigationToolbar2Tk(canvas, left_frame)
    canvas.draw()

    # create text widget for date and time
    text_widget = Text(left_frame,state='disabled')

    # create 2 text boxes for number of samples and sample rate
    samples_label = Label(root,text="Number of Samples")
    samples_text_box = Entry(root, width=20)
    sample_rate_label = Label(root,text="Sample Rate")
    sample_rate_text_box = Entry(root, width=20)
    samples_label.pack()
    samples_text_box.pack()
    sample_rate_label.pack()
    sample_rate_text_box.pack()
    
    # get data from text box and check if it's an int

    plot_button = Button(master = left_frame,
                          command = lambda: plot_waveform(ax, canvas, toolbar, text_widget, samples_text_box, sample_rate_text_box),
                          width = 10,
                          text = "Plot")
    
    # pack everything
    plot_button.pack()
    canvas.get_tk_widget().pack()
    text_widget.pack()

    root.mainloop() # this runs the main GUI
    