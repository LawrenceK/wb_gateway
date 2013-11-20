# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestAllWebBrick.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions
# See http://pyunit.sourceforge.net/pyunit.html
#

import unittest,sys
from MiscLib import TestUtils

import TestWb6Config
import TestWb6Status
import TestWb6Commands
import TestWbUdpCommands
import TestWbAccess

# Added:
#import TestWbDiscover

# Code to run unit tests from all library test modules
def getTestSuite(select="unit"):
    suite = unittest.TestSuite()
    suite.addTest(TestWb6Commands.getTestSuite(select=select))
    suite.addTest(TestWbUdpCommands.getTestSuite(select=select))
    suite.addTest(TestWbAccess.getTestSuite(select=select))
    suite.addTest(TestWb6Status.getTestSuite(select=select))
    suite.addTest(TestWb6Config.getTestSuite(select=select))
#    suite.addTest(TestWbDiscover.getTestSuite(select=select))

    return suite

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestAllWebBrick.log", getTestSuite, sys.argv)
