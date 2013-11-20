import threading,logging,time,Queue

class WrapperReactor(threading.Thread):
    def __init__(self):
        self._log = logging.getLogger( "WrapperReactor" )
        self.wrapperlistLock = threading.Lock()        
        self._wrapperList = []
        threading.Thread.__init__(self)  
        self.setDaemon( True )
        self.start()
        self.finished = False

    def addWrapper(self,wrapperID,wrapper,callback,mode):
        try:
            self.wrapperlistLock.acquire()
            self._log.debug('\nAdding new wrapper with info %s %s %s %s' %(wrapperID,wrapper,callback,mode))
            wrapperDict = {'wrapperid' : wrapperID ,'wrapper':wrapper,'callback':callback,'mode':mode} 
            self._wrapperList.append(wrapperDict)
            self.wrapperlistLock.release()
    
        except Exception,E:
            self._log.exception(E)
 
    def wrapperList(self):
        return self._wrapperList
 
    def removeWrapper(self,wrapperID):
        self.wrapperlistLock.acquire()
        for x in range(0,len(self._wrapperList)):
            if self._wrapperList[x]['wrapperid'] == wrapperID:
                self._log.debug("removing wrapper %s" %self._wrapperList[x])
                self._wrapperList.remove(self._wrapperList[x])                
                break
        self.wrapperlistLock.release()
                
    def start(self):    
        self._log.debug('\nStarting read thread')
        threading.Thread.start(self)
        
       
    def stop(self):
        self.running = False
        time.sleep(1)
  
    def run(self):
        try:
            #connect the wrappers
            
            self.data = ''
            self.running = True
            while self.running:
                self.wrapperlistLock.acquire()
                for wrapperinfo in self._wrapperList:     
                    try:    
                        if not wrapperinfo['wrapper'].connected:
                                wrapperinfo['wrapper'].connect()
                                self._log.debug("Wrapper connected %s" %wrapperinfo)
                        if wrapperinfo['mode'] == 'readline':
                                self.data = wrapperinfo['wrapper'].readline()
                        elif wrapperinfo['mode'] == 'read':
                                self.data = wrapperinfo['wrapper'].read()                           
                    
                    except Exception, E:
                        self._wrapperList.remove(wrapperinfo)
                        wrapperinfo['wrapper'] = None    
                        self._log.error(E)
                    
                    if self.data != '':
                        try:
                            self._log.debug('\nFound data %s' %self.data)
                            wrapperinfo['callback'](wrapperinfo['wrapperid'],self.data)
                            self.data = ''
                        except Exception, E:
                            self._log.exception(E)
                self.wrapperlistLock.release()
                time.sleep(0.01)               
        finally:
            self._log.info('\n terminating')
            self.running = False         
                                 
