# $id:$
#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import logging, threading

import time
from datetime import datetime

from EventLib.Event import Event

from EventHandlers.BaseHandler import BaseHandler

from MiscLib.Sun import Sun

_log = logging.getLogger( "EventHandlers.TimeEventGenerator" )

class Wb6TimeEvent(Event):
    """
    Creates an event for current time
    """
    def __init__ (self, subType, now ):
        super(Wb6TimeEvent,self).__init__ (u'http://id.webbrick.co.uk/events/time/' + subType, u'time/' + subType, dict() )
        self._payload["second"] = now[5]
        self._payload["minute"] = now[4]
        self._payload["hour"] = now[3]
        self._payload["day"] = now[6]+1  # Sunday is day 0.
        if now[6] == 6:
            self._payload["day"] = 0
        self._payload["date"] = now[2]
        self._payload["month"] = now[1]
        self._payload["year"] = now[0]
        # ISO8601 based formats.
        self._payload["timestr"] = "%02u:%02u:%02u" % (now[3],now[4],now[5])
        self._payload["datestr"] = "%04u-%02u-%02u" % (now[0],now[1],now[2])
        self._payload["datetimestr"] = "%sT%s" % (self._payload["datestr"],self._payload["timestr"])
        self._payload["dayofyear"] = now[7]
        self._payload["week"] = int(now[7]/7)    # TODO update to be ISO week number

class Wb6TimeEventIsDark(Event):
    """
    Creates an event for isDark
    """
    def __init__ (self, isDark ):
        super(Wb6TimeEventIsDark,self).__init__ (u'http://id.webbrick.co.uk/events/time/isDark', u'time/isDark', {'state':isDark} )

class Wb6TimeEventRunTime(Event):
    """
    Creates an event for runtime
    """
    def __init__ (self, elapsed ):
        super(Wb6TimeEventRunTime,self).__init__ (u'http://id.webbrick.co.uk/events/time/runtime', u'time/runtime', {'elapsed':elapsed} )

