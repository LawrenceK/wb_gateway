# $Id: TestWbUdpCommands.py 2809 2008-09-26 16:25:53Z lawrence.klyne $
#
# Integration testing for WebBrick hardware unit
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, time, logging
import unittest

sys.path.append("../..")

from MiscLib import TestUtils

from WebBrickLibs             import WbDefs
from WebBrickLibs.WbUdpCommands import sendUdpCommand
from WebBrickLibs.Wb6Config   import Wb6Config
from WebBrickLibs.Wb6Status   import Wb6Status

from TestWbConfig             import TestWbConfig
from TestWb6Config            import TestWb6Config

def showWorking():
    sys.stdout.write(".")

def showWait():
    sys.stdout.write("w")

# TestWb6Config is based on unittest.TestCase, 
class TestWb6Commands(TestWb6Config):

    _wbAddress  = TestWbConfig.WbAddress
    _wbAddressAndPort  = "%s:26482" %TestWbConfig.WbAddress
    #_udpAddress  = "255.255.255.255"
    _udpAddress  = "255.255.255.255"
    _wbPassword = TestWbConfig.WbFactoryPw

    def verifyCmdStatus( self ):
        sts = Wb6Status( self._wbAddress )
        cmdSts = sts.getCmdStatus()
        if cmdSts == 6: # webbrick started.
            cmdSts = 0
        self.assertEqual( cmdSts, 0 )

    def doLogin(self, wbAddress):
        sendUdpCommand( wbAddress, "LG%s" % (self._wbPassword) )
        # self.wb.Login( "installer" )
        return

    def doReboot(self):
        # takes a while.
        self.doLogin(self._wbAddress)
        sendUdpCommand( self._wbAddress, "RB" )
        time.sleep(5.0)
        return
        
    def setUp(self):
        return

    def tearDown(self):
        return
        
    # Actual tests follow

    def factoryReset(self):
        self.doLogin(self._wbAddress)
        sendUdpCommand( self._wbAddress, "FR1" )
        time.sleep(8.0) # takes a while.
        return

    def testSiteplayerReset(self):
        self.doLogin(self._udpAddress)
        sendUdpCommand( self._udpAddress, "RS" )
        time.sleep(8.0) # takes a while.
        return

    def testLogin(self):
        sendUdpCommand( self._wbAddress, "LG%s" % (self._wbPassword) )
        time.sleep(1.0) # takes a while.
        self.verifyCmdStatus()
        return

    def testDigOut(self):
        sendUdpCommand( self._wbAddress, "DO4T" )
        time.sleep(1.0) # takes a while.
        self.verifyCmdStatus()
        return

    def testBadCommand(self):
        # without login
        sendUdpCommand( self._wbAddress, "LG" )
        sendUdpCommand( self._wbAddress, "NNTest1234" )
        time.sleep(1.0) # takes a while.
        sts = Wb6Status( self._wbAddress )
        cmdSts = sts.getCmdStatus()
        if cmdSts == 6: # webbrick started.
            cmdSts = 0
        self.assertNotEqual( cmdSts, 0 )
        return

    def testNameNode(self):
        self.doLogin(self._wbAddress)
        sendUdpCommand( self._wbAddress, "NNTest1234" )
        self.verifyCmdStatus()
        
        sendUdpCommand( self._wbAddress, "SN1" )
        self.verifyCmdStatus()
        
        time.sleep(1)
        cfg = Wb6Config( self._wbAddress )
        self.assertEqual( cfg.getNodeNumber(), 1 )
        self.assertEqual( cfg.getNodeName(), "Test1234" )

    def testAlternatePort(self):
        # without login
        self.doLogin(self._wbAddressAndPort)
        sendUdpCommand( self._wbAddressAndPort, "NNTest1234" )
        time.sleep(1.0) # takes a while.
        sts = Wb6Status( self._wbAddress )
        cmdSts = sts.getCmdStatus()
        if cmdSts == 6: # webbrick started.
            cmdSts = 0
        self.assertEqual( cmdSts, 0 )
        return

    # Sentinel/placeholder tests

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "Pending test"

# Assemble test suite
#
# Select is:
#   "unit"      return suite of unit tests only
#   "component" return suite of unit and component tests
#   "all"       return suite of unit, component and integration tests
#   name        a single named test to be run
# testargs is a list of argument name/value pairs that are stored into the test class
#
def getTestSuite(select="unit", testargs=[]):
    testdict = {
        "unit": 
            [ "testUnits"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            , "factoryReset"
            , "testDigOut"
            , "testBadCommand"
            , "testLogin"
            , "testNameNode"
            , "testAlternatePort"
            , "testSiteplayerReset"
            , "factoryReset"
            ],
        "pending":
            [ "testPending"
            ]
        }
    for (argname,argval) in testargs:
        if argval: setattr(TestWb6Commands, argname, argval)
    return TestUtils.getTestSuite(TestWb6Commands, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    _wbAddress  = TestWbConfig.WbAddress
    _wbPassword = TestWbConfig.WbFactoryPw
    testargs = [ ("-a", "--address",  "ADR", "_wbAddress",  "IP address of WebBrick") 
               , ("-p", "--password", "PWD", "_wbPassword", "Password to access WebBrick")
               ]
    TestUtils.runTests("TestEvent.log", getTestSuite, sys.argv, testargs)

# End.
