#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przykład, pokazujący jak korzystać z biblioteki tkinter w języku Python.

CC-BY-NC-ND 2023 Sławomir Marczyński
"""

import tkinter as tk
from tkinter import ttk
import time

root = tk.Tk()
root.call("tk", "scaling", "2.0")
root.resizable(False, False)
root.title("STOPER")

style = ttk.Style()
# print(style.theme_names())
style.theme_use('clam')
style.configure("TButton", foreground="white", background="green")
style.map("TButton", background=[('active', 'lightgreen')])
style.configure("TEntry", fieldbackground="yellow")

frame0 = ttk.Frame(root)
frame = ttk.Frame(frame0)
frame0.pack()
frame.pack()


var_seconds = tk.IntVar()

is_stopped = True
delta_t = 0
t_start = 0


def start(*args):
    global is_stopped, t_start
    if is_stopped:
        is_stopped = False
        t_start = time.time()
        update()
        button_start["state"] = "disabled"
        button_stop["state"] = "normal"


def stop(*args):
    global is_stopped, delta_t
    if not is_stopped:
        is_stopped = True
        root.after_cancel(after_id)
        t_stop = time.time()
        delta_t += t_stop - t_start
        var_seconds.set(int(delta_t))
        button_start["state"] = "normal"
        button_stop["state"] = "disabled"


def reset(*args):
    global delta_t
    stop()
    delta_t = 0
    var_seconds.set(int(delta_t))


def update(*args):
    global is_stopped, after_id
    global t_start, delta_t
    if not is_stopped:
        t = time.time()
        var_seconds.set(int(delta_t + t - t_start))
        after_id = root.after(250, update)


label = ttk.Label(frame, text="czas jaki upłynął w sekundach")
entry = ttk.Entry(frame, width=20, textvariable=var_seconds, justify="right")
button_start = ttk.Button(frame, text="start", command=start, underline=0)
button_stop = ttk.Button(frame, text="stop", command=stop, underline=1)
button_reset = ttk.Button(frame, text="reset", command=reset, underline=0)

label.grid(row=0, column=0, columnspan=3)
entry.grid(row=1, column=0, columnspan=3)
button_start.grid(row=2, column=0)
button_stop.grid(row=2, column=1)
button_reset.grid(row=2, column=2)

frame.grid_configure(padx=20, pady=20)
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=10)

entry["state"] = "readonly"
button_stop["state"] = "disabled"

root.bind("<Control-Key-s>", start)
root.bind("<Control-Key-t>", stop)
root.bind("<Control-Key-r>", reset)

root.mainloop()
