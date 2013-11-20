# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestEventRouterLoad.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, logging, time, os
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent
from EventLib.EventAgent import EventAgent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger
import Utils

import Events

_log = logging.getLogger( "TestEventRouterLoad" )

# Configuration for the tests
testConfigTestEventLogger= """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigDefault = """<?xml version="1.0" encoding="utf-8"?>
<eventRouter type="">
    <eventInterfaces>
        <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
            <eventtype type="">
                <eventsource source="" >
	            <event>
                        <!-- interested in all events -->
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>

        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
                <eventsource source="webbrick/100/DO/0" >
                    <!-- all events from a single source -->
	            <event>
                        <newEvent type="local/url" source="local/BoilerOn" />
                        Test
	            </event>
                </eventsource>
                <eventsource source="webbrick/100/DO/1" >
	            <event>
                        <params>
                            <testEq name="state" value="1" />
                        </params>
                        <newEvent type="local/url" source="local/HwOn">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
</eventRouter>
"""

testConfigThreaded = """<?xml version="1.0" encoding="utf-8"?>
<eventRouter type="EventRouterThreaded">
    <eventInterfaces>
        <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
            <eventtype type="">
                <eventsource source="" >
	            <event>
                        <!-- interested in all events -->
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>

        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
                <eventsource source="webbrick/100/DO/0" >
                    <!-- all events from a single source -->
	            <event>
                        <newEvent type="local/url" source="local/BoilerOn" />
                        Test
	            </event>
                </eventsource>
                <eventsource source="webbrick/100/DO/1" >
	            <event>
                        <params>
                            <testEq name="state" value="1" />
                        </params>
                        <newEvent type="local/url" source="local/HwOn">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
</eventRouter>
"""

testConfigRouter = """<?xml version="1.0" encoding="utf-8"?>
<eventRouter type="EventRouter">
    <eventInterfaces>
        <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
            <eventtype type="">
                <eventsource source="" >
	            <event>
                        <!-- interested in all events -->
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>

        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
                <eventsource source="webbrick/100/DO/0" >
                    <!-- all events from a single source -->
	            <event>
                        <newEvent type="local/url" source="local/BoilerOn" />
                        Test
	            </event>
                </eventsource>
                <eventsource source="webbrick/100/DO/1" >
	            <event>
                        <params>
                            <testEq name="state" value="1" />
                        </params>
                        <newEvent type="local/url" source="local/HwOn">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
</eventRouter>
"""

testConfigPubSub = """<?xml version="1.0" encoding="utf-8"?>
<eventRouter type="EventPubSub">
    <eventInterfaces>
        <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
            <eventtype type="">
                <eventsource source="" >
	            <event>
                        <!-- interested in all events -->
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>

        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
                <eventsource source="webbrick/100/DO/0" >
                    <!-- all events from a single source -->
	            <event>
                        <newEvent type="local/url" source="local/BoilerOn" />
                        Test
	            </event>
                </eventsource>
                <eventsource source="webbrick/100/DO/1" >
	            <event>
                        <params>
                            <testEq name="state" value="1" />
                        </params>
                        <newEvent type="local/url" source="local/HwOn">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
</eventRouter>
"""

testConfigMultiple1 = """<?xml version="1.0" encoding="utf-8"?>
<eventRouter type="EventRouterThreaded">
    <eventInterfaces>
        <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
            <eventtype type="">
                <eventsource source="" >
	            <event>
                        <!-- interested in all events -->
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>

        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
                <eventsource source="webbrick/100/DO/0" >
                    <!-- all events from a single source -->
	            <event>
                        <newEvent type="local/url" source="local/BoilerOn" />
                        Test
	            </event>
                </eventsource>
                <eventsource source="webbrick/100/DO/1" >
	            <event>
                        <params>
                            <testEq name="state" value="1" />
                        </params>
                        <newEvent type="local/url" source="local/HwOn">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
</eventRouter>
"""

testConfigMultiple2 = """<?xml version="1.0" encoding="utf-8"?>
<eventRouter type="EventRouterHTTPS" name="https">
    <eventInterfaces>
        <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
                <eventsource source="webbrick/100/DO/0" >
                    <!-- all events from a single source -->
	            <event>
                        <newEvent type="local/url" source="local/BoilerOn" />
                        Test
	            </event>
                </eventsource>
                <eventsource source="webbrick/100/DO/1" >
	            <event>
                        <params>
                            <testEq name="state" value="1" />
                        </params>
                        <newEvent type="local/url" source="local/HwOn">
                        </newEvent>
	            </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
</eventRouter>
"""

testConfigMultipleRouters = """<?xml version="1.0" encoding="utf-8"?>
<eventRouters>
    <eventRouting>
        <source name="">
            <target name="">
            </target>
        </source>
    </eventRouting>

    <eventRouter type="EventRouterThreaded" name="default">
        <eventInterfaces>
            <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
                <eventtype type="">
                    <eventsource source="" >
	                <event>
                            <!-- interested in all events -->
	                </event>
                    </eventsource>
                </eventtype>
            </eventInterface>

            <eventInterface module='EventHandlers.EventMapper' name='EventMapper'>
                <eventtype type="http://id.webbrick.co.uk/events/webbrick/DO">
                    <eventsource source="webbrick/100/DO/0" >
                        <!-- all events from a single source -->
	                <event>
                            <newEvent type="local/url" source="local/BoilerOn" />
                            Test
	                </event>
                    </eventsource>
                    <eventsource source="webbrick/100/DO/1" >
	                <event>
                            <params>
                                <testEq name="state" value="1" />
                            </params>
                            <newEvent type="local/url" source="local/HwOn">
                            </newEvent>
	                </event>
                    </eventsource>
                </eventtype>
            </eventInterface>
        </eventInterfaces>
    </eventRouter>
