# $Id: TestX10.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, logging, time
import unittest
from StringIO import StringIO

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger
from DummyRouter import DummyRouter

import Events
from Utils import *

from EventHandlers.X10 import X10Handler

_log = logging.getLogger( "TestX10" )

testConfigX10 = """<?xml version="1.0" encoding="utf-8"?>
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

    <eventInterface module='EventHandlers.X10' name='X10Handler' serialPort='com9'>
        <eventtype type="">
            <eventsource source="time/second" >
                <event>
                    <params>
                        <testEq name="second" value="0"/>
                    </params>
                    <channelOn house="A" device="1"/>
                </event>
                <event>
                    <params>
                        <testEq name="second" value="30"/>
                    </params>
                    <channelOff house="A" device="1"/>
                </event>
                <event>
                    <params>
                        <testEq name="second" value="15"/>
                    </params>
                    <channelDim house="A" device="2" level="22" up="yes"/>
                </event>
                <event>
                    <params>
                        <testEq name="second" value="45"/>
                    </params>
                    <channelDim house="A" device="2" level="22"/>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

testConfigX10On = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventHandlers.X10' name='X10Handler' serialPort='com9'>
        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <channelOn house="A" device="1"/>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
"""

testConfigX10Off = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventHandlers.X10' name='X10Handler' serialPort='com9'>
        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <channelOff house="A" device="1"/>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
"""

testConfigX10Dim = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventHandlers.X10' name='X10Handler' serialPort='com9'>
        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <channelDim house="A" device="1" level="22"/>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
"""

