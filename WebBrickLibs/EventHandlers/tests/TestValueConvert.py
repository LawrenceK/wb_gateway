# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestValueConvert.py 3682 2010-08-03 15:11:15Z andy.harris $
#
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
# this test uses the two webbrick UDP triggers to trigger jobs.
# one job directly actions something
# The other job generates an event.
#
testConvertScaleConfig = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="webbrick/100/AI/1" >
                <event>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="local/value">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="webbrick/100/AI/1" >
                <event>
                    <newEvent type="local/value" source="local/Humidity/0" offset="20" multiplier="1.5">
                        <copy_other_data val="newVal"/>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

testConvertScaleConfig2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="webbrick/100/AI/1" >
                <event>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="local/value">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="webbrick/100/AI/1" >
                <event>
                    <newEvent type='local/value' source='local/Humidity/0' preoffset='20' postoffset='20' 
                                multiplier='1.5'>
                        <copy_other_data val="newVal"/>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

testConvertHexIntConfig1 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="testing/converion/hex_to_dec" >
                <event>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="">
            <eventsource source="testing/converion/dec_to_hex" >
                <event>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="local/value">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="testing/converion/hex_to_dec" >
                <event>
                    <newEvent type='local/value' source='testing/converion/hex_to_dec/result' 
                            conversion='hex_to_dec'
                            informat='string'
                            outformat='int'
                            attr='val'
                            >
                            <copy_other_data oldval="val"/>
                    </newEvent>
                </event>
            </eventsource>
            <eventsource source="testing/converion/dec_to_hex" >
                <event>
                    <newEvent type='local/value' source='testing/converion/dec_to_hex/result' 
                            conversion='dec_to_hex'
                            informat='int'
                            outformat='string'
                            attr='val'
                            >
                            <copy_other_data oldval="val"/>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

testConvertHexIntConfig2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="testing/converion/hex_to_dec" >
                <event>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="">
            <eventsource source="testing/converion/dec_to_hex" >
                <event>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="local/value">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="testing/converion/hex_to_dec" >
                <event>
                    <newEvent type='local/value' source='testing/converion/hex_to_dec/result' 
                            conversion='hex_to_dec'
                            informat='string'
                            outformat='int'
                            attr='val'
                            >
                            <copy_other_data oldval="val"/>
                    </newEvent>
                </event>
            </eventsource>
            <eventsource source="testing/converion/dec_to_hex" >
                <event>
                    <newEvent type='local/value' source='testing/converion/dec_to_hex/result' 
                            conversion='dec_to_hex'
                            informat='int'
                            outformat='bytes_dec'
                            attr='val'
                            >
                            <copy_other_data oldval="val"/>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""
testConvertNADDecConfig = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="testing/converion/NAD_to_dec" >
                <event>
                </event>
            </eventsource>
        </eventtype>
         <eventtype type="local/value">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="testing/converion/NAD_to_dec" >
                <event>
                    <newEvent type='local/value' source='testing/converion/NAD_to_dec/result' 
                            conversion='NAD_to_dec'
                            attr='val'
                            >
                            <copy_other_data oldval="val"/>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""
testConvertDecNADConfig = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="testing/converion/dec_to_NAD" >
                <event>
                </event>
            </eventsource>
        </eventtype>
         <eventtype type="local/value">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="testing/converion/dec_to_NAD" >
                <event>
                    <newEvent type='local/value' source='testing/converion/dec_to_NAD/result' 
                            conversion='dec_to_NAD'
                            attr='val'
                            >
                            <copy_other_data oldval="val"/>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConvertDivideConfig = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="webbrick/100/AI/1" >
                <event>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="local/value">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.ValueConvert' name='ValueConvert'>
        <eventtype type="">
            <eventsource source="webbrick/100/AI/1" >
                <event>
                    <newEvent type="local/value" source="local/Humidity/0" offset="0" divisor="10">
                        <copy_other_data val="newVal"/>
                    </newEvent>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""


