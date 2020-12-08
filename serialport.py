#!/usr/bin/env python
import serial
import serial.tools.list_ports
import time
import threading

class serial_ops:
    #s_config = {'port':0,'baudrate':0,'check_bit':0,'data_bit':0,'stop_bit':0,'flow_ctrl':0}
    def __init__(self):
        self.port = 'NONE'
        self.baudrate = 115200
        self.check_bit = serial.PARITY_NONE
        self.data_bit = serial.EIGHTBITS
        self.stop_bit = serial.STOPBITS_ONE
        self.flow_ctrl = 'NONE'
        self.ser = serial.Serial()
        #self.s_config['port'] = 'NONE'

    def get_comports(self):
        temp = ''
        for i in serial.tools.list_ports.comports():
            temp += i.device + ','
        portlist = tuple([ str(i) for i in temp.split(',') ])
        portlist = portlist[0:-1]
        return portlist 
#print(get_comports())

    def open_serial(self):
        if 'XON/XOFF' in self.flow_ctrl:
            sfc = True
        else:
            sfc = False
        if 'RTS/CTS' in self.flow_ctrl:
            hfc = True
        else:
            hfc = False
        if 'DTR/DSR' in self.flow_ctrl:
            hfc = True
        else:
            hfc = False
        
        
        self.ser.port = self.port
        self.ser.baudrate = self.baudrate
        self.ser.bytesize = self.data_bit
        self.ser.parity = self.check_bit
        self.ser.stopbits = self.stop_bit
        self.ser.xonxoff = sfc
        self.ser.rtscts = hfc
        self.ser.dsrdtr = hfc
        #self.ser.timeout = 1
        print('%s,%s,%d,%s,%d,%d' % (__name__ , self.port, self.baudrate,self.check_bit,self.data_bit,self.stop_bit))
        #self.ser = serial.Serial(port=self.port,baudrate=self.baudrate,bytesize=self.data_bit,parity=self.check_bit,stopbits=self.stop_bit,xonxoff=sfc,rtscts=hfc)

        self.ser.open()
        #return self.ser
    def close_serial(self):
        self.ser.close()

    def recv_data(self,serialid) :
        while True:
            rec_data = serialid.readline()
            if len(rec_data) != 0 :
                print( str(rec_data, encoding = "utf-8"),end='')
if __name__ == "__main__":
    fd1 = serial_ops()
    x = fd1.get_comports()
    print(x)
'''
ser = serial.Serial("/dev/ttyUSB3",115200,timeout = 0)
if ser.isOpen() == True:
    print('com is open')
    th=threading.Thread(target=recv_data,daemon=True,kwargs={"serialid":ser})
    th.start()
    while True:
        str1 = input("Please input:")
        if str1 == 'exit' :
            break
        else :
            str1 += '\r'
        ser.write(str1.encode('utf-8'))
        time.sleep(0.2)
    print('will close com')
    ser.close()
else :
    print('not open')
'''





