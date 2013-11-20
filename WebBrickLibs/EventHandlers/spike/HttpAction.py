# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Lawrence Klyne
#
#
import logging, time, threading

from xml.sax.saxutils import escape, unescape

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from MiscLib.DomHelpers          import *

from WebBrickLibs.WbAccess       import DoHTTPRequest
from WebBrickLibs.WbAccess       import HTTPTimeout, WbAccessException

from twisted.web import client
from twisted.web.error import PageRedirect
#from twisted.web2 import client
#from twisted.web2.http import RedirectResponse

#
# WebBrick time event generator
#
# global queues
#_singleQueue = True
#_singleQueue = False

_doDelay = True
#_doDelay = False
_delayTime = 0.1

class HttpAction_singleton:
    def __init__ (self):
        # self._thread = threading.Thread( target=self.run )
        # self._thread.setDaemon(True)
        # self._thread.start()
        self._queues = {}
#        self._queue = []
        self._lastSend = {}

    def getQueue( self, adrs ):
 #       if _singleQueue:
 #           return self._queue
#            return self._queue

        if not self._queues.has_key( adrs ):
            self._queues[adrs] = list()
            self._lastSend[adrs] = time.time()
            #self._queues[adrs] = list()
        return self._queues[adrs]
        #return self._queues[adrs]

    def checkQueue( self, adrs ):
        # we should be on the reactor thread
        if _doDelay == True and (_delayTime + self._lastSend[adrs]) > time.time():
            _log.debug("Delay checkQueue")
            from twisted.internet import reactor
            reactor.callLater( _delayTime, self.checkQueue, adrs )
        else:
            self.actionStart( adrs )
    
    def delQueueEntry( self, adrs ):
        # we are on the recator thread
        Q = self.getQueue(adrs)
        del Q[0]
        self.checkQueue(adrs)

    def addQueueEntry_prim( self, adrs, ntry ):
        # we are on the recator thread
        Q = self.getQueue(adrs)
        Q.append( ntry )
        self.checkQueue(adrs)

    def addQueueEntry( self, adrs, action, url ):
        # ensure on reactor thread
        from twisted.internet import reactor
        reactor.callFromThread( self.addQueueEntry_prim, adrs, (action, url) )

    def actionSuccess( self, data, action ):
        # we do nothing with the response.
        lines = data
        _log.debug("HTTP %s success targetUrl http://%s%s %s" % (action["cmd"],action["address"],action["uri"],lines) )
        self.delQueueEntry(action["address"])

    def actionError( self, failure, action ):
        if isinstance(failure.value, PageRedirect):
            _log.debug("HTTP %s redirect targetUrl http://%s%s" % (action["cmd"],action["address"],action["uri"]) )
        else:
            _log.error("HTTP %s error %s targetUrl http://%s%s" % (failure,action["cmd"],action["address"],action["uri"]) )
        self.delQueueEntry(action["address"])

    def twistedGetPage( self, url, action ):
        client.getPage( url, followRedirect=0 ).addCallback( self.actionSuccess, action ).addErrback( self.actionError, action )

    def actionStart( self, adrs ):
        # start a new action if current count not to high
        # this done so as to limit number of outstanding requests
        # This is running on reactor thread so access to queues is safe
        Q = self.getQueue(adrs)
        if len(Q) > 0 and Q[0][1] is not None:
            # not yet started.
            url = Q[0][1]
            Q[0] = (Q[0][0],None) # now started delete URI
            _log.debug("HTTP start %s", url )
            self._lastSend[adrs] = time.time()
            self.twistedGetPage( url, Q[0][0])

    # def run(self):
        # _log.debug( 'enter run' )
        # while 1:
            # time.sleep(0.1)
            # from twisted.internet import reactor
            # for k in self._queues:
                # reactor.callFromThread( self.actionStart, k )
        # _log.debug( 'exit run' )

_log = logging.getLogger( HttpAction_singleton.__module__ )
http_sin = HttpAction_singleton()

class HttpAction( BaseHandler ):
    """
    Handle events targetting urls
    <eventInterface module='HttpAction' name='HttpAction'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/TD/0" >
                <!-- all events from a single source -->
            <event>
                    <params>
                    </params>
            <url cmd="GET" address="localhost:20999" uri="/test?medianame=ITunes&amp;mediacmd=volup" />
                    Test
            </event>
            </eventsource>
        </eventtype>
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
        super(HttpAction,self).__init__(localRouter)
        # keyed by target address, contains lists of uris
        # only used for GET commands
        # removed when action completed.
#        self._queues = {}
#        self._queue = []

    def configureActions( self, cfgDict ):
        result = None
        if cfgDict.has_key("url"):
            if isinstance( cfgDict["url"], list ):
                result = cfgDict["url"]
            else:
                result = list()
                result.append(cfgDict["url"])
        self._log.debug("configureActions %s" % (result) )
        return result

    def doActions( self, actions, inEvent ):
        self._log.debug("doActions %s", actions)
        if actions :
            self._log.debug("doActions %s", actions)
            for action in actions:
                try:
                    cmd = action["cmd"]
                    adrs = action["address"]
                    uri = action["uri"]

                    # has uri got any % symbols in it, attempt substitution
                    if inEvent.getPayload() and '%' in uri:
                        # the uri can contain string substitutions of the form %(key)s where
                        # the key is a key into other_data, the s is the string specifier.
                        # See String Formatting Operations in the python library ref.
                        uri = uri % inEvent.getPayload()

                    self._log.info("url address : %s command: %s uri: %s" % (adrs, cmd, uri) )
                    if ( cmd == "GET" ):
                        # TODO rate limit requests to a webbrick at one time
                        url = str("http://%s%s" % (adrs,uri))
                        # list operations are thread safe
                        http_sin.addQueueEntry( adrs, action, url )
                    else:
                        # TODO shift to twisted for POST
                        resp = DoHTTPRequest(adrs, cmd, uri)
                        if resp and (resp.status != 200) and resp.read():
                            self._log.error("HTTP error %i : %s in targetUrl" % (resp.status,resp.reason) )
                except Exception, ex:
                    self._log.exception( ex )
