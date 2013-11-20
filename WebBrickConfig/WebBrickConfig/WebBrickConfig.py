# $Id: WebBrickConfig.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
"""
Read and parse a WebBrick XML configuration file, 
and convert into WebBrick configuration commands.
"""

from MiscLib.DomHelpers  import parseXmlFile, getElemText, getElemXml, getAttrText, getNamedElem
from MiscLib.Combinators import compose, curry
from MiscLib.Functions   import cond
from MiscLib.Logging     import Trace, Warn, Error

class WebBrickConfigException(Exception):
    """
    Exception value for reporting configuration problems.
    """

    def __init__(self, command=None, element=None, cause=None):
        self.cmd   = command
        self.elem  = element
        self.cause = cause
        return

    def __str__(self):
        s = "Configuration error"
        if self.cmd: s += " making %s command"%(self.cmd)
        if self.elem: 
            if self.cmd:
                s += " from"
            else:
                s += " processing"
            s += " element: \n"
            s += self.elem
        if self.cause:
            s += "\n%s\n"%(self.cause)
        return s

class WebBrickConfig:

    """
    Contains methods to read a WebBrick XML configuration file, 
    and convert it into WebBrick configuration commands.
    """

    def __init__(self):
        return None

    def makeConfigCommands(self,dom,override):
        """
        Convert the supplied DOM object into a list of webbrick
        configuration commands.  The override parameter is a dictionary
        of values that can be used to override values in the supplied
        DOM when generating the configuration commands; e.g.
            "password" - overrides password used with "LG" command
            "IP"       - overrides IP{ addresss et with "IA" command
        """
        p    = override.get("password") or "password"
        cmds = ["LG"+p,"SS1"]

        template = (
            # elem1 elem2 cmd   override    transform
            ("NN",  None, "NN", "NodeName", getNameText),   # Node name
            ("SN",  None, "SN", "NodeNum",  getElemText),   # Node number

            ("NOs", "NO", "NO", None,       idNameAttr),    # Name Digital Output
            ("CDs", "CD", "ND", None,       idNameAttr),    # Name Digital Input
            ("CDs", "CD", "CD", None,       idTrigger),     # Configure Digital Input
            #Monitors are now DIs 8-11
            #("NMs", "NM", "NM", None,       idNameAttr),    # Name Monitor Input

            ("NAs", "NA", "NA", None,       idNameAttr),    # Name Analogue Output
            ("CIs", "CI", "NI", None,       idNameAttr),    # Name Analogue Input
            ("CIs", "CI", "CI", None,       idAnalogLo),    # Configure Analogue Input Low threshold
            ("CIs", "CI", "CI", None,       idAnalogHi),    # Configure Analogue Input High threshold
            ("CTs", "CT", "NT", None,       idNameAttr),    # Name Temperature Sensor
            ("CTs", "CT", "CT", None,       idTempLo),      # Configure Temperature Sensor Low threshold
            ("CTs", "CT", "CT", None,       idTempHi),      # Configure Temperature Sensor High threshold
            ("SRs", "SR", "SR", None,       idValAttr),     # Rotary encoder step
            ("IR",  None, "IR", None,       maskNF(0x40)),  # Enable infrared receive?
            ("IR",  None, "IT", None,       maskNF(0x20)),  # Enable infrared transmit?
            ("IR",  None, "IA", None,       maskInt(0x1F)), # Infrared receiving address
            ("SF",  None, "SF", None,       getElemText),   # Fade rate
            ("MM",  None, "SM", None,       mimicLoHiFade), # Set mimic hi/lo/faderate
            ("MM",  None, "CM", None,       mimicAChan(0)), # Configure mimic channel for analog out 0
            ("MM",  None, "CM", None,       mimicAChan(1)), # Configure mimic channel for analog out 1
            ("MM",  None, "CM", None,       mimicAChan(2)), # Configure mimic channel for analog out 2
            ("MM",  None, "CM", None,       mimicAChan(3)), # Configure mimic channel for analog out 3
            ("MM",  None, "CM", None,       mimicDChan(0)), # Configure mimic channel for digital out 0
            ("MM",  None, "CM", None,       mimicDChan(1)), # Configure mimic channel for digital out 1
            ("MM",  None, "CM", None,       mimicDChan(2)), # Configure mimic channel for digital out 2
            ("MM",  None, "CM", None,       mimicDChan(3)), # Configure mimic channel for digital out 3
            ("MM",  None, "CM", None,       mimicDChan(4)), # Configure mimic channel for digital out 4
            ("MM",  None, "CM", None,       mimicDChan(5)), # Configure mimic channel for digital out 5
            ("MM",  None, "CM", None,       mimicDChan(6)), # Configure mimic channel for digital out 6
            ("MM",  None, "CM", None,       mimicDChan(7)), # Configure mimic channel for digital out 7
            ("CWs", "CW", "CW", None,       idElemText),    # Configure Dwell
            ("CSs", "CS", "CS", None,       idElemText),    # Configure Preset Point
            ("CEs", "CE", "CE", None,       idSchedule),    # Configure Schedule Event
            ("CCs", "CC", "CC", None,       idScene)        # Configure Scene
            )

        # for webbrick 6.5, when triggers changed.
        template6_5 = (
            # elem1 elem2 cmd   override    transform
            ("NN",  None, "NN", "NodeName", getNameText),   # Node name
            ("SN",  None, "SN", "NodeNum",  getElemText),   # Node number

            ("NOs", "NO", "NO", None,       idNameAttr),    # Name Digital Output
            ("CDs", "CD", "ND", None,       idNameAttr),    # Name Digital Input
            ("CDs", "CD", "CD", None,       idTrigger65),   # Configure Digital Input
            #Monitors are now DIs 8-11
            #("NMs", "NM", "NM", None,      idNameAttr),    # Name Monitor Input

            ("NAs", "NA", "NA", None,       idNameAttr),    # Name Analogue Output
            ("CIs", "CI", "NI", None,       idNameAttr),    # Name Analogue Input
            ("CIs", "CI", "CI", None,       idAnalogLo65),  # Configure Analogue Input Low threshold
            ("CIs", "CI", "CI", None,       idAnalogHi65),  # Configure Analogue Input High threshold
            ("CTs", "CT", "NT", None,       idNameAttr),    # Name Temperature Sensor
            ("CTs", "CT", "CT", None,       idTempLo65),    # Configure Temperature Sensor Low threshold
            ("CTs", "CT", "CT", None,       idTempHi65),    # Configure Temperature Sensor High threshold
            ("SRs", "SR", "SR", None,       idValAttr),     # Rotary encoder step
            ("SE",  None, "CR", None,       serialConfig),  # Serial config
            ("IR",  None, "IR", None,       maskNF(0x40)),  # Enable infrared receive?
            ("IR",  None, "IT", None,       maskNF(0x20)),  # Enable infrared transmit?
            ("IR",  None, "IA", None,       maskInt(0x1F)), # Infrared receiving address
            ("SF",  None, "SF", None,       getElemText),   # Fade rate
            ("MM",  None, "SM", None,       mimicLoHiFade), # Set mimic hi/lo/faderate
            ("MM",  None, "CM", None,       mimicAChan(0)), # Configure mimic channel for analog out 0
            ("MM",  None, "CM", None,       mimicAChan(1)), # Configure mimic channel for analog out 1
            ("MM",  None, "CM", None,       mimicAChan(2)), # Configure mimic channel for analog out 2
            ("MM",  None, "CM", None,       mimicAChan(3)), # Configure mimic channel for analog out 3
            ("MM",  None, "CM", None,       mimicDChan(0)), # Configure mimic channel for digital out 0
            ("MM",  None, "CM", None,       mimicDChan(1)), # Configure mimic channel for digital out 1
            ("MM",  None, "CM", None,       mimicDChan(2)), # Configure mimic channel for digital out 2
            ("MM",  None, "CM", None,       mimicDChan(3)), # Configure mimic channel for digital out 3
            ("MM",  None, "CM", None,       mimicDChan(4)), # Configure mimic channel for digital out 4
            ("MM",  None, "CM", None,       mimicDChan(5)), # Configure mimic channel for digital out 5
            ("MM",  None, "CM", None,       mimicDChan(6)), # Configure mimic channel for digital out 6
            ("MM",  None, "CM", None,       mimicDChan(7)), # Configure mimic channel for digital out 7
            ("CWs", "CW", "CW", None,       idElemText),    # Configure Dwell
            ("CSs", "CS", "CS", None,       idElemText),    # Configure Preset Point
            ("CEs", "CE", "CE", None,       idSchedule65),    # Configure Schedule Event
            ("CCs", "CC", "CC", None,       idScene)        # Configure Scene
            )

        ver_template = template
        # is this a version 6.5 webbrick, version is on root level 
        ver_str = getAttrText( getNamedElem(dom,"WebbrickConfig") , "Ver")
        if ver_str and ver_str > "6.4.1904":
            ver_template = template6_5

        for (en1,en2,cn,ov,transform) in ver_template:
            # Construct command, allowing for supplied override
            def mkCmd(cn,ov,transform,e):
                Trace("Generate command %s for element %s"%(cn,getElemXml(e)), "WebBrickConfig.WebBrickConfig")
                try:
                    val = (ov and override.get(ov)) or transform(e)
                except Exception, exc:
                    raise WebBrickConfigException(command=cn, element=getElemXml(e), cause=str(exc))
                return val and cn+val
            # Select top-level element
            Trace("Processing config element "+en1, "WebBrickConfig.WebBrickConfig")
            try:
                elms = dom.getElementsByTagName(en1)
                elm1 = elms and elms[0]
            except Exception, e:
                raise WebBrickConfigException(command=cn, cause=str(e))
            if not elm1: continue
            if not en2:
                # Single top-level element here
                newcmd = [mkCmd(cn,ov,transform,elm1)]
            else:
                # Multiple second-level elements
                elms   = elm1.getElementsByTagName(en2)
                newcmd = map(curry(mkCmd,cn,ov,transform),elms)
            if newcmd and newcmd[0]: cmds = cmds+newcmd

        # Finish up: new IP address and end
        ipaddr = override.get("IP")
        if ipaddr: 
            ipbytes = ipaddr.split(".")
            cmds = cmds+["SI"+ipbytes[0]+";"+ipbytes[1]+";"+ipbytes[2]+";"+ipbytes[3]]
        cmds = cmds+["SS2"]
        return cmds

