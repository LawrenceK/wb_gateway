# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestTCPWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
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
from Utils import *
import time
sys.path.append("../..")

from MiscLib.TCPWrapper import *

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
testConfigOffsetlines = ["hello1\nTY","hello2\nTY","hello3\nTY"]

class TestTCPWrapper(unittest.TestCase):
    
    def setUp(self):
        
        self._log = logging.getLogger( "TestTCPWrapper" )
        self._log.debug("\n\nsetUp")
        self.TCPServer = TestTCPServer(58450)
        self.TCPServer.start()
        self.TCPServer.ready.wait()
        self.tcpWrapper = TCPWrapper("127.0.0.1",58450,'\n')
 
    def makelargestring(self,char):
        self.bigstring = ''
        for i in range(1,20000):
            self.bigstring +=  char   
        return self.bigstring
            
    def tearDown(self):
        self._log.debug( "\n\ntearDown" )
        self.tcpWrapper.close()
        self.TCPServer.stop()  
           
    def testWrite(self):
        #write our test string using the wrapper
        self.tcpWrapper.write(testConfigstring)
        #give the server time to recieve it then check if its buffer matches test string
        time.sleep(1)
        assert self.TCPServer.data == testConfigstring
   
    def testRead(self):
        # tell server to send out our test string
        self.TCPServer.send(testConfigstring)
        # give the server time to send it
        time.sleep(1)
        #check our wrapper to see if we have it
        self.textbuffer = self.tcpWrapper.read()
        assert (self.textbuffer == testConfigstring)
        
    def testReadNonASCII(self):
        #test to see if we recieve non ascii values ok
        testchar = chr(255)
        self._log.debug('Non ASCII Char == %s' %testchar)
        # tell server to send out our test string
        self.TCPServer.send(testchar)
        # give the server time to send it
        time.sleep(1)
        #check our wrapper to see if we have it
        self.textbuffer = self.tcpWrapper.read()
        self._log.debug('Recieved is : ##%s##' %self.textbuffer)
        assert (self.textbuffer == testchar)   
        
    def testReadline(self):
    
        # tell server to send out our test strings
        for line in testConfiglines:
            self._log.debug("Sending : %s"%line)
            self.TCPServer.send(line)
            time.sleep(1)
        # give the server time to send it

        self.textbuffer = []
        for line in testConfiglines:
            self._log.debug("Expected : %s"%line)
                #check our wrapper to see if we have it
            temp = self.tcpWrapper.readline()
            self._log.debug("Got : %s" %temp)
            self.textbuffer.append(temp)
                
        assert (self.textbuffer[0] == "hello1\n")
        assert (self.textbuffer[1] == "hello2\n")
        assert (self.textbuffer[2] == "hello3\n")
        
    def testReadlineOffset(self):
        self.tcpWrapper.close()
        self.TCPServer.stop()        
        self.TCPServer = TestTCPServer(58450)
        self.TCPServer.start()
        self.TCPServer.ready.wait()
        self.tcpWrapper = TCPWrapper("127.0.0.1",58450,'\n',2)
        for line in testConfigOffsetlines:
            self._log.debug("Sending : %s"%line)
            self.TCPServer.send(line)
            time.sleep(1)
        # give the server time to send it

        self.textbuffer = []
        for line in testConfiglines:
            self._log.debug("Expected : %s"%line)
                #check our wrapper to see if we have it
            temp = self.tcpWrapper.readline()
            self._log.debug("Got : %s" %temp)
            self.textbuffer.append(temp)
                
        assert (self.textbuffer[0] == "hello1\nTY")
        assert (self.textbuffer[1] == "hello2\nTY")
        assert (self.textbuffer[2] == "hello3\nTY")
        
    def testDoubleWrite(self):
        #set up sync event
        self.event = threading.Event()
        self.aaa = self.makelargestring('a')
        self.bbb = self.makelargestring('b')
        #syncwrite will start itself in a new thread
        self.syncwrite = syncfunctioncall(self.event,self.tcpWrapper.write,self.bbb)
        # synchronize with syncwrite
        self.event.wait() 
        #write something at the same time as syncwrite
        self.tcpWrapper.write(self.aaa)
        # give the server time to fetch the new data
        time.sleep(1) 
        assert self.aaa in self.TCPServer.data
        assert self.bbb in self.TCPServer.data
        return    

    def testwriteServerdeath(self):
        self.event = threading.Event()
        self.aaa = self.makelargestring('a')
        self.syncdisconnect = syncfunctioncall(self.event,self.TCPServer.stop)
        self.event.wait()
        self.tcpWrapper.write(self.aaa)
        return
        
    def testreadServerdeath(self):
        self.event = threading.Event()
        self.aaa = self.makelargestring('a')
        self.TCPServer.send(self.aaa)
        time.sleep(1)
        self.syncdisconnect = syncfunctioncall(self.event,self.TCPServer.stop)
        self.event.wait()        
        self.tcpWrapper.read()
        return
        
    def testreadlineServerdeath(self):
        self.event = threading.Event()
        self.newline = "newline\n"
        self.TCPServer.send(self.newline)
        time.sleep(1)
        self.syncdisconnect = syncfunctioncall(self.event,self.TCPServer.stop)
        self.event.wait()
        self.tcpWrapper.readline()
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
            "testReadNonASCII",
            "testDoubleWrite",
            "testReadline",
            "testwriteServerdeath",
            "testreadServerdeath",
            "testreadlineServerdeath",
            "testReadlineOffset"
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
            "testDummy",  
            ]
        }
    return TestUtils.getTestSuite(TestTCPWrapper, testdict, select=select)



if __name__ == "__main__":
    TestUtils.runTests("TestTCPWrapper.log", getTestSuite, sys.argv)

# $Id: TestTCPWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
