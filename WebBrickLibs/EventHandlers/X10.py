#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import logging, threading, time

from Queue import Queue, Empty

import serial

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

#import logging, string, threading, time


_log = logging.getLogger( "EventHandlers.X10" )

# index by house code - 'A' or device code 0-15
# Note 0 based and not 1 based as in X10 spec.
_codeTable = [
    6,
    14,
    2,
    10,
    1,
    9,
    5,
    13,
    7,
    15,
    3,
    11,
    0,
    8,
    4,
    12
    ]

# reverse of _codeTable
_indexTable = [
    12, # M
    4,  # E
    2,  # C
    10, # K
    14, # O
    6,  # G
    0,  # A
    8,  # I
    13, # N
    5,  # F
    3,  # D
    11, # L
    15, # P
    7,  # H
    1,  # B
    9,  # J
    ]

X10_ALL_OFF = 0
X10_ALL_ON = 1
X10_SWITCH_ON = 2
X10_SWITCH_OFF = 3
X10_DIM = 4
X10_BRIGHT = 5
X10_ALL_LIGHTS_OFF = 6
X10_EXTENDED_CODE = 7
X10_HAIL_REQUEST = 8
X10_HAIL_ACK = 9
X10_PRESET_DIM_1 = 10
X10_PRESET_DIM_2 = 11
X10_EXT_DATA_TRANSFER = 12
X10_STATUS_ON = 13
X10_STATUS_OFF = 14
X10_STATUS_REQUEST = 15

def houseCode( ch ):
    return _codeTable[ord(ch)-ord('A')] 

def deviceCode( dev ):
    return _codeTable[int(dev)-1] 

def houseName( id ):
    return chr(_indexTable[id] + ord('A'))

def deviceId( id ):
    return _indexTable[id]+1

class X10Handler( BaseHandler, threading.Thread ):
    """
    Listen for X10 FASTAGI requests and turn into appropriate events.
    """

    def __init__ (self, localRouter, wfile = None, rfile = None ):
        # rfile and wfile are allowed mainly for testing purposes.
        self._log = _log    # so BaseHandler uses correct logger,
        threading.Thread.__init__(self)
        BaseHandler.__init__(self, localRouter)
        self.setDaemon( True ) # when main thread exits stop server as well
        self.running = False
        self._inFile = rfile
        self._outFile = wfile
        if rfile:
            _log.debug( "rFile %s " % (rfile.getvalue()) )
        if wfile:
            _log.debug( "wFile %s " % (wfile.getvalue()) )
        self.serialPort = "com1"
        self._taskList = Queue()
        self._csum = 0  # current checksum being calculated
        self.rxHouseCode = None
        self.rxDeviceCodes = None

    def configure( self, cfgDict ):
        """
        called with an XmlDom that contains the configuration for self
        """
        if cfgDict.has_key('serialPort'):
            self.serialPort = cfgDict['serialPort']
        _log.debug( "serialPort %s" % self.serialPort )
        BaseHandler.configure( self, cfgDict )

    def verifyActionAddress( self, cfgDict ):
        if cfgDict.has_key("house") and cfgDict.has_key("device"):
            if cfgDict["house"] >= 'A' and cfgDict["house"] <= 'P':
                idev = int(cfgDict["device"])
                if idev >= 0 and idev <= 15:
                    return True

        # log faulty
        _log.error("verifyActionAddress invalid X10 address %s" % (cfgDict) )
        return False

    def verifyActionLevel( self, cfgDict ):
        if cfgDict.has_key("level"):
            ilev = int(cfgDict["level"])
            if (ilev >= 0 ) and (ilev <= 22 ):
                return True
        # log faulty
        _log.error("verifyActionLevel invalid X10 level %s" % (cfgDict) )
        return False

    def configureActions( self, cfgDict ):
        result = list()
        if cfgDict.has_key("channelOn"):
            if isinstance( cfgDict["channelOn"], list ):
                for action in cfgDict["channelOn"]:
                    if self.verifyActionAddress(action):
                        result.append( ("channelOn", action) )
            else:
                if self.verifyActionAddress(cfgDict["channelOn"]):
                    result.append( ("channelOn", cfgDict["channelOn"]) )

        if cfgDict.has_key("channelOff"):
            if isinstance( cfgDict["channelOff"], list ):
                for action in cfgDict["channelOff"]:
                    if self.verifyActionAddress(action):
                        result.append( ("channelOff", action) )
            else:
                if self.verifyActionAddress(cfgDict["channelOff"]):
                    result.append( ("channelOff", cfgDict["channelOff"]) )

        if cfgDict.has_key("channelDim"):
            if isinstance( cfgDict["channelDim"], list ):
                for action in cfgDict["channelDim"]:
                    if self.verifyActionAddress(action) and self.verifyActionLevel(action):
                        result.append( ("channelDim", action) )
            else:
                if self.verifyActionAddress(cfgDict["channelDim"]) and self.verifyActionLevel(cfgDict["channelDim"]):
                    result.append( ("channelDim", cfgDict["channelDim"]) )
        _log.debug("configureActions %s" % (result) )
        return result

    # Terminate interface
    def stop(self):
        _log.debug( 'stop' )
        self.running = False
        self._taskList.put( ("stop",) )
        BaseHandler.stop(self)

    def alive(self):
        return self.running

    def start(self):
        _log.debug( 'start' )
        BaseHandler.start(self)
        self.running = True
        if not self._inFile or not self._outFile:
            # open serial port
            try:
                self._inFile = serial.Serial( port=self.serialPort, baudrate=4800, timeout=1 )
                self._outFile = self._inFile
            except Exception, ex:
                self._inFile = None
                _log.exception( ex )
        else:
            self.serialPort = None
        threading.Thread.start( self )
        self._taskList.put( ("start",) )

    def doActions( self, tasks, inEvent ):
        if tasks:
            for task in tasks:
                _log.debug( "doAction %s", task )
                self._taskList.put( task )

    def sendAddressHeaderCode( self, dim = 0):
        self._csum = (dim*8) + 4
        self.writeByte( self._csum )

    def sendAddress( self, task ):
        _log.debug( "house %s:%u device %s:%u" % (task["house"], houseCode(task["house"]), task["device"], deviceCode(task["device"]) ) )
        adr = (houseCode(task["house"])*16) + deviceCode(task["device"])
        self._csum = (self._csum + adr)% 256
        self.writeByte( adr )

    def sendFunctionHeaderCode( self, dim = 0):
        self._csum = (dim*8) + 6
        self.writeByte( self._csum )

    def sendFunction( self, task, fcode ):
        cod = (houseCode(task["house"])*16) + fcode
        self._csum = (self._csum + cod)% 256
        self.writeByte( cod )

    def writeByte( self, bt ):
        _log.debug( "writeByte %x " % (bt) )
        if self._outFile:
            self._outFile.write( chr(bt) )

    def readByte( self ):
        bt = None
        if self._inFile:
            s = self._inFile.read(1)
            if len(s) > 0 :
                bt = ord( s )
                _log.debug( "readByte %x " % (bt) )
        return bt

    def readByteRetry( self, wait = 0.1, retryCount = 10 ):
        # retried byte read
        for i in range(0,60):
            db = self.readByte()
            if db != None:
                return db
            time.sleep(1)

    def readCSum( self ):
        # retry checksum read
        for i in range(0,10):
            cs = self.readByte()
            if cs != None:
                return cs
            #return self.readByte()

    def readAck( self ):
        # retry ack read
        for i in range(0,60):
            ak = self.readByte()
            if ak != None:
                return ak
            time.sleep(1)

    def sendAddressSeq( self, task ):
        # a task consists of house and device id.
        if task:
