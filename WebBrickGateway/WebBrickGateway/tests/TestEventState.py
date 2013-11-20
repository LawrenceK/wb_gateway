# $Id: TestEventState.py 2609 2008-08-11 20:03:27Z graham.klyne $
#
# Unit testing for WebBrick panel definition HTML conversions.
#

import sys
import time
import unittest
import logging

from MiscLib.DomHelpers import *

#from WebBrickGateway.Webbrick import *

from EventLib.Event import Event, makeEvent
from EventLib.EventSource import EventSource
from EventHandlers.EventRouterLoad import EventRouterLoader

from EventHandlers.tests.TestEventLogger import TestEventLogger
import EventHandlers.tests.Events

from WebBrickGateway.EventState import *

testConfigEvent = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

# dummy cherry py request
class DummyRequest:
    def __init__(self):
        self.params = dict()

class TestEventState(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestEventState" )
        self.router = None
        self.loader = None
        self.eventState = None
        return

    def tearDown(self):
        if self.eventState:
            self.eventState.stop( self.router )
            self.eventState = None

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        time.sleep(1)

    # Actual tests follow

    def TestEventState(self):
        # create testDespatch
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEvent) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.eventState = EventState()

        self.eventState.start( self.router );

        # request URL from .. 
        q1 = self.eventState.queryCache( 'webbrick/100/DO/0', 'state' )
        self.assertEqual( q1["stsval"], None )
        self.assertEqual( q1["stserr"], 'Not Known' )

        # send event
        self.router.publish( EventSource("TestEventState"), EventHandlers.tests.Events.evtDO_0_off )    # 0 Off
        # request good URL
        q2 = self.eventState.queryCache( 'webbrick/100/DO/0', 'state' )
        self.assertEqual( q2["stsval"], '0' )
        self.assertEqual( q2["stserr"], None )

        # request bad URL
        q3 = self.eventState.queryCache( 'webbrick/100/DO/1', 'state' )
        self.assertEqual( q3["stsval"], None )
        self.assertEqual( q3["stserr"], 'Not Known' )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestEventState("TestEventState"))
    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestEventState( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
