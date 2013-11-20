# $Id: TestITunes.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import os
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
testConfigUPNP = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.ITunes' name='ITunes'>
    </eventInterface>
</eventInterfaces>
"""

# all these events target a specific soundbridge I have Lawrence.
udn = 'ITunes:127.0.0.1'

evt_Stop = Event( 'http://id.webbrick.co.uk/events/av/transport/control', 
                "testITunes", 
            {'udn':udn,
                'action':'stop'} )

evt_Play = Event( 'http://id.webbrick.co.uk/events/av/transport/control', 
                "testITunes", 
            {'udn':udn,
                'action':'play'} )

evt_Pause = Event( 'http://id.webbrick.co.uk/events/av/transport/control', 
                "testITunes", 
            {'udn':udn,
                'action':'pause'} )

evt_Next = Event( 'http://id.webbrick.co.uk/events/av/transport/control', 
                "testITunes", 
            {'udn':udn,
                'action':'next'} )

evt_Prev = Event( 'http://id.webbrick.co.uk/events/av/transport/control', 
                "testITunes", 
            {'udn':udn,
                'action':'prev'} )

evt_Volume0 = Event( 'http://id.webbrick.co.uk/events/av/render/control', 
                "testITunes", 
            {'udn':udn,
                'volume':0} )

evt_Volume50 = Event( 'http://id.webbrick.co.uk/events/av/render/control', 
                "testITunes", 
            {'udn':udn,
                'volume':50} )

evt_Volume100 = Event( 'http://id.webbrick.co.uk/events/av/render/control', 
                "testITunes", 
            {'udn':udn,
                'volume':100} )

class testITunes(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "testITunes" )
        self._log.debug( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        time.sleep(5)

    # Actual tests follow
    def testLoad(self):
        self._log.debug( "\nTestLoad" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(5)

    def testStartStop(self):
        self._log.debug( "\ntestStartStop" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Play )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Next )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Next )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Pause )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Play )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Prev )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Stop )
        time.sleep(5)

    def testVolume(self):
        self._log.debug( "\ntestVolume" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Play )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Volume100 )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Volume50 )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Volume0 )
        time.sleep(5)

        self.router.publish( EventAgent("testITunes"), evt_Volume100 )
        time.sleep(5)

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
        "zzcomponent":
            [ "testDummy"
            ],
        "integration":
            [ "testLoad"
            , "testStartStop"
            , "testVolume"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(testITunes, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("testITunes.log", getTestSuite, sys.argv)
 