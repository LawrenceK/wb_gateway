# $Id: RgbLedLighting.py 2748 2008-09-16 11:46:38Z lawrence.klyne $
#
#  Class to sending events after a delay
#
#  Lawrence Klyne
#
#
import logging, Queue, threading, time
import copy
from Queue import Queue
import serial

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

_log = logging.getLogger( "EventHandlers.RgbLedLighting" )


# Command codes as a result of IR remote control.
CMD_ON = 0x1c
CMD_OFF = 0x15
CMD_TOGGLE = 0x12

# The four programs
CMD_FLASH = 0x11
CMD_STROBE = 0x0f
CMD_FADE = 0x13
CMD_SMOOTH = 0x10

# part of smooth or fade
CMD_RGB = 0x3d # then 4 bytes. 3 bytes for brightness of each LED colour and 1 byte checksum

CMD_BRIGHT_LEVEL1 = 0x1a
CMD_BRIGHT_LEVEL2 = 0x1e
CMD_BRIGHT_LEVEL3 = 0x1b
CMD_BRIGHT_LEVEL4 = 0x1f

CMD_RED1 = 0x01
CMD_RED2 = 0x04
CMD_RED3 = 0x07
CMD_RED4 = 0x0a
CMD_RED5 = 0x0d
CMD_GREEN1 = 0x02
CMD_GREEN2 = 0x05
CMD_GREEN3 = 0x08
CMD_GREEN4 = 0x0b # query or is it 0?
CMD_GREEN5 = 0x0e
CMD_BLUE1 = 0x03
CMD_BLUE2 = 0x06
CMD_BLUE3 = 0x09
CMD_BLUE4 = 0x17
CMD_BLUE5 = 0x1d
CMD_WHITE = 0x19

CMD_LOCK = 0x16
CMD_UNLOCK = 0x14
CMD_SETUP = 0x18
CMD_CANCEL = 0x0D

# Give all the commands a text name that can be looked up.
CMD_LOOKUP = {
        "on": CMD_ON,
        "off": CMD_OFF,
        "toggle": CMD_TOGGLE,
        "flash": CMD_FLASH,
        "strobe": CMD_STROBE,
        "fade": CMD_FADE,
        "smooth": CMD_SMOOTH,
        "bright1": CMD_BRIGHT_LEVEL1,
        "bright2": CMD_BRIGHT_LEVEL2,
        "bright3": CMD_BRIGHT_LEVEL3,
        "bright4": CMD_BRIGHT_LEVEL4,
        "red1": CMD_RED1,
        "red2": CMD_RED2,
        "red3": CMD_RED3,
        "red4": CMD_RED4,
        "red5": CMD_RED5,
        "green1": CMD_GREEN1,
        "green2": CMD_GREEN2,
        "green3": CMD_GREEN3,
        "green4": CMD_GREEN4,
        "green5": CMD_GREEN5,
        "blue1": CMD_BLUE1,
        "blue2": CMD_BLUE2,
        "blue3": CMD_BLUE3,
        "blue4": CMD_BLUE4,
        "blue5": CMD_BLUE5,
        "white": CMD_WHITE,

        "lock": CMD_LOCK,
        "unlock": CMD_UNLOCK,
        "setup": CMD_SETUP,
        "cancel": CMD_CANCEL,
    }

class LedLightingDriver:
    """
    Handle LedLighting serial protocol.
    """
    def __init__( self, portName ):
        """
        pass in com port to use.
        """
        self._portName = portName
        try:
            # is it a numeric string?
            self._portName = int(self._portName)
        except Exception:
            pass

    def open(self):
        try:
            self._port = serial.Serial( port=self._portName, baudrate=57600, timeout=1 )
        except Exception, ex:
            self._port = None
            _log.exception( ex )

    def close(self):
        if self._port:
            self._port.close()
            self._port = None

    def sendPacket( self, data ):
        """
        """
        # validate address and cmd code.
        _log.debug( "data - %s" % ( data ) )
        csum = 0x7f
        self._port.write( chr(0xAA) )
        self._port.write( chr(0x7F) )
        if ( data ):
            for b in data:
                csum = csum + b
                self._port.write( chr(b) )
        csum = csum % 128
        _log.debug( "%u" % ( csum ) )
        self._port.write( chr(csum) )

    def sendCommand( self, cmd ):
        """
        """
        csum = (0x7f + cmd) %128
        _log.debug( "data - %x, csum %x" % ( cmd, csum ) )
        self._port.write( chr(0xAA) )
        self._port.write( chr(0x7F) )
        self._port.write( chr(cmd) )
        self._port.write( chr(csum) )

    def sendRGB( self, r, g, b ):
        self.sendPacket( [CMD_RGB, r, g, b] )

    def readByte( self ):
        """
        attempt to retrive a heatmiser data transmission
        return (cmd,data) or None
        """
        s = self._port.read()
        if len(s) > 0 :
            return ord(s)
        # should throw no Data exception
        return None

    def readPacket( self ):
        result = []
        b = self.readByte()
        while b <> None and b <> 0xAA:
            result.append(b)
            b = self.readByte()
        return result

