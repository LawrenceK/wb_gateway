# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestHeatmiser.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, logging, time
import unittest

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader
from EventHandlers.Heatmiser import *

import EventHandlers.tests.TestEventLogger as TestEventLogger
import Utils

import Events
from Utils import *

# sent to show current setting in schedule and we can update heatmiser
evtScheduleConfigure1230 = Event( 'http://id.webbrick.co.uk/events/config/get', 
            'schedule/room2/0', 
            { 'time': '12:30:00',
                'day' : '-MTWtF-'
                 } )

# sent to show current setting in schedule and we can update heatmiser
evtScheduleConfigure15Degrees = Event( 'http://id.webbrick.co.uk/events/config/get', 
            'schedule/room2/0/room2', 
            { 'val': 15.0 } )

# sent to activate something from our schedule.
evtCurrentConfigure16Degrees = Event( 'http://id.webbrick.co.uk/events/schedule/control', 
            'room2/set', 
            { 'val': 15.0 } )

evtScheduleConfigure0800 = Event( 'http://id.webbrick.co.uk/events/config/get', 
            'schedule/time', 
            { 'time': '08:00:00',
                'day' : '-MTWtF-'
             } )

# Configuration for the tests

serialPort      = 15    # com16
heatmiserAdr1    = 1
heatmiserAdr2    = 2
heatmiserdevKey = 'room2'

heatMiserCfg = { 'adr':2, 'schname': "room2", 'devkey': "room2", 'type': "PRT-N" }

testConfigHeatmiser = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EventHandlers.Heatmiser' name='HeatmiserHandler' serialPort='15'>

        <Xheatmiser adr="1" devkey="room1">
            <!-- no heating schedule in dtn-->
        </Xheatmiser>

        <heatmiser adr="2" schname="room2" devkey="room2">
            <!-- schname needed to link to gateway schedule -->
        </heatmiser>

        <eventtype type="">
            <eventsource source="time/second" >
                <!-- How often to read configuration from heatmisers -->
                <event>
                    <params>
                        <testEq name="second">
                            <value>0</value>
                            <value>15</value>
                            <value>30</value>
                            <value>45</value>
                        </testEq>
                    </params>
                    <action task="readSchedule"/>
                </event>
                <!-- How often to read status from heatmisers -->
                <event>
                    <params>
                        <testEq name="second">
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
                    <action task="readStatus"/>
                </event>
                <event>
                    <!-- once an hour in middle of hour -->
                    <params>
                        <testEq name="second">
                            <value>30</value>
                        </testEq>
                        <testEq name="minute">
                            <value>30</value>
                        </testEq>
                    </params>
                    <action task="verifyClock"/>
                </event>
            </eventsource>
        </eventtype>
        <eventtype type="http://id.webbrick.co.uk/events/config/get">
            <eventsource source="schedule/device" >
                <event>
                    <params>
                        <testEq name="devkey">
                            <value>room2</value>
                        </testEq>
                    </params>
                    <action task="verifyDevice"/>
                </event>
            </eventsource>
            <eventsource source="schedule/action" >
                <event>
                    <params>
                        <testEq name="devkey">
                            <value>room2</value>
                        </testEq>
                    </params>
                    <action task="verifyAction"/>
                </event>
            </eventsource>
            <eventsource source="schedule/time" >
                <event>
                    <params>
                        <testEq name="schkey">
                            <value>weekday1</value>
                            <value>weekday2</value>
                            <value>weekday3</value>
                            <value>weekday4</value>
                            <value>weekend1</value>
                            <value>weekend2</value>
                            <value>weekend3</value>
                            <value>weekend4</value>
                        </testEq>
                    </params>
                    <action task="verifySchTime" />
                </event>
            </eventsource>
        </eventtype>

        <eventtype type="http://id.webbrick.co.uk/events/schedule/control">
            <eventsource source="" >
                <event>
                    <params>
                        <testEq name="action">
                            <value>set</value>
                        </testEq>
                        <testEq name="devkey">
                            <value>room2</value>
                        </testEq>
                    </params>
                    <action task="doControl"/>
                </event>
            </eventsource>
        </eventtype>

    </eventInterface>
