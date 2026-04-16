#!/usr/bin/env python
import os
import time

class s_file:
    def __init__(self):
        current_dir = os.getcwd()
        if os.path.exists(current_dir + '/log') == True:
            print('log is exist')
            if os.path.isfile(current_dir + '/log') == True:
                os.mkdir(current_dir + '/log')
        else:
            os.mkdir(current_dir + '/log')
        self.fname = current_dir + '/log/' + self.timestamp()+'.log'    
        self.fd = open(self.fname,mode="w")

    def s_write(self,str1):
        self.fd.write(str1)

    def timestamp(self):
        currtime = int(time.time()*1000%1000)
        currtime = '%03d' % currtime
        strt = time.strftime("%Y%m%d%H%M%S", time.localtime())
        return str(strt) 

