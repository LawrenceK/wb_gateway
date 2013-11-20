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
from MiscLib.NADDriver import *

# Configuration for the tests

#

class TestNADDrivers(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestDrivers" )
        self._log.debug( "\n\nsetUp" )
        
    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    def EncodeMessage(self):
        lph = NADProtocolHandler()
        #test simple encoding
        encoded = lph.Encode((20,20,84,55,55,50))
        self._log.debug(encoded)
        assert encoded[0] == 1
        assert encoded[1] == 20
        assert encoded[2] == 20
        assert encoded[3] == 84
        assert encoded[4] == 55
        assert encoded[5] == 55
        assert encoded[6] == 50
        assert encoded[7] == 2
        assert encoded[8] == 227
        #test control code replacement
        encoded = lph.Encode((3,5,20,94))
        self._log.debug(encoded)
        assert encoded[0] == 1
        assert encoded[1] == 94
        assert encoded[2] == 67
        assert encoded[3] == 94
        assert encoded[4] == 69
        assert encoded[5] == 20
        assert encoded[6] == 94
        assert encoded[7] == 94
        assert encoded[8] == 2
        assert encoded[9] == 133
        #test crc being a control code
        encoded = lph.Encode((21,23,206))
        self._log.debug(encoded)
        assert encoded[0] == 1
        assert encoded[1] == 21
        assert encoded[2] == 23
        assert encoded[3] == 206
        assert encoded[4] == 2
        assert encoded[5] == 94
        assert encoded[6] == 69
                
    def DecodeMessage(self):
        lph = NADProtocolHandler()
        messages = lph.Decode((1,20,20,84,55,55,50,2,227))
        self._log.debug( messages[0] )
        assert messages[0] == [20,20,84,55,55,50]
        messages = lph.Decode((1,21,23,206,2,94,69))
        self._log.debug( messages[0] )
        assert messages[0] == [21,23,206]
        messages = lph.Decode((1,21,23,206))
        assert messages == []
        messages = lph.Decode((2,94,69))
        assert messages[0] == [21,23,206]
       
    def DecodeDirtyMessage(self):
        lph = NADProtocolHandler()
        messages = lph.Decode((1,21,23,206,2,1,21,23,206,1,21,23,206,2,94,69))
        self._log.debug(messages)        
        assert messages[0] == [21,23,206]
        
    def DecodeMultiple(self):
        lph = NADProtocolHandler()
        messages = lph.Decode((1,21,23,206,2,94,69,1,21,23,206,2,94,69))
        self._log.debug( messages )
        assert messages[0] == [21,23,206]
        assert messages[1] == [21,23,206]
        
    def DoCommand(self):
        lld = NADDriver('testDriver')
        message = lld.DoCommand("setvolume" , {'val' : '99'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,23,18)
        message = lld.DoCommand("mute")
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,24,1)
        message = lld.DoCommand("unmute")
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,24,0)
        message = lld.DoCommand("standby" , {'val' : '99'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,21,0)
        message = lld.DoCommand("on" , {'val' : '99'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,21,1)
        message = lld.DoCommand("setsource" , {'source' : 'DVD'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,53,0)
        message = lld.DoCommand("setsource" , {'source' : 'Satellite'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,53,1)
        message = lld.DoCommand("setsource" , {'source' : 'CAB/SAT'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,53,2)
        message = lld.DoCommand("setsource" , {'source' : 'VCR'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,53,3)
        message = lld.DoCommand("setsource" , {'source' : 'Video 4'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,53,4)
        message = lld.DoCommand("setsource" , {'source' : 'Tuner'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,53,5)        
        message = lld.DoCommand("setsource" , {'source' : 'External 5.1'})
        self._log.debug( "Unencoded command is :%s" %str(message) )
        assert message == (21,53,6)
        
        
    
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
            , "DoCommand"
            , "DecodeDirtyMessage"
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
    return TestUtils.getTestSuite(TestNADDrivers, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestNADDrivers.log", getTestSuite, sys.argv)
