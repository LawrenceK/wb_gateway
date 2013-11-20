# $Id: TestCompound.py 2612 2008-08-11 20:08:49Z graham.klyne $

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
testConfigCompoundEvent = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DI">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
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
        <eventtype type="http://simple">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.Compound' name='Compound'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DI">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/DI/0" >
                <event>
                    <params>
                        <testEq name='state' value='0'/>
                    </params>
                    <action name="Sensor1" value="0"/>
    	        </event>
                <event>
                    <params>
                        <testEq name='state' value='1'/>
                    </params>
                    <action name="Sensor1" value="1"/>
                </event>
            </eventsource>
            
            <eventsource source="webbrick/100/DI/1" >
                <event>
                    <action name="Sensor2" key="state"/>
                </event>
            </eventsource>
        </eventtype>
            
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/7" >
                <!--test that transient can be keyed this way -->
                <event>
                    <action name="AnInput" value="do" transient="yes"/>
                </event>
            </eventsource>
        </eventtype>

        <initialState name="Sensor1" value=""/>
        <initialState name="Sensor2" value=""/>

        <initialState name="SleepState" value="0"/>

        <compound>
            <params>
                <testEq name='Sensor1' value='0'/>
                <testEq name='Sensor2' value='0'/>
            </params>
            <newEvent type="http://simple" source="garage1/Error">
                <copy_other_data Sensor1="Sensor1"  Sensor2="Sensor2" />
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='Sensor1' value='0'/>
                <testEq name='Sensor2' value='1'/>
            </params>
            <newEvent type="http://simple" source="garage1/Open" >
                <copy_other_data Sensor1="Sensor1"  Sensor2="Sensor2" />
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='Sensor1' value='1'/>
                <testEq name='Sensor2' value='0'/>
            </params>
            <newEvent type="http://simple" source="garage1/Closed" >
                <copy_other_data Sensor1="Sensor1"  Sensor2="Sensor2" />
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='Sensor1' value='1'/>
                <testEq name='Sensor2' value='1'/>
            </params>
            <newEvent type="http://simple" source="garage1/Ajar">
                <other_data aval="2" />
                <copy_other_data Sensor1="Sensor1"  Sensor2="Sensor2" />
            </newEvent>
        </compound>

    </eventInterface>
</eventInterfaces>
"""

testConfigCompoundEvent2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://simple">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.Compound' name='Compound'>

        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <!-- events from a source of a specific type -->
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name='minute' value='1'/>
                    </params>
                    <action name="State1" value="0"/>
                    <action name="State2" value="0"/>
                </event>
                <event>
                    <params>
                        <testEq name='minute' value='2'/>
                    </params>
                    <action name="State1" value="0"/>
                    <action name="State2" value="1"/>
                </event>
                <event>
                    <params>
                        <testEq name='minute' value='3'/>
                    </params>
                    <action name="State1" value="1"/>
                    <action name="State2" value="0"/>
                </event>
                <event>
                    <params>
                        <testEq name='minute' value='4'/>
                    </params>
                    <action name="State1" value="1"/>
                    <action name="State2" value="1"/>
                </event>
            </eventsource>
        </eventtype>

        <initialState name="State1" value="0"/>
        <initialState name="State2" value="0"/>

        <compound>
            <params>
                <testEq name='State1' value='0'/>
                <testEq name='State2' value='0'/>
            </params>
            <newEvent type="http://simple" source="garage1/Error">
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='State1' value='0'/>
                <testEq name='State2' value='1'/>
            </params>
            <newEvent type="http://simple" source="garage1/Open" >
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='State1' value='1'/>
                <testEq name='State2' value='0'/>
            </params>
            <newEvent type="http://simple" source="garage1/Closed" >
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='State1' value='1'/>
                <testEq name='State2' value='1'/>
            </params>
            <newEvent type="http://simple" source="garage1/Ajar">
            </newEvent>
        </compound>

    </eventInterface>
</eventInterfaces>
"""

testConfigCompoundEventNewState = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.Compound' name='Compound'>

        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <!-- events from a source of a specific type -->
            <eventsource source="time/minute" >
                <event>
                    <action name="idx" key="minute"/>
                </event>
            </eventsource>
        </eventtype>

        <initialState name="testState" value="0"/>

        <compound>
            <params>
                <testEq name='idx' value='1'/>
            </params>
            <newState name="testState" value="1" />
        </compound>
        <compound>
            <params>
                <testEq name='idx' value='2'/>
            </params>
            <newEvent type="internal" source="testState" >
                <copy_other_data idx="testState" />
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='idx' value='3'/>
            </params>
            <newState name="testState" key="idx" />
        </compound>
        <compound>
            <params>
                <testEq name='idx' value='4'/>
            </params>
            <newEvent type="internal" source="testState" >
                <copy_other_data idx="testState" />
            </newEvent>
        </compound>

    </eventInterface>
