# $Id: TestAll.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (Functions.py)
# See http://pyunit.sourceforge.net/pyunit.html
#

import unittest, logging, sys

sys.path.append("../..")

from MiscLib import TestUtils

import TestWbConfigEdit
import TestParameterSet
import TestAllWebBrick
import TestTaskRunner

# Code to run unit tests from all library test modules
def getTestSuite(select="unit"):
    suite = unittest.TestSuite()
    suite.addTest(TestWbConfigEdit.getTestSuite(select=select))
    suite.addTest(TestParameterSet.getTestSuite(select=select))
    suite.addTest(TestAllWebBrick.getTestSuite(select=select))
    suite.addTest(TestTaskRunner.getTestSuite(select=select))
    return suite

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestAll.log", getTestSuite, sys.argv)

# End.
