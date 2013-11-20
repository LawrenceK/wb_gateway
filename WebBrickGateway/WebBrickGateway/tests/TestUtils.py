# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestUtils.py 2609 2008-08-11 20:03:27Z graham.klyne $
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

from WebBrickGateway.Utils import *

class DummyRequest:
    def __init__(self):
        self.headers = dict()

class TestUtils(unittest.TestCase):
    def setUp(self):
        # start from known state
        return

    def tearDown(self):
        return

    # Actual tests follow
    def testGetBrowserId(self):
        pass

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
#    suite.addTest(TestUtils("testGetBrowserId"))
    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestUtils( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
