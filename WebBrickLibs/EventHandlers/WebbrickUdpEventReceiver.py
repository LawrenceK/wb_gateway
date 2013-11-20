# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: WebbrickUdpEventReceiver.py 3182 2009-06-01 16:22:23Z philipp.schuster $
#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import socket, logging, threading, time
import errno

from EventLib.Event import Event

from EventLib.EventAgent import EventAgent
from EventLib.EventHandler import EventHandler

from EventHandlers.BaseHandler import BaseHandler
from EventHandlers.Utils import *

from WebBrickLibs.Wb6Commands    import resetSitePlayer
import WebBrickLibs.WbDefs as WbDefs

_log = logging.getLogger( "EventHandlers.WebbrickUdpEventReceiver" )

# webbrick 5 event decoder
class Wb5Event(Event):
    """
    Creates an event from a UDP packet received from a version 5 webbrick
    """
    def __init__ (self, adr, data):
        super(Wb5Event,self).__init__( u'http://id.webbrick.co.uk/events/webbrick/', u'webbrick', dict() )

        self._payload["ipAdr"] = str(adr[0])
        self._payload["udpType"] = "G"
        self._payload["pktType"] = "??"
        self._payload["version"] = 5

        if ( data[0] == "R" ):
            self._payload["pktType"] = "TD"
            self._payload["udpType"] = "R"
            self._payload["toNode"] = ord(data[1])
            self._payload["tgtChannel"] = ord(data[3])
            if ( data[2] == "D" ):
                self._payload["tgtType"] = 0
            else:
                # analogue
                self._payload["tgtType"] = 2
                self._payload["setPoint"] = ord(data[5])
        elif ( data[0:2] == "NN" ):
            self._payload["pktType"] = "NN"
            # thats it
        elif ( data[0:2] == "LT" ):
            self._payload["udpType"] = "A"
            self._payload["pktType"] = "Tt"
            self._payload["fromNode"] = ord(data[2])
            self._payload["val"] = ord(data[3]) * 16   # into 1/16ths to match DS18B20/Wb6
            # high or low? use temperature and limits to decide.
            if ( ord(data[3]) > ord(data[6]) ) :
                self._payload["pktType"] = "TT"
        elif ( data[0:2] == "LA" ):
            self._payload["udpType"] = "A"
            self._payload["pktType"] = "Ta"
            self._payload["fromNode"] = ord(data[3])
            if ( ord(data[2]) == "H" ) :
                self._payload["pktType"] = "TA"
            self._payload["val"] = ord(data[4]) + ( ord(data[5]) << 8)
        elif ( data[0:2] == "DI" ):
            self._payload["pktType"] = "TD"
            self._payload["fromNode"] = ord(data[2])
            self._payload["srcChannel"] = ord(data[3])
            # UDPString[4] = operand ;  // Ignore
        elif ( data[0:2] == "LI" ):
            # digital in generated alarm packet
            self._payload["udpType"] = "A"
            self._payload["pktType"] = "TD"
            self._payload["fromNode"] = ord(data[2])
            self._payload["srcChannel"] = ord(data[3])
        elif ( data[0:2] == "St" ):
            self._payload["pktType"] = "SS"
            self._payload["fromNode"] = ord(data[5])
        else:
            self._payload["pktType"] = data[0:2]

        self._evtype = u'http://id.webbrick.co.uk/events/webbrick/%s' % self._payload["pktType"] 
        if self._payload.has_key("fromNode"):
            if self._payload.has_key("srcChannel"):
                self._source = u'webbrick/%i/%s/%i' % (self._payload["fromNode"],self._payload["pktType"],self._payload["srcChannel"])
            else:
                self._source = u'webbrick/%i' % self._payload["fromNode"]
        else:
            self._source = u'webbrick/%s' % self._payload["ipAdr"]

