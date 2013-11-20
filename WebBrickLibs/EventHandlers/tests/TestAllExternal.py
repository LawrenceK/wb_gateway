# $Id: TestAllExternal.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (Functions.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# These tests depend on external hardware being available

import unittest, logging

import TestBaseHandler
import TestEventMapper
import TestEventRouterLoad
import TestLogEvents
import TestCompound
import TestEmailAction
import TestHttpAction
import TestShellAction
import TestTimeEventGenerator
import TestWebbrickUdpEventReceiver
import TestDelayedEvent
import TestEggNunciate
import TestValueConvert
import TestX10
import TestBackup
import TestWebbrickMonitor
import TestWebbrickStatusQuery

import TestAsterisk
import TestRgbLedLighting
import TestPersistFile


# Code to run unit tests from all library test modules
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestWebbrickUdpEventReceiver.getTestSuite())
    suite.addTest(TestBackup.getTestSuite())
    suite.addTest(TestWebbrickMonitor.getTestSuite())
    suite.addTest(TestWebbrickStatusQuery.getTestSuite())

# work in prgress
    suite.addTest(TestPersistFile.getTestSuite())

# need external stuff
    suite.addTest(TestAsterisk.getTestSuite())
    suite.addTest(TestRgbLedLighting.getTestSuite())
    suite.addTest(TestX10.getTestSuite())
    return suite

if __name__ == "__main__":
    # unittest.main()
    logging.basicConfig(level=logging.WARNING)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(getTestSuite())
    