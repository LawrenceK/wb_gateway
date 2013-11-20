# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestWebbrickUdpEventReceiver.py 3182 2009-06-01 16:22:23Z philipp.schuster $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys
import string
import time
import unittest
import socket

sys.path.append("../..")

from MiscLib.DomHelpers  import *

from EventLib.Event import Event

from EventHandlers.BaseHandler import *
from EventHandlers.WebbrickUdpEventReceiver import *
from EventHandlers.EventRouterLoad import *

#from DummyRouter import *
import EventHandlers.tests.TestEventLogger as TestEventLogger

allEvents = 0xFFFF  # value for all events seen

testEvents1 = [  
                # low Trigger from analogue
                "\012GTa\001\000\004\100\101\001\000\000",  
                # high Trigger from analogue
                "\012GTA\001\000\004\100\101\001\000\000",  
                # Trigger from remote DI command
                "\012GTd\001\000\004\100\101\001\000\000",  
                # Trigger from local digital input
                "\012GTD\001\000\004\100\101\001\000\000",  
                # low Trigger from temperature
                "\012GTt\001\000\004\100\101\001\000\000",  
                # hi Trigger from temperature
                "\012GTT\001\000\004\100\101\001\000\000",  
                # Trigger from scheduled event
                "\012GTS\001\000\004\100\101\001\000\000",  
                # new input value
                "\012GAI\001\000\004\100\101\001\000\000",  
                # new output value
                "\012GAO\001\000\004\100\101\001\000\000",  
                # new digital output state
                "\012GDO\001\000\004\100\101\001\000\000",  
                # unconfigured node.
                "\012GNN\001\000\004\100\101\001\000\000",  
                # node starting.
                "\012GSS\001\000\004\100\101\001\000\000",  
                # node sending attention
                "\012GAA\001\000\004\100\101\001\000\000",  
                # Current temperature
                "\012GCT\001\000\004\100\101\001\000\000",  
                # RTC clock data
                "\012GRR\001\000\004\100\101\001\000\000",  
                # infra red data
                "\012GIR\001\000\004\100\101\001\000\000"   
    ]


testEvents2 = [  
                # Trigger from local digital input
                # len,u,src,sCh,tCh,act,from,to,sp,valH/L
                "\x0CGTD\x00\x00\x04\x64\x65\x01\x00\x00",  
                "\x0CGTD\x01\x00\x04\x64\x65\x01\x00\x00",  
    ]

testEvents3 = [  
                # test what happens if invalid temp reading is 
                # received
                "\x0CGCT\x01\x00\x04\x64\x65\x01\x2F\xFF", 
                "\x0CGCT\x01\x00\x04\x64\x65\x01\x7F\xFF",  
                  
    ]


nullEvent = [  
                # len,u,src,sCh,tCh,act,from,to,sp,valH/L
                "\x0CZZZ\x00\x00\x00\x00\x00\x01\x00\x00",  
    ]

testConfigUdp = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
            <event>
                    <!-- interested in all events -->
            </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.WebbrickUdpEventReceiver' name='WebbrickUdpEventReceiver'>
    </eventInterface>
