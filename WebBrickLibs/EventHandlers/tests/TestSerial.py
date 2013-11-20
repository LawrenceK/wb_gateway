# $Id: TestSerial.py 2610 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for Serial Eventhandler (Serial.py) 
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE:  The local serial parts of this unittest require a serial cable with pins 2 and 3 shorted* to be available at  address /dev/ttyUSB0
# *tx wired to rx so anything sent down it is recieved back, wiring must be decent otherwise there will be noise so the test will fail, 

import sys, time
import unittest

from MiscLib.DomHelpers  import *
from MiscLib.tests.Utils import TestTCPServer
from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

#import Events
from DummyRouter import *

from EventHandlers.Serial import Serial

import EventHandlers.tests.TestEventLogger as TestEventLogger

# Configuration for the tests

#
testConfigTCP = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventHandlers.Serial' name='Serial'>
        <serialPorts>
            <serialPort id="serial-1"  
                        port_type="tcp" 
                        name='My TCP Serial Port' 
                        ipAddress='127.0.0.1' 
                        port='4747'
                        driver = "TestDriver"
                        protocol_handler = "TestPHandler"
                        />            
        </serialPorts>
        
         <eventtype type="internal/test/serial">
            <eventsource source="serial/test/1" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="send" action = "light1/on" id='serial-1' />
	        </event>
            </eventsource>            
        </eventtype>
    </eventInterface>
"""

testConfigLocal = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventHandlers.Serial' name='Serial'>
        
        <!-- This is -->
        <serialPorts>
            <serialPort id="serial-2"  
                        type="local" 
                        name='A local serial port' 
                        uDevID = '/dev/ttyUSB0'
                        baudRate = '115200'                       
                        driver = "TestDriver"
                        protocol_handler = "TestPHandler"
                        />
        </serialPorts>
        
        <eventtype type="internal/test/serial">
            <eventsource source="serial/test/2" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="write" data="65;66;67:" id='serial-2' />
	        </event>
            </eventsource>            
        </eventtype>
        
    </eventInterface>
"""
testConfigLocalAndTCP = """<?xml version="1.0" encoding="utf-8"?>
    <eventInterface module='EventHandlers.Serial' name='Serial'>
        <serialPorts>
            <serialPort id="serial-1"  
                        type="tcp" 
                        name='My TCP Serial Port' 
                        ipAddress='127.0.0.1' 
                        port='4747'                        
                        driver = "TestDriver"
                        protocol_handler = "TestPHandler"
                        />   
            <serialPort id="serial-2"  
                        type="local" 
                        name='A local serial port' 
                        uDevID = '/dev/ttyUSB0'
                        baudRate = '115200'                       
                        driver = "TestDriver"
                        protocol_handler = "TestPHandler"
                        />
        </serialPorts>
        <eventtype type="internal/test/serial">
            <eventsource source="serial/test/1" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="send" data="65;66;67:" id='serial-1' />
	        </event>
            </eventsource>            
        </eventtype>
        
        <eventtype type="internal/test/serial">
            <eventsource source="serial/test/2" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="send" data="66;67;68:" id='serial-2' />
	        </event>
            </eventsource>            
        </eventtype>
        
        
    </eventInterface>
"""


# Some Events we might want to send

#evtDO_0_off = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/DO', 'webbrick/100/DO/0', { 'state':'0' } )
#evtDO_0_off = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/DO', 'webbrick/100/DO/0', { 'state':'0' } )

