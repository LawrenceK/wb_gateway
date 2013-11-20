# $Id: Wb6Status.py 2934 2008-11-13 11:01:52Z graham.klyne $

"""
Module to handle and decode WebBrick status queries
"""

import xml.dom
import xml.dom.minidom

import WebBrickLibs.WbDefs as WbDefs
from WebBrickLibs.WbAccess   import GetHTTPData

from MiscLib.DomHelpers import *
from MiscLib.Logging    import Trace, Info

# These definitions copied from svn:/WebBrick/Trunk/PIC/errors.h
ERR_None            = 0
ERR_BadCommand      = 1
ERR_BadParam        = 2
ERR_NotLoggedIn     = 3
ERR_AddressLocked   = 4
ERR_Startup         = 5
ERR_NoCommand       = 6

TEMP_Undefined      = -1000.0       # Sentinel value for undefined temperature

class Wb6StatusXml:
    """
    Wb6StatusXml
    WbStatusXml loads the Xml DOM from the string provided in the constructor.
    Once loaded the values are held and multiple requests can be made to read the values.

    This means that a single request can be used to satisfy more that one data requirement.
    """
    def __init__ (self, xmlstr):
        """
        xmlstr is the data to be loaded into the DOM.
        """
        #TODO: improve diagnostics in the event of XML parsing failure
        #      (show uri path and XML returned)
        self.xmlstr = xmlstr    # save for debugging
        self.dom = xml.dom.minidom.parseString( xmlstr )

    def getCmdStatus(self):
        """
        Get the status for the last command received at the webbrick.
        Returns an integer status code;  zero indicates success.

        (See WebBrick/Trunk/PIC/errors.h for error codes.)
        """
        return int(getNamedNodeText(self.dom,"Error"))

    #TODO: deprecate me
    def getError(self):
        """
        Use getCmdStatus
        """
        return self.getCmdStatus()
        
    def getOperationalState(self):
        """
        Get the operationla state of the webbrick, See webbrick manual.
        """
        return int(getNamedNodeText(self.dom,"Context"))

    def getNodeNumber(self):
        """
        Retrive the webbrick node number
        """
        nn = getNamedNodeText(self.dom, "SN")
        if nn:
            return int( nn )
        return 0

    def getLoginState(self):
        """
        Get the login state of the webbrick, See webbrick manual.
        """
        return int(getNamedNodeText(self.dom,"LoginState"))

    def getOneWireBus(self):
        """
        Get the state of the one wire bus.
        """
        return int(getNamedNodeText(self.dom,"OWBus"))

    def convertTemp(self, val):
        if val == "32767": return TEMP_Undefined
        result = float(val) / 16.0
        if ( result > 127.0 ):
            result -= 256.0
        return round(result,1)
        
    def getTemp(self, idx):
        """
        Retrieve a single temperature value.
        """
        WbDefs.checkRange(idx, 0, WbDefs.TEMPCOUNT)
        nodeList = self.dom.getElementsByTagName("Tmp")
        return self.convertTemp(getElemText(nodeList[idx]))

        
    def getTempLowThresh(self, idx):
        """
        Retrieve an analogue input value.
        """
        WbDefs.checkRange(idx, 0, WbDefs.TEMPCOUNT)
        nodeList = self.dom.getElementsByTagName("Tmp")
        return self.convertTemp(getAttrText( nodeList[idx], "lo" ))
        
    def getTempHighThresh(self, idx):
        """
        Retrieve an analogue input value.
        """
        WbDefs.checkRange(idx, 0, WbDefs.TEMPCOUNT)
        nodeList = self.dom.getElementsByTagName("Tmp")
        return self.convertTemp(getAttrText( nodeList[idx], "hi" ))
        
    def getAnOut(self, idx):
        """
        Retrieve an analogue output value.
        """
        WbDefs.checkRange(idx, 0, WbDefs.AOCOUNT)
        nodeList = self.dom.getElementsByTagName("AO")
        val = float(getElemText(nodeList[idx]))
        return val
    
    def getAnIn(self, idx):
        """
        Retrieve an analogue input value.
        """
        WbDefs.checkRange(idx, 0, WbDefs.AICOUNT)
        nodeList = self.dom.getElementsByTagName("AI")
        val = float(getElemText(nodeList[idx]))
        return val
        
    def getAnInLowThresh(self, idx):
        """
        Retrieve an analogue input value.
        """
        WbDefs.checkRange(idx, 0, WbDefs.AICOUNT)
        nodeList = self.dom.getElementsByTagName("AI")
        val = float(getAttrText( nodeList[idx], "lo" ) )
        return val
        
    def getAnInHighThresh(self, idx):
        """
        Retrieve an analogue input value.
        """
        WbDefs.checkRange(idx, 0, WbDefs.AICOUNT)
        nodeList = self.dom.getElementsByTagName("AI")
        val = float(getAttrText( nodeList[idx], "hi" ) )
        return val
        
    def getDigIn(self, idx):
        """
        Retrieve a digital input state
        """
        WbDefs.checkRange(idx, 0, WbDefs.DICOUNT)
        val = int(getNamedNodeText(self.dom, "DI"))
        if ( val & ( 0x01 << idx ) ) != 0 :
            return True
        return False
        
    def getMonitor(self, idx):
        """
        Retrieve a monitor input state

        This is an obsolete function as monitor inputs are now the same as digital inputs
        This is retained for backward compatiblity but will eventually dissapear.
        Monitor 0-3 are the digital inouts 8-11
        """
        WbDefs.checkRange(idx, 0, WbDefs.MONCOUNT)
        return self.getDigIn( idx + 8 )
        
    def getDigOut(self, idx):
        """
        Retrieve a digital output state, note mimics are dig out 8-15
        """
        WbDefs.checkRange(idx, 0, WbDefs.DOCOUNT+WbDefs.MIMICCOUNT)
        val = int(getNamedNodeText(self.dom, "DO"))
        
        if ( val & ( 0x01 << idx ) ) != 0 :
            return True
        return False
    
    def getDate(self):
        """
        Retrive the date as known by the webbrick, not currently available.
        """
        return getNamedNodeText(self.dom, "Date")
    
    def getTime(self):
        """
        Retrive the time as known by the webbrick, in the format HH:MM:SS.
        """
        ts = getNamedNodeText(self.dom, "Time")
        # may be better to parse and recreate.
        if ( ts[1] == ':' ):
            # pad hour.
            ts = '0' +ts
        if ( ts[4] == ':' ):
            # pad minute
            ts = ts[0:3]+ '0' +ts[3:]
        if ( len(ts) == 7 ):
            # pad second
            ts = ts[0:6]+ '0' +ts[6:]
        return ts
        
    def getDay(self):
        """
        Retrive the day as known by the webbrick, 0 is sunday.
        """
        return int(getNamedNodeText(self.dom, "Day"))
        
    def getVersion(self):
        """
        Retrive the webbrick software version
        """
        return getNamedNodeAttrText( self.dom, "WebbrickStatus", "Ver" )

class Wb6Status( Wb6StatusXml ):
    """
    This variant retrieves the Xml and then passes to the base class for processing.
    """
    def __init__ (self, adrs):
        #TODO: improve diagnostics in the event of XML parsing failure
        #      (show uri path and XML returned)
        uripath  = "/wbStatus.xml"
        xmlstr   = GetHTTPData(adrs,uripath)
        Wb6StatusXml.__init__ (self, xmlstr )

# End. $Id: Wb6Status.py 2934 2008-11-13 11:01:52Z graham.klyne $
