# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestPanelHtml.py 2609 2008-08-11 20:03:27Z graham.klyne $
#
# Unit testing for WebBrick panel definition HTML conversions.
#

import sys
import unittest

# Extend python path to access other related modules
# sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../../WebBrickLibs")

from WebBrickGateway.PanelHtml import *
from MiscLib.ScanFiles import readDirNameFile
from MiscLib.Combinators import curry
from MiscLib.Functions import zipAll

class TestPanelDefinition(unittest.TestCase):
    def setUp(self):
        self.panelpath = "../../../../WebBrickPanel/src/test/resources/"
        self.xhtmlpath = "../resources/"
        return

    def tearDown(self):
        return

    # Actual tests follow

    def testFilter01(self):
        fullstr = "a b c\nd\te f"
        trimstr = list(stripSpaces(fullstr))
        expstr  = list("abcdef")
        assert trimstr==expstr, "stripSpaces, expected:\n"+expstr+"\nFound:\n"+trimstr

    def testFilter02(self):
        fullstr = "<!-abc-> <!--def--> <!- -ghi-->"
        trimstr = list(stripXmlComments(fullstr))
        expstr  = list("<!-abc->  <!- -ghi-->")
        assert trimstr==expstr, "stripSpaces, expected:\n"+expstr+"\nFound:\n"+trimstr

    def testFilter03(self):
        fullstr = "<!-abc-> <!--def--> <!- -ghi-->"
        trimstr = list(stripXmlSpaces(fullstr))
        expstr  = list("<!-abc-><!--ghi-->")
        assert trimstr==expstr, "stripSpaces, expected:\n"+expstr+"\nFound:\n"+trimstr

    def testXmlCompare(self):
        fullstr = "<!-abc-> <!--def--> <!- -ghi-->"
        trimstr = "<!-abc->\n<!- -ghi--> <!--def--> \n"
        assert compareXml(fullstr,trimstr)

    def testPanel01(self):
        deffile = "Test01-LightSwitch"
        return PanelXmlToHtmlTest(self.panelpath,self.xhtmlpath,deffile)

    def testPanel02(self):
        deffile = "Test02-LightSwitch"
        return PanelXmlToHtmlTest(self.panelpath,self.xhtmlpath,deffile)

# Test helper to construct dictionary from file and compare with a supplied value
def PanelXmlToHtmlTest(panelpath,xhtmlpath,deffile):
    # defdict = readPanelDefinition(panelpath,deffile)
    defhtml = makePanelHtml(panelpath,deffile)
    exphtml = readDirNameFile(xhtmlpath,deffile+".xhtml")
    if not compareXml(defhtml,exphtml):
        # assert False, "Panel def expected:\n    "+formatDict(expdict,4,60,0)+"\nFound:\n    "+formatDict(defdict,4,60,4)
        assert False, "Panel def expected:\n"+exphtml+"\nFound:\n"+defhtml

# Helper function to compare XML strings, ignoring spaces, newlines and XML comments
def compareXml(x1,x2):
    for c1,c2 in zipAll(stripXmlSpaces(x1),stripXmlSpaces(x2)):
        if c1 != c2: return False
    return True
   
# Helper function to strip spaces, newlines and XML comments from XML strings
# Returns an iterator
def stripXmlSpaces(x):
    return stripSpaces(stripXmlComments(x))
    # return composeFilters(stripSpaces,stripXmlComments)(x)

# Helper function to compose two iterators
def composeFilters(i1,i2):
    return i1([i for i in i2])

# Helper function to strip spaces and newlines from a string
def stripSpaces(x):
    for c in x:
        if c in " \t\n": continue   # Skip spaces, tabs, newlines
        yield c

# Helper function to XML comments from XML strings
def stripXmlComments(x):
    # State table for stripping XML comments
    stStripXmlComments = \
        { 0: match1('<',(1,stateFilterHold),(0,stateFilterPass))
        , 1: match1('!',(2,stateFilterHold),(0,stateFilterPass))
        , 2: match1('-',(3,stateFilterHold),(0,stateFilterPass))
        , 3: match1('-',(4,stateFilterDrop),(0,stateFilterPass))
        , 4: match1('-',(5,stateFilterDrop),(4,stateFilterDrop))
        , 5: match1('-',(6,stateFilterDrop),(4,stateFilterDrop))
        , 6: match1('>',(0,stateFilterDrop),(4,stateFilterDrop))
        }
    return stateFilter(stStripXmlComments,x)

# Simple state machine driven filter
#
# The state table is a dictionary indexed by state values, where the
# initial state is 0, and each entry is a function that accepts a next
# symbol and returns a pair of (next state, action), where action is 
# one of 'stateFilterPass', 'stateFilterDrop', 'stateFilterHold'.  
# stateFilterHold means that the disposition will be determined later.
#
# The result is an iterator that returns elements from the filtered 
# subsequence of the supplied sequence.
#
def stateFilter(stable,seq):
    queue = []
    state = 0
    for symbol in seq:
        (state,action) = stable[state](symbol)
        (queue,emit) = action(queue,symbol)
        for e in emit: yield e
    return
def stateFilterPass(q,n):
    return ([],q+[n])
def stateFilterDrop(q,n):
    return ([],[])
def stateFilterHold(q,n):
    return (q+[n],[])

# State transition function to match the specified symbol and return
# 'eqval' if matched, otherwise 'neval'
def match1(sym,eqval,neval):
    def m(sym,eqval,neval,next):
        if next==sym:  return eqval
        return neval
    return curry(m,sym,eqval,neval)

# State transition function to match one of several specified symbols
# and return a corresponding (state,action) pair, otherwise to return
# a default value if none is matched.
def matchN(matchvals,otherval):
    def m(matchvals,otherval,next):
        for (sym,eqval) in matchvals:
            if next==sym: return eqval
        return otherval
    return curry(m,matchvals,otherval)

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestPanelDefinition("testFilter01"))
    suite.addTest(TestPanelDefinition("testFilter02"))
    suite.addTest(TestPanelDefinition("testFilter03"))
    suite.addTest(TestPanelDefinition("testXmlCompare"))
    suite.addTest(TestPanelDefinition("testPanel01"))
    suite.addTest(TestPanelDefinition("testPanel02"))
    return suite

if __name__ == "__main__":
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(getTestSuite())
