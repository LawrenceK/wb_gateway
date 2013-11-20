# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

import sys, logging , time , os , thread
import unittest

from EventHandlers.tests.DummyRouter import *
from EventHandlers.hvac_components import *
from EventLib.Event import *
from MiscLib.DomHelpers import *
from EventHandlers.EventRouterLoad import EventRouterLoader
import EventHandlers.tests.TestEventLogger as TestEventLogger
_log = None
digitalCfg = """<valve name="Test Valve" key="tv1" type="digital">
            <directions>
                <direction name="Triangle Square (hot only)" key="TS" wbTarget ="10.100.100.102" do ="1" state='1'/> 
                <direction name="Circle Square (cold only)" key="CS" wbTarget ="10.100.100.102" do ="1" state='0'/>
            </directions>
        </valve>
        """
digitalTimedCfg = """<valve name="Test Valve" key="tv1" type="digitalTimed">
            <directions>
                <direction name="Triangle Square (hot only)" key="TS" wbTarget ="10.100.100.102" do ="1" pc='1'/> 
                <direction name="Circle Square (cold only)" key="CS" wbTarget ="10.100.100.102" do ="2" pc='2'/>
            </directions>
        </valve>
        """
aCfg = """<valve name="Test Valve" key="tv1" type="analog">
            <directions>
                <direction name="Triangle Square (hot only)" key="TS" wbTarget ="10.100.100.250" ao = '3' val = '30'/> 
                <direction name="Circle Square (cold only)" key="CS" wbTarget ="10.100.100.250" ao = '3'  val = '0'/>
            </directions>
        </valve>
        """
        
testELogger = """<eventInterfaces>
                    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
                        <eventtype type="">
                            <eventsource source="">
                                <event>
                                    <!-- stuff -->
                                </event>
                            </eventsource>
                        </eventtype>
                    </eventInterface>
                </eventInterfaces>
            """
