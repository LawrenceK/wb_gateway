# $Id: Heatmiser.py 2748 2008-09-16 11:46:38Z lawrence.klyne $
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

_log = logging.getLogger("EventHandlers.HeatMiser")


"""
command                     DT-N        PRT-N
--------------------------------------------------------------------------------------------
CMD_SET_ADDRESS         |           |
CMD_GET_STATE           |   ?       | Y
CMD_SET_STATE           |           |
CMD_GET_TEMP            |   N       | N
CMD_SET_TEMP            |           |

CMD_GET_FROST_TEMP      |   N       | N
CMD_SET_FROST_TEMP      |           |
CMD_SET_MANUAL_HW       |           |
CMD_SET_FROST_ENABLE    |           |
CMD_SET_ALL_KEYLOCKED   |           |
CMD_SET_TEMP_CAL        |           |
CMD_SET_FROST_STATE     |           |

CMD_GET_CURRENT         |           |

CMD_GET_HEAT_WEEK_C_SET |   Y(1)    | Y
CMD_SET_HEAT_WEEK_C_SET |           |
CMD_GET_HEAT_WEND_C_SET |           |
CMD_SET_HEAT_WEND_C_SET |           |

CMD_GET_HW_WEEK_SET     |           |
CMD_SET_HW_WEEK_SET     |           |
CMD_GET_HW_WEND_SET     |           |
CMD_SET_HW_WEND_SET     |           |

CMD_GET_HEAT_WEEK_F_SET |           |
CMD_SET_HEAT_WEEK_F_SET |           |
CMD_GET_HEAT_WEND_F_SET |           |
CMD_SET_HEAT_WEND_F_SET |           |

CMD_GET_PARAM           |   Y       | Y
CMD_SET_PARAM           |           |
CMD_GET_PARAMHW         |           |
CMD_SET_PARAMHW         |           |

"""

CMD_SET_ADDRESS = 1
CMD_GET_STATE = 2
CMD_SET_STATE = 128 + CMD_GET_STATE
CMD_GET_TEMP = 4    # invalid as write only.
CMD_SET_TEMP = 128 + CMD_GET_TEMP

CMD_GET_FROST_TEMP = 7
CMD_SET_FROST_TEMP = 128+CMD_GET_FROST_TEMP
CMD_SET_MANUAL_HW = 21
CMD_SET_FROST_ENABLE = 25
CMD_SET_ALL_KEYLOCKED = 26
CMD_SET_TEMP_CAL = 29
CMD_GET_FROST_STATE = 100
CMD_SET_FROST_STATE = 128 + CMD_GET_FROST_STATE

CMD_GET_CURRENT = 77

CMD_GET_HEAT_WEEK_C_SET = 78
CMD_SET_HEAT_WEEK_C_SET = 128+CMD_GET_HEAT_WEEK_C_SET
CMD_GET_HEAT_WEND_C_SET = 79
CMD_SET_HEAT_WEND_C_SET = 128+CMD_GET_HEAT_WEND_C_SET

CMD_GET_HW_WEEK_SET = 80
CMD_SET_HW_WEEK_SET = 128+CMD_GET_HW_WEEK_SET
CMD_GET_HW_WEND_SET = 81
CMD_SET_HW_WEND_SET = 128+CMD_GET_HW_WEND_SET

CMD_GET_HEAT_WEEK_F_SET = 82
CMD_SET_HEAT_WEEK_F_SET = 128+CMD_GET_HEAT_WEEK_F_SET
CMD_GET_HEAT_WEND_F_SET = 83
CMD_SET_HEAT_WEND_F_SET = 128+CMD_GET_HEAT_WEND_F_SET

CMD_GET_PARAM = 38
CMD_SET_PARAM = 128 + CMD_GET_PARAM
CMD_GET_PARAMHW = 41
CMD_SET_PARAMHW = 128 + CMD_GET_PARAMHW

