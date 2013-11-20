# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestTimeUtils.py 2610 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for TimeUtils module
# See http://pyunit.sourceforge.net/pyunit.html
#

import sys
import unittest

sys.path.append("../..")
from MiscLib.TimeUtils import *

timeStr = "01:02:03"
timeInt = 3600 + 120 + 3

class TestTimeUtils(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    # Test cases

    def testParseTime(self):
        # parse a time in format HH:MM:SS into integer seconds
        val = parseTime( timeStr )
        self.assertEqual( val, timeInt )
        
    def testParseTime2(self):
        # parse a time NOT in the format HH:MM:SS into integer seconds
        val = parseTime( "abc" )
        self.assertEqual( val, 0 )


    def testFormatTime(self):
        # format time as seconds into a string.
        str = formatTime( timeInt )
        self.assertEqual( str, timeStr )

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
             ,"testParseTime"
             ,"testParseTime2"
             ,"testFormatTime"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestTimeUtils, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TesttimeUtils.log", getTestSuite, sys.argv)


# Code to run unit tests directly from command line.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestTimeUtils("testCreateTimeUtils"))
    suite.addTest(TestTimeUtils("testReverseTimeUtils"))
    return suite

# End.
