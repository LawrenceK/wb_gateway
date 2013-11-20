# $Id: TestWebBrickConfig.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick configuration
# See http://pyunit.sourceforge.net/pyunit.html
#
# TODO: Create MockBrick WebBrick "mock object"
# TODO: Load commands to MockBrick, read back and confirm XML as expected
# TODO: Create new test harness to talk to real WebBrick
# TODO: Run all tests against real WebBrick
# TODO: Create command line utility to load/save WebBrick config
# TODO: Create test script to confirm round-tripping using 
#

import unittest
import string
import os
import sys

sys.path.append("../..")
sys.path.append("../../../WebBrickLibs")
sys.path.append("../../../WebBrickLibs/WebBrickLibs/tests")

from MiscLib import TestUtils

from MiscLib.Combinators import compose, curry
from MiscLib.DomHelpers import parseXmlFile, parseXmlString, getAttrText, getElemXml
from MiscLib.ScanFiles import readFile

from WebBrickConfig import WebBrickConfig

from TestWbConfig import TestWbConfig

# Helper for string suffixc testing
def endsWith(base,suff):
    return base[-len(suff):] == suff

# Helper for DOM processing
def getNodeListText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

# WebBrick configuration command test cases
class TestWebBrickConfig(unittest.TestCase):

    _wbAddress  = "10.100.100.100"      # Default IP address
    _wbPassword = "password"            # Default password

    def setUp(self):
        self.wbconfig = WebBrickConfig.WebBrickConfig()
        self.respath  = "./resources/"
        self.override = { "password" : TestWebBrickConfig._wbPassword,
                          "IP"       : TestWebBrickConfig._wbAddress
                        }
        return

    def tearDown(self):
        return

    def doAssert(self, cond, msg):
        assert cond , msg

    def test0Null(self):
        assert True, 'Null test failed'

    def test1Suff1(self):
        assert endsWith("xxx","xxx")

    def test1Suff2(self):
        assert endsWith("yyyzzz","zzz")

    def test1Suff3(self):
        assert not endsWith("xxxyyy","xxx")

    def test1Apply(self):
        # Is function application like BCPL?  (fn can be a variable)
        def ap(f,v): return f(v)
        def inc(n): return n+1
        assert ap(inc,2)==3

    def test1Curry(self):
        def f(a,b,c): return a+b+c
        g = curry(f,1,2)
        assert g(3) == 6

    def test1Compose(self):
        def f(a,b,c): return a+b+c
        def g(a,b):   return a*b
        h = compose(f,g,1000,200)
        assert h(3,4) == 1212, "h(3,4) is "+str(h(3,4))

    def test2Cwd(self):
        cwd = os.getcwd() 
        assert endsWith(cwd, "tests"), "Cwd is " + cwd

    def testReadConfig1(self):
        assert readFile(self.respath+"test1.xml"), "Read file 'test1.xml' failed"

    def testReadConfig2(self):
        assert readFile(self.respath+"test2.xml"), "Read file 'test2.xml' failed"

    def testReadConfig3(self):
        t1 = readFile(self.respath+"test1.xml")
        assert t1 == """<WebbrickConfig Ver="^SwVerMajor.^SwVerMinor.^SwVerBuild"/>\n""", "test1.xml is: "+t1

    def testParseConfigString(self):
        config = (
         """<?xml version="1.0" encoding="iso-8859-1" ?>
            <WebbrickConfig Ver="^SwVerMajor.^SwVerMinor.^SwVerBuild">
                <NN>^NodeName</NN>
                <SN>^NodeNumber</SN>
                <SRs>
                    <SR id="0" Value="^Rot0Step"/>
                    <SR id="1" Value="^Rot1Step"/>
                </SRs>
                <SF>^FadeRate</SF>
                <CWs>
                    <CW id="0">^Dw0</CW>
                    <CW id="1">^Dw1</CW>
                    <CW id="2">^Dw2</CW>
                    <CW id="3">^Dw3</CW>
                </CWs>
                <MM lo="4" hi="63" fr="2" dig="1985229328" an="12816" />
            </WebbrickConfig>
         """)
        assert parseXmlString(config), "Parse XML string failed"

    def testParseConfigFile1(self):
        assert parseXmlFile(self.respath+"test2.xml"), "Parse file 'test2.xml' failed"

    def testParseConfigFile2(self):
        dom = parseXmlFile(self.respath+"test2.xml")
        cws = dom.getElementsByTagName("CWs")[0]
        cw2 = cws.getElementsByTagName("CW")[2]
        id2 = getAttrText(cw2,"id")
        assert id2 == "2", """Wrong attribute value for <CW id="2">^Dw2</CW>: """ + id2
        dw2 = WebBrickConfig.getElemText(cw2)
        assert dw2 == "^Dw2", """Wrong content value for <CW id="2">^Dw2</CW>: """ + dw2

    def testConvertConfigParam1(self):
        dom = parseXmlFile(self.respath+"WbCfg-Public.xml")
        srs = dom.getElementsByTagName("SRs")[0]
        sr1 = srs.getElementsByTagName("SR")[1]
        par = WebBrickConfig.idValAttr(sr1)
        assert par == "1;8", """Wrong param for <SR id="1" Value="8"/>: """ + par

    def testConvertConfigParam2(self):
        dom = parseXmlFile(self.respath+"WbCfg-Public.xml")
        cws = dom.getElementsByTagName("CWs")[0]
        cw2 = cws.getElementsByTagName("CW")[2]
        par = WebBrickConfig.idElemText(cw2)
        assert par == "2;60", """Wrong param for <CW id="2">60</CW>: """ + par

    def testConvertConfigParam3(self):
        dom = parseXmlFile(self.respath+"WbCfg-Public.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd3 = cds.getElementsByTagName("CD")[3]
        par = WebBrickConfig.idTrigger(cd3)
        assert par == "3;D3;0;1;3;1;0", """Wrong param for <CD id = "3"><Trg B1="113" B2="3" B3="0" />: """ + par

    def testConvertConfigParam4(self):
        dom = parseXmlFile(self.respath+"WbCfg-Public.xml")
        cts = dom.getElementsByTagName("CTs")[0]
        ct4 = cts.getElementsByTagName("CT")[4]
        par = WebBrickConfig.idAnalogLo(ct4)
        # returns "chn;{H|L};<threshold>;{A|D}<chn>;<setpt>;<action>;<dwelltime>;<udptype>;<remotechan>
        assert par == "4;L;-800;D0;0;0;0;3;0", \
               """Wrong param for <CT id = "4"><TrgL Val="-800" B1="192" B2="0" B3="0" />: """ + par

    def testConvertConfigParam5(self):
        dom = parseXmlFile(self.respath+"WbCfg-Public.xml")
        ces = dom.getElementsByTagName("CEs")[0]
        ce5 = ces.getElementsByTagName("CE")[5]
        par = WebBrickConfig.idSchedule(ce5)
        assert par == "5;02;23;59;D0;0;0;0;3;0", \
               """Wrong param for <CE id="5" Days="5" Hrs="23" Mins="59"><Trg B1="192" B2="0" B3="0" />: """ + par

    def testConvertConfigParam6(self):
        dom = parseXmlFile(self.respath+"WbCfg-Public.xml")
        ccs = dom.getElementsByTagName("CCs")[0]
        cc6 = ccs.getElementsByTagName("CC")[6]
        par = WebBrickConfig.idScene(cc6)
        assert par == "6;INFNIIIIIIIIIIII;I;S3;I;S5", \
               """Wrong param for <CC id = "6" Dm="14" Ds="11" Am="10" Av="21554" />: """ + par

    def testConvertConfigParam7(self):
        dom = parseXmlFile(self.respath+"WbCfg-Public.xml")
        ir7 = dom.getElementsByTagName("IR")[0]
        ia7 = WebBrickConfig.maskInt(0x1F)(ir7)
        assert ia7 == "29", \
               """Wrong address for <IR>93</IR>: %s, expected 29""" + ia7
        it7 = WebBrickConfig.maskNF(0x20)(ir7)
        assert it7 == "F", \
               """Wrong transmit enable for <IR>93</IR>: %s, expected F""" + it7
        ir7 = WebBrickConfig.maskNF(0x40)(ir7)
        assert ir7 == "N", \
               """Wrong transmit enable for <IR>93</IR>: %s, expected N""" + ir7

    def testConvertConfigParam8(self):
        dom = parseXmlFile(self.respath+"WbCfg-Interesting.xml")
        #  <MM lo="4" hi="63" fr="2" dig="1985229328" an="12816" />
        mm8 = dom.getElementsByTagName("MM")[0]
        lo8 = getAttrText(mm8,"lo")
        assert lo8 == "4", \
               """Wrong value for <MM lo=.../>: %s, expected %s""" % (lo8,"4")
        hi8 = getAttrText(mm8,"hi")
        assert hi8 == "63", \
               """Wrong value for <MM hi=.../>: %s, expected %s""" % (hi8,"63")
        fr8 = getAttrText(mm8,"fr")
        assert fr8 == "2", \
               """Wrong value for <MM fr=.../>: %s, expected %s""" % (fr8,"2")
        di8 = getAttrText(mm8,"dig")
        assert int(di8) == 0x76543210, \
               """Wrong value for <MM dig=.../>: 0x%08X, expected 0x%08X""" % (int(di8),0x76543210)
        an8 = getAttrText(mm8,"an")
        assert int(an8) == 0x3210, \
               """Wrong value for <MM an=.../>: 0x%04X, expected 0x%04X""" % (int(an8),0x3210)

    def compareLists(self,c1,c2):
        # Compare lists, and return a pair of lists of elements 
        # in one but not in the other
        c1 = c1 or []
        c2 = c2 or []
        c1d = []
        c2d = []
        for c in c1: 
            if not (c in c2): c1d.append(c)
        for c in c2: 
            if not (c in c1): c2d.append(c)
        return (c1d,c2d)

    def compareCmds(self,(l1,c1),(l2,c2)):
        # Compare commands in c1 and c2, and return a list of differences.
        def reportDiff(l1,l2,c):
            return l1+": "+repr(c)+", not "+l2
        (c1d,c2d) = self.compareLists(c1,c2)
        c1e = map( curry(reportDiff,l1,l2), c1d )
        c2e = map( curry(reportDiff,l2,l1), c2d )
        return (c1e,c2e)

    def doTestConvertXmlToConfig(self,name,checkSpurious=False):
        dom = parseXmlFile(self.respath+name+".xml")
        return self.doTestConvertDomToConfig(dom,name,None,checkSpurious)

    def doTestConvertDomToConfig(self,dom,name,cfg=None,checkSpurious=False):
        # Local functions
        def notComment(cmd):
            return cmd.lstrip()[0] != '#'
        def cmdsHere((c1,c2)):
            return c1 and c2
        def identity(v):
            return v
        def stripTrailing(cmd):
            if cmd[-1] == "\n":  cmd = cmd[:-1]
            if cmd[-1] == ":":   cmd = cmd[:-1]
            if cmd[-1] == ";":   cmd = cmd[:-1]
            return cmd
        # Main test code
        if cfg:
            cfgold = cfg
        else:
            try:
                cfgfil = open(self.respath+name+".wb6")
            except IOError:
                assert False, "Config command file could not be opened: "+self.respath+name+".wb6"
            cfgold = map(stripTrailing,filter(notComment,cfgfil.readlines()))
            cfgfil.close()
        cfgnew = self.wbconfig.makeConfigCommands(dom,self.override)
        if cfg:
            cfgtmp = open(self.respath+"tmp/"+name+".tmp","w")
            for c in cfgnew: cfgtmp.write(c+":\n")
            cfgtmp.close()

        # pick out first 4 unequal commands
        (c1c,c1e) = self.compareCmds(("Converted",cfgnew),("Expected",cfgold))
        if (c1c and checkSpurious) or c1e: print
        if c1c and checkSpurious: print string.join(c1c,"\n")
        if c1e: print string.join(c1e,"\n")
        # select list of commands converted, not expected
        if checkSpurious:
            cfgcmp = c1c
            assert not cfgcmp, string.join(cfgcmp,"\n")
        # select list of commands expected, not converted
        cfgcmp = c1e
        assert not cfgcmp, string.join(cfgcmp,"\n")

    def testConvertXmlToConfig1(self):
        self.doTestConvertXmlToConfig("WbCfg-Public", checkSpurious=True)

    def testConvertXmlToConfig2(self):
        self.override["NodeName"] = "TestNodeNameOverride"
        self.doTestConvertXmlToConfig("WbCfg-GarageA")

    def testConvertXmlToConfig3(self):
        self.override["IP"] = "10.100.100.101"
        self.doTestConvertXmlToConfig("WbCfg-GarageB")

    def testConvertXmlToConfig4(self):
        self.doTestConvertXmlToConfig("WbCfg-GBoiler")

    def testConvertXmlToConfig5(self):
        self.doTestConvertXmlToConfig("WbCfg-GarageTop")

    def testConvertXmlToConfig6(self):
        self.doTestConvertXmlToConfig("WbCfg-Bedroom")

    def testConvertXmlToConfig7(self):
        self.doTestConvertXmlToConfig("WbCfg-Interesting")

    def testConvertConfigParam0_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd0 = cds.getElementsByTagName("CD")[0]
        cd0_xml = getElemXml(cd0)   # as string
        par = WebBrickConfig.idTrigger65(cd0)
        # <Trg B1="132" B2="0" B3="0" B4="0"/>
        assert par == "0;D0;0;4;0;1;0", "Wrong param for "+cd0_xml+": " + par

    def testConvertConfigParam1_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd1 = cds.getElementsByTagName("CD")[1]
        cd1_xml = getElemXml(cd1)   # as string
        par = WebBrickConfig.idTrigger65(cd1)
        # <Trg B1="124" B2="1" B3="0" B4="165"/>
        assert par == "1;D1;0;5;4;0;0;165;2", "Wrong param for "+cd1_xml+": " + par

    def testConvertConfigParam2_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd2 = cds.getElementsByTagName("CD")[2]
        cd2_xml = getElemXml(cd2)   # as string
        par = WebBrickConfig.idTrigger65(cd2)
        # <Trg B1="116" B2="2" B3="0" B4="165"/>
        assert par == "2;D2;0;6;4;0;0;165;2", "Wrong param for "+cd2_xml+": " + par

    def testConvertConfigParam3_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd3 = cds.getElementsByTagName("CD")[3]
        cd3_xml = getElemXml(cd3)   # as string
        par = WebBrickConfig.idTrigger65(cd3)
                      #3;D3;0;4;0;0;0
                      #\param{A\textbar{}D\textbar{}S\textbar{}T\textbar{}I}\param{targetChn}; 
                      #\param{SetPointNr}; 
                      #\param{actionType}; 
                      #\param{DwellNr}; 
                      #\param{UDPType}; 
                      #\param{AssociatedValue} 
                      #[; \param{OptValue}]:
        #assert par == "3;D3;0;4;0;0;0", """Wrong param for <CD id = "3"><Trg B1="4" B2="3" B3="0" B4="0" />: """ + par + "(" + cd3_xml + ")"
        #CHECKME:  I think the following is correct...
        # <Trg B1="9" B2="128" B3="0" B4="165"/>
        assert par == "3;A0;0;9;0;0;0;165;2", "Wrong param for "+cd3_xml+": " + par

    def testConvertConfigParam4_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd4 = cds.getElementsByTagName("CD")[4]
        cd4_xml = getElemXml(cd4)   # as string
        par = WebBrickConfig.idTrigger65(cd4)
        # <Trg B1="7" B2="64" B3="0" B4="165"/>
        assert par == "4;S0;0;7;0;0;0;165;2", "Wrong param for "+cd4_xml+": " + par

    def testConvertConfigParam5_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd5 = cds.getElementsByTagName("CD")[5]
        cd5_xml = getElemXml(cd5)   # as string
        par = WebBrickConfig.idTrigger65(cd5)
        # <Trg B1="16" B2="6" B3="0" B4="165"/>
        assert par == "5;D6;0;16;0;0;0;165;2", "Wrong param for "+cd5_xml+": " + par

    def testConvertConfigParam6_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd6 = cds.getElementsByTagName("CD")[6]
        cd6_xml = getElemXml(cd6)   # as string
        par = WebBrickConfig.idTrigger65(cd6)
        # <Trg B1="4" B2="75" B3="0" B4="165"/>
        assert par == "6;S11;0;4;0;0;0;165;2", "Wrong param for "+cd6_xml+": " + par

    def testConvertConfigParam7_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd7 = cds.getElementsByTagName("CD")[7]
        cd7_xml = getElemXml(cd7)   # as string
        par = WebBrickConfig.idTrigger65(cd7)
        # <Trg B1="4" B2="7" B3="0" B4="0"/>
        assert par == "7;D7;0;4;0;0;0", "Wrong param for "+cd7_xml+": " + par

    def testConvertConfigParam8_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd8 = cds.getElementsByTagName("CD")[8]
        cd8_xml = getElemXml(cd8)   # as string
        par = WebBrickConfig.idTrigger65(cd8)
        # <Trg B1="108" B2="3" B3="0" B4="111"/>
        assert par == "8;D3;0;19;4;0;0;111;3", "Wrong param for "+cd8_xml+": " + par

    def testConvertConfigParam9_v65(self):
        dom = parseXmlFile(self.respath+"WbCfg-65.xml")
        cds = dom.getElementsByTagName("CDs")[0]
        cd9 = cds.getElementsByTagName("CD")[9]
        cd9_xml = getElemXml(cd9)   # as string
        par = WebBrickConfig.idTrigger65(cd9)
        # <Trg B1="100" B2="4" B3="0" B4="111"/>
        assert par == "9;D4;0;18;4;0;0;111;3", "Wrong param for "+cd9_xml+": " + par

    def testConvertXmlToConfig0_v65(self):
        self.doTestConvertXmlToConfig("WbCfg-65", checkSpurious=True)

    def testConvertXmlToConfig1_v65(self):
        self.doTestConvertXmlToConfig("WbCfg1-65", checkSpurious=True)

    # the following characters should be stripped
    # unsigned char badChars[] = "<>& %?:;+'\"";
    def testStripReservedNameChars(self):
        newName = WebBrickConfig.stripReservedNameChars("Name 1")
        assert newName == "Name1", "Space not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name<1")
        assert newName == "Name1", "less than  not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name>1")
        assert newName == "Name1", "greater than not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name&1")
        assert newName == "Name1", "ambersand not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name%1")
        assert newName == "Name1", "percent  not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name?1")
        assert newName == "Name1", "question mark not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name:1")
        assert newName == "Name1", "colon not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name;1")
        assert newName == "Name1", "semi colon not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name+1")
        assert newName == "Name1", "plus sign  not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name'1")
        assert newName == "Name1", "single quote not allowed in name %s" % (newName)
        newName = WebBrickConfig.stripReservedNameChars("Name""1")
        assert newName == "Name1", "double quote not allowed in name %s" % (newName)

    def testNameNormalization(self):
        configxml = (
            """<?xml version="1.0" encoding="iso-8859-1" ?>
            <WebbrickConfig Ver="6.4.1898">

            <NN>Web Brick</NN>

            <CDs>
            <CD id="0" Name="DigIn%0" Opt="2">
            <Trg B1="4" B2="0" B3="0" B4="0"/>
            </CD>
            </CDs>

            <CTs>
            <CT id="1" Name="Temp?1">
            <TrgL Lo="-800" B1="0" B2="0" B3="0" B4="0"/>
            <TrgH Hi="1600" B1="0" B2="0" B3="0" B4="0"/>
            </CT>
            </CTs>

            <CIs>
            <CI id="2" Name="AnIn:2">
            <TrgL Lo="0" B1="0" B2="0" B3="0" B4="0"/>
            <TrgH Hi="100" B1="0" B2="0" B3="0" B4="0"/>
            </CI>
            </CIs>

            <NAs>
            <NA id="3" Name="AnOut;3"/>
            </NAs>

            <NOs>
            <NO id="4" Name="DigOut+4"/>
            </NOs>

            </WebbrickConfig> 
            """)
        configcmd = ["LGpassword"
            , "SS1"
            , "NNWebBrick"
            , "ND0;DigIn0"
            , "CD0;D0;0;4;0;0;0"
            , "NT1;Temp1"
            , "CT1;L;-50.0;D0;0;0;0;0;0"
            , "CT1;H;100.0;D0;0;0;0;0;0"
            , "NI2;AnIn2"
            , "CI2;L;0;D0;0;0;0;0;0"
            , "CI2;H;100;D0;0;0;0;0;0"
            , "NA3;AnOut3"
            , "NO4;DigOut4"
            , "SI10;100;100;100"
            , "SS2"
            ]
        dom = parseXmlString(configxml)
        self.doTestConvertDomToConfig(dom,"xxx",configcmd,checkSpurious=True)
        return

    # Sentinel/placeholder tests

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "Pending test"