MODEL_PRTN  = 81
MODEL_PRTHWN = 82
MODEL_FCVN = 83
MODEL_DTN = 85
modelMap = { MODEL_PRTN:"PRT-N", MODEL_PRTHWN:"PRTHW-N", MODEL_FCVN:"FCV-N", MODEL_DTN:"DT-N" }

PARTNR_DTN_UNKNOWN  = 0 # ???
PARTNR_DTN_WITH_FLOOR  = 1
PARTNR_DTN  = 2
PARTNR_PRTN  = 3
PARTNR_PRTN_WITH_FLOOR  = 4
PARTNR_PRTN_HC  = 5

class HeatmiserSchEntry:
    """
            <sch type="weekday" id='1' schkey='room2weekday1'>
    """
    # parameters to assit testing
    def __init__( self, hours=-1, minutes=-1, setPoint=-255 ):
        self._hours = hours
        self._minutes = minutes
        self._setPoint = setPoint

    def diffTime(self, hrs, mins):
        """
        # returns True if update data is different from self.
        """
        return hrs != self._hours or mins != self._minutes

    def diffSetPoint(self, sp):
        """
        # returns True if update data is different from self.
        """
        return sp != self._setPoint

    def updateTime(self, hrs, mins):
        """
        # returns True if update data is different from self.
        """
        _log.debug( " updateTime %s %s -> %s %s" % (self._hours, self._minutes, hrs, mins) )
        if hrs != self._hours or mins != self._minutes:
            self._hours = hrs
            self._minutes = mins
            return True
        return False

    def updateSetPoint(self, sp):
        """
        # returns True if update data is different from self.
        """
        if sp != self._setPoint:
            self._setPoint = sp
            return True
        return False

    def __str__(self):
        return "HeatmiserSchEntry type %s:%i name %s" % ( self._type, self._idx, self._name )