#
# WebBrick time event generator
#
class TimeEventGenerator(BaseHandler):
    """
    Generate time based events.
    """

    def __init__ (self, localRouter ):
        self._log = _log
        super(TimeEventGenerator,self).__init__( localRouter )
        self._thread = None
        self.running = False
        self.sunRise = Sun()
        self._nextSunRise = (0,0)
        self._nextSunSet = (0,0)
        # london england
        self._lat = 51.5086
        self._long = -0.1264
        self._doSeconds = False
        self._runtimeStop = 900    # seconds, 15 minutes
        self.startup_delay = 30     # wait before sending any time events

    def configure( self, cfgDict ):
        """
        called with an XmlDom that contains the configuration for self
        """
        # save latitude and longitude
        if cfgDict.has_key("latitude"):
            valStr = cfgDict["latitude"]
            if ( valStr and (len(valStr) > 0 ) ):
                self._lat = float( valStr )
        if cfgDict.has_key("longitude"):
            valStr = cfgDict["longitude"]
            if ( valStr and (len(valStr) > 0 ) ):
                self._long = float( valStr )
        if cfgDict.has_key("interval"):
            valStr = cfgDict["interval"]
            if ( valStr ):
                self._doSeconds = (valStr == 'seconds')
        if cfgDict.has_key("runtime"):
            valStr = cfgDict["runtime"]
            if ( valStr and (len(valStr) > 0 ) ):
                self._runtimeStop = int( valStr )
        if cfgDict.has_key("startup_delay"):
            valStr = cfgDict["startup_delay"]
            if ( valStr and (len(valStr) > 0 ) ):
                self.startup_delay = int( valStr )

    # Terminate interface
    def stop(self):
        _log.debug( 'stop' )
        self.running = False

    def alive(self):
        return self._thread and self._thread.isAlive()

    def start(self):
        _log.debug( 'start' )
        self.running = True
        self._thread = threading.Thread( target=self.run )
        self._thread.setDaemon(True)
        self._thread.start()

    def _nextSunRiseSunSet(self):
        # get todays values, returned as Daylight saving time values.
        riseSet = self.sunRise.sunRiseSetDST( self._long, self._lat )
        _log.debug( 'next Sun Rise/Sun Set %s' % (riseSet,) )
        # convert values, they are 
        self._nextSunRise = time.gmtime(riseSet[0] * 3600)
        self._nextSunSet = time.gmtime(riseSet[1] * 3600)
        _log.debug( 'next Sun Rise %s' % (self._nextSunRise,) )
        _log.debug( 'next Sun Set %s' % (self._nextSunSet,) )

    def sendIsDark(self, nowSplit):
        # between sunset and midnight
        if ( nowSplit[3] > self._nextSunSet[3] ) or ( ( nowSplit[3] == self._nextSunSet[3] ) and ( nowSplit[4] >= self._nextSunSet[4] ) ):
            self.sendEvent( Wb6TimeEventIsDark( 1 ) )
        # between midnight and sunrise
        elif ( nowSplit[3] < self._nextSunRise[3] ) or ( ( nowSplit[3] == self._nextSunRise[3] ) and ( nowSplit[4] <= self._nextSunRise[4] ) ):
            self.sendEvent( Wb6TimeEventIsDark( 1 ) )
        else:
            # daytime
            self.sendEvent( Wb6TimeEventIsDark( 0 ) )
    
    def run(self):
        # stay in loop reading packets while socket open.
        _log.debug( 'enter run' )

        # let system settle a bit before we cause lots of work.
        if self.startup_delay > 0:
            # sleep may get terminated by signals.
            to = time.time() + self.startup_delay
            while to > time.time():
                time.sleep(1)   

        startTime = time.time()
        lastSend = startTime
        nowTime = startTime
        elapsed = 0
        self._nextSunRiseSunSet()

        nowSplit = time.localtime( lastSend )
        self.sendIsDark( nowSplit )

        while ( self.running == True ):

            try:
                # wait for next second or minute
                if self._doSeconds :
                    # rounded up to timer tick resolution to ensure not back until 
                    # next second.
                    st = (1015000.0 - float(datetime.now().microsecond) ) / 1000000.0
                else:
                    st = 60-time.localtime()[5]
                    if ( st > 10 ):
                        st = 10 # faster shutdown otherwise wait a long time.

                # throws occasional error 514 as sleep using select. google Errno 514 python
                # http://mail.python.org/pipermail/python-dev/2007-January/070626.html
                time.sleep(st)

                # generate events.
                nowTime = time.time()
                # we may of been shutdown in the meantime.
                while self.running == True and lastSend < nowTime:
                    # this while is in case ione of the time event loops takes too long.
                    lastSend = lastSend + 1
                    nowSplit = time.localtime( lastSend )

                    if self._doSeconds :
                        self.sendEvent( Wb6TimeEvent('second',nowSplit) )

                    # There is an issue that this could miss seconds.
                    if ( nowSplit[5] == 0 ): # seconds in case we change the above wait..
                        self.sendEvent( Wb6TimeEvent('minute',nowSplit) )
                        if ( nowSplit[4] == 0 ):   # new hour
                            self.sendEvent( Wb6TimeEvent('hour',nowSplit) )
                            if ( nowSplit[3] == 0 ): # new day
                                self._nextSunRiseSunSet()  # get next pair.
                                self.sendEvent( Wb6TimeEvent('day',nowSplit) )
                                self.sendEvent( Wb6TimeEvent('date',nowSplit) )
                                if ( nowSplit[2] == 1 ): # new month
                                    self.sendEvent( Wb6TimeEvent('month',nowSplit) )
                                    if ( nowSplit[1] == 1 ): # new year
                                        self.sendEvent( Wb6TimeEvent('year',nowSplit) )

                        # sunrise/sunset.
                        if ( nowSplit[3] == self._nextSunRise[3] ) and ( nowSplit[4] == self._nextSunRise[4] ):
                            self.sendEvent( Wb6TimeEvent('sunrise',nowSplit) )
                            self.sendEvent( Wb6TimeEventIsDark( 0 ) )  # not dark
                        if ( nowSplit[3] == self._nextSunSet[3] ) and ( nowSplit[4] == self._nextSunSet[4] ):
                            self.sendEvent( Wb6TimeEvent('sunset',nowSplit) )
                            self.sendEvent( Wb6TimeEventIsDark( 1 ) )  # is dark

                        # lightingupstart/lightingupend.
                        # daystart/dayend.

                    # This is unlikely to generate events if running using minute ticks.
                    elapsed = int(lastSend-startTime)
                    # generate events at 5 second intervals
                    if ( elapsed < self._runtimeStop ) and (( elapsed % 5 ) == 0):
                        self.sendEvent( Wb6TimeEventRunTime(elapsed) )

                    if ( elapsed < 120 ) and (( elapsed % 10 ) == 0):
                        # Every 10 seconds for 2 minutes.
                        # Need to send these for a while at startup otherwise sent before some sub systems have subscribed.
                        # TODO have this event generator subscribe to subscribe events so it can resend some of them
                        self.sendIsDark( nowSplit )

                # decide on 
                #<li>http://id.webbrick.co.uk/events/time/lightingupstart</li>
                #<li>http://id.webbrick.co.uk/events/time/lightingupend</li>
                #<li>http://id.webbrick.co.uk/events/time/daystart</li>
                #<li>http://id.webbrick.co.uk/events/time/dayend</li>
            except Exception, ex:
                _log.exception( ex )

        _log.debug( 'exit run' )
                
# $id:$
0