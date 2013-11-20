# $Id: TestDataset.py 2610 2008-08-11 20:08:49Z graham.klyne $
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

testConfigDataset = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.Dataset' name='Dataset' columns="4">
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AI">
            <eventsource source="webbrick/100/AI/1" >
	        <event>
                    <data column="3" name="humidity" attr="val"/>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/CT">
            <eventsource source="webbrick/100/CT/1" >
	        <event>
                    <data column="4" name="lounge_temp" attr="val"/>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="">
            <eventsource source="time/minute" >
	        <event>
                    <data column="1" name="date" attr="datestr"/>
                    <data column="2" name="time" attr="timestr"/>
                    <action action="csv" logstream="Dataset.csv.1"/>
                    <action action="xml" logstream="Dataset.xml.1"/>
                    <action action="event" type="dataset/4" source="dataset/house"/>
                    <action action="clear" />
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

class TestDataset(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestDataset" )
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
    def testDataset(self):
        """
        Test the data set creator
        """
        self._log.debug( "\ntestDataset" )
        logHandler = testLogHandler()
        addTestLogHandler(logHandler,"Dataset")

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigDataset) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestLogEvent"), Events.evtAI_1_50 )
        self.router.publish( EventAgent("TestLogEvent"), Events.evtCT_1_25 )
        self.router.publish( EventAgent("TestLogEvent"), Events.evtMinute1 )
        time.sleep(1.0)

        self.assertEqual( logHandler.count(), 2 )
        TestEventLogger.expectNevents(4)
        TestEventLogger.logEvents()

        removeTestLogHandler(logHandler,"Dataset")

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
            [ "testDataset"
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
    return TestUtils.getTestSuite(TestDataset, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestDataset.log", getTestSuite, sys.argv)