class TestSerial(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestEventMapper" )
        self._log.debug( "\n\n-------------------------------setUp-------------------------------" )
        self._log.debug( "\nInitializing dummy router" )
        self._router = DummyRouter()
        

    def tearDown(self):
        self._log.debug( "\n\n-------------------------------tearDown-------------------------------" )
        time.sleep(5)

    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)

    # Actual tests follow

    def testConfigureTCP(self):
        self._log.debug( "\n\n-------------------------------testConfigureTCP-------------------------------" )
        
        self._log.debug( "\nInitializng TCP server" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start()
        try:
            self._log.debug( "\nInitializing eventhandler" )
            testCfg = getDictFromXmlString(testConfigTCP)
            self._log.debug( "testCfg %s" % testCfg )
            eh = Serial(self._router)
            self.assertNotEqual( eh, None)
            eh.configure(testCfg['eventInterface'])
            eh.start()
            
            configuredPorts = eh.getSerialPorts()
            self._log.debug( "\n\nconfigured ports are: %s" % configuredPorts )
            assert(configuredPorts.has_key("serial-1"))
            if configuredPorts.has_key("serial-1"):
                self.assertNotEqual( configuredPorts["serial-1"], None)
            eh.stop()
            
        finally:
            TCPServ.stop()   

    def testConfigureLocal(self):
        self._log.debug( "\n\n-------------------------------testConfigureLocal-------------------------------" )
        
        testCfg = getDictFromXmlString(testConfigLocal)
        self._log.debug( "\nInitializng eventhandler" )
        self._log.debug( "testCfg %s" % testCfg )
        eh = Serial(self._router)
        self.assertNotEqual( eh, None)
        eh.configure(testCfg['eventInterface'])
        eh.start()
        
        configuredPorts = eh.getSerialPorts()
        self._log.debug( "\n\nconfigured ports are: %s" % configuredPorts )
        assert(configuredPorts.has_key("serial-2"))
        if configuredPorts.has_key("serial-2"):
            self.assertNotEqual( configuredPorts["serial-2"], None)
        
        eh.stop()   
    def testConfigureLocalAndTCP(self):
    
        self._log.debug( "\n\n-------------------------------testconfigureLocalAndTCP-------------------------------" )
        
        self._log.debug( "\nInitializng TCP server" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start() 
        try:
            self._log.debug( "\nInitializng eventhandler" )
            #load the test xml that contains both a local and TCP port
            testCfg = getDictFromXmlString(testConfigLocalAndTCP)              
            self._log.debug( "testCfg %s" % testCfg )        
            #initialize the eventhandler and make sure it intialized
            eh = Serial(self._router)
            self.assertNotEqual( eh, None)
            #call the configure method to load the ports from the xml
            eh.configure(testCfg['eventInterface'])
            #start the eventhandler
            eh.start()
            
            
            #get the list of serial ports from our handler        
            configuredPorts = eh.getSerialPorts()
            self._log.debug( "\n\nconfigured ports are: %s" % configuredPorts )
            
            #check our list of serial ports contains the correct serial ports
            assert(configuredPorts.has_key("serial-1"))
            if configuredPorts.has_key("serial-1"):
                self.assertNotEqual( configuredPorts["serial-1"], None)
                
            assert(configuredPorts.has_key("serial-2"))
            if configuredPorts.has_key("serial-2"):
                self.assertNotEqual( configuredPorts["serial-2"], None)
           
            eh.stop()   
        finally:
            TCPServ.stop()
            
    def testWriteLocal(self):
        """
        Test what happens when we start a write event to a Local serial port.
        """
        self._log.debug( "\n\n-------------------------------testWriteLocal-------------------------------" )
        testCfg = getDictFromXmlString(testConfigLocal)
        self._log.debug( "testCfg %s" % testCfg )

        eh = Serial(self._router)
        self.assertNotEqual( eh, None)
        eh.configure(testCfg['eventInterface'])
        eh.start()
        testEvent = makeEvent( 'internal/test/serial', 'serial/test/2')
        eh.handleEvent( testEvent )
        time.sleep(2)
        portlist = eh.getSerialPorts()      
        self._log.debug(portlist)
        self.assertEqual( len(self._router._pubs), 1 )
        self.assertEqual( self._router._pubs[0][1].getType(), "http://id.webbrick.co.uk/events/serial/receive" )
        self.assertEqual( self._router._pubs[0][1].getSource(), "serial-2/receive" )
        self.assertEqual( self._router._pubs[0][1].getPayload()['data'], "65;66;67:" )
        eh.stop()   
        
    def testWriteLocalCustomPayload(self):
        """
        Test what happens when we start a write event with a custom payload to a Local serial port.
        """
        self._log.debug( "\n\n-------------------------------testWriteLocalCustomPayLoad-------------------------------" )
        testCfg = getDictFromXmlString(testConfigLocal)
        self._log.debug( "testCfg %s" % testCfg )

        eh = Serial(self._router)
        self.assertNotEqual( eh, None)
        eh.configure(testCfg['eventInterface'])
        eh.start()
        testEvent = makeEvent( 'internal/test/serial', 'serial/test/2', {'cmd':'write','data':'66;67;68:','address':'serial-2'} )
        eh.handleEvent( testEvent )
        time.sleep(2)
        portlist = eh.getSerialPorts()      
        self._log.debug(portlist)
        self.assertEqual( len(self._router._pubs), 1 )
        self.assertEqual( self._router._pubs[0][1].getType(), "http://id.webbrick.co.uk/events/serial/receive" )
        self.assertEqual( self._router._pubs[0][1].getSource(), "serial-2/receive" )
        self.assertEqual( self._router._pubs[0][1].getPayload()['data'], "66;67;68:" )
        eh.stop()     
        
    def testWriteTCP(self):
        """
        Test what happens when we start a write event to a TCP serial port
        """
        self._log.debug( "\n\n-------------------------------testWriteTCP-------------------------------" )
        self._log.debug( "\nInitializng TCP server" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start() 
        try:
            self._log.debug( "\nInitializing serial eventhandler" )
            testCfg = getDictFromXmlString(testConfigTCP)
            self._log.debug( "\ntestCfg  : %s" %testCfg )
            eh=Serial(self._router)
            self.assertNotEqual( eh, None )
            eh.configure(testCfg['eventInterface'])
            eh.start()
            
            
            self._log.debug( "\nCreating test event :" )
            testEvent = makeEvent( 'internal/test/serial', 'serial/test/1', {} )
            self._log.debug( testEvent )
            
            self._log.debug( "\nTesting eventhandler..." )
            eh.handleEvent( testEvent )
            time.sleep(1)
            portlist = eh.getSerialPorts()
            self._log.debug( "\nList of active ports : %s" %portlist )
            data = TCPServ.data
            self._log.debug( "\nTCP server recieved : ##%s##" %data ) 
            assert data == "turn lights onsuccess!"
            eh.stop()
        finally:
            
            TCPServ.stop()
        
    def testWriteTCPCustomPayload(self):
        
        """
        Test what happens when we start a write event  to a TCP serial port with a custom payload
        """
        self._log.debug( "\n\n-------------------------------testWriteTCPCustomPayload-------------------------------" )
        self._log.debug( "\nInitializng TCP server" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start() 
        try:
            self._log.debug( "\nInitializing serial eventhandler" )
            testCfg = getDictFromXmlString(testConfigTCP)
            self._log.debug( "\ntestCfg  : %s" %testCfg )
            eh=Serial(self._router)
            self.assertNotEqual( eh, None )
            eh.configure(testCfg['eventInterface'])
            eh.start()
            
            
            self._log.debug( "\nCreating test event :" )
            testEvent = makeEvent( 'internal/test/serial', 'serial/test/1', {'cmd':'send','action':'HELLO','id':'serial-1'} )
            self._log.debug( testEvent )
            
            self._log.debug( "\nTesting eventhandler..." )
            eh.handleEvent( testEvent )
            time.sleep(1)
            portlist = eh.getSerialPorts()
            self._log.debug( "\nList of active ports : %s" %portlist )
            data = TCPServ.data
            self._log.debug( "\nTCP server recieved : ##%s##" %data ) 
            assert data == "turn lights onsuccess!"  
            eh.stop()
        finally :  
            
            TCPServ.stop()
            time.sleep(2)        
            
    def testWriteTCPAndLocal(self):        
        """
        Test what happens when we start a write event  to a TCP serial port and a Local one at the same time
        """
        self._log.debug( "\n\n-------------------------------testWriteTCPAndLocal-------------------------------" )
        self._log.debug( "\nInitializng TCP server" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start() 
        try:
            self._log.debug( "\nInitializing serial eventhandler" )
            testCfg = getDictFromXmlString(testConfigLocalAndTCP)
            self._log.debug( "\ntestCfg  : %s" %testCfg )
            eh=Serial(self._router)
            self.assertNotEqual( eh, None )
            
            self._log.debug( "\n Configuring serial eventhandler" )
            eh.configure(testCfg['eventInterface'])
            eh.start()         
            
            self._log.debug( "\nCreating test events :" )   
            TCPSerialevent = makeEvent( 'internal/test/serial', 'serial/test/1', {} )  
            localSerialevent = makeEvent( 'internal/test/serial', 'serial/test/2', {} ) 
               
            self._log.debug( "%s and %s" %(localSerialevent,TCPSerialevent) )      
                        
            self._log.debug( "\nSending TCP event..." )
            eh.handleEvent( TCPSerialevent )            
            self._log.debug( "\nSending local event..." )
            eh.handleEvent( localSerialevent )
            
            time.sleep(1)
            
            portlist = eh.getSerialPorts()
            self._log.debug( "\nList of active ports : %s" %portlist )
            TCPData = TCPServ.data
            self._log.debug( "\nTCP server recieved : ##%s##" %TCPData ) 
            assert TCPData == 'ABC'
            self.assertEqual( len(self._router._pubs), 1 )
            self.assertEqual( self._router._pubs[0][1].getType(), "http://id.webbrick.co.uk/events/serial/receive" )
            self.assertEqual( self._router._pubs[0][1].getSource(), "serial-2/receive" )
            self.assertEqual( self._router._pubs[0][1].getPayload()['data'], "66;67;68:" )   

            self._log.debug( "\nLocal serial recieved local data ") 



            eh.stop()
        finally :  
            
            TCPServ.stop()
            time.sleep(1)        
    
    def testReadTCP(self):
        """
        Test recieve callback is working correctly for serial ports
        """
        self._log.debug( "\n\n-------------------------------testReadTCP-------------------------------" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start()
        try:
            self._log.debug( "\nInitializing serial eventhandler with tcp connection configured" )
            testCfg = getDictFromXmlString(testConfigTCP)
            eh = Serial(self._router)
            self.assertNotEqual( eh, None )
            
            eh.configure(testCfg['eventInterface'])
            eh.start()
            
            self._log.debug ( "Sending test data" )
            TCPServ.send("hello\r")
            time.sleep(1)
            self.assertEqual( len(self._router._pubs), 1 )
            self.assertEqual( self._router._pubs[0][1].getType(), "lighting/update" )
            self.assertEqual( self._router._pubs[0][1].getSource(), "light1/on" )
            self.assertEqual( self._router._pubs[0][1].getPayload()['lightval'], "1")   
            eh.stop()
        finally:
            
            TCPServ.stop()
            time.sleep(1)     
    
    def testReadLocal(self):
        """
        Test recieve callback is working correctly for serial ports
        """
        self._log.debug( "\n\n-------------------------------testReadLocal-------------------------------" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start()
        try:
            self._log.debug( "\nInitializing serial eventhandler with tcp connection configured" )
            testCfg = getDictFromXmlString(testConfigLocal)
            eh = Serial(self._router)
            self.assertNotEqual( eh, None )
            
            eh.configure(testCfg['eventInterface'])
            eh.start()
            
            self._log.debug ( "Sending test data" )
            portlist = eh.getSerialPorts()
            portlist["serial-2"].write("hello\r")
            portlist["serial-2"].write("world\r")
            time.sleep(2)
            self.assertEqual( len(self._router._pubs), 2 )
            self.assertEqual( self._router._pubs[0][1].getType(), "http://id.webbrick.co.uk/events/serial/receive" )
            self.assertEqual( self._router._pubs[0][1].getSource(), "serial-2/receive" )
            self.assertEqual( self._router._pubs[0][1].getPayload()['data'], "104;101;108;108;111:" )   
            self.assertEqual( self._router._pubs[1][1].getType(), "http://id.webbrick.co.uk/events/serial/receive" )
            self.assertEqual( self._router._pubs[1][1].getSource(), "serial-2/receive" )
            self.assertEqual( self._router._pubs[1][1].getPayload()['data'], "119;111;114;108;100:" )  
            eh.stop()
        finally:
            
            TCPServ.stop()
            time.sleep(1)
    
    def testDisconnectRecover(self):
        """
        Test recieve callback is working correctly for serial ports
        """
        self._log.debug( "\n\n-------------------------------testReadTCP-------------------------------" )
        TCPServ = TestTCPServer(4747)
        TCPServ.start()
        self._log.debug( "\nInitializing serial eventhandler with tcp connection configured" )
        testCfg = getDictFromXmlString(testConfigTCP)
        eh = Serial(self._router)
        self.assertNotEqual( eh, None )
            
        eh.configure(testCfg['eventInterface'])
        eh.start()
            
        self._log.debug ( "Sending test data" )
        TCPServ.send("hello\r")
        
            
        time.sleep(0.5)
        self.assertEqual( len(self._router._pubs), 1 ) 
        self.assertEqual( self._router._pubs[0][1].getType(), "lighting/update" )
        self.assertEqual( self._router._pubs[0][1].getSource(), "light1/on" )
        self.assertEqual( self._router._pubs[0][1].getPayload()['lightval'], "1")     
        TCPServ.stop()
        time.sleep(0.5)
        TCPServ = TestTCPServer(4747)
        TCPServ.start()
        testEvent = makeEvent( 'internal/test/serial', 'serial/test/1', {} )
        self._log.debug( testEvent )            
        self._log.debug( "\nTesting eventhandler..." )
        eh.handleEvent( testEvent )
        eh.handleEvent( testEvent )
        eh.handleEvent( testEvent )
        eh.handleEvent( testEvent ) 
        TCPServ.send("hello\r")
        time.sleep(1)
        assert TCPServ.read() == "turn lights onsuccess!turn lights onsuccess!"
        self.assertEqual( len(self._router._pubs), 2 )
        
        self.assertEqual( self._router._pubs[1][1].getType(), "lighting/update" )
        self.assertEqual( self._router._pubs[1][1].getSource(), "light1/on" )
        self.assertEqual( self._router._pubs[1][1].getPayload()['lightval'], "1")  
        time.sleep(0.5)
        
               
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
            [ 
            "testConfigureTCP",
            "testWriteTCP",
            "testWriteTCPCustomPayload",
            "testReadTCP",
            "testDisconnectRecover"
            ],
        "component":
            [
            "testConfigureLocal",
            "testConfigureLocalAndTCP",
            "testWriteLocal",
            "testWriteLocalCustomPayload",
            "testWriteTCPAndLocal",
            "testReadLocal" 
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestSerial, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestSerial.log", getTestSuite, sys.argv)
