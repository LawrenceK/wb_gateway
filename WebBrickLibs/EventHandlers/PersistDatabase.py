# $Id: PersistFile.py 2999 2008-12-17 17:42:15Z philipp.schuster $
#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Tom Bushby
#
#
import redis
import telnetlib
import logging
from os.path import join, split, abspath, exists
from os import rename, remove

from shutil import copy

import threading
import time

from xml.sax.saxutils import escape, unescape

from MiscLib.DomHelpers          import *

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred
from EventHandlers.BaseHandler import BaseHandler

# Import cPickle or pickle - used for serialising data. cPickle is the C version of pickle, which is faster.
try:
    import cPickle as pickle
except ImportError:
    import pickle

_log = logging.getLogger( "EventHandlers.PersistDatabase" )

class PersistDatabase( BaseHandler ):
    """
    Handle events saving persistant configuration and distribute configuration.
    <eventInterface module='EventHandlers.PersistDatabase' name='PersistDatabase' persistIP='127.0.0.1' persistPort='6379' persistDatabase='0'>
    </eventInterface>
    """

    def __init__ (self, localRouter):
        self._log = _log
        super(PersistDatabase,self).__init__(localRouter)
        # TODO: Do we need these?
        self._isUpdate = False
        self._subscribeTime = 30
        self._locked = threading.Lock()


    def configure( self, cfgDict ):
        """
        called with a dictionary that contains the configuration for self
        """
        _log.debug( 'configure' )

        if cfgDict.has_key('persistIP'):
            self._log.debug('Using persist IP %s', cfgDict['persistIP'])
            self._persistIP = cfgDict['persistIP']
        else:
            self._log.debug('No persist IP defined, using default IP 127.0.0.1')
            self._persistIP = '127.0.0.1'
        
        if cfgDict.has_key('persistPort'):
            self._log.debug('Using persist Port %s', cfgDict['persistPort'])
            self._persistPort = int(cfgDict['persistPort'])
        else:
            self._log.debug('No persist Port defined, using default Port 6379')
            self._persistPort = 6379
            
        if cfgDict.has_key('persistDatabase'):
            self._log.debug('Using persist Database %s', cfgDict['persistDatabase'])
            self._persistDatabase = cfgDict['persistDatabase']
        else:
            self._log.debug('No persist Database defined, using default Database 0')
            self._persistDatabase = '0'

        try:
            self._db = redis.Redis(self._persistIP, self._persistPort, self._persistDatabase)
        except Exception, ex:
            self._log.error("No Connection to database")
            self._log.exception( ex )

    def start(self):
        _log.debug( 'start' )
        self.__running = True
        self._localRouter.watch( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/config/get' )

        # subscribe to set so we can update persist data
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/runtime' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/config/set' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/minute' )

    def stop(self):
        _log.debug( 'stop' )
        self.__running = False
        self._localRouter.endWatch( self, 'http://id.webbrick.co.uk/events/config/get' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/config/set', '' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/runtime', '' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/minute' )

    def doDailyCompress( self ):
         tn = telnetlib.Telnet(self._persistIP, self._persistPort)
         self._log.debug(tn.read_eager())
         tn.write("BGREWRITEAOF\n")
         self._log.debug("Sent BGREWRITEAOF command")
         tn.close()


         
        
    def handleSet( self, inEvent ):

        key = inEvent.getType() + "," + inEvent.getSource()
        self._log.debug("Generated key %s", key)
  
        # Pickle used to serialise NVP data  
        result = self._db.set(key, pickle.dumps(inEvent.getPayload()))      
        if not result:
            self._log.error("Unable to set key %s with value %s, %s", key, inEvent.getPayload(), result)
        else:  
            self._log.info("Retrieved data from database: Key was %s and Result was %s\n", key, result)
            # let everyone know
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/config/get", 
                inEvent.getSource(), inEvent.getPayload() ) )    # copy other data as we may update

    def doPublishAll( self ):
        
        list = self._db.keys("*")
        for i in list:
            parts = i.split(",")
            evType = parts[0]
            evSource = parts[1]
            evPayload = {}
            evPayload.update(pickle.loads(self._db.get(i)))
        
            self.sendEvent( Event ( "http://id.webbrick.co.uk/events/config/get",
                    evSource, evPayload ) )
            

    def doHandleEvent( self, handler, inEvent ):
        if inEvent.getType() == "http://id.webbrick.co.uk/events/time/minute" :
            if int(inEvent.getPayload()["hour"]) == 2 and int(inEvent.getPayload()["minute"]) == 5:
                self.doDailyCompress()
    
        elif inEvent.getType() == "http://id.webbrick.co.uk/events/config/set" :
            self.handleSet( inEvent )

        elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/runtime" :
            if int(inEvent.getPayload()["elapsed"]) == 5:
                self.doPublishAll("")  # publish all the data.

        return makeDeferred(StatusVal.OK)

# End.       
# $Id$