class HeatmiserDriver:
    """
    Handle heatmiser serial protocol.
    """
    def __init__( self, portName ):
        """
        pass in com port to use.
        """
        self._portName = portName

    def open(self):
        try:
            self._port = serial.Serial( port=self._portName, baudrate=4800, timeout=1 )
        except Exception, ex:
            self._port = None
            _log.exception( ex )

    def close(self):
        if self._port:
            self._port.close()
            self._port = None

    def sendPacket( self, adr, cmd, data ):
        """
        turn parameters into heatmiser command packet
        """
        # validate address and cmd code.
        if self._port:
            _log.debug( "%u %u %s" % ( adr,cmd,data ) )
            csum = adr + cmd
            self._port.write( chr(adr) )
            self._port.write( chr(cmd) )
            if ( data ):
                for b in data:
                    csum = csum + b
                    self._port.write( chr(b) )
            csum = csum % 256
            _log.debug( "%u" % ( csum ) )
            self._port.write( chr(csum) )

    def readByte( self ):
        """
        attempt to retrive a heatmiser data transmission
        return (cmd,data) or None
        """
        if self._port:
            s = self._port.read()
            if len(s) > 0 :
                return ord(s)
            # should throw no Data exception
        return None

    def receivePacket( self, dataCount = 1 ):
        """
        attempt to retrive a heatmiser data transmission
        return (adr, cmd, data) or None
        """
        if self._port:
            adr = self.readByte()
            if adr:
                cmd = self.readByte()
                if cmd:
                    ccsum = adr + cmd
                    data = list()
                    for i in range( dataCount ):
                        b = self.readByte()
                        if b == None:
                            break
                        ccsum = ccsum + b
                        data.append( b )

                    rdsum = self.readByte()
                    if rdsum:
                        ccsum = ccsum % 256
                        _log.debug( "%u %u %s %u %u" % ( adr, cmd, data, rdsum, ccsum ) )
                        # verify check sum.
                        if rdsum == ccsum:
                            return ( adr, cmd, data )
                    else:
                        _log.debug( "%u %u %s %u" % ( adr, cmd, data, ccsum ) )
                else:
                    _log.debug( "%u" % ( adr ) )
        return None

    def query( self, adr, cmd, sndData, rxLen = 1 ):
        """
        send a retrieval command and read response.
        return (cmd,data) or None

        Does retries if no response
        """
        _log.debug( "query" )
        if self._port:
            rxCmd = cmd
            if cmd >= 128:
                rxCmd = cmd - 128

            for c in range(3):  # 3 attempts
                self.sendPacket( adr, cmd, sndData )
                reply = self.receivePacket( rxLen )
                if reply:
                    # verify address
                    # verify response code
                    if (reply[0] == adr) and (reply[1] == rxCmd):    # mask commmand bit.
                        return reply[2] # return result data
                _log.debug( "retry %u" % c )
                time.sleep(1)
        return None

    def getStatus( self, adr ):
        """
        return ( model, temp, setPoint, odata )
        """
        result = None
        _log.debug( "getStatus" )
        self.sendPacket( adr, CMD_GET_CURRENT, [0] )
        reply = self.receivePacket( 4 )
        if reply:
            result = dict()
            data = reply[2]
            result["model"] = data[0]
            result["modelName"] = modelMap[data[0]]
            result["roomT"] = data[1]-80
            result["setT"] = data[2]-80
            if (data[3] & 0x02) == 0:
                result["hotWater"] = "off"
            else:
                result["hotWater"] = "on"
            if (data[3] & 0x04) == 0:
                result["heating"] = "off"
            else:
                result["heating"] = "on"
        return result

    def identify( self, adr ):
        """
        return model code constant
        """
        vals = getStatus( self, adr )
        if vals:
            return vals["model"]
        return 0

    def getSwitchTime( self, adr, cmd, model ):
        """
        cmd needs to be one of.
        CMD_GET_HEAT_WEEK_C_SET, CMD_GET_HEAT_WEND_C_SET, (CMD_GET_HW_WEEK_SET, CMD_GET_HW_WEND_SET for PRTHW-N only)
        """
        assert( cmd in [CMD_GET_HEAT_WEEK_C_SET, CMD_GET_HEAT_WEND_C_SET])
        assert( model in [MODEL_PRTN,])
        result = None

        data = self.query( adr, cmd, [model], rxLen = 13 )

        if data and len(data) == 13:
            result = []
            result.append( ( data[1]-80, data[2]-80, data[3]-80 ) )
            result.append( ( data[4]-80, data[5]-80, data[6]-80 ) )
            result.append( ( data[7]-80, data[8]-80, data[9]-80 ) )
            result.append( ( data[10]-80, data[11]-80, data[12]-80 ) )
        return result

    def setSchedule( self, adr, cmd, model, schList ):
        """
        passed a list of HeatmiserSchEntry entries.
        """
        assert( cmd in [CMD_SET_HEAT_WEEK_C_SET, CMD_SET_HEAT_WEND_C_SET])
        assert( model in [MODEL_PRTN,])

        data = list()
        data.append( model )
        for ntry in schList:
            data.append( ntry._hours+80 )
            data.append( ntry._minutes+80 )
            data.append( ntry._setPoint+80 )

        data = self.query( adr, cmd, data, 1 )

