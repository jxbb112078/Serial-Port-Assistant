#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
import serialport
import serial
import time
import threading

def timestamp():
    currtime = int(time.time()*1000%1000)
    currtime = '%03d' % currtime
    strt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return str((strt +':'+str(currtime))) 

class window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('serial port debug by Rodney')
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        f_left = tk.Frame(self.root,bg='FloralWhite',relief=tk.RIDGE) #左边frame
        f_left.grid(row=0, column=0,stick=tk.NSEW)
        f_right = tk.Frame(self.root,bg='FloralWhite',relief=tk.RIDGE) #右边frame
        f_right.grid(row=0, column=1,sticky=tk.NSEW)
        f_left.rowconfigure(2, weight=1)
        f_right.rowconfigure(0, weight=1)
        f_right.columnconfigure(0, weight=1)
        
 #       print(f_left.grid_slaves())
#        self.combox(self.root)
        self.comport = serialport.serial_ops()
        
        self.setting_area(f_left,self.comport)
        self.rtxt,self.stxt,self.sbutton = self.data_area(f_right)
        self.default_value()
        self.rtxt.insert("end", 'para'+'\r\n')
    
 
    def default_value(self):
        comport_select.current(0)
        bdr_setting.current(9)
        check_bit.current(0)
        data_bit.current(3)
        stop_bit.current(0)
        flow_ctrl.current(0)
        serial_status.set('open')

    def serial_act(self):
        # open serial port
        if serial_status.get() == 'open':
            serial_status.set('close')
            #cfg.port = 
            #print('here1%s %s' % (__name__,data_bit.get()))
            comport_select['state'] = "disabled"
            bdr_setting['state'] = "disabled"
            check_bit['state'] = "disabled"
            data_bit['state'] = "disabled"
            stop_bit['state'] = "disabled"
            flow_ctrl['state'] = "disabled"
            self.comport.port = serial_port.get()
            self.comport.baudrate = baudrate.get()
            self.comport.check_bit = parity.get()
            self.comport.data_bit = bytesize.get()
            self.comport.stop_bit = stopbits.get()
            self.comport.flow_ctrl = 'NONE'

            ser = self.comport.open_serial()
            if app.comport.ser.isOpen() == True:
                print('com is open')
                th=threading.Thread(target=self.recv_data,daemon=True)
                th.start()
            else :
                print('not open')
        # close serial port
        else:
            serial_status.set('open')
            
            comport_select['state'] = "readonly"
            bdr_setting['state'] = "active"
            check_bit['state'] = "readonly"
            data_bit['state'] = "readonly"
            stop_bit['state'] = "readonly"
            flow_ctrl['state'] = "readonly"
            
            self.comport.close_serial()

    def update_port(self,event,cfg,para,value):
        
        if para == 'port':
            cfg.port = value
        elif para == 'baudrate' : 
            cfg.baudrate = value
        elif para == 'check_bit' :
            cfg.check_bit = value 
        elif para == 'data_bit' : 
            cfg.data_bit = value
            print('%s,%d' %(para,value))
        elif para == 'stop_bit' : 
            cfg.stop_bit = value
        elif para == 'flow_ctrl' : 
            cfg.flow_ctrl = value
        else:
            return 0

    def test(self,event):
        print('dfd')

    def send_data(self):
        #print(self.stxt.get('0.0','end'))
        str1 = self.stxt.get('0.0','end')
        sendstr = ''
        if send_dis.get() == 1:
            sendstr = str1.encode()
            #print(sendstr[0:1])
            #for i in str1:
            #    sendstr[i] = hex(ord(i))
            #    print(str1[i])
        if send_at_mode.get() == 1:
            #add carriage return mark for at command
            sendstr = str1[0:-1] + '\r'
            #print(sendstr)
  

        #for i in str1: 
        #   print('%x ' %ord(i))
        #str1 = str1[0:-2]+ '\r'
        #str1 = 'ati\r'
        #print()
        self.comport.ser.write(sendstr.encode('utf-8'))
        #return 
    def recv_data(self) :
        print('recv thread starting...')
        while True:
            rec_data = self.comport.ser.readline()
            if len(rec_data) != 0 :
                #print( 'recv len:%d\n %s' %(len(rec_data) ,str(rec_data, encoding = "utf-8")))
                #str1 = rec_data+'\n'
                if recv_log_mode.get() == 1 :
                    
                    self.rtxt.insert("end", '['+timestamp()+']','tag1')

                #else :
                print(str(rec_data, encoding = "utf-8").split('\r'))
                for i in str(rec_data, encoding = "utf-8").split('\r'):
                    if i != '' and i != '\r' :
                        self.rtxt.insert("end", i)
                #self.rtxt.insert("end", str(rec_data, encoding = "utf-8"))
                self.rtxt.see('end')


    def recv_update(self,para):
        if para == 'recv_dis':
            print('recv_dis')
        elif para == 'recv_log_mode':
            print('recv_log_mode')
        elif para == 'recv_line_feed':
            print('recv_line_feed')
        elif para == 'recv_hide_data':
            print('recv_hide_data')
        elif para == 'recv_save_to_file':
            print('recv_save_to_file')
        else:    
            return 0

    def send_update(self,para):
        if para == 'send_dis':
            print(send_dis.get())
        elif para == 'send_convert':
            print('send_convert')
        elif para == 'send_at_mode':
            print(send_at_mode.get())
        elif para == 'send_addtion':
            print('send_addtion')
        elif para == 'send_file':
            print('send_file')
        elif para == 'send_periodic':
            print('send_periodic')
        else: 
            return 0

    def serial_setting(self,frame,cfg):
        global comport_select,serial_port
        global bdr_setting,baudrate
        global check_bit,parity
        global data_bit,bytesize
        global stop_bit,stopbits
        global flow_ctrl,serial_status
        serial_port = tk.StringVar()
        #print(serial_port.get())
        tk.Label(frame, text='serial port',bg='FloralWhite').grid(row=0, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        comport_select=ttk.Combobox(frame,textvariable=serial_port,width=15)
        comport_select['value'] = cfg.get_comports()
        comport_select['state'] = "readonly"
        comport_select.current(3)
        #print(serial_port.get())
        comport_select.bind("<<ComboboxSelected>>",self.test)  #事件的绑定
        comport_select.grid(row=0, column=1,padx=5,sticky=tk.E)

        baudrate = tk.IntVar()
        tk.Label(frame, text='baud rate',bg='FloralWhite').grid(row=1, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        bdr_setting = ttk.Combobox(frame,textvariable=baudrate,width=15)
        bdr_setting['value'] = (1200,2400,4800,9600,14400,19200,38400,56000,57600,115200)
        #bdr_setting['state'] = "readonly"
        bdr_setting.current(9)
        bdr_setting.bind("<<ComboboxSelected>>",self.test)
        
        bdr_setting.grid(row=1, column=1,padx=5,sticky=tk.E)

        parity = tk.StringVar()
        tk.Label(frame, text='check bit',bg='FloralWhite').grid(row=2, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        check_bit = ttk.Combobox(frame,textvariable=parity,width=15)
        check_bit['value'] = (serial.PARITY_NONE,serial.PARITY_EVEN, serial.PARITY_ODD,serial.PARITY_MARK, serial.PARITY_SPACE)
        check_bit['state'] = "readonly"
        check_bit.current(0)
        check_bit.bind("<<ComboboxSelected>>",self.test)
        
        check_bit.grid(row=2, column=1,padx=5,sticky=tk.E)

        bytesize = tk.IntVar()
        tk.Label(frame, text='data bit',bg='FloralWhite').grid(row=3, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        data_bit = ttk.Combobox(frame,textvariable=bytesize,width=15)
        data_bit['value'] = ('5','6','7','8')
        data_bit['state'] = "readonly"
        data_bit.current(3)
        data_bit.bind("<<ComboboxSelected>>",self.test)
        
        data_bit.grid(row=3, column=1,padx=5,sticky=tk.E)

        stopbits = tk.IntVar()
        tk.Label(frame, text='stop bit',bg='FloralWhite').grid(row=4, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        stop_bit = ttk.Combobox(frame,textvariable=stopbits,width=15)
        stop_bit['value'] = ('1','1.5','2')
        stop_bit['state'] = "readonly"
        stop_bit.current(0)
        stop_bit.bind("<<ComboboxSelected>>",self.test)
        stop_bit.grid(row=4, column=1,padx=5,sticky=tk.E)

        fctrl = tk.StringVar()
        tk.Label(frame, text='flow control',bg='FloralWhite').grid(row=5, column=0,padx=5,pady=3,sticky=tk.N+tk.S+tk.W)
        flow_ctrl = ttk.Combobox(frame,textvariable=fctrl,width=15)
        flow_ctrl['value'] = ('NONE','XON/XOFF','RTS/CTS','DTR/DSR','RTS/CTS/XON/XOFF','DTR/DSR/XON/XOFF')
        flow_ctrl['state'] = "readonly"
        flow_ctrl.current(0)
        flow_ctrl.bind("<<ComboboxSelected>>",self.test)      
        flow_ctrl.grid(row=5, column=1,padx=5,sticky=tk.E)

        serial_status = tk.StringVar()
        serial_status.set('open')
        serial_ctrl = ttk.Button(frame,textvariable= serial_status,width=15,command = self.serial_act)
        serial_ctrl.grid(row=6,column=0,columnspan=2,pady=5,sticky=tk.S)
        # receive setting

    def recv_setting(self,frame):
        global recv_dis,recv_log_mode,recv_line_feed,recv_hide_data,recv_save_to_file
        recv_dis = tk.IntVar()
        recv_dis.set(0)
        recv_log_mode = tk.IntVar()
        recv_log_mode.set(1)
        recv_line_feed = tk.IntVar()
        recv_hide_data = tk.IntVar()
        recv_save_to_file = tk.IntVar()
        tk.Radiobutton(frame, variable=recv_dis, bg='FloralWhite',value='0', text='ASCII',command = lambda:self.recv_update('recv_dis')).grid(row=0, column=0,padx=14,pady=5,sticky=tk.E+tk.W)
        tk.Radiobutton(frame, variable=recv_dis,bg='FloralWhite', value='1', text='HEX',command = lambda:self.recv_update('recv_dis')).grid(row=0, column=1,padx=14,sticky=tk.E+tk.W)
        tk.Checkbutton(frame,text = "log mode",bg='FloralWhite', variable = recv_log_mode,command = lambda:self.recv_update('recv_log_mode')).grid(row=1, column=0,padx=5,pady=3,columnspan=2,sticky=tk.W)
        tk.Checkbutton(frame,text = "auto line feed",bg='FloralWhite', variable = recv_line_feed,command = lambda:self.recv_update('recv_line_feed')).grid(row=2, column=0,padx=5,pady=3,columnspan=2,sticky=tk.W)
        tk.Checkbutton(frame,text = "Hide recv data",bg='FloralWhite', variable = recv_hide_data,command = lambda:self.recv_update('recv_hide_data')).grid(row=3, column=0,padx=5,pady=3,columnspan=2,sticky=tk.W)
        tk.Checkbutton(frame,text = "Save to file",bg='FloralWhite', variable = recv_save_to_file,command = lambda:self.recv_update('recv_save_to_file')).grid(row=4, column=0,padx=5,pady=3,columnspan=2,sticky=tk.W)

    # send setting
    def send_setting(self,frame):
        global send_dis,send_convert,send_at_mode,send_addtion,send_file,send_periodic
        send_dis = tk.IntVar()
        send_dis.set(0)
        send_convert = tk.IntVar()
        send_at_mode = tk.IntVar()
        send_at_mode.set(1)
        send_addtion = tk.IntVar()
        send_file = tk.IntVar()
        send_periodic = tk.IntVar()
        #send_mode.set('1')
        tk.Radiobutton(frame, variable=send_dis,bg='FloralWhite', value='0', text='ASCII',command = lambda:self.send_update('send_dis')).grid(row=0, column=0,padx=14,sticky=tk.E+tk.W)
        tk.Radiobutton(frame, variable=send_dis,bg='FloralWhite', value='1', text='HEX',command = lambda:self.send_update('send_dis')).grid(row=0, column=1,padx=14,columnspan=2,sticky=tk.E+tk.W)
        tk.Checkbutton(frame,text = "convert",bg='FloralWhite', variable = send_convert,command = lambda:self.send_update('send_convert')).grid(row=1, column=0,padx=5,pady=3,columnspan=3,sticky=tk.W)
        tk.Checkbutton(frame,text = "AT mode",bg='FloralWhite', variable = send_at_mode,command = lambda:self.send_update('send_at_mode')).grid(row=2, column=0,padx=5,pady=3,columnspan=3,sticky=tk.W)
        tk.Checkbutton(frame,text = "add addtion",bg='FloralWhite', variable = send_addtion,command = lambda:self.send_update('send_addtion')).grid(row=3, column=0,padx=5,pady=3,columnspan=3,sticky=tk.W)
        tk.Checkbutton(frame,text = "open file",bg='FloralWhite', variable = send_file,command = lambda:self.send_update('send_file')).grid(row=4, column=0,padx=5,pady=3,columnspan=3,sticky=tk.W)
        tk.Checkbutton(frame,text = "period",bg='FloralWhite', variable = send_periodic,command = lambda:self.send_update('send_periodic')).grid(row=5, column=0,padx=5,pady=3,sticky=tk.W)
        tk.Entry(frame,width = 5).grid(row=5,column=1,sticky=tk.E)
        tk.Label(frame,bg='FloralWhite',text = 'ms').grid(row=5,column=2,sticky=tk.W)
        tk.Label(frame,bg='FloralWhite').grid(row=6,column=0,columnspan=3,sticky=tk.NS)

    #setting area
    def setting_area(self,frame,serial_cfg):

        f_serial_setting = tk.LabelFrame(frame,text='serial setting',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_serial_setting.grid(row=0, column=0,pady=5,ipadx=5,ipady=5,sticky=tk.NSEW)
        f_recv_setting = tk.LabelFrame(frame,text='receive setting',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_recv_setting.grid(row=1, column=0,pady=5,ipadx=5,ipady=5,sticky=tk.NSEW)
        f_send_setting = tk.LabelFrame(frame,text='send setting',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_send_setting.grid(row=2, column=0,pady=5,ipadx=5,ipady=5,sticky=tk.NSEW)
        f_send_setting.rowconfigure(6, weight=1)
        self.serial_setting(f_serial_setting,serial_cfg)
        self.recv_setting(f_recv_setting)
        self.send_setting(f_send_setting)

    def data_area(self,frame):
        #receive area
        #global recv_text,send_text
        f_data_rwin = tk.LabelFrame(frame,text='Data receive',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_data_rwin.grid(row=0, padx=5,pady=5,sticky=tk.NSEW)
        recv_text = tk.Text(f_data_rwin)
        recv_text.tag_config("tag1", foreground="green")
        recv_text.grid(row=0, column = 0,padx=5,pady=10,sticky=tk.NSEW)
        scroll = tk.Scrollbar(f_data_rwin)
        scroll.grid(row=0,column = 1,sticky=tk.NS)
        scroll.config(command=recv_text.yview)
        recv_text.config(yscrollcommand=scroll.set)
        f_data_rwin.rowconfigure(0, weight=1)
        f_data_rwin.columnconfigure(0, weight=1)

        #send data
        f_data_swin = tk.LabelFrame(frame,text='Data send',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_data_swin.grid(row=1, column=0,padx=5,pady=5,sticky=tk.NSEW)
        f_data_swin.columnconfigure(0, weight=1)

        send_text = tk.Text(f_data_swin,height=3)
        send_text.grid(row=0, column=0,sticky=tk.NSEW)
        send_button = tk.Button(f_data_swin,text='send',height=3,command = self.send_data).grid(row=0, column=1,sticky=tk.E)
        return recv_text,send_text,send_button


app = window()


app.root.mainloop()
'''
mainWindow = tk.Tk()
mainWindow.title('serial port debug by Rodney')

mainWindow.rowconfigure(0, weight=1)
mainWindow.columnconfigure(1, weight=1)

f_left = tk.Frame(mainWindow,bg='FloralWhite',relief=tk.RIDGE) #左边frame
f_left.grid(row=0, column=0,stick=tk.NSEW)
f_right = tk.Frame(mainWindow,bg='FloralWhite',relief=tk.RIDGE) #右边frame
f_right.grid(row=0, column=1,sticky=tk.NSEW)

f_left.rowconfigure(2, weight=1)
f_right.rowconfigure(0, weight=1)
f_right.columnconfigure(0, weight=1)

setting_area(f_left,comport)
rtxt,stxt,sbutton = data_area(f_right)
rtxt.insert("end", 'para'+'\n')
mainWindow.mainloop()
'''