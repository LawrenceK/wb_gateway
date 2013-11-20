# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: WbConfigEdit.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
Module to define a class for editing WebBrick configuration data.
"""

from WbConfigData import WbConfigData
import WbDefs

class WbConfigEdit(WbConfigData):
    """
    This class is used for updating Python internal representations of WebBrick configuration data.
    """

    def __init__ (self, copyfrom=None):
        """
        Initialize configuration data.
        
        If copyfrom is provided, 
        """
        # Initialize all data
        WbConfigData.__init__(self)
        if copyfrom: self.setConfig(copyfrom)

    def setConfig(self, copyfrom):
        """
        Copy configuration data from the supplied configuration object
        into the current object.
        """
        self.Version           = copyfrom.getVersion()
        self.NodeName          = copyfrom.getNodeName()
        self.NodeNumber        = copyfrom.getNodeNumber()
        self.FadeRate          = copyfrom.getFadeRate()
        self.IpAddress         = copyfrom.getIpAddress()
        self.MacAddress        = copyfrom.getMacAddress()
        self.IrAddress         = copyfrom.getIrAddress()
        self.IrTransmit        = copyfrom.getIrTransmit()
        self.IrReceive         = copyfrom.getIrReceive()
        self.RotaryStep        = [ copyfrom.getRotary(i)          for i in range(WbDefs.ROTARYCOUNT) ]
        self.MimicLo           = copyfrom.getMimicLoLevel()
        self.MimicHi           = copyfrom.getMimicHiLevel()
        self.MimicFade         = copyfrom.getMimicFadeRate()
        self.MimicMapDigital   = [ copyfrom.getDigOutMimic(i)     for i in range(WbDefs.DOCOUNT)     ]
        self.MimicMapAnalog    = [ copyfrom.getAnalogOutMimic(i)  for i in range(WbDefs.AOCOUNT)     ]
        self.DwellTime         = [ copyfrom.getDwell(i)           for i in range(WbDefs.DWELLCOUNT)  ]
        self.SetPoint          = [ copyfrom.getSetPoint(i)        for i in range(WbDefs.SPCOUNT)     ]  
        self.DigOutName        = [ copyfrom.getDigOutName(i)               for i in range(WbDefs.DOCOUNT)     ]  
        self.AnalogOutName     = [ copyfrom.getAnalogOutName(i)            for i in range(WbDefs.AOCOUNT)     ]
        self.DigInTrigger      = [ copyfrom.getDigInTrigger(i).copy()      for i in range(WbDefs.DICOUNT)     ]
        self.TempTriggerLow    = [ copyfrom.getTempTriggerLow(i).copy()    for i in range(WbDefs.TEMPCOUNT)   ]
        self.TempTriggerHigh   = [ copyfrom.getTempTriggerHigh(i).copy()   for i in range(WbDefs.TEMPCOUNT)   ]
        self.AnalogTriggerLow  = [ copyfrom.getAnalogTriggerLow(i).copy()  for i in range(WbDefs.AICOUNT)     ]
        self.AnalogTriggerHigh = [ copyfrom.getAnalogTriggerHigh(i).copy() for i in range(WbDefs.AICOUNT)     ]
        self.ScheduledEvent    = [ copyfrom.getScheduledEvent(i).copy()    for i in range(WbDefs.SCHEDCOUNT)  ]
        self.Scene             = [ copyfrom.getSceneAlt(i).copy()          for i in range(WbDefs.SCENECOUNT)  ]

    def setVersion(self, ver):
        """
        Set the WebBrick software version
        """
        self.Version = ver
        
    def setNodeName(self, nam):
        """
        Set the WebBrick node name
        """
        self.NodeName = nam

    def setNodeNumber(self, num):
        """
        Set the WebBrick node number
        """
        self.NodeNumber = num
        
    def setFadeRate(self, val):
        """
        Set the faderate, this controls how fast the analog outputs move towards there target value
        """
        self.FadeRate = val
    
    def setIpAddress(self, adr):
        """
        Set the WebBrick IP address
        """
        self.IpAddress = adr
        
    def setMacAddress(self, adr):
        """
        Set the WebBrick Ethernet MAC address
        """
        self.MacAddress = adr
        
    def setIrAddress(self, adr):
        """
        Set the WebBrick recognized Infrared address
        """
        self.IrAddress = adr
        
    def setIrTransmit(self, enabled):
        """
        Set the WebBrick Infrared transmit-enable flag
        """
        self.IrTransmit = enabled
        
    def setIrReceive(self, enabled):
        """
        Set the WebBrick Infrared receive-enable flag
        """
        self.IrReceive = enabled
        
    def setRotary(self, idx, val):
        """
        Set a rotary encoder step value.
        The current webbrick only supports a single encoder that connects to analog output zero.
        """
        WbDefs.checkRange(idx, 0, WbDefs.ROTARYCOUNT)
        self.RotaryStep[idx] = val

    def setMimicLoLevel(self, val):
        """
        Set PCM output level for mimic at low-brightness
        """
        self.MimicLo = val

    def setMimicHiLevel(self, val):
        """
        Set PCM output level for mimic at low-brightness
        """
        self.MimicHi = val

    def setMimicFadeRate(self, val):
        """
        Set value controlling the rate at which a mimic changes between 
        low and high brightness levels.
        """
        self.MimicFade = val
    
    def setDigOutMimic(self, idx, val):
        """
        Set the mimic output channel number for an analog output channel, 
        or -1 if no mimic is defined for the specified channel.
        """
        WbDefs.checkRange(idx, 0, WbDefs.DOCOUNT)
        self.MimicMapDigital[idx] = val
    
    def setAnalogOutMimic(self, idx, val):
        """
        Retrieve the mimic output channel number for an analog output channel, 
        or -1 if no mimic is defined for the specified channel.
        """
        WbDefs.checkRange(idx, 0, WbDefs.AOCOUNT)
        self.MimicMapAnalog[idx] = val

    def setDwell(self, idx, val):
        """
        Set one of the dwell values. These are measured in seconds.
        """
        WbDefs.checkRange(idx, 0, WbDefs.DWELLCOUNT)
        self.DwellTime[idx] = val
        
    def setSetPoint(self, idx, val):
        """
        Set one of the set points.  These are a number 0..100 (%)
        """
        WbDefs.checkRange(idx, 0, WbDefs.SPCOUNT)
        self.SetPoint[idx] = val
        
    def setDigOutName(self, idx, nam):
        """
        Set the name of a digital output channel
        """
        WbDefs.checkRange(idx, 0, WbDefs.DOCOUNT)
        self.DigOutName[idx] = nam
        
    def setAnalogOutName(self, idx, nam):
        """
        Set the name of an analog output channel
        """
        WbDefs.checkRange(idx, 0, WbDefs.AOCOUNT)
        self.AnalogOutName[idx] = nam
        
    def setDigInTrigger(self, idx, val):
        """
        Set a dictionary with the configuration of a single digital input:
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
        self.DigInTrigger[idx] = val
        
    def setTempTriggerLow(self, idx, val):
        """
        Set a dictionary defining the configuration of a temperature low threshold:
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
        self.TempTriggerLow[idx] = val
        
    def setTempTriggerHigh(self, idx, val):
        """
        Set a dictionary defining the configuration of a temperature high threshold:
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
        self.TempTriggerHigh[idx] = val
        
    def setAnalogTriggerLow(self, idx, val):
        """
        Set a dictionary defining the configuration of a analog low threshold:
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
        self.AnalogTriggerLow[idx] = val
        
    def setAnalogTriggerHigh(self, idx, val):
        """
        Set a dictionary defining the configuration of a analog high threshold:
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
        self.AnalogTriggerHigh[idx] = val
        
    def setScheduledEvent(self, idx, val):
        """
        Set a dictionary defining the configuration of a scheduled event:
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
        self.ScheduledEvent[idx] = val
        
    def setScene(self, idx, val):
        """
        Set a dictionary defining the configuration of a scene.
        
        Dictionary entries are of the form:
          ["Digital<n>"] = ("On"|"Off"|"Ignore")
          ["Analogue<n>"] = ("SetPoint<m>"|"Ignore")
        """
        ### Currently broke -- consider removing this method ###
        WbDefs.checkRange(idx, 0, WbDefs.SCENECOUNT)
        self.Scene[idx] = val
        
    def setSceneAlt(self, idx, val):
        """
        Set a scene configuration using an alternative interface:
        
        Dictionary entries are of the form:
          ["Digital"] = List of 8 values, each "On", "Off" or None
          ["Analog"]  = List of 4 values, each None or an integer set point number
        """
        WbDefs.checkRange(idx, 0, WbDefs.SCENECOUNT)
        self.Scene[idx] = val

# End. $Id: WbConfigEdit.py 2612 2008-08-11 20:08:49Z graham.klyne $