# Helpers for converting an XML element into a command parameter list

def ident(v):
    return v

def div16(v):
    return "%1.1f"%(int(v)/16.0)

def maskInt(mask):
    """
    Returns function to extract a masked integer value from the text of an element.
    """
    return (lambda e: "%i"%(int(getElemText(e))&mask))

def maskNF(mask):
    """
    Returns function to return N (on) or F (off) corresponding to the setting of
    a masked bit in the integer value of text from an element.
    
    E.g. maskNF(0x20) is "N" if the element contains a a number in which bit 0x20
    is set, otherwise "F".
    """
    def mapNF(v): 
        if v!=0: return "N"
        return "F"
    return (lambda e: mapNF(int(getElemText(e))&mask))

def maskToList(taglist,val):
    """
    Interprets the supplied value as a decimal integer representing a bit field, and 
    returns a concatenation of values from the supplied taglist string corresponding 
    to those bits that are set, (or an empty string if no bits are set).  The least 
    significant bit in the value is mapped to element 0 of the supplied list.
    """
    return maskIntToList(taglist,int(val))

def maskIntToList(taglist,mask):
    """
    The supplied value is a bit mask.  This function returns a concatenation of 
    values from the supplied taglist string corresponding to those bits that are set,
    (or an empty string if no bits are set).  The least significant bit in the value is
    mapped to element 0 of the supplied list.
    """
    if taglist:
        t = (mask&0x1 and taglist[0]) or ""
        return t+maskToList(taglist[1:],mask>>1)
    return ""