evtNAD_dec = makeEvent( 'value/NAD_to_dec', 'testing/converion/NAD_to_dec', { 'val':'1;21;23;94;67;2;208:' } )
evtdec_NAD = makeEvent( 'value/dec_to_NAD', 'testing/converion/dec_to_NAD', { 'val':'21;23;3:' } )
class TestValueConvert(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestValueConvert" )
        self._log.debug( "\n\nsetUp" )
        self.runner = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.runner:
            self.runner.stop()  # all tasks
            self.runner = None

    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)

    # Actual tests follow

    def testConvert(self):
        self._log.debug( "\ntestConvert" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertScaleConfig) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtAI_1_50 )    # Analogue In 1 50%, i.e. 2.5V

        self.expectNevents(2)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/AI/1" )
        self.assertEqual( TestEventLogger._events[1].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "local/Humidity/0" )
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"], 45.0 )

    def testDivide(self):
        self._log.debug( "\ntestDivide" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertDivideConfig) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtAI_1_50 )    # Analogue In 1 50%, i.e. 2.5V

        self.expectNevents(2)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/AI/1" )
        self.assertEqual( TestEventLogger._events[1].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "local/Humidity/0" )
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"], 5.0 )

    def testConvert2(self):
        self._log.debug( "\ntestConvert2" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertScaleConfig2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtAI_1_50 )    # Analogue In 1 50%, i.e. 2.5V

        self.expectNevents(2)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/AI/1" )
        self.assertEqual( TestEventLogger._events[1].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "local/Humidity/0" )
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"], 65.0 )

    def testConvertPayloadParams(self):
        self._log.debug( "\ntestConvertPayloadParams" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertScaleConfig2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtAI_1_50_plus_params )    # Analogue In 1 50%, i.e. 2.5V

        self.expectNevents(2)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/AI/1" )
        self.assertEqual( TestEventLogger._events[1].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "local/Humidity/0" )
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"], 90.0 )

    def testConvertPayloadParams2(self):
        self._log.debug( "\ntestConvertPayloadParams" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertScaleConfig2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtAI_1_60_plus_params )    # Analogue In 1 60%, i.e. 3.0V

        self.expectNevents(2)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "webbrick/100/AI/1" )
        self.assertEqual( TestEventLogger._events[1].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "local/Humidity/0" )
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"], 6.0 )

    def testConvertHexToInt(self):
        self._log.debug( "\ntestConvertHexToInt" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertHexIntConfig1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtHEX_0 )  # Hex 0 i.e. dec 0
        self.router.publish( EventAgent("TestValueConvert"), Events.evtHEX_32 ) # Hex 32 i.e. dec 50
        self.router.publish( EventAgent("TestValueConvert"), Events.evtHEX_64 ) # Hex 64 i.e. dec 100

        self.expectNevents(6)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "testing/converion/hex_to_dec" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "testing/converion/hex_to_dec" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "testing/converion/hex_to_dec" )
        
        self.assertEqual( TestEventLogger._events[3].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "testing/converion/hex_to_dec/result" )
        self.assertEqual( TestEventLogger._events[3].getPayload()["val"], 0 )  
        self.assertEqual( TestEventLogger._events[3].getPayload()["oldval"], "0" ) 
    
        self.assertEqual( TestEventLogger._events[4].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "testing/converion/hex_to_dec/result" )
        self.assertEqual( TestEventLogger._events[4].getPayload()["val"], 50 )  
        self.assertEqual( TestEventLogger._events[4].getPayload()["oldval"], "32" ) 
    
        self.assertEqual( TestEventLogger._events[5].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "testing/converion/hex_to_dec/result" )
        self.assertEqual( TestEventLogger._events[5].getPayload()["val"], 100 )  
        self.assertEqual( TestEventLogger._events[5].getPayload()["oldval"], "64" ) 
    
        
    def testConvertIntToHexString(self):
        self._log.debug( "\ntestConvertHexToInt" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertHexIntConfig1) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtINT_0 )    # dec 50, i.e. hex 32
        self.router.publish( EventAgent("TestValueConvert"), Events.evtINT_50 )    # dec 50, i.e. hex 32
        self.router.publish( EventAgent("TestValueConvert"), Events.evtINT_100 )    # dec 50, i.e. hex 32
        
        self.expectNevents(6)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "testing/converion/dec_to_hex" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "testing/converion/dec_to_hex" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "testing/converion/dec_to_hex" )        
        
        self.assertEqual( TestEventLogger._events[3].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "testing/converion/dec_to_hex/result" )
        self.assertEqual( TestEventLogger._events[3].getPayload()["val"], "0x0" )  
        self.assertEqual( TestEventLogger._events[3].getPayload()["oldval"], '0' ) 

        
        self.assertEqual( TestEventLogger._events[4].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "testing/converion/dec_to_hex/result" )
        self.assertEqual( TestEventLogger._events[4].getPayload()["val"], "0x32" )  
        self.assertEqual( TestEventLogger._events[4].getPayload()["oldval"], '50' ) 

        
        self.assertEqual( TestEventLogger._events[5].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "testing/converion/dec_to_hex/result" )
        self.assertEqual( TestEventLogger._events[5].getPayload()["val"], "0x64" )  
        self.assertEqual( TestEventLogger._events[5].getPayload()["oldval"], '100' ) 
        
    def testConvertIntToHexBytes(self):
        self._log.debug( "\ntestConvertHexToInt" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertHexIntConfig2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestValueConvert"), Events.evtINT_0 )    # dec 50, i.e. hex 32
        self.router.publish( EventAgent("TestValueConvert"), Events.evtINT_50 )    # dec 50, i.e. hex 32
        self.router.publish( EventAgent("TestValueConvert"), Events.evtINT_100 )    # dec 50, i.e. hex 32
        
        self.expectNevents(6)
        # first is subscribe event
        self.assertEqual( TestEventLogger._events[0].getSource(), "testing/converion/dec_to_hex" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "testing/converion/dec_to_hex" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "testing/converion/dec_to_hex" )        
        
        self.assertEqual( TestEventLogger._events[3].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "testing/converion/dec_to_hex/result" )
        self.assertEqual( TestEventLogger._events[3].getPayload()["val1"], 48 )
        self.assertEqual( TestEventLogger._events[3].getPayload()["val2"], 48 )
        self.assertEqual( TestEventLogger._events[3].getPayload()["oldval"], '0' ) 

        
        self.assertEqual( TestEventLogger._events[4].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "testing/converion/dec_to_hex/result" )
        self.assertEqual( TestEventLogger._events[4].getPayload()["val1"], 51 ) 
        self.assertEqual( TestEventLogger._events[4].getPayload()["val2"], 50 )        
        self.assertEqual( TestEventLogger._events[4].getPayload()["oldval"], '50' ) 

        
        self.assertEqual( TestEventLogger._events[5].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "testing/converion/dec_to_hex/result" )
        self.assertEqual( TestEventLogger._events[5].getPayload()["val1"], 54 )
        self.assertEqual( TestEventLogger._events[5].getPayload()["val2"], 52 )  
        self.assertEqual( TestEventLogger._events[5].getPayload()["oldval"], '100' )
    
    def testConvertNADtoDec(self):
        self._log.debug( "\ntestConvertNADtoDEC" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertNADDecConfig) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter() 
        self.router.publish( EventAgent("TestValueConvert"), evtNAD_dec )    #1;21;23;94;67;2;208:       
        self.expectNevents(2)
        
        self.assertEqual( TestEventLogger._events[1].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "testing/converion/NAD_to_dec/result" )
        # we expect back a string with all the control characters removed and the checksum removed, this is the payload of what the NAD is sending us
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"],'21;23;3:' )
        self.assertEqual( TestEventLogger._events[1].getPayload()["oldval"],'1;21;23;94;67;2;208:' )
    
    def testConvertdectoNAD(self):
        self._log.debug( "\ntestConvertdectoNAD" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConvertDecNADConfig) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter() 
        self.router.publish( EventAgent("TestValueConvert"), evtdec_NAD )    #21;23;3;2:       
        self.expectNevents(2)
        
        self.assertEqual( TestEventLogger._events[1].getType(), "local/value" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "testing/converion/dec_to_NAD/result" )
        # we expect back a string that has a 8-bit CRC on the end and a control characters correclty ORed
        self.assertEqual( TestEventLogger._events[1].getPayload()["val"],'1;21;23;94;67;2;208:' )
        self.assertEqual( TestEventLogger._events[1].getPayload()["oldval"],'21;23;3:' )    
        
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
            [ "testConvert"
            , "testDivide"
            , "testConvert2"
            , "testConvertPayloadParams"
            , "testConvertPayloadParams2"
            , "testConvertHexToInt"
            , "testConvertIntToHexString"
            , "testConvertIntToHexBytes"
            , "testConvertNADtoDec"
            , "testConvertdectoNAD"
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
    return TestUtils.getTestSuite(TestValueConvert, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestValueConvert.log", getTestSuite, sys.argv)
