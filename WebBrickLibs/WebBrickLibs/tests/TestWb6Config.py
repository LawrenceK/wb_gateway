# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestWb6Config.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address
#
# It also assumes that the webbrick has been factory reset

import sys
import time
import unittest
import types
from TestWbConfig import TestWbConfig

sys.path.append("../..")

import WebBrickLibs.WbDefs
from   WebBrickLibs.Wb6Config import *

class TestWb6Config(unittest.TestCase):

    _wbAddress = TestWbConfig.WbAddress

    def getAddressPort(self):
        a = self._wbAddress.split(":",2)+[""]
        return (a[0],a[1])

    def setUp(self):
        return

    def tearDown(self):
        return

    def verifyDiConfiguration(self, idx, cfg):
        di = cfg.getDigInTrigger(idx)
        self.assertEqual( di["name"], "Sw-"+str(idx) )
        if ( idx < 8 ):
            self.assertEqual( di["actionNr"], 4)
            self.assertEqual( di["action"], "Toggle")
            self.assertEqual( di["pairChn"], idx)
            self.assertEqual( di["options"], 2)
        else:
            self.assertEqual( di["actionNr"], 0)
            self.assertEqual( di["action"], "None")
            self.assertEqual( di["pairChn"], 0)
            self.assertEqual( di["options"], 3)
        self.assertEqual( di["dwell"], 0)
        self.assertEqual( di["typeNr"], 0)
        self.assertEqual( di["type"], "Digital")
        self.assertEqual( di["setPoint"], 0)
        self.assertEqual( di["UDPRem"], "None" )
        self.assertEqual( di["UDPRemNr"], 0)
        self.assertEqual( di["RemNode"], 0)

        return
        
    def verifyAiConfiguration(self, idx, cfg):
        ai = cfg.getAnalogueTriggerLow(idx)
        self.assertEqual( ai["name"], "AnIn-"+str(idx) )
        self.assertEqual( ai["threshold"], 0 )
        self.assertEqual( ai["actionNr"], 0 )
        self.assertEqual( ai["action"], "None" )
        self.assertEqual( ai["pairChn"], 0 )
        self.assertEqual( ai["dwell"], 0 )
        self.assertEqual( ai["typeNr"], 0 )
        self.assertEqual( ai["type"], "Digital" )
        self.assertEqual( ai["setPoint"], 0 )
        self.assertEqual( ai["UDPRem"], "None" )
        self.assertEqual( ai["UDPRemNr"], 0 )
        self.assertEqual( ai["RemNode"], 0 )
        
        ai = cfg.getAnalogueTriggerHigh(idx)
        self.assertEqual( ai["name"], "AnIn-"+str(idx) )
        self.assertEqual( ai["threshold"], 100 )
        self.assertEqual( ai["actionNr"], 0 )
        self.assertEqual( ai["action"], "None" )
        self.assertEqual( ai["pairChn"], 0 )
        self.assertEqual( ai["dwell"], 0 )
        self.assertEqual( ai["typeNr"], 0 )
        self.assertEqual( ai["type"], "Digital" )
        self.assertEqual( ai["setPoint"], 0 )
        self.assertEqual( ai["UDPRem"], "None" )
        self.assertEqual( ai["UDPRemNr"], 0 )
        self.assertEqual( ai["RemNode"], 0 )
        return
        
    def verifyTempConfiguration(self, idx, cfg):
        ti = cfg.getTempTriggerLow(idx)
        self.assertEqual( ti["name"], "Temp-"+str(idx) )
        self.assertEqual( ti["threshold"], -50 )
        self.assertEqual( ti["actionNr"], 0 )
        self.assertEqual( ti["action"], "None" )
        self.assertEqual( ti["pairChn"], 0 )
        self.assertEqual( ti["dwell"], 0 )
        self.assertEqual( ti["typeNr"], 0 )
        self.assertEqual( ti["type"], "Digital" )
        self.assertEqual( ti["setPoint"], 0 )
        self.assertEqual( ti["UDPRem"], "None" )
        self.assertEqual( ti["UDPRemNr"], 0 )
        self.assertEqual( ti["RemNode"], 0 )
        
        ti = cfg.getTempTriggerHigh(idx)
        self.assertEqual( ti["name"], "Temp-"+str(idx) )
        self.assertEqual( ti["threshold"], 100 )
        self.assertEqual( ti["actionNr"], 0 )
        self.assertEqual( ti["action"], "None" )
        self.assertEqual( ti["pairChn"], 0 )
        self.assertEqual( ti["dwell"], 0 )
        self.assertEqual( ti["typeNr"], 0 )
        self.assertEqual( ti["type"], "Digital" )
        self.assertEqual( ti["setPoint"], 0 )
        self.assertEqual( ti["UDPRem"], "None" )
        self.assertEqual( ti["UDPRemNr"], 0 )
        self.assertEqual( ti["RemNode"], 0 )
        return

    def verifyScheduleConfiguration(self, idx, cfg):
        sc = cfg.getScheduledEvent(idx)
        self.assertEqual( sc["days"], 0 )
        self.assertEqual( sc["hours"], 0 )
        self.assertEqual( sc["mins"], 0 )
        self.assertEqual( sc["actionNr"], 0 )
        self.assertEqual( sc["action"], "None" )
        self.assertEqual( sc["pairChn"], 0 )
        self.assertEqual( sc["dwell"], 0 )
        self.assertEqual( sc["typeNr"], 0 )
        self.assertEqual( sc["type"], "Digital" )
        self.assertEqual( sc["setPoint"], 0 )
        self.assertEqual( sc["UDPRemNr"], 0 )
        self.assertEqual( sc["UDPRem"], "None" )
        self.assertEqual( sc["RemNode"], 0 )

    def verifySceneConfiguration(self, idx, cfg):
        sc = cfg.getScene(idx)
        self.assertEqual( sc["Digital0"], "Ignore" )
        self.assertEqual( sc["Digital1"], "Ignore" )
        self.assertEqual( sc["Digital2"], "Ignore" )
        self.assertEqual( sc["Digital3"], "Ignore" )
        self.assertEqual( sc["Digital4"], "Ignore" )
        self.assertEqual( sc["Digital5"], "Ignore" )
        self.assertEqual( sc["Digital6"], "Ignore" )
        self.assertEqual( sc["Digital7"], "Ignore" )
        self.assertEqual( sc["Analogue0"], "Ignore" )
        self.assertEqual( sc["Analogue1"], "Ignore" )
        self.assertEqual( sc["Analogue2"], "Ignore" )
        self.assertEqual( sc["Analogue3"], "Ignore" )

    # Actual tests follow
    def verifyVersion(self):
        cfg = Wb6Config( self._wbAddress )
        st = cfg.getVersion()
        self.assertEqual( type(st), types.UnicodeType )
        self.failUnless( st > "6", "Version check" ) 
        return
        
    def verifyName(self):
        cfg = Wb6Config( self._wbAddress )
        name = cfg.getNodeName()
        self.assertEqual( type(name), types.UnicodeType )
        self.assertEqual( name, u"UnNamed" )
        return
        
    def verifyNodeNumber(self):
        cfg = Wb6Config( self._wbAddress )
        nr = cfg.getNodeNumber()
        self.assertEqual( type(nr), types.IntType )
        self.assertEqual( nr, 0 )
        return
        
    def verifyFadeRate(self):
        cfg = Wb6Config( self._wbAddress )
        fr = cfg.getFadeRate()
        self.assertEqual( type(fr), types.IntType )
        self.assertEqual( fr, 8 )
        return
        
    def verifyIp(self):
        cfg = Wb6Config( self._wbAddress )
        ip = cfg.getIpAddress()
        self.assertEqual( type(ip), types.UnicodeType )
        # self.assertEqual( ip, u"10.100.100.100" )
        (a,p) = self.getAddressPort()
        if p == "" or p == "80": self.assertEqual( ip, a )
        return
        
    def verifyMacAddress(self):
        cfg = Wb6Config( self._wbAddress )
        mac = cfg.getMacAddress()
        self.assertEqual( type(mac), types.UnicodeType )
        return

    def verifyRotary(self):
        cfg = Wb6Config( self._wbAddress )
        rot = cfg.getRotary(0)
        self.assertEqual( type(rot), types.IntType )
        self.assertEqual( rot, 64 )

        return
        
    def verifyDwellConfiguration(self):
        cfg = Wb6Config( self._wbAddress )

        dw = cfg.getDwell(0)
        self.assertEqual( type(dw), types.IntType )
        self.assertEqual( dw, 30 )

        dw = cfg.getDwell(1)
        self.assertEqual( type(dw), types.IntType )
        self.assertEqual( dw, 2 )

        dw = cfg.getDwell(2)
        self.assertEqual( type(dw), types.IntType )
        self.assertEqual( dw, 60 )

        dw = cfg.getDwell(3)
        self.assertEqual( type(dw), types.IntType )
        self.assertEqual( dw, 3600 )

