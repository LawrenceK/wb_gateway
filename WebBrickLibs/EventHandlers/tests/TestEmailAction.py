# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestEmailAction.py 2612 2008-08-11 20:08:49Z graham.klyne $
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
#
# this test uses the an event to send email.
#
testConfigEmail = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.EmailAction' name='EmailAction' smartHost='localhost' smartPort='12345'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
	        <event>
                    <params>
                    </params>
                    <email>
                        <to>TestUser</to>
                        <from>TestUser</from>
                        <body>TestUser</body>
                        <subject>TestUser</subject>
                    </email>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

testConfigEmail2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.EmailAction' name='EmailAction' smartHost='localhost' smartPort='12346'>
        <eventtype type="">
            <eventsource source="webbrick/100/DO/0" >
	        <event>
                    <params>
                    </params>
                    <email>
                        <to>TestUser</to>
                        <from>TestUser</from>
                        <body>TestUser %(state)s</body>
                        <subject>TestUser %(state)s</subject>
                    </email>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

class TestEmailAction(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestEmailAction" )
        self._log.debug( "\n\nsetUp" )

        self.smtpServer = None

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        if self.smtpServer:
            self.smtpServer.stop()
            self.smtpServer = None

        time.sleep(2)

    def waitNRequest(self, cnt):
        limit = 10
        while len(self.smtpServer.requests()) <> cnt and limit > 0:
            time.sleep(0.2)
            limit = limit - 1
        if len(self.smtpServer.requests()) <> cnt:
            self._log.debug( "testEmailEvent %s", self.smtpServer.requests() )
            
        self.assertEqual( len(self.smtpServer.requests()), cnt)
    
    # Actual tests follow
    def testEmailEvent(self):
        self._log.debug( "\n\ntestEmailEvent" )

        self.smtpServer = TestSmtpServer(12345)
        self.smtpServer.start()

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEmail) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(0.5)

        self.router.publish( EventAgent("TestMailAction"), Events.evtTD0 )    # 0 Off
        self.router.publish( EventAgent("TestMailAction"), Events.evtTD1 )    # 1 Off

        self.waitNRequest(1)

    def testEmailEvent2(self):
        self._log.debug( "\n\ntestEmailEvent2" )

        self.smtpServer = TestSmtpServer(12346) 
        self.smtpServer.start()

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEmail2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(0.5)

        self.router.publish( EventAgent("TestMailAction"), Events.evtDO_0_on )    # 0 Off

        self.waitNRequest(1)


# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestEmailAction("testEmailEvent"))
    suite.addTest(TestEmailAction("testEmailEvent2"))

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
            [ "testEmailEvent"
            , "testEmailEvent2"
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
    return TestUtils.getTestSuite(TestEmailAction, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestEmailAction.log", getTestSuite, sys.argv)

