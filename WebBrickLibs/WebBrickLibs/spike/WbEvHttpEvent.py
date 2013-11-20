#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import logging, string

from WbEvent import WbEvent

from twisted.web import http
from twisted.internet import reactor

_log = logging.getLogger( "EventDespatch.WbEvHttpEvent" )
        
class WbEvHttpRequestHandler( http.Request ):
    """
    Listen for UDP webbrick events and turn them into events for passing to an event
    consumer.
    """
    def process(self):
        try:
            # self.path is event source
            _log.debug( "URL %s" % self.path )

            self.channel.factory.despatch.handleEvent( WbEvent( u'http://id.webbrick.co.uk/events/uri', self.path ) )

            self.write("Ok\r\n")

        except Exception, ex:
            _log.exception( ex )

        self.finish()

class WbEvHttpConnectionHandler( http.HTTPChannel ):
    requestFactory = WbEvHttpRequestHandler

class WbEvHttpEvent( http.HTTPFactory ):
    """
    Listen for HTTP events and turn them into events for passing to an event
    consumer.
    """
    protocol = WbEvHttpConnectionHandler

    def __init__ (self, despatch ):
        self.despatch = despatch
        self.running = True

    def configure( self, cfgDict ):
        """
        called with an XmlDom that contains the configuration for self
        """
        self.listenPort = int( cfgDict['listenPort'] )
        _log.debug( "listen on %i" % self.listenPort )

    # Terminate interface
    def stop(self):
        _log.debug( 'stop' )
        if self.listener:
            self.listener.stopListening()
        self.running = False

    def alive(self):
        return self.running

    def start(self):
        _log.debug( 'start' )
        self.listener = reactor.listenTCP( self.listenPort, self )
