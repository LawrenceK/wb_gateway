# $Id: TestTaskRunner.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html

import threading
import logging
import sys
import string
import time
import unittest

sys.path.append("../..")

from WebBrickLibs.TaskRunner import TaskRunner

from MiscLib.DomHelpers import *

class testTask(threading.Thread):

    def __init__( self ):
        threading.Thread.__init__( self )
        self.setDaemon( True ) # when main thread exits stop server as well
        self._running = False
        self._runtime = 0
        self._value = ""

    def configure( self, xmlDom ):
        """
        called with an XmlDom that contains the configuration for the task
        """
        myDom = getNamedElem( xmlDom, "testTask" )
        if myDom:
            logging.debug( 'testTask configure %s %s' % ( getElemXml(myDom), getAttrText( myDom, 'testValue' ) ) )
            self._value = getAttrText( myDom, 'testValue' )
        pass

    def start( self ):
        logging.debug( 'testTask start' )
        self._running = True
        threading.Thread.start( self )

    def stop( self ):
        logging.debug( 'testTask stop' )
        self._running = False

    def run( self ):
        logging.debug( 'testTask run entry' )
        while self._running:
            time.sleep(0.5)
            self._runtime = self._runtime + 1
            logging.debug( 'testTask run %i' % self._runtime )
        logging.debug( 'testTask run exit' )

class TestTaskRunner(unittest.TestCase):

    def setUp(self):
        self._configure = "<TaskRunner><Task module='WebBrickLibs.tests.TestTaskRunner' name='testTask' ><testTask testValue='value'/></Task></TaskRunner>"
        return

    def tearDown(self):
        return

    # Actual tests follow

    def testTaskRunner(self):
        runner = TaskRunner()
        runner.configure( parseXmlString(self._configure) )
        runner.start()  # all tasks

        task = runner._tasks['testTask'] # hack.

        time.sleep(1)

        self.assertEqual( task._running, True )
        assert( task._runtime > 0, 'task did not run' )
        self.assertEqual( task._value, 'value' )
        runner.stop()

        time.sleep(1)

        self.assertEqual( task._running, False )

    # Sentinel/placeholder tests

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "No pending test"

# Assemble test suite

from MiscLib import TestUtils

def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testUnits"
            , "testTaskRunner"
            # , "testMakeConfig"
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
    return TestUtils.getTestSuite(TestTaskRunner, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestTaskRunner.log", getTestSuite, sys.argv)

