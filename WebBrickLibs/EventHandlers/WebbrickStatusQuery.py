# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import logging, string

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from MiscLib.NetUtils import getBroadcastAddress

from twisted.web import client

import WebBrickLibs.WbDefs

from WebBrickLibs.Wb6Config      import Wb6Config
from WebBrickLibs.Wb6Status      import *
from WebBrickLibs.WbUdpCommands  import sendUdpCommand
from WebBrickLibs.Wb6Commands    import resetSitePlayer

_log = None

class WebbrickStatusQuery( BaseHandler ):
    """
    This is an interim approach.

    Periodically request wbStatus from configured webbricks and send change events for any 
    values that have changed. Note for Analogue and Temperature values a different interval 
    may be chosen.
    """
    def __init__ (self, localRouter ):
        BaseHandler.__init__(self, localRouter)
        _log = self._log
        self._webbrickConfigs = dict()    # keyed by IP address and contains WbConfig objects.
        self._webbrickStati = dict()    # keyed by IP address and contains WbStatus objects.
        self._readFailCount = dict()    # keyed by IP address and contains a count of read errors

    def updateStatus( self, adrs, newSts ):
        # now look for changes in all values and generate correct events.
        if newSts.getOperationalState() == 255: # this is site-player reset value.
            # siteplayer has been reset, so data not valid.
            self._log.error( "read from webbrick %s with invalid status data %s" % (adrs, newSts.xmlstr) )
            # reset siteplayer.
            resetSitePlayer( adrs )
            return  # short circuit out of here

        oldSts = None
        if self._webbrickStati.has_key( adrs ) :
            oldSts = self._webbrickStati[adrs]

        nnr = self._webbrickConfigs[adrs][0]
        curCfg = self._webbrickConfigs[adrs][2]
        typeRoot = "http://id.webbrick.co.uk/events/webbrick/"
        srcRoot = "webbrick/%s" % nnr

        if not oldSts or ( oldSts.getLoginState() != newSts.getLoginState() ):
#            self.sendEvent( Event( typeRoot, srcRoot, {} ) )
            pass

        if not oldSts or ( oldSts.getDate() != newSts.getDate() ):
#            self.sendEvent( Event( typeRoot, srcRoot, {} ) )
            pass

        ow = newSts.getOneWireBus()
        for idx in range(WbDefs.TEMPCOUNT):
            if (ow & (0x01 << idx)) == 0:
                # sensor not there
                pass
            else:
                if not oldSts or ( oldSts.getTemp( idx ) != newSts.getTemp( idx ) ):

                    if newSts.getTemp( idx ) == -1000.0:
                        self._log.error( "Erroneous Temperature Reading %s %s" % (adrs, newSts.xmlstr) )
                        self.sendEvent( Event( typeRoot+"ET", 
                                "%s/ET/%i" % (srcRoot,idx) , 
                                { "fromNode": nnr, "srcChannel": idx, 
                                        "val": newSts.getTemp( idx ), 
                                        "curlo": newSts.getTempLowThresh( idx ),
                                        "curhi": newSts.getTempHighThresh( idx ),
                                        "deflo": curCfg.getTempTriggerLow( idx )["threshold"],
                                        "defhi": curCfg.getTempTriggerHigh( idx )["threshold"],
                                } ) )
                    else:
                        self.sendEvent( Event( typeRoot+"CT", 
                                "%s/CT/%i" % (srcRoot,idx) , 
                                { "fromNode": nnr, "srcChannel": idx, 
                                        "val": newSts.getTemp( idx ), 
                                        "curlo": newSts.getTempLowThresh( idx ),
                                        "curhi": newSts.getTempHighThresh( idx ),
                                        "deflo": curCfg.getTempTriggerLow( idx )["threshold"],
                                        "defhi": curCfg.getTempTriggerHigh( idx )["threshold"],
                                } ) )

        for idx in range(WbDefs.AOCOUNT):
            if not oldSts or ( oldSts.getAnOut( idx ) != newSts.getAnOut( idx ) ):
                self.sendEvent( Event( typeRoot+"AO", 
                        "%s/AO/%i" % (srcRoot,idx), 
                        { "fromNode": nnr, "srcChannel": idx, "val": newSts.getAnOut( idx ) } ) )

        for idx in range(WbDefs.AICOUNT):
            if not oldSts or ( oldSts.getAnIn( idx ) != newSts.getAnIn( idx ) ):
                self.sendEvent( Event( typeRoot+"AI", 
                        "%s/AI/%i" % (srcRoot,idx), 
                        { "fromNode": nnr, "srcChannel": idx, 
                                "val": newSts.getAnIn( idx ),
                                    "curlo": newSts.getAnInLowThresh( idx ),
                                    "curhi": newSts.getAnInHighThresh( idx ),
                                    "deflo": curCfg.getAnalogTriggerLow( idx )["threshold"],
                                    "defhi": curCfg.getAnalogTriggerHigh( idx )["threshold"],
                        } ) )

        for idx in range(WbDefs.DICOUNT):
            if not oldSts or ( oldSts.getDigIn( idx ) != newSts.getDigIn( idx ) ):
                state = 0
                if newSts.getDigIn( idx ):
                    state = 1
                self.sendEvent( Event( typeRoot+"DI", 
                        "%s/DI/%i" % (srcRoot,idx), 
                        { "fromNode": nnr, "srcChannel": idx, "state": state } ) )

        for idx in range(WbDefs.DOCOUNT+WbDefs.MIMICCOUNT):   # dig out 8-15 are the mimics.
            if not oldSts or ( oldSts.getDigOut( idx ) != newSts.getDigOut( idx ) ):
                state = 0
                if newSts.getDigOut( idx ):
                    state = 1
                self.sendEvent( Event( typeRoot+"DO", 
                        "%s/DO/%i" % (srcRoot,idx), 
                        { "fromNode": nnr, "srcChannel": idx, "state": state } ) )

        self._webbrickStati[adrs] = newSts
        return None

    def actionStatus( self, data, adrs ):
