# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestWebbrick.py 3026 2009-01-19 14:45:40Z andy.harris $
#
# Unit testing for WebBrick panel definition HTML conversions.
#

import sys
import time
import unittest
import logging

from MiscLib.DomHelpers import *

from WebBrickGateway.Webbrick import *

from EventLib.Event import Event
from EventHandlers.EventRouterLoad import EventRouterLoader

testConfigEventLogOnly = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.LogEvents' name='LogEvents' category='Logger'>
        <eventtype type="">
            <eventsource source="" >
                <!-- all events from a single source -->
                <event>
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

testConfigWebbrickStatusCache2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.WebbrickUdpEventReceiver' name='WebbrickUdpEventReceiver'>
    </eventInterface>

    <eventInterface module='EventHandlers.WebbrickStatusQuery' name='WebbrickStatusQuery'>
        <eventtype type="http://id.webbrick.co.uk/events/time/second">
            <eventsource source="time/second" >
                <!-- all events from a single source -->
                <event>
                    <params>
                        <!-- every 5 seconds -->
                        <testEq name='second'>
                            <value>0</value>
                            <value>5</value>
                            <value>10</value>
                            <value>15</value>
                            <value>20</value>
                            <value>25</value>
                            <value>30</value>
                            <value>35</value>
                            <value>40</value>
                            <value>45</value>
                            <value>50</value>
                            <value>55</value>
                        </testEq>
                    </params>
                    <scan/>
                    <recover/>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/time/minute">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="time/minute" >
                <event>
                    <discover address="255.255.255.255"/>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/NN">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AA">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/AT">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/SS">
            <!-- scan for new webbricks periodically. -->
            <eventsource source="" >
                <event>
                    <discoverFound />
                </event>
            </eventsource>
        </eventtype>
    </eventInterface>
</eventInterfaces>
"""

class TestWebbrick(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestWebbrick" )
        self.loader = None
        self.router = None
        self.nameCache = WebbrickNodeNameCache()
        self.cache = WebbrickStatusCache( self.nameCache )
        return

    def tearDown(self):
        self.cache.stop( self.router );
        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None
        return

    # Actual tests follow

    def testWebbrickNameCache(self):
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEventLogOnly) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.nameCache.start( self.router );
        self.router.publish( "TestWebbrick", Event( "http://id.webbrick.co.uk/events/webbrick/config/nodename", 
                "webbrick/100", 
                { "fromNode": 5, "nodename":"NameTest", "ipAdr": "1.2.3.4" } ) )
        self.assertEqual( self.nameCache.getNodeNumber("NameTest"), 5 )
        self.assertEqual( self.nameCache.getIpAddress("NameTest"), "1.2.3.4" )
        self.assertEqual( self.nameCache.getIpAddress(5), "1.2.3.4" )
        self.assertEqual( self.nameCache.getNodeNumFromIpAdr("1.2.3.4"), 5 )

    def testWebbrickStatusCache(self):
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigEventLogOnly) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.nameCache.start( self.router );
        self.cache.start( self.router );

        # send some test values.
        typeRoot = "http://id.webbrick.co.uk/events/webbrick/"
        srcRoot = "webbrick/100/"
        self.router.publish( "TestWebbrick", Event( typeRoot+"CT", 
                srcRoot + "CT/1", 
                { "fromNode": 100, "srcChannel": 1, "val": 21.5 } ) )
        self.router.publish( "TestWebbrick", Event( typeRoot+"DI", 
                srcRoot + "DI/1", 
                { "fromNode": 100, "srcChannel": 1, "state": 1 } ) )
        self.router.publish( "TestWebbrick", Event( typeRoot+"DO", 
                srcRoot + "DO/1", 
                { "fromNode": 100, "srcChannel": 1, "state": 1 } ) )
        self.router.publish( "TestWebbrick", Event( typeRoot+"AI", 
                srcRoot + "AI/1", 
                { "fromNode": 100, "srcChannel": 1, "val": 49.5 } ) )
        self.router.publish( "TestWebbrick", Event( typeRoot+"AO", 
                srcRoot + "AO/1", 
                { "fromNode": 100, "srcChannel": 1, "val": 49.5 } ) )
        #
        # now query cache.
        #
        res = self.cache.queryCache( "100","Tmp","1" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertEqual( res["stsval"], 21.5 )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( "100","DI","1" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertEqual( res["stsval"], "True" )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( "100","DO","1" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertEqual( res["stsval"], "True" )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( "100","AI","1" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertEqual( res["stsval"], 49.5 )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( "100","AO","1" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertEqual( res["stsval"], 49.5 )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( "100","AO","0" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertEqual( res["stsval"], None )
        self.assertNotEqual( res["stserr"], None )


    def testWebbrickStatusCache2(self):
        # create testDespatch
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigWebbrickStatusCache2) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.nameCache.start( self.router );
        self.cache.start( self.router );

        # Fiddle time, i.e. speed it up.
        self.router.publish( "TestWebbrick", Event( "http://id.webbrick.co.uk/events/time/minute", 
                "time/minute", { "minute": 0, "second": 1 } ) )
        time.sleep( 5 )
        # retrieve config
        self.router.publish( "TestWebbrick", Event( "http://id.webbrick.co.uk/events/time/second", 
                "time/second", { "minute": 0, "second": 5 } ) )
        time.sleep( 5 )
        # retrieve status
        self.router.publish( "TestWebbrick", Event( "http://id.webbrick.co.uk/events/time/second", 
                "time/second", { "minute": 0, "second": 10 } ) )
        time.sleep( 5 )

        #
        # now query cache.
        #
        nodeNr="UnNamed"
        res = self.cache.queryCache( nodeNr,"Tmp","0" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertNotEqual( res["stsval"], None )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( nodeNr,"DI","0" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertNotEqual( res["stsval"], None )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( nodeNr,"DO","0" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertNotEqual( res["stsval"], None )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( nodeNr,"AI","0" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertNotEqual( res["stsval"], None )
        self.assertEqual( res["stserr"], None )

        res = self.cache.queryCache( nodeNr,"AO","0" )
        self._log.debug( "queryCache %s", ( res ) )
        self.assertNotEqual( res["stsval"], None )
        self.assertEqual( res["stserr"], None )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestWebbrick("testWebbrickNameCache"))
    suite.addTest(TestWebbrick("testWebbrickStatusCache"))
    suite.addTest(TestWebbrick("testWebbrickStatusCache2"))
    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestWebbrick( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
