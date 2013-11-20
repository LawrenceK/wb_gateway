# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestDelayedEvent.py 2612 2008-08-11 20:08:49Z graham.klyne $
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

testConfigDelayedEvent1 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- Avoid time events -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="delta/delay">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.DelayedEvent' name='DelayedEvent'>
        <!-- requests a delay -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
                <event>
                    <delay delayMinutes="1">
                        <!-- After the timer a new event is sent -->
                        <newEvent type="delta/delay" source="delta/delay" />
                    </delay>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

testConfigDelayedEvent2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- Avoid time events -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="delta/delay">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.DelayedEvent' name='DelayedEvent'>
        <!-- requests a delay -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
                <event>
                    <delay delaySeconds="15">
                        <!-- After the timer a new event is sent -->
                        <newEvent type="delta/delay" source="delta/delay1" />
                        <newEvent type="delta/delay" source="delta/delay2" />
                    </delay>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigDelayedEvent3 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- Avoid time events -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="delta/delay">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.DelayedEvent' name='DelayedEvent'>
        <!-- requests a delay -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
                <event>
                    <delay delaySeconds="10">
                        <!-- After the timer a new event is sent -->
                        <newEvent type="delta/delay" source="delta/delay1" />
                    </delay>
                </event>
                <event>
                    <delay delaySeconds="20">
                        <!-- After the timer a new event is sent -->
                        <newEvent type="delta/delay" source="delta/delay2" />
                    </delay>
                </event>
                <event>
                    <delay delaySeconds="30">
                        <!-- After the timer a new event is sent -->
                        <newEvent type="delta/delay" source="delta/delay3" />
                    </delay>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

# receives data based on tests performed.

class TestDelayedEvent(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestDelayedEvent" )
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        time.sleep(1)

    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)

    # Actual tests follow
    def testDeltaTime1(self):
        """
        Test the delta time event generator.
        """
        self._log.debug( "\n\ntestDeltaTime" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigDeltaTime1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtTD0 )    # TD0 0 Off

        # time events are not in the log.
        TestEventLogger.logEvents()
        self.assertEqual( len(TestEventLogger._events), 2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/time/delta" )

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtMinute )    # minute
        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtMinute )    # minute

        # delayed event should now be here.
        self.assertEqual( len(TestEventLogger._events), 3)
        self.assertEqual( TestEventLogger._events[2].getType(), "delta/delay" )

    # Actual tests follow
    def testDeltaTime2(self):
        """
        Test the delta time event generator.
        """
        self._log.debug( "\n\ntestDeltaTime2" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigDeltaTime2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtTD0 )    # TD0 0 Off

        # time events are not in the log.
        TestEventLogger.logEvents()
        self.assertEqual( len(TestEventLogger._events), 2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/time/delta" )

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtMinute )    # minute
        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtMinute )    # minute
        # delayed event should now be here.
        self.assertEqual( len(TestEventLogger._events), 4)
        self.assertEqual( TestEventLogger._events[2].getType(), "delta/delay" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "delta/delay1" )
        self.assertEqual( TestEventLogger._events[3].getType(), "delta/delay" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "delta/delay2" )

    # Actual tests follow
    def testDelayedEvent1(self):
        """
        Test the delta time event generator.
        """
        self._log.debug( "\n\ntestDeltaTime" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigDelayedEvent1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtTD0 )    # TD0 0 Off

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )

        for i in range(0,61):
            self.router.publish( EventAgent("TestDelayedEvent"), Events.evtSecond5 )    # 61 seconds.

        # delayed event should now be here.
        self.expectNevents(2)
        self.assertEqual( TestEventLogger._events[1].getType(), "delta/delay" )

    # Actual tests follow
    def testDelayedEvent2(self):
        """
        Test the delta time event generator.
        """
        self._log.debug( "\n\ntestDeltaTime2" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigDelayedEvent2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtTD0 )    # TD0 0 Off

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )

        for i in range(0,20):
            self.router.publish( EventAgent("TestDelayedEvent"), Events.evtSecond5 )    # 20 seconds.

        # delayed event should now be here.
        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[1].getType(), "delta/delay" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "delta/delay1" )
        self.assertEqual( TestEventLogger._events[2].getType(), "delta/delay" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "delta/delay2" )

    # Actual tests follow
    def testDelayedEvent3(self):
        """
        Test the delta time event generator.
        """
        self._log.debug( "\n\ntestDeltaTime2" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigDelayedEvent3) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtTD0 )    # TD0 0 Off

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )

        for i in range(0,15):
            showWorking()
            self.router.publish( EventAgent("TestDelayedEvent"), Events.evtSecond5 )    # 20 seconds.

        self.expectNevents(2)
        self.assertEqual( TestEventLogger._events[1].getType(), "delta/delay" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "delta/delay1" )

        for i in range(0,10):
            showWorking()
            self.router.publish( EventAgent("TestDelayedEvent"), Events.evtSecond5 )    # 20 seconds.

        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[2].getType(), "delta/delay" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "delta/delay2" )

        for i in range(0,10):
            showWorking()
            self.router.publish( EventAgent("TestDelayedEvent"), Events.evtSecond5 )    # 20 seconds.

        self.expectNevents(4)
        self.assertEqual( TestEventLogger._events[3].getType(), "delta/delay" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "delta/delay3" )

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
            [ "testDelayedEvent1"
            , "testDelayedEvent2"
            , "testDelayedEvent3"
            ],
        "zzcomponent":
            [ "testComponents"
            ],
        "zzintegration":
            [ "testIntegration"
            ],
        "zzpending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestDelayedEvent, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestDelayedEvent.log", getTestSuite, sys.argv)

