#
#  Class to handle mapping of an event to one or more new events, mapping the value attribute.
#
#  Lawrence Klyne
#
#
import logging, string

from EventLib.Event import Event, makeEvent
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from icalendar import Calendar
#

#
class VacationEntry(object):
    
    def __init__ (self, startString, endString):
        self._start = startString
        self._end = endString
        
    def atStart(self, nowTime):
        return self._start == nowTime
    
    def atEnd(self, nowTime):
        return self._end == nowTime
        
    def onVacation(self, nowTime):
        return self._start >= nowTime and nowTime <= self._end
        
    def __str__(self):
        return 'Vacation from %s to %s' % (self._start, self._end)


class CalendarEvent( BaseHandler ):
    """
    This event interface is used to read an Ical file periodically and send at hoem or on vacation events as appropriate.

    The configuration for an CalendarEvent entry is as follows:

    <eventInterface module='EventHandlers.CalendarEvent' name='CalendarEvent' icalfile='path/to/calendarfile'>
    </eventInterface>

        eventtype, eventsource, event, params as as per BaseHandler.
        additonally is one or more newEvent elements that define the new event to be isssued. The type and source
        attributes of the newEvent element specify the event type and source. 
        
    """

    def __init__ (self, localRouter):
        super(CalendarEvent,self).__init__(localRouter)
        self._subscribeTime = 30
        self._entries = list()
        self._entries = [] 
        self._icalfile = ""
        self._currentStatus = None # 1 equals at home; 0 equals on Vacation; None means we have just started
        

    def start(self):
        self._log.debug( 'start' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/minute' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/runtime' )
        self.loadIcalSourceFile()
        
    def stop(self):
        self._log.debug( 'stop' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/minute', '' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/runtime', '' )
        
    def configure( self, cfgDict ):
        self._log.debug(cfgDict)
        if cfgDict.has_key("icalfile"):
            self._icalfile = cfgDict["icalfile"]
        
        
    
    def addVacation(self, event):
        self._log.debug(event)
        startDate = str(event['dtstart'])
        endDate = str(event['dtend']) 
        self._entries.append(VacationEntry(startDate, endDate))
    
    def loadIcalSourceFile( self ):
        try:
            if self._icalfile != "":
                cal = Calendar.from_string(open(self._icalfile,'rb').read())
                self._entries =[]
                for component in cal.walk('vevent'):
                    if component['summary'].strip().lower() == 'vacation:all':
                        self.addVacation(component)  
        except Exception, ex:
            self._log.exception(ex)
    
        for entry in self._entries:
            self._log.info(str(entry))
            
        # open ICal file
        # enumertae entries
        # look for summary that start Vacation:
        # identify End or Start
        # add entry to list of vacation times.
        # NOTE handle read error
        pass
        
    def checkVacationStatus( self, dt_str ):
        if self._currentStatus is None:
            self._log.debug(dt_str)
            self._currentStatus = 1
            for entry in self._entries:
                if entry.onVacation(dt_str):
                    self._currentStatus = 0
            self.sendEvent( makeEvent( 'http://id.webbrick.co.uk/events/config/set', 'occupants/home', {'val': self._currentStatus}) )
            
        else:
            pass
        #if first call
        #   if ical loaded
        #       locate current time and see whether between VacationStart/VacationEnd i.e. onVacation or not
        # send relevant event
        # else
        # if current time matches an entry send relevant event.
        pass
        
    def checkIcalSourceFile( self ):
        
        # check the timestamp of the file and if changed then reload.
        pass
        
    def doHandleEvent( self, handler, inEvent ):
        if inEvent.getType() == "http://id.webbrick.co.uk/events/time/minute" :
            od = inEvent.getPayload()
            curMin = od["minute"]
            if (curMin % 10) == 0:
                self.checkIcalSourceFile()
            self.checkVacationStatus( string.replace(string.replace(od["datetimestr"], "-", ""),":","") )
            # {'datetimestr': '2008-06-24T12:58:00', 'hour': 12, 'timestr': '12:58:00', 'month': 6, 'second': 0, 'datestr': '2008-06-24', 'year': 2008, 'date': 24, 'day': 2, 'minute': 58} 
        elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/runtime" :
            pass
        return makeDeferred(StatusVal.OK)    
        

