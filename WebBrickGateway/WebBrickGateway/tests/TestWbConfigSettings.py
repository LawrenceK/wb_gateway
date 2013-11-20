# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestWbConfigSettings.py 2609 2008-08-11 20:03:27Z graham.klyne $
#
# Unit testing for WebBrick panel definition HTML conversions.
#

import sys, logging
import time
import unittest

from WebBrickLibs.WbConfigBase import WbConfigBase
from WebBrickGateway.WbConfigSettings import WbConfigSettings as WbConfigSettings_hga
from WebBrickConfig.WbConfigSettings import WbConfigSettings as WbConfigSettings_cfg

class TestWbConfigSettings(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestWbConfigSettings" )
        self._log.debug( "\n\nsetUp" )

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    # send a simpel event
    def testCross(self):
        self._log.debug( "\ntestCross" )

        WbConfigBase.ConfDir = "string1"
        WbConfigSettings_hga.ConfDir = "string2"
        WbConfigSettings_cfg.ConfDir = "string3"
        self._log.debug( "WbConfigBase.ConfDir %s " % (WbConfigBase.ConfDir) )
        self._log.debug( "WbConfigSettings_hga.ConfDir %s " % (WbConfigSettings_hga.ConfDir) )
        self._log.debug( "WbConfigSettings_cfg.ConfDir %s " % (WbConfigSettings_cfg.ConfDir) )
        
        # We should see lots of events here as initial pass.
        self.assertEqual( WbConfigSettings_cfg.ConfDir, WbConfigSettings_hga.ConfDir )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestWbConfigSettings("testCross"))
    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestWbConfigSettings( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.INFO)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
