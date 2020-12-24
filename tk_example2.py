#!/usr/bin/python

import tkinter as tk
import tkinter.messagebox
import os

def file_confirm():
    current_path = fpath.get()
    if os.path.isfile(current_path) == True:
        print(fpath.get())
    else:
        tkinter.messagebox.showwarning('Warning','This is not a file')

top = tk.Tk()
top.title('Select file')
fpath = tk.StringVar()
fpath.set(os.getcwd()+'/')
tk.Entry(top,textvariable=fpath,width = 64,bd = 2).grid(row=0,column=0,padx=5,pady=6,sticky=tk.E)
tk.Button(top,text= 'OK',width=5,command = file_confirm).grid(row=0,column=1,padx=5,pady=6,sticky=tk.E)
top.mainloop()