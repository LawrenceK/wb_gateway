# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestWebbrickMonitor.py 2612 2008-08-11 20:08:49Z graham.klyne $
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
from DummyRouter import DummyRouter

from EventHandlers.WebBrickMonitor    import WebBrickMonitor

testConfigSetTime = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.WebBrickMonitor' name='WebBrickMonitor' webReset='2'  clockReset='3' >
    </eventInterface>
</eventInterfaces>
"""

class TestWebbrickMonitor(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestWebbrickMonitor" )
        self._log.debug( "\n\nsetUp" )

        self.httpServer = None
        self.httpServer = TestHttpServer()
        self.httpServer.start()

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        if self.httpServer:
            self.httpServer.stop()
            self.httpServer = None

        time.sleep(1)

    def expectNhttp(self, cnt ):
        idx = 20
        while (len(self.httpServer.requests()) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(self.httpServer.requests()) != cnt):
            self.httpServer.logRequests()

        self.assertEqual( len(self.httpServer.requests()), cnt)

    # Actual tests follow

    def testSetTimeDirect(self):
        """
        This test is a bit of fiddle to work without the event router
        """
        self._log.debug( "\ntestSetTimeDirect" )

        runner = WebBrickMonitor( DummyRouter() )

        runner.handleEvent( Events.evtSS )
        runner.handleEvent( Events.evtSS )
        runner.handleEvent( Events.evtSS )
        runner.handleEvent( Events.evtMinute10 )    # request 
        # check http requests
        self.expectNhttp(0)

        runner.handleEvent( Events.evtSS )
        runner.handleEvent( Events.evtSS )
        runner.handleEvent( Events.evtSS )
        runner.handleEvent( Events.evtMinute11 )    # request 

        self.expectNhttp(2)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=%3ALG%3bpassword%3A" )
        self.assertEqual( self.httpServer.requests()[1], "/hid.spi?com=%3AST1%3b4%3b11%3A" )

    def testSetTime(self):
        self._log.debug( "\n\ntestSetTime" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSetTime) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtSS )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtSS )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtSS )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute10 )    # request 
        # check http requests
        self.expectNhttp(0)

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtSS )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtSS )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtSS )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 

        self.expectNhttp(2)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=%3ALG%3bpassword%3A" )
        self.assertEqual( self.httpServer.requests()[1], "/hid.spi?com=%3AST1%3b4%3b11%3A" )

    def testTimeSignalReboot(self):
        # see we get a log message for uptime < 120 seconds
        self._log.debug( "\ntestTimeSignalReboot" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSetTime) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        logHandler = testLogHandler()
        logHandler.setLevel( logging.INFO )
        addTestLogHandler(logHandler,'EventHandlers')

        elog = logging.getLogger( "EventHandlers.WebBrickMonitor" )
        elog.setLevel(logging.INFO)

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_1MinUpTime )
        time.sleep(1.0) # default router is threaded.
        assert logHandler.count() >= 1

        removeTestLogHandler(logHandler,'EventHandlers')

    def testTimeSignalSetTime(self):
        # see we get time reset when out by more than 60 nseconds for 5 minutes.
        self._log.debug( "\ntestTimeSignalReboot" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSetTime) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        logHandler = testLogHandler()
        addTestLogHandler(logHandler,'EventHandlers')

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_10MinUpTime )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_10MinUpTime )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_10MinUpTime )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 

        # check http requests, should be none so far
        self.expectNhttp(0)

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_10MinUpTime )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_10MinUpTime )
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 

        self.expectNhttp(2)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=%3ALG%3bpassword%3A" )
        self.assertEqual( self.httpServer.requests()[1], "/hid.spi?com=%3AST1%3b4%3b11%3A" )

        removeTestLogHandler(logHandler,'EventHandlers')

    def testTimeSignalResetSiteplayer(self):
        # see we get siteplayer reset when no messages from siteplayer for a while
        self._log.debug( "\ntestTimeSignalResetSiteplayer" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSetTime) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        logHandler = testLogHandler()
        addTestLogHandler(logHandler,'EventHandlers')

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_10MinUpTime )  # get detected
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 

        # check http requests, should be none so far
        self.expectNhttp(0)

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 
        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtMinute11 )    # request 

        self.expectNhttp(2)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=%3ALG%3bpassword%3A" )
        self.assertEqual( self.httpServer.requests()[1], "/hid.spi?com=%3ARS%3A" )

        removeTestLogHandler(logHandler,'EventHandlers')

    def testTimeOfDayResetSiteplayer(self):
        # see we get reset at 3 AM
        self._log.debug( "\ntestTimeOfDayResetSiteplayer" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSetTime) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtST_10MinUpTime )  # get detected

        # check http requests, should be none so far
        self.expectNhttp(0)

        self.router.publish( EventAgent("TestWebbrickMonitor"), Events.evtHour03 )    # request 

        self.expectNhttp(2)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?com=%3ALG%3bpassword%3A" )
        self.assertEqual( self.httpServer.requests()[1], "/hid.spi?com=%3ARS%3A" )

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
            [ "testSetTimeDirect"
            , "testSetTime"
            , "testTimeSignalReboot"
            , "testTimeSignalSetTime"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            # these two need rework to pick up UDP commands being sent out.
            , "testTimeSignalResetSiteplayer"
            , "testTimeOfDayResetSiteplayer"
            ]
        }
    return TestUtils.getTestSuite(TestWebbrickMonitor, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestWebbrickMonitor.log", getTestSuite, sys.argv)
