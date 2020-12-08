#!/usr/bin/python

import tkinter as tk
import tkinter.ttk as ttk
import serial



class test:
    def __init__(self):
        self.top = tk.Tk()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(1, weight=1)
        #tk.Label(self.top,text="I am on top").grid(row=0, column=0)
        #btn_click = tk.Button(text="click me too",command=self.clicked).grid(row=1, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        self.combox(self.top)
        self.tt()
        #print(self.top.grid_slaves())
        #self.top.mainloop()
    def tt(self):
        data_bit.current(3)
    def combox(self,frame):
        global data_bit
        bytesize = tk.IntVar()
        tk.Label(frame, text='data bit').grid(row=3, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        data_bit = ttk.Combobox(frame,textvariable=bytesize,width=15)
        data_bit['value'] = ('5','6','7','8')
        data_bit['state'] = "normal"
        data_bit.current(3)
        data_bit.bind("<<ComboboxSelected>>",self.clicked)
        data_bit.grid(row=3, column=1,padx=5,sticky=tk.E)

    def update_port(self,event,bytesize):
        print(bytesize.get())
        print('fd')

    def handler_adaptor(self, fun, *kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, *kwds)    
        
    def clicked(self,event):

        second = tk.Toplevel()
        tk.Label(second,text="I am second").grid(row=0, column=0)
        btn_exit = tk.Button(second,text="exit",command=self.cexit).grid(row=1, column=0)
    


    def cexit(self):
        exit()

app = test()
app.top.mainloop()



