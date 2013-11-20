# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestShellAction.py 2911 2008-10-28 20:28:12Z lawrence.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *
from MiscLib.ScanFiles   import readFile

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

TestOutFile = "TestOut/TestShellAction.txt"

# Configuration for the tests
testConfigShell = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.ShellAction' name='ShellAction'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/TD/0" >
                <!-- all events from a single source -->
                <event>
                    <command cmd='cmd.exe' params=' echo response string1> TestOut/TestShellAction.txt' />
                        Test
                </event>
            </eventsource>
            <eventsource source="webbrick/100/TD/1" >
                <event>
                    <command cmd='cmd.exe' params=' echo response string2>> TestOut/TestShellAction.txt' />
                        Test
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

class TestShellAction(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestShellAction" )
        self._log.debug( "\n\nsetUp" )
        ClearDirectory( "TestOut" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

    # Actual tests follow
    def testShellEvent(self):
        self._log.debug( "\n\ntestShellEvent" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigShell) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtTD0 )
        self.router.publish( EventAgent("TestDelayedEvent"), Events.evtTD1 )
        time.sleep(1.0)

        # now look for correct contents in TestShellAction.txt
        try:
            res =  readFile(TestOutFile)
        except Exception, ex:
            self._log.exception(ex)
            res =""
        self.assertEqual( res, "response string1\nresponse string2\n" )
        ClearDirectory( "TestOut" )

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
            [ "testShellEvent"
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
    return TestUtils.getTestSuite(TestShellAction, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestShellAction.log", getTestSuite, sys.argv)
