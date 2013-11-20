# $Id: WbDiscover.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
"""
WebBrick discovery
"""

import time, logging

from WbUdpEventReceiver import WbUdpEventReceiver
from WbUdpCommands import sendUdpCommand
from WbEvent import WbEventTarget
from Wb6Config import Wb6Config

from MiscLib.NetUtils import getBroadcastAddress, parseNetAdrs, parseIpAdrs, ipInNetwork
from MiscLib.Logging  import Trace

class Discover( WbEventTarget ):
    """
    Helper class that deals with WebBrick discovery by sending out a 
    UDP probe message and listening for responses.
    """
    def __init__( self, network, forTime ):
        self.__log      = logging.getLogger( "WebBrickGateway.WbDiscover" )
        self._network   = network
        self._netbytes  = parseNetAdrs(network)
        self._webbricks = dict()
        self._forTime   = forTime

    def getWebBricks( self ):
        receiver = WbUdpEventReceiver( self )
        receiver.start()

        # send attention request
        #TODO: confirm password not needed for probe message
        #sendUdpCommand( getBroadcastAddress( self._network ), "LGpassword" )
        sendUdpCommand( getBroadcastAddress( self._network ), "DA" )

        # wait for events to be received.
        time.sleep( self._forTime )
        receiver.stop()
        # turn result dict into list.
        self.__log.debug( "result %s" % self._webbricks )
        return self._webbricks.values()

    def handleEvent( self, inEvent ):
        try:
            self.handleEvent1( inEvent )
        except Exception, e:
            self.__log.debug( 'Event handler raises: %s' % (str(e)) )

    def handleEvent1( self, inEvent ):
        self.__log.debug( 'Event %s : %s' % (inEvent.source(), inEvent.type()) )
        #self.__log.debug( 'Event.other_data %s' % (inEvent.other_data()) )
        if ( inEvent.type() == "http://id.webbrick.co.uk/events/webbrick/NN" ) or \
           ( inEvent.type() == "http://id.webbrick.co.uk/events/webbrick/AA" ):
            macStr = inEvent.other_data()["macAdr"]
            wb = None
            if self._webbricks.has_key( macStr ):
                # already seen
                wb = self._webbricks[macStr]
                #TODO: update values?
            else:
                # new entry: filter out responses from other networks
                ipStr   = inEvent.other_data()["ipAdr"]
                ipbytes = parseIpAdrs(ipStr)
                if ipInNetwork(ipbytes, self._netbytes):
                    wb = dict()
                    wb["macAdr"] = macStr
                    wb["ipAdr"]  = ipStr
                    self._webbricks[macStr] = wb
                    self.__log.debug( "new %s" % wb )
            if wb and inEvent.type() == "http://id.webbrick.co.uk/events/webbrick/NN":
                wb["unconfigured"] = True

# Main functions provided

def WbDiscover( network, forTime = 5 ):
    """
    This function looks for webbricks on the provided network.

    The network parameter is in the form nn.nn.nn.nn/bits and identifies 
    a subnet accessible to the current computer.

    The result is a list of dictionaries where there is a dictionary entry for each 
    discovered webbrick. The dictionary contains the ip and mac address for a webbrick
    the attribute unconfigured may also be present and if it is then the webbrick
    is sending newnode packets.

    Should this be a dictionary keyed by MAC address? Still enables for nod in discover.
    """
    disc = Discover( network, forTime )
    return disc.getWebBricks()

def WbDiscoverFull(network, forTime = 5):
    """
    This is an enhancement of WbDiscover that returns additional information about the 
    WebBricks discovered, for WebBricks with unique IP addresses
    """
    WebBricks = WbDiscover(network, forTime)
    byip = {}
    for wb in WebBricks:
        ip = wb["ipAdr"]
        if byip.has_key(ip):
            byip.append(wb)
        else:
            byip[ip] = [wb]
    wbfull = []
    for (ip,wbs) in byip.items():
        for wb in wbs:
            if len(wbs) == 1:
                # get details of WebBrick with address 'ip'
                #TODO: sort out attention status
                Trace("IP address %s" % ip, "WbDiscoverFull")
                WbDiscoverCheck(ip, wb)
            else:
                # Duplicate address; just use defaults
                wb["nodeNum"]   = None
                wb["nodeName"]  = None
                wb["attention"] = True
            wbfull.append(wb)
    return wbfull

def WbDiscoverCheck(ipadrs,wb=None):
    """
    Return directory of WebBrick properties given an IP address, or None
    If a dictionary is supplied the new values are added to that, 
    otherwise a new dictionary is created.
    """
    Trace(ipadrs,"WbDiscoverCheck")
    wbcfg = Wb6Config(ipadrs)
    if wbcfg.getConfigXml():
        if not wb: wb = {"ipAdr": ipadrs}
        wb["macAdr"]    = wbcfg.getMacAddress()
        wb["nodeNum"]   = wbcfg.getNodeNumber()
        wb["nodeName"]  = wbcfg.getNodeName()
        wb["attention"] = False
    else:
        wb = None
    return wb

# End. $Id: WbDiscover.py 2612 2008-08-11 20:08:49Z graham.klyne $
