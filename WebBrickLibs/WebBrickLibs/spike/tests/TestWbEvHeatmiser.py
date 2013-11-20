# $Id: TestWbEvHeatmiser.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import threading
import logging
from logging.handlers import MemoryHandler
import sys
import string
import time
from datetime import datetime
import unittest
from SocketServer import StreamRequestHandler, TCPServer
import socket
import os

sys.path.append("../..")

from WebBrickLibs.WbEvent        import *
from WebBrickLibs.WbAccess       import DoHTTPRequest
from WebBrickLibs.DespatchTask   import *
from WebBrickLibs.WbEvBaseAction import WbEvBaseAction
from WebBrickLibs.WbEvHeatmiser  import *

from MiscLib.DomHelpers  import *
from MiscLib.ScanFiles   import readFile
from MiscLib.SuperGlobal import SuperGlobal

from TestUtils import *

# sent to show current setting in schedule and we can update heatmiser
evtScheduleConfigure1230 = WbEventOther( 'http://id.webbrick.co.uk/events/schedule/time', 
            'schedule/time', 
            { 'time': ((12*3600) + (30*60) ),
                'days' : '1,2,3,4,5',
            'schKey': 'weekday4',
            'devKey': 'room2',
                 } )

# sent to show current setting in schedule and we can update heatmiser
evtScheduleConfigure15Degrees = WbEventOther( 'http://id.webbrick.co.uk/events/schedule/actions', 
            'schedule/action', 
            { 'val': 15.0,
            'schKey': 'weekday4',
            'devKey': 'room2',
                 } )

# sent to activate something from our schedule.
evtCurrentConfigure16Degrees = WbEventOther( 'http://id.webbrick.co.uk/events/schedule/control', 
            'room2/SetPoint', 
            { 'val': 15.0,
            'action': 'setPoint',
            'devKey': 'room2',
                 } )

evtScheduleConfigure0800 = WbEventOther( 'http://id.webbrick.co.uk/events/schedule/time', 
            'schedule/time', 
            { 'val': ((8*3600) + (0 * 60) ),
            'schKey': 'weekday4',
            'devKey': 'room2',
             } )

# Configuration for the tests

serialPort      = 15    # com16
heatmiserAdr1    = 1
heatmiserAdr2    = 2
heatmiserdevKey = 'room2'

heatMiserCfg = { 'adr':2, 'devKey': "room2", 'type': "PRT-N",
            'sch' : [ 
                    {'type':"weekday", 'idx': 0, 'schKey': 'weekday1' },
                    {'type':"weekday", 'idx': 1, 'schKey': 'weekday2' },
                    {'type':"weekday", 'idx': 2, 'schKey': 'weekday3' },
                    {'type':"weekday", 'idx': 3, 'schKey': 'weekday4' },
                    {'type':"weekend", 'idx': 0, 'schKey': 'weekend1' },
                    {'type':"weekend", 'idx': 1, 'schKey': 'weekend2' },
                    {'type':"weekend", 'idx': 2, 'schKey': 'weekend3' },
                    {'type':"weekend", 'idx': 3, 'schKey': 'weekend4' },
                    ]
                }

testConfigWbEvHeatmiser = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='TestUtils' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
	        <event>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='WbEvHeatmiser' name='WbEvHeatmiser' serialPort='15'>

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
            <eventsource source="schedule/device" >
                <event>
                    <params>
                        <testEq name="devKey">
                            <value>room2</value>
                        </testEq>
                    </params>
                    <action task="verifyDevice"/>
                </event>
            </eventsource>
            <eventsource source="schedule/action" >
                <event>
                    <params>
                        <testEq name="devKey">
                            <value>room2</value>
                        </testEq>
                    </params>
                    <action task="verifyAction"/>
                </event>
            </eventsource>
            <eventsource source="schedule/time" >
                <event>
                    <params>
                        <testEq name="schKey">
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
                            <value>setPoint</value>
                        </testEq>
                        <testEq name="devKey">
                            <value>room2</value>
                        </testEq>
                    </params>
                    <action task="doControl"/>
                </event>
            </eventsource>
        </eventtype>

        <Xheatmiser adr="1" devKey="room1">
            <!-- no heating schedule in dtn-->
        </Xheatmiser>

        <heatmiser adr="2" devKey="room2">
            <sch type="weekday" idx='0' schKey='weekday1'/>
            <sch type="weekday" idx='1' schKey='weekday2'/>
            <sch type="weekday" idx='2' schKey='weekday3'/>
            <sch type="weekday" idx='3' schKey='weekday4'/>
            <sch type="weekend" idx='0' schKey='weekend1'/>
            <sch type="weekend" idx='1' schKey='weekend2'/>
            <sch type="weekend" idx='2' schKey='weekend3'/>
            <sch type="weekend" idx='3' schKey='weekend4'/>
        </heatmiser>

    </eventInterface>
