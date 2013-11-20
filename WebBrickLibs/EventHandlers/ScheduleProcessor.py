# $Id: ScheduleProcessor.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Lawrence Klyne
#
#
import logging

import turbogears
import cherrypy

import logging

from EventLib.Event import Event, makeEvent
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from MiscLib.DomHelpers import *

_log = None

days = "SMTWtFs"

class aScheduleEntry(object):
    def __init__ (self):
        self._days = list()
        self._time = ""
        self._devices = dict()

    def setDays(self, dayStr):
        self._days = list()
        for idx in range(7):
            if days[idx] in dayStr:
                self._days.append(idx)

    def setTime(self, timeStr):
        # validate string?
        self._time = timeStr

    def doNow(self, dy, ti):
        return ti == self._time and dy in self._days

    def getDevices(self):
        for devKey in self._devices:
            yield (devKey,self._devices[devKey])
        return

    def updateDevice(self, devname, action ):
        if not self._devices.has_key(devname):
            self._devices[devname] = action
        else:
            self._devices[devname] = action

class aSchedule(object):
    def __init__ (self):
        self._enabled = True
        self._entries = dict()

    def setEnabled(self, enable):
        # validate string?
        es = str(enable).lower()
        self._enabled = enable or es == "1" or es == "true" or es == "yes"

    def update(self, args, params ):
        if len(args) > 2:
            if not self._entries.has_key(args[2]):
                self._entries[args[2]] = aScheduleEntry()
            # now update
            if len(args) > 3:
                # device
                self._entries[args[2]].updateDevice(args[3], params )
            else:
                # time, day, enable
                if params.has_key("day"):
                    self._entries[args[2]].setDays(params["day"])
                if params.has_key("time"):
                    self._entries[args[2]].setTime(params["time"])
        else:
            # updates to schedule itself.
            if params.has_key("enabled"):
                self.setEnabled(params["enabled"])

    def getEntries(self, nowDay, nowTime ):
        # return iterator that returns any scheduled events that match the
        if self._enabled:
            for k in self._entries:
                if self._entries[k].doNow(nowDay, nowTime):
                    yield self._entries[k]
        return

class ScheduleProcessor( BaseHandler ):
    """
    
    """
    def __init__ (self, localRouter):
        super(ScheduleProcessor,self).__init__(localRouter)
        global _log
        _log = self._log
        self.schedule = dict()
        self._subscribeTime = 30

    def start(self):
        _log.debug( 'start' )
        self.__running = True
        self._localRouter.subscribe( self._subscribeTime, self, "http://id.webbrick.co.uk/events/time/minute", "" )
        self._localRouter.subscribe( self._subscribeTime, self, "http://id.webbrick.co.uk/events/config/get", "" )

    def stop(self):
        _log.debug( 'stop' )
        self.__running = False
        self._localRouter.unsubscribe( self, "http://id.webbrick.co.uk/events/time/minute", "" )
        self._localRouter.unsubscribe( self, "http://id.webbrick.co.uk/events/config/get", "" )

    def handleMinute( self, inEvent ):
        """ Look through the schedule and process it """
        od = inEvent.getPayload()
        nowDay = od["day"]
        nowTime = od["timestr"]
        _log.debug( 'handleMinute %s %s', nowTime, nowDay )

        for schKey in self.schedule:
            _log.debug( 'schKey %s', schKey )
            for schEntry in self.schedule[schKey].getEntries(nowDay, nowTime):
                _log.debug( 'schEntry %s', schEntry )

                for devKey,devAction in schEntry.getDevices():

                    if devAction.has_key("onoff"):
                        self.sendEvent( makeEvent( "http://id.webbrick.co.uk/events/schedule/control", 
                                "%s/%s" % (devKey,devAction["onoff"]) ) )
                    if devAction.has_key("val"):
                        self.sendEvent( makeEvent( "http://id.webbrick.co.uk/events/schedule/control", 
                                "%s/set" % (devKey,) , 
                                {'val': devAction["val"] } ) )


    def handleConfiguration( self, inEvent ):
        """ disect the configuration event """

        args = inEvent.getSource().split( "/")
        _log.debug( 'handleConfiguration %s' % ( args ) )
        if len(args) >= 3 and args[0] == "schedule" and args[2].isdigit():
            od = inEvent.getPayload()
            _log.debug( 'handleConfiguration %s - %s' % ( inEvent.getSource(), od ) )
            # its one of ours.
            # args[1] is schedule name
            # args[2] is timepoint index
            # args[3] is device key, if relevant.
            # if args[3] missing then payload is day, time and possibly enabled (if missing assume enabled)
            # if args[3] present then either onoff or val given
            # when schedule time occurs issue
            # command events
            if not self.schedule.has_key(args[1]):
                self.schedule[args[1]] = aSchedule()
            self.schedule[args[1]].update(args,od)
        # else this is not for us.
        # This allows schedule/zonename/Xxx to be used to hold associated config data for a schedule.

    def doHandleEvent( self, handler, inEvent ):
        """ Update our cache of values """
        if inEvent.getType() == "http://id.webbrick.co.uk/events/time/minute" :
            self.handleMinute( inEvent )

        elif inEvent.getType() == "http://id.webbrick.co.uk/events/config/get":
            self.handleConfiguration( inEvent )

        return makeDeferred(StatusVal.OK)

