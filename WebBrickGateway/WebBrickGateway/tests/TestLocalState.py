# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestLocalState.py 2609 2008-08-11 20:03:27Z graham.klyne $
#
# Unit testing for WebBrick panel definition HTML conversions.
#

import sys
import time
import unittest
import logging

from MiscLib.DomHelpers import *

from EventLib.Event import Event
from EventHandlers.EventRouterLoad import EventRouterLoader

from WebBrickGateway.LocalState import *

testConfigLocalState = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.Compound' name='Compound'>

        <eventtype type="http://id.webbrick.co.uk/events/webbrick/DI">
            <!-- events from a source of a specific type -->
            <!-- This is slightly ott tyo show possibilities -->
            <eventsource source="webbrick/GarageA/DI/8" >
	        <event>
                    <params>
                        <testEq name='state' value='0' />
                    </params>
		    <action name="Door1IsClosed" value="0"/>
	        </event>
	        <event>
                    <params>
                        <testEq name='state' value='1' />
                    </params>
		    <action name="Door1IsClosed" value="1"/>
	        </event>
            </eventsource>
            <eventsource source="webbrick/GarageA/DI/9" >
	        <event>
		    <action name="Door1IsOpen" key="state"/>
	        </event>
            </eventsource>
        </eventtype>

        <compound>
            <params>
                <testEq name='Door1IsClosed' value='0' />
                <testEq name='Door1IsOpen' value='0' />
            </params>
            <newEvent type="http://id.webbrick.co.uk/events/state" source="Garage/Door/1">
                <other_data val='0'/>
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='Door1IsClosed' value='0' />
                <testEq name='Door1IsOpen' value='1' />
            </params>
            <newEvent type="http://id.webbrick.co.uk/events/state" source="Garage/Door/1">
                <other_data val='1'/>
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='Door1IsClosed' value='1' />
                <testEq name='Door1IsOpen' value='0' />
            </params>
            <newEvent type="http://id.webbrick.co.uk/events/state" source="Garage/Door/1">
                <other_data val='2'/>
            </newEvent>
        </compound>
        <compound>
            <params>
                <testEq name='Door1IsClosed' value='1' />
                <testEq name='Door1IsOpen' value='1' />
            </params>
            <newEvent type="http://id.webbrick.co.uk/events/state" source="Garage/Door/1">
                <other_data val='3'/>
            </newEvent>
        </compound>
        
    </eventInterface>   
</eventInterfaces>
"""

class TestLocalState(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestLocalState" )
        self.loader = None
        self.router = None
        self.cache = LocalState( )
        return

    def tearDown(self):
        self.cache.stop(self.router)
        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None
        return

    # Actual tests follow

    def testLocalState(self):
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigLocalState) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.cache.start( self.router );

        # Fiddle time, i.e. speed it up.
        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/8", { "state": 0 } ) )
        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/9", { "state": 0 } ) )

        res = self.cache.queryCache( "Garage/Door/1" )
        self.assertEqual( res["stsval"], "0" )
        self.assertEqual( res["stserr"], None )

        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/8", { "state": 0 } ) )
        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/9", { "state": 1 } ) )
        res = self.cache.queryCache( "Garage/Door/1" )
        self.assertEqual( res["stsval"], "1" )
        self.assertEqual( res["stserr"], None )
                
        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/8", { "state": 1 } ) )
        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/9", { "state": 0 } ) )
        res = self.cache.queryCache( "Garage/Door/1" )
        self.assertEqual( res["stsval"], "2" )
        self.assertEqual( res["stserr"], None )
                
        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/8", { "state": 1 } ) )
        self.router.publish( "TestLocalState", Event( "http://id.webbrick.co.uk/events/webbrick/DI", 
                "webbrick/GarageA/DI/9", { "state": 1 } ) )
        res = self.cache.queryCache( "Garage/Door/1" )
        self.assertEqual( res["stsval"], "3" )
        self.assertEqual( res["stserr"], None )
                
        res = self.cache.queryCache( "Garage/Door/2" )
        self.assertEqual( res["stsval"], None )
        self.assertNotEqual( res["stserr"], None )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestLocalState("testLocalState"))
    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestLocalState( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
