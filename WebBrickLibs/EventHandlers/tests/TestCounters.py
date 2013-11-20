# $Id: TestCounters.py 3664 2010-07-13 11:55:19Z andy.harris $
#
import sys
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import Events
import Utils
import EventHandlers.tests.TestEventLogger as TestEventLogger

_log = logging.getLogger( "TestCounters" )

# Configuration for the tests
testConfigIncrement = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <increment name="entryCount" />
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>

                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigIncrementPublish = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <increment name="entryCount" />
                    </event>
                    <event>
                        <newEvent type="test/entryCount" source="test/entryCount">
                            <copy_other_data val="entryCount" />
                        </newEvent>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>
                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCountTotal">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigIncrement2 = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <increment name="entryCount" limit="2">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </increment>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>

                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCountTotal">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigIncrement2Reset = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <increment name="entryCount" limit="2" resetvalue="0">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </increment>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>

                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCountTotal">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigDecrement = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount" maximum="100" resetvalue="100"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <decrement name="entryCount" />
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>
                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigDecrement2 = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount" maximum="100" resetvalue="100"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <decrement name="entryCount" limit="98">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </decrement>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>
                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCountTotal">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigDecrement2Reset = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount" maximum="100" resetvalue="100"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <decrement name="entryCount" limit="98" resetvalue="100">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </decrement>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>
                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCountTotal">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigFloatIncrement = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount" type="float"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <increment name="entryCount" by="2.5"/>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>

                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigFloatDecrement = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount" type="float"/>
            <counter name="entryCount" maximum="100" resetvalue="95.5" type="float"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <decrement name="entryCount" by="2.5"/>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>
                        <reset name="entryCount">
                            <newEvent type="test/entryCount" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigIncrementReset = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount"/>

            <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                <eventsource source="webbrick/100/TD/0" >
                    <event>
                        <increment name="entryCount" />
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/minute">
                <eventsource source="time/minute" >
                    <event>
                        <reset name="entryCount">
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

            <eventtype type="http://id.webbrick.co.uk/events/time/hour">
                <eventsource source="time/hour" >
                    <event>
                        <newEvent type="test/entryCount" source="test/entryCount">
                            <copy_other_data val="entryCount" />
                        </newEvent>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigAll = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <eventtype type="http://id.webbrick.co.uk/events/time/minute">
                <eventsource source="time/minute" >
                    <event>
                        <!-- all three are optional -->
                        <increment name="count1" limit="" by="" resetvalue="">
                            <!-- if limit is reached then send newEvent and clear -->
                            <newEvent type="test/1" source="test/1">
                                <copy_other_data val="count1" />
                            </newEvent>
                        </increment>

                        <decrement name="count1" resetvalue="0" by="">
                            <!-- if 0 is reached then send newEvent and set to resetvalue -->
                            <newEvent type="test/1" source="test/1">
                                <copy_other_data val="count1" />
                            </newEvent>
                        </decrement>

                        <newEvent type="test/1" source="test/1">
                            <!-- used to send a counter -->
                            <copy_other_data val="count1" />
                        </newEvent>

                        <reset name="count1" resetvalue="0" >
                            <!-- send newEvent and set to resetvalue -->
                            <newEvent type="test/1" source="test/1">
                                <copy_other_data val="count1" />
                            </newEvent>
                        </reset>
                    </event>
                </eventsource>
            </eventtype>

            <!-- All counters must be declared -->
            <counter name="count1" minimum="0" maximum="2147483647" type="int|float"/>

        </eventInterface>
    </eventInterfaces>
"""

testConfigCounterSet = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount" type="int" />

            <eventtype type="test/event">
                <eventsource source="set/counter" >
                    <event>
                        <set name="entryCount" key="val" >
                            <newEvent type="test/1" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </set>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""

testConfigFloatCounterSet = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.Counters' name='Counters'>
            <!-- All counters must be declared -->
            <counter name="entryCount" type="float" />

            <eventtype type="test/event">
                <eventsource source="set/counter" >
                    <event>
                        <set name="entryCount" key="val" >
                            <newEvent type="test/1" source="test/entryCount">
                                <copy_other_data val="entryCount" />
                            </newEvent>
                        </set>
                    </event>
                </eventsource>
            </eventtype>

        </eventInterface>
    </eventInterfaces>
"""


