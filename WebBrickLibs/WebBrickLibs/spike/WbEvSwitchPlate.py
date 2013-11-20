# $Id: WbEvSwitchPlate.py 2612 2008-08-11 20:08:49Z graham.klyne $
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

from WbEvent import WbEventOther
from WbEvBaseAction import WbEvBaseAction

_log = logging.getLogger( "EventDespatch.WbEvSwitchPlate" )

# if top bit set then this is address
ADR_ISADDRESS   = 0x80

ADR_DIRECTION_MASK   = 0x40
ADR_DIR_FROM_HOST   = 0x0
ADR_DIR_FROM_CLIENT   = 0x40
ADR_ADDRESS_MASK   = 0x3F

CMD_GROUP_MASK = 0x60
CMD_GROUP_DEVICE = 0x0
CMD_GROUP_UNIT = 0x20
CMD_GROUP_RESERVED1 = 0x40
CMD_GROUP_RESERVED2 = 0x60

CMD_DEVICE_CMD_MASK = 0x7F
CMD_UNIT_CMD_MASK = 0x78
CMD_UNIT_NR_MASK = 0x07

CMD_SET_ADDRESS = CMD_GROUP_DEVICE + 0
CMD_SET_RE_DELAY = CMD_GROUP_DEVICE + 1
CMD_SET_FADE_RATE = CMD_GROUP_DEVICE + 2

CMD_MIMIC = CMD_GROUP_UNIT + 0x00
CMD_SET_BUTTON = CMD_GROUP_UNIT + 0x08
CMD_INPUT_TRG = CMD_GROUP_UNIT + 0x10
CMD_RE_MOVE = CMD_GROUP_UNIT + 0x18

class SwitchPlateDriver:
    """
    Handle Switch Plate serial protocol.
    """
    def __init__( self, portName ):
        """
        pass in com port to use.
        """
        self._portName = int(portName)

    def open(self):
        try:
            _log.debug( "Open - %s" % ( self._portName ) )
            self._port = serial.Serial( port=self._portName, baudrate=19200, timeout=0.1 )
        except Exception, ex:
            self._port = None
            _log.exception( ex )

    def close(self):
        if self._port:
            self._port.close()
            self._port = None

    def sendPacket( self, b1,b2,b3 ):
        """
        """
        # validate address and cmd code.
        csum = 0x80 ^ b1 ^ b2 ^ b3
        _log.debug( "data - %x %x %x %x" % ( b1,b2,b3,csum ) )
        self._port.write( chr(b1) )
        self._port.write( chr(b2) )
        self._port.write( chr(b3) )
        self._port.write( chr(csum) )

    def doDevCommand( self, adr, command, value ):
        """
        """
        self.sendPacket( 0x80|adr, command|channel, value&0x7F)

    def doUnitCommand( self, adr, command, channel, value ):
        """
        """
        self.sendPacket( 0x80|adr, command|channel, value&0x7F)

    def doMimic( self, adr, channel, level ):
        """
        """
        self.doUnitCommand( adr, CMD_MIMIC, channel, level )

    def readByte( self ):
        """
        attempt to retrive a switch plate
        return (cmd,data) or None
        """
        s = self._port.read()
        if len(s) > 0 :
            _log.debug( "RxByte - %x" % ( ord(s) ) )
            return ord(s)
        # should throw no Data exception
        return None

    def readPacket( self ):
        result = None
        b1 = self.readByte()
        if b1 and ( (b1 & ADR_ISADDRESS) == ADR_ISADDRESS):
            b2 = self.readByte()
            if b2:
                b3 = self.readByte()
                if b3:
                    b4 = self.readByte()
                    if b4 and ( (0x80^b1 ^b2 ^b3) == b4 ):
                        # verify checksum
                        result = ( b1, b2 ,b3 )
                        # generate xxx
        return result

