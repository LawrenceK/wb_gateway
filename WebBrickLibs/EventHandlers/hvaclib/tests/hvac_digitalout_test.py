import sys, logging , time , os , thread
import unittest

from EventHandlers.tests.DummyRouter import *
from EventHandlers.hvac_components import *
from EventLib.Event import *
from MiscLib.DomHelpers import *
from EventHandlers.EventRouterLoad import EventRouterLoader
import EventHandlers.tests.TestEventLogger as TestEventLogger
_log = None
dCfg = """<valve name="valve name" key="unique key" type="diverting">
            <directions>
                <direction name="Triangle Square (hot only)" key="TS" wbTarget ="10.100.100.102" cmd ="DO;1;N:" /> 
                <direction name="Circle Square (cold only)" key="CS" wbTarget ="10.100.100.102" cmd ="DO;2;N:" />
            </directions>
        </valve>
        """
aCfg = """<valve name="valve name" key="unique key" type="diverting">
            <directions>
                <direction name="Triangle Square (hot only)" key="TS" wbTarget ="10.100.100.102" cmd ="AA;1;100:" /> 
                <direction name="Circle Square (cold only)" key="CS" wbTarget ="10.100.100.102" cmd ="AA;1;0:" />
            </directions>
        </valve>
        """
testELogger = """<eventInterfaces><eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
    </eventInterfaces>
    """
