# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestSerialDataConvertor.py 2610 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import Events
from DummyRouter import *

import EventHandlers.tests.TestEventLogger as TestEventLogger
#from EventHandlers.tests.TestEventLogger import *

# Configuration for the tests
# Test events
# Lexicon
evtLexiconVolume0a = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '\xfe\x04\x14\x08 \x00\x00\x07\x06\x07\x00\x04' } )
evtLexiconVolume0b = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 81, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '\x00\x02\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x12\x0f'} )
evtLexiconVolume50a = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 82, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '\xfe\x04\x14\x08 \x32\x00\x07\x06\x07\x00\x04'} )
evtLexiconVolume50b = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 83, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '\x00\x02\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x12\x0f'} )
evtLexiconVolume100a = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 84, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '\xfe\x04\x14\x08 \x64\x00\x07\x06\x07\x00\x04'} )
evtLexiconVolume100b = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 85, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '\x00\x02\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x12\x0f'} )
#evtLexiconVolume0a = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': [254,4,20,8,32,0,0,7,6,0,4] } )
#evtLexiconVolume0b = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 81, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': [0,2,15,15,15,15,15,15,15,18,15]} )
#evtLexiconVolume50a = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 82, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': [254,4,20,8,32,50,0,7,6,0,4]} )
#evtLexiconVolume50b = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 83, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': [0,2,15,15,15,15,15,15,15,18,15]} )
#evtLexiconVolume100a = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 84, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': [254,4,20,8,32,100,0,7,6,0,4]} )
#evtLexiconVolume100b = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 85, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': [0,2,15,15,15,15,15,15,15,18,15]} )

# Onkyo
evtOnkyoVolume0 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '!1MVL00\x1a' } )
evtOnkyoVolume50 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '!1MVL32\x1a' } )
evtOnkyoVolume100 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '!1MVL64\x1a' } )

#DecToAscii
evtDecToAscii = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '75;76;83;44;32;91;48;49;58;48;52;58;48;51;93;44;32;49;49;48;48;48;48;49;48;48;48;48;48;48;48;48;48;48;48;48;48;48;48;48;48:' } )

#8_bit_crc
evt8bitchecksum = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '20;20;84;55;55;50:' } )

#offset out of range
outofrangeoffset = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/1', 'webbrick/1/100', {'seqNr': 80, 'pktType': '1', 'ipAdr': '10.100.100.100', 'fromNode': 100, 'data': '00' } )

testConfigLexicon = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.SerialDataConvertor' name='SerialDataConvertor'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/1">
                <eventsource source="webbrick/1/100" >
                    <!-- all events from a single source -->
                    <event>
                        <!-- These are all matches in the data attribute of the payload -->
                        <match offset='0' value='254'/>
                        <match offset='1' value='4'/>
                        <match offset='2' value='20'/>
                        <newEvent type="avamplifier/volume/current" source="avamplifier/1/volume/main/current">
                            <other_data attr='val' offsetb='5' type="int"/>
                        </newEvent>
                    </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
"""
testConfigOnkyo = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.SerialDataConvertor' name='SerialDataConvertor'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/1">
                <eventsource source="webbrick/1/100" >
                    <!-- all events from a single source -->
                    <event>
                        <!-- These are all matches in the data attribute of the payload -->
                        <!-- !1MVLhh -->
                        <match offset='0' char='!'/>
                        <match offset='1' char='1'/>
                        <match offset='2' char='M'/>
                        <match offset='3' char='V'/>
                        <match offset='4' char='L'/>
                        <newEvent type="avamplifier/volume/current" source="avamplifier/1/volume/main/current">
                            <other_data attr='val' offsetb='5' lenb="2" type="hex_string"/>
                        </newEvent>
                    </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
"""
testDecAscii = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.SerialDataConvertor' name='SerialDataConvertor'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/1">
                <eventsource source="webbrick/1/100" >
                    <!-- all events from a single source -->
                    <event>
                        <!-- These are all matches in the data attribute of the payload -->
                        <match offset='0' char='7'/>
                        <match offset='1' char='5'/>
                        <match offset='3' char='7'/>
                        <match offset='4' char='6'/>
                        <match offset='6' char='8'/>
                        <match offset='7' char='3'/>
                        <newEvent type="avamplifier/volume/current" source="avamplifier/1/volume/main/current">
                            <other_data attr='val' offsetb='51' lenb="72" type="dec_ascii"/>
                        </newEvent>
                    </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
"""
test8bitchecksum = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.SerialDataConvertor' name='SerialDataConvertor'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/1">
                <eventsource source="webbrick/1/100" >
                    <!-- all events from a single source -->
                    <event>
                        <!-- These are all matches in the data attribute of the payload -->
                        <newEvent type="avamplifier/volume/current" source="avamplifier/1/volume/main/current">
                            <other_data attr='val' offsetb='0' type="8_bit_checksum"/>
                        </newEvent>
                    </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
"""
testConfigOutofRange = """<?xml version="1.0" encoding="utf-8"?>
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

        <eventInterface module='EventHandlers.SerialDataConvertor' name='SerialDataConvertor'>
            <eventtype type="http://id.webbrick.co.uk/events/webbrick/1">
                <eventsource source="webbrick/1/100" >
                    <!-- all events from a single source -->
                    <event>
                        <!-- These are all matches in the data attribute of the payload -->
                        <match offset='0' value='0'/>
                        <match offset='1' value='0'/>
                        <match offset='2' value='20'/>
                        <match offset='23' value='20'/>
                        <newEvent type="avamplifier/volume/current" source="avamplifier/1/volume/main/current">
                            <other_data attr='val' offsetb='5' type="int"/>
                        </newEvent>
                    </event>
                </eventsource>
            </eventtype>
        </eventInterface>
    </eventInterfaces>
"""
# Events for the test