#            if task.has_key("level"):
#                self.sendAddressHeaderCode( int(task["level"]))
#            else:
#                self.sendAddressHeaderCode()
            self.sendAddressHeaderCode( )
            self.sendAddress( task )
            cs = self.readCSum()
            if cs == self._csum:
                self.writeByte( 0 )
                ack = self.readAck()
                if ack == 0x55:
                    return True
                else:
                    _log.error( "received ack is not 0x55, Rx%s", ack )
            else:
                _log.error( "received checksum is not correct, Rx=%s, Expected=%s" % (cs,self._csum) )
        return False

    def sendFunctionSeq( self, task, fcode ):
        # a task consists of house and device id.
        if task:
            if task.has_key("level"):
                self.sendFunctionHeaderCode( int(task["level"]))
            else:
                self.sendFunctionHeaderCode()
            self.sendFunction( task, fcode )
            cs = self.readCSum()
            if cs == self._csum:
                self.writeByte( 0 )
                ack = self.readAck()
                if ack == 0x55:
                    return True
                else:
                    _log.error( "received ack is not 0x55, Rx%s", ack )
            else:
                _log.error( "received checksum is not correct, Rx=%s, Expected=%s" % (cs,self._csum) )
        return False

    def doChannelOn( self, task ):
        # a task consists of house and device id.
        if task:
            _log.debug( "doChannelOn %s", task )
            if self.sendAddressSeq( task ) and self.sendFunctionSeq( task, X10_SWITCH_ON ):
                pass

    def doChannelOff( self, task ):
        # a task consists of house and device id.
        if task:
            _log.debug( "doChannelOff %s", task )
            if self.sendAddressSeq( task ) and self.sendFunctionSeq( task, X10_SWITCH_OFF ):
                pass

    def doChannelDim( self, task ):
        # a task consists of house and device id and a level
        if task:
            _log.debug( "doChannelDim %s", task )
            if task.has_key("up"):
                if self.sendAddressSeq( task ) and self.sendFunctionSeq( task, X10_BRIGHT ):
                    pass
            else:
                if self.sendAddressSeq( task ) and self.sendFunctionSeq( task, X10_DIM ):
                    pass

    def doDownloadMacros( self ):
        _log.debug( "doDownloadMacros" )
        self.writeByte( 0xfb )  # macro start
        for i in range(42):
            self.writeByte( 0 )  # empty table for now
        cs = self.readCSum()
        if cs == 0:
            self.writeByte( 0 )  # checksum acknowledged
            ack = self.readAck()
            if ack == 0x55:
                return True
        return False

    def doSetClock( self ):
        _log.debug( "doSetClock" )
        self.writeByte( 0x9b )  # macro start
        for i in range(6):
            self.writeByte( 0 )  # clear all for now
        cs = self.readCSum()
        if cs == 0:
            self.writeByte( 0 )  # checksum acknowledged
            ack = self.readAck()
            if ack == 0x55:
                return True
        return False

    def doX10Receive( self ):
        _log.debug( "doX10Receive" )
        self.writeByte( 0xc3 )  # macro start
        # read byte length
        len = self.readByteRetry( self )
        # now read the bytes in
        if len:
            funcAddMask = self.readByteRetry( self )    # mask of whether a later byte is fuinction or address
            rxData = list()
            for i in range(len-1):  # Data Byte up to 8.
                rxData.append( self.readByteRetry( self ) )
            # log it.
            # decode it.
            # TODO handle DIM and BRIGHT as there is an extra data byte.
            i = 0
            while i < (len-1):
                house = houseName(rxData[i] >> 4)
                id = (rxData[i] & 0x0f)
                if (funcAddMask & (0x01 << i)) == 0:
                    # address byte
                    devCode = deviceId(id)
                    _log.debug( "X10 received house - %s devCode - %i" % (house,devCode) )
                    if self.rxHouseCode != house:
                        self.rxHouseCode = house
                        self.rxDeviceCodes = list() # reset device list
                    self.rxDeviceCodes.append(devCode)
                    _log.debug( "X10 received house - %s devCodes - %s" % (self.rxHouseCode,self.rxDeviceCodes) )
                else:
                    # function byte.
                    # TODO handle DIM and BRIGHT as there is an extra data byte.
                    func = id
                    odata = {'command':func}
                    if func == X10_DIM or func == X10_BRIGHT:
                        # next byte is dim/bright step
                        i = i + 1
                        odata['dim'] = rxData[i]
                    elif func == X10_EXTENDED_CODE:
                        i = i + 1
                        odata['data'] = rxData[i]
                        i = i + 1
                        odata['xcommand'] = rxData[i]

                    _log.debug( "X10 received house - %s function - %s" % (house,odata) )
                    _log.debug( "X10 received house - %s devCodes - %s" % (self.rxHouseCode,self.rxDeviceCodes) )
                    if self.rxHouseCode == None:
                        # command applies to all devices in house code
                        self.sendEvent( Event('http://id.webbrick.co.uk/events/X10',
                            'X10/%s' %(house), 
                            odata ) )
                    elif self.rxHouseCode == house:
                        for dev in self.rxDeviceCodes:
                            # send events
                            self.sendEvent( Event('http://id.webbrick.co.uk/events/X10',
                                'X10/%s/%s' %(house,dev), 
                                odata ) )
                    else:
                        # invalid change of house code.
                        _log.error( "received function house code (%s) does not match address house code (%s)" % (house,self.rxHouseCode) )

                    # now does this reset the address list?
                    # assume yes.
                    self.rxHouseCode = None
                    self.rxDeviceCodes = None
                i = i + 1

    def doCheckX10Notify( self ):
        # read all un requested data from X10.
        b = self.readByte()
        while b != None:
            _log.debug( "doCheckX10Notify %x" % b )
            if b == 0xa5:
                # power fail
                if self.doSetClock():
                    if self.doDownloadMacros():
                        _log.debug( "PowerFail Ok" )
                    else:
                        _log.error( "PowerFail Error" )
                else:
                    _log.error( "SetClock Error" )
            elif b == 0x5a: # X10 reception
                # incoming.
                self.doX10Receive()
            b = self.readByte()

    def run(self):
        _log.debug( 'enter run' )
        while self.alive():
            try:
                task = self._taskList.get( True, 0.1 )
                if task[0] == "channelOn" :
                    self.doChannelOn( task[1] )
                elif task[0] == "channelOff" :
                    self.doChannelOff( task[1] )
                elif task[0] == "channelDim" :
                    self.doChannelDim( task[1] )
                else:
                    # unrecognised
                    pass

            except Empty, ex:
                # look for data from X10
                self.doCheckX10Notify()

            except Exception, ex:
                _log.exception( ex )

        if self.serialPort:
            self._outFile.close()
            self.serialPort = None

        _log.debug( 'exit run' )