def idn(x): 
    """
    Identity function (for use with getMapParams)
    """
    return x

def stripReservedNameChars(nam):
    """
    Return identifier with reserved characters removed
    """
    reservedChars = """<>& %?:;+"'"""
    return "".join([c for c in nam if c not in reservedChars])

def getParams(elem,attrnames,more=None):
    """
    Return list of parameters corresponding to named attributes, 
    concatenated with the result of applying the supplied function 
    to the element.
    """
    return getMapParams(elem,map((lambda v: (v,idn)), attrnames),more)

def getMapParams(elem,attrmap,more=None):
    """
    The supplied 'attrmap' is a list of (name,function) pairs.
    This function returns a list of parameters corresponding to named 
    attributes from each of these pairs, converted using the associated 
    functions, concatenated with the result of applying the supplied 'more' 
    function to the element.
    """
    def getmapattr(p):
        nam, fn = p
        return fn( elem.getAttribute(nam) )
    params = ";".join(map(getmapattr,attrmap))
    if more: params = params + ";" + more(elem)
    return params

def getNameText(elem):
    return stripReservedNameChars(getElemText(elem))

def serialConfig(elem):
    # Return serial config command parameters
    # <SE fl="64"/>  ->  CR4;0:
    sflg = int(elem.getAttribute("fl"))
    return str((sflg>>4)&0xF)+";"+str(sflg&0xF)