# Assemble test suite
#
# Select is:
#   "unit"      return suite of unit tests only
#   "component" return suite of unit and component tests
#   "all"       return suite of unit, component and integration tests
#   name        a single named test to be run
# testargs is a list of argument name/value pairs that are stored into the test class
#
def getTestSuite(select="unit", testargs=[]):
    testdict = {
        "unit": 
            [ "testUnits"
            , "test0Null"
            , "test1Suff1"
            , "test1Suff2"
            , "test1Suff3"
            , "test1Apply"
            , "test1Curry"
            , "test1Compose"
            , "test2Cwd"
            , "testReadConfig1"
            , "testReadConfig2"
            , "testReadConfig3"
            , "testParseConfigString"
            , "testParseConfigFile1"
            , "testParseConfigFile2"
            , "testConvertConfigParam1"
            , "testConvertConfigParam2"
            , "testConvertConfigParam3"
            , "testConvertConfigParam4"
            , "testConvertConfigParam5"
            , "testConvertConfigParam6"
            , "testConvertConfigParam7"
            , "testConvertConfigParam8"
            , "testConvertXmlToConfig1"
            , "testConvertXmlToConfig2"
            , "testConvertXmlToConfig3"
            , "testConvertXmlToConfig4"
            , "testConvertXmlToConfig5"
            , "testConvertXmlToConfig6"
            , "testConvertXmlToConfig7"
            , "testConvertConfigParam0_v65"
            , "testConvertConfigParam1_v65"
            , "testConvertConfigParam2_v65"
            , "testConvertConfigParam3_v65"
            , "testConvertConfigParam4_v65"
            , "testConvertConfigParam5_v65"
            , "testConvertConfigParam6_v65"
            , "testConvertConfigParam7_v65"
            , "testConvertConfigParam8_v65"
            , "testConvertConfigParam9_v65"
            , "testConvertXmlToConfig0_v65"
            , "testConvertXmlToConfig1_v65"
            , "testStripReservedNameChars"
            , "testNameNormalization"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            ],
        "pending":
            [ "testPending"
            ]
        }
    for (argname,argval) in testargs:
        if argval: setattr(TestWb6Commands, argname, argval)
    return TestUtils.getTestSuite(TestWebBrickConfig, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestWebBrickConfig._wbAddress  = TestWbConfig.WbAddress
    TestWebBrickConfig._wbPassword = "password"     # TestWbConfig.WbFactoryPw
    testargs = [ ("-a", "--address",  "ADR", "_wbAddress",  "IP address of WebBrick") 
               , ("-p", "--password", "PWD", "_wbPassword", "Password to access WebBrick")
               ]
    TestUtils.runTests("TestWebBrickConfig.log", getTestSuite, sys.argv, testargs)

# End.