#        self._log.debug("wbStatus.xml success target %s" % (adrs) )
        self._log.debug("wbStatus.xml success target %s - %s" % (adrs, data) )
        # does 
        try:
            newSts = Wb6StatusXml( data )
            if self._webbrickConfigs[adrs]:
                self.updateStatus( adrs, Wb6StatusXml (data ) )
            else:
                self._log.error( "No wbconf.xml for: %s" %str(adrs) )
        except Exception, ex:
            self._log.exception( "actionStatus %s" % str(data) )

    def updateConfig( self, adrs, newCfg ):
        nnr = newCfg.getNodeNumber()
        nname = newCfg.getNodeName()
        self._webbrickConfigs[adrs] = (nnr,nname,newCfg)
        self._readFailCount[adrs] = 0
        self._log.info("Added %s - %s" % (adrs, self._webbrickConfigs[adrs]) )
        self.sendEvent( Event( "http://id.webbrick.co.uk/events/webbrick/config/nodename",  
                "webbrick/%s" % (nnr),
                { "fromNode": nnr, "nodename": nname, "ipAdr": adrs, "version":newCfg.getVersion()  } ) )

    def actionConfig( self, data, adrs ):
#        self._log.debug("wbCfg.xml success target %s" % (adrs) )
        self._log.debug("wbCfg.xml success target %s - %s" % (adrs, data) )
        try:
            self.updateConfig( adrs, Wb6Config( None, data ) )
        except Exception, ex:
            self._log.exception( "actionConfig %s" % str(data) )

    def clearWebBrick( self, adrs ):

        # loose status
        if self._webbrickConfigs.has_key( adrs ) and self._webbrickStati.has_key( adrs ) :
            # send clear events.
            nnr = self._webbrickConfigs[adrs][0]
            self._log.info("Drop %u: %s (%s)" % (nnr, self._webbrickConfigs[adrs][1], adrs) )
            # delete first, in case errors in event delivery.
            self._webbrickConfigs[ adrs ] = None
            del self._webbrickStati[adrs]
            del self._readFailCount[adrs]

            typeRoot = "http://id.webbrick.co.uk/events/webbrick/"
            srcRoot = "webbrick/%s" % nnr

            for idx in range(5):
                self.sendEvent( Event( typeRoot+"CT", 
                            "%s/CT/%i" % (srcRoot,idx) , 
                            { "fromNode": nnr, "srcChannel": idx } ) )

            for idx in range(4):
                self.sendEvent( Event( typeRoot+"AO", 
                            "%s/AO/%i" % (srcRoot,idx), 
                            { "fromNode": nnr, "srcChannel": idx } ) )

            for idx in range(4):
                self.sendEvent( Event( typeRoot+"AI", 
                            "%s/AI/%i" % (srcRoot,idx), 
                            { "fromNode": nnr, "srcChannel": idx } ) )

            for idx in range(12):
                self.sendEvent( Event( typeRoot+"DI", 
                            "%s/DI/%i" % (srcRoot,idx), 
                            { "fromNode": nnr, "srcChannel": idx } ) )

            for idx in range(8):
                self.sendEvent( Event( typeRoot+"DO", 
                            "%s/DO/%i" % (srcRoot,idx), 
                            { "fromNode": nnr, "srcChannel": idx } ) )

    def actionError( self, failure, adrs, url ):
        self._log.error("HTTP error %s target %s" % (failure,url) )
        self.clearWebBrick( adrs )
        return None

    def configureActions( self, cfgDict ):
        actions = list()

        if cfgDict.has_key("webbrick"):
            if isinstance( cfgDict["webbrick"], list ):
                for ntry in cfgDict["webbrick"]:
                    actions.append( ("webbrick", ntry["address"]) )
            else:
                actions.append( ("webbrick", cfgDict["webbrick"]["address"]) )

        if cfgDict.has_key("scan"):
            actions.append( ("scan",) )

        if cfgDict.has_key("recover"):
            actions.append( ("recover",) )

        if cfgDict.has_key("discoverFound"):
            actions.append( ("discoverFound",) )

        if cfgDict.has_key("discover"):
            if isinstance( cfgDict["discover"], list ):
                for ntry in cfgDict["discover"]:
                    actions.append( ("discover", ntry["address"]) )
            else:
                actions.append( ("discover", cfgDict["discover"]["address"]) )