#
# Led Lighting event interface
#
class RgbLedLighting( BaseHandler, threading.Thread ):
    """
    
    """

    def __init__ (self, localRouter):
        threading.Thread.__init__(self)
        self.setDaemon( True ) # when main thread exits stop server as well

        self._log = _log    # so BaseHandler uses correct logger,
        self._taskList = Queue()
        BaseHandler.__init__(self, localRouter)

    def start(self):
        BaseHandler.start(self)
        threading.Thread.start(self)
        self._LedLightingDriver.open()
        self._taskList.put( ("start",) )

    def stop(self):
        self._taskList.put( ("quit",) )
        self._LedLightingDriver.close()
        BaseHandler.stop(self)

    def doAddLedLighting(self, hmCfg ):
        """
        read LedLighting configuration and create correct object and add to dictionary.
        """
        _log.debug( "Create LedLighting %s" % hmCfg )
        newHm = LedLighting( self, self._LedLightingDriver, hmCfg )
        self._LedLightings[ newHm._name] = newHm

    def configure( self, cfgDict ):
        self._portName = cfgDict["serialPort"]

        BaseHandler.configure( self, cfgDict )
        self._LedLightingDriver = LedLightingDriver( self._portName )

    def createAction( self, cfgAction ):
        # an action is the keyword "rgb" and the 3 levels.
        if cfgAction.has_key("task"):
            tsk = cfgAction["task"]
            if tsk == "rgb":
                if cfgAction.has_key("red") and cfgAction.has_key("green") and cfgAction.has_key("blue"):
                    return ( tsk, int(cfgAction["red"]), int(cfgAction["green"]), int(cfgAction["blue"]) )
                else:
                    _log.error("Missing red, green or blue parameter in %s" % (tsk,cfgAction) )
            elif tsk == "command":
                if cfgAction.has_key("command") and CMD_LOOKUP.has_key(cfgAction["command"]):
                    return ( tsk, cfgAction["command"] )
                else:
                    _log.error("Missing or invalid command in %s" % (cfgAction) )
            elif tsk == "on" or tsk == "off":
                return ( tsk,  )  # single entry tuple
            else:
                # unknown task at present
                _log.error("Unrecognised command %s in %s" % (tsk,cfgAction) )
        else:
            _log.error("Missing task entry in %s" % (cfgAction) )
            
        return None

    def configureActions( self, cfgDict ):
        result = list()
        if cfgDict.has_key("action"):
            if isinstance( cfgDict["action"], list ):
                for action in cfgDict["action"]:
                    task = self.createAction(action)
                    if task:
                        result.append(task)
                    else:
                        _log.error("Configuration %s does not create task" % (action) )
            else:
                task = self.createAction(cfgDict["action"])
                if task:
                    result.append(task)
                else:
                    _log.error("Configuration %s does not create task" % (cfgDict["action"]) )
        _log.debug("configureActions %s" % (result) )
        return result

    def doActions( self, tasks, inEvent ):
        if tasks:
            for task in tasks:
                _log.debug( "doAction %s", task )
                if task:
                    self._taskList.put( task )
                else:
                    _log.error( 'No task, check configuration' )

    def run(self):
        _log.debug( 'enter run' )
        while self.alive():
            try:
                task = self._taskList.get( True )
                _log.debug( 'Task %s' % (str(task[0])) )
                if task[0] == "rgb" :
                    self._LedLightingDriver.sendRGB( task[1], task[2], task[3] )
                elif task[0] == "quit" :
                    break;  # while loop
                elif task[0] == "start" :
                    #self._LedLightingDriver.sendCommand( CMD_ON )
                    pass
                elif task[0] == "on" :
                    self._LedLightingDriver.sendCommand( CMD_ON )
                elif task[0] == "off" :
                    self._LedLightingDriver.sendCommand( CMD_OFF )
                elif task[0] == "command" :
                    self._LedLightingDriver.sendCommand( CMD_LOOKUP[task[1]] )
                else:
                    _log.error( 'Unrecognised task %s in %s' % (task[0], task) )

            except Exception, ex:
                _log.exception( ex )

        _log.debug( 'exit run' )
