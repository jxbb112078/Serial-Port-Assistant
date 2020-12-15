#!/usr/bin/python

import tkinter as tk
import tkinter.ttk as ttk
import serialport

def clickme():
    print(recv_text.get())

win=tk.Tk()
win.title("CommunicationTool")
win.rowconfigure(1, weight=1)
win.columnconfigure(0, weight=1)

#setting
setFrame = tk.LabelFrame(win,text="Setting")
setFrame.grid(row=0,sticky=tk.EW)

number = tk.StringVar()
#comLable = tk.Label(setFrame,text="COM Port: ").grid(row=0,column=0)
comSpiner = ttk.Combobox(setFrame,textvariable=number)
#comSpiner['values'] = ('fd')
comSpiner['values'] = ('5','6','7','8')
comSpiner.current(0)
#comSpiner.bind('<<ComboboxSelected>>', clickme)

comSpiner.grid(row=0,column=0,sticky=tk.EW)
setFrame.columnconfigure(1, weight=1)
#global refrashButton
refrashButton = ttk.Button(setFrame,text="Refresh",command = clickme).grid(row=0,column=1,sticky=tk.W)

recv_text = tk.Text(setFrame)
recv_text.grid(row=1, columnspan=2, padx=5,pady=10,sticky=tk.NSEW)
 
'''
inputLable = tk.Label(setFrame,text="Command: ").grid(row=1,column=0)
inputEntry = tk.Entry(setFrame).grid(row=1,column=1,sticky=tk.W+tk.E+tk.S+tk.N,columnspan=2)
sendButton = ttk.Button(setFrame,text="Send").grid(row=1,column=3)
setFrame.grid(row=0,sticky=tk.EW)
setFrame.columnconfigure(1, weight=1)
#output
outputFrame = tk.LabelFrame(win,text="Output")

area = tk.Text(outputFrame).grid(row=0,sticky=tk.NSEW)
outputFrame.grid(row=1,sticky=tk.NSEW)
outputFrame.rowconfigure(0,weight=1)
outputFrame.columnconfigure(0,weight=1)
'''
win.mainloop()

