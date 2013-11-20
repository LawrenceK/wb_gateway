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
class TestAnalogOutput(unittest.TestCase):
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
        time.sleep(0.5)
        self.router.publish(event.getSource() , event)
    
    def setAOTimeOut(self,ao,val):
        try:
            ao.SetAO(val)
        except:
            self._log.debug("SetAO timed out correctly")
            self.triggered = True
  
        
    def testConfig(self):
        self._log.debug( "\n\nTestConfig")
        ao = AnalogOutput('ao/type' , 'ao/source', self.router, '10.100.100.100','2')
        assert ao.wbTarget == '10.100.100.100'
        assert ao.eType == 'ao/type'
        assert ao.eSource == 'ao/source'
        assert ao.localrouter == self.router
        assert ao.aoCmd == 'AA;2;%(val)s:'
        assert ao.aoNum == '2'
        assert ao.nodeNum == '100'
        
    def testSetAO(self):
        self._log.debug( "\n\nTestSetAO" )
        self.timeout = time.time() + 5
        ao = AnalogOutput('ao/type','ao/source',self.router,'10.100.100.100','2')
        aoEvent = makeEvent('http://id.webbrick.co.uk/events/webbrick/AO' ,'webbrick/100/AO/2', { 'val' : '100' } )
        #thread.start_new_thread(self.sendDelayedEvent,(aoEvent,))
        ao.SetAO(100)
        #eventrouter is threaded so yield execution for a moment so events propagate
        time.sleep(0.2)
        assert TestEventLogger._events[0].getType() == 'ao/type'
        assert TestEventLogger._events[0].getSource() == 'ao/source'
        assert TestEventLogger._events[0].getPayload()['val'] == '100'
        TestEventLogger.logEvents()
        
    def testCorrectAO(self):
        self._log.debug( "\n\nTestSetAO" )
        self.timeout = time.time() + 5
        ao = AnalogOutput('ao/type','ao/source',self.router,'10.100.100.100','2')
        aoEvent = makeEvent('http://id.webbrick.co.uk/events/webbrick/AO' ,'webbrick/100/AO/2', { 'val' : '10' } )
        #thread.start_new_thread(self.sendDelayedEvent,(aoEvent,))
        ao.SetAO(100)
        #eventrouter is threaded so yield execution for a moment so events propagate
        time.sleep(0.2)
        self.router.publish(aoEvent.getSource() , aoEvent)
        time.sleep(0.2) 
        assert TestEventLogger._events[2].getType() == 'ao/type'
        assert TestEventLogger._events[2].getSource() == 'ao/source'
        assert TestEventLogger._events[2].getPayload()['val'] == '100'
        TestEventLogger.logEvents()   
              
from MiscLib import TestUtils

def getTestSuite(select="unit"):
    testdict = {
            "unit":
                [   "testSetAO",
                    "testCorrectAO",
                    "testConfig"
                ]
            }
    return TestUtils.getTestSuite(TestAnalogOutput,testdict,select=select)
    
if __name__ == "__main__":
    TestUtils.runTests("TestAnalogOutput.log" , getTestSuite , sys.argv)
