# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: SerialWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $

import serial
import logging

class SerialWrapper:
    def __init__(self, port, baud,deliminator,offset=0, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None,xonxoff = 0 , rtscts = 0, interCharTimeout = None):
        #the number of times we should attempt to send or receive before throwing an excep
        self._retrycount = 100
        #public member to indicated whether connected or not
        self.connected = False
        #using this lock to make the methods thread safe
        self._lock = threading.Lock()        
        
        self._deliminator = deliminator
        self._offset = offset
        self._log = logging.getLogger ( "SerialWrapper" )
        self._buffer = ""
        try: 
            self._serialport = serial.Serial(port,baud,bytesize,parity,stopbits,timeout,xonxoff,rtscts,interCharTimeout)
            self._serialport.open()
            self._serialport.flushInput()
            self._serialport.flushOutput()
            self._log.debug("\nSerial port opened")
        except Exception,e:
            self._log.exception("Opening serial port raised exception : %s" %str(e))
            
    def __splitbuffer(self):
         #this function splits our databuffer and returns the first half of it , then adds the rest back to the databuffer
         deliminatorindex = self._buffer.find(self._deliminator)
         line = ''
         if deliminatorindex != -1:
            if len(self._buffer) >= (deliminatorindex + 1 + self._offset):
                line = self._buffer[:deliminatorindex + self._offset + 1]
                self._buffer = self._buffer[deliminatorindex + self._offset +1:]
         return line
         
    def __buffer(self):
        #lock so nobody can write/read at the same time
        self._lock.acquire()
        try:
            if self._serialport.isOpen():
               if self._serialport.inWaiting() > 0:
                   self._buffer += self._serialport.read(self._serialport.inWaiting())
        except Exception , e:
            self.connected = False
            self._log.exception("Exception while reading from local serial port : %s" %str(e))
            raise                      
        finally:
            self._lock.release()
              
    def close(self):
        #we lock to ensure nobody is writing or reading to the socket
        self._lock.acquire()
        try:
            if self._serialport.isOpen():
                self._serialport.flushInput()
                self._serialport.flushOutput()
                self._serialport.close()
        except Exception,e:
            self._log.exception("Closing serial port raised exception : %s" %str(e))
        finally:
            #always release the lock
            self.connected = False
            self._lock.release() 
                         
           
    def write(self,data):
        #lock so nobody can read/close while we are writing
        self._lock.acquire()
        try:
            if self._serialport.isOpen():
                self._serialport.write(data)
        except Exception , e:
            self.connected = False
            self._log.debug(("\nProblem writing to serial port on port" + self._serialport.port))
            self._log.exception("Writing to serial port raised exception : %s" %str(e))    
            raise
        finally:
            self._lock.release()
    
    def read(self):
        self.__buffer()
        temp = self._buffer
        self._buffer = ""
        return temp
       
    def readline(self):
        self.__buffer()
        return self.__splitbuffer()
        
# $Id: SerialWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
    
