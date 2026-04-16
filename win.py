#!/usr/bin/env python
import tkinter as tk
# from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog
import serialport
import serial
import time
import threading
import sf
import os
import ttkbootstrap as ttk

def timestamp():
    currtime = int(time.time()*1000%1000)
    currtime = '%03d' % currtime
    strt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return str((strt +':'+str(currtime))) 

class window:
    def __init__(self):
        # self.root = tk.Tk()
        #想要切换主题，修改theme值即可，有以下这么多的主题，自己尝试吧：['vista', 'classic', 'cyborg', 'journal', 'darkly', 'flatly', 'clam', 'alt', 'solar', 'minty', 'litera', 'united', 'xpnative', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero', 'winnative', 'sandstone', 'default']
        self.root = ttk.Window(themename='superhero')
        self.root.title('Serial port assistant')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        '''
        There are 2 frames on root window. 
        there are 3 sub-frames on left frame,2 sub-frames on right frame.
        illustrate as below
        --------------------------------------------
        |                |                         |
        |f_serial_setting|                         |
        |                |                         |
        |                |                         |
        -----------------|      f_data_rwin        |
        |                |                         |
        |                |                         |
        | f_recv_setting |                         |
        |                |                         |
        --------------------------------------------
        |                |                         |
        |                |                         |
        |f_send_setting  |      f_data_swin        |
        |                |                         |
        --------------------------------------------
        '''

        f_left = tk.Frame(self.root,bg='FloralWhite',relief=tk.RIDGE) #left frame
        f_left.grid(row=0, column=0,stick=tk.NSEW)
        f_right = tk.Frame(self.root,bg='FloralWhite',relief=tk.RIDGE) #right frame
        f_right.grid(row=0, column=1,sticky=tk.NSEW)
        f_left.rowconfigure(2, weight=1)
        f_right.rowconfigure(0, weight=1)
        f_right.columnconfigure(0, weight=1)
        self.send_flag = False
        self.comport = serialport.serial_ops()  
        self.setting_area(f_left,self.comport)
        self.rtxt,self.stxt,self.sbutton = self.data_area(f_right)
        #self.default_value()
        threading.Thread(target=self.update_port,daemon=True).start()
    
    # Default setting of all of parameters
    def default_value(self):
        comport_select.current(0)
        bdr_setting.current(9)
        check_bit.current(0)
        #data_bit.current(3)
        stop_bit.current(0)
        flow_ctrl.current(0)
        serial_status.set('open')

    # To open a com port and start a receive thread
    def serial_act(self):
        # open serial port
        if serial_status.get() == 'open':
            serial_status.set('close')
            comport_select['state'] = "disabled"
            bdr_setting['state'] = "disabled"
            check_bit['state'] = "disabled"
            data_bit['state'] = "disabled"
            stop_bit['state'] = "disabled"
            flow_ctrl['state'] = "disabled"
            self.comport.port = serial_port.get()
            self.comport.baudrate = baudrate.get()
            #self.comport.check_bit = parity.get()
            self.comport.data_bit = bytesize.get()
            self.comport.stop_bit = stopbits.get()
            self.comport.flow_ctrl = 'NONE'
            if parity.get() == 'NONE':
                self.comport.check_bit = serial.PARITY_NONE
            elif parity.get() == 'EVEN':
                self.comport.check_bit = serial.PARITY_EVEN
            elif parity.get() == 'ODD':
                self.comport.check_bit = serial.PARITY_ODD
            elif parity.get() == 'MARK':
                self.comport.check_bit = serial.PARITY_MARK
            else:
                self.comport.check_bit = serial.PARITY_SPACE
            ser = self.comport.open_serial()
            if self.comport.ser.is_open:  # 使用 is_open 属性代替 isOpen() 方法
            #    print('com is open')
                self.comport.is_receiving = True  # 设置接收标志为 True
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
                
            self.comport.close_serial()  # 会先设置 is_receiving=False 并等待

    #Update serial device by specific period
    def update_port(self):
        while True:
            comport_select['value'] = self.comport.get_comports()
            #print('==')
            time.sleep(0.3)

    def test(self,event):
        comport_select['value'] = self.comport.get_comports()
        print(parity.get())

    def period_send(self,delay,contents):
        while True:
            self.comport.ser.write(contents.encode('utf-8'))
            time.sleep(delay/1000)
            if self.send_flag == False:
                break
        return

    #send the sepcificed file
    def file_trans(self):
        try:
            fd = open(selected_file, mode='r')
            while True:
                buf = fd.read(100)
                if buf == '':
                    break
                self.comport.ser.write(buf.encode('utf-8'))
        finally:
            print('close file')
            fd.close()

    # Be invoked when send buttion is clicked
    def send_command(self):
        if send_file.get() == 1:
            self.file_trans()
        else:
            self.send_data()
 
    #Send data which is located in send frame
    def send_data(self):
        str1 = self.stxt.get('0.0','end')
        sendstr = ''
        if send_dis.get() == 1:
            sendstr = str1.encode()
        if send_at_mode.get() == 1:
            sendstr = str1[0:-1] + '\r'
        if send_periodic.get() == 1: #send data as a fix period
            delay = int(ptime.get())
            if self.send_flag == False:
                self.send_flag = not self.send_flag
                th_send=threading.Thread(target=self.period_send,args=(delay,sendstr),daemon=True)
                th_send.start()
                self.stxt.configure(state='disabled',bg='lightgrey')
                dis_rbt_0['state'] = 'disabled'
                dis_rbt_1['state'] = 'disabled'
                at_chk_bt['state'] = 'disabled'
                add_chk_bt['state'] = 'disabled'
                f_chk_bt['state'] = 'disabled'
                p_chk_bt['state'] = 'disabled'
                t_chk_et['state'] = 'disabled'
                self.sbutton['text'] = 'stop send'
            else:
                self.send_flag = not self.send_flag
                self.stxt.configure(state='normal',bg='white')
                dis_rbt_0['state'] = 'normal'
                dis_rbt_1['state'] = 'normal'
                at_chk_bt['state'] = 'normal'
                add_chk_bt['state'] = 'normal'
                f_chk_bt['state'] = 'normal'
                p_chk_bt['state'] = 'normal'
                t_chk_et['state'] = 'normal'
                self.sbutton['text'] = 'send'
        else:
            self.comport.ser.write(sendstr.encode('utf-8'))

    #This function is invoked by receive thread and display contents in receive frame
    def recv_data(self) :
        print('recv thread starting...')
        while self.comport.is_receiving:  # 检查接收标志，安全退出
            try:
                # 检查串口是否打开
                if not self.comport.ser.is_open:
                    print('ERROR: Serial port is closed')
                    break
                
                rec_data = self.comport.ser.readline()
                if recv_hide_data.get() == 1: #doesn't display data in receive windows
                    continue
                if len(rec_data) != 0 :
                    #print( 'recv len:%d\n %s' %(len(rec_data) ,str(rec_data, encoding = "utf-8")))
                    #str1 = rec_data+'\n'
                    log_timestamp = '['+timestamp()+']'
                    if recv_log_mode.get() == 1 : # log mode enable
                        
                        self.rtxt.insert("end", log_timestamp,'tag1')
                        if recv_save_to_file.get() == 1:
                            fd.fd.write(log_timestamp)
                    #else :
                    #print(str(rec_data, encoding = "utf-8").split('\r'))
                    if recv_dis.get() == 1: #HEX mode display
                        for i in rec_data:
                            # print('0x{:02X} '.format(i))
                            self.rtxt.insert("end", '0x{:02X} '.format(i))
                        self.rtxt.insert("end", '\n')
                    else :
                        for i in str(rec_data, encoding = "utf-8").split('\r'):
                            if i != '' and i != '\r' :
                                self.rtxt.insert("end", i)
                                if recv_save_to_file.get() == 1:
                                    fd.fd.write(i)
                    #self.rtxt.insert("end", str(rec_data, encoding = "utf-8"))
                    self.rtxt.see('end')
            except Exception as e:
                if self.comport.is_receiving:  # 仅当串口应该打开时打印错误
                    print(f'ERROR in recv_data: {type(e).__name__}: {e}')
                break  # 安全退出接收线程
        print('recv thread stopped')

    #Excute corresponding actions when the receive setting is changed
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
            global fd
            if recv_save_to_file.get() == 1:
                print("open file")
                fd = sf.s_file()
                self.rtxt.insert("end", 'Will save log to file: ' + fd.fname + '\n')
                # self.rtxt.configure(state='disabled')
                
            else :
                fd.fd.close()
                self.rtxt.configure(state='normal')
        else:    
            return 

    #Close root window
    def main_closing(self):
        # 优雅地关闭串口
        if self.comport.ser.is_open:
            self.comport.close_serial()
        
        if recv_save_to_file.get() == 1:
            fd.fd.close()
        self.root.destroy()

    #Close popup window   
    def file_select_closing(self):
        send_file.set(0)
        top.destroy()
        self.stxt.delete(1.0,"end")
        self.stxt.configure(state='normal')

    #Excute corresponding actions when the send setting is changed
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
            if send_file.get() == 1:
                self.select_file()
            else:
                print(top)
                if top != '':
                    top.destroy()
                self.stxt.configure(state='normal',fg='white')
                self.stxt.delete(0.0,tk.END)
                
        elif para == 'send_periodic':
            print('send_periodic')
        else: 
            return 0

    #Excute corresponding actions during file selecting
    def file_confirm(self):
        global selected_file
        selected_file = fpath.get()
        if os.path.isfile(selected_file) == True:
            top.destroy()
            print(selected_file)
            self.stxt.insert("end", 'Ready to send file \n'+selected_file)
            self.stxt.configure(state='disabled',fg='gray')
        else:
            tkinter.messagebox.showwarning('Warning','This is not a file')
    def browse_file(self):
        global fpath
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select a file')
        if file_path:
            fpath.set(file_path)
    #To select a file that you would like to send.
    def select_file(self):
        print('select file')
        global top,fpath
        top = tk.Toplevel(bg='FloralWhite',relief=tk.RIDGE)
        top.title('Select file')
        fpath = tk.StringVar()
        fpath.set(os.getcwd()+'/')
        tk.Entry(top,textvariable=fpath,width = 64,bd = 2).grid(row=0,column=0,padx=5,pady=6,sticky=tk.E)
        tk.Button(top,text= 'Browse',width=5,command = self.browse_file).grid(row=1,column=0,padx=5,pady=6,sticky=tk.E)
        tk.Button(top,text= 'OK',width=5,command = self.file_confirm).grid(row=1,column=1,padx=5,pady=6,sticky=tk.E)
        top.columnconfigure(0, weight=1)
        top.protocol("WM_DELETE_WINDOW", self.file_select_closing)

    #f_serial_setting frame
    def serial_setting(self,frame,cfg):
        global comport_select,serial_port
        global bdr_setting,baudrate
        global check_bit,parity
        global data_bit,bytesize
        global stop_bit,stopbits
        global flow_ctrl,fctrl,serial_status
        serial_port = tk.StringVar()
        #print(serial_port.get())
        tk.Label(frame, text='Serial port',bg='FloralWhite').grid(row=0, column=0,padx=14,pady=3,sticky=tk.N+tk.S+tk.W)
        comport_select=ttk.Combobox(frame,textvariable=serial_port,width=15)
        comport_select['value'] = cfg.get_comports()
        comport_select['state'] = "readonly"
        comport_select.current(0)
        #print(serial_port.get())
        #comport_select.bind("<<ComboboxSelected>>",self.test)  #
        comport_select.grid(row=0, column=1,padx=5,sticky=tk.E)

        baudrate = tk.IntVar()
        ttk.Label(frame, text='Baud rate').grid(row=1, column=0,padx=14,pady=3,sticky=tk.N+tk.S+tk.W)
        bdr_setting = ttk.Combobox(frame,textvariable=baudrate,width=15,height=8)
        bdr_setting['value'] = (1200,2400,4800,9600,14400,19200,38400,56000,57600,115200,128000,230400,256000,460800,921600,1000000)
        #bdr_setting['state'] = "readonly"
        bdr_setting.current(9)
        #bdr_setting.bind("<<ComboboxSelected>>",self.test)
        bdr_setting.grid(row=1, column=1,padx=5,sticky=tk.E)

        parity = tk.StringVar()
        ttk.Label(frame, text='Check bit').grid(row=2, column=0,padx=14,pady=3,sticky=tk.N+tk.S+tk.W)
        check_bit = ttk.Combobox(frame,textvariable=parity,width=15)
        check_bit['value'] = ('NONE','EVEN','ODD','MARK','SPACE')
        check_bit['state'] = "readonly"
        check_bit.current(0)
        #check_bit.bind("<<ComboboxSelected>>",self.test)
        
        check_bit.grid(row=2, column=1,padx=5,sticky=tk.E)

        bytesize = tk.IntVar()
        tk.Label(frame, text='Data bit',bg='FloralWhite').grid(row=3, column=0,padx=14,pady=3,sticky=tk.N+tk.S+tk.W)
        data_bit = ttk.Combobox(frame,textvariable=bytesize,width=15)
        data_bit['value'] = ('5','6','7','8')
        data_bit['state'] = "readonly"
        data_bit.current(3)
        #data_bit.bind("<<ComboboxSelected>>",self.test)
        
        data_bit.grid(row=3, column=1,padx=5,sticky=tk.E)

        stopbits = tk.IntVar()
        tk.Label(frame, text='Stop bit',bg='FloralWhite').grid(row=4, column=0,padx=14,pady=3,sticky=tk.N+tk.S+tk.W)
        stop_bit = ttk.Combobox(frame,textvariable=stopbits,width=15)
        stop_bit['value'] = ('1','1.5','2')
        stop_bit['state'] = "readonly"
        stop_bit.current(0)
        #stop_bit.bind("<<ComboboxSelected>>",self.test)
        stop_bit.grid(row=4, column=1,padx=5,sticky=tk.E)

        fctrl = tk.StringVar()
        tk.Label(frame, text='Flow control',bg='FloralWhite').grid(row=5, column=0,padx=14,pady=3,sticky=tk.N+tk.S+tk.W)
        flow_ctrl = ttk.Combobox(frame,textvariable=fctrl,width=15)
        flow_ctrl['value'] = ('NONE','XON/XOFF','RTS/CTS','DTR/DSR','RTS/CTS/XON/XOFF','DTR/DSR/XON/XOFF')
        flow_ctrl['state'] = "readonly"
        flow_ctrl.current(0)
        #flow_ctrl.bind("<<ComboboxSelected>>",self.test)      
        flow_ctrl.grid(row=5, column=1,padx=5,sticky=tk.E)

        serial_status = tk.StringVar()
        serial_status.set('open')
        serial_ctrl = ttk.Button(frame,textvariable= serial_status,width=15,command = self.serial_act)
        serial_ctrl.grid(row=6,column=0,columnspan=2,pady=10,sticky=tk.N+tk.S)
        # receive setting

    #f_recv_setting frame
    def recv_setting(self,frame):
        global recv_dis,recv_log_mode,recv_line_feed,recv_hide_data,recv_save_to_file
        recv_dis = tk.IntVar()
        recv_dis.set(0)
        recv_log_mode = tk.IntVar()
        recv_log_mode.set(1)
        recv_line_feed = tk.IntVar()
        recv_hide_data = tk.IntVar()
        recv_save_to_file = tk.IntVar()
        ttk.Radiobutton(frame, variable=recv_dis,width=12,value='0', text='ASCII',command = lambda:self.recv_update('recv_dis')).grid(row=0, column=0,padx=14,pady=6,sticky=tk.E+tk.W)
        ttk.Radiobutton(frame, variable=recv_dis, value='1', text='HEX',command = lambda:self.recv_update('recv_dis')).grid(row=0, column=1,padx=14,pady=6,sticky=tk.E+tk.W)
        ttk.Checkbutton(frame,text = "Log mode", variable = recv_log_mode,command = lambda:self.recv_update('recv_log_mode')).grid(row=1, column=0,padx=14,pady=6,columnspan=2,sticky=tk.W)
        ttk.Checkbutton(frame,text = "Auto line feed", variable = recv_line_feed,command = lambda:self.recv_update('recv_line_feed')).grid(row=2, column=0,padx=14,pady=6,columnspan=2,sticky=tk.W)
        ttk.Checkbutton(frame,text = "Hide recv data", variable = recv_hide_data,command = lambda:self.recv_update('recv_hide_data')).grid(row=3, column=0,padx=14,pady=6,columnspan=2,sticky=tk.W)
        ttk.Checkbutton(frame,text = "Save to file", variable = recv_save_to_file,command = lambda:self.recv_update('recv_save_to_file')).grid(row=4, column=0,padx=14,pady=6,columnspan=2,sticky=tk.W)

    # f_send_setting frame
    def send_setting(self,frame):
        global send_dis,send_convert,send_at_mode,send_addtion,send_file,send_periodic,ptime
        global dis_rbt_0,dis_rbt_1,at_chk_bt,add_chk_bt,f_chk_bt,p_chk_bt,t_chk_et
        send_dis = tk.IntVar()
        send_dis.set(0)
        send_convert = tk.IntVar()
        send_at_mode = tk.IntVar()
        send_at_mode.set(1)
        send_addtion = tk.IntVar()
        send_file = tk.IntVar()
        send_periodic = tk.IntVar()
        ptime = tk.StringVar()
        ptime.set('500')
        #send_mode.set('1')
        dis_rbt_0 = ttk.Radiobutton(frame, variable=send_dis, value='0', text='ASCII',command = lambda:self.send_update('send_dis'))
        dis_rbt_0.grid(row=0, column=0,padx=14,pady=6,sticky=tk.E+tk.W)
        dis_rbt_1 = ttk.Radiobutton(frame, variable=send_dis, value='1', text='HEX',command = lambda:self.send_update('send_dis'))
        dis_rbt_1.grid(row=0, column=1,padx=14,pady=6,columnspan=2,sticky=tk.E+tk.W)
        #tk.Checkbutton(frame,text = "convert",bg='FloralWhite', variable = send_convert,command = lambda:self.send_update('send_convert')).grid(row=1, column=0,padx=5,pady=3,columnspan=3,sticky=tk.W)
        at_chk_bt=ttk.Checkbutton(frame,text = "AT mode", variable = send_at_mode,command = lambda:self.send_update('send_at_mode'))
        at_chk_bt.grid(row=2, column=0,padx=14,pady=6,columnspan=3,sticky=tk.W)
        add_chk_bt=ttk.Checkbutton(frame,text = "Add addtion", variable = send_addtion,command = lambda:self.send_update('send_addtion'))
        add_chk_bt.grid(row=3, column=0,padx=14,pady=6,columnspan=3,sticky=tk.W)
        f_chk_bt=ttk.Checkbutton(frame,text = "Send from file", variable = send_file,command = lambda:self.send_update('send_file'))
        f_chk_bt.grid(row=4, column=0,padx=14,pady=6,columnspan=3,sticky=tk.W)
        p_chk_bt=ttk.Checkbutton(frame,text = "Period", width=12,variable = send_periodic,command = lambda:self.send_update('send_periodic'))
        p_chk_bt.grid(row=5, column=0,padx=14,pady=6,sticky=tk.W)
        t_chk_et=ttk.Entry(frame,textvariable=ptime,width = 6)
        t_chk_et.grid(row=5,column=1,padx=2,sticky=tk.E)
        ttk.Label(frame,text = 'ms').grid(row=5,column=2,sticky=tk.W)
        # ttk.Label(frame,).grid(row=6,column=0,columnspan=3,sticky=tk.NS)

    #setting area, left frame
    def setting_area(self,frame,serial_cfg):

        f_serial_setting = tk.LabelFrame(frame,text='Serial setting',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_serial_setting.grid(row=0, column=0,pady=5,padx=5,ipadx=4,ipady=5,sticky=tk.NSEW)
        f_recv_setting = tk.LabelFrame(frame,text='Receive setting',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_recv_setting.grid(row=1, column=0,pady=5,padx=5,ipadx=14,ipady=5,sticky=tk.NSEW)
        f_send_setting = tk.LabelFrame(frame,text='Send setting',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_send_setting.grid(row=2, column=0,pady=5,padx=5,ipadx=14,ipady=5,sticky=tk.NSEW)
        f_send_setting.rowconfigure(6, weight=1)
        # f_send_setting.columnconfigure(1, weight=1)
        self.serial_setting(f_serial_setting,serial_cfg)
        self.recv_setting(f_recv_setting)
        self.send_setting(f_send_setting)

    #receive area, right frame
    def data_area(self,frame):
        f_data_rwin = tk.LabelFrame(frame,text='Data receive',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_data_rwin.grid(row=0, padx=5,pady=5,sticky=tk.NSEW)
        recv_text = tk.Text(f_data_rwin,width = 2)
        recv_text.tag_config("tag1", foreground="green")
        recv_text.grid(row=0, column = 0,padx=5,pady=10,sticky=tk.NSEW)
        scroll = tk.Scrollbar(f_data_rwin)
        scroll.grid(row=0,column = 1,sticky=tk.NS)
        scroll.config(command=recv_text.yview)
        recv_text.config(yscrollcommand=scroll.set)
        recv_text.bind('<Key>', lambda e: 'break')
        f_data_rwin.rowconfigure(0, weight=1)
        f_data_rwin.columnconfigure(0, weight=1)

        #send data
        f_data_swin = tk.LabelFrame(frame,text='Data send',bg='FloralWhite',bd=4,relief=tk.RIDGE)
        f_data_swin.grid(row=1, column=0,padx=5,pady=5,sticky=tk.NSEW)
        f_data_swin.columnconfigure(0, weight=1)

        send_text = tk.Text(f_data_swin,height=3)
        send_text.grid(row=0, column=0,sticky=tk.NSEW)
        send_button = tk.Button(f_data_swin,text='send',height=3,wraplength=60,command = self.send_command)
        send_button.grid(row=0, column=1,sticky=tk.E)
        return recv_text,send_text,send_button

if __name__ == "main":
    app = window()
    app.root.protocol("WM_DELETE_WINDOW", app.main_closing)
    app.root.mainloop()