</eventInterfaces>
"""

# this is to test the receiver in isolation.
class myDummyRouter(object):
    def __init__(self):
        self._seen = 0

    def trigger( self, event ):
        if event.getPayload().has_key("action"):
            action = event.getPayload()["action"]
            if action == 0:
                return "No Action"
            elif action == 1:
                return "Off"
            elif action == 2:
                return "On"
            elif action == 3:
                return "Momentary"
            elif action == 4:
                return "Toggle"
            elif action == 5:
                return "Dwell " + str(event.dwell())
            elif action == 6:
                return "DwellCan " + str(event.dwell())
            elif action == 7:
                return "Next"
            elif action == 8:
                return "Prev"
            return "Action %i" % action
        return ""

    def allValues( self, event ):
        return "%s %s %s %s" % ( event.getSource(), event.getType(), self.trigger(event), event.getPayload() )

    def publish(self, source, event):
        type = event.getType()[-2:]  # last two chars
        if ( type == "NN" ):
            self._seen = self._seen | 0x01
            logging.debug( 'Unconfigured WebBrick %s' % self.allValues(event) )
        elif ( type == "SS" ):
            self._seen = self._seen | 0x02
            logging.debug( 'WebBrick started %s' % self.allValues(event) )
        elif ( type == "AA" ):
            self._seen = self._seen | 0x04
            logging.debug( 'WebBrick Attention %s' % self.allValues(event) )
        elif ( type == "Ta" ):
            self._seen = self._seen | 0x08
            logging.debug( 'Analogue Under Threshold %s' % self.allValues(event) )
        elif ( type == "TA" ):
            self._seen = self._seen | 0x10
            logging.debug( 'Analogue Over Threshold %s' % self.allValues(event) )
        elif ( type == "Tt" ):
            self._seen = self._seen | 0x20
            logging.debug( 'Temperature Under Threshold %s' % self.allValues(event) )
        elif ( type == "TT" ):
            self._seen = self._seen | 0x40
            logging.debug( 'Temperature Over Threshold %s' % self.allValues(event) )
        elif ( type == "CT" ):
            self._seen = self._seen | 0x80
            logging.debug( 'Temperature %s' % self.allValues(event) )
        elif ( type == "TD" ):
            self._seen = self._seen | 0x100
            logging.debug( 'Digital In %s' % self.allValues(event) )
        elif ( type == "Td" ):
            self._seen = self._seen | 0x200
            logging.debug( 'Remote Digital In %s' % self.allValues(event) )
        elif ( type == "TS" ):
            self._seen = self._seen | 0x400
            logging.debug( 'Scheduled Event %s' % self.allValues(event) )
        elif ( type == "AI" ):
            self._seen = self._seen | 0x800
            logging.debug( 'Analogue In %s' % self.allValues(event) )
        elif ( type == "AO" ):
            self._seen = self._seen | 0x1000
            logging.debug( 'Analogue Out %s' % self.allValues(event) )
        elif ( type == "DO" ):
            self._seen = self._seen | 0x2000
            logging.debug( 'WbDigOut %s' % self.allValues(event) )
        elif ( type == "IR" ):
            self._seen = self._seen | 0x4000
            logging.debug( 'Infra red data %s' % self.allValues(event) )
        elif ( type == "RR" ):
            self._seen = self._seen | 0x8000
            logging.debug( 'RTC Clock data %s' % self.allValues(event) )
        else:
            self._seen = self._seen | 0x80000000
            logging.debug( 'Unknown Event %s' % self.allValues(event) )

class TestWebBrickUdpEventReceiver(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestWebBrickUdpEventReceiver" )
        self._log.debug( "\n\nsetUp" )
        self.loader = None
        self._router = None
        self.udpRx = None
        return

    def tearDown(self):
        self._log.debug( "tearDown" )
        if self.udpRx:
            self.udpRx.stop()
            self.udpRx = None
            time.sleep(3)   # ensure closed down.
        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
            time.sleep(3)   # ensure closed down.

        return

    def _sendUdpEvents(self, events ):
        # open socket
        testSkt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # generate some UDP event packets
        for pkt in events:
            self._log.debug( "send %s", str(pkt) )
            time.sleep(0.1)
            testSkt.sendto( pkt, ("localhost", 2552) )
        time.sleep(1)
        testSkt.close()

    # Actual tests follow
    def testGetEvents(self):
        self._log.debug( "\ntestGetEvents" )
        self._router = myDummyRouter()
        self.udpRx = WebbrickUdpEventReceiver( self._router )
        self.udpRx.start()

        # Not really a unit test as it just waits to log events.

        self._sendUdpEvents( testEvents1 )
        self.assertEqual( self._router._seen, allEvents )

    def testUdpEvent(self):
        self._log.debug( "\ntestUdpEvent" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUdp) )

        self.loader.start()  # all tasks

        self._router = self.loader.getEventRouter()

        self._sendUdpEvents( testEvents2 )
        time.sleep(1)

        TestEventLogger.logEvents()
        #needs updating t handle real webbrick also on network.
        self.assertEqual( len(TestEventLogger._events), 2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/TD/0" )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/webbrick/TD" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "webbrick/100/TD/1" )

    def testUdpTempEvent(self):
        self._log.debug( "\ntestUdpTempEvent" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUdp) )

        self.loader.start()  # all tasks

        self._router = self.loader.getEventRouter()

        self._sendUdpEvents( testEvents3 )
        time.sleep(1)

        TestEventLogger.logEvents()
        #needs updating t handle real webbrick also on network.
        self.assertEqual( len(TestEventLogger._events), 2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/webbrick/CT" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/CT/1" )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/webbrick/ET" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "webbrick/100/ET/1" )        

    def testLotsOfEvents(self):
        self._log.debug( "\n\ntestLotsOfEvents" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigUdp) )

        self.loader.start()  # all tasks

        self._router = self.loader.getEventRouter()

        NumEvents = 4096

        # open socket
        testSkt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # generate some UDP event packets
        pkt = "\012GTa\001\000\004\100\101\001\000\000\000"
        for i in range(NumEvents):
            testSkt.sendto( pkt+chr(i%256), ("localhost", 2552) )
        testSkt.close()

        time.sleep(5)

        self.failUnless( len(TestEventLogger._events) >= NumEvents, "NumEvents %i, received %i" % (NumEvents, len(TestEventLogger._events) ) )

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
            [ "testGetEvents"
            , "testUdpEvent"
            , "testUdpTempEvent"
            , "testLotsOfEvents"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestWebBrickUdpEventReceiver, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestWebBrickUdpEventReceiver.log", getTestSuite, sys.argv)
