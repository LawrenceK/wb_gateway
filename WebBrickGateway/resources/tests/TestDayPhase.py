# $Id: TestDayPhase.py 2611 2008-08-11 20:05:08Z graham.klyne $
#
import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import EventHandlers.tests.Events as Events
from EventHandlers.tests.Utils import *

# Configuration for the tests
#
# this test uses the two webbrick UDP triggers to trigger jobs.
# one job directly actions something
# The other job generates an event.
#
testDayPhaseConfig = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='resources/dayPhasePersist'>
    </eventInterface>

</eventInterfaces>
"""

testDayPhaseConfigBlank = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='resources/blankPersist'>
    </eventInterface>

</eventInterfaces>
"""

# "dayphase/weekday/morning" 04:30:00
# "dayphase/weekday/day" 09:00:00
# "dayphase/weekday/evening" 16:30:00
# "dayphase/weekday/night" 22:00:00

class TestDayPhase(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestDayPhase" )
        self._log.debug( "setUp" )
        self.runner = None

    def tearDown(self):
        self._log.debug( "tearDown" )

        TestEventLogger.logEvents()

        if self.runner:
            self.runner.stop()  # all tasks
            self.runner = None

    def load(self):
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testDayPhaseConfig) )
        self.loader.loadFromFile( "../../resources/eventdespatch/System/dayphase.xml" )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        
        time.sleep(1)   # let persist run.
        # we see persist events twice and generate 2 events for unknown - 10
        self.assert_( TestEventLogger.expectNevents(10) )
        TestEventLogger.logEvents()
        TestEventLogger.clearEvents()
        # clear events.

    def checkEvents(self, send, expect ):
        """
        send is tuples of an event and the number of events expected to be seen in the event log from the sending of the event
        expect is a list of events to be seen. We currently only check event source.
        
        If send has None as send event then we just check for events.
        """
        idx = 0
        limit = 0

        for ntry in send:
            if ntry[0]:
                self.router.publish( EventAgent("TestZones"), ntry[0] )
            limit = limit + ntry[1]
            while ( idx < limit ):
                self.assert_( TestEventLogger.expectAtLeastNevents(idx+1), "expecting %u events of %u" % (idx+1,limit)  )
                self._log.debug("%i check %s again %s" % (idx,TestEventLogger._events[idx],expect[idx]) )
                if isinstance(expect[idx], basestring):
                    # event source
                    self.assertEqual( TestEventLogger._events[idx].getSource(), expect[idx])
                elif isinstance(expect[idx], tuple) or isinstance(expect[idx], list):
                    # contains a test against the payload.
                    # assumes payload is a dictionary
                    # event source, attr, value
                    self.assertEqual( TestEventLogger._events[idx].getSource(), expect[idx][0])
                    od = TestEventLogger._events[idx].getPayload()
                    self.assertEqual( od[expect[idx][1]], expect[idx][2])
                else:
                    # assume event
                    self.assertEqual( TestEventLogger._events[idx].getSource(), expect[idx].getSource())
                idx = idx + 1

    def midnightStartup(self):
        self.load()

        # the events we send
        send = [ (Events.evtDark,1),
            (Events.evt0000,1),
            (Events.evtRuntime65,3)
            ]
        # the events that we expect to be logged.
        expect = [ "time/isDark",
            "time/minute",
            "time/runtime",
            ( "time/dayphase", "dayphasetext", "Night"),
            ( "time/dayphaseext", "dayphasetext", "Night:Dark"),
            ]

        self.checkEvents(send, expect)
        
        # clear all avents for visbility.
        TestEventLogger.clearEvents()

    # Actual tests follow

    def testLoad(self):
        self._log.debug( "testLoad" )
        self.load()

        TestEventLogger.logEvents()
            
    def testStartup1(self):
        self._log.debug( "testLoad" )
        self.load() # includes unknown and clears events
        time.sleep(1)
                
        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        self.assert_( TestEventLogger.expectNevents(1) )
        # no idea of time so unknown.
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/runtime" )
        # the rest are configuration.
        #self.assertEqual( TestEventLogger._events[10].getSource(), "time/dayphase" )
        #self.assertEqual( TestEventLogger._events[11].getSource(), "time/dayphaseext" )

    def testStartup2(self):
        self._log.debug( "testLoad2" )
        self.load()
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        time.sleep(0.1)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.1)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 2)

        # still no idea of time so still unknown.
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/isDark" )

    def testStartup3(self):
        self._log.debug( "testLoad2" )
        self.load()
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.1)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 1)

        # no idea of time so unknown, which is sent at startup
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )

    def testStartupNightDark(self):
        # night dark
        self._log.debug( "testStartupNightDark" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        self.assert_( TestEventLogger.expectNevents(1) )

        self.router.publish( EventAgent("TestDayPhase"), Events.evt0000 )
        self.assert_( TestEventLogger.expectNevents(2) )

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        self.assert_( TestEventLogger.expectNevents(5) )

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night:Dark" )

    def testStartupNightLight(self):
        # night dark
        self._log.debug( "testStartupNightLight" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evt0000 )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        time.sleep(0.2)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '2' )
        self.assertEqual( od["dayphasetext"], "Night:Light" )

    def testStartupNightLightNotSet(self):
        # night dark
        self._log.debug( "testStartupNightLightNotSet" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testDayPhaseConfigBlank) )
        self.loader.loadFromFile( "../../resources/eventdespatch/System/dayphase.xml" )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
                
        time.sleep(1)   # let persist run.

        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        self.assert_( TestEventLogger.expectAtLeastNevents(1) )

        self.router.publish( EventAgent("TestDayPhase"), Events.evt0000 )
        self.assert_( TestEventLogger.expectAtLeastNevents(2) )

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        self.assert_( TestEventLogger.expectAtLeastNevents(5) )

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/dayphase" )
        od = TestEventLogger._events[1].getPayload()
        self.assertEqual( od["dayphase"], '0' )
        self.assertEqual( od["dayphasetext"], "Unknown" )
        
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["dayphase"], '0' )
        self.assertEqual( od["dayphasetext"], "Unknown" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/runtime" )

    def testStartupMorningDark(self):
        # night dark
        self._log.debug( "testStartupMorningDark" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evt0500 )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        time.sleep(0.2)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning:Dark" )

    def testStartupMorningLight(self):
        # night dark
        self._log.debug( "testStartupMorningLight" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evt0500 )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        time.sleep(0.2)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '4' )
        self.assertEqual( od["dayphasetext"], "Morning:Light" )

    def testStartupDayDark(self):
        # night dark
        self._log.debug( "testStartupDayDark" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evt1200 )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        time.sleep(0.2)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day:Dark" )

    def testStartupDayLight(self):
        # night dark
        self._log.debug( "testStartupDayLight" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evt1200 )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        time.sleep(0.2)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '6' )
        self.assertEqual( od["dayphasetext"], "Day:Light" )

    def testStartupEveningDark(self):
        # night dark
        self._log.debug( "testStartupEveningDark" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        self.assert_( TestEventLogger.expectNevents(1) )

        self.router.publish( EventAgent("TestDayPhase"), Events.evt1800 )
        self.assert_( TestEventLogger.expectNevents(2) )

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        self.assert_( TestEventLogger.expectNevents(5) )

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening:Dark" )

    def testStartupEveningLight(self):
        # night dark
        self._log.debug( "testStartupEveningLight" )
        self.load()

        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evt1800 )
        time.sleep(0.2)   # let avove run

        self.router.publish( EventAgent("TestDayPhase"), Events.evtRuntime65 )
        time.sleep(0.2)   # let avove run

        TestEventLogger.logEvents()
            
        self.assertEqual( len(TestEventLogger._events), 5)
        
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/runtime" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/dayphase" )
        od = TestEventLogger._events[3].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '8' )
        self.assertEqual( od["dayphasetext"], "Evening:Light" )

    def testTransitionsLightNight(self):
        # We get light at night and do not go dark until night again.

        self._log.debug( "testTransitionsLightNight" )
        self.midnightStartup()
        
        # it is currently night and dark.
        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 3)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/dayphase" )
        od = TestEventLogger._events[1].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["dayphase"], '2' )
        self.assertEqual( od["dayphasetext"], "Night:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0430 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 6)
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphase" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[5].getPayload()
        self.assertEqual( od["dayphase"], '4' )
        self.assertEqual( od["dayphasetext"], "Morning:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0900 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 9)
        self.assertEqual( TestEventLogger._events[6].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "time/dayphase" )
        od = TestEventLogger._events[7].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[8].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[8].getPayload()
        self.assertEqual( od["dayphase"], '6' )
        self.assertEqual( od["dayphasetext"], "Day:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1630 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 12)
        self.assertEqual( TestEventLogger._events[9].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[10].getSource(), "time/dayphase" )
        od = TestEventLogger._events[10].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[11].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[11].getPayload()
        self.assertEqual( od["dayphase"], '8' )
        self.assertEqual( od["dayphasetext"], "Evening:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt2200 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 15)
        self.assertEqual( TestEventLogger._events[12].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[13].getSource(), "time/dayphase" )
        od = TestEventLogger._events[13].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[14].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[14].getPayload()
        self.assertEqual( od["dayphase"], '2' )
        self.assertEqual( od["dayphasetext"], "Night:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run
            
        # get double issue of dayphase events when dark transition is on the hour.
        
        self.assertEqual( len(TestEventLogger._events), 18)
        self.assertEqual( TestEventLogger._events[15].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[16].getSource(), "time/dayphase" )
        od = TestEventLogger._events[16].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[17].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[17].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night:Dark" )

    def testTransitionsLightMorning(self):
        # gets light in morning and dark in evening.

        self._log.debug( "testTransitionsLightNight" )
        self.midnightStartup()
        
        # it is currently night and dark.
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0430 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 3)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/dayphase" )
        od = TestEventLogger._events[1].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 6)
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphase" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[5].getPayload()
        self.assertEqual( od["dayphase"], '4' )
        self.assertEqual( od["dayphasetext"], "Morning:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0900 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 9)
        self.assertEqual( TestEventLogger._events[6].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "time/dayphase" )
        od = TestEventLogger._events[7].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[8].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[8].getPayload()
        self.assertEqual( od["dayphase"], '6' )
        self.assertEqual( od["dayphasetext"], "Day:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1630 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 12)
        self.assertEqual( TestEventLogger._events[9].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[10].getSource(), "time/dayphase" )
        od = TestEventLogger._events[10].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[11].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[11].getPayload()
        self.assertEqual( od["dayphase"], '8' )
        self.assertEqual( od["dayphasetext"], "Evening:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 15)
        self.assertEqual( TestEventLogger._events[12].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[13].getSource(), "time/dayphase" )
        od = TestEventLogger._events[13].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[14].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[14].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt2200 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 18)
        self.assertEqual( TestEventLogger._events[15].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[16].getSource(), "time/dayphase" )
        od = TestEventLogger._events[16].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[17].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[17].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night:Dark" )

    def testTransitionsLightDay(self):
        # gets light in morning and dark in evening.

        self._log.debug( "testTransitionsLightDay" )
        self.midnightStartup()
        
        # it is currently night and dark.
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0430 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 3)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/dayphase" )
        od = TestEventLogger._events[1].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0900 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 6)
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphase" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[5].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 9)
        self.assertEqual( TestEventLogger._events[6].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "time/dayphase" )
        od = TestEventLogger._events[7].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[8].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[8].getPayload()
        self.assertEqual( od["dayphase"], '6' )
        self.assertEqual( od["dayphasetext"], "Day:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 12)
        self.assertEqual( TestEventLogger._events[9].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[10].getSource(), "time/dayphase" )
        od = TestEventLogger._events[10].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[11].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[11].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1630 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 15)
        self.assertEqual( TestEventLogger._events[12].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[13].getSource(), "time/dayphase" )
        od = TestEventLogger._events[13].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[14].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[14].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt2200 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 18)
        self.assertEqual( TestEventLogger._events[15].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[16].getSource(), "time/dayphase" )
        od = TestEventLogger._events[16].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[17].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[17].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night:Dark" )

    def testTransitionsLightNight2(self):
        # We get light at night and do not go dark until night again.

        self._log.debug( "testTransitionsLightNight" )
        self.midnightStartup()
        
        # it is currently night and dark.
        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 3)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/dayphase" )
        od = TestEventLogger._events[1].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["dayphase"], '2' )
        self.assertEqual( od["dayphasetext"], "Night:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0430 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 6)
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphase" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[5].getPayload()
        self.assertEqual( od["dayphase"], '4' )
        self.assertEqual( od["dayphasetext"], "Morning:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0900 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 9)
        self.assertEqual( TestEventLogger._events[6].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "time/dayphase" )
        od = TestEventLogger._events[7].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[8].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[8].getPayload()
        self.assertEqual( od["dayphase"], '6' )
        self.assertEqual( od["dayphasetext"], "Day:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1630 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 12)
        self.assertEqual( TestEventLogger._events[9].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[10].getSource(), "time/dayphase" )
        od = TestEventLogger._events[10].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[11].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[11].getPayload()
        self.assertEqual( od["dayphase"], '8' )
        self.assertEqual( od["dayphasetext"], "Evening:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt2200 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 15)
        self.assertEqual( TestEventLogger._events[12].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[13].getSource(), "time/dayphase" )
        od = TestEventLogger._events[13].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[14].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[14].getPayload()
        self.assertEqual( od["dayphase"], '2' )
        self.assertEqual( od["dayphasetext"], "Night:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt2201 )
        time.sleep(0.2)   # let avove run
        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run
            
        # get double issue of dayphase events when dark transition is on the hour.
        
        self.assertEqual( len(TestEventLogger._events), 19)
        self.assertEqual( TestEventLogger._events[15].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[16].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[17].getSource(), "time/dayphase" )
        od = TestEventLogger._events[17].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[18].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[18].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night:Dark" )

    def testTransitionsLightMorning2(self):
        # gets light in morning and dark in evening.

        self._log.debug( "testTransitionsLightNight" )
        self.midnightStartup()
        
        # it is currently night and dark.
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0430 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 3)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/dayphase" )
        od = TestEventLogger._events[1].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0431 )
        time.sleep(0.2)   # let avove run
        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 7)
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "time/dayphase" )
        od = TestEventLogger._events[5].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[6].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[6].getPayload()
        self.assertEqual( od["dayphase"], '4' )
        self.assertEqual( od["dayphasetext"], "Morning:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0900 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 10)
        self.assertEqual( TestEventLogger._events[7].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[8].getSource(), "time/dayphase" )
        od = TestEventLogger._events[8].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[9].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[9].getPayload()
        self.assertEqual( od["dayphase"], '6' )
        self.assertEqual( od["dayphasetext"], "Day:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1630 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 13)
        self.assertEqual( TestEventLogger._events[10].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[11].getSource(), "time/dayphase" )
        od = TestEventLogger._events[11].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[12].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[12].getPayload()
        self.assertEqual( od["dayphase"], '8' )
        self.assertEqual( od["dayphasetext"], "Evening:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1631 )
        time.sleep(0.2)   # let avove run
        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 17)
        self.assertEqual( TestEventLogger._events[13].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[14].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[15].getSource(), "time/dayphase" )
        od = TestEventLogger._events[15].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[16].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[16].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt2200 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 20)
        self.assertEqual( TestEventLogger._events[17].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[18].getSource(), "time/dayphase" )
        od = TestEventLogger._events[18].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[19].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[19].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night:Dark" )

    def testTransitionsLightDay2(self):
        # gets light in morning and dark in evening.

        self._log.debug( "testTransitionsLightDay" )
        self.midnightStartup()
        
        # it is currently night and dark.
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0430 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 3)
        self.assertEqual( TestEventLogger._events[0].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "time/dayphase" )
        od = TestEventLogger._events[1].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[2].getPayload()
        self.assertEqual( od["dayphase"], '3' )
        self.assertEqual( od["dayphasetext"], "Morning:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0900 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 6)
        self.assertEqual( TestEventLogger._events[3].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "time/dayphase" )
        od = TestEventLogger._events[4].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[5].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt0901 )
        time.sleep(0.2)   # let avove run
        self.router.publish( EventAgent("TestDayPhase"), Events.evtLight )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 10)
        self.assertEqual( TestEventLogger._events[6].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[8].getSource(), "time/dayphase" )
        od = TestEventLogger._events[8].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[9].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[9].getPayload()
        self.assertEqual( od["dayphase"], '6' )
        self.assertEqual( od["dayphasetext"], "Day:Light" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1629 )
        time.sleep(0.2)   # let avove run
        self.router.publish( EventAgent("TestDayPhase"), Events.evtDark )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 14)
        self.assertEqual( TestEventLogger._events[10].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[11].getSource(), "time/isDark" )
        self.assertEqual( TestEventLogger._events[12].getSource(), "time/dayphase" )
        od = TestEventLogger._events[12].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day" )
        self.assertEqual( TestEventLogger._events[13].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[13].getPayload()
        self.assertEqual( od["dayphase"], '5' )
        self.assertEqual( od["dayphasetext"], "Day:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt1630 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 17)
        self.assertEqual( TestEventLogger._events[14].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[15].getSource(), "time/dayphase" )
        od = TestEventLogger._events[15].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening" )
        self.assertEqual( TestEventLogger._events[16].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[16].getPayload()
        self.assertEqual( od["dayphase"], '7' )
        self.assertEqual( od["dayphasetext"], "Evening:Dark" )
        
        self.router.publish( EventAgent("TestDayPhase"), Events.evt2200 )
        time.sleep(0.2)   # let avove run
            
        self.assertEqual( len(TestEventLogger._events), 20)
        self.assertEqual( TestEventLogger._events[17].getSource(), "time/minute" )
        self.assertEqual( TestEventLogger._events[18].getSource(), "time/dayphase" )
        od = TestEventLogger._events[18].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night" )
        self.assertEqual( TestEventLogger._events[19].getSource(), "time/dayphaseext" )
        od = TestEventLogger._events[19].getPayload()
        self.assertEqual( od["dayphase"], '1' )
        self.assertEqual( od["dayphasetext"], "Night:Dark" )

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
            , "testStartup1"
            , "testStartup2"
            , "testStartup3"
            , "testStartupNightDark"
            , "testStartupNightLight"
            , "testStartupNightLightNotSet"
            , "testStartupEveningDark"
            , "testStartupEveningLight"
            , "testStartupDayDark"
            , "testStartupDayLight"
            , "testStartupEveningDark"
            , "testStartupEveningLight"
            , "testTransitionsLightNight"
            , "testTransitionsLightMorning"
            , "testTransitionsLightDay"
            , "testTransitionsLightNight2"
            , "testTransitionsLightMorning2"
            , "testTransitionsLightDay2"
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
    return TestUtils.getTestSuite(TestDayPhase, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestDayPhase.log", getTestSuite, sys.argv)
