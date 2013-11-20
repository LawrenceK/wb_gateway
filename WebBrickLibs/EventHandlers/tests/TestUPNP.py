# $Id: TestUPNP.py 2612 2008-08-11 20:08:49Z graham.klyne $
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

import coherence.extern.louie as louie

from coherence.base import Coherence

from EventHandlers.BaseHandler import *
from EventHandlers.UPNP import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

# Configuration for the tests
testConfigUPNP = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />
    <eventInterface module='EventHandlers.UPNP' name='UPNP'>
        <webserver serverport='0' interface=''/>
    </eventInterface>
</eventInterfaces>
"""

testConfigUPNPDefaults = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.TwistedReactor' name='TwistedReactor' debug="yes" />
    <eventInterface module='EventHandlers.UPNP' name='UPNP'>
    </eventInterface>
</eventInterfaces>
"""

# all these events target a specific soundbridge I have Lawrence.

evt_Stop = Event( 'http://id.webbrick.co.uk/events/media/transport/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'action':'stop'} )

evt_Play = Event( 'http://id.webbrick.co.uk/events/media/transport/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'action':'play'} )

evt_Pause = Event( 'http://id.webbrick.co.uk/events/media/transport/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'action':'pause'} )

evt_Next = Event( 'http://id.webbrick.co.uk/events/media/transport/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'action':'next'} )

evt_Prev = Event( 'http://id.webbrick.co.uk/events/media/transport/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'action':'prev'} )

evt_Volume0 = Event( 'http://id.webbrick.co.uk/events/media/render/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'volume':0} )

evt_Volume50 = Event( 'http://id.webbrick.co.uk/events/media/render/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'volume':50} )

evt_Volume100 = Event( 'http://id.webbrick.co.uk/events/media/render/control', 
                "testUPNP", 
            {'udn':'uuid:526F6B75-536F-756E-6442-000D4B304910',
                'volume':100} )

class TestUPNP(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestUPNP" )
        self._log.info( "\n\nsetUp" )

        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.info( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        time.sleep(5)

    # Actual tests follow
    def testLoad(self):
        self._log.info( "\nTestLoad" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(30)

    def testLoadDefaults(self):
        self._log.info( "\nTestLoadDefaults" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNPDefaults) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(30)

    def testStartStop(self):
        self._log.info( "\ntestStartStop" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Play )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Next )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Next )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Pause )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Play )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Prev )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Stop )
        time.sleep(5)

    def testVolume(self):
        self._log.info( "\ntestVolume" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Play )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Volume100 )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Volume50 )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Volume0 )
        time.sleep(5)

        self.router.publish( EventAgent("TestUPNP"), evt_Volume100 )
        time.sleep(5)

    def logBrowseResult(self, result, client, object_id, starting_index ):
        returned_cnt = result['number_returned']
        total_cnt = result['total_matches']
        update_id = result['update_id']
        self._log.info( "logBrowseResult client - %s %s of %s (%s)", client.device.friendly_name, returned_cnt, total_cnt, update_id )
        # result['items'] is a dictionary
        for key,item in result['items'].iteritems():
            if item['upnp_class'] == 'object.container':
                self._log.info( "container item %s", item )
                # now browse that as well.
                self.do_browse(client, item['id'], 0 )
            else:
                self._log.info( "item %s", item )
            
        #'items': {'S:': {'parent_id': '0', 'child_count': 'None', 'id': 'S:', 'upnp_class': 'object.container', 'title': 'Music Shares'}, 'SQ:': {'parent_id': '0', 'child_count': 'None', 'id': 'SQ:', 'upnp_class': 'object.container', 'title': 'Saved Queues'}, 'Q:': {'parent_id': '0', 'child_count': 'None', 'id': 'Q:', 'upnp_class': 'object.container', 'title': 'Queues'}, 'G:': {'parent_id': '0', 'child_count': 'None', 'id': 'G:', 'upnp_class': 'object.container', 'title': 'Now Playing'}, 'R:': {'parent_id': '0', 'child_count': 'None', 'id': 'R:', 'upnp_class': 'object.container', 'title': 'Oldies'}, 'AI:': {'parent_id': '0', 'child_count': 'None', 'id': 'AI:', 'upnp_class': 'object.container', 'title': 'Audio Inputs'}, 'EN:': {'parent_id': '0', 'child_count': 'None', 'id': 'EN:', 'upnp_class': 'object.container', 'title': 'Entire Network'}, 'A:': {'parent_id': '0', 'child_count': 'None', 'id': 'A:', 'upnp_class': 'object.container', 'title': 'Attributes'}}}

        next_index = int(returned_cnt)+int(starting_index)
        if next_index < total_cnt:
            # continue browse
            self.do_browse(client, object_id, next_index )

    def _failure(self, error):
        self._log.error(error.getTraceback())

    def do_browse(self, client, object_id, starting_index ):
        defered = client.content_directory.browse(object_id,
                #browse_flag='BrowseDirectChildren',
                #filter='*', 
                #sort_criteria='',
                #requested_count=0,
                #process_result=True,
                #backward_compatibility=False,
                starting_index=starting_index
                )

        defered.addCallback( self.logBrowseResult, client=client, object_id=object_id, starting_index=0 ).addErrback(self._failure)

    def mediaserver_detected(self, client, udn ):
        self._log.info( "mediaserver_detected %s %s (%s)", client, client.content_directory, udn )
        self.do_browse(client, 0, 0 )

    def testBrowse(self):
        self._log.info( "\ntestBrowse" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        louie.connect( self.mediaserver_detected, 'Coherence.UPnP.ControlPoint.MediaServer.detected')

        time.sleep(30)
        # I want access to all media servers
#        self._coherence = Coherence()   #already started


    def add_server(self, client, udn ):
        self.directory.addClient(client, udn)

    def dumpDirectory(self, dirs):
        for ntry in dirs.enumItems():
            self._log.info( "item %s", ntry )
            
        for dir in dirs.enumContainers():
            self._log.info( "container %s", dir )
            self.dumpDirectory( dir )

    def testBrowse2(self):
        self._log.info( "\ntestBrowse2" )

        louie.connect( self.add_server, 'Coherence.UPnP.ControlPoint.MediaServer.detected')

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUPNP) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.directory = UPNP_Directory()


        time.sleep(5)
        for clnt in self.directory.getContainers():
            self.dumpDirectory(clnt)

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
            [ "testDummy"
            ],
        "integration":
            [ "testLoad"
            , "testStartStop"
            , "testVolume"
            ],
        "pending":
            [ "testLoadDefaults"
            , "testBrowse"
            ]
        }
    return TestUtils.getTestSuite(TestUPNP, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestUPNP.log", getTestSuite, sys.argv)
 