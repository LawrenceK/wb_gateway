# $Id: TestHttpAction.py 3499 2010-02-02 08:55:42Z philipp.schuster $
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

# NOTE
# *******
#   This only does a single twisted test as there seems to be an issue stopping and starting twisted
#   during tests.
#
# Configuration for the tests
testConfigHttpAction = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.HttpAction' name='HttpAction' usetwisted='1'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/TD/0" >
                <!-- all events from a single source -->
	        <event>
                    <params>
                    </params>
		    <url cmd="GET" address="localhost:20999" uri="/test?medianame=ITunes&amp;mediacmd=volup" />
                    Test
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigTwisted = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.HttpAction' name='HttpAction' usetwisted='1'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
	        <event>
		    <url cmd="GET" address="localhost:20999" uri="/test?medianame=ITunes&amp;mediacmd=volup" />
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigError = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.HttpAction' name='HttpAction' usetwisted='0'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/TD/0" >
                <!-- all events from a single source -->
	        <event>
                    <params>
                    </params>
		    <url cmd="GET" address="localhost:59999" uri="/test?medianame=ITunes&amp;mediacmd=volup" />
                    Test
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigHttpAction2 = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.HttpAction' name='HttpAction' usetwisted='0'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/DO/0" >
                <!-- all events from a single source -->
	        <event>
		    <url cmd="GET" address="localhost:20999" uri="/test?state=%(state)s" />
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigWebbrickRedirect = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />

    <eventInterface module='EventHandlers.HttpAction' name='HttpAction' usetwisted='0'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/TD/0" >
                <!-- all events from a single source -->
	        <event>
		    <url cmd="GET" address="localhost:20999" uri="/hid.spi?COM=DO0N:" />
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

class TestHttpAction(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestHttpAction" )
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

        time.sleep(5)

    # Actual tests follow
    def testHttpAction(self):
        self._log.debug( "\n\ntestHttpAction" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHttpAction) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off
        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD1 )    # 1 Off

        maxTime = 10
        while (len(self.httpServer.requests()) < 1) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        TestEventLogger.logEvents()

        # now look for correct url requests
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.assertEqual( len(self.httpServer.requests()), 1)
        self.assertEqual( self.httpServer.requests()[0], "/test?medianame=ITunes&mediacmd=volup" )

    def testHttpAction2Requests(self):
        self._log.debug( "\ntestHttpAction2Requests" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHttpAction) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off
        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off

        maxTime = 10
        while (len(self.httpServer.requests()) < 2) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        TestEventLogger.logEvents()

        # now look for correct url requests
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.assertEqual( len(self.httpServer.requests()), 2)
        self.assertEqual( self.httpServer.requests()[0], "/test?medianame=ITunes&mediacmd=volup" )
        self.assertEqual( self.httpServer.requests()[1], "/test?medianame=ITunes&mediacmd=volup" )

    def testHttpAction2RequestsSpaced(self):
        self._log.debug( "\ntestHttpAction2RequestsSpaced" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHttpAction) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off

        maxTime = 10
        while (len(self.httpServer.requests()) < 1) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off
        maxTime = 10
        while (len(self.httpServer.requests()) < 2) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        TestEventLogger.logEvents()

        # now look for correct url requests
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.assertEqual( len(self.httpServer.requests()), 2)
        self.assertEqual( self.httpServer.requests()[0], "/test?medianame=ITunes&mediacmd=volup" )
        self.assertEqual( self.httpServer.requests()[1], "/test?medianame=ITunes&mediacmd=volup" )

    def testTwisted(self):
        self._log.debug( "\ntestTwisted" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigTwisted) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off
        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD1 )    # 1 Off

        maxTime = 10
        while (len(self.httpServer.requests()) < 1) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        TestEventLogger.logEvents()

        # now look for correct url requests
        self._log.debug( "testTwisted %s", self.httpServer.requests() )
        self.assertEqual( len(self.httpServer.requests()), 1)
        self.assertEqual( self.httpServer.requests()[0], "/test?medianame=ITunes&mediacmd=volup" )

    def testHttpError(self):
        # TODO grab error log
        self._log.debug( "\ntestHttpError" )
        '''
            NOTE: This is expected to trow an Error!
        '''
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigError) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off
        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD1 )    # 1 Off

        time.sleep(5)

        TestEventLogger.logEvents()

        # now look for correct url requests, no responses
        self._log.debug( "testHttpAction %s", self.httpServer.requests() )
        self.assertEqual( len(self.httpServer.requests()), 0)

    def testHttpAction2(self):
        self._log.debug( "\n\ntestHttpAction2" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHttpAction2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtDO_0_on )    # 0 Off
        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD1 )    # 1 Off

        maxTime = 10
        while (len(self.httpServer.requests()) < 1) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        TestEventLogger.logEvents()

        # now look for correct url requests
        self._log.debug( "testHttpAction2 %s", self.httpServer.requests() )
        self.assertEqual( len(self.httpServer.requests()), 1)
        self.assertEqual( self.httpServer.requests()[0], "/test?state=1" )

    def testWebbrickRedirect(self):
        self._log.debug( "\ntestWebbrickRedirect" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigWebbrickRedirect) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD0 )    # 0 Off
        self.router.publish( EventAgent("TestHttpAction"), Events.evtTD1 )    # 1 Off

        maxTime = 10
        while (len(self.httpServer.requests()) < 1) and (maxTime > 0):
            maxTime -= 1
            time.sleep(1)

        TestEventLogger.logEvents()

        # now look for correct url requests
        self._log.debug( "testWebbrickRedirect %s", self.httpServer.requests() )
        self.assertEqual( len(self.httpServer.requests()), 1)
        self.assertEqual( self.httpServer.requests()[0], "/hid.spi?COM=DO0N:" )

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
            [ "testHttpAction"
            , "testHttpAction2Requests"
            , "testHttpAction2RequestsSpaced"
            , "testHttpError"
            , "testHttpAction2"
            , "testTwisted"
            , "testWebbrickRedirect"
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
    return TestUtils.getTestSuite(TestHttpAction, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestHttpAction.log", getTestSuite, sys.argv)

