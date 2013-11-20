# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#!/usr/bin/python
#
# $Id: TestWb6Status.py 3182 2009-06-01 16:22:23Z philipp.schuster $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address
#
# It also assumes that the webbrick has been factory reset

import sys
import time
import unittest
import types

sys.path.append("../..")

from TestWbConfig import TestWbConfig

from WebBrickLibs.WbAccess     import GetHTTPData
from WebBrickLibs.Wb6Status    import *

import MiscLib.DomHelpers

testXmlStr = """<?xml version="1.0" encoding="iso-8859-1" ?>
<WebbrickStatus Ver="6.0.1">
    <Error>0</Error>
    <Context>2</Context>
    <LoginState>1</LoginState>
    
    <SN>100</SN>
    <DI>4095</DI>
    <DO>0</DO>
    <Clock>
        <Date>2006/8/23</Date> 
        <Time>12:5:45</Time>
        <Day>5</Day>
    </Clock>
    
    <OWBus>1</OWBus>
    <Tmps>
        <Tmp id="1" lo="-450" hi="800">340</Tmp>
        <Tmp id="2" lo="-800" hi="1600">347</Tmp>
        <Tmp id="3" lo="-800" hi="1600">0</Tmp>
        <Tmp id="4" lo="-800" hi="1600">0</Tmp>
        <Tmp id="5" lo="-800" hi="1600">32767</Tmp>
    </Tmps>
    
    <AOs>
        <AO id="0">25</AO>
        <AO id="1">50</AO>
        <AO id="2">75</AO>
        <AO id="3">100</AO>
    </AOs>
    <AIs>
        <AI id="0" lo="10" hi="90">20</AI>
        <AI id="1" lo="10" hi="90">40</AI>
        <AI id="2" lo="10" hi="90">60</AI>
        <AI id="3" lo="10" hi="90">80</AI>
    </AIs>
</WebbrickStatus>
"""

class TestWb6Status(unittest.TestCase):

    _wbAddress = TestWbConfig.WbAddress

    def setUp(self):
        return

    def tearDown(self):
        return

    # Actual tests follow
    def testGetStatusXml(self):

        sts = Wb6StatusXml( testXmlStr )
        self.assertEqual( sts.getLoginState(), 1 )

        for idx in range(5):
            temp = sts.getTemp( idx )
            self.assertEqual( type(temp), types.FloatType )
            self.assertEqual( temp, TestWbConfig.ExpectedTemp[idx] )

        for idx in range(12):
            di = sts.getDigIn( idx )
            self.assertEqual( type(di), types.BooleanType, "Digital In %i" % idx )
            self.assertEqual( di, TestWbConfig.ExpectedDigIn[idx], 
                "Digital In %i" % idx )

        for idx in range(8):
            do = sts.getDigOut( idx )
            self.assertEqual( type(do), types.BooleanType, "Digital Out %i" % idx )
            self.assertEqual( do, False, "Digital Out %i" % idx )

        for idx in range(4):
            mi = sts.getMonitor( idx )
            self.assertEqual( type(mi), types.BooleanType, "Monitor %i" % idx )
            self.assertEqual( mi, TestWbConfig.ExpectedDigIn[idx+8], 
                "Monitor %i" % idx )

        for idx in range(4):
            ao = sts.getAnOut( idx )
            self.assertEqual( type(ao), types.FloatType, "An Out %i" % idx )

        for idx in range(4):
            ai = sts.getAnIn( idx )
            self.assertEqual( type(ai), types.FloatType, "An In %i" % idx )

        st = sts.getDate()
        self.assertEqual( type(st), types.UnicodeType )

        st = sts.getTime()
        self.assertEqual( type(st), types.UnicodeType )

        self.assertEqual( type(sts.getDay()), types.IntType )

        st = sts.getVersion()
        self.assertEqual( type(st), types.UnicodeType )
        self.failUnless( st > "6", "Version check" ) 

        self.assertEqual( sts.getOperationalState(), 2 )
        self.assertEqual( sts.getError(), 0 )
        self.assertEqual( sts.getCmdStatus(), 0 )
        self.assertEqual( sts.getNodeNumber(), 100 )

    # Actual tests follow
    def testGetStatus(self):

        sts = Wb6Status( self._wbAddress )
        self.assertEqual( sts.getLoginState(), 1 )

        for idx in range(5):
            temp = sts.getTemp( idx )
            self.assertEqual( type(temp), types.FloatType )

        for idx in range(12):
            di = sts.getDigIn( idx )
            self.assertEqual( type(di), types.BooleanType, "Digital In %i" % idx )
#            self.assertEqual( di, TestWbConfig.ExpectedDigInV7Hw[idx], 
            self.assertEqual( di, TestWbConfig.ExpectedDigIn[idx], 
                "Digital In %i" % idx )

        for idx in range(8):
            do = sts.getDigOut( idx )
            self.assertEqual( type(do), types.BooleanType, "Digital Out %i" % idx )
            self.assertEqual( do, False, "Digital Out %i" % idx )

        for idx in range(4):
            mi = sts.getMonitor( idx )
            self.assertEqual( type(mi), types.BooleanType, "Monitor %i" % idx )
#            self.assertEqual( mi, TestWbConfig.ExpectedDigInV7Hw[idx+8], 
            self.assertEqual( mi, TestWbConfig.ExpectedDigIn[idx+8], 
                "Monitor %i" % idx )

        for idx in range(4):
            ao = sts.getAnOut( idx )
            self.assertEqual( type(ao), types.FloatType, "An Out %i" % idx )

        for idx in range(4):
            ai = sts.getAnIn( idx )
            self.assertEqual( type(ai), types.FloatType, "An In %i" % idx )

        st = sts.getDate()
        self.assertEqual( type(st), types.UnicodeType )

        st = sts.getTime()
        self.assertEqual( type(st), types.UnicodeType )

        self.assertEqual( type(sts.getDay()), types.IntType )

        st = sts.getVersion()
        self.assertEqual( type(st), types.UnicodeType )
        self.failUnless( st > "6", "Version check" ) 

        self.assertEqual( sts.getOperationalState(), 2 )
        self.assertEqual( sts.getError(), 0 )
        self.assertEqual( sts.getCmdStatus(), 0 )
        self.assertEqual( sts.getNodeNumber(), 0 )

    # Sentinel/placeholder tests

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "Pending test"

# Assemble test suite
from MiscLib import TestUtils
def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"        return suite of unit tests only
            "component"   return suite of component tests
            "integration" return suite of integration tests
            "all"         return suite of unit and component tests
            "pending"     return suite of pending tests
            name          a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testUnits"
            , "testGetStatusXml"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            , "testGetStatus"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestWb6Status, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestWb6Status.log", getTestSuite, sys.argv)