#
# Led Lighting event interface
#
class WbEvSwitchPlate( WbEvBaseAction, threading.Thread ):
    """
    
    """

    def __init__ (self, despatch):
        threading.Thread.__init__(self)
        self.setDaemon( True ) # when main thread exits stop server as well

        self._log = _log    # so WbEvBaseAction uses correct logger,
        self._taskList = Queue()
        WbEvBaseAction.__init__(self, despatch)

    def start(self):
        WbEvBaseAction.start(self)
        self._SwitchPlateDriver.open()
        threading.Thread.start(self)
        self._taskList.put( ("start",) )

    def stop(self):
        self._taskList.put( ("quit",) )
        self._SwitchPlateDriver.close()
        WbEvBaseAction.stop(self)

    def configure( self, cfgDict ):
        self._portName = cfgDict["serialPort"]
        self._SwitchPlateDriver = SwitchPlateDriver( self._portName )

        WbEvBaseAction.configure( self, cfgDict )

    def createAction( self, cfgAction ):
        # an action is the keyword "rgb" and the 3 levels.
        if cfgAction.has_key("mimic"):
            return ( "mimic", int(cfgAction["adr"]), int(cfgAction["mimic"]), int(cfgAction["level"]) )
        return None

    def configureActions( self, cfgDict ):
        result = list()
        if cfgDict.has_key("action"):
            if isinstance( cfgDict["action"], list ):
                for action in cfgDict["action"]:
                    result.append(self.createAction(action))
            else:
                result.append(self.createAction(cfgDict["action"]))
        _log.debug("configureActions %s" % (result) )
        return result

    def doActions( self, tasks, inEvent ):
        if tasks:
            for task in tasks:
                _log.debug( "doAction %s", task )
                self._taskList.put( task )

    def decodeCmd( self, pkt ):
        # decode
        _log.debug( "Rx command - %x %x %x" % ( pkt[0], pkt[1], pkt[2] ) )
        adr = pkt[0] & ADR_ADDRESS_MASK
        grp = pkt[1] & CMD_GROUP_MASK
        if grp == CMD_GROUP_DEVICE:
            cmd = pkt[1] & CMD_DEVICE_CMD_MASK
            # no device commands expected
            #CMD_SET_ADDRESS = CMD_GROUP_DEVICE + 0
            #CMD_SET_RE_DELAY = CMD_GROUP_DEVICE + 1
            #CMD_SET_FADE_RATE = CMD_GROUP_DEVICE + 2
            _log.error( "Unexpected device command - %x %x %x" % ( pkt[0], pkt[1], pkt[2] ) )
            
        elif grp == CMD_GROUP_UNIT:
            cmd = pkt[1] & CMD_UNIT_CMD_MASK
            unit = pkt[1] & CMD_UNIT_NR_MASK
            if cmd == CMD_INPUT_TRG:
                # generate event
                self.sendEvent( WbEventOther( "http://id.webbrick.co.uk/events/switchplate/DI", "switchplate/%s/DI/%s" % (adr, unit) ) )
            elif cmd == CMD_RE_MOVE:
                # generate event
                self.sendEvent( WbEventOther( "http://id.webbrick.co.uk/events/switchplate/RE", "switchplate/%s/RE/%s" % (adr, unit), {'count':pkt[2]} ) )
                pass
            else:
                _log.error( "Unexpected unit command - %x %x %x" % ( pkt[0], pkt[1], pkt[2] ) )
            #CMD_MIMIC = CMD_GROUP_UNIT + 0x00
            #CMD_SET_BUTTON = CMD_GROUP_UNIT + 0x08
        else:
            # reserved
            _log.error( "Unrecognised command - %x %x %x" % ( pkt[0], pkt[1], pkt[2] ) )

    def run(self):
        _log.debug( 'enter run' )
        while self.alive():
            try:
                pkt = self._SwitchPlateDriver.readPacket()
                if pkt:
                    self.decodeCmd(pkt)
                if not self._taskList.empty():
                    task = self._taskList.get( False )
                    _log.debug( 'Task %s' % (str(task[0])) )
                    if task[0] == "mimic" :
                        self._SwitchPlateDriver.doMimic( task[1], task[2], task[3] )
                    elif task[0] == "quit" :
                        break;  # while loop
                    elif task[0] == "start" :
                        #self._SwitchPlateDriver.sendCommand( CMD_ON )
                        pass

            except Exception, ex:
                _log.exception( ex )

        _log.debug( 'exit run' )