# should be returning model code but is not, appears to be 3 bytes further in send data.
#        if data and data[0] == model
        if data:
            return True
        return False

    def readParameter( self, adr ):
        """
        """
        _log.debug( "readParameter" )
        result = None
        data = self.query( adr, CMD_GET_PARAM, [0], rxLen = 13 )

        if data:
            result = dict()

            result["model"] = data[0]
            result["modelName"] = modelMap[data[0]]
            result["floor"] = data[1] / 128
            result["preheat"] = (data[1] / 16) & 0x07
            result["dayOfWeek"] = data[1] & 0x0F

            result["hour"] = data[2]
            result["minute"] = data[3]
            result["roomT"] = data[4]

            result["differential"] = (data[5]/16) & 0x0F
            result["partNr"] = data[5] & 0x0F

            if (data[6] & 0x01) == 0:
                result["format"] = "C"
            else:
                result["format"] = "F"
            if (data[6] & 0x02) == 0:
                result["frostMode"] = "disabled"
            else:
                result["frostMode"] = "enabled"
            if (data[6] & 0x04) == 0:
                result["sensor"] = "internal"
            else:
                result["sensor"] = "remote"
            if (data[6] & 0x08 ) == 0:
                result["floorLimit"] = "disabled"
            else:
                result["floorLimit"] = "enabled"
            if (data[6] & 0x10) == 0:
                result["output"] = "off"
            else:
                result["output"] = "on"
            if (data[6] & 0x20) == 0:
                result["frostProt"] = "off"
            else:
                result["frostProt"] = "on"
            if (data[6] & 0x40) == 0:
                result["allKey"] = "unlocked"
            else:
                result["allKey"] = "locked"
            if (data[6] & 0x80) == 0:
                result["state"] = "off"
            else:
                result["state"] = "on"

            result["setT"] = data[7]
            result["frostT"] = data[8]
            result["delay"] = data[9]
            result["floorT"] = data[10]
            result["POC"] = data[11]
            result["floorMaxT"] = data[12]

        return result

    def writeParameter( self, adr, params ):
        """
        """
        _log.debug( "writeParameter %s" % (params) )

        data = list()
        data.append( int(params["model"]) )
        data.append( int(params["dayOfWeek"] ) )
        data.append( int(params["hour"] ) )
        data.append( int(params["minute"] ) )
        data.append( int(params["tempCal"] ) )
        #data.append( 0 )    # temp calibration
        data.append( int(params["partNr"] ) )    # part number
        data.append( int(params["differential"] ) )

        status = 0
        if params["format"] == "F":
            status = status + 1
        if params["frostMode"] == "enabled":
            status = status + 2
        if params["sensor"] == "remote":
            status = status + 4
        if params["floorLimit"] == "enabled":
            status = status + 8
        if params["frostProt"] == "on":
            status = status + 32
        if params["allKey"] == "locked":
            status = status + 64
        if params["state"] == "on":
            status = status + 128
        data.append( status )

        data.append( int(params["setT"] ) )
        data.append( int(params["frostT"] ) )
        data.append( int(params["delay"] ) )
        data.append( int(params["preheat"] ) ) # preheat

        data.append( int(params["floorMaxT"] ) )  # ??? TODO verify

#            result["POC"] = data[11]

        data = self.query( adr, CMD_SET_PARAM, data, 1 )
        if data:
            return True

        return False

    def setSetPoint( self, adr, val ):
        """
        """
        _log.debug( "setSetPoint" )
        data = self.query( adr, CMD_SET_TEMP, [val], 1 )
        if data:
            return True
        return None

