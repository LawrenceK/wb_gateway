# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

1# $Id: TestWrapperWrapper.py 2760 2008-09-19 14:29:53Z simon.hughes $
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

import time
sys.path.append("../..")

from MiscLib.WrapperReactor import *

class TestWrapper():
    def __init__(self):
        self.data = ''
        self.throwException = False
        self.lock = threading.Lock()
        
    def readline(self):
        self.lock.acquire()
        try:            
            if self.throwException:
                raise Exception('Test exception')
                return None
            temp = self.data
            self.data = ''
            return temp
        finally:
            self.lock.release()
            
    def close(self):
        self.lock.acquire()
        self.throwException = True
        self.lock.release()
                
    def throwexception(self):
        self.lock.acquire()
        self.throwException = True
        self.lock.release()
                
    def send(self,senddata):
        self.lock.acquire()
        self.data = senddata 
        self.lock.release()        

class TestWrapperReactor(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger ( "TestWrapperReactor" )
        self._log.debug("\n\n------------------setUp------------------\n\n")
        self._callBackQueue = Queue.Queue()
        
    def tearDown(self):
        self._log.debug("\n\n------------------tearDown------------------\n\n")    
    
    def callback(self,wrapperID,data):
        self._log.debug("\nRecieved callback for wrapper %s , data %s" %(wrapperID,data))
        self._callBackQueue.put((wrapperID,data),False)
        self._log.debug("\nQueue size is %s" %self._callBackQueue.qsize())
        self._log.debug("\nQueue empty is %s" %self._callBackQueue.empty())

    def makeWrappers(self,number):
        wrapperlist = []
        for x in range(0,number):
            testWrapper = TestWrapper()
            wrapperlist.append({'ID':x,'wrapper':testWrapper,'eol':'\n','callback':self.callback})
        return wrapperlist
        
    def testOneWrapper(self):
        self._log.debug('\nInitializing WrapperReactor')
        testWrapper = TestWrapper()
        wrapperlist = [{'ID':'test','wrapper':testWrapper,'eol':'\n','callback':self.callback}]
        wrapperReactor = WrapperReactor(wrapperlist)
        time.sleep(0.5)
        assert wrapperReactor.running
        self._log.debug('\nWrapperReactor initialized')
       
        self._log.debug('\nSending testdata')
        testWrapper.send('testdata')
        time.sleep(0.5)
        self._log.debug('\nData sent, checking callback queue : %s' %self._callBackQueue)
        assert self._callBackQueue.empty() == False
        data = self._callBackQueue.get(True)
        self._log.debug('\nData from callback queue is ##%s##' %data[1])
        assert data[0] == 'test'
        assert data[1] == 'testdata'
    
    def testTwoWrappers(self):
        self._log.debug('\nInitializing WrapperReactor')
        
        wrapperlist = self.makeWrappers(2)
        self._log.debug('\nWrapperlist is %s' %wrapperlist)
        wrapperReactor = WrapperReactor(wrapperlist)
        time.sleep(0.5)
        assert wrapperReactor.running
        self._log.debug('\nWrapperReactor initialized')
       
        self._log.debug('\nSending testdata')
        for x in wrapperlist:
            self._log.debug('\nSending wrapper%s --> %s' %(x["ID"],'testdata' + str(x["ID"])))
            x['wrapper'].send('testdata%s' %x["ID"])
            
        time.sleep(4)
        self._log.debug('\nData sent, checking callback queue : %s' %self._callBackQueue)
        
        assert self._callBackQueue.empty() == False
        counter = 0
        while self._callBackQueue.empty () == False:
            data = self._callBackQueue.get(True)
            self._log.debug('\nData from callback queue is ##%s##' %data[1])
            assert data[1] == ('testdata' + str(data[0]))
            counter += 1 
        assert counter == 2   
    
    def testManyWrappers(self):
        self._log.debug('\nInitializing WrapperReactor')
        
        wrapperlist = self.makeWrappers(200)
        self._log.debug('\nWrapperlist is %s' %wrapperlist)
        wrapperReactor = WrapperReactor(wrapperlist)
        time.sleep(0.5)
        assert wrapperReactor.running
        self._log.debug('\nWrapperReactor initialized')
       
        self._log.debug('\nSending testdata')
        for x in wrapperlist:
            x['wrapper'].send('testdata%s' %x["ID"])
            
        time.sleep(0.5)
        self._log.debug('\nData sent, checking callback queue : %s' %self._callBackQueue)
        
        assert self._callBackQueue.empty() == False
        counter = 0
        while self._callBackQueue.empty () == False:
            data = self._callBackQueue.get(True)
            self._log.debug('\nData from callback queue is ##%s##' %data[1])
            assert data[1] == ('testdata' + str(data[0]))
            counter += 1 
        assert counter == 200
        
    def testDisconnect(self):
        self._log.debug('\nInitializing WrapperReactor')
        
        wrapperlist=self.makeWrappers(5)
        self._log.debug('\nWrapperlist is %s' %wrapperlist)
        wrapperReactor = WrapperReactor(wrapperlist)
        time.sleep(0.5)
        assert wrapperReactor.running        
        self._log.debug('\nWrapperReactor initialized')
        for wrapper in wrapperlist:
            wrapper['wrapper'].throwexception()
        time.sleep(1)
        for wrapper in wrapperReactor.wrapperList():
            assert wrapper['wrapper'] == None
        
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
                    "testOneWrapper",
                    "testTwoWrappers",
                    "testManyWrappers",
                    "testDisconnect"
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
                    "testDummy"
                    ]
               }
    return TestUtils.getTestSuite(TestWrapperReactor, testdict, select=select)



if __name__ == "__main__":
    TestUtils.runTests("TestWrapperReactor.log", getTestSuite, sys.argv)

# $Id: TestReactorWrapper.py 2760 2008-09-19 14:29:53Z graham.klyne $