# webbrick 6 decoder
class Wb6Event(Event):
    """
    Creates an event from a UDP packet from a version 6 webbrick
    """
    def __init__ (self, adr, data):
        """
        data is the array of bytes fom the network.
        """
        super(Wb6Event,self).__init__( u'http://id.webbrick.co.uk/events/webbrick/', u'webbrick', dict() )

        self._payload["ipAdr"] = str(adr[0])
        self._payload["udpType"] = data[1]
        self._payload["pktType"] = data[2:4]
        self._payload["version"] = 6

        if ( self._payload["pktType"] == "NN" ) or ( self._payload["pktType"] == "AA" ):
            self._payload["macAdr"] = "%02X:%02X:%02X:%02X:%02X:%02X" % (ord(data[4]), ord(data[5]),ord(data[6]),ord(data[7]),ord(data[8]),ord(data[9]) )
            self._source = u'webbrick/%s/%s' % (self._payload["ipAdr"],self._payload["pktType"])
        elif ( self._payload["pktType"] == "RR" ):
            self._payload["rtc"] = [ord(data[4]), ord(data[5]),ord(data[6]),ord(data[7]),ord(data[8]),ord(data[9]),ord(data[10]),ord(data[11]) ]
            self._source = u'webbrick/%s' % self._payload["ipAdr"]
        else:
            self._payload["fromNode"] = ord(data[7])

            if ( self._payload["pktType"] == "SS" ):
                pass
            elif ( self._payload["pktType"] == "ST" ):
                self._payload["hour"] = ord(data[4])
                self._payload["minute"] = ord(data[5])
                self._payload["resetCode"] = ord(data[6])
                self._payload["second"] = ord(data[8])
                self._payload["day"] = ord(data[9])
                self._payload["uptime"] = (ord(data[10]) * 256) + ord(data[11])
            elif ( self._payload["pktType"] == "DB" ):
                self._payload["uptime"] = (ord(data[5]) * 256) + ord(data[4])
                self._payload["debug"] = "%x:%x:%x:%x:%x:%x" % data[6:11]
            elif ( self._payload["pktType"] == "AO" ):
                self._payload["srcChannel"] = ord(data[4])
                self._payload["val"] = (ord(data[10]) * 256) + ord(data[11])
            elif ( self._payload["pktType"] == "AI" ):
                self._payload["srcChannel"] = ord(data[4])
                self._payload["val"] = (ord(data[10]) * 256) + ord(data[11])
            elif ( self._payload["pktType"][0] == "T" ):
                self._payload["srcChannel"] = ord(data[4])
                self._payload["tgtChannel"] = ord(data[5]) & 0x1F
                #self._payload["val"] = (ord(data[10]) * 256) + ord(data[11])
                self._payload["action"] = ord(data[6]) & 0xF
                self._payload["dwell"] = ord(data[6]) >> 4
                self._payload["setPoint"] = ord(data[9])
                if ( self._payload["pktType"][1] == "D" ):
                    self._payload["val"] = (ord(data[10]) * 256) + ord(data[11])
                elif ( self._payload["pktType"][1] == "R" ):
                    self._payload["toNode"] = ord(data[8])
            elif ( self._payload["pktType"] == "DO" ):
                self._payload["srcChannel"] = ord(data[4])
                action=ord(data[6]) & 0xF
                if action == 2:
                    self._payload["state"] = 1
                else:
                    self._payload["state"] = 0
            elif ( self._payload["pktType"] == "IR" ):
                self._payload["irAddress"] = ord(data[8])
                self._payload["irChannel"] = ord(data[5])
            elif ( self._payload["pktType"] == "CT" ):
                self._payload["srcChannel"] = ord(data[4])
                # Check if the temperature reading is valid
                if ((ord(data[10]) * 256) + ord(data[11])) == 32767:
                    self._payload["pktType"] = "ET"
                    self._payload["val"] = -1000.0
                else:    
                    tmp = (((ord(data[10]) & 0x0F) * 256) + ord(data[11]))
                    if tmp > 2047:
                        tmp = tmp-4096  # negative
                    self._payload["val"] = round( (tmp / 16.0), 1)  # to tenth of a degree
            else:
                # Unrecognised event type...
                self._payload["srcChannel"] = ord(data[4])
                self._payload["tgtType"] = ord(data[5]) >> 6
                self._payload["tgtChannel"] = ord(data[5]) & 0x1F
                self._payload["action"] = ord(data[6]) & 0xF
                self._payload["dwell"] = ord(data[6]) >> 4
                self._payload["toNode"] = ord(data[8])
                self._payload["setPoint"] = ord(data[9])
                self._payload["val"] = (ord(data[10]) * 256) + ord(data[11])

            if self._payload.has_key("srcChannel"):
                self._source = u'webbrick/%i/%s/%i' % (self._payload["fromNode"],self._payload["pktType"],self._payload["srcChannel"])
            elif self._payload.has_key("irAddress"):
                self._source = u'webbrick/%i/%s/%i/%i' % (self._payload["fromNode"],self._payload["pktType"],self._payload["irAddress"],self._payload["irChannel"])
            else:
                self._source = u'webbrick/%i' % self._payload["fromNode"]
        self._evtype = u'http://id.webbrick.co.uk/events/webbrick/%s' % self._payload["pktType"] 

# TODO This needs extending to generate different event format dependant on the 
# pkttype. At present it is either debug or serial data in the payload.
class WB6BinaryEvent(Event):
    def __init__ (self, adr, data):
        super(WB6BinaryEvent,self).__init__( u'http://id.webbrick.co.uk/events/webbrick/%x' % (ord(data[1])), 
                    u'webbrick/%u/%u' % ( ord(data[2]), ord(data[1])) , dict() )
        self._payload["ipAdr"] = str(adr[0])
        # convert udpType to packet type
        self._payload["pktType"] = ("%x" % (ord(data[1])))
        self._payload["fromNode"] = ord(data[2])
        self._payload["seqNr"] = ord(data[3])
        #GK: This is the old code - I think it's wrong:  ***** TODO - check me *****
        #### self._payload["data"] = data[4:(ord(data[0])+1)]
        #GK: What I think it should be:
        self._payload["data"] = data[4:ord(data[0])]

