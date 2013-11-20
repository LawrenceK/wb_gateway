# $Id: WbConfigData.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
Module to define classes for handling WebBrick configuration data.

See also: Wb6Config.py.
"""

import WbDefs

class WbConfigData:
    """
    This class is an abstract base class for holding Python internal representations
    of WebBrick configuration data.
    
    The interface provided for accessing WebBrick configuration data is based on that
    provided by Wb6Config.py, but no methods are provided for setting the configuration
    data.  Derived classes should be defined to provide mechanisms for creating and/or
    updating configuration values.
    """

#TODO: move these to WbDefs?
    """ Operational state constants"""
    TD_Disabled  = 0
    TD_Startup   = 1
    TD_Normal    = 2
    TD_Quiescent = 3

#TODO: move these to WbDefs?
    """One wire status constants"""
    OW_None        = 0
    OW_BusGood     = 1
    OW_ReadingGood = 2
    OW_SoftwareErr = 3
    OW_BusBad      = 4

    def __init__ (self):
        """
        Initialize empty configuration data
        """
        def repeat(n,v): return [ v for i in range(n) ]
        self.Version           = None                     # String
        self.NodeName          = None                     # String
        self.NodeNumber        = -1                       # Int
        self.FadeRate          = -1                       # Int
        self.IpAddress         = None                     # String
        self.MacAddress        = None                     # String
        self.IrAddress         = 0                        # Int *
        self.IrTransmit        = False                    # Bool *
        self.IrReceive         = False                    # Bool *
        self.RotaryStep        = repeat(2,0)              # Int[2]
        self.MimicLo           = 0                        # Int *
        self.MimicHi           = 0                        # Int *
        self.MimicFade         = 0                        # Int *
        self.MimicMapDigital   = repeat(8,-1)             # Int(8) *
        self.MimicMapAnalog    = repeat(4,-1)             # Int(8) *
        self.DwellTime         = repeat(8,0)              # Int[8] (seconds)
        self.SetPoint          = repeat(8,0)              # Int[8]
        self.DigOutName        = repeat(8,None)           # String[8]
        self.AnalogOutName     = repeat(4,None)           # String[4]
        self.DigInTrigger      = repeat(12,{})            # Dictionary[12]
        self.TempTriggerLow    = repeat(5,{})             # Dictionary[5] 
        self.TempTriggerHigh   = repeat(5,{})             # Dictionary[5] 
        self.AnalogTriggerLow  = repeat(4,{})             # Dictionary[4]
        self.AnalogTriggerHigh = repeat(4,{})             # Dictionary[4] 
        self.ScheduledEvent    = repeat(16,{})            # Dictionary[16]
        self.Scene             = repeat(8,{})             # Dictionary[8] * suggest re-work
        
    def getVersion(self):
        """
        Retrieve the WebBrick software version
        """
        return self.Version
        
    def getNodeName(self):
        """
        Retrieve the WebBrick node name
        """
        return self.NodeName

    def getNodeNumber(self):
        """
        Retrieve the WebBrick node number
        """
        return self.NodeNumber

    def getNodeNumberStr(self):
        """
        Retrieve the WebBrick node number as a string
        """
        # return u'%03u' % self.NodeNumber
        return str(self.NodeNumber)
    
    def getFadeRate(self):
        """
        Retrieve the fade rate, as an integer.

        This controls how fast the analog outputs move towards their target value.
        """
        return self.FadeRate

    def getFadeRateStr(self):
        """
        Retrieve the fade rate, as a string.

        This controls how fast the analog outputs move towards their target value.
        """
        return str(self.FadeRate)

    def getIpAddress(self):
        """
        Retrieve the WebBrick IP address
        """
        return self.IpAddress
        
    def getMacAddress(self):
        """
        Retrieve the WebBrick Ethernet MAC address
        """
        return self.MacAddress
        
    def getIrAddress(self):
        """
        Retrieve the WebBrick recognized Infrared address
        """
        return self.IrAddress
        
    def getIrTransmit(self):
        """
        Retrieve the WebBrick Infrared transmit-enable flag
        """
        return self.IrTransmit
        
    def getIrReceive(self):
        """
        Retrieve the WebBrick Infrared receive-enable flag
        """
        return self.IrReceive
        
    def getRotary(self, idx):
        """
        Retrieve a rotary encoder step value.
        The current webbrick only supports a single encoder that connects to analog output zero.
        """
        WbDefs.checkRange(idx, 0, WbDefs.ROTARYCOUNT)
        return self.RotaryStep[idx]





    def getMimicLoLevel(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as an integer
        """
        return self.MimicLo

    def getMimicLoLevelStr(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as a string
        """
        return str(self.MimicLo)

    def getMimicHiLevel(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as an integer
        """
        return self.MimicHi

    def getMimicHiLevelStr(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as a string
        """
        return str(self.MimicHi)

    def getMimicFadeRate(self):
        """
        Retrieve value controlling the rate at which a mimic changes between 
        low and high brightness levels, as an integer.
        """
        return self.MimicFade

    def getMimicFadeRateStr(self):
        """
        Retrieve value controlling the rate at which a mimic changes between 
        low and high brightness levels, as a string.
        """
        return str(self.MimicFade)
    
    def getDigOutMimic(self, idx):
        """
        Retrieve the mimic output channel number for an analog output channel, 
        or -1 if no mimic is defined for the specified channel.
        """
        WbDefs.checkRange(idx, 0, WbDefs.DOCOUNT)
        return self.MimicMapDigital[idx]
    
    def getAnalogOutMimic(self, idx):
        """
        Retrieve the mimic output channel number for an analog output channel, 
        or -1 if no mimic is defined for the specified channel.
        """
        WbDefs.checkRange(idx, 0, WbDefs.AOCOUNT)
        return self.MimicMapAnalog[idx]
    
    def getDwell(self, idx):
        """
        Retrieve one of the dwell values. These are measured in seconds.
        """
        WbDefs.checkRange(idx, 0, WbDefs.DWELLCOUNT)
        return self.DwellTime[idx]
    
    def getDwellStr(self,idx):
        """
        Retrieve one of the dwell values as a user displayable string
        """
        dw = self.getDwell(idx)
        if (dw<=60):
            return u'%s Secs' % dw
        if (dw<=3600):
            return u'%i Mins' % round(dw/60)
        return u'%i Hours' % round(dw/3600)
        
    def getSetPoint(self,idx):
        """
        Retrieve one of the set points, these are a number between 0 and 100 (%)
        """
        WbDefs.checkRange(idx, 0, WbDefs.SPCOUNT)
        return self.SetPoint[idx]
        
    def getDigOutName(self, idx):
        """
        Get the name given to a digital output channel
        """
        WbDefs.checkRange(idx, 0, WbDefs.DOCOUNT)
        return self.DigOutName[idx]
        
    def getAnalogOutName(self, idx):
        """
        Get the name given to an analog output channel
        """
        WbDefs.checkRange(idx, 0, WbDefs.AOCOUNT)
        return self.AnalogOutName[idx]
    getAnalogueOutName = getAnalogOutName
        
    def getDigInName(self, idx):
        """
        Retrieve the name of a digital input
        """
        return self.getDigInTrigger(idx)["name"]

    def getDigInTrigger(self, idx):
        """
        Retrieve a dictionary defining the configuration of a single digital input.

        The result returned has the following values:
          ["name"]      = Digital input name
          ["options"]   = Digital input configuration options

          ["actionNr"]  = Trigger action code (see WbDefs.AT_NONE, etc.)
          ["action"]    = Trigger action descriptive string
          ["typeNr"]    = Trigger target type code (see WbDefs.TT_DIGITAL, etc.)
          ["type"]      = Trigger target type descriptive string
          ["UDPRemNr"]  = UDP packet type code (see WbDefs.UDPT_NONE, etc.)
          ["UDPRem"]    = UDP packet type descriptive string
          ["dwell"]     = dwell period
          ["RemNode"]   = remote node target for UDP packet
          ["setPoint"]  = Set point number
          ["pairChn"]   = Trigger target analog output, digital output or scene number
        """
        WbDefs.checkRange(idx, 0, WbDefs.DICOUNT)
        return self.DigInTrigger[idx]

    def getTempInName(self, idx):
        """
        Retrieve the name of a temperature input
        """
        return self.getTempTriggerLow(idx)["name"]
        
    def getTempTriggerLow(self, idx):
        """
        Retrieve a dictionary defining the configuration of a temperature low threshold

        The result returned has the following values:
          ["name"]      = Temperature input name
          ["threshold"] = Temperature low threshold value (float)

          ["actionNr"]  = Trigger action code (see WbDefs.AT_NONE, etc.)
          ["action"]    = Trigger action descriptive string
          ["typeNr"]    = Trigger target type code (see WbDefs.TT_DIGITAL, etc.)
          ["type"]      = Trigger target type descriptive string
          ["UDPRemNr"]  = UDP packet type code (see WbDefs.UDPT_NONE, etc.)
          ["UDPRem"]    = UDP packet type descriptive string
          ["dwell"]     = dwell period
          ["RemNode"]   = remote node target for UDP packet
          ["setPoint"]  = Set point number
          ["pairChn"]   = Trigger target analog output, digital output or scene number
        """
        WbDefs.checkRange(idx, 0, WbDefs.TEMPCOUNT)
        return self.TempTriggerLow[idx]
        
    def getTempTriggerHigh(self, idx):
        """
        Retrieve a dictionary defining the configuration of a temperature high threshold

        The result returned has the following values:
          ["name"]      = Temperature input name
          ["threshold"] = Temperature high threshold value (float)

          ["actionNr"]  = Trigger action code (see WbDefs.AT_NONE, etc.)
          ["action"]    = Trigger action descriptive string
          ["typeNr"]    = Trigger target type code (see WbDefs.TT_DIGITAL, etc.)
          ["type"]      = Trigger target type descriptive string
          ["UDPRemNr"]  = UDP packet type code (see WbDefs.UDPT_NONE, etc.)
          ["UDPRem"]    = UDP packet type descriptive string
          ["dwell"]     = dwell period
          ["RemNode"]   = remote node target for UDP packet
          ["setPoint"]  = Set point number
          ["pairChn"]   = Trigger target analog output, digital output or scene number
        """
        WbDefs.checkRange(idx, 0, WbDefs.TEMPCOUNT)
        return self.TempTriggerHigh[idx]

    def getAnalogInName(self, idx):
        """
        Retrieve the name of an analog input
        """
        return self.getAnalogTriggerLow(idx)["name"]
        
    def getAnalogTriggerLow(self, idx):
        """
        Retrieve a dictionary defining the configuration of a analog low threshold

        The result returned has the following values:
          ["name"]      = Analog input name
          ["threshold"] = Analog input low threshold value (float)

          ["actionNr"]  = Trigger action code (see WbDefs.AT_NONE, etc.)
          ["action"]    = Trigger action descriptive string
          ["typeNr"]    = Trigger target type code (see WbDefs.TT_DIGITAL, etc.)
          ["type"]      = Trigger target type descriptive string
          ["UDPRemNr"]  = UDP packet type code (see WbDefs.UDPT_NONE, etc.)
          ["UDPRem"]    = UDP packet type descriptive string
          ["dwell"]     = dwell period
          ["RemNode"]   = remote node target for UDP packet
          ["setPoint"]  = Set point number
          ["pairChn"]   = Trigger target analog output, digital output or scene number
        """
        WbDefs.checkRange(idx, 0, WbDefs.AICOUNT)
        return self.AnalogTriggerLow[idx]
    getAnalogueTriggerLow = getAnalogTriggerLow

    def getAnalogTriggerHigh(self, idx):
        """
        Retrieve a dictionary defining the configuration of a analog high threshold

        The result returned has the following values:
          ["name"]      = Analog input name
          ["threshold"] = Analog input high threshold value (float)

          ["actionNr"]  = Trigger action code (see WbDefs.AT_NONE, etc.)
          ["action"]    = Trigger action descriptive string
          ["typeNr"]    = Trigger target type code (see WbDefs.TT_DIGITAL, etc.)
          ["type"]      = Trigger target type descriptive string
          ["UDPRemNr"]  = UDP packet type code (see WbDefs.UDPT_NONE, etc.)
          ["UDPRem"]    = UDP packet type descriptive string
          ["dwell"]     = dwell period
          ["RemNode"]   = remote node target for UDP packet
          ["setPoint"]  = Set point number
          ["pairChn"]   = Trigger target analog output, digital output or scene number
        """
        WbDefs.checkRange(idx, 0, WbDefs.AICOUNT)
        return self.AnalogTriggerHigh[idx]
    getAnalogueTriggerHigh = getAnalogTriggerHigh
        
    def getScheduledEvent(self, idx):
        """
        Retrieve a dictionary defining the configuration of a scheduled event
          ["days"]      = (Mask) days-of-week on which the scheduled event occurs
          ["hours"]     = (Int) hour-of-day on which the scheduled event occurs
          ["mins"]      = (Int) minute-of-hour on which the scheduled event occurs

          ["actionNr"]  = Trigger action code (see WbDefs.AT_NONE, etc.)
          ["action"]    = Trigger action descriptive string
          ["typeNr"]    = Trigger target type code (see WbDefs.TT_DIGITAL, etc.)
          ["type"]      = Trigger target type descriptive string
          ["UDPRemNr"]  = UDP packet type code (see WbDefs.UDPT_NONE, etc.)
          ["UDPRem"]    = UDP packet type descriptive string
          ["dwell"]     = dwell period
          ["RemNode"]   = remote node target for UDP packet
          ["setPoint"]  = Set point number
          ["pairChn"]   = Trigger ta
        """
        WbDefs.checkRange(idx, 0, WbDefs.SCHEDCOUNT)
        return self.ScheduledEvent[idx]
        
    def getScene(self, idx):
        """
        Retrieve a dictionary defining the configuration of a scene.
        
        Dictionary entries are of the form:
          ["Digital<n>"]  = ("On"|"Off"|"Ignore")
          ["Analogue<n>"] = ("SetPoint<m>"|"Ignore")
        """
        def mkd(i):
            if   dvals[i] == None: return "Ignore"
            elif dvals[i]:         return "On"
            else:                  return "Off"
        def mka(i):
            if   avals[i] == None: return "Ignore"
            else:                  return "SetPoint%u"%(avals[i])
        dvals = self.getSceneAlt(idx)["Digital"]
        avals = self.getSceneAlt(idx)["Analog"]
        return { "Digital0":  mkd(0)
               , "Digital1":  mkd(1)
               , "Digital2":  mkd(2)
               , "Digital3":  mkd(3)
               , "Digital4":  mkd(4)
               , "Digital5":  mkd(5)
               , "Digital6":  mkd(6)
               , "Digital7":  mkd(7)
               , "Analogue0": mka(0)
               , "Analogue1": mka(1)
               , "Analogue2": mka(2)
               , "Analogue3": mka(3)
               }

    def getSceneAlt(self, idx):
        """
        Alternative scene configuration.
        
        Dictionary entries are of the form:
          ["Digital"] = List of 8 values, each "On", "Off" or None
          ["Analog"]  = List of 4 values, each None or an integer set point number
        """
        WbDefs.checkRange(idx, 0, WbDefs.SCENECOUNT)
        return self.Scene[idx]

# End. $Id: WbConfigData.py 2612 2008-08-11 20:08:49Z graham.klyne $