#        dw = cfg.getDwell(4)
#        self.assertEqual( type(dw), types.IntType )
#        self.assertEqual( dw, 300 )

#        dw = cfg.getDwell(5)
#        self.assertEqual( type(dw), types.IntType )
#        self.assertEqual( dw, 600 )

#        dw = cfg.getDwell(6)
#        self.assertEqual( type(dw), types.IntType )
#        self.assertEqual( dw, 900 )

#        dw = cfg.getDwell(7)
#        self.assertEqual( type(dw), types.IntType )
#        self.assertEqual( dw, 1200 )

        dw = cfg.getDwellStr(0)
        self.assertEqual( type(dw), types.UnicodeType )
        self.assertEqual( dw, u"30 Secs")

        dw = cfg.getDwellStr(1)
        self.assertEqual( type(dw), types.UnicodeType )
        self.assertEqual( dw, u"2 Secs")

        dw = cfg.getDwellStr(2)
        self.assertEqual( type(dw), types.UnicodeType )
        self.assertEqual( dw, u"60 Secs" )

        dw = cfg.getDwellStr(3)
        self.assertEqual( type(dw), types.UnicodeType )
        self.assertEqual( dw, u"60 Mins" )

#        dw = cfg.getDwellStr(4)
#        self.assertEqual( type(dw), types.UnicodeType )
#        self.assertEqual( dw, u"5 Mins" )

