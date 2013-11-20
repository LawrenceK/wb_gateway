# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestRgbLedLighting.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# NOTE: this is not strictly a unit test, it requires a an RGB light and an RS485 port

import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

testConfigRgbLedLighting = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="time/second" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.RgbLedLighting' name='RgbLedLighting' serialPort='com9'>

        <eventtype type="">
            <eventsource source="time/second" >
                <event>
                    <params>
                        <testEq name="second" value ="1" />
                    </params>
                    <action task="rgb" red="64" green="0" blue="0" />
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="2" />
                    </params>
                    <action task="rgb" red="0" green="64" blue="0" />
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="3" />
                    </params>
                    <action task="rgb" red="0" green="0" blue="64" />
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="4" />
                    </params>
                    <action task="on"/>
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="5" />
                    </params>
                    <action task="off"/>
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="10" />
                    </params>
                    <action task="command" command="white" />
                </event>
            </eventsource>
        </eventtype>

    </eventInterface>
</eventInterfaces>
"""

testConfigBadcommand = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="time/second" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.RgbLedLighting' name='RgbLedLighting' serialPort='com9'>
        <eventtype type="">
            <eventsource source="time/second" >
                <event>
                    <params>
                        <testEq name="second" value ="5" />
                    </params>
                    <action task="command" command="red"/>
                </event>
            </eventsource>
        </eventtype>

    </eventInterface>
</eventInterfaces>
"""

class TestRgbLedLighting(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestRgbLedLighting" )
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

    def testLoadConfig(self):
        self._log.debug( "\ntestLoadConfig" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigRgbLedLighting) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(1)

    def testOn(self):
        self._log.debug( "\ntestRed" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigRgbLedLighting) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestRgbLedLighting"), Events.evtSecond4 )
        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()

        self.assertEqual( oldLen, 1 )

    def testOff(self):
        self._log.debug( "\ntestOff" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigRgbLedLighting) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestRgbLedLighting"), Events.evtSecond5 )
        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()

        self.assertEqual( oldLen, 1 )

    def testCommand(self):
        self._log.debug( "\ntestCommand" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigRgbLedLighting) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestRgbLedLighting"), Events.evtSecond10 )
        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()

        self.assertEqual( oldLen, 1 )

    def testRed(self):
        self._log.debug( "\ntestRed" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigRgbLedLighting) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestRgbLedLighting"), Events.evtSecond1 )
        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()

        self.assertEqual( oldLen, 1 )

    def testGreen(self):
        self._log.debug( "\ntestGreen" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigRgbLedLighting) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestRgbLedLighting"), Events.evtSecond2 )
        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()

        self.assertEqual( oldLen, 1 )

    def testBlue(self):
        self._log.debug( "\ntestBlue" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigRgbLedLighting) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestRgbLedLighting"), Events.evtSecond3 )
        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()

        self.assertEqual( oldLen, 1 )

    def testBadCommand(self):
        self._log.debug( "\ntestBadCommand" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigBadcommand) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestRgbLedLighting"), Events.evtSecond5 )
        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        TestEventLogger.logEvents()

        self.assertEqual( oldLen, 1 )

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
            [ "testLoadConfig"
            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testOn"
            , "testRed"
            , "testGreen"
            , "testBlue"
            , "testCommand"
            , "testOff"
            , "testBadCommand"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestRgbLedLighting, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestRgbLedLighting.log", getTestSuite, sys.argv)
