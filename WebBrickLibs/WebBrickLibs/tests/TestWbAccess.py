# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestWbAccess.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys
# import os
import unittest

sys.path.append("../..")

from TestWbConfig import TestWbConfig

from WebBrickLibs.WbAccess import *

from MiscLib.DomHelpers import parseXmlString

class TestWbAccess(unittest.TestCase):

    _wbAddress = TestWbConfig.WbAddress
    _wbNoAddress = TestWbConfig.WbNoAddress

    _homepage = (
        [ '<html>'
        , '<head>'
        , '<script type="text/javascript" src="Values.inc"></script>'
        , '<script type="text/javascript" src="lib.js"></script>'
        , '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">'
        , '<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">'
        , '</head>'
        , '<body>'
        , '<script>'
        , 'ShowPage();'
        , '</script>'
        , '</body>'
        , '</html>'
        ] )

    def setUp(self):
        self.baseUri = "http://"+TestWbAccess._wbAddress+"/"
        return

    def tearDown(self):
        return

    # Actual tests follow

    def testGetHomepage(self):
        def trimcrlf(txt):
            if len(txt) > 0:
                if txt[-1] == '\n': txt = txt[:-1]
            if len(txt) > 0:
                if txt[-1] == '\r': txt = txt[:-1]
            return txt
        data = GetHTTPLines(TestWbAccess._wbAddress,"/")
        assert data, "No homepage data returned: "+TestWbAccess._wbAddress+"/"
        data = map(trimcrlf,data)
        for (l1,l2) in zip(TestWbAccess._homepage,data):
            if l1 != l2:
                print "--difference"
                print l1
                print l2
        assert data == TestWbAccess._homepage, "Wrong homepage data: "+repr(data)

    def testGetStatus(self):
        data = GetHTTPData(TestWbAccess._wbAddress,"/WbStatus.xml")
        assert data, "No page data returned: "+TestWbAccess._wbAddress+"/WbStatus.xml"
        dom  = parseXmlString(data)
        root = dom.documentElement
        assert root.nodeName == "WebbrickStatus", "Wrong root element tag: "+root.nodeName
        assert root.getAttribute("Ver") in TestWbConfig.WbVersions, "Wrong WebBrick version: "+root.getAttribute("Ver")

    def testGetConfig(self):
        data = GetHTTPData(TestWbAccess._wbAddress,"/WbCfg.xml")
        assert data, "No page data returned: "+TestWbAccess._wbAddress+"/WbCfg.xml"
        dom  = parseXmlString(data)
        root = dom.documentElement
        assert root.nodeName == "WebbrickConfig", "Wrong root element tag: "+root.nodeName
        assert root.getAttribute("Ver") in TestWbConfig.WbVersions, "Wrong WebBrick version: "+root.getAttribute("Ver")

    def testCommand(self):
        h = SendHTTPCmd(TestWbAccess._wbAddress,"DO0N")   # Turn on digital O/P 1
        assert h, "Command failed"
        h = SendHTTPCmd(TestWbAccess._wbAddress,"DO0F")   # Turn off digital O/P 1
        assert h, "Command failed"

    def testNoWebbrick(self):
        data = None
        try:
            data = GetHTTPData(TestWbAccess._WbNoAddress,"/WbStatus.xml")
        except Exception,ex :
            print ex

        self.failUnLess( data, None,"No page data returned: "+TestWbAccess._wbNoAddress+"/WbStatus.xml")

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
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            , "testGetHomepage"
            , "testGetStatus"
            , "testGetConfig"
            , "testCommand"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestWbAccess, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestWbAccess.log", getTestSuite, sys.argv)

