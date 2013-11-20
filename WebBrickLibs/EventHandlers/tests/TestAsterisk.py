# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestAsterisk.py 2612 2008-08-11 20:08:49Z graham.klyne $

import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

testConfigAsteriskListen = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="http://id.webbrick.co.uk/events/asterisk">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.Asterisk' name='Asterisk' listenPort="4573">
    </eventInterface>
</eventInterfaces>
"""

testConfigAsteriskSend = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="http://id.webbrick.co.uk/events/asterisk">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.Asterisk' name='Asterisk' listenPort="20998">
    </eventInterface>
</eventInterfaces>
"""

class TestAsterisk(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestAsterisk" )
        self._log.debug( "\n\nsetUp" )
        self.router = None
        self.loader = None
        return

    def tearDown(self):
        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        self._log.debug( "tearDown" )
        return

    # Actual tests follow
    def testListen(self):
        self._log.debug( "\ntestListen" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigAsteriskListen) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        cDown = 120
        while cDown > 0 and len(TestEventLogger._events) <= 0:
            cDown = cDown - 1
            time.sleep(1)

        TestEventLogger.logEvents()
        self.assert_( len(TestEventLogger._events) >= 1)

    def testSend(self):
        self._log.debug( "\ntestListen" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigAsteriskSend) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect(("localhost", 20998))

        skt.send( " agi_request: dialparties.agi\n" )
        skt.send( " agi_channel: SIP/100-b7a017f8\n" )
        skt.send( " agi_language: en\n" )
        skt.send( " agi_type: SIP\n" )
        skt.send( " agi_uniqueid: 1173178145.6\n" )
        skt.send( " agi_callerid: 100\n" )
        skt.send( " agi_calleridname: SNOM\n" )
        skt.send( " agi_callingpres: 0\n" )
        skt.send( " agi_callingani2: 0\n" )
        skt.send( " agi_callington: 0\n" )
        skt.send( " agi_callingtns: 0\n" )
        skt.send( " agi_dnid: 200\n" )
        skt.send( " agi_rdnis: unknown\n" )
        skt.send( " agi_context: macro-dial\n" )
        skt.send( " agi_extension: s\n" )
        skt.send( " agi_priority: 1\n" )
        skt.send( " agi_enhanced: 0.0\n" )
        skt.send( " agi_accountcode:\n" )
        skt.send( "\n" )

        skt.close()
    
        time.sleep(2)
        TestEventLogger.logEvents()
        self.assert_( len(TestEventLogger._events) >= 1)

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestAsterisk("testSend"))
    suite.addTest(TestAsterisk("testListen"))
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
        "zzunit": 
            [ "testDummy"
            ],
        "zzcomponent":
            [ "testDummy"
            ],
        "integration":
            [ "testSend"
            , "testListen"
            ],
        "zzpending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestCounters, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestCounters.log", getTestSuite, sys.argv)