def mimicLoHiFade(elem):
    # return Mimic lo/hi/faderate command parameters
    # <MM lo="2" hi="63" dig="1985229328" an="-1" fr="8"/>
    # <MM lo="2" hi="63" dig="1985229328" an="-1" fr="8" fl="0"/>
    if elem.getAttribute("fl"):
        par = getParams(elem,["lo","hi","fr","fl"])
    else:
        par = getParams(elem,["lo","hi","fr"])
    return par

def mimicParams(chan,ad,attr):
    # return function for deriving Mimic channel configuration command parameters
    def params(elem):
        mchan = (int(elem.getAttribute(attr)) >> (chan*4)) & 0xF
        if mchan >= 8: return None
        return ad+str(chan)+";"+str(mchan)
    return params

def mimicAChan(chan):
    # return function for analog Mimic channel configuration command parameters
    return mimicParams(chan,"A","an")

def mimicDChan(chan):
    # return digital Mimic channel configuration command parameters
    return mimicParams(chan,"D","dig")

def idValAttr(elem):
    # return command parameters corresponding to 'id="x" Value="y"'
    return getParams(elem,["id","Value"])

def idNameAttr(elem):
    # return command parameters corresponding to 'id="x" Name="y"'
    ###return getParams(elem,["id","Name"])
    attrmap = [("id",idn),("Name",stripReservedNameChars)]
    return getMapParams(elem, attrmap)

def idElemText(elem):
    # return command parameters corresponding to 'id="x"' and body text
    return getParams(elem,["id"],getElemText)

def trigger(trgname,opt,base):
    def mkInt(s):
        return int(s or "0")
    # Retrieve sub-element with trigger attributes
    elem = base.getElementsByTagName(trgname)[0]
    # Extract trigger parameters from Opt and B1 B2 B3 B4 attributes
    (b1,b2,b3,b4) = map( compose(mkInt,elem.getAttribute), ("B1","B2","B3","B4") )    
    # Construct result of form:
    # {A|D}<chn>;<setpt>;<action>;<dwelltime>;<udptype>;<assocval>;<b4>;<opt>
    if b2 & 0x80:
        ads    = "A"
        opchan = (b2 >> 4) & 0x7    # Analog output channel (0-7)
        setpt  =  b2       & 0xF    # Set point number (0-15)
    else:
        ads    = "D"
        opchan = b2 & 0xF           # Digital output channel (0-15)
        if b2&0x40: ads = "S"       # Digital or scene output?
        setpt  = 0                  # No set point

    action = b1        & 0xF        # action number
    dwtime = (b1 >> 4) & 0x3        # dwell time
    udpopt = (b1 >> 6) & 0x3        # UDP (0-none,1-general,2-remote,3-alarm)

    assocv = b3                     # associated value (was remote)
    
    result = ( ads+str(opchan)+
               ";"+str(setpt)+
               ";"+str(action)+
               ";"+str(dwtime)+
               ";"+str(udpopt)+
               ";"+str(assocv) )
    # b4 and opt are not defined for all webbricks
    # opt is used only if b4 is present
    if b4:
        result += ";"+str(b4)       # Add 'B4' attribute if present
        if opt: result += ";"+opt   # Add 'Opt' attribute if present
    return result