</eventInterfaces>
"""

_log = logging.getLogger( "TestHeatmiser" )

class TestHeatmiser(unittest.TestCase):

    def setUp(self):
        _log.debug( "\n\nsetUp" )
        TestEventLogger._events = []  # empty list

        self.router = None
        self.loader = None

    def tearDown(self):
        _log.debug( "\n\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        #time.sleep(1)

    def testReadParameters(self):
        driver = HeatmiserDriver( serialPort )
        driver.open()
        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        driver.close()

    def testGetStatus(self):
        driver = HeatmiserDriver( serialPort )
        driver.open()
        par = driver.getStatus( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        driver.close()

    def testScan(self):
        # locate heatmisers
        driver = HeatmiserDriver( serialPort )
        driver.open()
        for idx in range(32):
            par = driver.getStatus( idx )
            if par:
                _log.info( "Heatmiser %i %s", idx, par )

        driver.close()

    def testReadParameters2(self):
        driver = HeatmiserDriver( serialPort )
        driver.open()

        par = driver.readParameter( heatmiserAdr1 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        driver.close()

    def testWriteParameters(self):
        _log.debug( "\ntestWriteParameters" )
        driver = HeatmiserDriver( serialPort )
        driver.open()
        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        #par["partNr"] = 3
        par["hour"] = 20
        par["minute"] = 30
        par["dayOfWeek"] = 7
        par["tempCal"] = par["roomT"]

        driver.writeParameter( heatmiserAdr2, par )
        _log.debug( "%s", par )

        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        driver.close()

    def testWriteParameters2(self):
        _log.debug( "\ntestWriteParameters2" )
        driver = HeatmiserDriver( serialPort )
        driver.open()

        par = driver.readParameter( heatmiserAdr1 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        par["tempCal"] = par["roomT"]
        par["hour"] = 20
        par["minute"] = 30
        par["dayOfWeek"] = 7

        driver.writeParameter( heatmiserAdr1, par )
        _log.debug( "%s", par )


        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        _log.debug( "%s", par )

        par["tempCal"] = par["roomT"]
        par["hour"] = 20
        par["minute"] = 30
        par["dayOfWeek"] = 7

        driver.writeParameter( heatmiserAdr2, par )
        _log.debug( "%s", par )

        driver.close()

    def testResetAll(self):
        # Not so much a test but set heatmiser to known state
        _log.debug( "\ntestResetAll" )
        driver = HeatmiserDriver( serialPort )
        driver.open()
        params = driver.readParameter( heatmiserAdr2 )
        self.failIfEqual( params, None, "no comms" )
        _log.debug( "%s", params )

        params["dayOfWeek"] = 1
        params["hour"] = 23
        params["minute"] = 45
        params["tempCal"] = 18
        params["partNr"]  = 3
        params["differential"] = 1

        params["format"] = "C"
        params["frostMode"] = "disabled"
        params["sensor"] = "internal"
        params["floorLimit"] = "disabled"
        params["frostProt"] = "off"
        params["allKey"] = "unlocked"
        params["state"] = "off"
        params["setT"] = 20
        params["frostT"] = 7
        params["delay"] = 1
        params["preheat"] = 0
        params["floorMaxT"] = 30

        self.assert_( driver.writeParameter( heatmiserAdr2, params ) )

        daySchList = [
            HeatmiserSchEntry( hours=7, minutes=0, setPoint=18 ),
            HeatmiserSchEntry( hours=8, minutes=30, setPoint=14 ),
            HeatmiserSchEntry( hours=16, minutes=0, setPoint=21 ),
            HeatmiserSchEntry( hours=22, minutes=30, setPoint=14 ),
            ]

        wendSchList = [
            HeatmiserSchEntry( hours=7, minutes=0, setPoint=18 ),
            HeatmiserSchEntry( hours=8, minutes=30, setPoint=14 ),
            HeatmiserSchEntry( hours=16, minutes=0, setPoint=21 ),
            HeatmiserSchEntry( hours=22, minutes=30, setPoint=14 ),
            ]
        
        self.assert_( driver.setSchedule( heatmiserAdr2, CMD_SET_HEAT_WEEK_C_SET, MODEL_PRTN, daySchList ) )
        self.assert_( driver.setSchedule( heatmiserAdr2, CMD_SET_HEAT_WEND_C_SET, MODEL_PRTN, wendSchList ) )

        driver.close()

    def testSetClock(self):
        _log.debug( "\ntestSetClock" )

        driver = HeatmiserDriver( serialPort )

        interface = HeatmiserState( None, driver, heatMiserCfg ) # No event router
        driver.open()

        _log.debug( "%s" % interface.readStatus() )    # ensure model initialised

        self.assert_( interface.setClock( 1, 12, 34 ) )

        clk = interface.readClock()
        _log.debug( "%s", clk )

        driver.close()
        self.assertEqual( clk["dayOfWeek"], 1 )
        self.assertEqual( clk["hour"], 12 )
        self.assertEqual( clk["minute"], 34 )

    def testLoadConfig(self):
        _log.debug( "\ntestLoadConfig" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(1)

    def testFirstRead(self):
        _log.debug( "\ntestFirstRead" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(1)

        oldLen = len(TestEventLogger._events)
        # for each schedule entry 4 weekday, 4 weekend
        # send time and day event and set point event
        # 16 events
        # send two current values setpoint and current value
        
        expectedEvents = { 
                    "http://id.webbrick.co.uk/events/config/set" : 
                            [
                                ("schedule/room2/0" , 'time', '07:00:00', 'day', '-MTWtF-'),
                                ("schedule/room2/1" , 'time', '08:30:00', 'day', '-MTWtF-'),
                                ("schedule/room2/2" , 'time', '16:00:00', 'day', '-MTWtF-'),
                                ("schedule/room2/3" , 'time', '22:30:00', 'day', '-MTWtF-'),
                                ("schedule/room2/4" , 'time', '07:00:00', 'day', 'S-----s'),
                                ("schedule/room2/5" , 'time', '08:30:00', 'day', 'S-----s'),
                                ("schedule/room2/6" , 'time', '16:00:00', 'day', 'S-----s'),
                                ("schedule/room2/7" , 'time', '22:30:00', 'day', 'S-----s'),
                                ("schedule/room2/0/room2" , 'val', None),
                                ("schedule/room2/1/room2" , 'val', None),
                                ("schedule/room2/2/room2" , 'val', None),
                                ("schedule/room2/3/room2" , 'val', None),
                                ("schedule/room2/4/room2" , 'val', None),
                                ("schedule/room2/5/room2" , 'val', None),
                                ("schedule/room2/6/room2" , 'val', None),
                                ("schedule/room2/7/room2" , 'val', None),
                            ],
                    "http://id.webbrick.co.uk/events/heatmiser/current":
                            [
                                ("heatmiser/room2/setpoint" , 'val', None ),
                                ("heatmiser/room2/temperature" , 'val', None ),
                            ]
                }

        TestEventLogger.logEvents()
        _log.info( "Expected Events %s " % (expectedEvents) )
        haveErr, excessEvents = Utils.verifyEvents( expectedEvents, TestEventLogger._events )

        _log.info( "Excess Events %s " % (excessEvents) )

        self.assertEqual( haveErr, False, "Incorrect event set" )

    def testSecondRead(self):
        _log.debug( "\ntestSecondRead" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(1)   # allow start
        oldLen = len(TestEventLogger._events)
        self.assertEqual( oldLen, 18 )

        self.router.publish( EventAgent("TestHeatmiser"), Events.evtSecond15 )  # re-read
        time.sleep(1)

        TestEventLogger.logEvents()

        # additional time event
        self.assertEqual( oldLen+1, len(TestEventLogger._events) )

    def testSendConfigure(self):
        _log.debug( "\ntestSendConfigure" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        oldLen = len(TestEventLogger._events)
        self.assertEqual( oldLen, 18 )

        # send command event

        self.router.publish( EventAgent("TestHeatmiser"), Events.evtSecond15 )  # re-read
        time.sleep(1)

        TestEventLogger.logEvents()

        # additional time event
        self.assertEqual( oldLen+1, len(TestEventLogger._events) )

    def testVerifyClock(self):
        _log.debug( "\ntestVerifyClock" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        time.sleep(1)

        self.router.publish( EventAgent("TestHeatmiser"), Events.evtTimexx3030 )   # trigger heatmiser verify of clock.
        time.sleep(3)

        self.loader.stop()  # all tasks
        self.loader = None
        self.router = None

        # re opne to read clock.
        driver = HeatmiserDriver( serialPort )

        interface = HeatmiserState( None, driver, heatMiserCfg ) # No event router
        driver.open()

        _log.debug( "%s" % interface.readStatus() )    # ensure model initialised

        clk = interface.readClock()
        _log.debug( "%s" % clk )

        driver.close()

        nowTime = time.gmtime()
        # nowTime[3] = hour
        # nowTime[4] = minute
        # nowTime[6] = day of week

        self.assertEqual( clk["dayOfWeek"], nowTime[6]+1 )
        self.assertEqual( clk["hour"], nowTime[3] )
        self.assertEqual( clk["minute"], nowTime[4] )

    def testChangeCurSetPoint(self):
        _log.debug( "\ntestChangeCurSetPoint" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(1)
        oldLen = len(TestEventLogger._events)
        self.assertEqual( oldLen, 18 )

        # send command event
        self.router.publish( EventAgent("TestHeatmiser"), evtCurrentConfigure16Degrees )

        self.router.publish( EventAgent("TestHeatmiser"), Events.evtSecond15 )  # re-read

        time.sleep(1)

        TestEventLogger.logEvents()

        # additional time event
        self.assertEqual( oldLen+3, len(TestEventLogger._events) )

    def testChangeSchTime(self):
        _log.debug( "\ntestChangeSchTime" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(1)
        oldLen = len(TestEventLogger._events)
        self.assertEqual( oldLen, 18 )

        # send command event
        self.router.publish( EventAgent("TestHeatmiser"), evtScheduleConfigure1230 )
        time.sleep(1)

        self.router.publish( EventAgent("TestHeatmiser"), Events.evtSecond15 )  # re-read
        time.sleep(1)

        TestEventLogger.logEvents()

        # additional events, control. time, 2  update events.
        self.assertEqual( oldLen+4, len(TestEventLogger._events) )

    def testChangeSchAction(self):
        _log.debug( "\ntestChangeSchAction" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeatmiser) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        time.sleep(1)
        oldLen = len(TestEventLogger._events)
        self.assertEqual( oldLen, 18 )

        # send command event
        self.router.publish( EventAgent("TestHeatmiser"), evtScheduleConfigure15Degrees )
        time.sleep(1)

        self.router.publish( EventAgent("TestHeatmiser"), Events.evtSecond15 )  # re-read
        time.sleep(1)

        TestEventLogger.logEvents()

        # additional events, control. time, 1  update events.
        self.assertEqual( oldLen+3, len(TestEventLogger._events) )

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
            [ "testDummy"
            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testResetAll"
             ,"testGetStatus"
             ,"testReadParameters"
             ,"testWriteParameters"
             ,"testSetClock"
             ,"testLoadConfig"
             ,"testFirstRead"
             ,"testSecondRead"
             ,"testVerifyClock"
             ,"testChangeCurSetPoint"
             ,"testChangeSchTime"
             ,"testChangeSchAction"
            ],
        "pending":
            [ "testScan"
            ]
        }
    return TestUtils.getTestSuite(TestHeatmiser, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestHeatmiser.log", getTestSuite, sys.argv)
