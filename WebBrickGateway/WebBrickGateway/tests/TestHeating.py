# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestHeating.py 2609 2008-08-11 20:03:27Z graham.klyne $
#
#

import sys
import time
import unittest

from MiscLib.DomHelpers import *

from WebBrickGateway.Webbrick import *

from EventLib.Event import Event
from EventHandlers.EventRouterLoad import EventRouterLoader

from WebBrickGateway.HeatingHandler import *

#from EventHandlers.tests.TestEventLogger 
import EventHandlers.tests.TestEventLogger 

testConfigHeating ="""<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='WebBrickGateway.HeatingHandler' name='HeatingHandler'>
        <heatingDevice devKey='BoilerHW'>Boiler</heatingDevice>
        <heatingDevice devKey='BoilerCH'>Hot Water</heatingDevice>
        <heatingDevice devKey='HFKitchen' setPoint='15.0' >Kitchen</heatingDevice>
        <heatingDevice devKey='HFEnsuite' setPoint='15.0' >Ensuite</heatingDevice>
        <heatingDevice devKey='HFFamilyBath' setPoint='15.0' >Family</heatingDevice>
        <heatingDevice devKey='HotWater' setPoint='57.0' >HotWater Temperature</heatingDevice>
        <heatingDevice devKey='Zone1' setPoint='21.0' >DownStairs</heatingDevice>
        <heatingDevice devKey='Zone2' setPoint='18.0' >UpStairs</heatingDevice>
        <heatingDevice devKey='Zone3' setPoint='15.0' >Guest</heatingDevice>

        <!-- This second part is stuff that is generated at system config, and can be updated through the UI -->
        <!-- structure is to support multiple schedule sets for different uses, e.g. winter,summer,holiday -->
        <schedules current="default">
            <scheduleSet devKey="default">
                <entry schKey="weekday1" days="1,2,3,4,5" time="05:30:00"/>
                <entry schKey="weekday2" days="1,2,3,4,5" time="08:00:00"/>
                <entry schKey="weekday3" days="1,2,3,4,5" time="16:00:00"/>
                <entry schKey="weekday4" days="1,2,3,4,5" time="22:00:00"/>
                <entry schKey="saturday1" days="6" time="07:30:00"/>
                <entry schKey="saturday2" days="6" time="22:30:00"/>
                <entry schKey="sunday1" days="0" time="07:30:00"/>
                <entry schKey="sunday2" days="0" time="22:30:00"/>
            </scheduleSet>
        </schedules>

        <!-- These can also be triggered by events targetted at heating ? -->
        <actionGroup schKey="weekday1">
            <action devKey="BoilerCH" action="On"/>
            <action devKey="BoilerHW" action="On"/>
            <action devKey="HotWater" setPoint="60.0"/>
            <action devKey="Zone1" setPoint="18.0"/>
            <action devKey="Zone2" setPoint="21.0"/>
            <action devKey="Zone3" setPoint="15.0"/>
        </actionGroup>
        <actionGroup schKey="weekday2">
            <action devKey="BoilerCH" action="Off"/>
            <action devKey="HotWater" setPoint="55.0"/>
        </actionGroup>
        <actionGroup schKey="weekday3">
            <action devKey="BoilerCH" action="On"/>
            <action devKey="HotWater" setPoint="60.0"/>
            <action devKey="Zone1" setPoint="21.0"/>
            <action devKey="Zone2" setPoint="18.0"/>
        </actionGroup>
        <actionGroup schKey="weekday4">
            <action devKey="BoilerCH" action="Off"/>
            <action devKey="BoilerHW" action="Off"/>
        </actionGroup>
        <actionGroup schKey="saturday1">
            <action devKey="BoilerCH" action="On"/>
            <action devKey="BoilerHW" action="On"/>
            <action devKey="HotWater" setPoint="60.0"/>
            <action devKey="Zone1" setPoint="18.0"/>
            <action devKey="Zone2" setPoint="21.0"/>
            <action devKey="Zone3" setPoint="15.0"/>
        </actionGroup>
        <actionGroup schKey="saturday2">
            <action devKey="BoilerCH" action="Off"/>
            <action devKey="BoilerHW" action="Off"/>
        </actionGroup>
        <actionGroup schKey="sunday1">
            <action devKey="BoilerCH" action="On"/>
            <action devKey="BoilerHW" action="On"/>
            <action devKey="HotWater" setPoint="60.0"/>
            <action devKey="Zone1" setPoint="18.0"/>
            <action devKey="Zone2" setPoint="21.0"/>
            <action devKey="Zone3" setPoint="15.0"/>
        </actionGroup>
        <actionGroup schKey="sunday2">
            <action devKey="BoilerCH" action="Off"/>
            <action devKey="BoilerHW" action="Off"/>
        </actionGroup>
    </eventInterface>

    <eventInterface module='EventHandlers.tests.TestEventLogger' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

</eventInterfaces>
"""

