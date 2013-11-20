# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestEggNunciate.py 2612 2008-08-11 20:08:49Z graham.klyne $
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

# a test with a single egg
testConfigEggNunciate1 = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.EggNunciate' name='EggNunciate'>

        <eventtype type="">
            <!-- setup default scene -->
            <eventsource source="time/runtime" >
	        <event>
                    <params>
                        <testEq name="elapsed">
                            <value>5</value>
                        </testEq>
                    </params>
		    <add name="defaultHigh" egg="lower" pri="0"/>
		    <add name="defaultLow" egg="lower" pri="0"/>
	        </event>
            </eventsource>
        </eventtype>

        <eventtype type="">
            <!-- setup default scene -->
            <eventsource source="time/second" >
	        <event>
		    <next/>
	        </event>
            </eventsource>
        </eventtype>

        <eventtype type="">
            <!-- Garage -->
            <eventsource source="webbrick/100/DO/0" >
	        <event>
                    <params>
                        <testEq name="state">
                            <value>1</value>
                        </testEq>
                    </params>
		    <add name="garageOpenLow" egg="lower" pri="1"/>
		    <add name="garageOpenHigh" egg="lower" pri="1"/>
		    <add name="somethingActive" egg="lower" pri="1"/>
	        </event>
	        <event>
                    <params>
                        <testEq name="state">
                            <value>0</value>
                        </testEq>
                    </params>
		    <delete name="garageOpenLow" egg="lower" pri="1"/>
		    <delete name="garageOpenHigh" egg="lower" pri="1"/>
		    <delete name="somethingActive" egg="lower" pri="1"/>
	        </event>
            </eventsource>

            <!-- Alarm -->
            <eventsource source="webbrick/100/DO/1" >
	        <event>
                    <params>
                        <testEq name="state">
                            <value>1</value>
                        </testEq>
                    </params>
		    <add name="AlarmOnLow" egg="lower" pri="1"/>
		    <add name="AlarmOnHigh" egg="lower" pri="1"/>
		    <add name="somethingActive" egg="lower" pri="1"/>
	        </event>
	        <event>
                    <params>
                        <testEq name="state">
                            <value>0</value>
                        </testEq>
                    </params>
		    <delete name="AlarmOnLow" egg="lower" pri="1"/>
		    <delete name="AlarmOnHigh" egg="lower" pri="1"/>
		    <delete name="somethingActive" egg="lower" pri="1"/>
	        </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <step id="defaultHigh" redMin="16" redMax="16" blueMin="16" blueMax="16"  greenMin="16" greenMax="16"/>
        <step id="defaultLow" redMin="8" redMax="8" blueMin="8" blueMax="8"  greenMin="8" greenMax="8"/>

        <step id="AlarmOnLow" redMin="33" redMax="33" blueMin="33" blueMax="33"  greenMin="33" greenMax="33"/>
        <step id="AlarmOnHigh" redMin="47" redMax="47" blueMin="47" blueMax="47"  greenMin="47" greenMax="47"/>

        <step id="garageOpenLow" redMin="32" redMax="32" blueMin="32" blueMax="32"  greenMin="32" greenMax="32"/>
        <step id="garageOpenHigh" redMin="48" redMax="48" blueMin="48" blueMax="48"  greenMin="48" greenMax="48"/>

        <step id="somethingActive" redMin="4" redMax="4" blueMin="4" blueMax="4"  greenMin="4" greenMax="4"/>

        <!-- what eggs we have and there addresses and channels -->
        <!-- the cmdTemplate and adr are mandatory, the cmdTemplate will be filled using a combination of the dictionary with all
            these attributes and the red,green,blue attributes calculated for a scene -->
        <egg name="lower" adr="localhost:20999" 
                redChn="0" greenChn="1" blueChn="2" 
                cmdTemplate="/hid.spi?com=:DM%(redChn)s;%(red)s;%(greenChn)s;%(green)s;%(blueChn)s;%(blue)s:"/>

    </eventInterface>