#        dw = cfg.getDwellStr(5)
#        self.assertEqual( type(dw), types.UnicodeType )
#        self.assertEqual( dw, u"10 Mins" )

#        dw = cfg.getDwellStr(6)
#        self.assertEqual( type(dw), types.UnicodeType )
#        self.assertEqual( dw, u"15 Mins" )

#        dw = cfg.getDwellStr(7)
#        self.assertEqual( type(dw), types.UnicodeType )
#        self.assertEqual( dw, u"20 Mins" )

        return
        
    def verifySetPointConfiguration(self):
        cfg = Wb6Config( self._wbAddress )

        sp = cfg.getSetPoint(0)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 0 )

        sp = cfg.getSetPoint(1)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 14 )

        sp = cfg.getSetPoint(2)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 28 )

        sp = cfg.getSetPoint(3)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 42 )

        sp = cfg.getSetPoint(4)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 57 )

        sp = cfg.getSetPoint(5)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 71 )

        sp = cfg.getSetPoint(6)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 85 )

        sp = cfg.getSetPoint(7)
        self.assertEqual( type(sp), types.IntType )
        self.assertEqual( sp, 100 )

        return

    def verifyDoNameConfiguration(self):
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.DOCOUNT ):
            assert cfg.getDigOutName(idx) == "DigOut-"+str(idx), cfg.getDigOutName(idx)
    
    def verifyAoNameConfiguration(self):
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.AOCOUNT ):
            assert cfg.getAnalogueOutName(idx) == "AnOut-"+str(idx), cfg.getAnalogueOutName(idx)
    
    def verifyDigitalIn(self):
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.DICOUNT ):
            self.verifyDiConfiguration(idx, cfg)

    def verifyTemperatures(self):
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.TEMPCOUNT ):
            self.verifyTempConfiguration(idx, cfg)
        
    def verifyAnalogueIn(self):
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.AICOUNT ):
            self.verifyAiConfiguration(idx, cfg)

    def verifySchedules(self):
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.SCHEDCOUNT ):
            self.verifyScheduleConfiguration(idx, cfg)
        
    def verifyScenes(self):
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.SCENECOUNT ):
            self.verifySceneConfiguration(idx, cfg)

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
from MiscLib import TestUtils
def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"        return suite of unit tests only
            "component"   return suite of component tests
            "integration" return suite of integration tests
            "all"         return suite of unit and component tests
            "pending"     return suite of pending tests
            name          a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testUnits"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            , "verifyVersion"
            , "verifyName"
            , "verifyNodeNumber"
            , "verifyFadeRate"
            , "verifyIp"
            , "verifyMacAddress"
            , "verifyRotary"
            , "verifyDwellConfiguration"
            , "verifySetPointConfiguration"
            , "verifyDoNameConfiguration"
            , "verifyAoNameConfiguration"
            , "verifyDigitalIn"
            , "verifyTemperatures"
            , "verifyAnalogueIn"
            , "verifySchedules"
            , "verifyScenes"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestWb6Config, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestWb6Config.log", getTestSuite, sys.argv)

