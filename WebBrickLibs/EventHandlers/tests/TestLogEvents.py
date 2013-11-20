# $Id: TestLogEvents.py 2612 2008-08-11 20:08:49Z graham.klyne $
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

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

# Configuration for the tests

testConfigEventLogger = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.LogEvents' name='LogEvents'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DI">
            <eventsource source="" >
	        <event>
                    <exclude/>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

class TestLogEvents(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestLogEvents" )
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
    def testEventLogger(self):
        """
        Test the even logger
        """
        self._log.debug( "\ntestEventLogger" )
        logHandler = testLogHandler()
        # need to ensure log level is at INFO for the eventlog stream otherwise test fails.
        addTestLogHandler(logHandler,"EventLog")

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEventLogger) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestLogEvent"), Events.evtTD0 )
        self.router.publish( EventAgent("TestLogEvent"), Events.evtDI_1_off )
        time.sleep(1.0)

        self.assertEqual( logHandler.count(),1 )

        removeTestLogHandler(logHandler,"EventLog")

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
            [ "testEventLogger"
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
    return TestUtils.getTestSuite(TestLogEvents, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestLogEvents.log", getTestSuite, sys.argv)
