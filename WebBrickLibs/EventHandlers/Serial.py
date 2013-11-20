#----------------------------------------------------------------------------------
#
#   Class handling connections to a serial device via tcp or local serial cable
#
#----------------------------------------------------------------------------------
import logging
from MiscLib import TCPWrapper, SerialWrapper
from EventLib.Event import Event, makeEvent

from EventLib.EventAgent import EventAgent
from EventLib.EventHandler import EventHandler

from EventHandlers.BaseHandler import BaseHandler
from EventHandlers.Utils import *

from MiscLib import TestUtils

from WebBrickLibs.ParameterSet import ParameterSet
from MiscLib.WrapperReactor import *

from MiscLib import DummyDriver
from MiscLib import LutronDriver
from MiscLib import NADDriver
from MiscLib import SkyDriver
from MiscLib import DuskyDriver

class SerialConnection():
    def __init__( self, SerialPort, Driver , ProtocolHandler, Id, Config ):
        self.SerialPort = SerialPort
        self.Driver = Driver
        self.ProtocolHandler = ProtocolHandler
        self.Id = Id 
        self.Config = Config
        
class Serial( BaseHandler ):
    """
    
    The configuration for a Serial Event Handler entry is as follows:

    
    
    Setting up serial ports at runtime 
    
    <eventInterface module='EventHandlers.Serial' name='Serial'>
        <serialPorts>
            <serialPort id="serial-1"  
                        type="tcp" 
                        name='LutronTCP' 
                        ipAddress = 'localhost' 
                        port='23'
                        driver = 'drivertype'
                        protocol_handler = 'handler'
                        />
            <serialPort id="serial-2"  
                        type="local" 
                        name='LutronLocal' 
                        uDevID = 'serial'
                        baudRate = '115200'
                        driver = 'drivertype'
                        protocol_handler = 'handler'
                        />
            </serialPort>
            <serialPort id="serial-3"  type="http" name='An http to serial relay' >
                <soonToCome/>
            </serialPort>     
        </serialPorts>
    </eventInterface>
    
    Listening for data via Serial Ports:
     <eventInterface module='EventHandlers.Serial' name='Serial'>
        <eventtype type="internal/test/serial">
            <eventsource source="serial/test/1" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="read" data="64;65;66:" id='serial-1' />
	        </event>
            </eventsource>
            <eventsource source="serial/test/2" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="read" data="64 65 66:" id='serial-2' />
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
    
    Sending data via Serial Ports:

    <eventInterface module='EventHandlers.Serial' name='Serial'>
        <eventtype type="internal/test/serial">
            <eventsource source="serial/read/1" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="write" data="64;65;66:" id='serial-1' />
	        </event>
            </eventsource>
            <eventsource source="serial/read/2" >
	        <event>
                    <params>
                    </params>
                    <serial cmd="write" data="64 65 66:" id='serial-2' />
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    """
    def __init__ ( self , localRouter ):
        super( Serial , self ).__init__( localRouter )
        self._serialPorts = dict()
         #the reactor starts automatically
        self._wrapperReactor = WrapperReactor()
    
    def AddConnection( self , PortConfig ):
        if PortConfig.has_key( "id" ) & PortConfig.has_key( "driver" ) & PortConfig.has_key( "protocol_handler" ) & (self.isValidTCPCFG( PortConfig ) | self.isValidLocalCFG( PortConfig )):                 
                driver = self.GetDriver( PortConfig[ "driver" ] , PortConfig["id"] )
                if driver != None:
                    pHandler = self.GetProtocolHandler( PortConfig[ "protocol_handler" ] )
                    if pHandler != None:
                        self._log.debug( 'Attempting to connect to port %s' % PortConfig )         
                        wrapper = self.GetWrapper( PortConfig )
                        serialC = SerialConnection( wrapper , driver , pHandler , PortConfig[ 'id' ], PortConfig )
                        self._log.debug( 'Adding port %s to list' %serialC )
                        self._serialPorts[ PortConfig[ 'id' ] ] = serialC
                        if wrapper != None:
                            self._log.debug( 'Inserting port "%s" into reactor' %serialC )               
                            self._wrapperReactor.addWrapper( serialC.Id , serialC.SerialPort , self.DataReceivedCallback ,"read" )   
                        else:
                            self._log.error( 'Failed to initialize wrapper, possible connection problem , will retry later' )
                    else:
                        self._log.error( "Protocol Handler %s does not exist , invalid Serial Port - Ignoring" %PortConfig[ "protocol_handler" ] )
                else:
                    self._log.error( "Driver %s does not exist , invalid Serial Port - Ignoring" %PortConfig["driver"] )
        else:
            self._log.error( "%s is not a valid configuration, please check syntax" %PortConfig)       

    def configure( self , cfgDict ):
        # NOTE Here we try and initialize the configured serial wrappers,
        # if they fail to initialize they are set to None , and whenever a write command is triggered an attempt to reinitialize them is made
        #also pass the config to the baseclass configure       
        super( Serial , self ).configure( cfgDict )
        self._log.debug( 'Configure.cfgDict == %s' %cfgDict )        
        if cfgDict.has_key( "serialPorts" ):
            self._log.debug( 'Found serialPorts to configure' )
            for portConfig in cfgDict[ "serialPorts" ]:
                self.AddConnection( portConfig )
   
    def configureActions( self, cfgDict ):
        self._log.debug( "configureActions %s" %cfgDict )
        result = None
        if cfgDict.has_key( "serial" ):
            if isinstance( cfgDict[ "serial" ], list ):
                result = cfgDict[ "serial" ]
            else:
                result = list()
                result.append( cfgDict[ "serial" ]  )        
        self._log.debug( "configureActions %s" %result )
        return result
    
    def WriteSerial( self, SerialC , Bytes ):
        if SerialC.SerialPort != None:
            try:
                for byte in Bytes:
                    SerialC.SerialPort.write(chr(byte))            
            except Exception ,e :
                self._log.error(e)
                SerialC.SerialPort = None 
        else:
            self._log.error("SerialC.SerialPort is None!")
            self._wrapperReactor.removeWrapper(SerialC.Id)
            self.AddConnection(SerialC.Config)
            
                            
                
    def DoCommand( self , command ):
        if (command["cmd"] == "send") & command.has_key( "id" ) & command.has_key( "action" ):
            if self._serialPorts.has_key( command['id'] ):
                serialC = self._serialPorts[ command['id'] ]                
                message = serialC.Driver.GetCommand( command[ 'action' ] , command )                
                bytes = serialC.ProtocolHandler.Encode( message )
                self._log.debug( 'Writing %s to serial' %bytes )            
                self.WriteSerial( serialC , bytes )                
            else:
                self._log.error( '%s is not a configured port cannot execute command' %command[ 'id' ] )            
        elif ( command["cmd"] == "NewConnection" ):
                 self.AddConnection(command)                   
        else:
            self._log.error("Unrecognized command: %s" %command)
            
    def doActions( self, actions, inEvent ):
        if actions:
            for action in actions:
                self._log.debug( "Action to execute, action: %s" % action )
                self._log.debug( "Incoming Event, inEvent: %s" % inEvent )
                incomingPayload = inEvent.getPayload()
                self._log.debug( "Payload of inEvent: %s" % incomingPayload )
                #check if the incoming event has a data  payload , if it does we override whatever we have configured
                if (incomingPayload != {}):
                    if incomingPayload.has_key( "cmd" ):
                        self.DoCommand( incomingPayload )
                    else:
                        self._log.error( "Error , payload exists but is invalid check syntax : %s " %inEvent ) 
                  #if the incoming event has no data payload we use the default payload defined in the initial configuration
                elif action.has_key( "cmd" ):
                        if ( action["cmd"] == "send" ) & action.has_key( "action" ) & action.has_key( "id" ):
                            self.DoCommand( action )
                        else:
                            self._log.error( "Serial Action not correctly formatted, ignoring" )
    
                                                                   
    def stop(self):
        #we need to shut down the reactor and close all the serial wrappers
        if self._wrapperReactor != None:
           self._wrapperReactor.stop()
        for (portId , port) in self._serialPorts.items():
            port.SerialPort.close()
        super(Serial,self).stop()                           
                           
    #this is the wrapperReactor Callback 
    def DataReceivedCallback( self, PortId , Message ):
        decimalMessage = ''
        self._log.debug( '\nRecieved bytes %s' %Message )  
        #pass our message to the correct protocol_handler instance
        messages = self._serialPorts[ PortId ].ProtocolHandler.Decode( Message ) 
        self._log.debug("Messages is from received bytes is :%s" %str(messages))
        for message in messages:
            if message != None:
                events = self._serialPorts[ PortId ].Driver.GetEvents( message ) 
                for event in events:
                    if event.has_key("source") & event.has_key("type") & event.has_key("payload"):
                        self.sendEvent( makeNewEvent( event, '', '' , event['payload'] ) )
                    else:
                        self._log.error("Driver returned incorrectly formatted event : %s" %event)
                    
            
    def GetWrapper( self, PortConfig ):
        wrapper = None
        try:
            if PortConfig[ 'port_type' ] == 'tcp': 
                wrapper = TCPWrapper.TCPWrapper( PortConfig[ 'ipAddress' ],int( PortConfig[ 'port' ] ) )                            
                
            #local type (connected via serial cable)                                                         
            elif PortConfig[ 'port_type' ] == 'local':                                                    
                wrapper = SerialWrapper.SerialWrapper( PortConfig[ 'uDevID' ] , PortConfig[ 'baudRate' ]  )                            
                   
        except Exception,exception:
            self._log.error( "Problem while initializing serial wrapper : %s" %exception )
        return wrapper   
        
    def GetDriver( self, DriverName , Id):
        if DriverName == "NAD5":
            return NADDriver.NADDriver(Id)
        elif DriverName == "Dusky":
            return DuskyDriver.DuskyDriver(Id)
        elif DriverName == "Sky":
            return SkyDriver.SkyDriver(Id)    
        elif DriverName == "Lutron":
            return LutronDriver.LutronLightDriver(Id)            
        elif DriverName == "Raw":
            return RawDriver
        elif DriverName == "TestDriver":
            return DummyDriver.DummyDriver()
        return None
            
    def GetProtocolHandler( self,  ProtocolName ):
        if ProtocolName == "NAD5":
            return NADDriver.NADProtocolHandler()
        elif ProtocolName == "Lutron":
            return LutronDriver.LutronProtocolHandler()
        elif ProtocolName == "Sky":
            return SkyDriver.SkyProtocolHandler()
        elif ProtocolName == "Dusky":
            return DuskyDriver.DuskyProtocolHandler()
        elif ProtocolName == "TestPHandler":
            return DummyDriver.DummyProtocolHandler()
        else:
            return None
            
    def isValidTCPCFG( self , portCFG ):
        if portCFG.has_key( "port_type" ):
            if (portCFG["port_type"] == "tcp") & portCFG.has_key( "ipAddress" ) & portCFG.has_key( "port" ) & portCFG.has_key( "id" ) :
                return True
        return False
        
    def isValidLocalCFG(self , portCFG ):
        if portCFG.has_key( "port_type" ):
            if (portCFG["port_type"] == "local") & portCFG.has_key( "uDevID" ) & portCFG.has_key( "baudRate" ) & portCFG.has_key( "id" ):
                return True                
        return False
                                  
    def getSerialPorts(self):
        return self._serialPorts        
            
                       
    
    
               
               
               
               