def trigger65(trgname,opt,base):
    def mkInt(s):
        return int(s or "0")
    # Retrieve sub-element with trigger attributes
    elem = base.getElementsByTagName(trgname)[0]
    # Extract trigger parameters from Opt and B1 B2 B3 B4 attributes
    (b1,b2,b3,b4) = map( compose(mkInt,elem.getAttribute), ("B1","B2","B3","B4") )    
    # Construct result of form:
    # {A|D}<chn>;<setpt>;<action>;<dwelltime>;<udptype>;<assocval>;<b4>;<opt>
    if b2 & 0x80:
        ads    = "A"
        opchan = (b2 >> 4) & 0x7    # Analog output channel (0-7)
        setpt  =  b2       & 0xF    # Set point number (0-15)
    else:
        ads    = "D"
        opchan = b2 & 0xF           # Digital output channel (0-15)
        if b2&0x40: ads = "S"       # Digital or scene output?
        setpt  = 0                  # No set point

    udpopt = (b1 >> 7) & 0x1        # UDP (0-none,1-general)
    dwtime = 0                      # default dwell time
    action = 0

    b1 = b1 & 0x7F
    if b1 >= 0x60:
        # dwell group
        action = (b1 >> 3 ) & 0x03  # action number
        action = (18,19,6,5)[action]
        dwtime = b1 & 0x7           # dwell time, now bottom 3 bits
    elif b1 >= 0x40:
        #not used
        pass
    elif b1 >= 0x20:
        # not used
        pass
    else:
        # group 1
        action = b1 & 0x1F        # action number
    assocv = b3                     # associated value (was remote)
    result = ( ads+str(opchan)+
               ";"+str(setpt)+
               ";"+str(action)+
               ";"+str(dwtime)+
               ";"+str(udpopt)+
               ";"+str(assocv) )
    # b4 and opt are not defined for all webbricks
    # opt is used only if b4 is present (non-zero)
    if b4:
        result += ";"+str(b4)       # Add 'B4' attribute if present
        if opt: result += ";"+opt   # Add 'Opt' attribute if present
    return result

def idTrigger(elem):
    # <CD id = "2" Name="Pb-2" Opt="123">
    #   <Trg B1="69" B2="2" B3="0" B4="0" />
    # </CD>
    opt = elem.getAttribute("Opt")
    return getParams(elem,["id"],curry(trigger,"Trg",opt))

def idTrigger65(elem):
    # <CD id = "2" Name="Pb-2" Opt="123">
    #   <Trg B1="69" B2="2" B3="0" B4="0" />
    # </CD>
    opt = elem.getAttribute("Opt")
    return getParams(elem,["id"],curry(trigger65,"Trg",opt))

def idTempLo(elem):
    return idAnalogIn(elem, "L", div16, "TrgL")

def idTempHi(elem):
    return idAnalogIn(elem, "H", div16, "TrgH")

def idTempLo65(elem):
    return idAnalogIn65(elem, "L", div16, "TrgL")

def idTempHi65(elem):
    return idAnalogIn65(elem, "H", div16, "TrgH")

def idAnalogLo(elem):
    return idAnalogIn(elem, "L", ident, "TrgL")

def idAnalogHi(elem):
    return idAnalogIn(elem, "H", ident, "TrgH")

def idAnalogLo65(elem):
    return idAnalogIn65(elem, "L", ident, "TrgL")

def idAnalogHi65(elem):
    return idAnalogIn65(elem, "H", ident, "TrgH")

