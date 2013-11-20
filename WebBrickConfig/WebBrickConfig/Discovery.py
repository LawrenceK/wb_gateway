# $Id: Discovery.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
"""
WebBrick discovery
"""

import time, logging

from EventLib.Event         import Event
from EventLib.Status        import StatusVal
from EventLib.SyncDeferred  import makeDeferred

from EventLib.EventHandler  import EventHandler

from WebBrickLibs.Wb6Config import Wb6Config
from WebBrickLibs.WbUdpCommands import sendUdpCommand

from MiscLib.NetUtils import getBroadcastAddress, parseNetAdrs, parseIpAdrs, ipInNetwork
from MiscLib.Logging import Trace

class DiscoverHandler( EventHandler ):
    """
    Helper class that deals with WebBrick discovery by subscribing to the correct events.
    """
    def __init__( self ):
        super(DiscoverHandler,self).__init__("http:\\id.webbrick.co.uk\handlers\Discovery", self.doHandleEvent)
        self.__log      = logging.getLogger( "WebBrickGateway.WbDiscover" )
        self._webbricks = dict()
        self.subcribeTimeout = 30

    def start( self, despatch ):
        # subscribe to all required events.
        despatch.subscribe( self.subcribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/SS", "" )
        despatch.subscribe( self.subcribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/NN", "" )
        despatch.subscribe( self.subcribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/AT", "" )
        despatch.subscribe( self.subcribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/AA", "" )
        despatch.subscribe( self.subcribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/ST", "" )    # webbricks send heartbeat
        despatch.subscribe( self.subcribeTimeout, self, "http://id.webbrick.co.uk/events/time/minute", "time" )

    def stop( self, despatch ):
        # subscribe to all required events.
        despatch.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/SS", "" )
        despatch.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/NN", "" )
        despatch.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/AT", "" )
        despatch.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/AA", "" )
        despatch.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/ST", "" )    # webbricks send heartbeat
        despatch.unsubscribe( self, "http://id.webbrick.co.uk/events/time/minute", "time" )

    def startDiscovery( self, network ):
        ba = getBroadcastAddress( network )
        self.__log.debug( "startDiscovery %s, %s" % (network,ba) )
        # send attention request
        #TODO: confirm password not needed for probe message
        #sendUdpCommand( ba, "LGpassword" )
        sendUdpCommand( ba, "DA" )

    def getWebBricks( self, network ):
        result = list()
        # turn result dict into list.
        self.__log.debug( "result %s" % self._webbricks )

        netbytes = parseNetAdrs(network)
        # now filter out all unwanted webbricks.
        for ntry in self._webbricks:
            wb = self._webbricks[ntry]
            ipbytes = parseIpAdrs( wb["ipAdr"] )
            if ipInNetwork(ipbytes, netbytes):
                result.append( wb )
        return result

    def doHandleEvent( self, handler, inEvent ):
        try:
            if inEvent.getType() == "http://id.webbrick.co.uk/events/time/minute":
                self.handleMinute( inEvent )
            else:
                self.handleDiscoveryEvents( inEvent )
        except Exception, e:
            self.__log.exception( 'Event handler raises: %s' % (str(e)) )
        return makeDeferred(StatusVal.OK)

    def handleMinute( self, inEvent ):
        """
        Remove webbricks that have not beeen seen for a while.

        It should be remembered that in most setups the WebbrickStatusQuery will be using discovery
        periodically. So we check every 5 minutes.
        """
        if ( inEvent.getPayload()["minute"] % 5 ) == 0 :
            for mac in self._webbricks.keys():
                wb = self._webbricks[mac] 
                if wb["count"] == 1:
                    del self._webbricks[mac]
                else:
                    wb["count"] = wb["count"] - 1

    def handleDiscoveryEvents( self, inEvent ):
        self.__log.debug( 'Event %s : %s' % (inEvent.getSource(), inEvent.getType()) )
        #self.__log.debug( 'Event.other_data %s' % (inEvent.getPayload()) )
        od = inEvent.getPayload()
        # TODO enhance to just accept IP address and query for MAC address if needed.
        if od and od.has_key("macAdr") and od.has_key("ipAdr") \
           and od.has_key("version") and ( od["version"] >= 6 ):
            # valid V6 event
            macStr = od["macAdr"]
            ipStr   = od["ipAdr"]
            wb = None
            if self._webbricks.has_key( macStr ):
                # already seen
                wb = self._webbricks[macStr]
                wb["count"] = wb["count"] + 1
                #TODO: update values?
            else:
                # new entry
                wb = dict()
                wb["macAdr"] = macStr
                wb["count"] = 1
                self._webbricks[macStr] = wb
                self.__log.debug( "new %s" % wb )
            wb["ipAdr"]  = ipStr    # in case it has changed
            if wb and inEvent.getType() == "http://id.webbrick.co.uk/events/webbrick/NN":
                wb["unconfigured"] = True

# Main functions provided
def WbDiscoverFull( disc, network, forTime = 0):
    """
    This is an enhancement of WbDiscover that returns additional information about the 
    WebBricks discovered, for WebBricks with unique IP addresses
    """
    disc.startDiscovery(network)
    # wait for events to be received.
    time.sleep( forTime )
    WebBricks = disc.getWebBricks(network)
    byip = {}
    for wb in WebBricks:
        ip = wb["ipAdr"]
        if byip.has_key(ip):
            byip[ip].append(wb)
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
    try:
        wbcfg = Wb6Config(ipadrs)
        if wbcfg.getConfigXml():
            if not wb: wb = {"ipAdr": ipadrs}
            wb["macAdr"]    = wbcfg.getMacAddress()
            wb["nodeNum"]   = wbcfg.getNodeNumber()
            wb["nodeName"]  = wbcfg.getNodeName()
            wb["attention"] = False
        else:
            wb = None
    except Exception, ex:
        log = logging.getLogger( "WebBrickGateway.WbDiscover.WbDiscoverCheck" )
        log.error( "Wb6Config from %s" % ( ipadrs ) )
        log.exception( ex )
        wb = None
    return wb

# End. $Id: Discovery.py 2612 2008-08-11 20:08:49Z graham.klyne $
