#!/usr/bin/env python
import os
import time

class s_file:
    def __init__(self):
        if os.path.exists('log') == True:
            print('log is exist')
            if os.path.isfile('log') == True:
                os.mkdir('log')
        else:
            os.mkdir('log')
            
        self.fd = open('log/'+self.timestamp()+'.log',mode="w")

    def s_write(self,str1):
        self.fd.write(str1)

    def timestamp(self):
        currtime = int(time.time()*1000%1000)
        currtime = '%03d' % currtime
        strt = time.strftime("%Y%m%d%H%M%S", time.localtime())
        return str(strt) 
if __name__ == "__main__":
    x = s_file()
    x.fd.write("fsdfsd\n\r\r")
    x.fd.write("fsdfsd\n\r\r")
    x.fd.close()
