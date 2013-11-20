# $Id: TestAll.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (Functions.py)
# See http://pyunit.sourceforge.net/pyunit.html
#

import sys, unittest, logging

# Add main library directory to python path
# So CI tests run, without WebBRickLibs being an installed egg. (or setup.py develop)
sys.path.append("../..")

from MiscLib import TestUtils

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
import TestScheduleProcessor
import TestHVAC

import TestAsterisk
import TestRgbLedLighting
import TestPersistFile


# Code to run unit tests from all library test modules
def getTestSuite(select="unit"):
    suite = unittest.TestSuite()
    suite.addTest(TestBaseHandler.getTestSuite(select=select))
    suite.addTest(TestEventMapper.getTestSuite(select=select))
    suite.addTest(TestEventRouterLoad.getTestSuite(select=select))
    suite.addTest(TestLogEvents.getTestSuite(select=select))
    suite.addTest(TestCompound.getTestSuite(select=select))
    suite.addTest(TestEmailAction.getTestSuite(select=select))
    suite.addTest(TestHttpAction.getTestSuite(select=select))
    suite.addTest(TestShellAction.getTestSuite(select=select))
    suite.addTest(TestTimeEventGenerator.getTestSuite(select=select))
    suite.addTest(TestWebbrickUdpEventReceiver.getTestSuite(select=select))
    suite.addTest(TestDelayedEvent.getTestSuite(select=select))
    suite.addTest(TestEggNunciate.getTestSuite(select=select))
    suite.addTest(TestValueConvert.getTestSuite(select=select))
#    suite.addTest(TestBackup.getTestSuite(select=select))
    suite.addTest(TestWebbrickMonitor.getTestSuite(select=select))
    suite.addTest(TestWebbrickStatusQuery.getTestSuite(select=select))
    suite.addTest(TestScheduleProcessor.getTestSuite(select=select))
    suite.addTest(TestHVAC.getTestSuite(select=select))

# work in prgress
    suite.addTest(TestPersistFile.getTestSuite(select=select))

# need external stuff
#    suite.addTest(TestAsterisk.getTestSuite())
#    suite.addTest(TestRgbLedLighting.getTestSuite())
#    suite.addTest(TestX10.getTestSuite())
    return suite

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestAll.log", getTestSuite, sys.argv)
    