#
# Singleton object for socket that listens for webbrick events
#
# Thus, multiple (serial) instances of the WebbrickUdpEventReceiver object will use
# the same socket object, avoiding problems encountered trying to create new socket
# instance (had observed address still in use errors)
#

LOCALHOST = ''
WbPORT    = 2552   # default from webbrick.
WebBrickSocket = None

def getWebBrickSocket():
    global WebBrickSocket
    global WbPORT
    global LOCALHOST
    if not WebBrickSocket: 
        WebBrickSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        WebBrickSocket.settimeout( 2 )  # so we shutdown?
        WebBrickSocket.bind((LOCALHOST, WbPORT))
        _log.debug( 'buffer size %i' % (WebBrickSocket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)) )
        WebBrickSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        _log.debug( 'New buffer size %i' % (WebBrickSocket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)) )
    return WebBrickSocket

def closeWebBrickSocket():
    global WebBrickSocket
    if WebBrickSocket:
        try:
            WebBrickSocket.shutdown( socket.SHUT_RDWR )
            WebBrickSocket.close()
        except socket.error, err:
            _log.exception( err )
        WebBrickSocket = None 

#
# WebBrick UDP event receiver
#

class WebbrickUdpEventReceiver(BaseHandler):
    """
    Listen for UDP webbrick events and turn them into events for passing to an event
    consumer.
    """

    def __init__ (self, localRouter):
        self._log = _log
        super(WebbrickUdpEventReceiver,self).__init__( localRouter )
        self.running = False
        self._thread = None

    def configure( self, cfgDict ):
        """
        called with an XmlDom that contains the configuration for self
        """
        global WbPORT
        if cfgDict.has_key('listenPort'):
            WbPORT = int(cfgDict['listenPort'])
        self._log.debug( "listen on %i" % WbPORT )

    # Terminate interface
    def stop(self):
        self._log.debug( 'stop' )
        self.running = False
        self.closeSocket()

    def closeSocket(self):
        ### closeWebBrickSocket() ???
        self.WbSkt = None

    def alive(self):
        return self._thread and self._thread.isAlive()

    def start(self):
        self._log.debug( 'start' )
        self.running = True
        self._thread = threading.Thread( target=self.run )
        self._thread.setDaemon(True)
        self._thread.start()

    def run(self):
        # stay in loop reading packets while socket open.
        self._log.debug( 'enter run' )
        seqNrs = dict()
        try:
            # bind socket
            self.WbSkt = getWebBrickSocket()
            while ( self.running ):
                # read packet
                try:
                    data = self.WbSkt.recvfrom(32)
                    if data and self.running:
                        evnt = None
                        adr = str(data[1][0])
                        if adr == WbDefs.DEFAULT_SP_ADR:
                            resetSitePlayer( adr )  # then events do not get beyond here.
                        else:
                            self._log.debug( 'Receive %s' % str(data) )
                            # create WbUdpEvents
                            # Wb 6 UDP packets have a length byte in the first position, use to decide on 5 or 6.
                            len = ord(data[0][0])
                            if  len < 32 :
                                if ( ord(data[0][1]) >= 32 ):
                                    # lets filter out duplicates
                                    # simple approach that only handles duplicates when
                                    # appear immediatly.
                                    if len >= 13:    # contains sequenece number
                                        sn = ord(data[0][12])
                                        if (not seqNrs.has_key(adr)) or seqNrs[adr] <> sn:
                                            seqNrs[adr] = sn
                                            evnt = Wb6Event( data[1], data[0] )
                                        else:
                                            self._log.debug( 'Duplicate %i' % sn  )
                                    else:
                                        evnt = Wb6Event( data[1], data[0] )
                                else:
                                    # len, type, from, seq, 
                                    sn = ord(data[0][3])
                                    if (not seqNrs.has_key(adr)) or seqNrs[adr] <> sn:
                                        seqNrs[adr] = sn
                                        evnt = WB6BinaryEvent( data[1], data[0] )
                                    else:
                                        self._log.debug( 'Duplicate %i' % sn  )
                            else:
                                evnt = Wb5Event( data[1], data[0] )

                        # call eventTgt method.
                        if (evnt):
                            self._log.debug( evnt )
                            self.sendEvent( evnt )

                    # end if data
                except socket.error, err:
                    if err[0] == errno.EINTR:
                        continue    # ignore error
                    if err[0] == errno.EAGAIN:
                        continue    # ignore error
                    if (str(err) != "timed out") and not self.running:
                        self._log.exception( err )
                except Exception, ex:
                    self._log.exception( ex )
            self.closeSocket()
        except Exception, ex:
            self._log.exception( ex )

        self._log.debug( 'exit run' )
                
# End. $Id: WebbrickUdpEventReceiver.py 3182 2009-06-01 16:22:23Z philipp.schuster $
