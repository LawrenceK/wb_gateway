# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import logging, string, threading, socket
from SocketServer import StreamRequestHandler, TCPServer

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

_log = None
        
class AsteriskRequestHandler(StreamRequestHandler):

    def handle(self):
        _log.debug( "from %s" % (str(self.client_address)) )
        # self.request, self.client_address, self.server
        # self.request is a socket
        # self.wfile write stream on socket
        # self.rfile read stream on socket
        try:
            other_data = {}
            # READ all attributes.
            line = self.rfile.readline().strip()
            while line:
                _log.debug( "line %s" % line )
                # parse and create dictionary
		key,value = line.split( ':', 1 )
                other_data[key.strip()] = value.strip()
                line = self.rfile.readline().strip()

            ev = Event( "http://id.webbrick.co.uk/events/asterisk", "asterisk/%s" % (self.client_address[0]), other_data )
            _log.debug( "%s", ev )
            self.server.handler.sendEvent( ev )

        except Exception, ex:
            _log.exception( ex )
            pass

class Asterisk( BaseHandler, threading.Thread ):
    """
    Listen for asterisk FASTAGI requests and turn into appropriate events.
    """

    def __init__ (self, localRouter ):
        threading.Thread.__init__(self)
        BaseHandler.__init__(self, localRouter)
        global _log
        _log = self._log
        self.setDaemon( True ) # when main thread exits stop server as well
        self.running = False
        self.LOCALHOST = ''
        self.listenPORT = 4573   # default from webbrick.

    def configure( self, cfgDict ):
        """
        called with an XmlDom that contains the configuration for self
        """
        if cfgDict.has_key('listenPort'):
            self.listenPORT = int(cfgDict['listenPort'])
        _log.debug( "listen on %i" % self.listenPORT )

    # Terminate interface
    def stop(self):
        _log.debug( 'stop' )
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect(("localhost", self.listenPORT))
        skt.close()
        self.running = False

    def alive(self):
        return self.running

    def start(self):
        _log.debug( 'start' )
        self.running = True
        threading.Thread.start( self )

    def run(self):
        _log.debug( "run start" )
        try :
            self.tcpServer = TCPServer( ('',self.listenPORT), AsteriskRequestHandler)
            self.tcpServer.handler = self
            while ( self.running ):
                self.tcpServer.handle_request() 
        except Exception, ex:
            self._log.exception( ex )
        self.running = False
        _log.debug( "run exit" )
