# $Id: TestEventMapper.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import Events
from DummyRouter import *

from EventHandlers.EventMapper import EventMapper

import EventHandlers.tests.TestEventLogger as TestEventLogger

# Configuration for the tests

#
testConfigJob = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
                <!-- all events from a single source -->
	        <event>
                    <params>
                    </params>
                    <newEvent type="local/url" source="local/BoilerOn" />
                    Test
	        </event>
            </eventsource>
            <eventsource source="webbrick/100/TD/1" >
	        <event>
                    <params>
                    </params>
                    <newEvent type="local/url" source="local/HwOn">
                    </newEvent>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
"""

#
testConfigJob3 = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventMapper' name='EventMapper'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
            <eventsource source="webbrick/100/DO/0" >
	        <event>
                    <params>
                    </params>
                    <newEvent type="local/url" source="local/HwOn">
                        <other_data val1="1"/>
                        <copy_other_data state="state"/>
                    </newEvent>
	        </event>
            </eventsource>
            <eventsource source="webbrick/100/DO/7" >
	        <event>
                    <params>
                    </params>
                    <newEvent type="local/url" source="local/NotToBeTriggerred">
                        <other_data val1="7"/>
                        <copy_other_data state="state"/>
                    </newEvent>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
"""

testDoubleHandler = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/time/minute">
                <eventsource source="time/minute" >
	            <event>
                        <params>
                        </params>
                        <newEvent type="test/1" source="test/1">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>

        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/time/minute">
                <eventsource source="time/minute" >
	            <event>
                        <params>
                        </params>
                        <newEvent type="test/2" source="test/2">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
"""

class TestEventMapper(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestEventMapper" )
        self._log.debug( "\n\nsetUp" )
        self._router = DummyRouter()

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)

    # Actual tests follow

    def testJobEvent(self):
        self._log.debug( "\n\ntestJobEvent" )
        testCfg = getDictFromXmlString(testConfigJob)
        self._log.debug( "testCfg %s" % testCfg )

        em = EventMapper(self._router)
        self.assertNotEqual( em, None)
        em.configure(testCfg['eventInterface'])
        em.start()

        em.handleEvent( Events.evtTD0 )    # 0 Off
        em.handleEvent( Events.evtTD1 )    # 1 Off

        self.assertEqual( len(self._router._pubs), 2 )
        self.assertEqual( self._router._pubs[0][1].getType(), "local/url" )
        self.assertEqual( self._router._pubs[0][1].getSource(), "local/BoilerOn" )
        self.assertEqual( self._router._pubs[1][1].getType(), "local/url" )
        self.assertEqual( self._router._pubs[1][1].getSource(), "local/HwOn" )
        em.stop()   

    def testJobEvent3(self):
        self._log.debug( "\n\ntestJobEvent3" )

        testCfg = getDictFromXmlString(testConfigJob3)
        self._log.debug( "testCfg %s" % testCfg )

        em = EventMapper(self._router)
        self.assertNotEqual( em, None)
        em.configure(testCfg['eventInterface'])
        em.start()

        em.handleEvent( Events.evtDO_0_on )    # 0 Off
        em.handleEvent( Events.evtDO_1_on )    # 1 Off

        self.assertEqual( len(self._router._pubs), 1 )
        self.assertEqual( self._router._pubs[0][1].getType(), "local/url" )
        self.assertEqual( self._router._pubs[0][1].getSource(), "local/HwOn" )
        od = self._router._pubs[0][1].getPayload()
        self.assertEqual( od["val1"], "1" )
        self.assertEqual( od["state"], "1" )

    # Actual tests follow
    def testDoubleHandler(self):
        """
        Test what happens with two copies loaded.
        """
        self._log.debug( "\ntestDoubleHandler" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testDoubleHandler) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testDoubleHandler"), Events.evtMinute1 )    # TD0 0 Off

        # time events are not in the log.
        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[1].getType(), "test/1" )
        self.assertEqual( TestEventLogger._events[2].getType(), "test/2" )

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
            [ "testJobEvent"
            , "testJobEvent3"
            , "testDoubleHandler"
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
    return TestUtils.getTestSuite(TestEventMapper, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestEventMapper.log", getTestSuite, sys.argv)
