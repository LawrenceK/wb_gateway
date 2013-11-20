# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# 
#
# Unit testing for hvac mixing circuit class
# See http://pyunit.sourceforge.net/pyunit.html
#

import os
import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *
from EventHandlers.hvac_mix import MixingCircuit
from EventLib.Event import Event
# Configuration for the tests
testConfigPump = """<mixingcircuit key = "1" control="simple" step_100="10" step_1="5"  deadband="2" settletime = "1" >

<!-- Optional -->

    <slope type="internal/hvac/slope" source="temperature/zonegroup/2" key="val" />
    <offset type="internal/hvac/offset" source="temperature/zonegroup/2" key="val" />
    <outsidetemp type="internal/hvac/outside" source="temperature/zonegroup/2" key="val" />   
    <actualtemp type="internal/hvac/actual" source="temperature/zonegroup/2" key="val" />
    
<!-- Mandatory -->
    <valve key="ufhmix" >
        <hotter direction= "CT"/>
        <cooler direction= "ST"/>
    </valve>

<!-- Optional -->
    <pump key="ufhpump"/>
    
</mixingcircuit>
"""
testConfigNoPump = """<mixingcircuit key = "1" control="simple" step_100="10" step_1="5"  deadband="2" settletime = "1" >

<!-- Optional -->

    <slope type="internal/hvac/slope" source="temperature/zonegroup/2" key="val" />
    <offset type="internal/hvac/offset" source="temperature/zonegroup/2" key="val" />
    <outsidetemp type="internal/hvac/outside" source="temperature/zonegroup/2" key="val" />   
    <actualtemp type="internal/hvac/actual" source="temperature/zonegroup/2" key="val" />
    
<!-- Mandatory -->
    <valve key="ufhmix" >
        <hotter direction= "CT"/>
        <cooler direction= "ST"/>
    </valve>    
</mixingcircuit>
"""
testConfigDefaults = """<mixingcircuit key = "1" control="simple" step_100="10" step_1="5"  deadband="2" settletime = "1" >
    
<!-- Mandatory -->
    <valve key="ufhmix" >
        <hotter direction= "CT"/>
        <cooler direction= "ST"/>
    </valve>    
</mixingcircuit>
"""
testConfigStepping = """<mixingcircuit key = "1" control="simple" step_10="10" step_1="1" step_2="2" step_3="3" step_4="4" deadband="2" settletime = "1" >    
<!-- Mandatory -->
    <valve key="ufhmix" >
        <hotter direction= "CT"/>
        <cooler direction= "ST"/>
    </valve>    
</mixingcircuit>
"""
class dummyHvac():
    def __init__(self):
        self.subList = {}
        self.actionedList = {}
    def subEvent(self,event,mc):
        if self.subList.has_key(mc):
            self.subList[mc][event] = True
        else:
            self.subList[mc] = { event : True }    
    
    def actionComponent(self,componentType,key,*args):
        if self.actionedList.has_key(componentType):        
            self.actionedList[componentType][key] = args
        else:
            self.actionedList[componentType] = { key : args }
            
