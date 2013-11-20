# $Id: TestReadEventLogs.py 2610 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader
from EventHandlers.ReadEventLogs import *

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

# Configuration for the tests

testConfig = """<?xml version="1.0" encoding="utf-8"?>
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
</eventInterfaces>
"""

class TestReadEventLogs(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestReadEventLogs" )
        elog = logging.getLogger( "EventLog" )
        elog.setLevel(logging.INFO)
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

    # Actual tests follow
    def testEventFromString(self):
        """
        Test the event logger
        """

        self._log.debug( "\ntestEventFromString" )
        
        evtStr = "2008-10-26 18:18:24,184 http://id.webbrick.co.uk/events/webbrick/CT,webbrick/9/CT/3,{'srcChannel': 3, 'curhi': 100.0, 'val': 19.600000000000001, 'fromNode': 9, 'curlo': -50.0, 'defhi': 100.0, 'deflo': -50.0}"

        evt = EventFromString(evtStr)
        self._log.debug( "type %s source %s payload %s", evt.getType(), evt.getSource(), evt.getPayload() )
        self.assertEqual( evt.getType(),"http://id.webbrick.co.uk/events/webbrick/CT" )
        self.assertEqual( evt.getSource(),"webbrick/9/CT/3" )
        self.assertNotEqual( evt.getPayload(),None )
        od = evt.getPayload()
        self.assertEqual( od["srcChannel"], '3')
        self.assertEqual( od["val"], '19.600000000000001')

    def testReadLogFile(self):
        cnt = 0
        rdr = ReadLogFile("resources/EventLog.log")
        ln = rdr.next()
        while ln:
            evt = EventFromString(ln)
            cnt = cnt + 1
            ln = rdr.next()
        self.assertEqual( cnt, 9 )
    
    def testReadLogFile2(self):

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfig) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        ReadLogFileSendEvents( "resources/EventLog.log", self.router )

        TestEventLogger.expectNevents(9)
        self.assertEqual( TestEventLogger._events[0].getSource(), "temperature/outside" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "webbrick/3/1" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "webbrick/3/1" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "webbrick/6" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "webbrick/2" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "webbrick/7" )
        self.assertEqual( TestEventLogger._events[6].getSource(), "webbrick/4" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "webbrick/9/CT/3" )
        self.assertEqual( TestEventLogger._events[8].getSource(), "webbrick/9/AI/0" )

    def testLineReader(self):
        cnt = 0
        bytes = file("resources/EventLog.log").read()
        rdr = LineReader(bytes)
        ln = rdr.next()
        while ln:
            evt = EventFromString(ln)
            cnt = cnt + 1
            ln = rdr.next()
        self.assertEqual( cnt, 9 )

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
            [ "testEventFromString"
            , "testReadLogFile"
            , "testReadLogFile2"
            , "testLineReader"
            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            , "testReadLogFiles"
            , "ReadZipFileSendEvents"
            , "ReadZipFilesSendEvents"
            ]
        }
    return TestUtils.getTestSuite(TestReadEventLogs, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestReadEventLogs.log", getTestSuite, sys.argv)
