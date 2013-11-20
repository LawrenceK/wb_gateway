# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Philipp Schuster
#
#
import logging

from xml.sax.saxutils import escape, unescape

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from MiscLib.DomHelpers          import *

import telnetlib 
import time



_log = None

# Limit the number of ports that can be opened at one time to ONE
_remotePorts = {}

class Connection:

    def __init__(self, adrs):
        if ":" in adrs:
            self._host = str(adrs.split(":")[0])
            self._port = str(adrs.split(":")[1])
        else: 
            self._host = adrs
            self._port = "23"
        
        self._portopen = False
        self._queue = []
        
    def addToQueue( self, data):
        self._queue.append(data)
        
    def sendData (self):
        try:
        
            while self._portopen:
                _log.info( "Port Already Open... " )
                time.sleep(0.5)  
            self._portopen = True
            _log.info("client address: %s    port: %s" % (self._host, self._port) )
            tn = telnetlib.Telnet(self._host,self._port)

            # Write data one byte at a time.
            
            while len(self._queue) > 0:
                data = self._queue[0]
                byte_list = data.split(";")
                for b in byte_list:
                    tn.write(chr(int(b)))
            
                del self._queue[0]
            # Close the port on remote host
            
            tn.close()
            time.sleep(1)  
            self._portopen = False
        except Exception, ex:
            _log.exception( ex )
            
        
class RemotePort( BaseHandler ):
    """
    Handle events targetting urls
    <eventInterface module='EventHandler.RemotePort' name='RemotePort'>
        
        
    </eventInterface>

    The interface specific configuration is handled within the url element. Where the cmd attribute is
    the HTTP command, typically GET. The address is the server IP/DNS address and port number if not 80. the
    uri attribute is the uri to be passed to the server for retrieval.

    The uri get strings substituted into it from the event other data attributes.

    The value substition is handled by Python standard string formatting using a look up dictionary. 
    For general use this means that a string of the form %(key)s is replaced by looking up key in the 
    event other data attributes.

    See the event specific configuration for keys into the event other data. 
    """
    def __init__ (self, localRouter):
        global _log
        super(RemotePort,self).__init__(localRouter)
        _log = self._log
    
    def sendData(self, adrs, data):
        global _remotePorts
        if not _remotePorts.has_key( adrs ):
            _remotePorts[adrs] = Connection(adrs)
        
        _log.info("remotePorts: %s" % (_remotePorts) )
        _remotePorts[adrs].sendData(data)
    
    def addToQueue(self, adrs, data):
        global _remotePorts
        if not _remotePorts.has_key( adrs ):
            _remotePorts[adrs] = Connection(adrs)
        
        _log.info("Adding Data to Queue" % (_remotePorts) )
        _remotePorts[adrs].addToQueue(data)
    
    def sendAll(self):
        _log.info("Send all data" % (_remotePorts) )
        for i in _remotePorts:
            _remotePorts[i].sendData()
    
    def configureActions( self, cfgDict ):
        result = None
        if cfgDict.has_key("port"):
            if isinstance( cfgDict["port"], list ):
                result = cfgDict["port"]
            else:
                result = list()
                result.append(cfgDict["port"])
        _log.debug("configureActions %s" % (result) )
        return result

    def doActions( self, actions, inEvent ):
        _log.debug("doActions %s", actions)
        if actions:
            _log.debug("doActions %s", actions)
            for action in actions:
                try:
                    cmd = action["cmd"]
                    adrs = action["address"]
                    data = action["data"]

                    # has uri got any % symbols in it, attempt substitution
                    if inEvent.getPayload() and '%' in data:
                        # the uri can contain string substitutions of the form %(key)s where
                        # the key is a key into other_data, the s is the string specifier.
                        # See String Formatting Operations in the python library ref.
                        data = data % inEvent.getPayload()

                    _log.info("client address: %s    command: %s    data: %s" % (adrs, cmd, data) )
                    if ( cmd == "write" ):
                        # Check if the address specifies a port otehr wise use default
                        self.addToQueue(adrs, data)
                        
                    else:
                        _log.error("RemotePort cmd unknown: %s" % (cmd) )
                except Exception, ex:
                    _log.exception( ex )
            self.sendAll()