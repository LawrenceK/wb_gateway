# $Id: TestWbConfigEdit.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick configuration data edit class
# See http://pyunit.sourceforge.net/pyunit.html
#

import sys,os
from os.path import exists
import unittest

sys.path.append("../..")

from WebBrickLibs.WbConfigData import WbConfigData 
from WebBrickLibs.WbConfigEdit import WbConfigEdit
from WebBrickLibs.Wb6Config    import Wb6Config

from MiscLib.Functions         import compareDicts

class TestWbConfigEdit(unittest.TestCase):

    def setUp(self):
        # Initialize configuration object 'self.wbconf' from XML data    
        self.setCwd = False
        if exists("WebBrickLibs/tests/resources"):
            # so tests run from WebBrcikLibs root
            self.setCwd = True
            os.chdir("WebBrickLibs/tests")
            
        self.respath  = "resources/"
        xmlpath  = self.respath+"WbConfigData.xml"
        f = open(xmlpath, mode="r")
        cnfxml = f.read()
        f.close()
        self.wbconf = Wb6Config(cnfxml=cnfxml)
        return

    def tearDown(self):
        if self.setCwd:
            os.chdir("../..")
        return

    # Test cases
    def testEq(self, label, actual, expect):
        assert actual==expect, "Mismatch %s: \n'%s' where \n'%s' expected" % (label, actual, expect)

    def testEqDict(self, label, actual, expect):
        d = compareDicts(actual, expect)
        assert d==None, "Dictionary mismatch: %s\n %s seen,\n %s expected" % ((label,)+d)

    # Test selected configuration against original
    def testSomeConfig(self, testconfig):
        self.testEq("getVersion",               testconfig.getVersion(),                "6.0.252")
        self.testEq("getNodeName",              testconfig.getNodeName(),               "Build2")
        self.testEq("getNodeNumber",            testconfig.getNodeNumber(),             23)
        self.testEq("getNodeNumberStr",         testconfig.getNodeNumberStr(),          "23")
        self.testEq("getFadeRate",              testconfig.getFadeRate(),               4)
        self.testEq("getIpAddress",             testconfig.getIpAddress(),              None)
        self.testEq("getMacAddress",            testconfig.getMacAddress(),             None)
        self.testEq("getIrAddress",             testconfig.getIrAddress(),              29)
        self.testEq("getIrTransmit",            testconfig.getIrTransmit(),             False)
        self.testEq("getIrReceive",             testconfig.getIrReceive(),              True)
        self.testEq("getRotary",                testconfig.getRotary(0),                8)
        self.testEq("getMimicLoLevel",          testconfig.getMimicLoLevel(),           4)
        self.testEq("getMimicHiLevel",          testconfig.getMimicHiLevel(),           63)
        self.testEq("getMimicFadeRate",         testconfig.getMimicFadeRate(),          2)
        self.testEq("getMimicForDigital",       testconfig.getDigOutMimic(5),           5)
        self.testEq("getMimicForAnalog",        testconfig.getAnalogOutMimic(2),        2)
        self.testEq("getMimicForDigital",       testconfig.getDigOutMimic(7),           -1)
        self.testEq("getMimicForAnalog",        testconfig.getAnalogOutMimic(3),        -1)
        self.testEq("getDwell",                 testconfig.getDwell(1),                 5)
        self.testEq("getDwellStr",              testconfig.getDwellStr(2),              "60 Secs")
        self.testEq("getSetPoint",              testconfig.getSetPoint(3),              35)
        self.testEq("getDigOutName",            testconfig.getDigOutName(4),            "Out4")
        self.testEq("getAnalogueOutName",       testconfig.getAnalogueOutName(3),       "An-4")
        self.testEq("getDigInName",             testconfig.getDigInName(5),             "Pb-5")
        d = { 'name': u'AnOn'
            , 'options': 2 
            , 'actionNr': 2
            , 'action': 'On'
            , 'typeNr': 2
            , 'type': 'Analogue' 
            , 'UDPRemNr': 0
            , 'UDPRem' : 'None'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 5
            , 'pairChn': 0
            }
        self.testEq("getDigInTrigger",          testconfig.getDigInTrigger(6),          d)
        self.testEq("getTempInName",            testconfig.getTempInName(0),            "Temp-1")
        d = { 'name': u'Temp-1'
            , 'threshold': -50.0
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        self.testEq("getTempTriggerLow",        testconfig.getTempTriggerLow(0),        d)
        d = { 'name': u'Temp-1'
            , 'threshold': 100.0
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        self.testEq("getTempTriggerHigh",       testconfig.getTempTriggerHigh(0),       d)
        self.testEq("getAnalogInName",          testconfig.getAnalogInName(1),          "An-2")
        d = { 'name': u'An-2'
            , 'threshold': 0
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        self.testEq("getAnalogueTriggerLow",    testconfig.getAnalogueTriggerLow(1),    d)
        d = { 'name': u'An-2'
            , 'threshold': 100
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 0
            , 'UDPRem' : 'None'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        self.testEq("getAnalogueTriggerHigh",   testconfig.getAnalogueTriggerHigh(1),   d)
        d = { 'days': 0
            , 'hours': 2
            , 'mins': 2
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        self.testEq("getScheduledEvent",        testconfig.getScheduledEvent(2),        d)
        d = { "Digital0":  "On"
            , "Digital1":  "Off"
            , "Digital2":  "On"
            , "Digital3":  "Ignore"
            , "Digital4":  "Ignore"
            , "Digital5":  "Ignore"
            , "Digital6":  "Ignore"
            , "Digital7":  "Ignore"
            , "Analogue0": "SetPoint2"
            , "Analogue1": "Ignore"
            , "Analogue2": "SetPoint4"
            , "Analogue3": "SetPoint5"
            }
        self.testEq("getScene",                 testconfig.getScene(1),                 d)
        d = { "Digital":  [True,False,True,None,None,None,None,None]
            , "Analog":   [2,None,4,5]
            }
        self.testEq("getSceneAlt",              testconfig.getSceneAlt(1),              d)
        return

    # Test configuration as loaded from XML file
    def testOrigConfig(self):
        self.testSomeConfig( self.wbconf )

    # Construct new config from original and test again
    def testMakeConfig(self):
        self.testSomeConfig( WbConfigEdit(copyfrom=self.wbconf) )

    # Copy original config and test again
    def testCopyConfig(self):
        newconfig = WbConfigEdit()
        newconfig.setConfig(self.wbconf)
        self.testSomeConfig( newconfig )

    # Construct config using setter methods, and test
    def testSetConfig(self):
        newconfig = WbConfigEdit()
        newconfig.setVersion("6.0.252")
        newconfig.setNodeName("Build2")
        newconfig.setNodeNumber(23)
        newconfig.setFadeRate(4)
        newconfig.setIpAddress(None)
        newconfig.setMacAddress(None)
        newconfig.setIrAddress(29)
        newconfig.setIrTransmit(False)
        newconfig.setIrReceive(True)
        newconfig.setRotary(0, 8)
        newconfig.setMimicLoLevel(4)
        newconfig.setMimicHiLevel(63)
        newconfig.setMimicFadeRate(2)
        newconfig.setDigOutMimic(5, 5)
        newconfig.setAnalogOutMimic(2, 2)
        newconfig.setDigOutMimic(7, -1)
        newconfig.setAnalogOutMimic(3, -1)
        newconfig.setDwell(1, 5)
        newconfig.setDwell(2, 60)
        newconfig.setSetPoint(3, 35)
        newconfig.setDigOutName(4, "Out4")
        newconfig.setAnalogOutName(3, "An-4")
        d = { 'name': u'Pb-5'
            }
        newconfig.setDigInTrigger(5, d)
        d = { 'name': u'AnOn'
            , 'options': 2 
            , 'actionNr': 2
            , 'action': 'On'
            , 'typeNr': 2
            , 'type': 'Analogue' 
            , 'UDPRemNr': 0
            , 'UDPRem' : 'None'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 5
            , 'pairChn': 0
            }
        newconfig.setDigInTrigger(6, d)
        d = { 'name': u'Temp-1'
            , 'threshold': -50.0
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        newconfig.setTempTriggerLow(0, d)
        d = { 'name': u'Temp-1'
            , 'threshold': 100.0
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        newconfig.setTempTriggerHigh(0, d)
        d = { 'name': u'An-2'
            , 'threshold': 0
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        newconfig.setAnalogTriggerLow(1, d)
        d = { 'name': u'An-2'
            , 'threshold': 100
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 0
            , 'UDPRem' : 'None'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        newconfig.setAnalogTriggerHigh(1, d)
        d = { 'days': 0
            , 'hours': 2
            , 'mins': 2
            , 'actionNr': 0
            , 'action': 'None'
            , 'typeNr': 0
            , 'type': 'Digital' 
            , 'UDPRemNr': 3
            , 'UDPRem' : 'Alarm'
            , 'dwell': 0
            , 'RemNode': 0
            , 'setPoint': 0
            , 'pairChn': 0
            }
        newconfig.setScheduledEvent(2, d)
        d = { "Digital0":  "On"
            , "Digital1":  "Off"
            , "Digital2":  "On"
            , "Digital3":  "Ignore"
            , "Digital4":  "Ignore"
            , "Digital5":  "Ignore"
            , "Digital6":  "Ignore"
            , "Digital7":  "Ignore"
            , "Analogue0": "SetPoint2"
            , "Analogue1": "Ignore"
            , "Analogue2": "SetPoint4"
            , "Analogue3": "SetPoint5"
            }
        ### newconfig.setScene(1, d) ### Broken method, should be removed ###
        d = { "Digital":  [True,False,True,None,None,None,None,None]
            , "Analog":   [2,None,4,5]
            }
        newconfig.setSceneAlt(1, d)
        # Now test it
        self.testSomeConfig( newconfig )

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
            , "testOrigConfig"
            , "testMakeConfig"
            , "testCopyConfig"
            , "testSetConfig"
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
    return TestUtils.getTestSuite(TestWbConfigEdit, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestWbConfigEdit.log", getTestSuite, sys.argv)

