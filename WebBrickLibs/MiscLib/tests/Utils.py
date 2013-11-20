# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

import socket , select , time , logging , threading
 
class TestTCPServer(threading.Thread):

    def __init__(self,port=23):
    
        self.port = port
        self.lock = threading.Lock()
        threading.Thread.__init__(self)
        self.serversocket = None
        self.setDaemon( True ) #close when main thread closes
        self.haveLine = False  # indicate whether we managed to recieve something
        self.lastlines = []
        self.sendbuffer = ''
        self.clientsocket = None
        self.ready = threading.Event()
        self.data = ''
        self._log = logging.getLogger( "TestTCPServer" )
    def run(self):
        self.running = True
        self.serversocket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(('',self.port)) #accept connections over localhost loopback only
        self.serversocket.listen(1) # only want one connection in the listen queue
        self.ready.set()
        self.serversocket.setblocking(0)
        
        while self.running & (self.serversocket != None) & (self.clientsocket == None):
            waiting_connections , waiting_writes , in_error = select.select([self.serversocket],[self.serversocket],[self.serversocket],0)
            if self.serversocket in in_error:
                self.running = false
                self._log.exception("Server errored before client connected")
                self.running = false
                break
            if self.serversocket in waiting_connections:
                (self.clientsocket,self.address) = self.serversocket.accept()                  
        
                           
            while True:
                self.lock.acquire()
                try:
                    if self.running & (self.clientsocket != None) & (self.serversocket != None):
                        self.ready_to_read, self.ready_to_write , self.in_error = select.select([self.clientsocket],[self.clientsocket],[self.clientsocket],0)
                        if (self.sendbuffer != '') & (self.clientsocket in self.ready_to_write):
                           self._log.debug("\nTCP server is sending ##%s##" %self.sendbuffer)
                           self.clientsocket.send(self.sendbuffer)
                           self.sendbuffer = ''
                        elif self.clientsocket in self.ready_to_read:
                            self.data =  self.data + self.clientsocket.recv(1024)  # append any incoming data to any old data we have               
                        if self.clientsocket in self.in_error:
                            break
                    else:
                        break                        
                except Exception,ex:
                    self.running = False
                    self._log.exception(ex)
                finally:
                    self.lock.release()

        if self.serversocket != None:
            self.serversocket.close()   
        if self.clientsocket != None:
            self.clientsocket.close()
        self.running = False
        
    def clear(self):
        self.data = ''
    
    def send(self,send):
        self.lock.acquire()
        self.sendbuffer += send
        self.lock.release()
                  
    def start(self):    
        threading.Thread.start( self )
        time.sleep( 0.5 ) #wait for startup to finish
        
    def read(self):    
        return self.data      
         
    def stop(self):
      self.lock.acquire()
      self.running = False
      if self.serversocket != None:
        self.serversocket.close()
      if self.clientsocket != None:
        self.clientsocket.close()
      self.lock.release()  
    def data(self):    
        return self.data
    
