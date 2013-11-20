# $Id: TestClientProfiles.py 3193 2009-06-09 15:47:44Z philipp.schuster $
#
# Unit testing for WebBrick panel definition HTML conversions.
#

import sys
import time
import unittest
import logging
import os
from shutil import copyfile

# Extend python path to access other related modules
# sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../../WebBrickLibs")

from MiscLib.DomHelpers import *

import WebBrickGateway.ClientProfiles

BROWSER_PFOFILES = "./resources/browser.profiles.xml"

class DummyRequest:
    def __init__(self):
        self.headers = dict()
        self.params = dict()

class TestClientProfiles(unittest.TestCase):
    def setUp(self):
        # start from known state
        copyfile( "./resources/browser.profiles.xml.original", BROWSER_PFOFILES)
        return

    def tearDown(self):
        return

    def doLoad(self):
        self._profiles = WebBrickGateway.ClientProfiles.ClientProfiles( BROWSER_PFOFILES )
        self._profiles.load()

    # Actual tests follow
    def testGetBrowserId(self):
        self.doLoad()
        k = self._profiles.getBrowserId( "ABrowserNoOneHasHeardOf" )
        self.assertEqual( k, "unknown" )

    def testLoadProfiles(self):
        # testLoadProfiles
        self.doLoad()

    def testClientKey(self):
        # testLoadProfiles
        self.doLoad()

        request = DummyRequest()
        request.headers['User-Agent'] = "firefoxUaString"
        ck = self._profiles.clientKey( request )
        self.assertEqual( ck, "firefox" )

    def testNoProfilefile(self):
        # testLoadProfiles
        self.doLoad()

        request = DummyRequest()
        request.headers['User-Agent'] = "firefoxUaString"
        ck = self._profiles.clientKey( request )
        self.assertEqual( ck, "firefox" )

    def testNoUserAgentString(self):
        # testLoadProfiles
        os.remove("./resources/browser.profiles.xml")
        self.doLoad()

        request = DummyRequest()
        ck = self._profiles.clientKey( request )
        self.assertEqual( ck, "unknown" )

    def testClientKey2(self):
        # testLoadProfiles
        self.doLoad()

        request = DummyRequest()
        request.headers['User-Agent'] = "ABrowserNoOneHasHeardOf"
        ck = self._profiles.clientKey( request )
        self.assertEqual( ck, "unknown" )

    def testSaveProfiles(self):
        # testLoadProfiles
        self.doLoad()

        request = DummyRequest()
        request.headers['User-Agent'] = "msie"
        self._profiles.clientKey( request )
        # now verify file data

    def testMakeStandardResponse1(self):
        # testLoadProfiles
        WebBrickGateway.ClientProfiles.load( BROWSER_PFOFILES )

        request = DummyRequest()
        request.headers['User-Agent'] = "firefoxUaString"
        result = WebBrickGateway.ClientProfiles.makeStandardResponse( request, "welcome" )
        self.assertEqual( result["tg_template"], "WebBrickGateway.templates.welcome" )

    def testMakeStandardResponse2(self):
        # testLoadProfiles
        WebBrickGateway.ClientProfiles.load( BROWSER_PFOFILES )

        request = DummyRequest()
        request.params["val"] = 123
        request.params["name"] = "test"
        request.headers['User-Agent'] = "firefoxUaString"
        result = WebBrickGateway.ClientProfiles.makeStandardResponse( request, "welcome" )
        self.assertEqual( result["tg_template"], "WebBrickGateway.templates.welcome" )
        self.assertEqual( result["val"], 123 )
        self.assertEqual( result["name"], "test" )
        
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
            [ "testGetBrowserId"
            , "testLoadProfiles"
            , "testClientKey" 
            , "testNoUserAgentString"
            , "testClientKey2"
            , "testSaveProfiles"
            , "testNoProfilefile"
            , "testMakeStandardResponse1"
            , "testMakeStandardResponse2"
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
    return TestUtils.getTestSuite(TestClientProfiles, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestClientProfiles.log", getTestSuite, sys.argv)
