# $Id: TestScheduleProcessor.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
#

import sys, logging, time, os
from os.path import exists
import time
import unittest

from MiscLib.DomHelpers import *

from EventLib.Event import Event
from EventLib.EventAgent import EventAgent
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger
from EventHandlers.tests.Events import *

testConfig1 ="""<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='./resources/ScheduleProcessor'>
    </eventInterface>

    <eventInterface module='EventHandlers.ScheduleProcessor' name='ScheduleProcessor'>
    </eventInterface>

</eventInterfaces>
"""

TestPersistFile = "./resources/ScheduleProcessor.xml"

verifySched = {
    u'0': {'time': '05:30:00', 'days': '-MTWtF-' },
    u'1': {'time': '08:00:00', 'days': '-MTWtF-' },
    u'2': {'time': '16:00:00', 'days': '-MTWtF-' },
    u'3': {'time': '22:00:00', 'days': '-MTWtF-' },
    }

verifyDevices = {
    u'boiler':'Boiler',
    u'zone1':'Zone 1',
    }

verifyActions = {
    u'0': {
                    'boiler': 'On', 
                    'zone1': '21.0',
                 },
    u'1': {
                    'zone1': '18.0',
                 },
    u'2': {
                    'boiler': 'Off', 
                 },
    u'3': {
                    'boiler': 'On', 
                    'zone1': '21.0',
                 },
    }

class TestScheduleProcessor(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestScheduleProcessor" )
        self._log.debug( "\n\nsetUp" )

        self.loader = None
        self.router = None
        self.setCwd = False
        if exists("EventHandlers/tests/resources"):
            self.setCwd = True
            os.chdir("EventHandlers/tests")

    def tearDown(self):
        self._log.debug( "\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None
        if self.setCwd:
            os.chdir("../..")

        time.sleep(1)

    # Actual tests follow
    def testLoad(self):
        self._log.debug( "\ntestLoad" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfig1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1.0)

        # We should see lots of events here as initial pass.
        TestEventLogger.logEvents()
        oldLen = len(TestEventLogger._events)
        self.assertEqual( oldLen, 11 )  # twice sent.

    def testRun(self):
        self._log.debug( "\ntestRun" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfig1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(0.1)

        # We should see lots of events here as initial pass.
        TestEventLogger.logEvents()
        oldLen = len(TestEventLogger._events)
        self.assertEqual( oldLen, 11 )  # twice sent.
        TestEventLogger.clearEvents()
        
        # send midnight
        # no new events, just me
        self.router.publish( EventAgent("TestScheduleProcessor"), evtMidnightMon )
        time.sleep(0.1)
        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()
        self.assertEqual( oldLen, 1 )
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )

        # first event time
        self.router.publish( EventAgent("TestScheduleProcessor"), evt0530 )
        time.sleep(0.2)
        # time and two actions
        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()
        self.assertEqual( oldLen, 4 )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "zone1/set" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "boiler/On" )

        # second event time
        self.router.publish( EventAgent("TestScheduleProcessor"), evt0800 )
        time.sleep(0.1)
        # time and one actions
        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()
        self.assertEqual( oldLen, 6 )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "zone1/set" )

        # third event time
        self.router.publish( EventAgent("TestScheduleProcessor"), evt1600 )
        time.sleep(0.1)
        # time and one actions
        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()
        self.assertEqual( oldLen, 8 )
        self.assertEqual( TestEventLogger._events[6].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "boiler/Off" )

        # fourth event time
        self.router.publish( EventAgent("TestScheduleProcessor"), evt2200 )
        time.sleep(0.1)
        # time and two actions
        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()
        self.assertEqual( oldLen, 11 )
        self.assertEqual( TestEventLogger._events[8].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[9].getSource(), "zone1/set" )
        self.assertEqual( TestEventLogger._events[10].getSource(), "boiler/On" )


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
            , "testRun"
            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestScheduleProcessor, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestScheduleProcessor.log", getTestSuite, sys.argv)
