# $Id: TestEventMapper.py 2610 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for Lutron driver (LutronDriver.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, time
import unittest

from MiscLib.DomHelpers  import *
from MiscLib.LutronDriver import *

# Configuration for the tests

#

class TestDrivers(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestDrivers" )
        self._log.debug( "\n\nsetUp" )
        
    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    def EncodeMessage(self):
        lph = LutronProtocolHandler()
        encoded = lph.Encode("Test")
        self._log.debug(encoded)
        assert encoded[0] == 84
        assert encoded[1] == 101
        assert encoded[2] == 115
        assert encoded[3] == 116
        assert encoded[4] == 13
            
    def DecodeMessage(self):
        lph = LutronProtocolHandler()
        messages = lph.Decode("Test\r")
        self._log.debug( messages )
        assert messages[0] == "Test"
    
    def DecodeMultiple(self):
        lph = LutronProtocolHandler()
        messages = lph.Decode("Test\rOne\rTwo\rThree\r")
        self._log.debug( messages )
        assert messages[0] == "Test"
        assert messages[1] == "One"
        assert messages[2] == "Two"
        assert messages[3] == "Three"
        
    def DecodePartial(self):
        lph = LutronProtocolHandler()
        messages = lph.Decode("Test")        
        self._log.debug( messages )
        assert len(messages) == 0
        messages = lph.Decode("\rOne\rTwo\r")
        self._log.debug( messages )
        assert messages[0] == "Test"
        assert messages[1] == "One"
        assert messages[2] == "Two"
    
    def DecodePartials(self):
        lph = LutronProtocolHandler()
        messages = lph.Decode("T")
        assert len(messages) == 0             
        messages = lph.Decode("e")
        assert len(messages) == 0 
        messages = lph.Decode("s")
        assert len(messages) == 0 
        messages = lph.Decode("t")
        assert len(messages) == 0 
        messages = lph.Decode("\r")
        self._log.debug( messages )
        assert messages[0] == "Test"
        
    def DoCommand(self):
        lld = LutronLightDriver('testlight')
        message = lld.DoCommand("togglelight" , {'processor':'01' , 'link':'04' , 'keypad' : '01' , 'light' : '1'})
        self._log.debug( "Unencoded command is :%s" %message )
        assert message == "KBP, [01:04:01], 1"
        
    def DriverIntergration(self):
        lld = LutronLightDriver('testlight')
        message = lld.DoCommand("togglelight" , {'processor':'01' , 'link':'04' , 'keypad' : '01' , 'light' : '1'})
        self._log.debug( "Unencoded command is :%s" %message )
        assert message == "KBP, [01:04:01], 1"
        lph = LutronProtocolHandler()
        message = lph.Encode(message)
        self._log.debug( "Encoded message is : %s" %message )
        assert message == [75,66,80,44,32,91,48,49,58,48,52,58,48,49,93,44,32,49,13]
    
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
            [ "EncodeMessage"
            , "DecodeMessage"
            , "DecodeMultiple"
            , "DecodePartial"
            , "DecodePartials"
            , "DoCommand"
            , "DriverIntergration"
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
    return TestUtils.getTestSuite(TestDrivers, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestDrivers.log", getTestSuite, sys.argv)