class HeatmiserState:
    """
    hold heatmiser configuration and state.

        <heatmiser adr="2" devkey="room2" schname='room2'>
        </heatmiser>

    """
    def __init__( self, eventRouter, driver, hmCfg ):
        self._eventRouter = eventRouter
        self._adr = int(hmCfg["adr"])
        self._name = hmCfg["devkey"]
        self._weekdaySch = [None,None,None,None]
        self._weekendSch = [None,None,None,None]
        self._parameters = None
        self._curSetPoint = 0
        self._curTemp = 0
        self._heatmiserDriver = driver
        self._type = ""
        self._model = 0 # not yet known
        self._schname = None

        if hmCfg.has_key("schname"):
            self._schname = hmCfg["schname"]
            for idx in range(4):
                self._weekdaySch[idx] = HeatmiserSchEntry()
                self._weekendSch[idx] = HeatmiserSchEntry()

    def checkScheduleGroup( self, inData, to, base, dayStr ):
        for idx in range(4):
            if to[idx].updateTime( inData[idx][0], inData[idx][1] ):
                od = dict()
                od["time"] = "%02u:%02u:00" % (inData[idx][0],inData[idx][1])
                od["day"] = dayStr
                if self._eventRouter:
                    self._eventRouter.sendEvent( Event( "http://id.webbrick.co.uk/events/config/set", 
                                "schedule/%s/%i" %(self._schname, base+idx) , od ) )

            if to[idx].updateSetPoint( inData[idx][2] ):
                od = dict()
                od["val"] = inData[idx][2]
                if self._eventRouter:
                    self._eventRouter.sendEvent( Event( "http://id.webbrick.co.uk/events/config/set", 
                                "schedule/%s/%i/%s" %(self._schname, base+idx,self._name) , od ) )

    def readSchedules( self ):
        #if self._model == MODEL_PRTN:
        if self._schname:
            sch = self._heatmiserDriver.getSwitchTime( self._adr, CMD_GET_HEAT_WEEK_C_SET, self._model )
            self.checkScheduleGroup( sch, self._weekdaySch, 0, "-MTWtF-" )

            sch = self._heatmiserDriver.getSwitchTime( self._adr, CMD_GET_HEAT_WEND_C_SET, self._model )
            self.checkScheduleGroup( sch, self._weekendSch, 4, "S-----s" )

    def readStatus( self ):
        # if setpoint changed or temp changed.
        sts = self._heatmiserDriver.getStatus( self._adr )
        if sts:
            self._model = sts["model"]
            self._type = modelMap[self._model]

            if sts["roomT"] != self._curTemp:
                self._curTemp = sts["roomT"]
                if self._eventRouter:
                    self._eventRouter.sendEvent( Event( "http://id.webbrick.co.uk/events/heatmiser/current", 
                                "heatmiser/%s/temperature"%(self._name), { 'val': self._curTemp } ) )

            if sts["setT"] != self._curSetPoint:
                self._curSetPoint = sts["setT"]
                if self._eventRouter:
                    self._eventRouter.sendEvent( Event( "http://id.webbrick.co.uk/events/heatmiser/current", 
                                "heatmiser/%s/setpoint"%(self._name), { 'val': self._curSetPoint } ) )

    def start( self ):
        # do initial reads
        self._parameters = self._heatmiserDriver.readParameter( self._adr )
        self.readStatus()
        self.readSchedules()

    def setClock( self, dayOfWeek, hour, minute ):
        if self._model: # have we read the status yet.
            self._parameters = self._heatmiserDriver.readParameter( self._adr )
            self._parameters["hour"] = hour
            self._parameters["minute"] = minute
            self._parameters["dayOfWeek"] = dayOfWeek
            self._parameters["tempCal"] = self._parameters["roomT"]
            return self._heatmiserDriver.writeParameter( self._adr, self._parameters )
        return False;

    def readClock( self ):
        if self._model: # have we read the status yet.
            self._parameters = self._heatmiserDriver.readParameter( self._adr )
            return self._parameters
        return None

    def checkClock( self ):
        if self._model: # have we read the status yet.
            self._parameters = self._heatmiserDriver.readParameter( self._adr )
            if self._parameters:
                # verify against local time.
                # monday is 0 sunday is 6
                nowTime = time.gmtime()
                # nowTime[3] = hour
                # nowTime[4] = minute
                # nowTime[6] = day of week
                #self._parameters["hour"]
                if self._parameters["hour"] != nowTime[3] or self._parameters["minute"] != nowTime[4] or self._parameters["minute"] != nowTime[6] + 1 :
                    self._parameters["hour"] = nowTime[3]
                    self._parameters["minute"] = nowTime[4]
                    self._parameters["dayOfWeek"] = nowTime[6]+1
                    self._parameters["tempCal"] = self._parameters["roomT"]
                    self._heatmiserDriver.writeParameter( self._adr, self._parameters )

    def doVerifyAction( self, schkey, val ):
        _log.debug( "doVerifyAction %s %s" % (schkey, val) )
        # update action at time point
        if self._model == MODEL_PRTN:
            for idx in range(4):
                if self._weekdaySch[idx]._name == schkey:
                    # found it.
                    if self._weekdaySch[idx].diffSetPoint( val ):
                        # write to device
                        newSch = copy.copy( self._weekdaySch )
                        newSch[idx] = copy.copy( self._weekdaySch[idx] )
                        newSch[idx].updateSetPoint( val )
                        self._heatmiserDriver.setSchedule( self._adr, CMD_SET_HEAT_WEEK_C_SET, self._model, newSch )
                    return

            for idx in range(4):
                if self._weekendSch[idx]._name == schkey:
                    # found it.
                    if self._weekendSch[idx].diffSetPoint( val ):
                        # write to device
                        newSch = copy.copy( self._weekendSch )
                        newSch[idx] = copy.copy( self._weekendSch[idx] )
                        newSch[idx].updateSetPoint( val )
                        self._heatmiserDriver.setSchedule( self._adr, CMD_SET_HEAT_WEND_C_SET, self._model, newSch )
                    return

        # finished

    def doVerifySchTime( self, idx, timeStr ):
        # update time for action.
        if self._model == MODEL_PRTN:
            timeparts = timeStr.split(':')
            hrs = int(timeparts[0])
            mins = int(timeparts[1])
            if mins != 0 and mins != 30:
                # heatmiser does not handle finer resolution
                # round time to nearest 30 minute interval.
                if mins < 15:
                    mins = 0
                elif mins < 45:
                    mins = 30
                else:
                    mins = 0
                    hrs = hrs + 1
                    if hrs > 23:
                        hrs = 0


            assert( hrs < 24 )
            assert( mins < 60 )

            _log.debug( "doVerifySchTime %s %s, %s:%s" % (self._model, idx, hrs, mins) )

            if idx < 4:
                # weekday schedule
                if self._weekdaySch[idx].diffTime( hrs, mins ):
                    # write to device
                    newSch = copy.copy( self._weekdaySch )
                    newSch[idx] = copy.copy( self._weekdaySch[idx] )
                    newSch[idx].updateTime( hrs, mins )
                    self._heatmiserDriver.setSchedule( self._adr, CMD_SET_HEAT_WEEK_C_SET, self._model, newSch )
            else:
                idx = idx - 4
                if self._weekendSch[idx].diffTime( hrs, mins ):
                    # write to device
                    newSch = copy.copy( self._weekendSch )
                    newSch[idx] = copy.copy( self._weekendSch[idx] )
                    newSch[idx].updateTime( hrs, mins )
                    self._heatmiserDriver.setSchedule( self._adr, CMD_SET_HEAT_WEEK_C_SET, self._model, newSch )
        # finished

    def doControl( self, val ):
        # update current setpoint
        if self._model: # have we read the status yet.
            self._heatmiserDriver.setSetPoint( self._adr, val )

    def __str__(self):
        return "HeatmiserState %s" % ( __dict__ )