</eventInterfaces>
"""

# a test with two egg
testConfigEggNunciate2 = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.EggNunciate' name='EggNunciate'>

        <eventtype type="">
            <!-- setup default scene -->
            <eventsource source="time/runtime" >
	        <event>
                    <params>
                        <testEq name="elapsed">
                            <value>5</value>
                        </testEq>
                    </params>
		    <add name="defaultHigh" egg="lower" pri="0"/>
		    <add name="defaultHigh" egg="upper" pri="0"/>
		    <add name="defaultLow" egg="lower" pri="0"/>
		    <add name="defaultLow" egg="upper" pri="0"/>
	        </event>
            </eventsource>
        </eventtype>

        <eventtype type="">
            <!-- setup default scene -->
            <eventsource source="time/second" >
	        <event>
		    <next/>
	        </event>
            </eventsource>
        </eventtype>

        <eventtype type="">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/DO/0" >
	        <event>
                    <params>
                        <testEq name="state">
                            <value>1</value>
                        </testEq>
                    </params>
		    <add name="garageOpenLow" egg="lower" pri="1"/>
		    <add name="garageOpenHigh" egg="lower" pri="1"/>
		    <add name="somethingActive" egg="lower" pri="1"/>
	        </event>
	        <event>
                    <params>
                        <testEq name="state">
                            <value>0</value>
                        </testEq>
                    </params>
		    <delete name="garageOpenLow" egg="lower" pri="1"/>
		    <delete name="garageOpenHigh" egg="lower" pri="1"/>
		    <delete name="somethingActive" egg="lower" pri="1"/>
	        </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <step id="defaultHigh" redMin="16" redMax="16" blueMin="16" blueMax="16"  greenMin="16" greenMax="16"/>
        <step id="defaultLow" redMin="8" redMax="8" blueMin="8" blueMax="8"  greenMin="8" greenMax="8"/>

        <step id="garageOpenLow" redMin="32" redMax="32" blueMin="32" blueMax="32"  greenMin="32" greenMax="32"/>
        <step id="garageOpenHigh" redMin="48" redMax="48" blueMin="48" blueMax="48"  greenMin="48" greenMax="48"/>

        <step id="somethingActive" redMin="4" redMax="4" blueMin="4" blueMax="4"  greenMin="4" greenMax="4"/>

        <!-- what eggs we have and there addresses and channels -->
        <!-- the cmdTemplate and adr are mandatory, the cmdTemplate will be filled using a combination of the dictionary with all
            these attributes and the red,green,blue attributes calculated for a scene -->
        <egg name="lower" adr="localhost:20999" 
                redChn="0" greenChn="1" blueChn="2" 
                cmdTemplate="/hid.spi?com=:DM%(redChn)s;%(red)s;%(greenChn)s;%(green)s;%(blueChn)s;%(blue)s:"/>
        <egg name="upper" adr="localhost:20999" 
                redChn="3" greenChn="4" blueChn="5" 
                cmdTemplate="/hid.spi?com=:DM%(redChn)s;%(red)s;%(greenChn)s;%(green)s;%(blueChn)s;%(blue)s:"/>

    </eventInterface>
</eventInterfaces>
"""

