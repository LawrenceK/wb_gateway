# 
#  Tests for timer
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

# Configuration for the tests
#
# this test uses the an event test a timer
#
testConfigTimer = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface  module='EventHandlers.Timer' name='Timer' >
        <presence type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/0' key="state" invert="true"/>
        <duration type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/duration' />   
        <enable type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/enable' />  
        <hold type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/1' key="state" invert="true" />  
        
        <eventtype type="http://id.webbrick.co.uk/events/timer" >
            <eventsource source="testing/timer/1">
                <event>
                    <params>
                        <testEq name="dayphase" value='Morning:Dark' />
                        <testEq name="occupancy" value='1' />
                        <testEq name="hold" value="0" />
                    </params>
                    <newEvent type='testing' source='result/timertest' >
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
   </eventInterface>
</eventInterfaces>
"""


testConfigTimer2 = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface  module='EventHandlers.Timer' name='Timer' >
        <presence type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/0' key="state" />
        <duration type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/duration' />   
        <enable type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/enable' />  
        <hold type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/1' key="state" invert="1" />  
        
        <eventtype type="http://id.webbrick.co.uk/events/timer" >
            <eventsource source="testing/timer/1">
                <event>
                    <params>
                        <testEq name="dayphase" value='Morning:Dark' />
                        <testEq name="occupancy" value='1' />
                        <testEq name="hold" value="0" />
                    </params>
                    <newEvent type='testing' source='result/timertest' >
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
   </eventInterface>
</eventInterfaces>
"""


testConfigTimer3 = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface  module='EventHandlers.Timer' name='Timer' >
        <presence type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/0' key="state" invert="true"/>
        <light_state type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/2' invert='true'/>   
        <duration type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/duration' />   
        <enable type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/enable' />  
        <hold type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/1' key="state" invert="true" />  
        
        <eventtype type="http://id.webbrick.co.uk/events/timer" >
            <eventsource source="testing/timer/1">
                <event>
                    <params>
                        <testEq name="dayphase" value='Morning:Dark' />
                        <testEq name="occupancy" value='1' />
                        <testEq name="hold" value="0" />
                    </params>
                    <newEvent type='testing' source='result/timertest' >
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
   </eventInterface>
</eventInterfaces>
"""

testConfigTimer4 = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface  module='EventHandlers.Timer' name='Timer' >
        <presence type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/0' key="state" invert="true"/>
        <light_state type='http://id.webbrick.co.uk/events/webbrick/AI' source='webbrick/100/AI/0' threshold='80' invert="true"/>   
        <duration type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/duration' />   
        <enable type='http://id.webbrick.co.uk/events/config/get' source='test/timer/1/enable' />  
        <hold type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/100/DO/1' key="state" invert="true" />  
        
        <eventtype type="http://id.webbrick.co.uk/events/timer" >
            <eventsource source="testing/timer/1">
                <event>
                    <params>
                        <testEq name="dayphase" value='Morning:Dark' />
                        <testEq name="occupancy" value='1' />
                        <testEq name="hold" value="0" />
                        <testEq name="light_state" value="0" />                        
                    </params>
                    <newEvent type='testing' source='result/timertest' >
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
   </eventInterface>
</eventInterfaces>
"""




