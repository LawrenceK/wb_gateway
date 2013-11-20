# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestPersistFile.py 3736 2010-09-29 12:56:06Z tombushby $
#
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

refFile1 = "./resources/persist.xml.original"
refFile2 = "./resources/persist2.xml.original"
refFile3 = "./resources/persist3.xml.original"
outFile = "./TestOut/persist.xml"
outFileBak = "./TestOut/persist.xml.bak"
outFileDaily = "./TestOut/persist.xml.daily"

testPersistCfg = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='TestOut/persist'>
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

testPersistCfg2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='TestOut/persist'>
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

testPersistCfg3 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='TestOut/persist.xml'>
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

class TestPersistFile(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestPersistFile" )
        self._log.debug( "\nsetUp" )
        self.setCwd = False
        if exists("EventHandlers/tests/resources"):
            self.setCwd = True
            os.chdir("EventHandlers/tests")
            
        if exists(outFile):
            os.unlink( outFile )
        
        if exists(outFile+'.bak'):
            os.unlink( outFile+'.bak' )
            
        if exists(outFile+'.daily'):
            os.unlink( outFile+'.daily' )
        
        self.router = None
        self.loader = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        time.sleep(1)
        if self.setCwd:
            os.chdir("../..")
            
    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)

    def sendSeconds ( self ):
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/time/second',
                'time/second',
                {'val':1} ) )
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/time/second',
                'time/second',
                {'val':1} ) )
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/time/second',
                'time/second',
                {'val':1} ) )
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/time/second',
                'time/second',
                {'val':1} ) )
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/time/second',
                'time/second',
                {'val':1} ) )
                

    # Actual tests follow

    def testCreate_fromScratch(self):
        """ NOTE: This will throw an Error, since there is no persist file! This Error is expected and should occur!
        """
        self._log.debug( "\ntestCreate_fromScratch" )
            
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist4',
                {'val':4} ) )
        self.expectNevents(2)
        
        # thats all folks.
        self.failUnless( exists(outFile) )

    def testCreate_fromBak(self):
        self._log.debug( "\ntestCreate_fromBak" )
        copyfile( refFile1, outFileBak )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        # Only want to know if .bak was copied to outfile
        self.failUnless( exists(outFile) )
        
    def testCreate_fromDaily(self):
        self._log.debug( "\ntestCreate_fromDaily" )
        copyfile( refFile1, outFileDaily )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        # Only want to know if .daily was copied to outfile
        self.failUnless( exists(outFile) )
        
        
    def testCreateAndAdd(self):
        """ NOTE: This will throw an Error, since there is no persist file! This Error is expected and should occur!
        """
        self._log.debug( "\ntestCreateAndAdd" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist4',
                {'val':4} ) )

        self.expectNevents(2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist4" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], 4 )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist4" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 4 )

    def testCreateAndAdd2(self):
        """ NOTE: This will throw an Error, since there is no persist file! This Error is expected and should occur!
        """
        self._log.debug( "\ntestCreateAndAdd2" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist4',
                {'val':4} ) )

        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist5',
                {'val':5} ) )

        self.expectNevents(4)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist4" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], 4 )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist5" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 5 )
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist4" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val'], 4 )
        self.assertEqual( TestEventLogger._events[3].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "test/persist5" )
        self.assertEqual( TestEventLogger._events[3].getPayload()['val'], 5 )

    def testStartup(self):
        self._log.debug( "\ntestStartup" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.expectNevents(1)
               
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )

    def testStartup2(self):
        self._log.debug( "\ntestStartup2" )
        copyfile( refFile2, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        # copy baseline file to working.
        # expect a single event of the only persisted value

        self.expectNevents(2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist2" )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist" )

    def testStartup3(self):
        self._log.debug( "\ntestStartup3" )
        copyfile( refFile3, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        self.router.publish( EventAgent("TestPersistFile"), Events.evtRuntime5)

        # copy baseline file to working.
        # expect a single event of the only persisted value

        self.expectNevents(4)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist2" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val2'], '2' )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], '1' )

    def testStartup4(self):
        self._log.debug( "\ntestStartup" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg3) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        # expect a single event of the only persisted value

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )

    def testUpdateExist(self):
        self._log.debug( "\ntestUpdateExist" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )

        # copy baseline file to working.
        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist',
                {'val':3} ) )

        self.sendSeconds()

        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 3 )
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val'], 3 )
        


    def testUpdateExist2(self):
        self._log.debug( "\ntestUpdateExist2" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )

        # copy baseline file to working.
        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist',
                {'val':3} ) )
                
        self.sendSeconds()

        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 3 )
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val'], 3 )

    def testUpdateExistMultiValue(self):
        self._log.debug( "\ntestUpdateExistMultiValue" )
        copyfile( refFile3, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()
        
        self.expectNevents(2)
        

        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist2" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val2'], '2' )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], '1' )

        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist2',
                {'val2':3} ) )

        self.sendSeconds()
        
        self.expectNevents(4)
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist2" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val2'], 3 )
        self.assertEqual( TestEventLogger._events[3].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "test/persist2" )
        self.assertEqual( TestEventLogger._events[3].getPayload()['val'], '1' )
        self.assertEqual( TestEventLogger._events[3].getPayload()['val2'], 3 )
    
    def testDailyExists(self):
        self._log.debug( "\ntestDailyExists" )
        copyfile( refFile1, outFile )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        # send in 19.00 time event
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/time/minute',
                'time/minute',
                {'hour':19
                , 'minute': 5} ) )
        time.sleep(1)
        self.expectNevents(1)
        # Only want to know if current xml was coppied to .daily
        self.failUnless( exists(outFileDaily) )
    
    def testWriteNew(self):
        self._log.debug( "\ntestWriteNew" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )

        # copy baseline file to working.
        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist4',
                {'val':4} ) )

        self.sendSeconds()

        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist4" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 4 )
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist4" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val'], 4 )

    def testUpdateReload(self):
        self._log.debug( "\ntestUpdateReload" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )

        # copy baseline file to working.
        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist5',
                {'val':5} ) )

        self.sendSeconds()

        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist5" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 5 )
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist5" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val'], 5 )

        self.loader.stop()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()

        time.sleep(2)
        self.expectNevents(2)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist5" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], '5' )

    def testPersistFileWrite ( self ):
        """
        A testcase to determine the functionality of the persist file modifications with the countdown timer implementation.        
        """
        
        self._log.debug( "\ntestPersistFileWrite" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg3) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )
        
        self.sendSeconds()

        savePath = os.path.join("/usr/lib/python2.5/site-packages/WebBrickLibs-2.0-py2.5.egg/EventHandlers/tests/TestOut/persist.xml")
        content = ""
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        time.sleep(1)

        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist',
                {'val':57} ) )
                
        self.sendSeconds()

        time.sleep(2)

        i = 0
        for line in open(savePath, "r"):
            self._log.debug("line: " + line)
            i = i + 1

        self.assertEqual(i, 8)

        self.expectNevents(3)
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 57 )
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val'], 57 )

    def testNoPersistFileWrite ( self ):
        """
        A testcase to determine the functionality of the persist file modifications with the countdown timer implementation.        
        """
        
        self._log.debug( "\ntestPersistFileWrite" )
        copyfile( refFile1, outFile )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testPersistCfg3) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.sendSeconds()

        self.expectNevents(1)
        self.assertEqual( TestEventLogger._events[0].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[0].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[0].getPayload()['val'], '1' )
        
        self.sendSeconds()

        savePath = os.path.join("/usr/lib/python2.5/site-packages/WebBrickLibs-2.0-py2.5.egg/EventHandlers/tests/TestOut/persist.xml")
        content = ""
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        time.sleep(1)

        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist',
                {'val':1} ) )
                
        self.sendSeconds()

        time.sleep(2)

        content = ""
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        time.sleep(1)

        # expect a single event of the only persisted value
        self.router.publish( EventAgent("TestPersistFile"), Event( 'http://id.webbrick.co.uk/events/config/set',
                'test/persist',
                {'val':1} ) )

        time.sleep(2)

        i = 0
        for line in open(savePath, "r"):
            self._log.debug("line: " + line)
            i = i + 1



        self.assertEqual(i, 0)

        self.expectNevents(5)
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/config/set" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[1].getPayload()['val'], 1 )
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/config/get" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "test/persist" )
        self.assertEqual( TestEventLogger._events[2].getPayload()['val'], 1 )



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
            [ "testCreate_fromScratch"
             ,"testCreate_fromBak"
             ,"testCreate_fromDaily"
             ,"testCreateAndAdd"
             ,"testCreateAndAdd2"
             ,"testStartup"
             ,"testStartup2"
             ,"testStartup3"  # multi valued entity
             ,"testStartup4"  # extension given in configuration entry
             ,"testUpdateExist"
             ,"testUpdateExist2"
             ,"testUpdateExistMultiValue"
             ,"testDailyExists"
             ,"testWriteNew"
             ,"testPersistFileWrite"
             ,"testNoPersistFileWrite"
            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
             ,"testUpdateReload"
            ]
        }
    return TestUtils.getTestSuite(TestPersistFile, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestPersistFile.log", getTestSuite, sys.argv)
