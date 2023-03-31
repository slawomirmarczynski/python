#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przykład, pokazujący jak korzystać z biblioteki tkinter w języku Python.

CC-BY-NC-ND 2023 Sławomir Marczyński
"""

import tkinter as tk
from tkinter import ttk

from tkinter_example_worker import my_fancy_function

def _(string):
    return string

root = tk.Tk()
root.resizable(True, False)
root.call("tk", "scaling", 2.0)
root.title("Program przykładowy")

var_user = tk.StringVar()
var_password = tk.StringVar()


def button_callback(*args):
    user = var_user.get()
    password = var_password.get()
    my_fancy_function(user, password)
    # print("użytkownik:", user, "hasło:", password)

frame0 = ttk.Frame(root)
frame = ttk.Frame(frame0)
frame0.pack(fill="both")
frame.pack(fill="both")

label_title = ttk.Label(frame, text=_("Logowanie do systemu"))

label_user = ttk.Label(frame, text=_("użytkownik:"), underline=0)
label_password = ttk.Label(frame, text=_("hasło:"), underline=0)
entry_user = ttk.Entry(frame, width=40, textvariable=var_user)
entry_password = ttk.Entry(frame, width=40, show='*',textvariable=var_password)
button_login = ttk.Button(frame, text=_("login"), command=button_callback)

label_title.grid(column=0, row=0, sticky="w")
label_user.grid(column=0, row=1, sticky="e")
label_password.grid(column=0, row=2, sticky="e")
entry_user.grid(column=1, row=1, sticky="we")
entry_password.grid(column=1, row=2, sticky="we")
button_login.grid(column=1, row=3, sticky="e")

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", foreground='white', background='green')
style.map("TButton", background=[('active', 'lightgreen')])

frame.columnconfigure(1, weight=1)

frame.pack_configure(padx=20, pady=20)
for widget in frame.winfo_children():
    widget.grid_configure(padx=5, pady=10)

root.bind(_('<Alt-KeyPress-u>'), lambda *args: entry_user.focus())
root.bind(_('<Alt-KeyPress-h>'), lambda *args: entry_password.focus())
root.bind('<Return>', button_callback)

root.mainloop()