class TestEggNunciate(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestEggNunciate" )
        self._log.debug( "\n\nsetUp" )

        self.httpServer = None
        self.httpServer = TestHttpServer()
        self.httpServer.start()

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        time.sleep(1)   # allow twisted time
        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        if self.httpServer:
            self.httpServer.stop()

        time.sleep(5)

    def expectNhttp(self, cnt ):
        idx = 20
        while (len(self.httpServer.requests()) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(self.httpServer.requests()) != cnt):
            for req in self.httpServer.requests():
                self._log.debug( "request %s", req )

        self.assertEqual( len(self.httpServer.requests()), cnt)

    # Actual tests follow
    def testEggNunciateSingle(self):
        self._log.debug( "\ntestEggNunciateSingle" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEggNunciate1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtRuntime5 )    # set up base scene
        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )

        # expect single HTTP request for default scene step 1.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 1)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=:DM0;16;1;16;2;16:" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )
        # expect second HTTP request for default scene step 2.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 2)
        self.assertEqual( self.httpServer.requests()[1], "/hid.spi?com=:DM0;8;1;8;2;8:" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )
        # expect third HTTP request for default scene step 1.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 3)
        self.assertEqual( self.httpServer.requests()[2], "/hid.spi?com=:DM0;16;1;16;2;16:" )

    def testEggNunciateTwo(self):
        self._log.debug( "\ntestEggNunciateTwo" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEggNunciate2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtRuntime5 )    # set up base scene
        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )

        # expect single HTTP request for default scene step 1.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 2)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=:DM3;16;4;16;5;16:" )
        self.assertEqual( self.httpServer.requests()[1], "/hid.spi?com=:DM0;16;1;16;2;16:" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )
        # expect second HTTP request for default scene step 2.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 4)
        self.assertEqual( self.httpServer.requests()[3], "/hid.spi?com=:DM0;8;1;8;2;8:" )
        self.assertEqual( self.httpServer.requests()[2], "/hid.spi?com=:DM3;8;4;8;5;8:" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )
        # expect third HTTP request for default scene step 1.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 6)
        self.assertEqual( self.httpServer.requests()[5], "/hid.spi?com=:DM0;16;1;16;2;16:" )
        self.assertEqual( self.httpServer.requests()[4], "/hid.spi?com=:DM3;16;4;16;5;16:" )

    def subCheckSeq(self, reqs):
        # each time tick causes another http request
        idx = len(self.httpServer.requests())
        for i in range(len(reqs)):
            self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )
            self.expectNhttp( idx+1 )
            hReq = self.httpServer.requests()[idx]
            self._log.debug( "testHttpAction (%u:%s) (%u:%s)", idx, hReq, i, reqs[i] )
            self.assertEqual( hReq, reqs[i] )
            idx = idx + 1

    def subTestGarageOpen(self):
        self._log.debug( "\nsubTestGarageOpen" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtDO_0_on )

        reqs = ["/hid.spi?com=:DM0;32;1;32;2;32:",
                "/hid.spi?com=:DM0;48;1;48;2;48:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
                "/hid.spi?com=:DM0;32;1;32;2;32:",
                "/hid.spi?com=:DM0;48;1;48;2;48:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
            ]
        self.subCheckSeq(reqs)

    def subTestGarageClose(self):
        self._log.debug( "\nsubTestGarageClose" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtDO_0_off )

        reqs = ["/hid.spi?com=:DM0;16;1;16;2;16:",
                "/hid.spi?com=:DM0;8;1;8;2;8:",
                "/hid.spi?com=:DM0;16;1;16;2;16:",
                "/hid.spi?com=:DM0;8;1;8;2;8:",
            ]
        self.subCheckSeq(reqs)

    # Actual tests follow
    def testEggNunciateGarage(self):
        self._log.debug( "\ntestEggNunciateEvent" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEggNunciate1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtRuntime5 )    # set up base scene
        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )

        # expect HTTP request for default scene 1 step 1.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 1)
        hReq = self.httpServer.requests()[len(self.httpServer.requests())-1]
        self.assertEqual( hReq, "/hid.spi?com=:DM0;16;1;16;2;16:" )

        self.subTestGarageOpen()
        self.expectNhttp( 7)
        self.subTestGarageClose()
        self.expectNhttp( 11)

        self.subTestGarageOpen()
        self.expectNhttp( 17)
        self.subTestGarageClose()
        self.expectNhttp( 21)

    def subTestAlarmOn(self):
        self._log.debug( "\nsubTestAlarmOn" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtDO_1_on )

        reqs = ["/hid.spi?com=:DM0;33;1;33;2;33:",
                "/hid.spi?com=:DM0;47;1;47;2;47:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
                "/hid.spi?com=:DM0;33;1;33;2;33:",
                "/hid.spi?com=:DM0;47;1;47;2;47:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
            ]
        self.subCheckSeq(reqs)

    def subTestAlarmOff(self):
        self._log.debug( "\nsubTestAlarmOn" )

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtDO_1_off )

        reqs = ["/hid.spi?com=:DM0;16;1;16;2;16:",
                "/hid.spi?com=:DM0;8;1;8;2;8:",
                "/hid.spi?com=:DM0;16;1;16;2;16:",
                "/hid.spi?com=:DM0;8;1;8;2;8:",
            ]
        self.subCheckSeq(reqs)

    # Actual tests follow
    def testEggNunciateAlarm(self):
        self._log.debug( "\ntestEggNunciateAlarm" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEggNunciate1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtRuntime5 )    # set up base scene
        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )

        # expect HTTP request for default scene 1 step 1.
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.expectNhttp( 1)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=:DM0;16;1;16;2;16:" )

        self.subTestAlarmOn()
        self.subTestAlarmOff()

        self.subTestAlarmOn()
        self.subTestAlarmOff()

    # Actual tests follow
    def testEggNunciateGarageAlarm(self):
        self._log.debug( "\ntestEggNunciateGarageAlarm" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEggNunciate1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtRuntime5 )    # set up base scene
        self.router.publish( EventAgent("TestEggNunciate"), Events.evtSecond5 )

        # expect HTTP request for default scene 1 step 1.
        self.expectNhttp( 1)
        hReq = self.httpServer.requests()[len(self.httpServer.requests())-1]
        self._log.debug( "testHttpAction %u:%s", (len(self.httpServer.requests())-1,hReq) )
        self.assertEqual( hReq, "/hid.spi?com=:DM0;16;1;16;2;16:" )

        self.subTestGarageOpen()
        self.expectNhttp( 7)

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtDO_1_on )

        reqs = ["/hid.spi?com=:DM0;33;1;33;2;33:",
                "/hid.spi?com=:DM0;47;1;47;2;47:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
                "/hid.spi?com=:DM0;32;1;32;2;32:",
                "/hid.spi?com=:DM0;48;1;48;2;48:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
                "/hid.spi?com=:DM0;33;1;33;2;33:",
                "/hid.spi?com=:DM0;47;1;47;2;47:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
                "/hid.spi?com=:DM0;32;1;32;2;32:",
                "/hid.spi?com=:DM0;48;1;48;2;48:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
                
            ]
        self.subCheckSeq(reqs)

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtDO_0_off )    # garage closed

        reqs = ["/hid.spi?com=:DM0;33;1;33;2;33:",
                "/hid.spi?com=:DM0;47;1;47;2;47:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
                "/hid.spi?com=:DM0;33;1;33;2;33:",
                "/hid.spi?com=:DM0;47;1;47;2;47:",
                "/hid.spi?com=:DM0;4;1;4;2;4:",
            ]
        self.subCheckSeq(reqs)

        self.router.publish( EventAgent("TestEggNunciate"), Events.evtDO_1_off )    # Alarm

        reqs = ["/hid.spi?com=:DM0;16;1;16;2;16:",
                "/hid.spi?com=:DM0;8;1;8;2;8:",
                "/hid.spi?com=:DM0;16;1;16;2;16:",
                "/hid.spi?com=:DM0;8;1;8;2;8:",
            ]
        self.subCheckSeq(reqs)

    def testDummy(self):
        pass

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
            [ "testEggNunciateSingle"
            , "testEggNunciateTwo"
            , "testEggNunciateGarage"
            , "testEggNunciateAlarm"
            , "testEggNunciateGarageAlarm"
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
    return TestUtils.getTestSuite(TestEggNunciate, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestEggNunciate.log", getTestSuite, sys.argv)