</eventInterfaces>
"""

class TestCompound(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestCompound" )
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None
            
    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)

    # Actual tests follow
    def testCompoundEvent(self):
        self._log.debug( "\n\ntestCompoundEvent" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigCompoundEvent) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestCompound"), Events.evtDI_0_off )    # 0 Off
        self.router.publish( EventAgent("TestCompound"), Events.evtDI_1_off )    # 1 Off

        self.expectNevents( 3 )
        self.assertEqual( TestEventLogger._events[2].getType(), u'http://simple' )
        self.assertEqual( TestEventLogger._events[2].getSource(), "garage1/Error" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["Sensor1"], "0" )
        self.assertEqual( od["Sensor2"], "0" )

        self.router.publish( EventAgent("TestCompound"), Events.evtDI_1_on )    # 1 On
        self.expectNevents( 5 )
        self.assertEqual( TestEventLogger._events[4].getType(), u'http://simple' )
        self.assertEqual( TestEventLogger._events[4].getSource(), "garage1/Open" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["Sensor1"], "0" )
        self.assertEqual( od["Sensor2"], "1" )

        self.router.publish( EventAgent("TestCompound"), Events.evtDI_0_on )    # 0 On
        self.expectNevents( 7 )
        self.assertEqual( TestEventLogger._events[6].getType(), u'http://simple' )
        self.assertEqual( TestEventLogger._events[6].getSource(), "garage1/Ajar" )
        od = TestEventLogger._events[6].getPayload()
        self.assertEqual( od["aval"], "2" )
        self.assertEqual( od["Sensor1"], "1" )
        self.assertEqual( od["Sensor2"], "1" )

        self.router.publish( EventAgent("TestCompound"), Events.evtDI_1_off )    # 1 Off
        self.expectNevents( 9 )
        self.assertEqual( TestEventLogger._events[8].getType(), u'http://simple' )
        self.assertEqual( TestEventLogger._events[8].getSource(), "garage1/Closed" )
        od = TestEventLogger._events[8].getPayload()
        self.assertEqual( od["Sensor1"], "1" )
        self.assertEqual( od["Sensor2"], "0" )

    def testCompoundEvent2(self):
        # What happens if an updated updates multiple bits of local state
        # and gets repeated events
        self._log.debug( "\n\ntestCompoundEvent2" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigCompoundEvent2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        # initial state is all things off.
        self.router.publish( EventAgent("TestCompound"), Events.evtMinute1 )

        self.expectNevents( 1 )

        self.router.publish( EventAgent("TestCompound"), Events.evtMinute2 )
        self.expectNevents( 3 )
        self.assertEqual( TestEventLogger._events[2].getType(), u'http://simple' )
        self.assertEqual( TestEventLogger._events[2].getSource(), "garage1/Open" )

        self.router.publish( EventAgent("TestCompound"), Events.evtMinute3 )
        self.expectNevents( 5 )
        self.assertEqual( TestEventLogger._events[4].getType(), u'http://simple' )
        self.assertEqual( TestEventLogger._events[4].getSource(), "garage1/Closed" )

        self.router.publish( EventAgent("TestCompound"), Events.evtMinute2 )
        self.expectNevents( 7 )
        self.assertEqual( TestEventLogger._events[6].getType(), u'http://simple' )
        self.assertEqual( TestEventLogger._events[6].getSource(), "garage1/Open" )

    def testCompoundNewState(self):
        self._log.debug( "\ntestCompoundNewState" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigCompoundEventNewState) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        # initial state is all things off.
        self.router.publish( EventAgent("TestCompound"), Events.evtMinute1 )

        TestEventLogger.logEvents()
        self.expectNevents( 1 )

        self.router.publish( EventAgent("TestCompound"), Events.evtMinute2 )
        self.expectNevents( 3 )
        self.assertEqual( TestEventLogger._events[2].getType(), u'internal' )
        self.assertEqual( TestEventLogger._events[2].getSource(), "testState" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["idx"], '1' )

        self.router.publish( EventAgent("TestCompound"), Events.evtMinute3 )
        self.expectNevents( 4 )

        self.router.publish( EventAgent("TestCompound"), Events.evtMinute4 )
        self.expectNevents( 6 )
        self.assertEqual( TestEventLogger._events[5].getType(), u'internal' )
        self.assertEqual( TestEventLogger._events[5].getSource(), "testState" )
        od = TestEventLogger._events[5].getPayload()
        self.assertEqual( od["idx"], 3 )  # previous minute

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
            [ "testCompoundEvent"
            , "testCompoundEvent2"
            , "testCompoundNewState"
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
    return TestUtils.getTestSuite(TestCompound, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestHttpAction.log", getTestSuite, sys.argv)

