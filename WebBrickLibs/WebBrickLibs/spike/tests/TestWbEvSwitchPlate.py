# $Id: TestWbEvSwitchPlate.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#

import threading
import logging
from logging.handlers import MemoryHandler
import sys
import string
import time
from datetime import datetime
import unittest
from SocketServer import StreamRequestHandler, TCPServer
import socket
import os

sys.path.append("../..")

from WebBrickLibs.WbEvent        import *
from WebBrickLibs.WbAccess       import DoHTTPRequest
from WebBrickLibs.DespatchTask   import *
from WebBrickLibs.WbEvBaseAction import WbEvBaseAction
from WebBrickLibs.WbEvSwitchPlate  import *

from MiscLib.DomHelpers  import *
from MiscLib.ScanFiles   import readFile
from MiscLib.SuperGlobal import SuperGlobal

from TestUtils import *

testConfigWbEvSwitchPlate = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='TestUtils' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='WbEvSwitchPlate' name='WbEvSwitchPlate' serialPort='15'>

        <eventtype type="">
            <eventsource source="time/second" >
                <event>
                    <params>
                        <testEq name="second" value ="1" />
                    </params>
                    <action adr="1" mimic="0" level="8" />
                    <action adr="1" mimic="1" level="48" />
                    <action adr="1" mimic="2" level="8" />
                    <action adr="1" mimic="3" level="0" />
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="2" />
                    </params>
                    <action adr="1" mimic="1" level="8" />
                    <action adr="1" mimic="2" level="48" />
                    <action adr="1" mimic="3" level="8" />
                    <action adr="1" mimic="0" level="0" />
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="3" />
                    </params>
                    <action adr="1" mimic="2" level="8" />
                    <action adr="1" mimic="3" level="48" />
                    <action adr="1" mimic="0" level="8" />
                    <action adr="1" mimic="1" level="0" />
                </event>
                <event>
                    <params>
                        <testEq name="second" value ="4" />
                    </params>
                    <action adr="1" mimic="3" level="8" />
                    <action adr="1" mimic="0" level="48" />
                    <action adr="1" mimic="1" level="8" />
                    <action adr="1" mimic="2" level="0" />
                </event>
            </eventsource>
        </eventtype>

    </eventInterface>
</eventInterfaces>
"""

superglobal1 = SuperGlobal()

class TestWbEvSwitchPlate(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestWbEvSwitchPlate" )
        self._log.debug( "\n\nsetUp" )
        superglobal1.testEventLogData = []  # empty list

        self.runner = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.runner:
            self.runner.stop()  # all tasks
            self.runner = None

        #time.sleep(1)

    def testLoadConfig(self):
        self._log.debug( "\ntestLoadConfig" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvSwitchPlate )
        self.runner.start()  # all tasks

    def testMimics(self):
        self._log.debug( "\ntestMimics" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvSwitchPlate )
        self.runner.start()  # all tasks

        self.runner.sendEvent( evtSecond1 )
        time.sleep(3)
        self.runner.sendEvent( evtSecond2 )
        time.sleep(3)
        self.runner.sendEvent( evtSecond3 )
        time.sleep(3)
        self.runner.sendEvent( evtSecond4 )
        time.sleep(3)

        oldLen = len(superglobal1.testEventLogData)
        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        self.assertEqual( oldLen, 4 )

    def testSwitch(self):
        self._log.debug( "\ntestSwitch" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvSwitchPlate )
        self.runner.start()  # all tasks

        time.sleep(10)

        oldLen = len(superglobal1.testEventLogData)
        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        self.assertEqual( oldLen, 1 )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(TestWbEvSwitchPlate("testLoadConfig"))
    suite.addTest(TestWbEvSwitchPlate("testMimics"))
    suite.addTest(TestWbEvSwitchPlate("testSwitch"))

    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestWbEvSwitchPlate( sys.argv[1] )
    else:
#        logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