verifySched = {
    u'weekday1': {'time': '05:30:00', 'days': '-MTWtF-','schKey': 'weekday1' },
    u'weekday2': {'time': '08:00:00', 'days': '-MTWtF-','schKey': 'weekday2' },
    u'weekday3': {'time': '16:00:00', 'days': '-MTWtF-','schKey': 'weekday3' },
    u'weekday4': {'time': '22:00:00', 'days': '-MTWtF-','schKey': 'weekday4' },
    u'saturday1': {'time': '07:30:00', 'days': '------s','schKey': 'saturday1' },
    u'saturday2': {'time': '22:30:00', 'days': '------s','schKey': 'saturday2' },
    u'sunday1': {'time': '07:30:00', 'days': 'S------','schKey': 'sunday1' },
    u'sunday2': {'time': '22:30:00', 'days': 'S------','schKey': 'sunday2' },
    }

verifyDevices = {
    u'BoilerCH':'Boiler CH',
    u'BoilerHW':'Hot Water',
    u'Zone1':'DownStairs',
    u'Zone2':'UpStairs',
    u'Zone3':'Guest',
    u'HFKitchen':'Kitchen',
    u'HFEnsuite':'Ensuite',
    u'HFFamilyBath':'Family',
    u'HotWater':'HotWater Temperature',
    }

verifyActions = {
    u'weekday1': {
                    'BoilerCH': 'On', 
                    'BoilerHW': 'On', 
                    'HotWater': '60.0', 
                    'Zone1': '18.0',
                    'Zone2': '21.0',
                    'Zone3': '15.0' 
                 },
    u'weekday2': {
                    'BoilerCH': 'Off', 
                    'HotWater': '55.0' 
                 },
    u'weekday3': {
                    'BoilerCH': 'On', 
                    'HotWater': '60.0', 
                    'Zone1': '21.0',
                    'Zone2': '18.0' 
                 },
    u'weekday4': {
                    'BoilerCH': 'Off', 
                    'BoilerHW': 'Off', 
                 },
    u'saturday1': {
                    'BoilerCH': 'On', 
                    'BoilerHW': 'On', 
                    'HotWater': '60.0', 
                    'Zone1': '18.0',
                    'Zone2': '21.0',
                    'Zone3': '15.0' },
    u'saturday2': {
                    'BoilerCH': 'Off', 
                    'BoilerHW': 'Off', 
                   },
    u'sunday1': {
                    'BoilerCH': 'On', 
                    'BoilerHW': 'On', 
                    'HotWater': '60.0', 
                    'Zone1': '18.0',
                    'Zone2': '21.0',
                    'Zone3': '15.0' },
    u'sunday2': {
                    'BoilerCH': 'Off', 
                    'BoilerHW': 'Off', 
                },
    }

class TestHeating(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger( "TestHeating" )
        self._log.debug( "\n\nsetUp" )

        self.loader = None
        self.router = None

    def tearDown(self):
        self._log.debug( "\ntearDown" )

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        time.sleep(1)

    # Actual tests follow
    def testLoad(self):
        self._log.debug( "\ntestLoad" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeating) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        # We should see lots of events here as initial pass.
        oldLen = len(EventHandlers.tests.TestEventLogger._events)
        self.assert_( oldLen > 0 )
        EventHandlers.tests.TestEventLogger.logEvents()

    def testLoadVerify(self):
        self._log.debug( "\ntestLoadVerify" )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigHeating) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        deviceDict = dict(verifyDevices)
        schedDict = dict(verifySched)
        actionDict = dict(verifyActions)
        time.sleep(1)

        # see whether we received what we expected
        self._log.debug( "************************************************************" )
        for ev in EventHandlers.tests.TestEventLogger._events:
            od = ev.getPayload()
            self._log.debug( "%s:%s:%s" % (ev.getType(),ev.getSource(),od) )
            if ev.getSource() == 'schedule/device':
                if deviceDict.has_key( od["devKey"] ):
                    del deviceDict[od["devKey"]]
            elif ev.getSource() == 'schedule/time':
                if schedDict.has_key( od["schKey"] ):
                    del schedDict[od["schKey"]]
            elif ev.getSource() == 'schedule/action':
                if actionDict.has_key( od["schKey"] ):
                    del actionDict[od["schKey"]]

        self._log.debug( "************************************************************" )
        #verify devices
        for ent in deviceDict:
            self._log.debug( "%s, %s" % (ent,deviceDict[ent]) )
        self.assertEqual( len(deviceDict.keys()),  0 )
        #verify schedules
        for ent in schedDict:
            self._log.debug( "%s, %s" % (ent,schedDict[ent]) )
        self.assertEqual( len(schedDict.keys()),  0 )
        #verify actions
        for ent in actionDict:
            self._log.debug( "%s, %s" % (ent,actionDict[ent]) )
        self.assertEqual( len(actionDict.keys()),  0 )
            

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestHeating("testLoad"))
    suite.addTest(TestHeating("testLoadVerify"))
    return suite

if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestHeating( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
