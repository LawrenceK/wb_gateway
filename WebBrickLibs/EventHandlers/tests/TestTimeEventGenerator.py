# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestTimeEventGenerator.py 2672 2008-09-01 18:56:24Z lawrence.klyne $
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
from EventHandlers.TimeEventGenerator import TimeEventGenerator

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events

# Configuration for the tests
testConfigTime1 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="http://id.webbrick.co.uk/events/time/isDark">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.TimeEventGenerator' name='TimeEventGenerator' latitude='51.5086' longitude='-0.1264' interval='minutes' runtime='0' startup_delay='1'>
    </eventInterface>

</eventInterfaces>
"""

testConfigTime2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="local/url">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.TimeEventGenerator' name='TimeEventGenerator' latitude='51.5086' longitude='-0.1264' interval='seconds' startup_delay='5'>
    </eventInterface>

    <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <eventsource source="time/minute" >
                <!-- all events from a single source -->
	        <event>
                    <newEvent type="local/url" source="local/BoilerOn" />
                    Test
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/time/second">
            <eventsource source="time/second" >
                <!-- all events from a single source -->
	        <event>
                    <params>
                        <testEq name='second'>
                            <value>5</value>
                            <value>20</value>
                            <value>35</value>
                            <value>50</value>
                        </testEq>
                    </params>
                    <newEvent type="local/url" source="local/HwOn">
                    </newEvent>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigTime3 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <!-- all events from a single source -->
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
    <eventInterface module='EventHandlers.tests.TestTimeEventGenerator' name='TestDelay'>
        <eventtype type="http://id.webbrick.co.uk/events/time/second">
            <eventsource source="time/second" >
                <!-- all events from a single source -->
	        <event>
                    <params>
                        <testEq name='second'>
                            <value>0</value>
                            <value>5</value>
                            <value>10</value>
                            <value>15</value>
                            <value>20</value>
                            <value>25</value>
                            <value>30</value>
                            <value>35</value>
                            <value>40</value>
                            <value>45</value>
                            <value>50</value>
                            <value>55</value>
                        </testEq>
                    </params>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
    <eventInterface module='EventHandlers.TimeEventGenerator' name='TimeEventGenerator' latitude='51.5086' longitude='-0.1264' interval='seconds' startup_delay='5'>
    </eventInterface>
</eventInterfaces>
"""

testConfigTime4 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="http://id.webbrick.co.uk/events/time/isDark">
            <eventsource source="" >
                <!-- all events from a single source -->
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/time/second">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
    <eventInterface module='EventHandlers.TimeEventGenerator' name='TimeEventGenerator' latitude='51.5086' longitude='-0.1264' interval='seconds' startup_delay='5'>
    </eventInterface>