class TestX10(unittest.TestCase):

    def setUp(self):
        self._outfile = StringIO()
        self._infile = StringIO()

        self.router = None
        self.loader = None

        return

    def tearDown(self):
        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
            time.sleep(2)
        self.router = None

        _log.debug( "tearDown" )
        return

    def testChannelDim(self):
        _log.debug( "\ntestChannelDim" )

        # 3 bytes address 3 bytes function
        sentChars = "\x04\x66\x00\xB6\x64\x00"
        rxChars = "\x6A\x55\x1A\x55"
        self._infile = StringIO( rxChars )
        self.x10 = X10Handler( "TestX10", DummyRouter(), self._outfile, self._infile )
        cfg = getDictFromXml(parseXmlString(testConfigX10Dim) )
        self.x10.configure( cfg['eventInterface'])
        self.x10.start()

        self.x10.handleEvent( Events.evtMinute1 )  # send channel command
        time.sleep( 1.0 )

        sent = self._outfile.getvalue()
        _log.debug( "sent %s - %s" % (sent, sentChars) )
        # verify.
        self.assertEqual( sent, sentChars )

        self.x10.stop()

    def testChannelOn(self):
        _log.debug( "\ntestChannelOn" )

        # 3 bytes address 3 bytes function
        sentChars = "\x04\x66\x00\x06\x62\x00"
        rxChars = "\x6A\x55\x68\x55"
        self._infile = StringIO( rxChars )
        self.x10 = X10Handler( "TestX10", DummyRouter(), self._outfile, self._infile )
        cfg = getDictFromXml(parseXmlString(testConfigX10On) )
        self.x10.configure( cfg['eventInterface'])
        self.x10.start()

        self.x10.handleEvent( Events.evtMinute1 )  # send channel command
        time.sleep( 1.0 )

        sent = self._outfile.getvalue()
        _log.debug( "sent %s - %s" % (sent, sentChars) )
        # verify.
        self.assertEqual( sent, sentChars )

        self.x10.stop()

    def testPowerFail(self):
        _log.debug( "\ntestPowerFail" )
        # Test popwer fail from CM11

        # 3 bytes address 3 bytes function
        sentChars = "\xfb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        rxChars = "\xa5\x00"
        self._infile = StringIO( rxChars )
        self.x10 = X10Handler( "TestX10", DummyRouter(), self._outfile, self._infile )
        cfg = getDictFromXml(parseXmlString(testConfigX10On) )
        self.x10.configure( cfg['eventInterface'])
        self.x10.start()

        time.sleep( 2.0 )

        self.x10.stop()

    def testPowerFail2(self):
        _log.debug( "\ntestPowerFail2" )
        # Test popwer fail from CP10

        # 3 bytes address 3 bytes function
        sentChars = "\xfb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        rxChars = "\xa6\x00"
        self._infile = StringIO( rxChars )
        self.x10 = X10Handler( "TestX10", DummyRouter(), self._outfile, self._infile )
        cfg = getDictFromXml(parseXmlString(testConfigX10On) )
        self.x10.configure( cfg['eventInterface'])
        self.x10.start()

        time.sleep( 2.0 )

        self.x10.stop()

    def testChannelOff(self):
        _log.debug( "\ntestChannelOff" )

        # 3 bytes address 3 bytes function
        sentChars = "\x04\x66\x00\x06\x63\x00"
        rxChars = "\x6A\x55\x69\x55"
        self._infile = StringIO( rxChars )
        self.x10 = X10Handler( "TestX10", DummyRouter(), self._outfile, self._infile )
        cfg = getDictFromXml(parseXmlString(testConfigX10Off) )
        self.x10.configure( cfg['eventInterface'])
        self.x10.start()

        self.x10.handleEvent( Events.evtMinute1 )  # send channel command
        time.sleep( 1.0 )

        sent = self._outfile.getvalue()
        _log.debug( "sent %s - %s" % (sent, sentChars) )
        # verify.
        self.assertEqual( sent, sentChars )

        self.x10.stop()

    def testChannelReceive(self):
        _log.debug( "\ntestChannelReceive" )

        # 3 bytes address 3 bytes function
        sentChars = "\xc3"
        # address byte, function
        self.router = DummyRouter()
        rxChars = "\x5a\x03\x02\x66\x62"
        self._infile = StringIO( rxChars )
        self.x10 = X10Handler( "TestX10", self.router, self._outfile, self._infile )
        cfg = getDictFromXml(parseXmlString(testConfigX10Off) )
        self.x10.configure( cfg['eventInterface'])
        self.x10.start()
        time.sleep( 1.0 )

        sent = self._outfile.getvalue()
        _log.debug( "sent %s - %s" % (sent, sentChars) )
        # verify.
        self.assertEqual( sent, sentChars )

        self.x10.stop()

        self.assert_( len(self.router._pubs) >= 1)

    def testRealToggle(self):
        _log.debug( "\ntestRealToggle" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigX10) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(2)   # let it start

        self.router.publish( EventAgent("TestX10"), Events.evtSecond0 ) # Switch On
        time.sleep(2)

        self.router.publish( EventAgent("TestX10"), Events.evtSecond30 ) # Switch Off
        time.sleep(2)

        # command a device to switch on.
        # verify command string.
        #self.assert_( len(TestEventLogger._events) >= 1)

    def testRealChannelOn(self):
        _log.debug( "\ntestRealChannelOn" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigX10) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(2)   # let it start

        self.router.publish( EventAgent("TestX10"), Events.evtSecond0 ) # Switch On
        time.sleep(2)

        # command a device to switch on.
        # verify command string.
        #self.assert_( len(TestEventLogger._events) >= 1)

    def testRealChannelDimOn(self):
        _log.debug( "\ntestRealChannelDimOn" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigX10) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(2)   # let it start

        self.router.publish( EventAgent("TestX10"), Events.evtSecond15 ) # Switch On
        time.sleep(10)

        # command a device to switch on.
        # verify command string.
        #self.assert_( len(TestEventLogger._events) >= 1)

    def testRealChannelDimOff(self):
        _log.debug( "\ntestRealChannelDimOff" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigX10) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(2)   # let it start

        self.router.publish( EventAgent("TestX10"), Events.evtSecond45 ) # Switch On
        time.sleep(10)

        # command a device to switch on.
        # verify command string.
        #self.assert_( len(TestEventLogger._events) >= 1)

    def testRealChannelOff(self):
        _log.debug( "\ntestRealChannelOff" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigX10) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(2)   # let it start

        self.router.publish( EventAgent("TestX10"), Events.evtSecond30 ) # Switch Off
        time.sleep(2)

        # command a device to switch on.
        # verify command string.
        #self.assert_( len(TestEventLogger._events) >= 1)

    # Actual tests follow
    def testRealPowerFail(self):
        _log.debug( "\ntestRealPowerFail" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigX10) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(10)   # let it start

        # command a device to switch on.
        # verify command string.
        #self.assert_( len(TestEventLogger._events) >= 1)

    # Actual tests follow
    def testRealChannelReceive(self):
        _log.debug( "\ntestRealChannelReceive" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigX10) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(10)   # let it start

        # command a device to switch on.
        # verify command string.
        self.assert_( len(TestEventLogger._events) >= 1)

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
            [ "testPowerFail"
            , "testPowerFail2"
            , "testChannelOn"
            , "testChannelOff"
            , "testChannelDim"
            , "testChannelReceive"
            ],
        "zzcomponent":
            [ "testComponents"
            ],
        "integration":
            [ "testRealPowerFail"
            , "testRealToggle"
            , "testRealChannelOn"
            , "testRealChannelOff"
            , "testRealChannelDimOn"
            , "testRealChannelDimOff"
            , "testRealChannelReceive"
            ],
        "zzpending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestX10, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestX10.log", getTestSuite, sys.argv)