def idAnalogIn(elem,hilo,valmap,trgnam):
    # <CT id="0" Name="Temp-1">
    #   <TrgL Val="-800" B1="192" B2="0" B3="0" B4="0" />
    #   <TrgH Val="1600" B1="192" B2="0" B3="0" B4="0" />
    # </CT>
    #
    # (also <CI> elements)
    return getParams(elem,["id"],curry(idAnalogThreshold,hilo,valmap,trgnam))
    pass

def idAnalogIn65(elem,hilo,valmap,trgnam):
    # <CT id="0" Name="Temp-1">
    #   <TrgL Val="-800" B1="192" B2="0" B3="0" B4="0" />
    #   <TrgH Val="1600" B1="192" B2="0" B3="0" B4="0" />
    # </CT>
    #
    # (also <CI> elements)
    return getParams(elem,["id"],curry(idAnalogThreshold65,hilo,valmap,trgnam))

#TODO: check WB6.1 commands for analog thresholds
def idAnalogThreshold(hilo,valmap,trgnam,elem):
    # returns "{H|L};<threshold>;{A|D}<chn>;<setpt>;<action>;<dwelltime>;<udptype>;<remotechan>
    trg = elem.getElementsByTagName(trgnam)[0]
    val = trg.getAttribute("Val") or trg.getAttribute("Lo") or trg.getAttribute("Hi") 
    Trace("trg %s, val %s"%(getElemXml(trg),val), "WebBrickConfig.idAnalogThreshold")
    return hilo+";"+valmap(val)+";"+trigger(trgnam,None,elem)
    
def idAnalogThreshold65(hilo,valmap,trgnam,elem):
    # returns "{H|L};<threshold>;{A|D}<chn>;<setpt>;<action>;<dwelltime>;<udptype>;<remotechan>
    trg = elem.getElementsByTagName(trgnam)[0]
    val = trg.getAttribute("Val") or trg.getAttribute("Lo") or trg.getAttribute("Hi") 
    Trace("trg %s, val %s"%(getElemXml(trg),val), "WebBrickConfig.idAnalogThreshold")
    return hilo+";"+valmap(val)+";"+trigger65(trgnam,None,elem)
    
# Days are bitmapped in the XML and a string of numbers in the command.
# The XML is literal data and it is easier for anyone using the command to put 0123456 etc.
# i.e. Sunday only is 1 in the XML and the string 0 in the command
# Monday to Fri is 62 in the XML and 12345 in the command.
#
def idSchedule(elem):
    # <CE id="5" Days="5" Hrs="23" Mins="59" >
    #   <Trg B1="192" B2="0" B3="0" B4="0" />
    # </CE>
    attrmap = [("id",idn),("Days",curry(maskToList,"0123456")),("Hrs",idn),("Mins",idn)]
    return getMapParams(elem, attrmap, curry(trigger,"Trg",None))

def idSchedule65(elem):
    # <CE id="5" Days="5" Hrs="23" Mins="59" >
    #   <Trg B1="192" B2="0" B3="0" B4="0" />
    # </CE>
    attrmap = [("id",idn),("Days",curry(maskToList,"0123456")),("Hrs",idn),("Mins",idn)]
    return getMapParams(elem, attrmap, curry(trigger65,"Trg",None))

def idScene(elem):
    # <CC id = "6" Dm="0" Ds="0" Am="10" Av="21554" />
    def mkDout(i,dm,ds):
        m = 1 << i
        return cond(m&dm,(cond(m&ds,"N","F")),"I")
    def mkAout(i,am,as):
        return cond(am & (1 << i), "S"+str((as>>(i*4))&0xF), "I")
    (dm,ds,am,av) = map( compose(int,elem.getAttribute), ("Dm","Ds","Am","Av") )
    params = getParams(elem,["id"]) + ";"
    for i in range(16): params = params + mkDout(i,dm,ds)
    for i in range(4):  params = params + ";" + mkAout(i,am,av)
    return params

# End $Id: WebBrickConfig.py 2612 2008-08-11 20:08:49Z graham.klyne $