class TestTimerAction(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestTimerAction" )
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None
        time.sleep(2)

    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)


    # Actual tests follow
    def testTimerEvent(self):
        self._log.debug( "\n\ntestTimerEvent" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTimer) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConEnable )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDuration )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtHome )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtMorningDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_on )   # this should kick presence but not create an event
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_off )  # this should kick presence because invert is true
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_off )  # this should kick presence because invert is true (twice because this happens)
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond0 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond1 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond2 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond3 )  # Create a 'second'
        time.sleep(1)
        self.expectNevents( 14 )
        
        self.assertEqual( TestEventLogger._events[12].getType(), u'http://id.webbrick.co.uk/events/timer' )
        self.assertEqual( TestEventLogger._events[12].getSource(), "testing/timer/1" )
        self.assertEqual( TestEventLogger._events[13].getType(), u'testing' )
        self.assertEqual( TestEventLogger._events[13].getSource(), "result/timertest" ) 


    def testTimerDisable(self):
        self._log.debug( "\n\ntestTimerDisable" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTimer) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDisable )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDuration )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtHome )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtMorningDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_off )  # this should kick presence
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond0 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond1 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond2 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond3 )  # Create a 'second'
        self.expectNevents( 10 )
            
    def testTimerHold(self):
        self._log.debug( "\n\ntestTimerHold" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTimer) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConEnable )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDuration )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtHome )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtMorningDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_1_off ) # this should create a hold state  (because invert is set)
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_off )  # this should kick presence
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond0 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond1 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond2 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond3 )  # Create a 'second'
        self.expectNevents( 11 )


    def testTimerHoldPI(self):
        self._log.debug( "\n\ntestTimerHoldPI" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTimer2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConEnable )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDuration )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtHome )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtMorningDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_1_on ) # this should NOT create a hold state  (because invert is set)
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_on )  # this should kick presence
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond0 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond1 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond2 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond3 )  # Create a 'second'
        self.expectNevents( 13 )


        self.assertEqual( TestEventLogger._events[11].getType(), u'http://id.webbrick.co.uk/events/timer' )
        self.assertEqual( TestEventLogger._events[11].getSource(), "testing/timer/1" )
        self.assertEqual( TestEventLogger._events[12].getType(), u'testing' )
        self.assertEqual( TestEventLogger._events[12].getSource(), "result/timertest" ) 



    def testTimerEventWithState(self):
        self._log.debug( "\n\ntestTimerEventWithState" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTimer3) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConEnable )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDuration )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtHome )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtMorningDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_2_off )  # this should kick light on, but without presence
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond0 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond1 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond2 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond3 )  # Create a 'second'
        self.expectNevents( 12 )
            
        self.assertEqual( TestEventLogger._events[10].getType(), u'http://id.webbrick.co.uk/events/timer' )
        self.assertEqual( TestEventLogger._events[10].getSource(), "testing/timer/1" )
        self.assertEqual( TestEventLogger._events[11].getType(), u'testing' )
        self.assertEqual( TestEventLogger._events[11].getSource(), "result/timertest" ) 


    def testTimerEventWithStateAndPresence(self):
        self._log.debug( "\n\ntestTimerEventWithStateAndPresence" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTimer3) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConEnable )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDuration )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtHome )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtMorningDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_2_off )  # this should kick light on, 
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_off )  # this should kick  presence
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_off )  # this should kick  presence  (twice because this happens!)
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond0 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond1 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond2 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond3 )  # Create a 'second'
        self.expectNevents( 14 )
            
        self.assertEqual( TestEventLogger._events[12].getType(), u'http://id.webbrick.co.uk/events/timer' )
        self.assertEqual( TestEventLogger._events[12].getSource(), "testing/timer/1" )
        self.assertEqual( TestEventLogger._events[13].getType(), u'testing' )
        self.assertEqual( TestEventLogger._events[13].getSource(), "result/timertest" ) 


    def testTimerEventWithAnalogue(self):
        self._log.debug( "\n\ntestTimerEventWithAnalogue" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTimer4) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConEnable )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtTimerConDuration )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtHome )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtMorningDark )
        self.router.publish( EventAgent("TestTimerAction"), Events.evtAI_0_10 )  # this should show light off, 
        self.router.publish( EventAgent("TestTimerAction"), Events.evtAI_0_90 )  # this should kick light on, 
        self.router.publish( EventAgent("TestTimerAction"), Events.evtAI_0_90 )  # this should kick light on, twice because it can happen 
        self.router.publish( EventAgent("TestTimerAction"), Events.evtDO_0_off )  # this should kick  presence
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond0 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond1 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond2 )  # Create a 'second'
        self.router.publish( EventAgent("TestTimerAction"), Events.evtSecond3 )  # Create a 'second'
        self.expectNevents( 15 )
            
        self.assertEqual( TestEventLogger._events[13].getType(), u'http://id.webbrick.co.uk/events/timer' )
        self.assertEqual( TestEventLogger._events[13].getSource(), "testing/timer/1" )
        self.assertEqual( TestEventLogger._events[14].getType(), u'testing' )
        self.assertEqual( TestEventLogger._events[14].getSource(), "result/timertest" ) 


# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestTimerAction("testTimerEvent"))

    return suite

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
            [ "testTimerEvent" ,
            "testTimerDisable" ,
            "testTimerHold" , 
            "testTimerHoldPI" ,
            "testTimerEventWithState" ,
            "testTimerEventWithStateAndPresence" ,
            "testTimerEventWithAnalogue"
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
    return TestUtils.getTestSuite(TestTimerAction, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestTimerAction.log", getTestSuite, sys.argv)

