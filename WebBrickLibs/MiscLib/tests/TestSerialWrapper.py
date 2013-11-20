# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

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


# NOTE - For this test to run a USB serial device with pins 2-3 (tx-rx) shorted must be connected on and available at /dev/ttyUSB0


import sys
import unittest
import threading
import time
sys.path.append("../..")

from MiscLib.SerialWrapper import *

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

class TestSerialWrapper(unittest.TestCase):
    
    def setUp(self):
        self.ninebytestring = "helloff\n"
        self.serialWrapper = SerialWrapper("/dev/ttyUSB0","115200","\n")
        self._log = logging.getLogger ( "TestSerialWrapper" )
        self._log.debug("\n\nsetUp")
        
 
    def makelargestring(self,char):
        self.bigstring = ''
        for i in range(1,65):
            self.bigstring +=  char   
        return self.bigstring
            
    def tearDown(self):
        self._log.debug( "\n\ntearDown" )
        self.serialWrapper.close()
           
    def testReadWrite(self):
        #write our test string using the wrapper
        self._log.debug( "\nTesting writing" )
        self.serialWrapper.write(self.ninebytestring)
        #give wait a moment so we are sure anything we send has arrived back
        time.sleep(1)
        self._log.debug( "\nTesting reading" )
        self.temp = self.serialWrapper.read()
        self._log.debug( "\nRead string is " + self.temp )
        assert self.temp == self.ninebytestring
    
    def testReadline(self):
        # tell wrapper to send out a couple of our test strings
        self._log.debug( "\nWriting strings so we can test readine" )
        self.serialWrapper.write(self.ninebytestring)
        self.serialWrapper.write(self.ninebytestring)
        self.serialWrapper.write(self.ninebytestring)
        self.serialWrapper.write(self.ninebytestring)
        # give the server time to send it
        time.sleep(1)
        self._log.debug( "\nTesting serialWrapper.readline()" )
        
        assert self.serialWrapper.readline() == 'helloff'
        assert self.serialWrapper.readline() == 'helloff'
        assert self.serialWrapper.readline() == 'helloff'
        assert self.serialWrapper.readline() == 'helloff'
    def testReadlineOffset(self):
        self.serialWrapper.close()
        self.serialWrapper= SerialWrapper("/dev/ttyUSB0","115200","\n",2)
        testOffset = "TESTSTRING\nTY"
        self._log.debug( "\nWriting strings so we can test readine" )
        self.serialWrapper.write(testOffset)
        self.serialWrapper.write(testOffset)
        self.serialWrapper.write(testOffset)
        self.serialWrapper.write(testOffset)
        # give the server time to send it
        time.sleep(1)
        self._log.debug( "\nTesting serialWrapper.readline()" )
        
        line1 = self.serialWrapper.readline()
        self._log.debug ("line 1 is %s" %line1)
        assert line1 == testOffset
                
        line2 = self.serialWrapper.readline()
        self._log.debug ("line 2 is %s" %line2)        
        assert line2 == testOffset
        
        line3 = self.serialWrapper.readline()
        self._log.debug ("line 3 is %s" %line3)       
        assert line3 == testOffset
        
        line3 = self.serialWrapper.readline()
        self._log.debug ("line 3 is %s" %line3)
        assert line3 == testOffset
        
    def testDoubleWrite(self):
        #set up sync event
        self.event = threading.Event()
        self.aaa = self.makelargestring('a')
        self.bbb = self.makelargestring('b')
        #syncwrite will start itself in a new thread
        self.syncwrite = syncfunctioncall(self.event,self.serialWrapper.write,self.bbb)
        # synchronize with syncwrite
        self.event.wait()
        #write something at the same time as syncwrite
        self.serialWrapper.write(self.aaa)
        # give the server time to fetch the new data
        time.sleep(1) 
        #self.serialWrapper.read() should read everything in the buffer if no number of bytes is specified
        self.tempbuffer = self.serialWrapper.read()
        self._log.debug( "\ntestDoubleWrite - recieved data is + " + self.tempbuffer )
        assert self.aaa in self.tempbuffer
        assert self.bbb in self.tempbuffer
        return    

    def testwriteServerdeath(self):
        self.serialWrapper.serialport.close()
        self.serialWrapper.write(self.ninebytestring)
        return
        
    def testreadServerdeath(self):
        self.serialWrapper.serialport.close()
        self.serialWrapper.read()
        return
        
    def testreadlineServerdeath(self):
        self.serialWrapper.serialport.close()
        self.serialWrapper.readline()
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
            "testDummy"
            ],
        "component":
            [ 
            "testReadWrite",
            "testDoubleWrite",
            "testReadline",
            "testwriteServerdeath",
            "testreadServerdeath",
            "testreadlineServerdeath",
            "testReadlineOffset"
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
    return TestUtils.getTestSuite(TestSerialWrapper, testdict, select=select)



if __name__ == "__main__":
    TestUtils.runTests("TestSerialWrapper.log", getTestSuite, sys.argv)

# $Id: TestTelnetWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
