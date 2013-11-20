# $Id: TestTwistedReactor.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import logging
import sys
import time
import unittest

from MiscLib.DomHelpers  import *

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

from twisted.internet import reactor
from twisted.web import client

from Utils import *

# Configuration for the tests
testConfigTwistedReactor = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />
</eventInterfaces>
"""

_twisted = list()
_log = logging.getLogger( "TestTwistedReactor" )

testHost = "http://localhost:20999"
testUrl = "/test/url"

# minimal twisted callback.
def twistedTimeCallBack( msg ):
    _log.debug( "twistedTimeCallBack" )
    global _twisted
    _twisted.append("Success %s" % msg)

def twistedSuccessCallBack( result, msg ):
    _log.debug( "twistedSuccessCallBack" )
    global _twisted
    _twisted.append("Success")

def twistedErrorCallBack( result, other ):
    _log.debug( "twistedErrorCallBack" )
    global _twisted
    _twisted.append("Error %s" % other)

class TestTwistedReactor(unittest.TestCase):

    def setUp(self):
        _log.debug( "\n\nsetUp" )
        global _twisted
        _twisted = list()
        self.router = None
        self.loader = None

        self.httpServer = None
        self.httpServer = TestHttpServer()
        self.httpServer.start()

    def tearDown(self):
        _log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        if self.httpServer:
            self.httpServer.stop()

        time.sleep(0.1)

    def doCallLater(self, dt):
        reactor.callLater( dt, twistedTimeCallBack, "test" )

    def doHttpGet(self):

        deferred = client.getPage( "%s%s" % (testHost,testUrl) )
        deferred.addCallback( twistedSuccessCallBack, self )
        deferred.addErrback( twistedErrorCallBack, self )

    # Actual tests follow
    def testTwistedReactor(self):
        """
        Test thet the twisted reactor starts up.
        """
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTwistedReactor) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        reactor.callFromThread( self.doCallLater, 1 )

        time.sleep(2)
        _log.debug( "%s", (_twisted) )
        self.assertEqual( _twisted[0], "Success test" )

    def testHttpGet(self):
        """
        Test that a tiwsted HTTP get succedes.
        """
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTwistedReactor) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        reactor.callFromThread( self.doHttpGet )
        maxTime = 10
        while (len(self.httpServer.requests()) < 1) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        # now look for correct url requests

        _log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.assertEqual( self.httpServer.requests()[0], testUrl )

        _log.debug( "%s", (_twisted) )
        self.assertEqual( _twisted[0], "Success" )

    def testTwoCalls(self):
        """
        Test that a tiwsted HTTP get succedes.
        """
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTwistedReactor) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        reactor.callFromThread( self.doCallLater, 5 )

        reactor.callFromThread( self.doHttpGet )

        maxTime = 10
        while (len(self.httpServer.requests()) < 1) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        # now look for correct url requests

        _log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.assertEqual( self.httpServer.requests()[0], testUrl )

        time.sleep(10)
        _log.debug( "%s", (_twisted) )
        self.assertEqual( _twisted[0], "Success" )
        self.assertEqual( _twisted[1], "Success test" )

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
            [ "testTwistedReactor"
            , "testHttpGet"
            , "testTwoCalls"
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
    return TestUtils.getTestSuite(TestTwistedReactor, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestTwistedReactor.log", getTestSuite, sys.argv)
