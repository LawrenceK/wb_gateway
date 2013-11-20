# $Id: TestPersistFile.py 3499 2010-02-02 08:55:42Z philipp.schuster $
#

import redis
import getpass
import sys
import telnetlib

import sys, logging, time, os
from os.path import exists
import unittest
from shutil import copyfile

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

try:
    import cPickle as pickle
except ImportError:
    import pickle



testPersistCfg = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistDatabase' name='PersistDatabase' persistIP='127.0.0.1' persistPort='6379' persistDatabase='0'>
    </eventInterface>

    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="http://id.webbrick.co.uk/events/config/set">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/config/get">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events of this type -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

class TestPersistDatabase(unittest.TestCase):

    def persistDatabaseEmpty(self):
        host="127.0.0.1"
        port="6379"
        tn = telnetlib.Telnet(host, port)
        self._log.debug(tn.read_eager())
        tn.write("FLUSHDB\n")
        tn.close()

    def persistDatabaseWrite4(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set("http://id.webbrick.co.uk/events/config/set,test/source1.new",pickle.dumps("{'name':'value1'}"))
        r.set("http://id.webbrick.co.uk/events/config/set,test/source2.new",pickle.dumps("{'name':'value2'}"))
        r.set("http://id.webbrick.co.uk/events/config/set,test/source3.new",pickle.dumps("{'name':'value3'}"))
        r.set("http://id.webbrick.co.uk/events/config/set,test/source4.new",pickle.dumps("{'name':'value4', 'name2':'value5'}"))

    def queryDatabase(self, key):
        #self._log.info("Entering query database with key %s (cont.d)", key)
        r = redis.Redis(host='localhost', port=6379, db=0)
        value = r.get(key)
        if not value:
            value = {}
        else:
            value = pickle.loads(value)

        return value

    def setUp(self):
        self._log = logging.getLogger( "TestPersistDatabase" )
        self._log.debug( "\nsetUp" )
        self.persistDatabaseEmpty() 
        self._log.info("Emptying Database")
        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )
        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None
            
    def expectNevents(self, cnt ):
        idx = 2000
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)


    def testWriteEmptyDatabase(self):
        """
        Test to write one entry to an empty database
        """
        self._log.debug( "\ntestWriteEmptyDatabase" )
            
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist4',
                {'val':4} ) )
        self.expectNevents(2)
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/persist4"), {'val':4})
      

    def testDatabaseWriteNew(self):
        """
        Test to write new data to database using events 
        """
        self._log.debug( "\ntestDatabaseWrite4" )
            
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source1',
                {'name':'value1.0'}) )
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source2',
                {'name':'value2.0'}) )
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source3',
                {'name':'value3.0'}) )
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source4',
                {'name':'value4.0', 'name2':'value5.0'}) )                
        
        
        self.expectNevents(8)
        
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source1"), {'name':'value1.0'})
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source2"), {'name':'value2.0'})
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source3"), {'name':'value3.0'})        
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source4"), {'name':'value4.0', 'name2':'value5.0'})        
        
              
    
    def testDatabaseWrite4(self):
        """
        Test to over-write existing keys with new data; 4 keys present    
        """
        self.persistDatabaseEmpty() 
        self.persistDatabaseWrite4()
        self._log.debug( "\ntestDatabaseWrite4" )
            
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source1.new',
                {'name':'value1.0'}) )
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source2.new',
                {'name':'value2.0'}) )
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source3.new',
                {'name':'value3.0'}) )
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/source4.new',
                {'name':'value4.0', 'name2':'value5.0'}) )                
        self.expectNevents(8)
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source1.new"), {'name':'value1.0'})
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source2.new"), {'name':'value2.0'})
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source3.new"), {'name':'value3.0'})        
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source4.new"), {'name':'value4.0', 'name2':'value5.0'})   
             


    def testDatabaseWriteLoop(self):
        """
        Test to write x number of NvPs to empty database, default 2000
        """
        self.persistDatabaseEmpty() 
        self._log.debug( "\ntestDatabaseWriteLoop" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        for i in range(0,2000):  
            self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                   'test/source'+str(i)+'.new',
                   {'name'+str(i):'value'+str(i)+'.0'}) )
                   
        self.expectNevents(4000)
        
        for i in range(0,2000):
            self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/source"+str(i)+".new"), {'name'+str(i):'value'+str(i)+'.0'})
      
 
    def testDatabaseMultiValue(self):
        """
        Test to write multi value to database
        """
        self.persistDatabaseEmpty() 
        self._log.debug( "\ntestDatabaseMultiValue" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
               'test/multivalue',
               {0:0, 1:1, 1:'name', 'name':1, 'key':'var', 9:9 } ) )                  
        self.expectNevents(2)
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/multivalue"), {0:0, 1:1, 1:'name', 'name':1, 'key':'var', 9:9})

 
    def testDatabaseSameSource(self):
        """
        Test to multi-event, same source
        """
        self.persistDatabaseEmpty() 
        self._log.debug( "\ntestDatabaseSameSource" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        for i in range(0,2000):
            self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/config/set',
                   'test/same',
                   {1:0, 2:i } ) )   
           
        self.expectNevents(4000)
        self.assertEqual(self.queryDatabase("http://id.webbrick.co.uk/events/config/set,test/same"), {1:0, 2:1999})
            
                 
               
 
    def testCompress(self):
        """
        Test database compression    
        """
        self._aofFilePath = "/home/tombushby/Documents/Redis/redis2rc/redis-2.0.0-rc2/appendonly.aof"
        self._startSize = os.path.getsize(self._aofFilePath)       
        self.persistDatabaseEmpty() 
        self.persistDatabaseWrite4()
        self.persistDatabaseWrite4()
        self.persistDatabaseWrite4()
        self.persistDatabaseWrite4()                        
        self.persistDatabaseWrite4()
        self._log.debug( "\ntestDatabaseCompress" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistDatabase"), Event( 'http://id.webbrick.co.uk/events/time/minute',
                   'test/source',
                   {'hour':2, 'minute':5}) )
            
        time.sleep(5) # BGREWRITEAOF (compressing the AOF file) is a background process, it needs time          

        self._endSize = os.path.getsize(self._aofFilePath)
        self.assertEqual(self._startSize > self._endSize, True)
        
     
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
            [ "testWriteEmptyDatabase",
              "testDatabaseWriteNew",
              "testDatabaseWrite4",
              "testDatabaseWriteLoop",
              "testDatabaseMultiValue",
              "testDatabaseSameSource",
              "testCompress"

            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestPersistDatabase, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestPersistDatabase.log", getTestSuite, sys.argv)
