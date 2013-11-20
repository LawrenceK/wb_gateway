# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestWebbrickStatusQuery.py 2612 2008-08-11 20:08:49Z graham.klyne $
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
# depends what is connected to webbrick under test
NUM_TEMP_SENSORS = 3

testConfigWebbrickStatusQuery = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/CT">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AO">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AI">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DI">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.WebbrickStatusQuery' name='WebbrickStatusQuery'>
        <eventtype type="http://id.webbrick.co.uk/events/time/second">
            <eventsource source="time/second" >
                <!-- all events from a single source -->
                <event>
                    <params>
                        <!-- every 5 seconds -->
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
                    <webbrick address="10.100.100.100" />
                    <webbrickz address="localhost:8019" />
                    <scan/>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="time/minute" >
                <event>
                    <discoverz address="255.255.255.255"/>
                    <recover/>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/NN">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AA">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

# <!-- This test expects a real webbrick on the network -->
testConfigWebbrickStatusQueryReal = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/CT">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AO">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AI">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DI">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.WebbrickUdpEventReceiver' name='WebbrickUdpEventReceiver'>
    </eventInterface>

    <eventInterface module='EventHandlers.WebbrickStatusQuery' name='WebbrickStatusQuery'>
        <eventtype type="http://id.webbrick.co.uk/events/time/second">
            <eventsource source="time/second" >
                <!-- all events from a single source -->
                <event>
                    <params>
                        <!-- every 5 seconds -->
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
                    <NOwebbrick address="localhost:8019" />
                    <scan/>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="time/minute" >
                <event>
                    <discover address="255.255.255.255"/>
                    <recover/>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/NN">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AA">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

def waitNSeconds(n):
    # with twisted around time.sleep may and can exit early.
    stop = time.time() + n
    while stop > time.time():
        time.sleep(1)

class TestWebbrickStatusQuery(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestWebbrickStatusQuery" )
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        waitNSeconds(2)
            
    def testWebbrickStatusQuery(self):
        self._log.debug( "\n\ntestWebbrickStatusQuery" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigWebbrickStatusQuery) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtSecond5 )   # so webbrick is in list for recover
        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtMinute1 )    # do recover
        waitNSeconds(2)   # recover is async
        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtSecond5 )   # do scan
        waitNSeconds(2)   # scan is async

        # We should see lots of events here as initial pass.

        # my test rig only has 1 temp sensors.
        # so:
        # 1 temp sensors
        # 4 analogue in
        # 4 analogue out
        # 12 digital in
        # 8 digital out
        # 8 mimic out
        self.assert_( TestEventLogger.expectAtLeastNevents(36+NUM_TEMP_SENSORS), "expecting %u events" % (36+NUM_TEMP_SENSORS)  )
        oldLen = len(TestEventLogger._events)

        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtSecond5 )   # do scan
        waitNSeconds(2)   # scan is async

        TestEventLogger.logEvents()
        self.assert_( oldLen <= len(TestEventLogger._events) )
        
    def testWebbrickStatusQueryReal(self):
        self._log.debug( "\n\ntestWebbrickStatusQueryReal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigWebbrickStatusQueryReal) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtSecond5 )   # so webbrick is in list for recover
        waitNSeconds(2)   # scan is async
        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtMinute1 )    # do discover
        waitNSeconds(30)
        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtMinute1 )    # do recover
        waitNSeconds(2)   # recover is async
        self.router.publish( EventAgent("TestWebbrickStatusMonitor"), Events.evtSecond5 )   # do scan
        waitNSeconds(2)   # scan is async

        # We should see lots of events here as initial pass.
        self.assert_( TestEventLogger.expectAtLeastNevents(10), "expecting %u events" % (10)  )

        # wait for 5 seconds to pass.
        #time.sleep(5)
        #self.assertEqual( oldLen, len(TestEventLogger._events) )

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
            [ "testDummy"
            ],
        "component":
            [ "testWebbrickStatusQuery"
            , "testWebbrickStatusQueryReal"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestWebbrickStatusQuery, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestWebbrickStatusQuery.log", getTestSuite, sys.argv)
