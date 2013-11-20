# $Id: WebBrickMonitor.py 2996 2008-12-02 14:31:18Z andy.harris $
#
"""
WebBrick Set time
"""

import time, logging
from os import system

from MiscLib.NetUtils import arpCacheFlush

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from WebBrickLibs.Wb6Commands import Wb6Commands
from WebBrickLibs.WbUdpCommands  import sendUdpCommand
from WebBrickLibs.Wb6Commands    import resetSitePlayer
import WebBrickLibs.WbDefs as WbDefs

_log = logging.getLogger( "EventHandlers.WebBrickMonitor" )

# time out of step for circa 3 minutes
SETTIME_THRESHOLD = 3

# circa 3 minutes to discover
SPRESET_THRESHOLD = 2

# maximum of 120 seconds out before we reset.
CLOCK_MAX_ERROR = 120

class WebBrickMonitor( BaseHandler ):
    """
    event handler that will reset webbrick clocks if they do not know the time, i.e.
    no RTC or RTC failed.

    TODO Also need to read RTC periodically and adjust as required.

    """
    def __init__ (self, localRouter):
        self._log = _log
        super(WebBrickMonitor,self).__init__(localRouter)
        self._SpCounters = dict()
        self._ClockCounters = dict()
        self._resetWebIfTimer = SPRESET_THRESHOLD
        self._resetClocktimer = SETTIME_THRESHOLD
        self._clockMaxError = CLOCK_MAX_ERROR
        self._subscribeTime = 30
        self._resetOnDefault = 0    # reset siteplayer if on default IP address

    def start( self ):
        # subscribe to all required events.
        self._localRouter.subscribe( self._subscribeTime, self, "http://id.webbrick.co.uk/events/webbrick/SS", "" )
        self._localRouter.subscribe( self._subscribeTime, self, "http://id.webbrick.co.uk/events/webbrick/ST", "" )
        self._localRouter.subscribe( self._subscribeTime, self, "http://id.webbrick.co.uk/events/time/minute", "time/minute" )
        self._localRouter.subscribe( self._subscribeTime, self, "http://id.webbrick.co.uk/events/time/hour", "time/hour" )

    def stop( self ):
        # subscribe to all required events.
        self._localRouter.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/SS", "" )
        self._localRouter.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/ST", "" )
        self._localRouter.unsubscribe( self, "http://id.webbrick.co.uk/events/time/minute", "time/minute" )
        self._localRouter.unsubscribe( self, "http://id.webbrick.co.uk/events/time/hour", "time/hour" )

    def alive(self):
        return False

    def configure( self, cfgDict ):
        """
        called with a dictiopnary that contains the configuration for self
        """
        if cfgDict.has_key( "webReset" ):
            try:
                self._resetWebIfTimer = int(cfgDict["webReset"])
            except Exception, ex :
                _log.debug( "webReset '%s' invalid", cfgDict["webReset"])
                self._resetWebIfTimer = SPRESET_THRESHOLD

        if cfgDict.has_key( "clockReset" ):
            try:
                self._resetClocktimer = int(cfgDict["clockReset"])
            except Exception, ex :
                _log.debug( "clockReset '%s' invalid", cfgDict["clockReset"])
                self._resetClocktimer = SETTIME_THRESHOLD

        if cfgDict.has_key( "clockMaxError" ):
            try:
                self._clockMaxError = int(cfgDict["clockMaxError"])
            except Exception, ex :
                _log.debug( "clockMaxError '%s' invalid", cfgDict["clockMaxError"])
                self._clockMaxError = CLOCK_MAX_ERROR

        if cfgDict.has_key( "noDefaultReset" ):
            try:
                self._resetOnDefault = int(cfgDict["resetOnDefault"])
            except Exception, ex :
                _log.debug( "resetOnDefault '%s' invalid", cfgDict["resetOnDefault"])
                self._resetOnDefault = 0    # reset siteplayer if on default IP address

        _log.info( "configure web timer %u, clock timer %u MaxClockError %u seconds resetOnDefault:%u" % (self._resetWebIfTimer, self._resetClocktimer, self._clockMaxError, self._resetOnDefault) )

    def doHandleEvent( self, handler, inEvent ):
        try:
            if inEvent.getType() == "http://id.webbrick.co.uk/events/time/minute":
                self.handleMinute( inEvent )
            elif inEvent.getType() == "http://id.webbrick.co.uk/events/webbrick/SS":
                self.handleStarted( inEvent )
            elif inEvent.getType() == "http://id.webbrick.co.uk/events/webbrick/ST":
                self.handleTimeSignal( inEvent )
            elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/hour":
                self.handleHour( inEvent )
        except Exception, e:
            _log.exception( 'Event handler raises: %s' % (str(e)) )
        return makeDeferred(StatusVal.OK)

    def handleStarted( self, inEvent ):
        _log.info( "handleStarted %s" % (self._ClockCounters) )
        od = inEvent.getPayload()
        if od and od.has_key("ipAdr"):
            tgt = od["ipAdr"]
            if self._ClockCounters.has_key( tgt ):
                self._ClockCounters[tgt] = self._ClockCounters[tgt] + 1
            else:
                self._ClockCounters[tgt] = 1

    def handleHour( self, inEvent ):
        """
        """
        od = inEvent.getPayload()
        if od and od.has_key("hour") and (od["hour"] == 3) and self._SpCounters:
            # reset all site players now.
			# PS temporarily commented out due to possible instability 
			pass
            # for tgt in self._SpCounters:
            #     resetSitePlayer( tgt )

    def handleMinute( self, inEvent ):
        """
        """
        #_log.debug( "handleMinute %s" % (self._SpCounters) )

        # if entry goes positive then clock needs resetting as getting SS or ST meddages with clock more 
        # then a configurable number of seconds out of step.
        od = inEvent.getPayload()
        for tgt in self._SpCounters:
            self._SpCounters[tgt] = self._SpCounters[tgt] + 1
            if self._SpCounters[tgt] > self._resetWebIfTimer:
                self._SpCounters[tgt] = 0
                # webbrick has not sent any UDP events for a period of time
                resetSitePlayer( tgt )

        for tgt in self._ClockCounters.keys():
            if self._ClockCounters[tgt] > self._resetClocktimer:
                # webbrick has not picked up time from RTC or RTC is too far out of step.
                self._log.info( "SetTime on node %s " % tgt )
                cmd = Wb6Commands(tgt)
                cmd.Login( "password" )
                cmd.SetTime( od["day"], od["hour"], od["minute"] )
                del self._ClockCounters[tgt]

    def handleTimeSignal( self, inEvent ):
        # If time from webbrick is more than x away from Gateway reset it.
        od = inEvent.getPayload()

        if od and od.has_key("ipAdr"):
            tgt = od["ipAdr"]

            self._SpCounters[tgt] = 0  # reset site player monitor

            if od["uptime"] < 5:    # minutes
                _log.info( "Webbrick %s rebooted reason %u" % (tgt, od["resetCode"]) )

            if tgt == WbDefs.DEFAULT_IP_ADR:
                # on default IP address
                _log.info( "Webbrick %s on default IP address" % (tgt) )
                if self._resetOnDefault:
                    resetSitePlayer( tgt )

            if tgt == WbDefs.DEFAULT_SP_ADR:
                # on default Siteplayer IP address
                _log.info( "Webbrick %s on default siteplayer IP address" % (tgt) )
                resetSitePlayer( tgt )

            # add to monitor list
            if od.has_key("hour") and od.has_key("minute") and od.has_key("second"):
                now = time.time() % 86400   # in seconds today.
                wbNow = od["second"] + (60 * od["minute"]) + (3600 * od["hour"])
                if ( abs(now-wbNow) > self._clockMaxError ):
                    # let the minute handle and system started code handle this.
                    if self._ClockCounters.has_key(tgt):
                        self._ClockCounters[tgt] = self._ClockCounters[tgt] + 1
                    else:
                        self._ClockCounters[tgt] = 1
                    _log.info( "Webbrick %s clock error(%i) - %s" % (tgt, self._ClockCounters[tgt], od) )
                else:
                    if self._ClockCounters.has_key(tgt):
                        del self._ClockCounters[tgt]


# End. $Id: WebBrickMonitor.py 2996 2008-12-02 14:31:18Z andy.harris $
