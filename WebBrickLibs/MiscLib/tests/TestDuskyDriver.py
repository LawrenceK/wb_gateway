# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

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
from MiscLib.DuskyDriver import *

# Configuration for the tests#

class TestSkyDrivers(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestDrivers" )
        self._log.debug( "\n\nsetUp" )
        
    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    def GetCommand(self):
        lph = DuskyDriver("test")
        #test simple encoding
        Command = "setchannel"
        Params = {"val":'232'}
        message = lph.GetCommand(Command,Params)
        assert message == "As01sk232x"
        Params["val"] = '202002020'
        message = lph.GetCommand(Command,Params)
        assert message == ''
        Params["val"] = '1'
        message = lph.GetCommand(Command,Params)
        assert message == ''
        Params["val"] = "999"
        message = lph.GetCommand(Command,Params)
        assert message == "As01sk999x"
        Command = "on"
        Params = "ee22eekl"
        message = lph.GetCommand(Command,Params)
        assert message == "As01skx"
        Command = "off"
        message = lph.GetCommand(Command)
        assert message == "As01skkpx"        
        
    def EncodeMessage(self):
        lld = DuskyProtocolHandler()
        message1 = "12345"
        message2 = "ABCD"
        message3 = "\nE#@"
        
        encoded1 = lld.Encode(message1)
        self._log.debug("Message1 == %s" %encoded1)
        encoded2 = lld.Encode(message2)
        self._log.debug("Message2 == %s" %encoded2)
        encoded3 = lld.Encode(message3)
        self._log.debug("Message3 == %s" %encoded3)       
        assert encoded1 == [49,50,51,52,53]
        assert encoded2 == [65,66,67,68]
        assert encoded3 == [10,69,35,64]
        
        
    
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
            , "GetCommand"
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
    return TestUtils.getTestSuite(TestSkyDrivers, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestSkyDrivers.log", getTestSuite, sys.argv)
