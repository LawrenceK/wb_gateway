# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#

import logging, threading, sys, time

from twisted.python import log

from EventHandlers.BaseHandler import BaseHandler

from MiscLib.TwistedLogObserver import TwistedLogObserver

dummyCallTime = 0.5

#
# WebBrick time event generator
#
class TwistedReactor(BaseHandler, threading.Thread):
    """
    Helper to start the Twisted Reactor
    """

    def __init__ (self, localRouter):
        BaseHandler.__init__(self, localRouter)
        self.__running = False
        threading.Thread.__init__(self)
        self.setDaemon( True )
        self._debug = False
        self._reactor = "select"
        pass

    def configure( self, cfgDict ):
        """
        called with an XmlDom that contains the configuration for self
        """
        if cfgDict.has_key("debug"):
            self._debug = cfgDict["debug"] == "yes"
        if cfgDict.has_key("reactor"):
            self._reactor = cfgDict["reactor"]

    # Terminate interface
    def stop(self):
        self._log.debug( 'stop' )
        from twisted.internet import reactor
        reactor.callFromThread( reactor.stop )
        maxSleep = 15
        while self.__running and maxSleep > 0:
            time.sleep(1)
            maxSleep = maxSleep - 1
        reactor.crash()
        
        self._tlog.stop()
        self._tlog = None
        
    def start(self):
        self._log.debug( 'start' )
        self._tlog = TwistedLogObserver()
        self._tlog.start()

        self.__running = True
        threading.Thread.start(self)

    def alive(self):
        return self.__running

    def dummyCall(self):
        # dummy function to be called later on a looping call.
        #reactor.callLater( dummyCallTime, self.dummyCall )
        pass

    def run(self):
        self._log.debug( 'enter run' )
        try:
#
# With Coherence around we cannot guarantee to run early enough to chose a reactor
# So if you get errors here select the platform default reactor.
#
            if self._reactor == "poll":
                from twisted.internet import pollreactor
                pollreactor.install()

            from twisted.internet import reactor

            self._log.debug( 'twisted reactor is %s', sys.modules['twisted.internet.reactor'] )

            #from twisted.internet import task
            #l = task.LoopingCall(self.dummyCall)
            #l.start(dummyCallTime)

            reactor.run(installSignalHandlers=0)
        except Exception, ex:
            self._log.exception( ex )

        self.__running = False
        self._log.debug( 'exit run' )
