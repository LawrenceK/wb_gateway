# $Id$
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

from EventHandlers.GenerateManifest import GenerateManifest

import Events
from DummyRouter import *
from Utils import *

cfgStringNoFiles = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.GenerateManifest' name='GenerateManifest' >
        <skin directory="/usr/lib/python2.5/site-packages/WebBrickLibs-2.0-py2.5.egg/EventHandlers/tests/resources/manifest/nofiles" />
    </eventInterface>
    
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

cfgStringOneSkin = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.GenerateManifest' name='GenerateManifest' >
        <skin directory="/usr/lib/python2.5/site-packages/WebBrickLibs-2.0-py2.5.egg/EventHandlers/tests/resources/manifest/oneskin" />
    </eventInterface>
    
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

cfgStringOneSkinDifferent = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.GenerateManifest' name='GenerateManifest' >
        <skin directory="/usr/lib/python2.5/site-packages/WebBrickLibs-2.0-py2.5.egg/EventHandlers/tests/resources/manifest/oneskindifferent" />
    </eventInterface>
    
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

cfgStringTwoSkins = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.GenerateManifest' name='GenerateManifest' >
        <skin directory="/usr/lib/python2.5/site-packages/WebBrickLibs-2.0-py2.5.egg/EventHandlers/tests/resources/manifest/twoskins" />
    </eventInterface>
    
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

cfgStringTwoSkinsDifferent = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.GenerateManifest' name='GenerateManifest' >
        <skin directory="/usr/lib/python2.5/site-packages/WebBrickLibs-2.0-py2.5.egg/EventHandlers/tests/resources/manifest/twoskinsdifferent" />
    </eventInterface>
    
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <eventtype type="">
            <eventsource source="" >
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

