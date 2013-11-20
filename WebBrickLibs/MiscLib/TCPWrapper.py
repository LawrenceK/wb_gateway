# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TCPWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
# This class uses sockets to read and write from a standard tcp connection

import socket ,logging , select,threading


class TCPWrapper():
    def __init__(self,hostname,port,deliminator =13,offset = 0):
        #the number of times we should attempt to send or receive before throwing an exception
        self.retrycount = 100
        #public member to indicated whether connected or not
        self.connected = False
        #using this lock to make the methods thread safe
        self.lock = threading.Lock()
        #the offset is the number of bytes to read after we receive the deliminator
        self.offset = offset
        #the deliminator is the byte that denotes where a message ends
        self.deliminator = deliminator
        #port number
        self.port = port
        #hostname
        self.hostname = hostname
        #the buffer to store incoming data in
        self.databuffer =''
        self._log = logging.getLogger ( "TCPWrapper" )
        try:
            #attempt to create an outgoing socket connection to the address/port
            self.tcpConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.tcpConnection.connect((hostname,port))
            #we need the socket to be in non blocking mode 
            self.tcpConnection.setblocking(0)
            #we should be ready to performance I/Os now
            self.connected = True
        except Exception,ex:
            #exceptions here are probably caused by a host refusing a connection or not existing
            self.tcpConnection = None
            self._log.exception("Exception while connecting to tcp server : %s" %str(ex))
            
    def close(self):
        #we lock to ensure nobody is writing or reading to the socket
        self.lock.acquire()
        try:
            self.tcpConnection.close()
        except Exception,ex:
            #probably because the server is already closed
            self.tcpConnection = None 
            self.connected = False
            self._log.debug(self.error)
            self._log.exception("Exception while closing connection to tcp server : %s" %str(ex))
        finally:
            #we always release the lock when we are done
            self.lock.release()    
        
    def write(self,word):
        #lock so nobody can read/close while we are writing
        self.lock.acquire()
        try:
            counter = 0
            #this is a short loop that is nessecary incase select fails the first time
            while True:
                #use select to ensure we are ready for writing                    
                _read,_write,_error = select.select([self.tcpConnection],[self.tcpConnection],[self.tcpConnection])
                if self.tcpConnection in _write:
                    #we use sendall to ensure we send the entirity of the data
                    self.tcpConnection.sendall(word)
                    break
                else:
                    #not ready yet, increase counter and try again, throw an exception if our retry count is too high
                    counter += 1
                    if counter > self.retrycount:
                        raise Exception("TCPConnection not ready to write after %i retrys" %counter)    
        except Exception,ex:
            #exception occured so we log our info and drop the connection
            self.tcpConnection = None
            self.connected = False
            self._log.debug("Problem while writing to tcp server: %s %i "  %(self.hostname,self.port))
            raise    
        finally:
            self.lock.release()      
                   
    def __buffer(self):
        #lock so nobody can write/close while we are reading
        self.lock.acquire()
        try:
            if self.connected:
                _read,_write,_error = select.select([self.tcpConnection],[self.tcpConnection],[self.tcpConnection])
                if self.tcpConnection in _read:
                    self.databuffer += self.tcpConnection.recv(1024)                       
                    
            else:
                #tcp socket not connected
                raise Exception("TCPConnection is not connected")                          
        except Exception,ex:
                #if an exception occurs we drop the connection and log the hostname and port then raise the exception again
                self.tcpConnection = None
                self.connected = False
                self._log.error("Problem while reading from tcp server: %s %i "  %(self.hostname,self.port))
                raise
        finally:
            #always release the lock!
            self.lock.release()     
            
    def __splitdatabuffer(self,splitstring):
         #this function splits our databuffer and returns the first half of it , then adds the rest back to the databuffer
         deliminatorindex = self.databuffer.find(self.deliminator)
         line = ''
         if deliminatorindex != -1:
            if len(self.databuffer) >= (deliminatorindex + 1 + self.offset):
                #we use deliminator + 1 + offset because the offset is the number of characters AFTER the deliminator we should include   
                line = self.databuffer[:deliminatorindex + 1 + self.offset]
                self.databuffer = self.databuffer[deliminatorindex + 1 + self.offset:]
         return line
                   
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

        
    def read(self):
        self.__buffer()
        temp = self.databuffer
        self.databuffer = ''
        return temp
        
        

# $Id: TCPWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