</eventInterfaces>
"""

# Minimal event interface
# this one delays so as to make sure the event time generator issues all events
class TestDelay(BaseHandler):
    def __init__ (self, localRouter):
        self._log = logging.getLogger( "EventHandlers.tests.TestDelay" )
        super(TestDelay,self).__init__(localRouter)

    def doActions( self, actions, inEvent ):
        """
        Save it so we can see what happens.
        """
        time.sleep( 4 )

class TestTimeEventGenerator(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestTimeEventGenerator" )
        self._log.debug( "\n\nsetUp" )
        TestEventLogger._events = []  # empty list

        self.runner = None
        self.dumpEvents = True  # set to false if we reaxch the end successfully.

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.runner:
            self.runner.stop()  # all tasks
            self.runner = None

        time.sleep(5)
        if self.dumpEvents:
            idx = 0
            for evt in TestEventLogger._events:
                self._log.info( "%u:%s" % (idx,evt) )
                idx = idx + 1

    def waitNEvents(self, cnt, maxt = 10):
        maxTime = maxt
        while (len(TestEventLogger._events) < cnt) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)
        
    def testTimeEvent1(self):
        """
        Run test with time interval in minutes.
        """
        self._log.debug( "\n\ntestTimeEvent1" )
        loader = EventRouterLoader()
        loader.loadHandlers( getDictFromXmlString(testConfigTime1) )

        loader.start()  # all tasks

        self._router = loader.getEventRouter()

        self.waitNEvents( 1 )

        # should have isDark or isLight event
        TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), 1)
        self.assertEqual( TestEventLogger._events[0].getType(), u'http://id.webbrick.co.uk/events/time/isDark' )
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        # assume testing during daylight hours
        od = TestEventLogger._events[0].getPayload()
        #self.assertEqual( od["state"], 0 )

        maxTime = 70
        while (TestEventLogger._events[-1].getType() != u'http://id.webbrick.co.uk/events/time/minute') and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        TestEventLogger.logEvents()

        # now look for correct url requests
        self.failUnless( len(TestEventLogger._events) >= 2)
        self.assertEqual( TestEventLogger._events[-1].getType(), u'http://id.webbrick.co.uk/events/time/minute' )
        self.assertEqual( TestEventLogger._events[-1].getSource(), "time/minute" )
        od = TestEventLogger._events[-1].getPayload()
        self.failUnless( od.has_key("second") ) 
        self.failUnless( od.has_key("minute") ) 
        self.failUnless( od.has_key("hour") ) 
        self.failUnless( od.has_key("day") ) 
        self.failUnless( od.has_key("date") ) 
        self.failUnless( od.has_key("month") ) 
        self.failUnless( od.has_key("year") ) 
        self.failUnless( od.has_key("week") ) 
        self.failUnless( od.has_key("dayofyear") ) 
        self.failUnless( od.has_key("timestr") ) 
        self.failUnless( od.has_key("datestr") ) 
        self.failUnless( od.has_key("datetimestr") ) 

        loader.stop()  # all tasks
        self.dumpEvents = False

    def testTimeEvent2(self):
        """
        Run test with time interval in seconds.
        """
        self._log.debug( "\ntestTimeEvent2" )
        loader = EventRouterLoader()
        loader.loadHandlers( getDictFromXmlString(testConfigTime2) )

        loader.start()  # all tasks

        self.waitNEvents( 5, 70 )

        # now look for correct url requests
        TestEventLogger.logEvents()
        self.assertEqual( len(TestEventLogger._events), 5)

        # the requests could be in either order.
        seenOne = 0
        seenTwo = 0
        for evnt in TestEventLogger._events:
            if ( evnt.getSource() == "local/BoilerOn" ):
                seenOne += 1
            elif ( evnt.getSource() == "local/HwOn" ):
                seenTwo += 1
            else:
                pass    # error
        self.assertEqual( seenOne, 1 )
        self.assertEqual( seenTwo, 4 )

        loader.stop()  # all tasks
        self.dumpEvents = False

    def testTimeEvent3(self):
        """
        Run test with time interval in seconds.
        """
        self._log.debug( "\n\ntestTimeEvent3" )
        loader = EventRouterLoader()
        loader.loadHandlers( getDictFromXmlString(testConfigTime3) )

        loader.start()  # all tasks

        self._router = loader.getEventRouter()

        self.waitNEvents( 16, 20 )

        TestEventLogger.logEvents()
        self.assert_( len(TestEventLogger._events) > 16)

        loader.stop()  # all tasks
        self.dumpEvents = False

    def testTimeEvent4(self):
        """
        Run test with time interval in seconds.
        """
        self._log.debug( "\n\ntestTimeEvent4" )
        loader = EventRouterLoader()
        loader.loadHandlers( getDictFromXmlString(testConfigTime4) )

        loader.start()  # all tasks

        self._router = loader.getEventRouter()

        self.waitNEvents( 1 )
        TestEventLogger.logEvents()

        # first event should be isDark
        self.assert_( len(TestEventLogger._events) > 0)
        self.assertEqual( TestEventLogger._events[0].getType(), u'http://id.webbrick.co.uk/events/time/isDark' )
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )

        self.waitNEvents( 5 )
        TestEventLogger.logEvents()
        self.assert_( len(TestEventLogger._events) > 4)
        evt = TestEventLogger._events[1]
        od = evt.getPayload()
        self.assertEqual( len(od["timestr"]),8 )
        self.assertEqual( len(od["datestr"]),10 )
        self.assertEqual( len(od["datetimestr"]),19 )

        loader.stop()  # all tasks
        self.dumpEvents = False

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
            [ "testTimeEvent1"
            , "testTimeEvent2"
            , "testTimeEvent3"
            , "testTimeEvent4"
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
    return TestUtils.getTestSuite(TestTimeEventGenerator, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestTimeEventGenerator.log", getTestSuite, sys.argv)
