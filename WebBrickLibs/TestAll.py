# $Id: TestAll.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrickLibs
#

import sys, unittest, logging

# Add main library directory to python path
sys.path.append(".")

from MiscLib import TestUtils

import MiscLib.tests.TestAll
import WebBrickLibs.tests.TestAll
import EventLib.tests.TestAll
import EventHandlers.tests.TestAll

# Code to run unit tests from all library test modules
#
# This is not yet complete, anumber iof tests fail when not run from their own directory.
def getTestSuite(select="unit"):
    suite = unittest.TestSuite()
    suite.addTest(MiscLib.tests.TestAll.getTestSuite(select=select))
    suite.addTest(WebBrickLibs.tests.TestAll.getTestSuite(select=select))
    suite.addTest(EventLib.tests.TestAll.getTestSuite(select=select))
    suite.addTest(EventHandlers.tests.TestAll.getTestSuite(select=select))
    return suite

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestAll.log", getTestSuite, sys.argv)

# End.
