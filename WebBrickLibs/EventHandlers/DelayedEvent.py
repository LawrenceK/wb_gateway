# $Id: DelayedEvent.py 2748 2008-09-16 11:46:38Z lawrence.klyne $
#
#  Class to sending events after a delay
#
#  Lawrence Klyne
#
#
import logging

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from Utils import makeNewEvent

_log = None

class DelayedEventEntry:
    """
    Delays measured in seconds.
    """
    def __init__( self, delay, events ):
        self._delay = int(delay)
        self._events = events

    def delta( self ):
        return self._delay

    def expired( self ):
        return self._delay <= 0

    def decrement( self, by = 1 ):
        self._delay = self._delay - by

    def __str__(self):
        return "DeltaEntry delay %s %s" % ( self._delay, self._events)

#
# 
#
class DelayedEvent( BaseHandler ):
    """
    A delayed job is a set of events to send after a delay of minutes or seconds. .

    The configuration for an DelayedEvent entry is as follows:

    <eventInterface module='DelayedEvent' name='DelayedEvent'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
	        <event>
                    <params>
                    </params>
                    <delay delayMinutes="1">
                        <newEvent type="local/url" source="local/HwOn">
                            <other_data val1="1"/>
                            <copy_other_data state="state"/>
                        </newEvent>
                    </delay>
	        </event>
            </eventsource>
            <eventsource source="webbrick/100/TD/7" >
	        <event>
                    <params>
                    </params>
                    <delay delaySeconds="15">
                        <newEvent type="local/url" source="local/NotToBeTriggerred">
                            <other_data val1="7"/>
                            <copy_other_data state="state"/>
                        </newEvent>
                    </delay>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

        eventtype, eventsource, event, params as as per BaseHandler.
        additonally is one or more newEvent elements that define the new event to be isssued. The type and source
        attributes of the newEvent element specify the event type and source. 
        
        The delay element has a delay time attribute and one or more newEvent elements.

        The newEvent element may contain:
        an other_data element which specifies constant name value pairs for the other data in the new event.
        a copy_other_data element which is used to control copying of other_data attributes from the original event,
        within this each attribute name is used as an attribute name fro the new event and the attribute value 
        specifies an attribute name within the original event. This enables identity mapping or name changing.
    
    """

    def __init__ (self, localRouter):
        super(DelayedEvent,self).__init__(localRouter)
        global _log
        _log = self._log
        self._subscribeTime = 30

    def start(self):
        self._waiting = list()  # a list of DelayedEventEntry's
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/second', 'time/second' )
        super(DelayedEvent,self).start()

    def stop(self):
        self._waiting = list()  # clear outstanding entries, TODO possibly log them?
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/second', 'time/second' )
        super(DelayedEvent,self).stop()

    def configureActions( self, cfgDict ):
        #_log.debug("configureActions %s" % (cfgDict) )
        result = None
        if cfgDict.has_key("delay"):
            if isinstance( cfgDict["delay"], list ):
                result = cfgDict["delay"]
            else:
                result = list()
                result.append(cfgDict["delay"])
        _log.debug("configureActions %s" % (result) )
        return result

    def doActions( self, delays, inEvent ):
        if delays:
            for delay in delays:
                _log.debug( 'createDelay %s' % (delay) )
                # a delay entry has delayMinutes or delaySeconds attribute 
                # a newEvent list/entry.
                secs = 0
                if delay.has_key( "delayMinutes" ):
                    secs = int(delay["delayMinutes"]) * 60
                if delay.has_key( "delaySeconds" ):
                    secs = secs + int(delay["delaySeconds"])
                if delay.has_key( "delayHours" ):
                    secs = secs + int(delay["delayHours"]) * 3600

                newEvents = list()
                if isinstance( delay["newEvent"], list ):
                    for newEvent in delay["newEvent"]:
                        newEvents.append( makeNewEvent( newEvent, inEvent, None ) )
                else:
                    newEvents.append( makeNewEvent( delay["newEvent"], inEvent, None ) )

                # insert into list at correct point
                ntry = DelayedEventEntry(secs,newEvents)
                idx = 0
                #_log.debug( 'insert into %s self %s ' % (self._waiting, ntry) )
                while idx < len(self._waiting):
                    #_log.debug( 'insert %i Test self %i against %i ' % (idx, ntry.delta(), self._waiting[idx].delta()) )
                    if (self._waiting[idx].delta() > ntry.delta() ):
                        # insert here
                        self._waiting[idx].decrement( ntry.delta() )
                        self._waiting.insert( idx, ntry )
                        break
                    else:
                        ntry.decrement( self._waiting[idx].delta() )
                        idx = idx + 1
                if idx >= len(self._waiting):
                    # onto end of list
                    self._waiting.append( ntry )
                _log.info( 'createdDelay %s' % (ntry) )

    def checkDelays( self ):
        while (len(self._waiting) > 0) and self._waiting[0].expired():
            # trigger and remove event
            ntry = self._waiting.pop(0)
            _log.debug( 'trigger and remove event %s' % ( ntry ) )
            for event in ntry._events:
                self.sendEvent( event )
            
        # update next element timeout.
        if len(self._waiting) > 0:
            self._waiting[0].decrement()
#            _log.debug( 'decrement %i %s:%s' % (self._waiting[0]._delay, self._waiting[0]._type, self._waiting[0]._source) )

    def doHandleEvent( self, handler, inEvent ):
        """
        Override base class to pick up second events.
        """
        if inEvent.getType() == "http://id.webbrick.co.uk/events/time/second":
            self.checkDelays()
            return makeDeferred(StatusVal.OK)

        return super(DelayedEvent,self).doHandleEvent( handler, inEvent )

