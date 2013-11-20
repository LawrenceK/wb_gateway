# $Id: TelnetWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
# THIS CLASS USES THE TELNETLIB 
# IT SHOULD ONLY BE USED IN CIRCUMSTANCES WHERE YOU DO NOT EVER EXPECT TO RECIEVE BYTES OF VALUE HIGHER THAN 239
# IF YOU ATTEMPT TO WRITE BYTES HIGHER THAN 239 IT WILL AUTOMATICALLY SEND THEM TWICE TO CONFORM WITH THE TELNET RFC 854
# DO NOT USE THIS CLASS TO INTERACT WITH NETMEDIA SITEPLAYER TELNET-SERIAL INTERFACES , IT DOES NOT CONFORM TO THE TELNET RFC, USE TCPWRAPPER INSTEAD

import telnetlib
import logging

class TelnetWrapper():
    def __init__(self,hostname,port,deliminator =''):
        self.deliminator = deliminator
        self.port = port
        self.hostname = hostname
        self.databuffer =''
        self._log = logging.getLogger ( "TelnetWrapper" )
        try:
            self.telnetConnection = telnetlib.Telnet(hostname,port)
        except Exception,ex:
            self.error = "Problem while connecting to telnet server @ " + self.hostname 
            self._log.debug(self.error)
            self._log.exception("Exception while connecting to telnet server : %s" %str(ex))
            
    def close(self):
        try:
            self.telnetConnection.close()
        except Exception,ex:
            self.error = "Problem while closing connection to telnet server @ " + self.hostname 
            self._log.debug(self.error)
            self._log.exception("Exception while connecting to telnet server : %s" %str(ex))
            
        
    def write(self,word):
        try:
            self.telnetConnection.write(word)
        except Exception,ex:
            self.error = "Problem while sending to telnet server @ " + self.hostname 
            self._log.debug(self.error)
            self._log.exception("Exception while connecting to telnet server : %s" %str(ex))
                     
    def __buffer(self):
        try:
            self.databuffer += self.telnetConnection.read_very_eager()
            self._log.debug("Databuffer is %s" %self.databuffer)
        except Exception,ex:
            self.error = "Problem while reading from telnet server @ " + self.hostname
            self._log.debug(self.error)
            self._log.exception("Exception while connecting to telnet server : %s" %str(ex))
             
            
    def __splitdatabuffer(self,splitstring):
         #this function splits our databuffer and returns the first half of it , then adds the rest back to the databuffer
         self.lines = self.databuffer.split(splitstring,1)
         self._log.debug("Buffer split using %s as EoL is : %s" %(splitstring,self.lines))
         self.databuffer = ''
         self.line = self.lines[0]
         self.lines.remove(self.line)
         for rest in self.lines:
            self.databuffer += rest         
         return self.line  
                   
    def readline(self):
        self.line = ''
        self.__buffer()
        if self.deliminator != '':
        #split up the current recieved data using our splitbuffer function
            if (self.deliminator in self.databuffer):
                self.line = self.__splitdatabuffer(self.deliminator)
            return self.line
        else:
            return self.read()
        #if ("\r\n"  in self.databuffer) | ("\n\r" in self.databuffer):
         #   self.rnindex = self.databuffer.find("\r\n")            
          #  self.nrindex = self.databuffer.find("\n\r")
           # 
            #if (self.rnindex < self.nrindex) & (self.rnindex != -1):
             #   self.line = self.__splitdatabuffer("\r\n")
            #    
           # else:
          #      self.line = self.__splitdatabuffer("\n\r")
         #check if the buffer contains any \n on their own        
        #elif "\n" in self.databuffer:
       #     self.line = self.__splitdatabuffer("\n")
      #      
     #   return self.line
        
    def read(self):
        self.__buffer()
        temp = self.databuffer
        self.databuffer = ''
        return temp
        
        

# $Id: TelnetWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
