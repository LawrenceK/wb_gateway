# $Id: Wb6Config.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
Module to handle access to configuration data in an active WebBrick
"""

import xml.dom
import xml.dom.minidom

import WbDefs
from WebBrickLibs.WbAccess import GetHTTPData
from MiscLib.DomHelpers    import getElemText, getNamedNodeText, getNamedNodeAttrText

class Wb6Config:
    """
    This class handles access to the webbrick config. The constructor takes the 
    address of a webbrick and it loads the xml formatted configuration from it.

    This class then access the correct part of the Xml and decodes it on request. The
    Xml is cached in this object, only retrieved once, if you know or think the configuration
    has changed you throw away the object and create a new one.
    """

    """ Dispayable Operational state strings """
    ToDStrs = ["Commands Disabled", "Startup", "Normal Operation", "Quiescent Operation"]
    # AStrs = ["Off", "Enabled"]
    """ Dispayable One wire status strings """
    OneWStrs = ["No Sensors Found", "Bus Good, Sensor Found", "Bus Good, Reading Good", "Bus Good, Software Error", "Bus Bad, Held Low"]

    def __init__ (self, ipadrs=None, cnfxml=None):
        """
        Load xml config from webbrick at adrs
        
        If supplied, xml is a string of XML data that is used in place of
        XML configuration data read from a WebBrick.
        """
        if   cnfxml:
            self.xml = cnfxml
        elif ipadrs:
            self.xml = GetHTTPData(ipadrs, "/wbCfg.xml")
        else:
            raise "Wb6Config requires IP address or XML data"
        self.dom = xml.dom.minidom.parseString(self.xml)

    def getConfigXml(self):
        """
        Retrieve the WebBrick Configuration as an XML string
        """
        return self.xml

    def getVersion(self):
        """
        Retrieve the webbrick software version
        """
        return getNamedNodeAttrText(self.dom, "WebbrickConfig", "Ver")

    def getNodeName(self):
        """
        Retrieve the webbrick node name
        """
        return getNamedNodeText(self.dom, "NN")

    def getNodeNumber(self):
        """
        Retrieve the webbrick node number
        """
        return int(self.getNodeNumberStr())

    def getNodeNumberStr(self):
        """
        Retrieve the webbrick node number as a string
        """
        return getNamedNodeText(self.dom, "SN")
        
    def getFadeRate(self):
        """
        Retrieve the fade rate, as an integer.
        
        This controls how fast the analog outputs move towards their target value.
        """
        return int(self.getFadeRateStr())
        
    def getFadeRateStr(self):
        """
        Retrieve the fade rate, as a string.
        
        This controls how fast the analog outputs move towards their target value.
        """
        return getNamedNodeText(self.dom, "SF")
    
    def getIpAddress(self):
        """
        Retrieve the webbrick IP address
        """
        return getNamedNodeAttrText(self.dom, "SI", "ip")
        
    def getMacAddress(self):
        """
        Retrieve the webbrick Ethernet MAC address
        """
        return getNamedNodeAttrText(self.dom, "SI", "mac")
        
    def getIrAddress(self):
        """
        Retrieve the WebBrick recognized Infrared address
        """
        irconf = int(getNamedNodeText(self.dom, "IR"))
        return irconf&0x1F
        
    def getIrTransmit(self):
        """
        Retrieve the WebBrick Infrared transmit-enable flag
        """
        irconf = int(getNamedNodeText(self.dom, "IR"))
        return (irconf&0x20) != 0
        
    def getIrReceive(self):
        """
        Retrieve the WebBrick Infrared receive-enable flag
        """
        irconf = int(getNamedNodeText(self.dom, "IR"))
        return (irconf&0x40) != 0
        
    def getRotary(self, idx):
        """
        Retrieve a rotary encoder step value, the current webbrick only supports a single encoder
        that connects to analog output zero.
        """
        WbDefs.checkRange(idx, 0, WbDefs.ROTARYCOUNT)
        nodeList = self.dom.getElementsByTagName("SR")
        s = nodeList[idx].attributes["Value"].value
        return int(s)

    def getMimicLoLevel(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as an integer
        """
        return int(self.getMimicLoLevelStr())

    def getMimicLoLevelStr(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as a string
        """
        return getNamedNodeAttrText(self.dom, "MM", "lo")

    def getMimicHiLevel(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as an integer
        """
        return int(self.getMimicHiLevelStr())

    def getMimicHiLevelStr(self):
        """
        Retrieve PCM output level for mimic at low-brightness, as a string
        """
        return getNamedNodeAttrText(self.dom, "MM", "hi")

    def getMimicFadeRate(self):
        """
        Retrieve value controlling the rate at which a mimic changes between 
        low and high brightness levels, as an integer.
        """
        return int(self.getMimicFadeRateStr())

    def getMimicFadeRateStr(self):
        """
        Retrieve value controlling the rate at which a mimic changes between 
        low and high brightness levels, as a string.
        """
        return getNamedNodeAttrText(self.dom, "MM", "fr")
    
    def getDigOutMimic(self, idx):
        """
        Retrieve the mimic output channel number for an analog output channel, 
        or -1 if no mimic is defined for the specified channel.
        """
        WbDefs.checkRange(idx, 0, WbDefs.DOCOUNT)
        dms = getNamedNodeAttrText(self.dom, "MM", "dig")
        if dms:
            dm = int(dms)
            dv = dm >> (idx*4) & 0xF
            if dv < 8: return dv
        return -1
    
    def getAnalogOutMimic(self, idx):
        """
        Retrieve the mimic output channel number for an analog output channel, 
        or -1 if no mimic is defined for the specified channel.
        """
        WbDefs.checkRange(idx, 0, WbDefs.AOCOUNT)
        ams = getNamedNodeAttrText(self.dom, "MM", "an")
        if ams:
            am = int(ams)
            av = am >> (idx*4) & 0xF
            if av < 8: return av
        return -1
    
    def getDwell(self, idx):
        """
        Retrieve one of the dwell values. These are measured in seconds.
        """
        WbDefs.checkRange(idx, 0, WbDefs.DWELLCOUNT)
        nodeList = self.dom.getElementsByTagName("CW")
        return int(getElemText(nodeList[idx]))
    
    def getDwellStr(self,idx):
        """
        Retrieve one of the dwell values as a user displayable string
        """
        WbDefs.checkRange(idx, 0, WbDefs.DWELLCOUNT)
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
        nodeList = self.dom.getElementsByTagName("CS")
        return int(getElemText(nodeList[idx]))
        
    def _getName(self, type, idx):
        """
        Helper to extract a channel name 
        """
        nodeList = self.dom.getElementsByTagName(type)
        return nodeList[idx].attributes["Name"].value
        
    def getDigOutName(self, idx):
        """
        Get the name given to a digital output channel
        """
        WbDefs.checkRange(idx, 0, WbDefs.DOCOUNT)
        return self._getName('NO', idx)
        
    def getAnalogOutName(self, idx):
        """
        Get the name given to an analog output channel
        """
        WbDefs.checkRange(idx, 0, WbDefs.AOCOUNT)
        return self._getName('NA', idx)
    getAnalogueOutName = getAnalogOutName
        
    def _decodeTrigger(self, elem):
        """
        Helper to decode a trigger into its constituent parts and store them in a dictionary.
        This handles decoding the 4 standard bytes used to hold a trigger in a webbrick
        """
        encoding = "6.0"
        ver = self.getVersion()
        if ver[0:3] >= "6.5": encoding = "6.5"
        if ver >= "6.4.1898": encoding = "6.5"
        
        result = dict() # empty dictionary
        b1 = int(elem.attributes["B1"].value)
        b2 = int(elem.attributes["B2"].value)
        b3 = int(elem.attributes["B3"].value)

        if encoding == "6.0":
            result["actionNr"] = (b1 & 0x0F)
            result["action"] = WbDefs.ActionStrs[result["actionNr"]]
            result["dwell"] = ((b1 & 0x30) /16)
            result["UDPRemNr"] = ((b1 & 0xC0) /64)
            result["UDPRem"] = WbDefs.UDPRemStrs[result["UDPRemNr"]]
            result["RemNode"] = b3
        elif encoding == "6.5":
            grp = b1 & 0x60
            if grp == 0x60:
                # decode dwell
                dwellact = ( WbDefs.AT_DWELLON, WbDefs.AT_DWELLOFF
                           , WbDefs.AT_DWELLCAN, WbDefs.AT_DWELLALWAYS )
                result["actionNr"] = dwellact[(b1/8) & 0x3]
                result["dwell"]    = ((b1 & 0x07))
            elif grp == 0x00:
                # Not dwell here
                result["actionNr"] = (b1 & 0x1F)
                result["dwell"]    = 0
            else:
                raise Exception("Unrecognized command group "+str(grp))
            result["action"]   = WbDefs.ActionStrs65[result["actionNr"]]
            result["UDPRemNr"] = ((b1 & 0x80) / 128)
            result["UDPRem"]   = WbDefs.UDPRemStrs65[result["UDPRemNr"]]
            result["RemNode"]  = b3
        else:
            raise Exception("Unrecognized trigger encoding scheme")

        if ((b2 & 0x80) != 0):
            result["typeNr"] = WbDefs.TT_ANALOG
            result["setPoint"] = (b2 & 0x0F)
            result["pairChn"] = ((b2 & 0x70) /16)
        else:
            if ((b2 & 0x40) != 0):
                result["typeNr"] = WbDefs.TT_SCENE
            else:
                result["typeNr"] = WbDefs.TT_DIGITAL
            result["setPoint"] = 0
            result["pairChn"] = (b2 & 0x0F)
        result["type"] = WbDefs.ChannelTypeStrs[result["typeNr"]]
        return result
        
    def getDigInName(self, idx):
        """
        Retrieve the name of a digital input
        """
        return self.getDigInTrigger(idx)["name"]
        
    def getDigInTrigger(self, idx):
        """
        Retrieve a dictionary defining the configuration of a single digital input.
        """
        WbDefs.checkRange(idx, 0, WbDefs.DICOUNT)
        nodeList = self.dom.getElementsByTagName("CD")
        if idx >= len(nodeList): return {}              # For b/w compatibility - was fewer DIs
        node = nodeList[idx]
        result = self._decodeTrigger( node.getElementsByTagName("Trg")[0])
        result["name"] = node.attributes["Name"].value
        result["options"] = int(node.getAttribute("Opt") or "2")
        ### result["options"] = int(node.attributes["Opt"].value)
        return result

    def getTempInName(self, idx):
        """
        Retrieve the name of a temperature input
        """
        return self.getTempTriggerLow(idx)["name"]
        
    def getTempTriggerLow(self, idx):
        """
        Retrieve a dictionary defining the configuration of a temperature low threshold
        """
        WbDefs.checkRange(idx, 0, WbDefs.TEMPCOUNT)
        nodeList = self.dom.getElementsByTagName("CT")
        node = nodeList[idx]
        trg = node.getElementsByTagName("TrgL")[0]
        result = self._decodeTrigger( trg)
        result["name"] = node.attributes["Name"].value
        ta = trg.getAttribute("Val") or trg.getAttribute("Lo")
        result["threshold"] = float(ta)/16.0
        ### result["threshold"] = float(trg.attributes["Lo"].value)/16.0
        return result
        
    def getTempTriggerHigh(self, idx):
        """
        Retrieve a dictionary defining the configuration of a temperature high threshold
        """
        WbDefs.checkRange(idx, 0, WbDefs.TEMPCOUNT)
        nodeList = self.dom.getElementsByTagName("CT")
        node = nodeList[idx]
        trg = node.getElementsByTagName("TrgH")[0]
        result = self._decodeTrigger( trg)
        result["name"] = node.attributes["Name"].value
        ta = trg.getAttribute("Val") or trg.getAttribute("Hi")
        result["threshold"] = float(ta)/16.0
        ### result["threshold"] = float(trg.attributes["Hi"].value)/16.0
        return result

    def getAnalogInName(self, idx):
        """
        Retrieve the name of an analog input
        """
        return self.getAnalogTriggerLow(idx)["name"]
 
    def getAnalogTriggerLow(self, idx):
        """
        Retrieve a dictionary defining the configuration of a analog low threshold
        """
        WbDefs.checkRange(idx, 0, WbDefs.AICOUNT)
        nodeList = self.dom.getElementsByTagName("CI")
        node = nodeList[idx]
        trg = node.getElementsByTagName("TrgL")[0]
        result = self._decodeTrigger(trg)
        result["name"] = node.attributes["Name"].value
        ta = trg.getAttribute("Val") or trg.getAttribute("Lo")
        result["threshold"] = int(ta)
        ### result["threshold"] = int(trg.attributes["Lo"].value)
        return result
    getAnalogueTriggerLow = getAnalogTriggerLow
        
    def getAnalogTriggerHigh(self, idx):
        """
        Retrieve a dictionary defining the configuration of a analog high threshold
        """
        WbDefs.checkRange(idx, 0, WbDefs.AICOUNT)
        nodeList = self.dom.getElementsByTagName("CI")
        node = nodeList[idx]
        trg = node.getElementsByTagName("TrgH")[0]
        result = self._decodeTrigger( trg)
        result["name"] = node.attributes["Name"].value
        ta = trg.getAttribute("Val") or trg.getAttribute("Hi")
        result["threshold"] = int(ta)
        ### result["threshold"] = int(trg.attributes["Hi"].value)
        return result
    getAnalogueTriggerHigh = getAnalogTriggerHigh
        
    def getScheduledEvent(self, idx):
        """
        Retrieve a dictionary defining the configuration of a scheduled event
        """
        WbDefs.checkRange(idx, 0, WbDefs.SCHEDCOUNT)
        nodeList = self.dom.getElementsByTagName("CE")
        node = nodeList[idx]
        result = self._decodeTrigger( node.getElementsByTagName("Trg")[0])
        result["days"]  = int(node.getAttribute("Days"))
        result["hours"] = int(node.getAttribute("Hours") or node.getAttribute("Hrs"))
        result["mins"]  = int(node.getAttribute("Mins"))
        ###result["days"] = int(node.attributes["Days"].value)
        ###result["hours"] = int(node.attributes["Hours"].value)
        ###result["mins"] = int(node.attributes["Mins"].value)
        return result
        
    def getScene(self, idx):
        """
        Retrieve a dictionary defining the configuration of a scene.
        """
        WbDefs.checkRange(idx, 0, WbDefs.SCENECOUNT)
        result = dict() # empty dictionary
        nodeList = self.dom.getElementsByTagName("CC")
        node = nodeList[idx]
        Dm = int(node.attributes["Dm"].value)
        Ds = int(node.attributes["Ds"].value)
        Am = int(node.attributes["Am"].value)
        Av = int(node.attributes["Av"].value)
        
        for i in range(8):
            if ( ( Dm & ( 1 << i) ) != 0 ):
                if ( ( Ds  & ( 1 << i) ) != 0 ):
                    result["Digital"+str(i)] = "On"
                else:
                    result["Digital"+str(i)] = "Off"
            else:
                result["Digital"+str(i)] = "Ignore"
                
        for i in range(4):
            if ( ( Am & ( 1 << i) ) != 0 ):
                result["Analogue"+str(i)] = "SetPoint"+str(Av & 0x0F)
            else:
                result["Analogue"+str(i)] = "Ignore"
            Av >>= 4
        
        return result
        
    def getSceneAlt(self, idx):
        """
        Retrieve an alternative dictionary defining the configuration of a scene.
        """
        WbDefs.checkRange(idx, 0, WbDefs.SCENECOUNT)
        nodeList = self.dom.getElementsByTagName("CC")
        ds = [None for i in range(8)]
        as = [None for i in range(4)]
        if idx < len(nodeList):                 # For b/w compatibility - was fewer scenes
            node = nodeList[idx]
            Dm = int(node.attributes["Dm"].value)
            Ds = int(node.attributes["Ds"].value)
            Am = int(node.attributes["Am"].value)
            Av = int(node.attributes["Av"].value)
            for i in range(8):
                if ( ( Dm & ( 1 << i) ) != 0 ):
                    ds[i] = ( ( Ds  & ( 1 << i) ) != 0 )
            for i in range(4):
                if ( ( Am & ( 1 << i) ) != 0 ):
                    as[i] = Av & 0x0F
                Av >>= 4
        return { "Digital": ds, "Analog": as }

# End. $Id: Wb6Config.py 2612 2008-08-11 20:08:49Z graham.klyne $
