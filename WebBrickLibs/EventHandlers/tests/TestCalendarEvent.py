# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestCalendarEvent.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

# Configuration for the tests
#
# this test uses the two webbrick UDP triggers to trigger jobs.
# one job directly actions something
# The other job generates an event.
#
# The TestCalendar.ics file has a holiday from the 1st of July to the 2nd of July
#

testCalendarConfig = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.CalendarEvent' name='CalendarEvent' icalfile='resources/TestCalendar.ics'>
    </eventInterface>

</eventInterfaces>
"""

evtMinuteAtHome = makeEvent( 'http://id.webbrick.co.uk/events/time/minute', 'time/minute', {'datetimestr': '2008-06-24T12:58:00', 'hour': 12, 'timestr': '12:58:00', 'month': 6, 'second': 0, 'datestr': '2008-06-24', 'year': 2008, 'date': 24, 'day': 2, 'minute': 58}  )


class TestCalendarEvent(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestCalendarEvent" )
        self._log.debug( "\n\nsetUp" )
        self.runner = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.runner:
            self.runner.stop()  # all tasks
            self.runner = None

    # Actual tests follow
    def testLoad(self):
        self._log.debug( "\ntestLoad" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testCalendarConfig) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

    def testStartupAtHome(self):
        self._log.debug( "\ntestStartupAtHome" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testCalendarConfig) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestCalendarEvent"), evtMinuteAtHome )

        self.assert_( TestEventLogger.expectNevents(2), "Expected 2 events only seen %s" % (len(TestEventLogger._events)) )
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "occupants/home" )
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"], 1 )
        
        
       
    
    def testDummy(self):
        return

from MiscLib import TestUtils
def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testLoad"
            , "testStartupAtHome"
            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            , "testStartupOnVacation"
            , "testGoOnHoliday"
            , "testComeHome"
            ]
        }
    return TestUtils.getTestSuite(TestCalendarEvent, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestCalendarEvent.log", getTestSuite, sys.argv)
