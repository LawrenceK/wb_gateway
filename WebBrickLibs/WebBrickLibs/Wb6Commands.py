# $Id: Wb6Commands.py 2830 2008-10-01 13:56:23Z graham.klyne $
#
# WebBrickSystems.com
#
"""
Class to handle Commands to a webbrick and retrieve data from a webbrick

The aim is for this to provide low level webbrick access, this version uses
HTTP exclusively, where as the original used UDP packets.
"""
import logging

import WbDefs
from WbAccess import SendHTTPCmd

from MiscLib.NetUtils import arpCacheFlush
_log = logging.getLogger("WebBrickLibs.Wb6Commands")

class Wb6Commands:
    """
    This class acts as a higher level interface to the webbrick commands.
    """
    
    def __init__( self, addr ):
        """
        Construct an WebBrick object and save the target address
        """
        self._wbAddress = addr

    # General access and setup
    def Login(self, password):
        """
        Login to webbrick. This is required if you want to send configuration commands.
        """
        SendHTTPCmd(self._wbAddress,"LG;" + password )

    def ConfigNode(self, node):
        """
        Configure node number for webBrick.
        Used by testing software so that event source is predictable.
        """
        SendHTTPCmd(self._wbAddress,"SN%i"%(node) )

    # I/O control and configuration commands
    def DigTrigger(self, chn):
        """
        send a trigger to a digital input, the equivalent to the input being physically triggered.
        """
        SendHTTPCmd(self._wbAddress,"DI" + str(chn) )

    def DigOn(self, chn):
        """
        Set a digital output On
        """
        SendHTTPCmd(self._wbAddress,"DO" + str(chn) + ";N" )

    def DigOff(self, chn):
        """
        Set a digital output Off
        """
        SendHTTPCmd(self._wbAddress,"DO" + str(chn) + ";F" )

    def DigToggle(self, chn):
        """
        Toggle a digital output

        It is preferable to use commands that the result does not depend on the initial state, 
        i.e. if two automatic services send a Toggle because they want the output on then the result
        will be Off. Therefore it is better to send an explicit On.
        """
        SendHTTPCmd(self._wbAddress,"DO" + str(chn) + ";T" )

    def DigDwell(self, chn, DwellNr):
        """
        Switch a digital output on for a period of time, selected by the dwell number.
        The dwell times are separated from the dwell numbers.
        """
        SendHTTPCmd(self._wbAddress,"DO" + str(chn) + ";D;" + str(DwellNr) )

    def DoMimic(self, chn, value):
        """
        Set a digital output Off
        """
        SendHTTPCmd(self._wbAddress,"DM" + str(chn) + ";" + str(value) )

    def AnOutSp(self, chn, sp):
        """
        Switch an analogue output to one of the setpoints
        """
        SendHTTPCmd(self._wbAddress,"AA" + str(chn) + ";S" + str(sp) )

    def AnOutPercent(self, chn, val):
        """
        Switch an analogue output to a specific percentage value (0-100%)
        """
        SendHTTPCmd(self._wbAddress,"AA" + str(chn) + ";" + str(val) )

    def SetScene(self, sc):
        """
        Set a scene, equivalent to a trigger targetting a Scene with an On command.
        """
        WbDefs.checkRange(sc, 0, WbDefs.SCENECOUNT)
        SendHTTPCmd(self._wbAddress,"SC" + str(sc) )

    # day 0-6, hour 0-23, minute 0-59    
    def SetTime(self, day, hr, min):
        """
        Update the webbrick clock.
        """
        WbDefs.checkRange(day,0,7)
        WbDefs.checkRange(hr,0,24)
        WbDefs.checkRange(min,0,60)
        SendHTTPCmd(self._wbAddress,"ST" + str(day) + ";" + str(hr) + ";" + str(min) )
        
    def _CreateTriggerString(self, tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved ):
        """
        Internal helper

        Create the trigger string.
        tgtType - a single character identiying the target type
        tgtIdx - the index/channel number of tgtType
        sp - setpoint if relevant.
        dwell - if relevant
        udpType - control whether UDP packet sent and what type.
        associatedValue - an action/udpType value.
        reserved - future enhancement
        channelOptions - option values for the channel
        """
        WbDefs.checkRange(tgtIdx, 0, 16)    # variable
        WbDefs.checkRange(action, WbDefs.AT_NONE, WbDefs.AT_SPARE)
        WbDefs.checkRange(sp, 0, 8)
        WbDefs.checkRange(dwell, 0, 4)
        WbDefs.checkRange(udpType, 0, 4)
        WbDefs.checkRange(associatedValue, 0, 256)
        cmd = ";%s%i;%i;%i;%i;%i;%i" % ( WbDefs.TTCommandTags[tgtType], tgtIdx, sp, action, dwell, udpType, associatedValue )
        if ( reserved != None ):
            cmd = "%s;%i" % (cmd,reserved)
        return cmd

    def ConfigDigIn(self, iChn, tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved = None, channelOptions = None ):
        """
        Configure the trigger action for a digital input, the later two parameters are optional at present.
        iChn - channel number
        tgtType - a single character identiying the target type
        tgtIdx - the index/channel number of tgtType
        sp - setpoint if relevant.
        dwell - if relevant
        udpType - control whether UDP packet sent and what type.
        associatedValue - an action/udpType value.
        reserved - future enhancement
        channelOptions - option values for the channel
        """
        # CD<chn>;<ADS><tgtChn>;<sp>;<actionType>;<dwell>;<udpType>;<associatedValue>,][< reserved>[channelOptions]]:

        cmd = "CD%i%s" % ( iChn, self._CreateTriggerString(tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved ) )
        if ( channelOptions != None ):
            if ( reserved == None ):
                cmd = "%s;0;%i" % (cmd,channelOptions)
            else:
                cmd = "%s;%i" % (cmd,channelOptions)
        self.Send(cmd )

    def SendTrigger(self, tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved = None ):
        """
        Get a webbrick to action a the trigger.
        tgtType - a single character identiying the target type
        tgtIdx - the index/channel number of tgtType
        sp - setpoint if relevant.
        dwell - if relevant
        udpType - control whether UDP packet sent and what type.
        associatedValue - an action/udpType value.
        reserved - future enhancement
        """
        # DT<chn>;<ADS><tgtChn>;<sp>;<actionType>;<dwell>;<udpType>;<associatedValue>,][< reserved>[channelOptions]]:
        cmd = "DT%s" % ( self._CreateTriggerString(tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved) )
        self.Send(cmd)

    def sendSerial(self, data):
        cmd = "RD" + (";".join( map((lambda c:str(ord(c))), data) ))
        self.Send(cmd)
        return

    def ConfigFadeRate(self, rate):
        """
        Configure the analogue output fade rate
        """
        WbDefs.checkRange(rate, 0, 256)
        self.Send("SF%i" % rate)

    def ConfigSerial(self, mode, baud):
        """
        Configure the serial port
        
        mode=0  no change
        mode=2  RS232
        mode=3  DMX
        mode=4  RS485
        
        baud=0  300
        baud=1  600
        baud=2  1200
        baud=3  2400
        baud=4  4800
        baud=5  9600
        """
        WbDefs.checkRange(mode, 0, 5)
        WbDefs.checkRange(baud, 0, 6)
        self.Send("CR%i;%i" % (mode,baud))

    def ConfigAnIn(self, iChn, thType, thVal, tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved = None ):
        """
        Configure the trigger action for a analog input, the later two parameters are optional at present.
        iChn - channel number
        tgtType - a single character identiying the target type
        tgtIdx - the index/channel number of tgtType
        sp - setpoint if relevant.
        dwell - if relevant
        udpType - control whether UDP packet sent and what type.
        associatedValue - an action/udpType value.
        """
        # CI<chn>;<L|H><val>;<ADS><tgtChn>;<sp>;<actionType>;<dwell>;<udpType>;<associatedValue>:

        WbDefs.checkRange(iChn, 0, WbDefs.AICOUNT)
        WbDefs.checkRange(thVal, 0, 256)

        trg = self._CreateTriggerString(tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved )
        cmd = "CI%i;%s%i%s"%(iChn, thType, thVal, trg)

        self.Send( cmd )

    def ConfigAnThreshold(self, iChn, thType, thVal ):
        """
        Configure the threshold for an analogue input. This only sets the active value.
        iChn - channel number
        thType - a single character identiying the threshold hight or low
        thVal - The threshold value
        """
        # CI<chn>;<L|H><val>;<ADS><tgtChn>;<sp>;<actionType>;<dwell>;<udpType>;<associatedValue>:

        WbDefs.checkRange(iChn, 0, WbDefs.AICOUNT)
        WbDefs.checkRange(thVal, 0, 256)

        cmd = "TA%i;%s%i" %  ( iChn, thType, thVal )

        self.Send( cmd )

    def ConfigTemp(self, iChn, thType, thVal, tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved = None ):
        """
        """
        WbDefs.checkRange(iChn, 0, WbDefs.TEMPCOUNT)
        WbDefs.checkRange(thVal, -50, 125)
        # CTchn;[L|H]Val;Trigger
        cmd = "CT%i;%s%1.1f%s" %  ( iChn, thType, thVal, self._CreateTriggerString(tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved ) )
        self.Send( cmd )

    def ConfigTempThreshold(self, iChn, thType, thVal ):
        """
        Configure the threshold for a temperature sensor. This only sets the active value.
        iChn - channel number
        thType - a single character identiying the threshold hight or low
        thVal - The threshold value
        """
        WbDefs.checkRange(iChn, 0, WbDefs.TEMPCOUNT)
        WbDefs.checkRange(thVal, -50, 125)
        cmd = "TT%i;%s%1.1f" %  ( iChn, thType, thVal )
        self.Send( cmd )

    def ConfigScheduled(self, iEv, days, hour, min, tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved = None ):
        # CE<num>;<Days>;<Hours>;<Mins>;<ADS><tgtChn>;<sp>;<actionType>;<dwell>;<udpType>;<nodeNr>;<val>:
        WbDefs.checkRange(iEv, 0, WbDefs.SCHEDCOUNT)
        WbDefs.checkRange(hour, 0, 24)
        WbDefs.checkRange(min, 0, 60)

        cmd = "CE%i;%s;%i;%i%s" %  ( iEv, days, hour, min, self._CreateTriggerString(tgtType, tgtIdx, action, sp, dwell, udpType, associatedValue, reserved ) )

        self.Send( cmd )

    def ConfigScene(self, iScene, digOut, anOut ):
        # CC\param{nr};[NFI][NFI][NFI][NFI][NFI][NFI][NFI][NFI];[I|S\param{nn}];[I|S\param{nn}];[I|S\param{nn}];[I|S\param{nn}]:
        WbDefs.checkRange(iScene, 0, WbDefs.SCENECOUNT)
        assert (len(digOut) == WbDefs.DOCOUNT )
        assert (len(anOut) == WbDefs.AOCOUNT )

        cmd = "CC%i;" % (iScene)
        for d in digOut:
            assert d in ["N","F","I"], "Bad digital parameter"
            cmd = cmd + d
        for a in anOut:
            if ( a == "I" ):
                cmd = "%s;I" % cmd
            elif (a[0] == "S"):
                WbDefs.checkRange(a[1], 0, WbDefs.SPCOUNT)
                cmd = "%s;S%i"% (cmd,a[1])
            else:
                assert False, "Bad analogue parameter"
        self.Send( cmd )

    def Send(self,cmd):
        """
        A helper that enables sending commands that have yet to be implemented as separate functions.
        Its main purpose is to ensure that it is terminated.
        """
        # include colon in case caller misses them out. Now handled in SendHTTPCmd
        # the first colon is to flush any crap in the receive buffer.
        #if ( cmd[0] != ":" ) or ( cmd[-1] != ":" ):
        #    cmd = ":%s:" % cmd
        SendHTTPCmd(self._wbAddress, cmd )

def resetSitePlayer( ipAdr ):
    """
    """
    _log.info( "Reset Siteplayer on node %s " % ipAdr )
    arpCacheFlush(ipAdr)
    SendHTTPCmd(ipAdr,"LGpassword:RS")
#    from WebBrickLibs.WbUdpCommands  import sendUdpCommand
#    sendUdpCommand( ipAdr, "LGpassword:RS" )

# End: $Id: Wb6Commands.py 2830 2008-10-01 13:56:23Z graham.klyne $