</eventRouters>
"""

class TestEventRouterLoad(unittest.TestCase):

    def setUp(self):
        _log.debug( "\n\nsetUp" )
        self._loader = None
        self._router = None
        self.setCwd = False
        if exists("EventHandlers/tests/resources"):
            self.setCwd = True
            os.chdir("EventHandlers/tests")

    def tearDown(self):
        _log.debug( "\n\ntearDown" )

        if self._loader:
            self._loader.stop()
            self._loader = None
        self._router = None
        time.sleep(1)
        if self.setCwd:
            os.chdir("../..")

    # Actual tests follow

    def testTestEventLogger(self):
        """
        Test loading the test event logger
        """
        _log.debug( "\ntestTestEventLogger" )
        self._loader = EventRouterLoader()
        self._loader.loadHandlers( getDictFromXmlString(testConfigTestEventLogger) )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()

        self._router.publish( EventAgent("TestEventRouterLoad"), Events.evtTD0 )
        self._router.publish( EventAgent("TestEventRouterLoad"), Events.evtTD1 )
        
        if len(TestEventLogger._events) < 2 :
            time.sleep(1)   # allow threading to catch up.

        # now look for correct events requests
        TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), 2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/TD/0" )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "webbrick/100/TD/1" )

    def doSimpleTest(self):

        self._router.publish( EventAgent("TestEventRouterLoad"), Events.evtDO_0_off )
        self._router.publish( EventAgent("TestEventRouterLoad"), Events.evtDO_1_off )
        self._router.publish( EventAgent("TestEventRouterLoad"), Events.evtDO_1_on )

        if len(TestEventLogger._events) < 8 :
            time.sleep(1)   # allow threading to catch up.

        # now look for correct events requests
        TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), 5)
        base = 0
#        self.assertEqual( len(TestEventLogger._events), 8)
#        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/subscribe" )
#        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/subscribe" )
#        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/subscribe" )
#        base = 3

        #
        # artifact of simple router is that the event logger may see new events before triggering events.
        #
        # type, source and space for a parameter

        expectedEvents = { 
                    "local/url" : 
                            [
                                ("local/BoilerOn",),
                                ("local/HwOn",),
                            ],
                    "http://id.webbrick.co.uk/events/webbrick/DO" : 
                            [   
                                ("webbrick/100/DO/0",),
                                ("webbrick/100/DO/1",),
                                ("webbrick/100/DO/1",),
                            ],
                     }
        _log.debug( "Received Events %s " % (TestEventLogger._events) )

        haveErr, excessEvents = Utils.verifyEvents( expectedEvents, TestEventLogger._events )

        _log.debug( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testConfigureDefault(self):
        """
        Test loading a single event handler
        """
        _log.debug( "\ntestConfigureDefault" )
        self._loader = EventRouterLoader()
        self._loader.loadHandlers( getDictFromXmlString(testConfigDefault) )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()
        self.doSimpleTest()

    def testConfigureThreaded(self):
        """
        Test loading a single event handler
        """
        _log.debug( "\ntestConfigureThreaded" )
        self._loader = EventRouterLoader()
        self._loader.loadHandlers( getDictFromXmlString(testConfigThreaded) )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()
        self.doSimpleTest()

    def testConfigureRouter(self):
        """
        Test loading a single event handler
        """
        _log.debug( "\ntestConfigureRouter" )
        self._loader = EventRouterLoader()
        self._loader.loadHandlers( getDictFromXmlString(testConfigRouter) )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()
        self.doSimpleTest()

        self._loader.stop()  # all tasks

    def testConfigurePubSub(self):
        """
        Test loading a single event handler
        """
        _log.debug( "\ntestConfigurePubSub" )
        self._loader = EventRouterLoader()
        self._loader.loadHandlers( getDictFromXmlString(testConfigPubSub) )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()
        self.doSimpleTest()

    def testFileConfigure(self):
        _log.debug( "\ntestDirectoryConfigure" )

        self._loader = EventRouterLoader()
        self._loader.loadFromFile( "./resources/testEventRouterLoad/fromFile.xml" )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()

        self.doSimpleTest()

    def testDirectoryConfigure(self):
        _log.debug( "\ntestDirectoryConfigure" )

        self._loader = EventRouterLoader()
        self._loader.loadFromDirectories( "./resources/testEventRouterLoad/fromDirLoad" )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()

        self.doSimpleTest()

    def testDirectoriesConfigure(self):
        _log.debug( "\ntestDirectoryConfigure" )

        self._loader = EventRouterLoader()
        self._loader.loadFromDirectories( "./resources/testEventRouterLoad/fromDirLoad1:./resources/testEventRouterLoad/fromDirLoad2" )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()

        self.doSimpleTest()

    def testConfigureMultiple(self):
        """
        Test loading a single event handler
        """
        _log.debug( "\ntestConfigureMultiple" )
        self._loader = EventRouterLoader()
        self._loader.loadHandlers( getDictFromXmlString(testConfigMultiple1) )
        self._loader.loadHandlers( getDictFromXmlString(testConfigMultiple2) )

        self._loader.start()  # all tasks

        self._router = self._loader.getEventRouter()
        self.doSimpleTest()

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
            [ "testTestEventLogger"
            , "testConfigureDefault"
            , "testConfigurePubSub"
            , "testConfigureRouter"
            , "testConfigureThreaded"
            , "testFileConfigure"
            , "testDirectoryConfigure"
            , "testDirectoriesConfigure"
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
    return TestUtils.getTestSuite(TestEventRouterLoad, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestEventRouterLoad.log", getTestSuite, sys.argv)