class TestGenerateManifest(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestGenerateManifest" )
        self._log.debug( "\nsetUp" )
        self._router = DummyRouter()

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )
            
    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1

        if ( len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()

        self.assertEqual( len(TestEventLogger._events), cnt)

    # Actual tests follow

    def testNoFiles(self):
        
        self._log.debug( "\ntestNoFiles" )
        
        manifest = os.path.join(getDictFromXmlString(cfgStringNoFiles)['eventInterfaces'][0]['skin']['directory'], "round", "static", "manifest", "round.manifest")
        content = ""
        fileHandle = open(manifest, 'w')
        fileHandle.write(content)
        fileHandle.close()
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(cfgStringNoFiles) )
        self.loader.start()  
        self.router = self.loader.getEventRouter()
        time.sleep(0.5)
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        
        manifest = os.path.join(getDictFromXmlString(cfgStringNoFiles)['eventInterfaces'][0]['skin']['directory'], "round", "static", "manifest", "round.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 0)
        
        self.assertEqual( len(TestEventLogger._events), 1 )
        # Tom: Commented out, this test's functionality should not produce a manifest file
        #self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        #self.assertEqual( TestEventLogger._events[1].getSource(), "manifest/publish/activeskin")
        #self.assertEqual( TestEventLogger._events[1].getPayload(), {"val":""} )        
        
    def testOneSkin(self):
        
        self._log.debug( "\ntestOneSkin" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(cfgStringOneSkin) )
        self.loader.start()  
        self.router = self.loader.getEventRouter()
        time.sleep(1)
        
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkin)['eventInterfaces'][0]['skin']['directory'], "second", "static", "css", "test.css")
        content = ""
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        time.sleep(1)
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        time.sleep(1)
        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkin)['eventInterfaces'][0]['skin']['directory'], "second", "static", "manifest", "second.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 2 )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "manifest/publish/secondskin")
        self.assertEqual( TestEventLogger._events[1].getPayload(), {"val":"55ba7f7885ab81a55dd6ddda087b280b"} )        
        
    def testOneSkinDifferent(self):
        
        self._log.debug( "\ntestOneSkinDifferent" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(cfgStringOneSkinDifferent) )
        self.loader.start()  
        self.router = self.loader.getEventRouter()
        
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = ""
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        
        time.sleep(0.5)       
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        
        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 2 )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "manifest/publish/thirdskin")
        self.assertEqual( TestEventLogger._events[1].getPayload(), {"val":"55ba7f7885ab81a55dd6ddda087b280b"} )        

        # Modify content       
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = "this is new content"
        fileHandle1 = open(savePath, 'w')
        fileHandle1.write(content)
        fileHandle1.close()
       
        time.sleep(5)
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        time.sleep(0.5)

        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1

        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 4 )
        self.assertEqual( TestEventLogger._events[3].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "manifest/publish/thirdskin")
        self.assertNotEqual( TestEventLogger._events[3].getPayload(), {"val":"55ba7f7885ab81a55dd6ddda087b280b"} )        


        # Modify content again      
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = "this is new more!"
        fileHandle2 = open(savePath, 'w')
        fileHandle2.write(content)
        fileHandle2.close()        
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        time.sleep(0.5)

        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1

       
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 6 )
        self.assertEqual( TestEventLogger._events[5].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "manifest/publish/thirdskin")
        self.assertNotEqual( TestEventLogger._events[5].getPayload(), TestEventLogger._events[3].getPayload() )   
        
        # Modify content again      
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = "this is new more1!"
        fileHandle3 = open(savePath, 'w')
        fileHandle3.write(content)
        fileHandle3.close() 
        time.sleep(0.5)       
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifestNew"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        time.sleep(5)       
        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1

       
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 8 )
        self.assertEqual( TestEventLogger._events[7].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[7].getSource(), "manifest/publish/thirdskin")
        self.assertNotEqual( TestEventLogger._events[7].getPayload(), TestEventLogger._events[5].getPayload() )               
       
    def testWriteSame(self):
        
        self._log.debug( "\ntestWriteSame" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(cfgStringOneSkinDifferent) )
        self.loader.start()  
        self.router = self.loader.getEventRouter()
        
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = ""
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        
        time.sleep(0.5)
        
        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 2 )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "manifest/publish/thirdskin")
        self.assertEqual( TestEventLogger._events[1].getPayload(), {"val":"55ba7f7885ab81a55dd6ddda087b280b"} )        

        # Modify content
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = "this is new more!"
        fileHandle2 = open(savePath, 'w')
        fileHandle2.write(content)
        fileHandle2.close()        
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        time.sleep(0.5)

        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1

       
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 4 )
        self.assertEqual( TestEventLogger._events[3].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[3].getSource(), "manifest/publish/thirdskin")
        self.assertNotEqual( TestEventLogger._events[3].getPayload(), TestEventLogger._events[1].getPayload() )   
        
        # Modify content again      
        savePath = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = "this is new more!"
        fileHandle3 = open(savePath, 'w')
        fileHandle3.write(content)
        fileHandle3.close()        
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        time.sleep(0.5)
        
        manifest = os.path.join(getDictFromXmlString(cfgStringOneSkinDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1

       
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 6 )
        self.assertEqual( TestEventLogger._events[5].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "manifest/publish/thirdskin")
        self.assertEqual( TestEventLogger._events[5].getPayload(), TestEventLogger._events[3].getPayload() )               
              
    def testTwoSkins(self):
        
        self._log.debug( "\ntestTwoSkins" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(cfgStringTwoSkins) )
        self.loader.start()  
        self.router = self.loader.getEventRouter()
        
        savePath = os.path.join(getDictFromXmlString(cfgStringTwoSkins)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = "same"
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        
        savePath = os.path.join(getDictFromXmlString(cfgStringTwoSkins)['eventInterfaces'][0]['skin']['directory'], "four", "static", "css", "test.css")
        content = "same"
        fileHandle = open(savePath, 'w')
        fileHandle.write(content)
        fileHandle.close()
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        
        time.sleep(0.5)
        
        manifest = os.path.join(getDictFromXmlString(cfgStringTwoSkins)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 8)
                
        manifest = os.path.join(getDictFromXmlString(cfgStringTwoSkins)['eventInterfaces'][0]['skin']['directory'], "four", "static", "manifest", "four.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 8)
    
        # check content
        self.assertEqual( len(TestEventLogger._events), 3 )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "manifest/publish/fourskin")
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "manifest/publish/thirdskin")
        self.assertEqual( TestEventLogger._events[1].getPayload(), TestEventLogger._events[2].getPayload() )   
        
        # modify content        
        savePath = os.path.join(getDictFromXmlString(cfgStringTwoSkins)['eventInterfaces'][0]['skin']['directory'], "third", "static", "css", "test.css")
        content = "this is new"
        fileHandle2 = open(savePath, 'w')
        fileHandle2.write(content)
        fileHandle2.close()        
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        time.sleep(0.5)

        manifest = os.path.join(getDictFromXmlString(cfgStringTwoSkins)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1

       
        self.assertEqual(i, 8)
        
        self.assertEqual( len(TestEventLogger._events), 6 )
        self.assertEqual( TestEventLogger._events[4].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[4].getSource(), "manifest/publish/fourskin")
        self.assertEqual( TestEventLogger._events[5].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[5].getSource(), "manifest/publish/thirdskin")
        self.assertEqual( TestEventLogger._events[4].getPayload(), TestEventLogger._events[2].getPayload() )   
        self.assertNotEqual( TestEventLogger._events[4].getPayload(), TestEventLogger._events[5].getPayload() )   

    def testTwoSkinsDifferent(self):
        
        self._log.debug( "\ntestTwoSkinsDifferent" )
        
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(cfgStringTwoSkinsDifferent) )
        self.loader.start()  
        self.router = self.loader.getEventRouter()
        
        evPayload = {"elapsed": "5"}
        self.router.publish( EventAgent("TestGenerateManifest"), Event ( "http://id.webbrick.co.uk/events/time/runtime", "http://id.webbrick.co.uk/events/time/runtime", evPayload ) )    # 0 Off
        
        time.sleep(2)
        
        manifest = os.path.join(getDictFromXmlString(cfgStringTwoSkinsDifferent)['eventInterfaces'][0]['skin']['directory'], "third", "static", "manifest", "third.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 9)
                
        manifest = os.path.join(getDictFromXmlString(cfgStringTwoSkinsDifferent)['eventInterfaces'][0]['skin']['directory'], "four", "static", "manifest", "four.manifest")
        i = 0
        for line in open(manifest, "r"):
            self._log.debug("line: " + line)
            i = i + 1
        
        self.assertEqual(i, 8)
    
        # check content
        self.assertEqual( len(TestEventLogger._events), 3 )
        self.assertEqual( TestEventLogger._events[1].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[1].getSource(), "manifest/publish/fourskin")
        self.assertEqual( TestEventLogger._events[2].getType(), "http://id.webbrick.co.uk/events/manifest/publish" )
        self.assertEqual( TestEventLogger._events[2].getSource(), "manifest/publish/thirdskin")
        self.assertNotEqual( TestEventLogger._events[1].getPayload(), TestEventLogger._events[2].getPayload() )   
        
        
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
            [ "testNoFiles",
              "testOneSkin",
              "testOneSkinDifferent",
              "testWriteSame",
              "testTwoSkins",
              "testTwoSkinsDifferent"
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
    return TestUtils.getTestSuite(TestGenerateManifest, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestGenerateManifest.log", getTestSuite, sys.argv)
