# $Id: TestWbDiscover.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions
# See http://pyunit.sourceforge.net/pyunit.html
#

import sys
import os
import unittest

sys.path.append("../..")

from TestWbConfig import TestWbConfig

from WebBrickLibs.WbDiscover import *

class TestWbDiscover(unittest.TestCase):
    def setUp(self):
        self.netmask = TestWbConfig.WbNetMask
        self.wbipadr = TestWbConfig.WbAddress
        return
        #TODO: Now redundant...
        #conf = "default"
        conf = "GK"
        if conf == "GK":
            self.netmask = "193.123.216.64/26"
            self.wbipadr = "193.123.216.121"
        else:
            self.netmask = "10.100.100.100/8"
            self.wbipadr = "10.100.100.100"
        return

    def tearDown(self):
        return

    # Actual tests follow

    def testDiscover(self):
        res = WbDiscover( self.netmask, 10 )
        logging.debug( "%s" % ( res ) )
        self.assertEqual( len(res), 1 )
        wb = res[0]
        self.assertEqual( wb["ipAdr"], self.wbipadr )
        time.sleep(3)   # the udp event receiver can take a few seconds to close th socket.

    def testDiscoverFull(self):
        res = WbDiscoverFull( self.netmask )
        logging.debug( "%s" % ( res ) )
        self.assertEqual( len(res), 1 )
        wb = res[0]
        self.assertEqual( wb["ipAdr"],    self.wbipadr )
        self.assertEqual( wb["nodeNum"],  0 )
        self.assertEqual( wb["nodeName"], "UnNamed" )
        self.assertEqual( wb["attention"], False )
        time.sleep(3)   # the udp event receiver can take a few seconds to close th socket.


# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestWbDiscover("testDiscover"))
    suite.addTest(TestWbDiscover("testDiscoverFull"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(getTestSuite())
    