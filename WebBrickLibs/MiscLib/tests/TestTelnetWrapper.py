# $Id: TestTelnetWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
#
# Support functions for running different test suites
#
# Test suites are selected using a command line argument or supplied parameter:
#
# Test classes are:
#   "unit"          These are stand-alone tests that all complete within a few 
#                   seceonds and do not depend on resources external to the 
#                   package being tested, (other than other libraries used).
#   "component"     These are tests that take loonger to run, or depend on 
#                   external resources, (files, etc.) but do not depend on 
#                   external services.
#   "integration"   These are tests that exercise interactions with seperate
#                   services.
#   "pending"       These are tests that have been designed and created, but 
#                   for which the corresponding implementation has not been
#                   completed.
#   "all"           return suite of unit, component and integration tests
#   name            a single named test to be run.
#
import sys
import unittest
import threading
from Utils import TestTCPServer
import time
sys.path.append("../..")

from MiscLib.TelnetWrapper import *

#use this class to emulate two different threads calling the same method at the same time to test for thread saftey, event is a threading.Event and
#you should block in another thread using event.wait() before calling the method you wish to test
class syncfunctioncall(threading.Thread):
        def __init__(self,event,functionpointer,parameter = ''):
            self.syncevent = event
            self.function = functionpointer
            self.parameter = parameter
            threading.Thread.__init__( self )
            threading.Thread.start( self )
        def run(self):
            time.sleep(1)            
            if self.parameter == '':
                self.syncevent.set()
                self.function()
            else:
                self.syncevent.set()
                self.function(self.parameter)


testConfigstring = "hello"
testConfiglines = ["hello1\n","hello2\n","hello3\n"]

class TestTelnet(unittest.TestCase):
    
    def setUp(self):
        
        self._log = logging.getLogger( "TestTelnet" )
        self._log.debug("\n\nsetUp")
        self.telnetServer = TestTCPServer(58450) # we set up a tcp server to use as a telnet server
        self.telnetServer.start()
        self.telnetServer.ready.wait()
        self.telnetWrapper = TelnetWrapper("127.0.0.1",58450,'\n')
 
    def makelargestring(self,char):
        self.bigstring = ''
        for i in range(1,20000):
            self.bigstring +=  char   
        return self.bigstring
            
    def tearDown(self):
        self._log.debug( "\n\ntearDown" )
        self.telnetWrapper.close()
        self.telnetServer.stop()  
           
    def testWrite(self):
        #write our test string using the wrapper
        self.telnetWrapper.write(testConfigstring)
        #give the server time to recieve it then check if its buffer matches test string
        time.sleep(1)
        assert self.telnetServer.data == testConfigstring
   
    def testRead(self):
        # tell server to send out our test string
        self.telnetServer.send(testConfigstring)
        # give the server time to send it
        time.sleep(1)
        #check our wrapper to see if we have it
        self.textbuffer = self.telnetWrapper.read()
        assert (self.textbuffer == testConfigstring)
        
    def testReadNonASCII(self):
        #test to see if we recieve non ascii values ok
        testchar = chr(255)
        self._log.debug('Non ASCII Char == %s' %testchar)
        # tell server to send out our test string
        self.telnetServer.send(testchar)
        # give the server time to send it
        time.sleep(1)
        #check our wrapper to see if we have it
        self.textbuffer = self.telnetWrapper.read()
        self._log.debug('Recieved is : ##%s##' %self.textbuffer)
        assert (self.textbuffer == testchar)   
        
    def testReadline(self):
    
        # tell server to send out our test strings
        for line in testConfiglines:
            self._log.debug("Sending : %s"%line)
            self.telnetServer.send(line)
            time.sleep(1)
        # give the server time to send it

        self.textbuffer = []
        for line in testConfiglines:
            self._log.debug("Expected : %s"%line)
                #check our wrapper to see if we have it
            temp = self.telnetWrapper.readline()
            self._log.debug("Got : %s" %temp)
            self.textbuffer.append(temp)
                
        assert (self.textbuffer[0] == "hello1")
        assert (self.textbuffer[1] == "hello2")
        assert (self.textbuffer[2] == "hello3")
            
    def testDoubleWrite(self):
        #set up sync event
        self.event = threading.Event()
        self.aaa = self.makelargestring('a')
        self.bbb = self.makelargestring('b')
        #syncwrite will start itself in a new thread
        self.syncwrite = syncfunctioncall(self.event,self.telnetWrapper.write,self.bbb)
        # synchronize with syncwrite
        self.event.wait() 
        #write something at the same time as syncwrite
        self.telnetWrapper.write(self.aaa)
        # give the server time to fetch the new data
        time.sleep(1) 
        assert self.aaa in self.telnetServer.data
        assert self.bbb in self.telnetServer.data
        return    

    def testwriteServerdeath(self):
        self.event = threading.Event()
        self.aaa = self.makelargestring('a')
        self.syncdisconnect = syncfunctioncall(self.event,self.telnetServer.stop)
        self.event.wait()
        self.telnetWrapper.write(self.aaa)
        return
        
    def testreadServerdeath(self):
        self.event = threading.Event()
        self.aaa = self.makelargestring('a')
        self.telnetServer.send(self.aaa)
        time.sleep(1)
        self.syncdisconnect = syncfunctioncall(self.event,self.telnetServer.stop)
        self.event.wait()        
        self.telnetWrapper.read()
        return
        
    def testreadlineServerdeath(self):
        self.event = threading.Event()
        self.newline = "newline\n"
        self.telnetServer.send(self.newline)
        time.sleep(1)
        self.syncdisconnect = syncfunctioncall(self.event,self.telnetServer.stop)
        self.event.wait()
        self.telnetWrapper.readline()
        return
        
    def testDummy(self):
        return
from MiscLib import TestUtils
def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ 
            "testRead",
            "testWrite",
            "testDoubleWrite",
            "testReadline",
            "testwriteServerdeath",
            "testreadServerdeath",
            "testreadlineServerdeath"
            ],
        "component":
            [ 
            "testDummy"
            ],
        "integration":
            [ 
            "testDummy"
            ],
        "pending":
            [ 
            "testReadNonASCII", 
            ]
        }
    return TestUtils.getTestSuite(TestTelnet, testdict, select=select)



if __name__ == "__main__":
    TestUtils.runTests("TestTelnet.log", getTestSuite, sys.argv)

# $Id: TestTelnetWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
