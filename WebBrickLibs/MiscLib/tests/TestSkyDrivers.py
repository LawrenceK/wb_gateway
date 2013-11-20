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
from MiscLib.SkyDriver import *

# Configuration for the tests#

class TestSkyDrivers(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestDrivers" )
        self._log.debug( "\n\nsetUp" )
        
    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    def GetEvents(self):
        sdriver = SkyDriver('testDriver')
        #test simple encoding
        message1 = 'CE000101--'
        message2 = 'PUCP069Audio Unavailable Please check your digital satellite receiver'
        message3 = "SSCN010101"
        message4 = "SSCA030This is a channel name"
        message5 = "SSDT01210:30"
        message6 = "SST001210:30"
        message7 = "SSN0014" + chr(0x86) + "PgrNm" + chr(0x87)
        message8 = "SSE0012PgrDs"
        msg1evts = sdriver.GetEvents(message1)
        msg2evts = sdriver.GetEvents(message2)
        msg3evts = sdriver.GetEvents(message3)
        msg4evts = sdriver.GetEvents(message4)
        msg5evts = sdriver.GetEvents(message5)
        msg6evts = sdriver.GetEvents(message6)
        msg7evts = sdriver.GetEvents(message7)
        msg8evts = sdriver.GetEvents(message8)
        self._log.debug("msg1evts == %s" %msg1evts)
        assert msg1evts == []
        self._log.debug("msg2evts == %s" %msg2evts)
        assert msg2evts == []
        self._log.debug("msg3evts == %s" %msg3evts)
        assert msg3evts == [{'source': 'Sky/Device/Id/testDriver/ChannelNumber', 'type' : 'Sky/Device/Update', 'payload' : {'val':101}}]
        self._log.debug("msg4evts == %s" %msg4evts)
        assert msg4evts == [{'source': 'Sky/Device/Id/testDriver/ChannelName', 'type' : 'Sky/Device/Update', 'payload' : {'val':'This is a channel name'}}]
        self._log.debug("msg5evts == %s" %msg5evts)
        assert msg5evts == [{'source': 'Sky/Device/Id/testDriver/CurrentTime', 'type' : 'Sky/Device/Update', 'payload' : {'val':'10:30'}}]
        self._log.debug("msg6evts == %s" %msg6evts)
        assert msg6evts == [{'source': 'Sky/Device/Id/testDriver/StartTime', 'type' : 'Sky/Device/Update', 'payload' : {'val':'10:30'}}]
        self._log.debug("msg7evts == %s" %msg7evts)
        assert msg7evts == [{'source': 'Sky/Device/Id/testDriver/ProgramName', 'type' : 'Sky/Device/Update', 'payload' : {'val':'PgrNm'}}]
        self._log.debug("msg8evts == %s" %msg8evts)
        assert msg8evts == [{'source': 'Sky/Device/Id/testDriver/ProgramDescription', 'type' : 'Sky/Device/Update', 'payload' : {'val':'PgrDs'}}]

        
    def DecodeMessage(self):
        lph = SkyProtocolHandler()
        m1 = lph.Decode("\n015CE000101--a4")
        m2 = lph.Decode("\n074PUCP069Audio Unavailable Please check your digital satellite receiverd3")
        self._log.debug("m1 == %s , m2 == %s" %(m1,m2))
        assert m1 == ["CE000101--"]
        assert m2 == ["PUCP069Audio Unavailable Please check your digital satellite receiver"]      
        
    def DecodeDirtyMessage(self):
        lph = SkyProtocolHandler()
        m1 = lph.Decode("\n074PUCP069Audio\n015CE000101-Unavailable Please check your\n074PUCP\n015CE000101--a4069Audio Unavailable\n Please check your digital\n015CE000101--a4 satellite receiverd3 digital satellite receiverd3")
        assert m1 == []
        m1 = lph.Decode('\n015CE000101--a4')
        assert m1 == ['CE000101--']
        
    def DecodeMultiple(self):
        lph = SkyProtocolHandler()
        m1 = lph.Decode('\n015CE000101--a4\n015CE000101--a4\n015CE000101--a4\n015CE000101--a4\n015CE000101--a4\n074PUCP069Audio Unavailable Please check your digital satellite receiverd3')
        self._log.debug("m1 == %s" %m1)
        assert m1 == ['CE000101--','CE000101--','CE000101--','CE000101--','CE000101--',"PUCP069Audio Unavailable Please check your digital satellite receiver"]
             
    
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
            [
              "GetEvents"            
            , "DecodeMessage"
            , "DecodeMultiple"
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
    return TestUtils.getTestSuite(TestSkyDrivers, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestSkyDrivers.log", getTestSuite, sys.argv)