</eventInterfaces>
"""

superglobal1 = SuperGlobal()

class TestWbEvHeatmiser(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestWbEvHeatmiser" )
        self._log.debug( "\n\nsetUp" )
        superglobal1.testEventLogData = []  # empty list

        self.runner = None

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

        if self.runner:
            self.runner.stop()  # all tasks
            self.runner = None

        #time.sleep(1)

    def testReadParameters(self):
        driver = HeatmiserDriver( serialPort )
        driver.open()
        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        driver.close()

    def testGetStatus(self):
        driver = HeatmiserDriver( serialPort )
        driver.open()
        par = driver.getStatus( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        driver.close()

    def testReadParameters2(self):
        driver = HeatmiserDriver( serialPort )
        driver.open()

        par = driver.readParameter( heatmiserAdr1 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        driver.close()

    def testWriteParameters(self):
        self._log.debug( "\ntestWriteParameters" )
        driver = HeatmiserDriver( serialPort )
        driver.open()
        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        #par["partNr"] = 3
        par["hour"] = 20
        par["minute"] = 30
        par["dayOfWeek"] = 7
        par["tempCal"] = par["roomT"]

        driver.writeParameter( heatmiserAdr2, par )
        self._log.debug( "%s", par )

        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        driver.close()

    def testWriteParameters2(self):
        self._log.debug( "\ntestWriteParameters2" )
        driver = HeatmiserDriver( serialPort )
        driver.open()

        par = driver.readParameter( heatmiserAdr1 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        par["tempCal"] = par["roomT"]
        par["hour"] = 20
        par["minute"] = 30
        par["dayOfWeek"] = 7

        driver.writeParameter( heatmiserAdr1, par )
        self._log.debug( "%s", par )


        par = driver.readParameter( heatmiserAdr2 )
        self.assertNotEqual( par, None )
        self._log.debug( "%s", par )

        par["tempCal"] = par["roomT"]
        par["hour"] = 20
        par["minute"] = 30
        par["dayOfWeek"] = 7

        driver.writeParameter( heatmiserAdr2, par )
        self._log.debug( "%s", par )

        driver.close()

    def testResetAll(self):
        # Not so much a test but set heatmiser to known state
        self._log.debug( "\ntestResetAll" )
        driver = HeatmiserDriver( serialPort )
        driver.open()
        params = driver.readParameter( heatmiserAdr2 )
        self.failIfEqual( params, None, "no comms" )
        self._log.debug( "%s", params )

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
            HeatmiserSchEntry( {'idx':0, 'schKey':'k1', 'type': 'weekday', 'hours': 7, 'minutes': 0, 'setPoint': 18 } ),
            HeatmiserSchEntry( {'idx':1, 'schKey':'k2', 'type': 'weekday', 'hours': 8, 'minutes': 30, 'setPoint': 14 } ),
            HeatmiserSchEntry( {'idx':2, 'schKey':'k3', 'type': 'weekday', 'hours': 16, 'minutes': 0, 'setPoint': 21 } ),
            HeatmiserSchEntry( {'idx':3, 'schKey':'k4', 'type': 'weekday', 'hours': 22, 'minutes': 30, 'setPoint': 14 } ),
            ]

        wendSchList = [
            HeatmiserSchEntry( {'idx':0, 'schKey':'k1', 'type': 'weekday', 'hours': 7, 'minutes': 0, 'setPoint': 18 } ),
            HeatmiserSchEntry( {'idx':1, 'schKey':'k2', 'type': 'weekday', 'hours': 8, 'minutes': 30, 'setPoint': 14 } ),
            HeatmiserSchEntry( {'idx':2, 'schKey':'k3', 'type': 'weekday', 'hours': 16, 'minutes': 0, 'setPoint': 21 } ),
            HeatmiserSchEntry( {'idx':3, 'schKey':'k4', 'type': 'weekday', 'hours': 22, 'minutes': 30, 'setPoint': 14 } ),
            ]
        
        self.assert_( driver.setSchedule( heatmiserAdr2, CMD_SET_HEAT_WEEK_C_SET, MODEL_PRTN, daySchList ) )
        self.assert_( driver.setSchedule( heatmiserAdr2, CMD_SET_HEAT_WEND_C_SET, MODEL_PRTN, wendSchList ) )

        driver.close()

    def testSetClock(self):
        self._log.debug( "\ntestSetClock" )

        driver = HeatmiserDriver( serialPort )

        interface = Heatmiser( None, driver, heatMiserCfg ) # No event router
        driver.open()

        self._log.debug( "%s" % interface.readStatus() )    # ensure model initialised

        self.assert_( interface.setClock( 1, 12, 34 ) )

        clk = interface.readClock()
        self._log.debug( "%s", clk )

        driver.close()
        self.assertEqual( clk["dayOfWeek"], 1 )
        self.assertEqual( clk["hour"], 12 )
        self.assertEqual( clk["minute"], 34 )

    def testLoadConfig(self):
        self._log.debug( "\ntestLoadConfig" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks

        time.sleep(1)

    def testFirstRead(self):
        self._log.debug( "\ntestFirstRead" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks

        time.sleep(1)

        oldLen = len(superglobal1.testEventLogData)

        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        self.assertEqual( oldLen, 26 )


    def testSecondRead(self):
        self._log.debug( "\ntestSecondRead" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks

        time.sleep(1)   # allow start
        oldLen = len(superglobal1.testEventLogData)
        self.assertEqual( oldLen, 26 )

        self.runner.sendEvent( evtSecond15 )  # re-read
        time.sleep(1)

        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        # additional time event
        self.assertEqual( oldLen+1, len(superglobal1.testEventLogData) )

    def testSendConfigure(self):
        self._log.debug( "\ntestSendConfigure" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks

        oldLen = len(superglobal1.testEventLogData)
        self.assertEqual( oldLen, 26 )

        # send command event

        self.runner.sendEvent( evtSecond15 )  # re-read
        time.sleep(1)

        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        # additional time event
        self.assertEqual( oldLen+1, len(superglobal1.testEventLogData) )

    def testVerifyClock(self):
        self._log.debug( "\ntestVerifyClock" )

        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks
        time.sleep(1)

        self.runner.sendEvent( evtTimexx3030 )   # trigger heatmiser verify of clock.
        time.sleep(3)

        self.runner.stop()  # all tasks
        self.runner = None

        # re opne to read clock.
        driver = HeatmiserDriver( serialPort )

        interface = Heatmiser( None, driver, heatMiserCfg ) # No event router
        driver.open()

        self._log.debug( "%s" % interface.readStatus() )    # ensure model initialised

        clk = interface.readClock()
        self._log.debug( "%s" % clk )

        driver.close()

        nowTime = time.gmtime()
        # nowTime[3] = hour
        # nowTime[4] = minute
        # nowTime[6] = day of week

        self.assertEqual( clk["dayOfWeek"], nowTime[6]+1 )
        self.assertEqual( clk["hour"], nowTime[3] )
        self.assertEqual( clk["minute"], nowTime[4] )

    def testChangeCurSetPoint(self):
        self._log.debug( "\ntestChangeCurSetPoint" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks

        time.sleep(1)
        oldLen = len(superglobal1.testEventLogData)
        self.assertEqual( oldLen, 26 )

        # send command event
        self.runner.sendEvent( evtCurrentConfigure16Degrees )

        self.runner.sendEvent( evtSecond15 )  # re-read

        time.sleep(1)

        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        # additional time event
        self.assertEqual( oldLen+3, len(superglobal1.testEventLogData) )

    def testChangeSchTime(self):
        self._log.debug( "\ntestChangeSchTime" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks

        time.sleep(1)
        oldLen = len(superglobal1.testEventLogData)
        self.assertEqual( oldLen, 26 )

        # send command event
        self.runner.sendEvent( evtScheduleConfigure1230 )
        time.sleep(1)

        self.runner.sendEvent( evtSecond15 )  # re-read
        time.sleep(1)

        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        # additional events, control. time, 2  update events.
        self.assertEqual( oldLen+4, len(superglobal1.testEventLogData) )

    def testChangeSchAction(self):
        self._log.debug( "\ntestChangeSchAction" )
        self.runner = loadDespatchTaskFromString( testConfigWbEvHeatmiser )
        self.runner.start()  # all tasks

        time.sleep(1)
        oldLen = len(superglobal1.testEventLogData)
        self.assertEqual( oldLen, 26 )

        # send command event
        self.runner.sendEvent( evtScheduleConfigure15Degrees )
        time.sleep(1)

        self.runner.sendEvent( evtSecond15 )  # re-read
        time.sleep(1)

        for ev in superglobal1.testEventLogData:
            self._log.debug( "%s", ev )

        # additional events, control. time, 1  update events.
        self.assertEqual( oldLen+3, len(superglobal1.testEventLogData) )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    # use just low level driver
    suite.addTest(TestWbEvHeatmiser("testResetAll"))    # a form of factory reset
    suite.addTest(TestWbEvHeatmiser("testGetStatus"))
    suite.addTest(TestWbEvHeatmiser("testReadParameters"))
    suite.addTest(TestWbEvHeatmiser("testWriteParameters"))
#    suite.addTest(TestWbEvHeatmiser("testReadParameters2"))
#    suite.addTest(TestWbEvHeatmiser("testWriteParameters2"))

    # use HeatMiser
    suite.addTest(TestWbEvHeatmiser("testSetClock"))

    # use event interface
    suite.addTest(TestWbEvHeatmiser("testLoadConfig"))
    suite.addTest(TestWbEvHeatmiser("testFirstRead"))
    suite.addTest(TestWbEvHeatmiser("testSecondRead"))
    suite.addTest(TestWbEvHeatmiser("testVerifyClock"))
    suite.addTest(TestWbEvHeatmiser("testChangeCurSetPoint"))
    suite.addTest(TestWbEvHeatmiser("testChangeSchTime"))
    suite.addTest(TestWbEvHeatmiser("testChangeSchAction"))

    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestWbEvHeatmiser( sys.argv[1] )
    else:
#        logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