class TestValve(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestValve" )
        self._log.debug( "\n\nsetUp" )
        eLogCfg = getDictFromXmlString(testELogger)
        self.loader = EventRouterLoader()
        self.loader.loadHandlers(eLogCfg)
        self.loader.start()
        self.router = self.loader.getEventRouter()
        self.triggered = False
     
        
    def tearDown(self):
        self._log.debug( "\n\nteardown" )
        TestEventLogger.logEvents()
        
    def testAnalogConfig(self):
        """
            Test to make sure the valve is configuring itself properly when using an analog output
        """
        TestEventLogger.logEvents()
        self._log.debug( "\n\nTestConfig")
        valveCfg = getDictFromXmlString(aCfg)
        self.valve = Valve(valveCfg['valve'],self.router)
        
        assert self.valve.aOutput == '3'
        assert self.valve.name == "Test Valve"
        assert self.valve.key == "tv1"
        assert self.valve.ao.aoCmd == 'AA;3;%(val)s:'
    
    def testDigitalConfig(self):
        """
            Test to make sure the valve is configuring itself properly when using a single digital output
            Commonly a spring loaded valve
        """
        TestEventLogger.logEvents()
        self._log.debug( "\n\nTestConfig")
        valveCfg = getDictFromXmlString(digitalCfg)
        valve = Valve(valveCfg['valve'],self.router)
     
        assert valve.wbTarget == "10.100.100.102"
        assert valve.name == "Test Valve"
        assert valve.key == "tv1"
        assert valve.type == 'digital'
        assert valve.move == {'CS':'0','TS':'1'}
        assert valve.dOutput == '1'
        assert valve.do.onCmd == 'DO;1;N:'
    
    def testDigitalTimedConfig(self):
        """
            Test to make sure the valve is configuring itself properly with two digital outputs
        """
        TestEventLogger.logEvents()
        self._log.debug( "\n\nTestConfig")
        valveCfg = getDictFromXmlString(digitalTimedCfg)
        valve = Valve(valveCfg['valve'],self.router)
        assert valve.move['TS'][1] == 1
        assert valve.move['CS'][1] == 2
        
        assert valve.move['TS'][0].onCmd == 'DO;1;N:'
        assert valve.move['CS'][0].onCmd == 'DO;2;N:'
        
    def publishDelayedEvent(self,event):
        time.sleep(0.5)
        self.router.publish(event.getSource() , event)
        
    def testAoTurn(self):
        """
            Test to make sure the correct events are being sent out when we request valvage
            We fake the return webbrick event to avoid having to set up a live webbrick
            The outgoing http request also never gets sent as we dont initialize twisted
        """            
        valveCfg = getDictFromXmlString(aCfg)
        self.valve = Valve(valveCfg['valve'],self.router)
        
        #turn the valve all the way to hot
        self.valve.doTurn("TS" , 100)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/analogoutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/3'
        assert TestEventLogger._events[0].getPayload()['val'] == '30'
        TestEventLogger.clearEvents()
        
        #turn the valve all the way to cold
        self.valve.doTurn("CS" , 100)        
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/analogoutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/3'
        assert TestEventLogger._events[0].getPayload()['val'] == '0'        
        TestEventLogger.clearEvents()
        
        #turn the valve halfway to hot
        self.valve.doTurn("TS" , 50)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/analogoutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/3'
        assert TestEventLogger._events[0].getPayload()['val'] == '15'        
        TestEventLogger.clearEvents()
        
        #turn the valve 25% further to hot, should end up getting rounded to 22
        self.valve.doTurn("TS" , 25)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/analogoutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/3'
        assert TestEventLogger._events[0].getPayload()['val'] == '22'        
        TestEventLogger.clearEvents()
    
    def testDoTurn(self):
        valveCfg = getDictFromXmlString(digitalCfg)
        self.valve = Valve(valveCfg['valve'],self.router)
        
        #because of the way the digital valves work, any turn its 100% in either direction
        #turn the valve all the way to hot
        self.valve.doTurn("TS" , 100)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/digitaloutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/1/on'
        TestEventLogger.clearEvents()
        
        #turn the valve all the way to cold
        self.valve.doTurn("CS" , 100)        
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/digitaloutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/1/off'
        TestEventLogger.clearEvents()
        
        #turn the valve halfway to hot 
        self.valve.doTurn("TS" , 50)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/digitaloutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/1/on'
        TestEventLogger.clearEvents()
        
        #turn the valve 25% further to hot
        self.valve.doTurn("TS" , 25)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/digitaloutput'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/1/on'     
        TestEventLogger.clearEvents()
    
    def testDoTTurn(self):
        valveCfg = getDictFromXmlString(digitalTimedCfg)
        self.valve = Valve(valveCfg['valve'],self.router)
        
        #turn the valve all the way to hot
        self.valve.doTurn("TS" , 100)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'internal/hvac/digitalout'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/2/off'
        assert TestEventLogger._events[1].getType()  == 'internal/hvac/digitalout'
        assert TestEventLogger._events[1].getSource() == 'hvac/valve/tv1/1/dwell'
        assert TestEventLogger._events[1].getPayload()['val'] == '100'        
        TestEventLogger.clearEvents()
        
        #turn the valve all the way to cold
        self.valve.doTurn("CS" , 100)        
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/digitalout'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/1/off'
        assert TestEventLogger._events[1].getType()  == 'internal/hvac/digitalout'
        assert TestEventLogger._events[1].getSource() == 'hvac/valve/tv1/2/dwell'
        assert TestEventLogger._events[1].getPayload()['val'] == '200'        
        TestEventLogger.clearEvents()
        
        #turn the valve halfway to hot
        self.valve.doTurn("TS" , 50)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/digitalout'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/2/off'  
        
        assert TestEventLogger._events[1].getType()  == 'internal/hvac/digitalout'
        assert TestEventLogger._events[1].getSource() == 'hvac/valve/tv1/1/dwell'
        assert TestEventLogger._events[1].getPayload()['val'] == '50'        
        TestEventLogger.clearEvents()
        
        #turn the valve 25% further to hot, should end up getting rounded to 22
        self.valve.doTurn("TS" , 25)
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType()  == 'internal/hvac/digitalout'
        assert TestEventLogger._events[0].getSource() == 'hvac/valve/tv1/2/off'  
        
        assert TestEventLogger._events[1].getType()  == 'internal/hvac/digitalout'
        assert TestEventLogger._events[1].getSource() == 'hvac/valve/tv1/1/dwell'
        assert TestEventLogger._events[1].getPayload()['val'] == '25'        
        TestEventLogger.clearEvents()
        
from MiscLib import TestUtils

def getTestSuite(select="unit"):
    testdict = {
            "unit":
                [   
                    "testAnalogConfig",
                    "testDigitalConfig",
                    "testDigitalTimedConfig",
                    "testAoTurn",
                    "testDoTurn",
                    "testDoTTurn"
                    
                ]
            }
    return TestUtils.getTestSuite(TestValve,testdict,select=select)
    
if __name__ == "__main__":
    TestUtils.runTests("TestValve.log" , getTestSuite , sys.argv)
