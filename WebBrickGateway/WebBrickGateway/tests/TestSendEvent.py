# $Id: TestSendEvent.py 2609 2008-08-11 20:03:27Z graham.klyne $
#
# Unit testing for WebBrick panel definition HTML conversions.
#

import sys
import time
import unittest

from MiscLib.DomHelpers import *

from turbogears import testutil
from turbogears import controllers
import cherrypy

from EventLib.Event import Event, makeEvent
from EventLib.EventSource import EventSource
from EventHandlers.EventRouterLoad import EventRouterLoader

from EventHandlers.tests.TestEventLogger import TestEventLogger
import EventHandlers.tests.Events

from WebBrickGateway.SendEvent import *

testConfigSendEvent ="""<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="http://id.webbrick.co.uk/events/uri">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/test/type">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

class TestRoot(controllers.RootController):
    def __init__( self, router ):
        self.sendevent = SendEventLocal(router)

class TestSendEvent(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestSendEvent" )
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

        ClientProfiles.load( "./Output/browser_profiles.xml" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSendEvent) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        cherrypy.root = TestRoot(self.router)

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        time.sleep(1)

    # send a simpel event
    def testSimpleEvent(self):
        self._log.debug( "\ntestSimpleEvent" )

        testutil.create_request("/sendevent/test/event")

        # We should see lots of events here as initial pass.
        self.assertEqual( len(EventHandlers.tests.TestEventLogger._events), 1 )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/uri" )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getSource(), "test/event" )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getPayload(), None )

    # send an event with a different event type
    def testAlternateEventType(self):
        self._log.debug( "\ntestAlternateEventType" )

        testutil.create_request("/sendevent/test/event?type=http://id.webbrick.co.uk/test/type")

        self.assertEqual( len(EventHandlers.tests.TestEventLogger._events), 1 )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/test/type" )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getSource(), "test/event" )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getPayload(), None )

    # send an event with a different event type
    def testParameters(self):
        self._log.debug( "\ntestParameters" )

        testutil.create_request("/sendevent/test/event?p1=1&p2=2")

        self.assertEqual( len(EventHandlers.tests.TestEventLogger._events), 1 )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/uri" )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getSource(), "test/event" )
        self.assertEqual( len(EventHandlers.tests.TestEventLogger._events[0].getPayload()), 2 )

    # send an event with a different event type
    def testAlternateEventTypeAndParameters(self):
        self._log.debug( "\ntestAlternateEventTypeAndParameters" )

        testutil.create_request("/sendevent/test/event?type=http://id.webbrick.co.uk/test/type&p1=1&p2=2")

        self.assertEqual( len(EventHandlers.tests.TestEventLogger._events), 1 )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/test/type" )
        self.assertEqual( EventHandlers.tests.TestEventLogger._events[0].getSource(), "test/event" )
        self.assertEqual( len(EventHandlers.tests.TestEventLogger._events[0].getPayload()), 2 )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestSendEvent("testSimpleEvent"))
    suite.addTest(TestSendEvent("testAlternateEventType"))
    suite.addTest(TestSendEvent("testParameters"))
    suite.addTest(TestSendEvent("testAlternateEventTypeAndParameters"))
    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestSendEvent( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