class TestCounters(unittest.TestCase):

    def setUp(self):
        _log.debug( "\n\nsetUp" )

    def tearDown(self):
        _log.debug( "\n\ntearDown" )

    # Actual tests follow
    def testLoad(self):
        _log.debug( "\ntestLoad" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrement) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtMinute1 )

        Utils.expectNevents(self, 1)

        TestEventLogger.logEvents()
        self.assertEqual( len(TestEventLogger._events), 1)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )

    def testIntCounterSet(self):
        """
        Set Counter to a fixed value 
        """
        _log.debug( "\ntestIntCounterSet" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigCounterSet) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), makeEvent( 'test/event', 'set/counter', { 'val':'200' } ) )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "test/event" : 
                            [
                                ("set/counter" , 'val', 200)
                            ],
                    "test/1" : 
                            [   ("test/entryCount",'val', 200)
                            ]
                     }
       
        Utils.expectNevents(self, 2)
        
        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )


    def testFloatCounterSet(self):
        """
        Set Counter to a fixed value 
        """
        _log.debug( "\ntestFloatCounterSet" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigFloatCounterSet) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), makeEvent( 'test/event', 'set/counter', { 'val':'300.45' } ) )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "test/event" : 
                            [
                                ("set/counter" , 'val', 300.45)
                            ],
                    "test/1" : 
                            [   ("test/entryCount",'val', 300.45)
                            ]
                     }
       
        Utils.expectNevents(self, 2)

        
        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )


    def testIntCounter(self):
        """
        Normal increment, no events on increment just a reset
        """
        _log.debug( "\ntestIntCounter" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrement) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 2)
                            ],
                     }
        Utils.expectNevents(self, 4)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounterPublish(self):
        """
        Normal increment, events on limit and a reset event
        """
        _log.debug( "\ntestIntCounterPublish" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrementPublish) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 1)
                            ,   ("test/entryCount",'val', 2)
                            ,   ("test/entryCountTotal",'val', 2)
                            ],
                     }

        Utils.expectNevents(self, 6)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )


    def testIntCounter2(self):
        """
        Normal increment, events on limit and a reset event
        """
        _log.debug( "\ntestIntCounter2" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrement2) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 2)
                            ,   ("test/entryCountTotal",'val', 2)
                            ],
                     }
        Utils.expectNevents(self, 5)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounter2Reset(self):
        """
        Normal increment, events on limit and a reset event
        """
        _log.debug( "\ntestIntCounter2" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrement2Reset) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 2)
                            ,   ("test/entryCountTotal",'val', 0)   # we resetted counter
                            ],
                     }

        Utils.expectNevents(self, 5)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounter3(self):
        """
        Normal increment, events on limit no reset until twice below limit.
        """
        _log.debug( "\ntestIntCounter3" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrement2) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 2)
                            ,   ("test/entryCount",'val', 3)
                            ,   ("test/entryCountTotal",'val', 3)
                            ],
                     }
        Utils.expectNevents(self, 7)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounter3Reset(self):
        """
        """
        _log.debug( "\ntestIntCounter3Reset" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrement2Reset) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 2)
                            ,   ("test/entryCountTotal",'val', 1)
                            ],
                     }
        Utils.expectNevents(self, 6)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounterDec(self):
        _log.debug( "\ntestIntCounterDec" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigDecrement) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()

        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 98)
                            ],
                     }
        Utils.expectNevents(self, 4)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounterDec2(self):
        _log.debug( "\ntestIntCounterDec2" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigDecrement2) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()

        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 98)
                            ,   ("test/entryCountTotal",'val', 98)
                            ],
                     }
        Utils.expectNevents(self, 5)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounterDec2Reset(self):
        _log.debug( "\ntestIntCounterDec2Reset" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigDecrement2Reset) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()

        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 98)
                            ,   ("test/entryCountTotal",'val', 100)
                            ],
                     }
        Utils.expectNevents(self, 5)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounterDec3(self):
        _log.debug( "\ntestIntCounterDec3" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigDecrement2) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()

        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 98)
                            ,   ("test/entryCount",'val', 97)
                            ,   ("test/entryCountTotal",'val', 97)
                            ],
                     }
        Utils.expectNevents(self, 7)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounterDec3Reset(self):
        _log.debug( "\ntestIntCounterDec3Reset" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigDecrement2Reset) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()

        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 98)
                            ,   ("test/entryCountTotal",'val', 99)
                            ],
                     }
        Utils.expectNevents(self, 6)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testFloatCounter(self):
        _log.debug( "\ntestFloatCounter" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigFloatIncrement) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 5.0)
                            ],
                     }
        Utils.expectNevents(self, 4)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testFloatCounterDec(self):
        _log.debug( "\ntestIntCounterDec" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigFloatDecrement) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()

        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 90.5)
                            ],
                     }
        Utils.expectNevents(self, 4)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testIntCounterReset(self):
        _log.debug( "\ntestIntCounterReset" )
        self.loader = EventRouterLoader()
        errCount = self.loader.loadHandlers( getDictFromXmlString(testConfigIncrementReset) )
        self.assertEqual( errCount, 0)

        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtMinute1 )
        self.router.publish( EventAgent("testCounters"), Events.evtTD0 )
        self.router.publish( EventAgent("testCounters"), Events.evtHour03 )

        TestEventLogger.logEvents()
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/webbrick/TD" : 
                            [
                                ("webbrick/100/TD/0" , None, None),
                                ("webbrick/100/TD/0" , None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/minute" : 
                            [   ("time/minute",None, None)
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour",None, None)
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 1)
                            ],
                     }
        Utils.expectNevents(self, 5)

        haveErr, excessEvents = Utils.verifyEvents2( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testDummy(self):
        expectedEvents = { 
                    "local/url" : 
                            { 
                                "local/BoilerOn": 1,
                                "local/HwOn": 1 
                            },
                    "http://id.webbrick.co.uk/events/webbrick/DO" : 
                            {   "webbrick/100/DO/0": 1,
                                "webbrick/100/DO/1": 2,
                            },
                     }
                     
        haveErr, excessEvents = Utils.verifyEvents( expectedEvents, TestEventLogger._events )
        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

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
            [ "testLoad"
            , "testIntCounterSet"
            , "testFloatCounterSet"
            , "testIntCounter"
            , "testIntCounterPublish"
            , "testIntCounter2"
            , "testIntCounter3"
            , "testIntCounter2Reset"
            , "testIntCounter3Reset"
            , "testIntCounterDec"
            , "testIntCounterDec2"
            , "testIntCounterDec3"
            , "testIntCounterDec2Reset"
            , "testIntCounterDec3Reset"
            , "testFloatCounter"
            , "testFloatCounterDec"
            , "testIntCounterReset"
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
    return TestUtils.getTestSuite(TestCounters, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestCounters.log", getTestSuite, sys.argv)