class testMixingCircuit(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "testHvac_MixingCircuit" )
        self._log.debug( "\n\nsetUp" )
        self.hvac = dummyHvac()


    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    # Actual tests follow
    def testConfigure_pump(self):
        self._log.debug( "\nTestConfigure_Pump" )
        cfgDict = getDictFromXmlString(testConfigPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        self._log.debug("MC.SettleTime : %i" %self.mc.settleTime)
        self._log.debug("MC.hotterDirectionKey : %s" %self.mc.hotterDirectionKey)
        self._log.debug("MC.coolerDirectionKey : %s" %self.mc.coolerDirectionKey)
        self._log.debug("MC.valveKey : %s" %self.mc.valveKey)
        self._log.debug("MC.pumpKey : %s" %self.mc.pumpKey)
        assert self.mc.settleTime == 1
        assert self.mc.hotterDirectionKey == "CT"
        assert self.mc.coolerDirectionKey == "ST"
        assert self.mc.valveKey == "ufhmix"
        assert self.mc.pumpKey == "ufhpump"
    
    def testConfigure_nopump(self):
        self._log.debug( "\nTestConfigure_NoPump" )
        cfgDict = getDictFromXmlString(testConfigNoPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        self._log.debug("MC.SettleTime : %i" %self.mc.settleTime)
        self._log.debug("MC.hotterDirectionKey : %s" %self.mc.hotterDirectionKey)
        self._log.debug("MC.coolerDirectionKey : %s" %self.mc.coolerDirectionKey)
        self._log.debug("MC.valveKey : %s" %self.mc.valveKey)
        self._log.debug("MC.pumpKey : %s" %self.mc.pumpKey)
        assert self.mc.settleTime == 1
        assert self.mc.hotterDirectionKey == "CT"
        assert self.mc.coolerDirectionKey == "ST"
        assert self.mc.valveKey == "ufhmix"
        assert self.mc.pumpKey == None    
    
    def testSubscribes(self):
        self._log.debug( "\nTestConfigure_Subscribes" )
        cfgDict = getDictFromXmlString(testConfigPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        assert self.hvac.subList.has_key(self.mc)
        foundOffset = False
        foundSlope = False
        foundOutside = False
        foundActual = False
        for event in self.hvac.subList[self.mc]:
            if event.getType() == "internal/hvac/slope" and event.getSource() == "temperature/zonegroup/2":
                foundSlope = True    
            if event.getType() == "internal/hvac/offset" and event.getSource() == "temperature/zonegroup/2":
                foundOffset = True
            if event.getType() == "internal/hvac/actual" and event.getSource() == "temperature/zonegroup/2":
                foundActual = True
            if event.getType() == "internal/hvac/outside" and event.getSource() == "temperature/zonegroup/2":
                foundOutside = True
        assert foundOffset and foundSlope and foundOutside and foundActual
        
    def testDefaultSubscribes(self):
        self._log.debug( "\nTestConfigure_DefaultSubscribes" )
        cfgDict = getDictFromXmlString(testConfigDefaults)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        assert self.hvac.subList.has_key(self.mc)
        foundOffset = False
        foundSlope = False
        foundOutside = False
        foundActual = False
        for event in self.hvac.subList[self.mc]:
            if event.getType() == "internal/hvac/slope" and event.getSource() == "mixingcircuit/1":
                foundSlope = True    
            if event.getType() == "internal/hvac/offset" and event.getSource() == "mixingcircuit/1":
                foundOffset = True
            if event.getType() == "internal/hvac/actualtemp" and event.getSource() == "mixingcircuit/1":
                foundActual = True
            if event.getType() == "internal/hvac/outsidetemp" and event.getSource() == "mixingcircuit/1":
                foundOutside = True
        assert foundOffset and foundSlope and foundOutside and foundActual    
    
    def testSlope(self):
        self._log.debug( "\nTestSlope" )
        cfgDict = getDictFromXmlString(testConfigPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        slopeEvent = Event("internal/hvac/slope","temperature/zonegroup/2" , {"val" : "5"})
        self.mc.newEvent(slopeEvent)
        self._log.debug("MC.Slope = %s" %self.mc.slope)
        assert self.mc.slope == 5.0
        
    def testOffset(self):
        self._log.debug( "\nTestOffset" )
        cfgDict = getDictFromXmlString(testConfigPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        offsetEvent = Event("internal/hvac/offset","temperature/zonegroup/2" , {"val" : "30"})
        self.mc.newEvent(offsetEvent)
        self._log.debug("MC.Offset = %s" %self.mc.offset)
        assert self.mc.offset == 30
        
    def testOutsideTemp(self):
        self._log.debug( "\nTestOutsideTemp" )
        cfgDict = getDictFromXmlString(testConfigPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        outsideEvent = Event("internal/hvac/outside","temperature/zonegroup/2" , {"val" : "50"})
        self.mc.newEvent(outsideEvent)
        self._log.debug("MC.outsidetemp = %s" %self.mc.outsidetemp)
        assert self.mc.outsidetemp == 50
        
    def testActualTemp(self):
        self._log.debug( "\nTestActualTemp" )
        cfgDict = getDictFromXmlString(testConfigPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        actualEvent = Event("internal/hvac/actual","temperature/zonegroup/2" , {"val" : "70"})
        self.mc.newEvent(actualEvent)
        self._log.debug("MC.actualtemp = %s" %self.mc.actualtemp)
        assert self.mc.actualtemp == 70
    
    def testDemand(self):    
        self._log.debug( "\nTestActualTemp" )
        cfgDict = getDictFromXmlString(testConfigPump)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        offsetEvent = Event("internal/hvac/offset","temperature/zonegroup/2" , {"val" : "30"})
        slopeEvent = Event("internal/hvac/slope","temperature/zonegroup/2" , {"val" : "5"})
        outsideEvent = Event("internal/hvac/outside","temperature/zonegroup/2" , {"val" : "50"})
        actualEvent = Event("internal/hvac/actual","temperature/zonegroup/2" , {"val" : "70"})
        
        self.mc.newEvent(offsetEvent)
        self.mc.newEvent(slopeEvent)
        self.mc.newEvent(outsideEvent)
        self.mc.newEvent(actualEvent)
        #we expect no actions to be taken as there is no demand
        assert self.hvac.actionedList == {}
        self.mc.onDemand()
        #pump should be switched on now
        assert self.mc.demand == True
        assert self.hvac.actionedList["pump"]["ufhpump"] == ('TURN ON',)
        self.mc.onNoDemand()
        #pump should be turned off and the valve should be requested to turn fully to cold
        assert self.hvac.actionedList["pump"]["ufhpump"] == ('TURN OFF',)
        assert self.hvac.actionedList["valve"]["ufhmix"] == ({'turn' : 'ST' , 'amount' : 100},)
        #turn demand back on
        self.mc.onDemand()
        assert self.mc.demand == True
        assert self.hvac.actionedList["pump"]["ufhpump"] == ('TURN ON',)
        self.hvac.actionedList = {}
        outsideEvent = Event("internal/hvac/outside" , "temperature/zonegroup/2" , {"val" : "-10000"})
        self.mc.newEvent(outsideEvent)
        #throttling should prevent any actions
        assert self.hvac.actionedList == {}

        time.sleep(1.5)
        self.mc.newEvent(outsideEvent)
        #now a new event should trigger a valve movement
        assert self.hvac.actionedList["valve"]["ufhmix"] == ({'turn' : 'CT' , 'amount' : 100},)
        
        time.sleep(1.5)
        outsideEvent = Event("internal/hvac/outside" , "temperature/zonegroup/2" , {"val" : "10000"})
        self.mc.newEvent(outsideEvent)
        #should trigger a valve movement in the opposite direction
        assert self.hvac.actionedList["valve"]["ufhmix"] == ({'turn' : 'ST' , 'amount' : 100},)
    def testStepping(self):
        self._log.debug( "\nTestActualTemp" )
        cfgDict = getDictFromXmlString(testConfigStepping)
        self.mc = MixingCircuit(cfgDict["mixingcircuit"],self.hvac)
        assert self.mc.stepDict == {1:1 , 2:2 , 3:3 , 4:4 , 10:10}
        
    def testDummy(self):
        return
    
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
            [ "testConfigure_pump",
              "testConfigure_nopump",
              "testSlope",
              "testOffset",
              "testOutsideTemp",
              "testActualTemp",
              "testDemand",
              "testSubscribes",
              "testDefaultSubscribes",
              "testStepping"
            
            ],
        "zzcomponent":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(testMixingCircuit, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("hvac_mixingcircuit_test.log", getTestSuite, sys.argv)
 
