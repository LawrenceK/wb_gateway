# $Id: TestAll.py 2609 2008-08-11 20:03:27Z graham.klyne $
#
# Unit testing for WebBrick library functions (Functions.py)
# See http://pyunit.sourceforge.net/pyunit.html
#

import unittest, logging

import TestHeating
import TestLocalState
import TestEventState
#import TestPanelHtml
import TestSendEvent
import TestWebbrick
import test_controllers
import test_model

# Added:
#import TestParameterSet

# Code to run unit tests from all library test modules
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestHeating.getTestSuite())
    suite.addTest(TestLocalState.getTestSuite())
    suite.addTest(TestEventState.getTestSuite())
    #suite.addTest(TestPanelHtml.getTestSuite())
    suite.addTest(TestSendEvent.getTestSuite())
    suite.addTest(TestWebbrick.getTestSuite())
    #suite.addTest(test_controllers.getTestSuite())
    #suite.addTest(test_model.getTestSuite())
    return suite

if __name__ == "__main__":
    # unittest.main()
    # logging.basicConfig(level=logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(getTestSuite())
    