class TestSerialDataConvertor(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestSerialDataConvertor" )
        self._log.debug( "\n\nsetUp" )
        self._router = DummyRouter()

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    # Actual tests follow
    def testLexicon(self):
        self._log.debug( "\ntestLexicon" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigLexicon) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testVolume"), evtLexiconVolume0a )

        # time events are not in the log.
        self.assert_(TestEventLogger.expectNevents(2))
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/1/100" )
        evt = TestEventLogger._events[1]
        self.assertEqual( evt.getType(), "avamplifier/volume/current" )
        self.assertEqual( evt.getSource(), "avamplifier/1/volume/main/current" )
        evtod = evt.getPayload()
        self.assert_( evtod.has_key("val") )
        self.assertEqual( evtod["val"], 0 )
        
        self.router.publish( EventAgent("testVolume"), evtLexiconVolume0b )
        self.assert_(TestEventLogger.expectNevents(3))
        
        self.router.publish( EventAgent("testVolume"), evtLexiconVolume50a )
        self.assert_(TestEventLogger.expectNevents(5))
        
        self.router.publish( EventAgent("testVolume"), evtLexiconVolume50b )
        self.assert_(TestEventLogger.expectNevents(6))
        
        self.router.publish( EventAgent("testVolume"), evtLexiconVolume100a )
        self.assert_(TestEventLogger.expectNevents(8))
        
        self.router.publish( EventAgent("testVolume"), evtLexiconVolume100b )
        self.assert_(TestEventLogger.expectNevents(9))
        TestEventLogger.logEvents()
        
    def testOnkyo(self):
        self._log.debug( "\ntestOnkyo" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigOnkyo) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testVolume"), evtOnkyoVolume0 )

        # time events are not in the log.
        self.assert_(TestEventLogger.expectNevents(2))
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/1/100" )
        evt = TestEventLogger._events[1]
        self.assertEqual( evt.getType(), "avamplifier/volume/current" )
        self.assertEqual( evt.getSource(), "avamplifier/1/volume/main/current" )
        evtod = evt.getPayload()
        self.assert_( evtod.has_key("val") )
        self.assertEqual( evtod["val"], 0 )
        
        self.router.publish( EventAgent("testVolume"), evtOnkyoVolume50 )
        self.assert_(TestEventLogger.expectNevents(4))
        
        self.router.publish( EventAgent("testVolume"), evtOnkyoVolume100 )
        self.assert_(TestEventLogger.expectNevents(6))
        
        TestEventLogger.logEvents()
        
    def testDecAscii(self):
        self._log.debug( "\ntestDecAscii" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testDecAscii) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testVolume"), evtDecToAscii )

        # time events are not in the log.
        self.assert_(TestEventLogger.expectNevents(2))
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/1/100" )
        evt = TestEventLogger._events[1]
        self.assertEqual( evt.getType(), "avamplifier/volume/current" )
        self.assertEqual( evt.getSource(), "avamplifier/1/volume/main/current" )
        evtod = evt.getPayload()
        self.assert_( evtod.has_key("val") )
        self.assertEqual( evtod["val"], '110000100000000000000000' )
        
      
        TestEventLogger.logEvents()
        
    def test8BitChecksum(self):
        self._log.debug( "\ntest8BitChecksum" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(test8bitchecksum) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testVolume"), evt8bitchecksum )

        # time events are not in the log.
        self.assert_(TestEventLogger.expectNevents(2))
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/1/100" )
        evt = TestEventLogger._events[1]
        self.assertEqual( evt.getType(), "avamplifier/volume/current" )
        self.assertEqual( evt.getSource(), "avamplifier/1/volume/main/current" )
        evtod = evt.getPayload()
        self.assert_( evtod.has_key("val") )
        self.assertEqual( evtod["val"], '20;20;84;55;55;50;2;227:' )
        
      
        TestEventLogger.logEvents()
        
    def testOutOfRange(self):
        self._log.debug( "\ntestOutOfRange" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigOutofRange) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("testVolume"), outofrangeoffset )
        time.sleep(1)        
        self.assertEqual( len(TestEventLogger._events), 1 )
        TestEventLogger.logEvents()
        #we should get no resulting events and no exceptions
        
    def testUnit(self):
        return

    def testComponent(self):
        return

    def testIntegration(self):
        return

    def testPending(self):
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
            [ "testUnit"
            , "testLexicon"
            , "testOnkyo"
            , "testDecAscii"
            , "test8BitChecksum"
            , "testOutOfRange"
            ],
        "component":
            [ "testComponent"
            ],
        "integration":
            [ "testIntegration"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestSerialDataConvertor, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestSerialDataConvertor.log", getTestSuite, sys.argv)