class TestDigitalOutput(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestAnalogOuput" )
        self._log.debug( "\n\nsetUp" )
        eLogCfg = getDictFromXmlString(testELogger)
        self.loader = EventRouterLoader()
        self.loader.loadHandlers(eLogCfg)
        self.loader.start()
        self.router = self.loader.getEventRouter()
        self.triggered = False
        
    def tearDown(self):
        self._log.debug( "\n\nteardown" )
        
    def sendDelayedEvent(self,event,*args):
        time.sleep(2)
        self.router.publish(event.getSource() , event)
    
    def turnDoOn(self,do):
        do.turnOn()
        self.triggered = True
        
    def turnDoOff(self,do):
        do.turnOff()
        self.triggered = True
        
    def testConfig(self):
        self._log.debug( "\n\nTestConfig")
        do = DigitalOutput('do/type' , 'do/source', self.router, '10.100.100.100','2')
        httpActionCfg = do.httpAction.__dict__['_typeConfig']
        self._log.debug(httpActionCfg)
        self._log.debug("wbTarget : %s" %do.wbTarget)
        self._log.debug("eType : %s" %do.eType)
        self._log.debug("eOnSource : %s" %do.eOnSource)
        self._log.debug("eOffSource : %s" %do.eOffSource)
        self._log.debug("onCmd : %s" %do.onCmd)
        self._log.debug("offCmd : %s" %do.offCmd)
        self._log.debug("doNum : %s" %do.doNum)
        self._log.debug("nodeNum : %s" %do.nodeNum)
        self._log.debug("eDwellSource : %s" %do.eDwellSource)
        self._log.debug("dwellCmd : %s" %do.dwellCmd)
        
        #check httpaction was configured properly, some funkyness required to get to the action uri
        assert len(httpActionCfg['do/type']) == 3
        assert httpActionCfg['do/type']['do/source/off'][0][1][0]['uri'] == '/cfg.spi?com=DO;2;F:'
        assert httpActionCfg['do/type']['do/source/on'][0][1][0]['uri'] == '/cfg.spi?com=DO;2;N:'
        assert httpActionCfg['do/type']['do/source/dwell'][0][1][0]['uri'] == '/cfg.spi?com=DO;2;D;%(val)s:'
        
        assert do.wbTarget == '10.100.100.100'
        assert do.eType == 'do/type'
        assert do.eOnSource == 'do/source/on'
        assert do.eOffSource == 'do/source/off'
        assert do.localrouter == self.router
        assert do.onCmd == 'DO;2;N:'
        assert do.offCmd == 'DO;2;F:'
        assert do.doNum == '2'
        assert do.nodeNum == '100'
        assert do.eDwellSource == 'do/source/dwell'
        assert do.dwellCmd == 'DO;2;D;%(val)s:'
        
    def testSetDOOn(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/on'
        
        
    def testSetDOOnDwell(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn(100)
        #let eventrouter catch up
        time.sleep(0.2)
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/dwell'
        assert TestEventLogger._events[0].getPayload()['val'] == '100'
        TestEventLogger.logEvents()
    
    def testSetDODwellFinish(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/on'
                          
    def testSetDOOff(self):
        self._log.debug( "\n\ntestSetDOOff" )
        self.timeout = time.time() + 5
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOff()
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/off'
    
    def testSetDOOnCorrect(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        doEvent = makeEvent('http://id.webbrick.co.uk/events/webbrick/DO','webbrick/100/DO/2',{'state':'0'})
        do.turnOn()
        self.router.publish(doEvent.getSource(),doEvent)
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/on'
        assert TestEventLogger._events[2].getType() == 'do/type'
        assert TestEventLogger._events[2].getSource() == 'do/source/on'
    
    def testSetDOOnDwellCorrect(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        doEvent = makeEvent('http://id.webbrick.co.uk/events/webbrick/DO','webbrick/100/DO/2',{'state':'0'})
        do.turnOn(10)
        self.router.publish(doEvent.getSource(),doEvent)
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/dwell'
        assert TestEventLogger._events[0].getPayload()['val'] == '10'
        assert TestEventLogger._events[2].getType() == 'do/type'
        assert TestEventLogger._events[2].getSource() == 'do/source/dwell'
        assert TestEventLogger._events[2].getPayload()['val'] == '10'
    
    def testSetDOOffCorrect(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        doEvent = makeEvent('http://id.webbrick.co.uk/events/webbrick/DO','webbrick/100/DO/2',{'state':'1'})
        do.turnOff()
        self.router.publish(doEvent.getSource(),doEvent)
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/off'        
        assert TestEventLogger._events[2].getType() == 'do/type'
        assert TestEventLogger._events[2].getSource() == 'do/source/off'
    
    #test every possible transition
    def testOnOff(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn()
        do.turnOff()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/on'        
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/off'
    
    def testOffOn(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOff()
        do.turnOn()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/off'        
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/on'
        
    def testDwellDwell(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn(10)
        do.turnOn(10)
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/dwell'    
        assert TestEventLogger._events[0].getPayload()['val'] == '10'       
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/dwell'            
        assert TestEventLogger._events[1].getPayload()['val'] == '10'
        
    def testDwellOff(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn(10)
        do.turnOff()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/dwell'            
        assert TestEventLogger._events[0].getPayload()['val'] == '10'       
         
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/off'
        
    def testDwellOn(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn(10)
        do.turnOn()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/dwell'                    
        assert TestEventLogger._events[0].getPayload()['val'] == '10'
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/on'
        
    def testOffDwell(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOff()
        do.turnOn(10)
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/off'        
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/dwell'            
        assert TestEventLogger._events[1].getPayload()['val'] == '10'
        
    def testOnDwell(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn()
        do.turnOn(10)
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/on'        
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/dwell'    
        assert TestEventLogger._events[1].getPayload()['val'] == '10'
        
        
    def testOnOn(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOn()
        do.turnOn()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/on'        
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/on'
        
    def testOffOff(self):
        self._log.debug( "\n\ntestSetDOOn" )
        self.timeout = time.time() + 15
        do = DigitalOutput('do/type','do/source',self.router,'10.100.100.100','2')
        do.turnOff()
        do.turnOff()
        #let eventrouter catch up
        time.sleep(0.2)
        TestEventLogger.logEvents()
        assert TestEventLogger._events[0].getType() == 'do/type'
        assert TestEventLogger._events[0].getSource() == 'do/source/off'        
        assert TestEventLogger._events[1].getType() == 'do/type'
        assert TestEventLogger._events[1].getSource() == 'do/source/off'
        
from MiscLib import TestUtils

def getTestSuite(select="unit"):
    testdict = {
            "unit":
                [   "testSetDOOn",
                    "testSetDOOnDwell",
                    "testSetDOOff",
                    "testConfig",
                    "testOnOff",
                    "testOffOn",
                    "testDwellDwell",
                    "testDwellOff",
                    "testDwellOn",
                    "testOffDwell",
                    "testOnDwell",
                    "testOnOn",
                    "testOffOff"
                ]
            }
    return TestUtils.getTestSuite(TestDigitalOutput,testdict,select=select)
    
if __name__ == "__main__":
    TestUtils.runTests("TestDigitalOutput.log" , getTestSuite , sys.argv)