#
# WebBrick time event generator
#
class HeatmiserHandler( BaseHandler, threading.Thread ):
    """
    
    """

    def __init__ (self, localRouter):
        BaseHandler.__init__(self, localRouter)
        global _log
        _log = self._log
        threading.Thread.__init__(self)
        self.setDaemon( True ) # when main thread exits stop server as well

        self._taskList = Queue()
        self._heatmisers = dict()   # keyed by name

    def start(self):
        BaseHandler.start(self)
        threading.Thread.start(self)
        self._heatmiserDriver.open()
        self._taskList.put( ("start",) )

    def stop(self):
        self._taskList.put( ("quit",) )
        self._heatmiserDriver.close()
        BaseHandler.stop(self)

    def doAddHeatmiser(self, hmCfg ):
        """
        read heatmiser configuration and create correct object and add to dictionary.
        """
        _log.debug( "Create heatmiser %s" % hmCfg )
        newHm = HeatmiserState( self, self._heatmiserDriver, hmCfg )
        self._heatmisers[ newHm._name] = newHm

    def configure( self, cfgDict ):
        self._portName = cfgDict["serialPort"]
        try:
            # is it a numeric string?
            self._portName = int(self._portName)
        except Exception:
            pass

        BaseHandler.configure( self, cfgDict )
        self._heatmiserDriver = HeatmiserDriver( self._portName )

        # load heatmisers
        if isinstance( cfgDict["heatmiser"], list ):
            for hm in cfgDict["heatmiser"]:
                self.doAddHeatmiser( hm )
        else:
            self.doAddHeatmiser( cfgDict["heatmiser"] )

    def configureActions( self, cfgDict ):
        result = list()
        if cfgDict.has_key("action"):
            if isinstance( cfgDict["action"], list ):
                for action in cfgDict["action"]:
                    result.append(action["task"])
            else:
                result.append(cfgDict["action"]["task"])
        _log.debug("configureActions %s" % (result) )
        return result

    def doActions( self, tasks, inEvent ):
        if tasks:
            for task in tasks:
                _log.debug( "doAction %s", task )
                self._taskList.put( (task,inEvent) )

    def doStartAll( self ):
        for ky in self._heatmisers:
            _log.debug( "doStartAll heatmiser %s", ky )
            self._heatmisers[ky].start()

    def doReadSchedules( self ):
        for ky in self._heatmisers:
            _log.debug( "doReadSchedules heatmiser %s", ky )
            self._heatmisers[ky].readSchedules()

    def doReadStatus( self ):
        for ky in self._heatmisers:
            _log.debug( "doReadStatus heatmiser %s", ky )
            self._heatmisers[ky].readStatus()

    def doVerifyClock( self ):
        for ky in self._heatmisers:
            _log.debug( "doVerifyClock heatmiser %s", ky )
            self._heatmisers[ky].checkClock()

    def doVerifyDevice( self, inEvent ):
        # a device event is mainly used to notify us a device exists.
        # provides a display name and a default setpoint.
        od = inEvent.getPayload()
        if self._heatmisers.has_key( od["devkey"] ):
            pass

    def doVerifyAction( self, inEvent ):
        # a action event is used to change the action at a schkey time
        # {'schkey': schkey, 'devkey':act["devkey"], 'val': val } ) )
        od = inEvent.getPayload()
        if self._heatmisers.has_key( od["devkey"] ):
            schkey = od["schkey"]
            val = float(od["val"])    # parameter may be decimal
            self._heatmisers[od["devkey"]].doVerifyAction( schkey, int(round(val)) ) 

    def doVerifySchTime( self, inEvent ):
        # The time event should have a schname and idx, both from event source
        # this should be the keyword schedukle, schedule name and idx.
        es = inEvent.getSource().split('/')
        od = inEvent.getPayload()
        if es[1] in self._heatmisers and od and od.has_key('time'):
            # will not have both time and day?
            self._heatmisers[ky].doVerifySchTime( int(es[2]), od['time'] )

    def doControl( self, inEvent ):
        # a control event is used to adjust the current setting of a device
        od = inEvent.getPayload()
        if self._heatmisers.has_key( od["devkey"] ):
            val = float(od["val"])    # parameter may be decimal
            self._heatmisers[od["devkey"]].doControl( int(round(val)) )

    def run(self):
        # THIS IS BECAUSE we did not get twisted to go and we should not do lengthy code on the timer thread

        _log.debug( 'enter run' )
        while self.alive():
            try:
                task = self._taskList.get( True )
                if task[0] == "readSchedule" :
                    self.doReadSchedules()
                elif task[0] == "readStatus" :
                    self.doReadStatus()
                elif task[0] == "verifyClock" :
                    self.doVerifyClock()
                elif task[0] == "verifyDevice" :
                    self.doVerifyDevice( task[1] )
                elif task[0] == "verifyAction" :
                    self.doVerifyAction( task[1] )
                elif task[0] == "verifySchTime" :
                    self.doVerifySchTime( task[1] )
                elif task[0] == "doControl" :
                    self.doControl( task[1] )
                elif task[0] == "quit" :
                    break;  # while loop
                elif task[0] == "start" :
                    self.doStartAll()

            except Exception, ex:
                _log.exception( ex )

        _log.debug( 'exit run' )