#        self._log.debug("configureActions %s" % (actions) )
        return actions

    def startRetrieve( self, adrs ):
        """
        Issue an HTTP GEt to retrieve the WbStatus
        """
        url = str("http://%s/wbStatus.xml" % adrs )
        self._log.debug( 'startRetrieve %s' % (url) )
        client.getPage( url, followRedirect=0 ).addCallback( lambda data: self.actionStatus( data, adrs ) ).addErrback( lambda fail: self.actionError( fail, adrs, url ) )

    def startRecover( self, adrs ):
        """
        Issue an HTTP GET to retrieve the WbConfig
        """
        # need to retrieve config first.
        url = str("http://%s/wbcfg.xml" % adrs )
        self._log.debug( 'startRecover %s' % (url) )

        client.getPage( url, followRedirect=0 ).addCallback( lambda data: self.actionConfig( data, adrs ) ).addErrback( lambda fail: self.actionError( fail, adrs, url ) )

    def doWebBrick( self, action ):
        # instead of doing immediate retrieve, use to populate the list for next scan
        if not self._webbrickConfigs.has_key( action[1] ):
            self._webbrickConfigs[action[1]] = None

        # so system knows the address.
        self.sendEvent( Event( "http://id.webbrick.co.uk/events/webbrick/config/nodename",  
                "webbrick/%s" % (0),
                { "fromNode": 0, "nodename": "???", "ipAdr": action[1] } ) )

    def doRecover( self ):
        for adrs in self._webbrickConfigs:
            if self._webbrickConfigs[ adrs ] == None:
                self.startRecover( adrs )

    def doRetrieve( self ):
        for adrs in self._webbrickConfigs:
            if self._webbrickConfigs[ adrs ]:
                # can scan once retrieved config.
                self.startRetrieve( adrs )

    def doDiscover( self, action ):
        # send DA command
        ba = getBroadcastAddress( action[1] )
        self._log.debug( "discover %s, %s" % (action[1],ba) )
        #sendUdpCommand( ba, "LGpassword" )
        sendUdpCommand( ba, "DA" )

    def doDiscoverFound( self, action, inEvent ):
        # verify webbrick is in the address list
        od = inEvent.getPayload()
        if od.has_key("version") and od["version"] >= 6 :
            adrs = od["ipAdr"]
            if adrs == WbDefs.DEFAULT_SP_ADR:
                resetSitePlayer(adrs)
            elif not self._webbrickConfigs.has_key( adrs ):
                self._webbrickConfigs[adrs] = None

    def doActions( self, actions, inEvent ):
        """
        """
        self._log.debug( 'doActions %s' % (actions) )
        for action in actions:
            try:
                # we need to handle this on the reactor thread as it will
                # make network calls twisted is not thread safe!
                # defer import to here so we can install alternate reactors.
                from twisted.internet import reactor
                if ( action[0] == "webbrick" ):
                    self.doWebBrick( action )

                elif ( action[0] == "scan" ):
                    reactor.callFromThread( self.doRetrieve )

                elif ( action[0] == "recover" ):
                    reactor.callFromThread( self.doRecover )

                elif ( action[0] == "discover" ):
                    self.doDiscover( action )

                elif ( action[0] == "discoverFound" ):
                    self.doDiscoverFound( action, inEvent )

            except Exception, ex:
                self._log.exception( "doActions %s" % str(action) )
