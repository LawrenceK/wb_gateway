# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# 
#
# Unit testing for hvac roomcontroller class
# See http://pyunit.sourceforge.net/pyunit.html
#

import os
import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *
from EventHandlers.hvac_RC import RoomController

# Configuration for the tests
testConfigClean = """<?xml version="1.0" encoding="utf-8"?>
    <roomcontroller zonekey="1">
        <offsets>
            <offset min="0" max = "10" offset="1"/>
            <offset min="11" max = "15" offset="2"/>
            <offset min="16" max = "20" offset="3"/>
            <offset min="21" max = "25" offset="4"/>
            <offset min="26" max = "30" offset="5"/>
        </offsets>
    </roomcontroller>
"""
testConfigDirty1 = """<?xml version="1.0" encoding="utf-8"?>
    <roomcontroller zonekey="1">
        <offsets>
            <offset min="0" max = "10" offset="1"/>
            <offset min="11" max = "16" offset="2"/>
            <offset min="15" max = "20" offset="3"/>
            <offset min="15" max = "20" offset="4"/>
            <offset min="26" max = "30" offset="5"/>
        </offsets>
    </roomcontroller>
"""
testConfigDirty2 ="""<?xml version="1.0" encoding="utf-8"?>
    <roomcontroller zonekey="1">
        <offsets>
            <offset min="0" max = "10" offset="1"/>
            <offset min="11" max = "15" offset="2"/>
            <offset min="15" max = "20" offset="3"/>
            <offset min="4" max = "5" offset="4"/>
            <offset min="26" max = "30" offset="5"/>
        </offsets>
    </roomcontroller>
"""


class testRoomController(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "testHvac_RC" )
        self._log.debug( "\n\nsetUp" )


    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    # Actual tests follow
    def testCleanConfigure(self):
        self._log.debug( "\nTestClean" )
        cfgDict = getDictFromXmlString(testConfigClean)
        rc = RoomController(cfgDict)
        assert rc.getOffset(5) == "1"
        assert rc.getOffset(11) == "2"
        assert rc.getOffset(15) == "2"
        assert rc.getOffset(16) == "3"
        assert rc.getOffset(26) == "5"
        assert rc.getOffset(29) == "5"
        assert rc.getOffset(30) == "5"
        assert rc.getOffset(31) == None
        
    def testDirtyConfigure1(self):
        self._log.debug( "\nTestDirty1" )
        cfgDict = getDictFromXmlString(testConfigDirty1)
        #print cfgDict
        try:
            rc = RoomController(cfgDict)
        except Exception ,e:
            if str(e) == "Duplicate offset range!":
                pass
            else:
                raise e
                
    def testDirtyConfigure2(self):
        self._log.debug( "\nTestDirty2" )
        cfgDict = getDictFromXmlString(testConfigDirty2)
        #print cfgDict
        try:
            rc = RoomController(cfgDict)
        except Exception ,e:
            if str(e) == "Overlap in ranges, invalid rangemap":
                pass
            else:
                raise e
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
            [ "testCleanConfigure",
            "testDirtyConfigure1",
            "testDirtyConfigure2"
            
            ],
        "zzcomponent":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(testRoomController, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("hvac_roomcontroller_test.log", getTestSuite, sys.argv)
 
