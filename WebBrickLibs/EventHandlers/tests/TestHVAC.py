# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestHVAC.py 3201 2009-06-15 15:21:25Z philipp.schuster $
#
import sys, logging, time, os
from os.path import isfile
import unittest
from shutil import copyfile

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import EventHandlers.tests.Events as Events
from EventHandlers.tests.Utils import *

"""

"""

#
# zone 1 not used in tests
# zone 2 enabled,no weather, no occupancy.
# zone 3 enabled, no weather, follow occupancy
# zone 4 enabled, weather, no occupancy
# zone 5 enabled, weather, follow occupancy
#

# Configuration for the tests
#
# resources/hvac/PersistZone1 configures zone2 as enabled, no weather, no occupancy

TestHeatingVentilationACConfigAll = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone1"  name='HZone1' />
            <zone key="zone2"  name='HZone2' />
            <zone key="zone3"  name='HZone3' />
            <zone key="zone4"  name='HZone4' />
            <zone key="zone5"  name='HZone5' />
            <zone key="zone6"  name='HZone6' />
            <zone key="zone7"  name='HZone7' />
            <zone key="zone8"  name='HZone8' />
            <zone key="zone9"  name='HZone9' />
            <zone key="zone10"  name='HZone10' />
            <zone key="zone11"  name='HZone11' />
            <zone key="zone12"  name='HZone12' />
            <zone key="zone13"  name='HZone13' />
            <zone key="zone14"  name='HZone14' />
            <zone key="zone15"  name='HZone15' />
            <zone key="zone16"  name='HZone16' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
            <zonegroup key="2"  name='HZG2' />
            <zonegroup key="3"  name='HZG3' />
            <zonegroup key="4"  name='HZG4' />
            <zonegroup key="5"  name='HZG5' />
        </zonegroups>
        <heatsources>
            <heatsource key="1" type="boiler" name="Boiler" />
            <heatsource key="2" type="ground" name="Ground Source" />
            
            <heatsource key="3" type="multisolar" name="Multi Solar">
                <elevations>
                    <elevation key="east" type="elevation" name="East"/>
                    <elevation key="south" type="elevation" name="South"/>
                    <elevation key="west" type="elevation" name="West"/>
                </elevations>
            </heatsource>
            
            <heatsource key="4" type="solar" name="Solar" />
            <heatsource key="5" type="multiboiler" name="Multi Boiler" >
                <boilers>
                    <boiler key="1" name="Boiler 1" />
                    <boiler key="2" name="Boiler 2" />
                </boilers>
            </heatsource>
        </heatsources>
        <zonemaster active="1" />
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

TestHeatingVentilationACSolar = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone17" type='single' name='HZone17' />
        </zones>
        <zonegroups>
            <zonegroup key="6" name='HZG6' />
        </zonegroups>
        <heatsources>     
            <heatsource key="3" type="multisolar" name="Multi Solar">
                <elevations>
                    <elevation key="south" type="elevation" name="South"/>
                </elevations>
            </heatsource>
        </heatsources>
        <zonemaster active="1" />
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


TestHeatingVentilationACConfigGroup = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone1"  type='single' name='HZone1' />
            <zone key="zone2"  type='single' name='HZone2' />
            <zone key="zone3"  type='single' name='HZone3' />
            <zone key="zone4"  type='single' name='HZone4' />
            <zone key="zone5"  type='single' name='HZone5' />
            <zone key="zone6"  type='single' name='HZone6' />
            <zone key="zone7"  type='single' name='HZone7' />
            <zone key="zone8"  type='single' name='HZone8' />
            <zone key="zone9"  type='single' name='HZone9' />
            <zone key="zone10"  type='single' name='HZone10' />
            <zone key="zone11"  type='single' name='HZone11' />
            <zone key="zone12"  type='single' name='HZone12' />
            <zone key="zone13"  type='single' name='HZone13' />
            <zone key="zone14"  type='single' name='HZone14' />
            <zone key="zone15"  type='single' name='HZone15' />
            <zone key="zone16"  type='single' name='HZone16' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
            <zonegroup key="2"  name='HZG2' />
            <zonegroup key="3"  name='HZG3' />
            <zonegroup key="4"  name='HZG4' />
            <zonegroup key="5"  name='HZG5' />
        </zonegroups>
        <zonemaster active="0" />
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
# likely to be  removed again later
TestHeatingVentilationACConfigMultiZone = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        
        <zones>
            <zone key="multizone1"  type='multi' name='1' >
                <parts>
                    <part key="zone1" name='HZone1' />
                    <part key="zone2" name='HZone2' />
                </parts>
            </zone>


        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
            <zonegroup key="2"  name='HZG2' />
            <zonegroup key="3"  name='HZG3' />
            <zonegroup key="4"  name='HZG4' />
            <zonegroup key="5"  name='HZG5' />
        </zonegroups>
        <zonemaster active="0" />
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


TestHeatingVentilationACConfigHeatSourceGeneric = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <heatsources>
            <heatsource key="1" type="generic" name="Boiler default" />
            <heatsource key="2" type="generic" name="Boiler Custom" runtime="3" interval="2"/>
        </heatsources>
        <zonemaster active="1" />
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

TestHeatingVentilationACConfigHeatSource1 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <heatsources>
            <heatsource key="1" type="boiler" name="Boiler" />
        </heatsources>
        <zonemaster active="1" />
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

TestHeatingVentilationACConfigHeatSource2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <heatsources>
            <heatsource key="2" type="ground" name="Ground Source" />
        </heatsources>
        <zonemaster active="1" />
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

TestHeatingVentilationACConfigHeatSource3 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>      
        <heatsources>
            <heatsource key="3" type="multisolar" name="Multi Solar">
                <elevations>
                    <elevation key="east" type="elevation" name="East" />
                    <elevation key="south" type="elevation" name="South" />
                    <elevation key="west" type="elevation" name="West" />
                </elevations>
            </heatsource>
        </heatsources>
        <zonemaster active="1" />
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

TestHeatingVentilationACConfigHeatSource4 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <heatsources>
            <heatsource key="4" type="solar" name="Solar" />
        </heatsources>
        <zonemaster active="1" />
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

TestMultipleBoilerHeatSource = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        
        <heatsources>
            <heatsource key="5" type="multiboiler" name="Multiple Boiler"
                    flowreturnmin="4" flowreturnmax="10" checkinterval="4" >
                <boilers>
                    <boiler key="1" name="Boiler 1" />
                    <boiler key="2" name="Boiler 2" />
                </boilers>
            </heatsource>
        </heatsources>
        <zonemaster active="1" />
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

TestHeatingVentilationACConfigMaster = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone1"  type='single' name='HZone1' />
            <zone key="zone2"  type='single' name='HZone2' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
            <zonegroup key="2"  name='HZG2' />
            <zonegroup key="3"  name='HZG3' />
            <zonegroup key="4"  name='HZG4' />
            <zonegroup key="5"  name='HZG5' />
        </zonegroups>
        <heatsources>
            <heatsource key="1" type="boiler" name="Boiler" />
            <heatsource key="2" type="ground" name="Ground Source" />
            <heatsource key="4" type="solar" name="Solar" />
        </heatsources>
        <zonemaster active="1" />
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
TestHeatingVentilationACConfig2Groups2Zones = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone1"  type='single' name='HZone1' />
            <zone key="zone2"  type='single' name='HZone2' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
            <zonegroup key="2"  name='HZG2' />
        </zonegroups>
        <heatsources>
            <heatsource key="1" type="boiler" name="Boiler" />
            <heatsource key="2" type="ground" name="Ground Source" />
            <heatsource key="4" type="solar" name="Solar" />
        </heatsources>
        <zonemaster active="1" />
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

TestHeatingVentilationACConfig1 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZonesAll'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone1"  type='single' name='HZone1' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
        </zonegroups>
        <heatsources>
            <heatsource key="1" type="boiler" name="Boiler" />
        </heatsources>
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


# resources/hvac/Cfg2 configures zone3 as enabled, no weather, follow occupancy
TestHeatingVentilationACConfig2 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZone2'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone2"  type='single' name='HZone2' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
        </zonegroups>
        <heatsources>
            <heatsource key="1" type="boiler" name="Boiler" />
        </heatsources>
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

# resources/hvac/PersistZone3 configures zone3 as enabled, no weather, follow occupancy
TestHeatingVentilationACConfig3 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZone3'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone3"  type='single' name='HZone3' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
        </zonegroups>
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

# resources/hvac/PersistZone4 configures zone4 as enabled, weather compensation 1, no occupancy
TestHeatingVentilationACConfig4 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZone4'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone4"  type='single' name='HZone4' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
        </zonegroups>
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

# resources/hvac/PersistZone5 configures zone5 as enabled, weather compensation 1, follow occupancy
TestHeatingVentilationACConfig5 = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>

    <eventInterface module='EventHandlers.PersistFile' name='PersistFile' persistFile='work/PersistZone5'>
    </eventInterface>

    <eventInterface module='EventHandlers.HVAC' name='HeatingVentilationAC'>
        <zones>
            <zone key="zone5"  type='single' name='HZone5' />
        </zones>
        <zonegroups>
            <zonegroup key="1"  name='HZG1' />
        </zonegroups>
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

# Some test events that can be sent.
evtMasterRunning = makeEvent( 'http://id.webbrick.co.uk/zones/master', 'zonemaster/running' )
evtMasterStop = makeEvent( 'http://id.webbrick.co.uk/zones/master', 'zonemaster/stop' )
evtMasterRun = makeEvent( 'http://id.webbrick.co.uk/zones/master', 'zonemaster/run' )
evtMasterStopped = makeEvent( 'http://id.webbrick.co.uk/zones/master', 'zonemaster/stopped' )
evtMasterDebug = makeEvent( 'http://id.webbrick.co.uk/zones/master', 'zonemaster/debug' )

evtHS1RequestRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/1/requestrun' )
evtHS1DoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/1/dorun' )
evtHS1Running = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/1/running' )
evtHS1RequestStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/1/requeststop' )
evtHS1DoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/1/dostop' )
evtHS1Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/1/stopped' )

evtHS2RequestRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/2/requestrun' )
evtHS2DoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/2/dorun' )
evtHS2Running = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/2/running' )
evtHS2RequestStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/2/requeststop' )
evtHS2DoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/2/dostop' )
evtHS2Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/2/stopped' )
evtHS2Enable = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zoneheatsource/2/enabled', {'val': 1} )
evtHS2Disable = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zoneheatsource/2/enabled', {'val': 0} )

evtHS3RequestRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/requestrun' )
evtHS3RequestStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/requeststop' )
evtHS3CommonDoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/dorun' )
evtHS3CommonDoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/dostop' )
evtHS3EastDoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/east/dorun' )
evtHS3EastDoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/east/dostop' )
evtHS3SouthDoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/south/dorun' )
evtHS3SouthDoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/south/dostop' )
evtHS3WestDoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/west/dorun' )
evtHS3WestDoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/west/dostop' )
evtHS3Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/stopped' )
evtHS3Running = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/3/running' )

evtHS3PanelEastTemp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/1', {'val': 5.0} )
evtHS3PanelEastTemp25 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/1', {'val': 25.0} )
evtHS3PanelEastTemp95 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/1', {'val': 95.0} )
evtHS3PanelSouthTemp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/2', {'val': 5.0} )
evtHS3PanelSouthTemp25 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/2', {'val': 25.0} )
evtHS3PanelSouthTemp95 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/2', {'val': 95.0} )
evtHS3PanelWestTemp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/3', {'val': 5.0} )
evtHS3PanelWestTemp25 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/3', {'val': 25.0} )
evtHS3PanelWestTemp95 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/3', {'val': 95.0} )
evtHS3HeatExTemp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/6', {'val': 5.0} )
evtHS3HeatExTemp25 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/6', {'val': 25.0} )
evtHS3HeatExTemp95 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/903/CT/6', {'val': 95.0} )

evtHS4RequestRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/4/requestrun' )
evtHS4RequestStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/4/requeststop' )
evtHS4DoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/4/dorun' )
evtHS4DoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/4/dostop' )
evtHS4Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/4/stopped' )
evtHS4Running = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/4/running' )

evtHS4PanelTemp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/904/CT/0', {'val': 5.0} )
evtHS4PanelTemp25 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/904/CT/0', {'val': 25.0} )
evtHS4PanelTemp95 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/904/CT/0', {'val': 95.0} )
evtHS4HeatExTemp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/904/CT/5', {'val': 5.0} )
evtHS4HeatExTemp25 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/904/CT/5', {'val': 25.0} )
evtHS4HeatExTemp95 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/904/CT/5', {'val': 95.0} )

evtHS5RequestRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/requestrun' )
evtHS5DoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/dorun' )
evtHS5Running = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/running' )
evtHS5RequestStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/requeststop' )
evtHS5DoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/dostop' )
evtHS5Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/stopped' )
evtHS5_1DoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/1/dorun' )
evtHS5_1DoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/1/dostop' )
evtHS5_1Running = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/1/running' )
evtHS5_1Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/1/stopped' )
evtHS5_2DoRun = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/2/dorun' )
evtHS5_2DoStop = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/2/dostop' )
evtHS5_2Running = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/2/running' )
evtHS5_2Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/heatsource', 'heatsource/5/2/stopped' )
evtHS5FlowTemp80 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/905/CT/0', {'val': 80.0} )
evtHS5ReturnTemp60 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/905/CT/1', {'val': 60.0} )
evtHS5ReturnTemp75 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/905/CT/1', {'val': 75.0} )

evtZG1Running = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/1/running' )
evtZG1Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/1/stop' )
evtZG1Run = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/1/run' )
evtZG1Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/1/stopped' )
evtZG1HeatSource = makeEvent( 'http://id.webbrick.co.uk/zones/group/heatsource', 'zonegroup/1/heatsource' )

evtZG2Running = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/2/running' )
evtZG2Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/2/stop' )
evtZG2Run = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/2/run' )
evtZG2Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/2/stopped' )
evtZG2HeatSource = makeEvent( 'http://id.webbrick.co.uk/zones/group/heatsource', 'zonegroup/2/heatsource' )

evtZG3Running = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/3/running' )
evtZG3Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/3/stop' )
evtZG3Run = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/3/run' )
evtZG3Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/3/stopped' )
evtZG3HeatSource = makeEvent( 'http://id.webbrick.co.uk/zones/group/heatsource', 'zonegroup/3/heatsource' )

evtZG4Running = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/4/running' )
evtZG4Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/4/stop' )
evtZG4Run = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/4/run' )
evtZG4Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/4/stopped' )
evtZG4HeatSource = makeEvent( 'http://id.webbrick.co.uk/zones/group/heatsource', 'zonegroup/4/heatsource' )

evtZG5Running = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/5/running' )
evtZG5Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/5/stop' )
evtZG5Run = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/5/run' )
evtZG5Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/5/stopped' )
evtZG5HeatSource = makeEvent( 'http://id.webbrick.co.uk/zones/group/heatsource', 'zonegroup/5/heatsource' )

evtZG6Running = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/6/running' )
evtZG6Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/6/stop' )
evtZG6Run = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/6/run' )
evtZG6Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zonegroup', 'zonegroup/6/stopped' )
evtZG6HeatSource = makeEvent( 'http://id.webbrick.co.uk/zones/group/heatsource', 'zonegroup/6/heatsource' )

evtZone1Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone1/running' )
evtZone1Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone1/stop' )
evtZone1Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone1/run' )
evtZone1Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone1/stopped' )
evtZone2Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone2/running' )
evtZone2Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone2/stop' )
evtZone2Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone2/run' )
evtZone2Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone2/stopped' )
evtZone3Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone3/running' )
evtZone3Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone3/stop' )
evtZone3Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone3/run' )
evtZone3Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone3/stopped' )
evtZone4Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone4/running' )
evtZone4Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone4/stop' )
evtZone4Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone4/run' )
evtZone4Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone4/stopped' )
evtZone5Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone5/running' )
evtZone5Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone5/stop' )
evtZone5Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone5/run' )
evtZone5Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone5/stopped' )
evtZone6Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone6/running' )
evtZone6Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone6/stop' )
evtZone6Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone6/run' )
evtZone6Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone6/stopped' )
evtZone7Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone7/running' )
evtZone7Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone7/stop' )
evtZone7Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone7/run' )
evtZone7Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone7/stopped' )
evtZone8Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone8/running' )
evtZone8Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone8/stop' )
evtZone8Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone8/run' )
evtZone8Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone8/stopped' )
evtZone9Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone9/running' )
evtZone9Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone9/stop' )
evtZone9Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone9/run' )
evtZone9Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone9/stopped' )
evtZone10Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone10/running' )
evtZone10Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone10/stop' )
evtZone10Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone10/run' )
evtZone10Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone10/stopped' )
evtZone11Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone11/running' )
evtZone11Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone11/stop' )
evtZone11Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone11/run' )
evtZone11Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone11/stopped' )
evtZone12Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone12/running' )
evtZone12Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone12/stop' )
evtZone12Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone12/run' )
evtZone12Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone12/stopped' )
evtZone13Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone13/running' )
evtZone13Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone13/stop' )
evtZone13Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone13/run' )
evtZone13Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone13/stopped' )
evtZone14Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone14/running' )
evtZone14Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone14/stop' )
evtZone14Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone14/run' )
evtZone14Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone14/stopped' )
evtZone15Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone15/running' )
evtZone15Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone15/stop' )
evtZone15Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone15/run' )
evtZone15Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone15/stopped' )
evtZone16Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone16/running' )
evtZone16Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone16/stop' )
evtZone16Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone16/run' )
evtZone16Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone16/stopped' )
evtZone17Running = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone17/running' )
evtZone17Stop = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone17/stop' )
evtZone17Run = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone17/run' )
evtZone17Stopped = makeEvent( 'http://id.webbrick.co.uk/zones/zone', 'zone17/stopped' )

evtWeather1Run = makeEvent( 'http://id.webbrick.co.uk/zones/weather', 'weather/1', {'state':'Run'} )
evtWeather1HoldOff = makeEvent( 'http://id.webbrick.co.uk/zones/weather', 'weather/1', {'state':'HoldOff'} )
evtWeather2Run = makeEvent( 'http://id.webbrick.co.uk/zones/weather', 'weather/2', {'state':'Run'} )
evtWeather2HoldOff = makeEvent( 'http://id.webbrick.co.uk/zones/weather', 'weather/2', {'state':'HoldOff'} )
evtWeather3Run = makeEvent( 'http://id.webbrick.co.uk/zones/weather', 'weather/3', {'state':'Run'} )
evtWeather3HoldOff = makeEvent( 'http://id.webbrick.co.uk/zones/weather', 'weather/3', {'state':'HoldOff'} )

evtZone1Temp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/1/CT/0', {'val': 5.0} )
evtZone1Temp15 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/1/CT/0', {'val': 15.0} )
evtZone1Temp22 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/1/CT/0', {'val': 22.0} )
evtZone1SetPoint0 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone1/set', {'val': 0.0} )
evtZone1SetPoint14 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone1/set', {'val': 14.0} )
evtZone1SetPoint18 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone1/set', {'val': 18.0} )
evtZone1SetPoint25 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone1/set', {'val': 25.0} )

evtZone2Temp4 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/2/CT/0', {'val': 4.0} )
evtZone2Temp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/2/CT/0', {'val': 5.0} )
evtZone2Temp13 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/2/CT/0', {'val': 13.0} )
evtZone2Temp14 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/2/CT/0', {'val': 14.0} )
evtZone2Temp15 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/2/CT/0', {'val': 15.0} )
evtZone2Temp22 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/2/CT/0', {'val': 22.0} )
evtZone2SetPoint0 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone2/set', {'val': 0.0} )
evtZone2SetPoint14 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone2/set', {'val': 14.0} )
evtZone2SetPoint18 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone2/set', {'val': 18.0} )
evtZone2SetPoint25 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone2/set', {'val': 25.0} )
evtZone2ManSetPoint0 = makeEvent( 'http://id.webbrick.co.uk/events/zones/manual', 'zone2/manual/set', {'val': 0.0} )
evtZone2ManSetPoint8 = makeEvent( 'http://id.webbrick.co.uk/events/zones/manual', 'zone2/manual/set', {'val': 8.0} )
evtZone2ManSetPoint14 = makeEvent( 'http://id.webbrick.co.uk/events/zones/manual', 'zone2/manual/set', {'val': 14.0} )
evtZone2ManSetPoint18 = makeEvent( 'http://id.webbrick.co.uk/events/zones/manual', 'zone2/manual/set', {'val': 18.0} )
evtZone2ManSetPoint25 = makeEvent( 'http://id.webbrick.co.uk/events/zones/manual', 'zone2/manual/set', {'val': 25.0} )

evtZone3Temp15 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/3/CT/0', {'val': 15.0} )
evtZone3SetPoint14 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone3/set', {'val': 14.0} )
evtZone3SetPoint18 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone3/set', {'val': 18.0} )

evtZone4Temp15 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/4/CT/0', {'val': 15.0} )
evtZone4SetPoint14 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone4/set', {'val': 14.0} )
evtZone4SetPoint18 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone4/set', {'val': 18.0} )

evtZone5Temp15 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/5/CT/0', {'val': 15.0} )
evtZone5SetPoint14 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone5/set', {'val': 14.0} )
evtZone5SetPoint18 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone5/set', {'val': 18.0} )
evtZone5ManualSetPoint22 = makeEvent( 'http://id.webbrick.co.uk/events/zones/manual', 'zone5/manual/set', {'val': 22.0} )

evtZone17Temp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/17/CT/0', {'val': 5.0} )
evtZone17Temp15 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/17/CT/0', {'val': 15.0} )
evtZone17Temp22 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/17/CT/0', {'val': 22.0} )
evtZone17SetPoint14 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone17/set', {'val': 14.0} )
evtZone17SetPoint18 = makeEvent( 'http://id.webbrick.co.uk/events/schedule/control', 'zone17/set', {'val': 18.0} )
evtZone17ManualSetPoint22 = makeEvent( 'http://id.webbrick.co.uk/events/zones/manual', 'zone17/manual/set', {'val': 22.0} )

evtTemp5 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/5/CT/1', {'val': 5.0} )
evtTemp10 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/5/CT/1', {'val': 10.0} )
evtTemp15 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/5/CT/1', {'val': 15.0} )
evtTemp20 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/5/CT/1', {'val': 20.0} )
evtTemp22 = makeEvent( 'http://id.webbrick.co.uk/events/webbrick/CT', 'webbrick/5/CT/1', {'val': 22.0} )

evtOccupied = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'occupants/home', {'val': 1} )
evtUnOccupied = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'occupants/home', {'val': 0} )

evtZone2Enable = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zone2/enabled', {'val': 1} )
evtZone2Disable = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zone2/enabled', {'val': 0} )

evtZone2FrostStat0 = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zone2/matStat', {'val': 0} )
evtZone2FrostStat5 = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zone2/matStat', {'val': 5.0} )
evtZone2FrostStat9 = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zone2/matStat', {'val': 9.0} )
evtZone2FrostStat16 = makeEvent( 'http://id.webbrick.co.uk/events/config/get', 'zone2/matStat', {'val': 16.0} )

masterSingleFileList = (
                    "../../../WebBrickGateway/resources/samples1/eventdespatch/zones_inactive/zonemaster_single_inputs.xml",
                    "../../../WebBrickGateway/resources/eventdespatch/System/testdummies/zonemaster_outputs.xml",
        )

masterDualFileList = (
                    "../../../WebBrickGateway/resources/samples1/eventdespatch/zones_inactive/zonemaster_solar_and_boiler_inputs.xml",
                    "../../../WebBrickGateway/resources/eventdespatch/System/testdummies/zonemaster_outputs.xml",
        )

masterMultipleFileList = (
                    "./resources/hvac/zonemaster_multiple_inputs.xml",
                    "./resources/hvac/zonemaster_multiple_outputs.xml",
        )

heatSourceGenericFileList = ( 
                    "./resources/hvac/zoneheatsource_generic_inputs.xml", 
                    "./resources/hvac/zoneheatsource_generic_outputs.xml",   
        )
        
# Oil/Gas Boiler
heatSource1FileList = (
                    "./resources/hvac/zoneheatsource_boiler_1_inputs.xml",
                    "./resources/hvac/zoneheatsource_boiler_1_outputs.xml",
                    
        )

# ground source heat pump
heatSource2FileList = (
                    "./resources/hvac/zoneheatsource_heatpump_2_inputs.xml",
                    "./resources/hvac/zoneheatsource_heatpump_2_outputs.xml",
        )

# Multi Solar Panel
heatSource3FileList = (
                    "./resources/hvac/zoneheatsource_multisolar_3_inputs.xml",
                    "./resources/hvac/zoneheatsource_multisolar_3_outputs.xml",
        )

# Single Solar
heatSource4FileList = (
                    "./resources/hvac/zoneheatsource_solar_4_inputs.xml",
                    "./resources/hvac/zoneheatsource_solar_4_outputs.xml",
        )
        
# Multi Boiler 
heatSource5FileList = (
                    "./resources/hvac/zoneheatsource_multiboiler_5_inputs.xml",
                    "./resources/hvac/zoneheatsource_multiboiler_5_outputs.xml",
        )

groupFileList = (
                    "./resources/hvac/zonegroup1_inputs.xml",
                    "./resources/hvac/zonegroup1_outputs.xml",
                    
                    "./resources/hvac/zonegroup2_inputs.xml",
                    "./resources/hvac/zonegroup2_outputs.xml",
                    
                    "./resources/hvac/zonegroup3_inputs.xml",
                    "./resources/hvac/zonegroup3_outputs.xml",
                    
                    "./resources/hvac/zonegroup4_inputs.xml",
                    "./resources/hvac/zonegroup4_outputs.xml",
                    
                    "./resources/hvac/zonegroup5_inputs.xml",
                    "./resources/hvac/zonegroup5_outputs.xml",
                    
                    "./resources/hvac/zonegroup6_inputs.xml",
                    "./resources/hvac/zonegroup6_outputs.xml",
            )

zone1FileList = (
                    "./resources/hvac/zone1_inputs.xml",
                    "./resources/hvac/zone1_outputs.xml",)
zone2FileList = (
                    "./resources/hvac/zone2_inputs.xml",
                    "./resources/hvac/zone2_outputs.xml",)
zone3FileList = (
                    "./resources/hvac/zone3_inputs.xml",
                    "./resources/hvac/zone3_outputs.xml",)
zone4FileList = (
                    "./resources/hvac/zone4_inputs.xml",
                    "./resources/hvac/zone4_outputs.xml",)
zone5FileList = (
                    "./resources/hvac/zone5_inputs.xml",
                    "./resources/hvac/zone5_outputs.xml",)
zone6FileList = (
                    "./resources/hvac/zone6_inputs.xml",
                    "./resources/hvac/zone6_outputs.xml",)
zone7FileList = (
                    "./resources/hvac/zone7_inputs.xml",
                    "./resources/hvac/zone7_outputs.xml",)
zone8FileList = (
                    "./resources/hvac/zone8_inputs.xml",
                    "./resources/hvac/zone8_outputs.xml",)
zone9FileList = (
                    "./resources/hvac/zone9_inputs.xml",
                    "./resources/hvac/zone9_outputs.xml",)
zone10FileList = (
                    "./resources/hvac/zone10_inputs.xml",
                    "./resources/hvac/zone10_outputs.xml",)
zone11FileList = (
                    "./resources/hvac/zone11_inputs.xml",
                    "./resources/hvac/zone11_outputs.xml",)
zone12FileList = (
                    "./resources/hvac/zone12_inputs.xml",
                    "./resources/hvac/zone12_outputs.xml",)
zone13FileList = (
                    "./resources/hvac/zone13_inputs.xml",
                    "./resources/hvac/zone14_outputs.xml",)
zone14FileList = (
                    "./resources/hvac/zone14_inputs.xml",
                    "./resources/hvac/zone14_outputs.xml",)
zone15FileList = (
                    "./resources/hvac/zone15_inputs.xml",
                    "./resources/hvac/zone15_outputs.xml",)
zone16FileList = (
                    "./resources/hvac/zone16_inputs.xml",
                    "./resources/hvac/zone16_outputs.xml",)
zone17FileList = (
                    "./resources/hvac/zone17_inputs.xml",
                    "./resources/hvac/zone17_outputs.xml",)                   
                    

zone1FileListInputOnly = (
                    "./resources/hvac/zone1_inputs.xml",)   
                    
zone2FileListInputOnly = (
                    "./resources/hvac/zone2_inputs.xml",)                    

weatherFileList = (
                    "./resources/hvac/zoneweather_inputs.xml",
                    "./resources/hvac/zoneweather_outputs.xml",
        )

workDir =  "./work"
sourceDir =  "./resources/hvac"

class TestHeatingVentilationAC(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestHeatingVentilationAC" )
        self._log.debug( "setUp" )
        self.runner = None
        # clear work directory and copy all from resources/Zones/*
        """        
        for fn in os.listdir( workDir ):
            fnf = "%s/%s" % (workDir,fn)
            if isfile(fnf):
                self._log.debug( "remove %s", fnf )
                os.remove( fnf )
        for fn in os.listdir( sourceDir ):
            fnf = "%s/%s" % (sourceDir,fn)
            if isfile(fnf):
                self._log.debug( "Copy %s", fnf )
                copyfile( fnf, "%s/%s" % (workDir,fn) )
        """

    def tearDown(self):
        self._log.debug( "tearDown" )

        TestEventLogger.logEvents()

        if self.runner:
            self.runner.stop()  # all tasks
            self.runner = None

    def copyConfig(self, name):
        copyfile( "%s/%s.xml" % (sourceDir,name), "%s/%s.xml" % (workDir,name) )
    
    def expectNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1
        if (len(TestEventLogger._events) != cnt):
            TestEventLogger.logEvents()
        
        self.assertEqual( len(TestEventLogger._events), cnt)

    def waitNevents(self, cnt ):
        idx = 20
        while (len(TestEventLogger._events) < cnt) and (idx > 0):
            time.sleep(0.05)
            idx = idx - 1
        if (len(TestEventLogger._events) < cnt):
            TestEventLogger.logEvents()
            self.assertEqual( len(TestEventLogger._events), cnt)

    def checkEvents(self, send, expect ):
        """
        send is tuples of an event and the number of events expected to be seen in the event log from the sending of the event
        expect is a list of events to be seen. We currently only check event source.
        
        If send has None as send event then we just check for events.
        """
        offset = len(TestEventLogger._events)
        idx = 0
        limit = 0

        for ntry in send:
            if ntry[0]:
                self.router.publish( EventAgent("TestHeatingVentilationAC"), ntry[0] )
            limit = limit + ntry[1]
            while ( idx < limit ):
                self.waitNevents(idx+1)
                self._log.debug("%i check %s again %s" % (idx,TestEventLogger._events[idx],expect[idx]) )
                if isinstance(expect[idx], basestring):
                    # event source
                    self.assertEqual( TestEventLogger._events[idx].getSource(), expect[idx], 
                            "Mismatch at %i have %s, expect %s" % (idx,TestEventLogger._events[idx].getSource(), expect[idx]))
                elif isinstance(expect[idx], tuple) or isinstance(expect[idx], list):
                    # contains a test against the payload.
                    # assumes payload is a dictionary
                    # event source, attr, value
                    self.assertEqual( TestEventLogger._events[idx].getSource(), expect[idx][0], 
                            "Mismatch at %i have %s, expect %s" % (idx,TestEventLogger._events[idx].getSource(), expect[idx][0]))
                    od = TestEventLogger._events[idx].getPayload()
                    self.assert_( od.has_key(expect[idx][1]),
                            "Mismatch at %i expect to see %s in %s" % (idx,expect[idx][1], od))
                    self.assertEqual( od[expect[idx][1]], expect[idx][2], 
                            "Mismatch at %i have %s, expect %s" % (idx,od[expect[idx][1]], expect[idx][2]))
                else:
                    # assume event
                    self.assertEqual( TestEventLogger._events[idx].getSource(), expect[idx].getSource(), 
                            "Mismatch at %i have %s, expect %s" % (idx,TestEventLogger._events[idx].getSource(), expect[idx].getSource()))
                idx = idx + 1
        time.sleep(1)   # let system settle.
        # have we received only those we expect
        self.assertEqual( len(TestEventLogger._events), limit)

    def loadPrimitive(self, cfgFile, cfgstr, fileListList):
        self.copyConfig(cfgFile)
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(cfgstr) )
        if fileListList:
            for fileList in fileListList:
                for fn in fileList:
                    self.loader.loadFromFile( fn )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        
        time.sleep(1)   # let persist run.
        TestEventLogger.logEvents()

        # we may see persist events multiple times and we may add more.
        self.assertNotEqual( len(TestEventLogger._events), 0)
#        self.assertEqual( len(TestEventLogger._events), 22)
        TestEventLogger.clearEvents()
        # clear events.

    def load(self):
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, None )

    def loadMasterSingle(self):
        # a tuple or a list is required for second parameter
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (masterSingleFileList,heatSource1FileList,) )
            
    def loadMasterDual(self):
        # a tuple or a list is required for second parameter
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (masterDualFileList,heatSource1FileList,heatSource3FileList) )
            
    def loadMasterMultiple(self):
        # a tuple or a list is required for second parameter
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfig2Groups2Zones, (masterMultipleFileList,heatSource1FileList,heatSource2FileList,heatSource4FileList, groupFileList, zone1FileList, zone2FileList) )
            
    def loadGroup(self):
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigGroup, (groupFileList,) )   # a tuple or a list is required

    def loadZone1(self):
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone1FileList,) )   # a tuple or a list is required
            
    def loadZone2(self):
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone2FileList,) )   # a tuple or a list is required

    def loadZone3(self):
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone3FileList,) )   # a tuple or a list is required

    def loadZone4(self):
        self.loadPrimitive( "PersistZone4", TestHeatingVentilationACConfig4, (zone4FileList,weatherFileList) )   # a tuple or a list is required

    def loadZone5(self):
        self.loadPrimitive( "PersistZone5", TestHeatingVentilationACConfig5, (zone5FileList,weatherFileList) )   # a tuple or a list is required

#    def loadZone6(self):
#        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone6FileList,) )   # a tuple or a list is required

#    def loadZone7(self):
#        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone7FileList,) )   # a tuple or a list is required

#    def loadZone8(self):
#        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone8FileList,) )   # a tuple or a list is required

#    def loadZone9(self):
#        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone9FileList,) )   # a tuple or a list is required
            
    def loadAllZones(self):
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (zone1FileList,zone2FileList,zone3FileList,zone4FileList,
            zone5FileList,zone6FileList,zone7FileList,zone8FileList,
            zone9FileList,zone10FileList,zone11FileList,zone12FileList,
            zone13FileList,zone14FileList,zone15FileList,zone16FileList,
            ) )   # a tuple or a list is required
            
    def loadWeather(self):
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfig2, (weatherFileList,) )   # a tuple or a list is required
            
    def loadMasterAndGroups(self):
        # a tuple or a list is required for second parameter
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, (masterSingleFileList, groupFileList, heatSource1FileList) )

    # Actual tests follow
    def testLoad(self):
        self._log.debug( "testLoad" )
        self.load()
        TestEventLogger.logEvents()
            
    def testLoadAll(self):
        self._log.debug( "testLoadAll" )
        # This test is just so we see all files will load.
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigAll, 
            (   
                # masterSingleFileList, 
                # masterDualFileList, 
                masterMultipleFileList, 
                heatSource1FileList,
                heatSource2FileList,
                heatSource3FileList,
                groupFileList, 
                weatherFileList,
                zone1FileList,zone2FileList,zone3FileList,zone4FileList,
                zone5FileList,zone6FileList,zone7FileList,zone8FileList,
                zone9FileList,zone10FileList,zone11FileList,zone12FileList,
                zone13FileList,zone14FileList,zone15FileList,zone16FileList,
            ) )   # a tuple or a list is required
        TestEventLogger.logEvents()

    def testZoneMasterSingleGroup1(self):
        self._log.debug( "testZoneMasterSingleGroup1" )
        self.loadMasterSingle()

        # the events we send
        send = [ (evtZG1Running,5),
            (Events.evtMinute1,7),
            (evtZG1Stop,4),
            (Events.evtMinute1,8),
            ]
        # the events that we expect to be logged.
        expect = [ evtZG1Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/1/heatsource",
            "zone1/heatsource",
            
            evtZG1Stop,
            evtHS1RequestStop,
            "zonegroup/1/heatsource",
            "zone1/heatsource",
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)
            
    def testZoneMasterSingleGroup2(self):
        self._log.debug( "testZoneMasterSingleGroup2" )
        self.loadMasterSingle()

        # the events we send
        send = [ (evtZG2Running,5),
            (Events.evtMinute1,11),
            (evtZG2Stop,8),
            (Events.evtMinute1,8),
            ]
        # the events that we expect to be logged.
        expect = [ evtZG2Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/2/heatsource",
            "zone3/heatsource",
            "zone2/heatsource",
            "zone6/heatsource",
            "zone5/heatsource",  
            "zone4/heatsource",
            
            evtZG2Stop,
            evtHS1RequestStop,
            "zonegroup/2/heatsource",
            "zone3/heatsource",
            "zone2/heatsource",
            "zone6/heatsource",
            "zone5/heatsource",  
            "zone4/heatsource",
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)
            
    def testZoneMasterSingleGroup3(self):
        self._log.debug( "testZoneMasterSingleGroup3" )
        self.loadMasterSingle()
        
        # the events we send
        send = [ (evtZG3Running,5),
            (Events.evtMinute1,11),
            (evtZG3Stop,8),
            (Events.evtMinute1,8),
            ]
        # the events that we expect to be logged.
        expect = [ evtZG3Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/3/heatsource",
            "zone11/heatsource",
            "zone10/heatsource",
            "zone7/heatsource",
            "zone9/heatsource",  
            "zone8/heatsource",
            
            evtZG3Stop,
            evtHS1RequestStop,
            "zonegroup/3/heatsource",
            "zone11/heatsource",
            "zone10/heatsource",
            "zone7/heatsource",
            "zone9/heatsource",  
            "zone8/heatsource",
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)
            
    def testZoneMasterSingleGroup4(self):
        self._log.debug( "testZoneMasterSingleGroup4" )
        self.loadMasterSingle()
        
        # the events we send
        send = [ (evtZG4Running,5),
            (Events.evtMinute1,9),
            (evtZG4Stop,6),
            (Events.evtMinute1,8),
            ]
        # the events that we expect to be logged.
        expect = [ evtZG4Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/4/heatsource",
            "zone13/heatsource",
            "zone12/heatsource",
            "zone14/heatsource",
            
            evtZG4Stop,
            evtHS1RequestStop,
            "zonegroup/4/heatsource",
            "zone13/heatsource",
            "zone12/heatsource",
            "zone14/heatsource",
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)
            
    def testZoneMasterSingleGroup5(self):
        self._log.debug( "testZoneMasterSingleGroup5" )
        self.loadMasterSingle()
        
        # the events we send
        send = [ (evtZG5Running,5),
            (Events.evtMinute1,8),
            (evtZG5Stop,5),
            (Events.evtMinute1,8),
            ]
        # the events that we expect to be logged.
        expect = [ evtZG5Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/5/heatsource",
            "zone16/heatsource",
            "zone15/heatsource",
            
            evtZG5Stop,
            evtHS1RequestStop,
            "zonegroup/5/heatsource",
            "zone16/heatsource",
            "zone15/heatsource",
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)
            
    def testZoneMasterPair(self):
        self._log.debug( "testZoneMasterPair" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigMaster, (masterSingleFileList, heatSource1FileList,) )


        # the events we send
        send = [ (evtZG1Running,5),
            (Events.evtMinute1,6),
            (evtZG2Running,3),
            (evtZG2Stop,3),
            (evtZG1Stop,3),
            (Events.evtMinute1,8),
            ]
        # the events that we expect to be logged.
        expect = [ evtZG1Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/1/heatsource",
            
            evtZG2Running,
            "zonegroup/2/heatsource",
            "zone2/heatsource",
            
            evtZG2Stop,
            "zonegroup/2/heatsource",
            "zone2/heatsource",
            evtZG1Stop,
            evtHS1RequestStop,
            "zonegroup/1/heatsource",
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]
            
        self.checkEvents(send, expect)

    def testZoneMasterAll(self):
        self._log.debug( "testZoneMasterAll" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigMaster, (masterSingleFileList,heatSource1FileList,) )

        # the events we send
        send = [ (evtZG1Running,5),
            (Events.evtMinute1,6),
            (evtZG2Running,3),
            (Events.evtMinute1,5),
            (evtZG3Running,2),
            (Events.evtMinute1,5),
            (evtZG4Running,2),
            (Events.evtMinute1,5),
            (evtZG5Running,2),
            (Events.evtMinute1,5),
            (evtZG5Stop,2),
            (Events.evtMinute1,5),
            (evtZG4Stop,2),
            (Events.evtMinute1,5),
            (evtZG3Stop,2),
            (Events.evtMinute1,5),
            (evtZG2Stop,3),
            (Events.evtMinute1,5),
            (evtZG1Stop,3),
            (Events.evtMinute1,8),
            ]
            
        # the events that we expect to be logged.
        expect = [ evtZG1Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/1/heatsource",
            evtZG2Running,
            "zonegroup/2/heatsource",
            "zone2/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG3Running,
            "zonegroup/3/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG4Running,
            "zonegroup/4/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG5Running,
            "zonegroup/5/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG5Stop,
            "zonegroup/5/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG4Stop,
            "zonegroup/4/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG3Stop,
            "zonegroup/3/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG2Stop,
            "zonegroup/2/heatsource",
            "zone2/heatsource",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG1Stop,
            evtHS1RequestStop,
            "zonegroup/1/heatsource",
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]
            
        self.checkEvents(send, expect)

    def testZoneGroup1Zone1_a(self):
        self._log.debug( "testZoneGroup1Zone1_a" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfig1, (groupFileList,) )

        # the events we send
        send = [ 
            (evtZone1Running,4),
            (evtZone1Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ 
            evtZone1Running,
            evtZG1Run,
            "webbrick/901/DO/1",
            evtZG1Running,
            evtZone1Stop,
            evtZG1Stop,
            "webbrick/901/DO/1",
            evtZG1Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup1Zone1_b(self):
        # tests if the run and stop event for zonegroups on minute events
        # are resent, if no running and stopped events are comming back.
        self._log.debug( "testZoneGroup1Zone1_b" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfig1, (zone1FileList,) )
    
        # the events we send
        send = [ 
            (Events.evtMinute1,5),  # startup

            (Events.evtRuntime30,6),
            (Events.evtMinute1,2),
            (evtZG1Stopped,1),
            (evtZone1SetPoint18,5),
            (evtZone1Temp22,3),
            (evtZone1Temp15,6),
            (Events.evtMinute1,2),
            (evtZG1Running,1),
            (Events.evtMinute1,1),
            (evtZone1Temp22,6),
            (Events.evtMinute1,2),
            (evtZG1Stopped,1),
            (Events.evtMinute1,1),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS1DoStop,
            "zone1/stop",
            "zonegroup/1/stop",
            "zone1/stopped",
#            "zonegroup/1/stop",

            "time/runtime",
            "zone1/stop",
            "zone1/targetset",
            "zone1/state",
            "zone1/name",
            evtZone1Stopped,
#            evtZG1Stop,

            Events.evtMinute1,
            evtZG1Stop,
            evtZG1Stopped,
            
            evtZone1SetPoint18,
            "zone1/schedulesetpoint",
            ("zone1/targetset","val",18.0),
            ("zone1/state","cmdsource","Schedule"),
            "zone1/schedulesetpoint",
            
            evtZone1Temp22,
            "zone1/sensor",
            ("zone1/state","status","Idle"),
            
            evtZone1Temp15,
            "zone1/sensor",
            "zone1/run",
            ("zone1/state","status","Demand"),
            evtZone1Running,
            evtZG1Run,
            
            Events.evtMinute1,
            evtZG1Run,
            
            evtZG1Running,
            
            Events.evtMinute1,
            
            evtZone1Temp22,
            "zone1/sensor",
            "zone1/stop",
            ("zone1/state","status","Idle"),
            evtZone1Stopped,
            evtZG1Stop,
            
            Events.evtMinute1,
            evtZG1Stop,
            
            evtZG1Stopped,
            
            Events.evtMinute1,
            
            ]
        

        self.checkEvents(send, expect)    
    
    def testZoneGroup1Zone1_c(self):
        self._log.debug( "testZoneGroup1Zone1_c" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfig1, (groupFileList,) )

        # the events we send
        send = [ 
            (evtZone1Running,4),
            (evtZone1Stopped,4)
            ]
        # the events that we expect to be logged.
        expect = [ 
            evtZone1Running,
            evtZG1Run,
            "webbrick/901/DO/1",
            evtZG1Running,
            evtZone1Stopped,
            evtZG1Stop,
            "webbrick/901/DO/1",
            evtZG1Stopped
            ]

        self.checkEvents(send, expect)
    
    def testZoneGroup2Zone2(self):
        self._log.debug( "testZoneGroup2Zone2" )
        self.loadGroup()

        # the events we send
        send = [ (evtZone2Running,4),
            (evtZone2Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone2Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            evtZG2Running,
            evtZone2Stop,
            evtZG2Stop,
            "webbrick/902/DO/1",
            evtZG2Stopped
            ]

        self.checkEvents(send, expect)
        
    def testZoneGroup2Zone3(self):
        self._log.debug( "testZoneGroup2Zone3" )
        self.loadGroup()
        
        # the events we send
        send = [ (evtZone3Running,4),
            (evtZone3Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone3Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            evtZG2Running,
            evtZone3Stop,
            evtZG2Stop,
            "webbrick/902/DO/1",
            evtZG2Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup2Zone4(self):
        self._log.debug( "testZoneGroup2Zone4" )
        self.loadGroup()
        
        # the events we send
        send = [ (evtZone4Running,4),
            (evtZone4Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone4Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            evtZG2Running,
            evtZone4Stop,
            evtZG2Stop,
            "webbrick/902/DO/1",
            evtZG2Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup2Zone5(self):
        self._log.debug( "testZoneGroup2Zone5" )
        self.loadGroup()
        
        # the events we send
        send = [ (evtZone5Running,4),
            (evtZone5Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone5Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            evtZG2Running,
            evtZone5Stop,
            evtZG2Stop,
            "webbrick/902/DO/1",
            evtZG2Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup2Zone6(self):
        self._log.debug( "testZoneGroup2Zone6" )
        self.loadGroup()

        # the events we send
        send = [ (evtZone6Running,4),
            (evtZone6Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone6Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            evtZG2Running,
            evtZone6Stop,
            evtZG2Stop,
            "webbrick/902/DO/1",
            evtZG2Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup2All(self):
        self._log.debug( "testZoneGroup2All" )

        self.loadGroup()
        # the events we send
        send = [ (evtZone6Running,4),
            (evtZone5Running,1),
            (evtZone4Running,1),
            (evtZone3Running,1),
            (evtZone2Running,1),
            (evtZone6Stop,1),
            (evtZone5Stop,1),
            (evtZone4Stop,1),
            (evtZone3Stop,1),
            (evtZone2Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone6Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            evtZG2Running,
            evtZone5Running,
            evtZone4Running,
            evtZone3Running,
            evtZone2Running,
            evtZone6Stop,
            evtZone5Stop,
            evtZone4Stop,
            evtZone3Stop,
            evtZone2Stop,
            evtZG2Stop,
            "webbrick/902/DO/1",
            evtZG2Stopped
            ]

        self.checkEvents(send, expect)
        
    def testZoneGroup3Zone7(self):
        self._log.debug( "testZoneGroup3Zone7" )
        self.loadGroup()
        # the events we send

        send = [ (evtZone7Running,4),
            (evtZone7Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone7Running,
            evtZG3Run,
            "webbrick/903/DO/1",
            evtZG3Running,
            evtZone7Stop,
            evtZG3Stop,
            "webbrick/903/DO/1",
            evtZG3Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup3Zone8(self):
        self._log.debug( "testZoneGroup3Zone8" )
        self.loadGroup()

        send = [ (evtZone8Running,4),
            (evtZone8Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone8Running,
            evtZG3Run,
            "webbrick/903/DO/1",
            evtZG3Running,
            evtZone8Stop,
            evtZG3Stop,
            "webbrick/903/DO/1",
            evtZG3Stopped
            ]

        self.checkEvents(send, expect)
        
    def testZoneGroup3Zone9(self):
        self._log.debug( "testZoneGroup3Zone9" )
        self.loadGroup()

        send = [ (evtZone9Running,4),
            (evtZone9Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone9Running,
            evtZG3Run,
            "webbrick/903/DO/1",
            evtZG3Running,
            evtZone9Stop,
            evtZG3Stop,
            "webbrick/903/DO/1",
            evtZG3Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup3Zone10(self):
        self._log.debug( "testZoneGroup3Zone10" )
        self.loadGroup()

        send = [ (evtZone10Running,4),
            (evtZone10Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone10Running,
            evtZG3Run,
            "webbrick/903/DO/1",
            evtZG3Running,
            evtZone10Stop,
            evtZG3Stop,
            "webbrick/903/DO/1",
            evtZG3Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup3Zone11(self):
        self._log.debug( "testZoneGroup3Zone11" )
        self.loadGroup()

        send = [ (evtZone11Running,4),
            (evtZone11Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone11Running,
            evtZG3Run,
            "webbrick/903/DO/1",
            evtZG3Running,
            evtZone11Stop,
            evtZG3Stop,
            "webbrick/903/DO/1",
            evtZG3Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup3All(self):
        self._log.debug( "testZoneGroup3All" )
        self.loadGroup()

        send = [ (evtZone7Running,4),
            (evtZone8Running,1),
            (evtZone9Running,1),
            (evtZone10Running,1),
            (evtZone11Running,1),
            (evtZone11Stop,1),
            (evtZone10Stop,1),
            (evtZone9Stop,1),
            (evtZone8Stop,1),
            (evtZone7Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone7Running,
            evtZG3Run,
            "webbrick/903/DO/1",
            evtZG3Running,
            evtZone8Running,
            evtZone9Running,
            evtZone10Running,
            evtZone11Running,
            evtZone11Stop,
            evtZone10Stop,
            evtZone9Stop,
            evtZone8Stop,
            evtZone7Stop,
            evtZG3Stop,
            "webbrick/903/DO/1",
            evtZG3Stopped
            ]

        self.checkEvents(send, expect)
        
    def testZoneGroup4Zone12(self):
        self._log.debug( "testZoneGroup4Zone12" )
        self.loadGroup()

        send = [ (evtZone12Running,4),
            (evtZone12Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone12Running,
            evtZG4Run,
            "webbrick/904/DO/1",
            evtZG4Running,
            evtZone12Stop,
            evtZG4Stop,
            "webbrick/904/DO/1",
            evtZG4Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup4Zone13(self):
        self._log.debug( "testZoneGroup4Zone13" )
        self.loadGroup()
        
        send = [ (evtZone13Running,4),
            (evtZone13Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone13Running,
            evtZG4Run,
            "webbrick/904/DO/1",
            evtZG4Running,
            evtZone13Stop,
            evtZG4Stop,
            "webbrick/904/DO/1",
            evtZG4Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup4Zone14(self):
        self._log.debug( "testZoneGroup4Zone14" )
        self.loadGroup()
        
        send = [ (evtZone14Running,4),
            (evtZone14Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone14Running,
            evtZG4Run,
            "webbrick/904/DO/1",
            evtZG4Running,
            evtZone14Stop,
            evtZG4Stop,
            "webbrick/904/DO/1",
            evtZG4Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup4All(self):
        self._log.debug( "testZoneGroup4All" )
        self.loadGroup()

        send = [ (evtZone12Running,4),
            (evtZone13Running,1),
            (evtZone14Running,1),
            (evtZone14Stop,1),
            (evtZone13Stop,1),
            (evtZone12Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone12Running,
            evtZG4Run,
            "webbrick/904/DO/1",
            evtZG4Running,
            evtZone13Running,
            evtZone14Running,
            evtZone14Stop,
            evtZone13Stop,
            evtZone12Stop,
            evtZG4Stop,
            "webbrick/904/DO/1",
            evtZG4Stopped
            ]

    def testZoneGroup5Zone15(self):
        self._log.debug( "testZoneGroup5Zone15" )
        self.loadGroup()
        
        send = [ (evtZone15Running,4),
            (evtZone15Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone15Running,
            evtZG5Run,
            "webbrick/905/DO/1",
            evtZG5Running,
            evtZone15Stop,
            evtZG5Stop,
            "webbrick/905/DO/1",
            evtZG5Stopped
            ]

        self.checkEvents(send, expect)
        
    def testZoneGroup5Zone16(self):
        self._log.debug( "testZoneGroup5Zone16" )
        self.loadGroup()
        
        send = [ (evtZone16Running,4),
            (evtZone16Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone16Running,
            evtZG5Run,
            "webbrick/905/DO/1",
            evtZG5Running,
            evtZone16Stop,
            evtZG5Stop,
            "webbrick/905/DO/1",
            evtZG5Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup5All(self):
        self._log.debug( "testZoneGroup5All" )
        self.loadGroup()

        send = [ (evtZone15Running,4),
            (evtZone16Running,1),
            (evtZone16Stop,1),
            (evtZone15Stop,4)
            ]
        # the events that we expect to be logged.
        expect = [ evtZone15Running,
            evtZG5Run,
            "webbrick/905/DO/1",
            evtZG5Running,
            evtZone16Running,
            evtZone16Stop,
            evtZone15Stop,
            evtZG5Stop,
            "webbrick/905/DO/1",
            evtZG5Stopped
            ]

        self.checkEvents(send, expect)

    def testZoneGroup1AndMasterSingle(self):
        self._log.debug( "testZoneGroup1AndMasterSingle" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfig1, (masterSingleFileList, groupFileList, heatSource1FileList) )
        
        send = [ (evtZone1Running,8),
            (Events.evtMinute1,7),
            (evtZone1Stop,7),
            (Events.evtMinute1,8),
            ]

        # the events that we expect to be logged.
# TODO The zonegroup template propogates changes to heat source to all zones, suppress when inactive
        expect = [ evtZone1Running,
            evtZG1Run,
            "webbrick/901/DO/1",
            evtZG1Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/1/heatsource",
            "zone1/heatsource",

            evtZone1Stop,
            evtZG1Stop,
            evtHS1RequestStop,
            "zonegroup/1/heatsource",
            "webbrick/901/DO/1",
            "zone1/heatsource",
            evtZG1Stopped,
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped,
            ]

        self.checkEvents(send, expect)

    def testZoneGroup2AndMasterSingle(self):
        self._log.debug( "testZoneGroup2AndMasterSingle" )
        self.loadMasterAndGroups()
        
        send = [ (evtZone2Running,8),
            (Events.evtMinute1,11),
            (evtZone2Stop,11),
            (Events.evtMinute1,8),
            ]
# TODO The zonegroup template propogates changes to heat source to all zones, suppress when inactive
        # the events that we expect to be logged.
        expect = [ evtZone2Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            evtZG2Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/2/heatsource",
         
            "zone3/heatsource",
            "zone2/heatsource",
            "zone6/heatsource",
            "zone5/heatsource",
            "zone4/heatsource",
            
            

            evtZone2Stop,
            evtZG2Stop,
            evtHS1RequestStop,
            "zonegroup/2/heatsource",
            "webbrick/902/DO/1",
            "zone3/heatsource",
            "zone2/heatsource",
            "zone6/heatsource",
            "zone5/heatsource",
            "zone4/heatsource",
            evtZG2Stopped,
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped,
            ]
            
        self.checkEvents(send, expect)

# TODO The zonegroup template propogates changes to heat source to all zones, suppress when inactive
    def testZoneGroup3AndMasterSingle(self):
        self._log.debug( "testZoneGroup3AndMasterSingle" )
        self.loadMasterAndGroups()
        
        send = [ (evtZone7Running,8),
            (Events.evtMinute1,11),
            (evtZone7Stop,11),
            (Events.evtMinute1,8),
            ]

        expect = [ evtZone7Running,
            evtZG3Run,
            "webbrick/903/DO/1",
            evtZG3Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/3/heatsource", 
            "zone11/heatsource",
            "zone10/heatsource",
            "zone7/heatsource",
            "zone9/heatsource",  
            "zone8/heatsource",

            evtZone7Stop,
            evtZG3Stop,
            evtHS1RequestStop,
            "zonegroup/3/heatsource",
            "webbrick/903/DO/1",
            "zone11/heatsource",
            "zone10/heatsource",
            "zone7/heatsource",
            "zone9/heatsource",  
            "zone8/heatsource",
            evtZG3Stopped,
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped,
            ]

        self.checkEvents(send, expect)
        
# TODO The zonegroup template propogates changes to heat source to all zones, suppress when inactive
    def testZoneGroup4AndMasterSingle(self):
        self._log.debug( "testZoneGroup4AndMasterSingle" )
        self.loadMasterAndGroups()
        
        send = [ (evtZone12Running,8),
            (Events.evtMinute1,9),
            (evtZone12Stop,9),
            (Events.evtMinute1,8),
            ]

        expect = [ evtZone12Running,
            evtZG4Run,
            "webbrick/904/DO/1",
            evtZG4Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/4/heatsource",
            "zone13/heatsource",
            "zone12/heatsource",
            "zone14/heatsource",

            evtZone12Stop,
            evtZG4Stop,
            evtHS1RequestStop,
            "zonegroup/4/heatsource",
            "webbrick/904/DO/1",
            "zone13/heatsource",
            "zone12/heatsource",
            "zone14/heatsource",
            evtZG4Stopped,
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped,
            ]

        self.checkEvents(send, expect)

# TODO The zonegroup template propogates changes to heat source to all zones, suppress when inactive
    def testZoneGroup5AndMasterSingle(self):
        self._log.debug( "testZoneGroup5AndMasterSingle" )
        self.loadMasterAndGroups()
        
        send = [ (evtZone15Running,8),
            (Events.evtMinute1,8),
            (evtZone15Stop,8),
            (Events.evtMinute1,8),
            ]

        expect = [ evtZone15Running,
            evtZG5Run,
            "webbrick/905/DO/1",
            evtZG5Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Running,
            "zonegroup/5/heatsource",
            "zone16/heatsource",
            "zone15/heatsource",

            evtZone15Stop,
            evtZG5Stop,
            evtHS1RequestStop,
            "zonegroup/5/heatsource",
            "webbrick/905/DO/1",
            "zone16/heatsource",
            "zone15/heatsource",
            evtZG5Stopped,
            
            Events.evtMinute1,
            evtHS1DoStop,
            "zone/check",
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped,
            ]

        self.checkEvents(send, expect)

    def testWeather1(self):
        self._log.debug( "testWeather1" )
        self.loadWeather()
        
        # weather compensation has 3 sets of data, There is also a default set that always presents Run
        # for each set of data
        # if current temp is rising and current temp > rise-threshold hold off
        # if current temp is falling and current temp > fall-threshold hold off
        # else Run.

        # the events we send
        send = [ 
            (Events.evtMinute1,4),  # startup
            (Events.evtRuntime10,8),
            (evtTemp22,2),
            (Events.evtMinute10,3),
            (evtZone2Stopped,1),
            (evtZG1Stopped,1),
            (evtTemp15,2),
            (Events.evtMinute10,8),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS1DoStop,
            "zone2/stop",
            evtZG1Stop,

            Events.evtRuntime10,
            "weather/0",
            "weather/1",
            "weather/2",
            "weather/3",
            "zone2/state",
            "zone2/state",
            "zone2/state",
            ("webbrick/5/CT/1","val",22.0),
            "weather/outsideTemp",
            Events.evtMinute10,
            evtZone2Stop,
            evtZG1Stop,
            evtZone2Stopped,
            evtZG1Stopped,
            
            ("webbrick/5/CT/1","val",15.0),
            "weather/outsideTemp",
            Events.evtMinute10,
            "weather/global",
            ("weather/1","state", "HoldOff"),
            ("weather/2","state", "Run"),
            ("weather/3","state", "Run"),
            
            
            "zone2/state",
            "zone2/state",
            "zone2/state",
            ]

        self.checkEvents(send, expect)
        
    def testWeather2(self):
        self._log.debug( "testWeather2" )
        self.loadWeather()
        
        # weather compensation has 3 sets of data, There is also a default set that always presents Run
        # for each set of data
        # if current temp is rising and current temp > threshold hold off
        # if current temp is falling and current temp > fall-threshold hold off
        # else Run.

        send = [ 
            (Events.evtMinute1,4),  # startup
            (Events.evtRuntime10,8),
            (evtTemp15,2),
            (Events.evtMinute10,3),
            (evtZone2Stopped,1),
            (evtZG1Stopped,1),
            (evtTemp22,2),
            (Events.evtMinute10,8),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS1DoStop,
            "zone2/stop",
            evtZG1Stop,

            Events.evtRuntime10,
            "weather/0",
            "weather/1",
            "weather/2",
            "weather/3",
            "zone2/state",
            "zone2/state",
            "zone2/state",
            ("webbrick/5/CT/1","val",15.0),
            "weather/outsideTemp",
            Events.evtMinute10,
            evtZone2Stop,
            evtZG1Stop,
            evtZone2Stopped,
            evtZG1Stopped,
            
            ("webbrick/5/CT/1","val",22.0),
            "weather/outsideTemp",
            Events.evtMinute10,
            "weather/global",
            ("weather/1","state", "HoldOff"),
            ("weather/2","state", "Run"),
            ("weather/3","state", "HoldOff"),
            
            
            "zone2/state",
            "zone2/state",
            "zone2/state",
            ]

        self.checkEvents(send, expect)

    def testZone_2_start(self):
        # test multiple minutes
        self._log.debug( "testZone_2_start" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        send = [ 
            (Events.evtRuntime30,6),
            ]
        # the events that we expect to be logged.
        # setpoint has defaulted to mintemp we see run/state/running twice.
        expect = [             
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            ]

        self.checkEvents(send, expect)

    def testZone_2a(self):
        # no setpoint given - test minpoint works.
        self._log.debug( "testZone_2a" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature

        send = [ 
            (Events.evtRuntime30,6),
            (evtZone2Temp15,3),
            (evtZone2Temp4,5),
            (evtZone2Temp15,5),
            ]
        # the events that we expect to be logged.
        # TODO as setpoint has defaulted to mintemp we see run/state/running twice.
        expect = [             
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            ("webbrick/2/CT/0","val",15.0),
            "zone2/sensor",
            ("zone2/state","cmdsource","Frost"),
            ("webbrick/2/CT/0","val",4.0),
            "zone2/sensor",
            "zone2/run",
            ("zone2/state","cmdsource","Frost"),
            "zone2/running",
            ("webbrick/2/CT/0","val",15.0),
            "zone2/sensor",
            "zone2/stop",
            ("zone2/state","cmdsource","Frost"),
            "zone2/stopped",
            ]

        self.checkEvents(send, expect)

    def testZone_2b(self):
        # test just set point change
        self._log.debug( "testZone_2b" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature
        # scheduled setpoint changes

        send = [ (Events.evtRuntime30,6), 
            (evtZone2SetPoint14,5),
            (evtZone2Temp15,3),
            (evtZone2SetPoint18,7),
            (evtZone2SetPoint14,7),
            ]
        # the events that we expect to be logged.
        expect = [
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            evtZone2SetPoint14,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",14.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
            evtZone2Temp15,
            "zone2/sensor",
            ("zone2/state","status","Idle"),
            evtZone2SetPoint18,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",18.0),
            "zone2/run",
            ("zone2/state","status","Demand"),
            "zone2/schedulesetpoint",
            "zone2/running",
            evtZone2SetPoint14,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",14.0),
            "zone2/stop",
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
            "zone2/stopped",
            ]

        self.checkEvents(send, expect)
        
    def testZone_2c(self):
        # test temperature change
        self._log.debug( "testZone_2c" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature
        # scheduled setpoint changes

        send = [ 
            (Events.evtRuntime30,6),
            (evtZone2SetPoint18,5),
            (evtZone2Temp22,3),
            (evtZone2Temp15,5),
            (evtZone2Temp22,5),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            evtZone2SetPoint18,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",18.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
            evtZone2Temp22,
            "zone2/sensor",
            ("zone2/state","status","Idle"),
            evtZone2Temp15,
            "zone2/sensor",
            "zone2/run",
            ("zone2/state","status","Demand"),
            "zone2/running",
            evtZone2Temp22,
            "zone2/sensor",
            "zone2/stop",
            ("zone2/state","status","Idle"),
            "zone2/stopped",
            ]

        self.checkEvents(send, expect)

    def testZone_2d(self):
        # test temperature change to below min
        # and back up again.
        self._log.debug( "testZone_2d" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature
        # scheduled setpoint changes
        send = [ 
            (Events.evtRuntime30,6),
            (evtZone2SetPoint14,5),
            (evtZone2SetPoint0,5),
            (evtZone2Temp22,3),
            (evtZone2Temp4,5),
            (evtZone2Temp22,5),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            evtZone2SetPoint14,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",14.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
            evtZone2SetPoint0,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",5.2),
            ("zone2/state","cmdsource","Frost"),    # as setpoint below frost
            "zone2/schedulesetpoint",
            evtZone2Temp22,
            "zone2/sensor",
            ("zone2/state","status","Idle"),
            evtZone2Temp4,
            "zone2/sensor",
            "zone2/run",
            ("zone2/state","status","Demand"),
            "zone2/running",
            evtZone2Temp22,
            "zone2/sensor",
            "zone2/stop",
            ("zone2/state","status","Idle"),
            "zone2/stopped",
            ]

        self.checkEvents(send, expect)

    
    def testZone_2e(self):
        # tests if the resending of the run and stop event is working on minute events
        # if no running and stopped events are comming back.
        self._log.debug( "testZone_2e" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileListInputOnly,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature
        # scheduled setpoint changes

        send = [ 
            (Events.evtMinute1,4),  # startup
            (evtZone2Stopped, 1),
            (evtZG1Stopped, 1),
            (evtHS1Stopped, 1),

            (Events.evtRuntime30,5),
            (evtZone2SetPoint18,5),
            (evtZone2Temp22,3),
            (evtZone2Temp15,4),
            (Events.evtMinute1,2),
            (evtZone2Running, 1),
            (Events.evtMinute1,1),
            (evtZone2Temp22,4),
            (Events.evtMinute1,2),
            (evtZone2Stopped, 1),
            (Events.evtMinute1,1),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS1DoStop,
            "zone2/stop",
            evtZG1Stop,

            evtZone2Stopped,
            evtZG1Stopped,
            evtHS1Stopped,

            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            

            evtZone2SetPoint18,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",18.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",

            evtZone2Temp22,
            "zone2/sensor",
            ("zone2/state","status","Idle"),

            evtZone2Temp15,
            "zone2/sensor",
            "zone2/run",
            ("zone2/state","status","Demand"),

            Events.evtMinute1,
            evtZone2Run,
            
            evtZone2Running,
            
            Events.evtMinute1,
            
            evtZone2Temp22,
            "zone2/sensor",
            "zone2/stop",
            ("zone2/state","status","Idle"),
            
            Events.evtMinute1,
            evtZone2Stop,
            
            evtZone2Stopped,
            
            Events.evtMinute1,
            
            ]

        self.checkEvents(send, expect)
        

    def testZone_2f(self):
        # test hysteriesis
        self._log.debug( "testZone_2f" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature
        # scheduled setpoint changes

        send = [ (Events.evtRuntime30,6), 
            (evtZone2SetPoint14,5),
            (evtZone2Temp15,3),
            (evtZone2Temp14,3),
            (evtZone2Temp13,5),
            (evtZone2Temp14,3),
            (evtZone2Temp15,5),
            ]
        # the events that we expect to be logged.
        expect = [
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
#6
            evtZone2SetPoint14,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",14.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
#11
            evtZone2Temp15,
            "zone2/sensor",
            ("zone2/state","status","Idle"),
#14
            evtZone2Temp14,
            "zone2/sensor",
            ("zone2/state","status","Idle"),
#17
            evtZone2Temp13,
            "zone2/sensor",
            "zone2/run",
            ("zone2/state","status","Demand"),
            "zone2/running",
#22
            evtZone2Temp14,
            "zone2/sensor",
            ("zone2/state","status","Demand"),
#25
            evtZone2Temp15,
            "zone2/sensor",
            "zone2/stop",
            ("zone2/state","status","Idle"),
            "zone2/stopped",
            ]

        self.checkEvents(send, expect)
        
    
    def testZone_2g(self):
        # test setpoint behaviour when zone enable is changed
        self._log.debug( "testZone_2g" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature
        # scheduled & manual setpoint changes
        send = [ 
            (Events.evtRuntime30,6),
            (evtZone2SetPoint14,5),
            (evtZone2Disable,3),
            (evtZone2SetPoint18,4),
            (evtZone2Enable,3),
            (evtZone2ManSetPoint14,3),
            (evtZone2Disable,3),
            (evtZone2ManSetPoint18,2),
            (evtZone2Enable,3),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            
            evtZone2SetPoint14,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",14.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
            
            evtZone2Disable,
            ("zone2/targetset","val",5.2),
            ("zone2/state","cmdsource","Frost"),    # as disabled
            
            evtZone2SetPoint18,
            "zone2/schedulesetpoint",
            ("zone2/state","schedulesetpoint",18.0),
            "zone2/schedulesetpoint",

            evtZone2Enable,
            ("zone2/targetset","val",18.0),
            ("zone2/state","cmdsource","Schedule"),
            
            evtZone2ManSetPoint14,
            ("zone2/targetset","val",14.0),
            ("zone2/state","cmdsource","Manual"),
            
            evtZone2Disable,
            ("zone2/targetset","val",5.2),
            ("zone2/state","cmdsource","Frost"),
            
            evtZone2ManSetPoint18,
            ("zone2/state","manualsetpoint",18.0),
            
            evtZone2Enable,
            ("zone2/targetset","val",18.0),
            ("zone2/state","cmdsource","Manual"),
            ]

        self.checkEvents(send, expect)
        
    def testZone_2h(self):
        # test setpoint behaviour when zone enable is changed
        self._log.debug( "testZone_2h" )
        self.loadPrimitive( "PersistZone2", TestHeatingVentilationACConfig2, (zone2FileList,) )   # a tuple or a list is required

        # zone 2 enabled,no weather, no occupancy.

        # other inputs are 
        # zone2/sensor - current temperature
        # scheduled & manual setpoint changes
        send = [ 
            (Events.evtRuntime30,6),
            (evtZone2SetPoint14,5),
            (evtZone2FrostStat9,2),
            (evtZone2FrostStat16,3),
            (evtZone2SetPoint18,5),
            (evtZone2Disable,3),
            (evtZone2FrostStat5,3),
            (evtZone2Enable,3),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            
            evtZone2SetPoint14,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",14.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
            
            evtZone2FrostStat9,
            ("zone2/state","minzonetemp", 9.0),
            
            evtZone2FrostStat16,
            ("zone2/targetset","val",16.0),
            ("zone2/state","minzonetemp", 16.0),
            
             evtZone2SetPoint18,
            "zone2/schedulesetpoint",
            ("zone2/targetset","val",18.0),
            ("zone2/state","cmdsource","Schedule"),
            "zone2/schedulesetpoint",
            
            evtZone2Disable,
            ("zone2/targetset","val",16.0),
            ("zone2/state","cmdsource","Frost"),    # as disabled
            
            evtZone2FrostStat5,
            ("zone2/targetset","val",5.0),
            ("zone2/state","minzonetemp", 5.0),
            
            evtZone2Enable,
            ("zone2/targetset","val",18.0),
            ("zone2/state","cmdsource","Schedule"),
            
            ]

        self.checkEvents(send, expect)


    
    def testZone_3_start(self):
        # no setpoint given - test minpoint works.
        self._log.debug( "testZone_3_start" )
        self.loadPrimitive( "PersistZone3", TestHeatingVentilationACConfig3, (zone3FileList,) )   # a tuple or a list is required

        # zone 3 enabled, no weather, follow occupancy

        # other inputs are 
        # zone3/sensor - current temperature

        send = [
            (Events.evtRuntime30,6),
            (evtOccupied,2),
            ]
            
        # the events that we expect to be logged.
        # TODO as setpoint has defaulted to mintemp we see run/state/running twice.
        expect = [
            "time/runtime",
            "zone3/stop",
            "zone3/targetset",
            "zone3/state",
            "zone3/name",
            "zone3/stopped",
            "occupants/home",
            "zone3/state",
            ]
        
        self.checkEvents(send, expect)
        TestEventLogger.logEvents()
        
    def testZone_3a(self):
        self._log.debug( "testZone_3a" )
        self.loadPrimitive( "PersistZone3", TestHeatingVentilationACConfig3, (zone3FileList,) )   # a tuple or a list is required

        # zone 3 enabled, no weather, follow occupancy

        # This one we start unoccupied and then go occupied 
        send = [ 
            (Events.evtRuntime30,6),
            (evtZone3SetPoint14,5),
            (evtUnOccupied,3),
            (evtZone3Temp15,3),
            (evtZone3SetPoint18,4),
            (evtOccupied,5),
            (evtZone3SetPoint14,7),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone3/stop",
            "zone3/targetset",
            "zone3/state",
            "zone3/name",
            "zone3/stopped",
            evtZone3SetPoint14,
            "zone3/schedulesetpoint",
            ("zone3/targetset","val",14.0),
            ("zone3/state","cmdsource","Schedule"),
            "zone3/schedulesetpoint",
            evtUnOccupied,
            ("zone3/targetset","val",10.0),
            ("zone3/state","cmdsource","Frost"),
            evtZone3Temp15,
            "zone3/sensor",
            ("zone3/state","status","Idle"),
            evtZone3SetPoint18,
            "zone3/schedulesetpoint",
            ("zone3/state","cmdsource","Frost"),
            "zone3/schedulesetpoint",
            evtOccupied,
            ("zone3/targetset","val",18.0),
            "zone3/run",
            ("zone3/state","cmdsource","Schedule"),
            "zone3/running",
            evtZone3SetPoint14,
            "zone3/schedulesetpoint",
            ("zone3/targetset","val",14.0),
            "zone3/stop",
            ("zone3/state","status","Idle"),
            "zone3/schedulesetpoint",
            "zone3/stopped",
            ]

        self.checkEvents(send, expect)

    def testZone_3b(self):
        self._log.debug( "testZone_3b" )
        self.loadPrimitive( "PersistZone3", TestHeatingVentilationACConfig3, (zone3FileList,) )   # a tuple or a list is required

        # zone 3 enabled, no weather, follow occupancy
        
        # This one we start occupied and then go unoccupied 
        send = [ 
            (Events.evtRuntime30,6),
            (evtZone3SetPoint14,5),
            (evtOccupied,2),
            (evtZone3Temp15,3),
            (evtZone3SetPoint18,7),
            (evtUnOccupied,5),
            (evtZone3SetPoint14,4),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone3/stop",
            "zone3/targetset",
            "zone3/state",
            "zone3/name",
            "zone3/stopped",
            evtZone3SetPoint14,
            "zone3/schedulesetpoint",
            ("zone3/targetset","val",14.0),
            ("zone3/state","cmdsource","Schedule"),
            "zone3/schedulesetpoint",
            evtOccupied,
            ("zone3/state","cmdsource","Schedule"),
            evtZone3Temp15,
            "zone3/sensor",
            ("zone3/state","cmdsource","Schedule"),
            evtZone3SetPoint18,
            "zone3/schedulesetpoint",
            ("zone3/targetset","val",18.0),
            "zone3/run",
            ("zone3/state","cmdsource","Schedule"),
            "zone3/schedulesetpoint",
            "zone3/running",
            evtUnOccupied,
            ("zone3/targetset","val",10.0),
            "zone3/stop",
            ("zone3/state","cmdsource","Frost"),
            "zone3/stopped",
            evtZone3SetPoint14,
            "zone3/schedulesetpoint",
            ("zone3/state","cmdsource","Frost"),
            "zone3/schedulesetpoint",
            ]

        self.checkEvents(send, expect)

    def testZone_4_start(self):
        # zone 4 enabled, weather, no occupancy
        # no setpoint given - test minpoint works.
        self._log.debug( "testZone_4_start" )
        self.loadZone4()

        # zone is configured with:
        # enabled
        # no weather compensation
        # matstat (froststat) at 10 degrees
        # to follow occupancy

        # other inputs are 
        # zone3/sensor - current temperature

        send = [ 
            (Events.evtRuntime30,6),
            (evtOccupied,2),
            ]
            
        # the events that we expect to be logged.
        # TODO as setpoint has defaulted to mintemp we see run/state/running twice.
        expect = [
            "time/runtime",
            "zone4/stop",
            "zone4/targetset",
            "zone4/state",
            "zone4/name",
            "zone4/stopped",
            "occupants/home",
            "zone4/state",
            ]
        
        self.checkEvents(send, expect)
        TestEventLogger.logEvents()

    def testZone_4a(self):
        # zone 4 enabled, weather, no occupancy
        # test set point change
        self._log.debug( "testZone_4a" )
        self.loadZone4()

        send = [
            (Events.evtRuntime30,6),
            (evtZone4SetPoint14,5),
            (evtZone4Temp15,3),
            (evtZone4SetPoint18,7),
            (evtZone4SetPoint14,7),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone4/stop",
            "zone4/targetset",
            "zone4/state",
            "zone4/name",
            "zone4/stopped",
            evtZone4SetPoint14,
            "zone4/schedulesetpoint",
            ("zone4/targetset","val",14.0),
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",
            evtZone4Temp15,
            "zone4/sensor",
            ("zone4/state","cmdsource","Schedule"),
            evtZone4SetPoint18,
            "zone4/schedulesetpoint",
            ("zone4/targetset","val",18.0),
            "zone4/run",
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",
            "zone4/running",
            evtZone4SetPoint14,
            "zone4/schedulesetpoint",
            ("zone4/targetset","val",14.0),
            "zone4/stop",
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",
            "zone4/stopped",
            ]

        self.checkEvents(send, expect)

    def testZone_4b(self):
        # zone 4 enabled, weather, no occupancy
        # test set point change
        # This test sees what happens when Hold Off on up change of set point
        self._log.debug( "testZone_4b" )
        self.loadZone4()

        # first put zone in hold off state
        send = [ 
            (Events.evtRuntime30,6),
            (Events.evtRuntime10,8),
            (Events.evtMinute1,2),
            (evtZG1Stopped,1),

            (evtZone4SetPoint14,5),
            (evtTemp22,2),
            (Events.evtMinute10,1),
            (evtTemp15,2),
            (Events.evtMinute10,7),
            (evtZone4Temp15,3),
            (evtZone4SetPoint18,4),

            (evtTemp5,2),
            (Events.evtMinute10,12),

            (evtZone4SetPoint14,7),
            ]

        # the events that we expect to be logged.
        expect = [ 
#0
            "time/runtime",
            "zone4/stop",
            "zone4/targetset",
            "zone4/state",
            "zone4/name",
            "zone4/stopped",
#5
            Events.evtRuntime10,
            "weather/0",
            "weather/1",
            "weather/2",
            "weather/3",
            ("zone4/state","cmdsource","Frost"),
            ("zone4/state","cmdsource","Frost"),
            ("zone4/state","cmdsource","Frost"),
#13
            Events.evtMinute1,
            evtZG1Stop,
            evtZG1Stopped,

            evtZone4SetPoint14,
            "zone4/schedulesetpoint",
            ("zone4/targetset","val",14.0),
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",

            ("webbrick/5/CT/1","val",22.0),
            "weather/outsideTemp",

            Events.evtMinute10,

            ("webbrick/5/CT/1","val",15.0),
            "weather/outsideTemp",

            Events.evtMinute10,
            "weather/global",
            ("weather/1","state", "HoldOff"),
            ("weather/2","state", "Run"),
            ("weather/3","state", "Run"),
            
            
            ("zone4/state","cmdsource","Schedule"), 
            ("zone4/state","cmdsource","Schedule"), #necessary, because weather 2 and 3 could potentially have changed and a change cannot easily be detected within zone
            ("zone4/state","cmdsource","Schedule"), #necessary, because weather 2 and 3 could potentially have changed and a change cannot easily be detected within zone
#33
            evtZone4Temp15,
            "zone4/sensor",
            ("zone4/state","cmdsource","Schedule"),
#36
            evtZone4SetPoint18,
            "zone4/schedulesetpoint",
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",
#40
            ("webbrick/5/CT/1","val",5.0),
            "weather/outsideTemp",
#42
            Events.evtMinute10,
            "weather/global",
            ("weather/1","state", "Run"),
            ("weather/2","state", "Run"),
            ("weather/3","state", "Run"),
            
            
            ("zone4/targetset","val",18.0),
            "zone4/run",
            ("zone4/state","cmdsource","Schedule"),
            ("zone4/state","cmdsource","Schedule"),  
            ("zone4/state","cmdsource","Schedule"),
            "zone4/running",
#52
            evtZone4SetPoint14,
            "zone4/schedulesetpoint",
            ("zone4/targetset","val",14.0),
            "zone4/stop",
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",
            "zone4/stopped",
            ]

        self.checkEvents(send, expect)

    def testZone_4c(self):
        # zone 4 enabled, weather, no occupancy
        # test set point change
        # This test sees what happens when Hold Off on down change of set point
        self._log.debug( "testZone_4c" )
        self.loadZone4()

        # first put zone in hold off state
        send = [ 
            (Events.evtRuntime30,6),
            (Events.evtRuntime10,8),
            (Events.evtMinute1,2),
            (evtZG1Stopped,1),

            (evtZone4SetPoint18,5),

            (evtTemp22,2),
            (Events.evtMinute10,1),
            (evtTemp15,2),
            (Events.evtMinute10,8),
            (evtZone4Temp15,3),
            (evtZone4SetPoint14,5),

            ]

        # the events that we expect to be logged.
        expect = [ 
#0       
            "time/runtime",
            "zone4/stop",
            "zone4/targetset",
            "zone4/state",
            "zone4/name",
            "zone4/stopped",
#5
            Events.evtRuntime10,
            "weather/0",
            "weather/1",
            "weather/2",
            "weather/3",
            ("zone4/state","cmdsource","Frost"),
            ("zone4/state","cmdsource","Frost"),
            ("zone4/state","cmdsource","Frost"),

            Events.evtMinute1,
            evtZG1Stop,
            evtZG1Stopped,
#13
            evtZone4SetPoint18,
            "zone4/schedulesetpoint",
            ("zone4/targetset","val",18.0),
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",
#13
            ("webbrick/5/CT/1","val",22.0),
            "weather/outsideTemp",
            Events.evtMinute10,
            
            ("webbrick/5/CT/1","val",15.0),
            "weather/outsideTemp",
#19
            Events.evtMinute10,
            "weather/global",
            ("weather/1","state", "HoldOff"),
            ("weather/2","state", "Run"),
            ("weather/3","state", "Run"),
            
            
            ("zone4/state","cmdsource","Schedule"),
            ("zone4/state","cmdsource","Schedule"),
            ("zone4/state","cmdsource","Schedule"),
#27
            evtZone4Temp15,
            "zone4/sensor",
            ("zone4/state","cmdsource","Schedule"),
#30
            evtZone4SetPoint14,
            "zone4/schedulesetpoint",
            ("zone4/targetset","val",14.0),
            ("zone4/state","cmdsource","Schedule"),
            "zone4/schedulesetpoint",
            ]

        self.checkEvents(send, expect)

    def testZone_5_start(self):
        # zone 5 enabled, weather, follow occupancy
        # no setpoint given - test minpoint works.
        self._log.debug( "testZone_5_start" )
        self.loadZone5()

        # other inputs are 
        # zone5/sensor - current temperature

        send = [ 
            (Events.evtRuntime30,6),
            (evtOccupied,2),
#            (evtZone5Temp15,2),
#            (Events.evtMinute1,1),
#            (Events.evtMinute1,1),
#            (Events.evtMinute1,1),
            ]
            
        # the events that we expect to be logged.
        # TODO as setpoint has defaulted to mintemp we see run/state/running twice.
        expect = [
            "time/runtime",
            "zone5/stop",
            "zone5/targetset",
            "zone5/state",
            "zone5/name",
            "zone5/stopped",
            "occupants/home",
            "zone5/state",
            ]
        
        self.checkEvents(send, expect)
        TestEventLogger.logEvents()

    def testZone_5a(self):
        # zone 5 enabled, weather, follow occupancy
        # test set point change
        self._log.debug( "testZone_5a" )
        self.loadZone5()

        send = [ 
            (Events.evtRuntime30,6),
            (evtZone5SetPoint14,5),
            (evtZone5Temp15,3),
            (evtZone5ManualSetPoint22,5),
            (evtZone5SetPoint14,5),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone5/stop",
            "zone5/targetset",
            "zone5/state",
            "zone5/name",
            "zone5/stopped",
            evtZone5SetPoint14,
            "zone5/schedulesetpoint",
            ("zone5/targetset","val",14.0),
            ("zone5/state","cmdsource","Schedule"),
            "zone5/schedulesetpoint",
            evtZone5Temp15,
            "zone5/sensor",
            ("zone5/state","cmdsource","Schedule"),
            
            evtZone5ManualSetPoint22,
            ("zone5/targetset","val",22.0),
            "zone5/run",
            ("zone5/state","cmdsource","Manual"),
            "zone5/running",
            evtZone5SetPoint14,
            ("zone5/targetset","val",14.0),
            "zone5/stop",
            ("zone5/state","cmdsource","Schedule"),
            "zone5/stopped",
            ]

        self.checkEvents(send, expect)

    
    def testMultiZone_1(self):
        # zone 5 enabled, weather, follow occupancy
        # test set point change
        self._log.debug( "testMultiZone_1" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigMultiZone, (zone1FileList, zone2FileList) )

        send = [ 
            (Events.evtRuntime30,11),
            ]
        # the events that we expect to be logged.
        expect = [ 
            "time/runtime",
            "zone1/stop",
            "zone1/targetset",
            "zone1/state",
            "zone1/name",
            "zone1/stopped",
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone2/stopped",
            
            ]

        self.checkEvents(send, expect)
        
        
    def testHeatSourceSolarSingle(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceSolarSingle" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSource4, (heatSource4FileList,) )

        # the events we send
        send = [ 
            (Events.evtRuntime20,2),
            (evtHS4PanelTemp5,2),
            (evtHS4HeatExTemp5,3),
            (evtHS4PanelTemp25,3),
            (evtHS4PanelTemp95,3),
            (evtHS4RequestRun,1),
            (Events.evtMinute1,6),
            (Events.evtMinute1,6),
            (evtHS4RequestStop,1),
            (Events.evtMinute1,6)
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtRuntime20,
            ("heatsource/4/availability","availability",0),
            
            evtHS4PanelTemp5,
            "heatsource/4/panel",
            
            evtHS4HeatExTemp5,
            "heatsource/4/heatexbot",
            "heatsource/4/heatex",
            
            evtHS4PanelTemp25,
            "heatsource/4/panel",
            ("heatsource/4/availability","availability",1),
            
            evtHS4PanelTemp95,
            "heatsource/4/panel",
            ("heatsource/4/availability","availability",2),
            
            evtHS4RequestRun,
            
            Events.evtMinute1,
            evtHS4DoRun,
            "webbrick/904/DO/4",
            evtHS4Running,
            "heatsource/4/state",
            "heatsource/4/state",
            
            Events.evtMinute1,
            evtHS4DoRun,
            "webbrick/904/DO/4",
            evtHS4Running,
            "heatsource/4/state",
            "heatsource/4/state",
            
            evtHS4RequestStop,
            
            Events.evtMinute1,
            evtHS4DoStop,
            "webbrick/904/DO/4",
            evtHS4Stopped,
            "heatsource/4/state",
            "heatsource/4/state"
            ]

        self.checkEvents(send, expect)    
    
    def testHeatSourceSolarEast(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceSolarEast" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSource3, (heatSource3FileList,) )

        # the events we send
        send = [ 
            (Events.evtMinute1,9),  # startup
            (evtHS3PanelEastTemp5,2),
            (evtHS3HeatExTemp5,3),
            (evtHS3PanelEastTemp25,4),
            (evtHS3PanelEastTemp95,4),
            (evtHS3RequestRun,1),
            (Events.evtMinute1,7),
            (Events.evtMinute1,7),
            (evtHS3RequestStop,1),
            (Events.evtMinute1,7)
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3WestDoStop,
            evtHS3EastDoStop,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state",

            evtHS3PanelEastTemp5,
            "heatsource/3/elevation/east",
            
            evtHS3HeatExTemp5,
            "heatsource/3/heatexbot",
            "heatsource/3/heatex",
            
            evtHS3PanelEastTemp25,
            "heatsource/3/elevation/east",
            ("heatsource/3/east/availability","availability",1),
            ("heatsource/3/availability","availability",1),
            
            evtHS3PanelEastTemp95,
            "heatsource/3/elevation/east",
            ("heatsource/3/east/availability","availability",2),
            ("heatsource/3/availability","availability",2),
            
            evtHS3RequestRun,
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3RequestStop,
            
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3EastDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state"
            ]

        self.checkEvents(send, expect)

    def testHeatSourceSolarSouth(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceSolarSouth" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSource3, (heatSource3FileList,) )

        # the events we send
        send = [ 
            (Events.evtMinute1,9),  # startup
            (evtHS3PanelSouthTemp5,2),
            (evtHS3HeatExTemp5,3),
            (evtHS3PanelSouthTemp25,4),
            (evtHS3PanelSouthTemp95,4),
            (evtHS3RequestRun,1),
            (Events.evtMinute1,7),
            (Events.evtMinute1,7),
            (evtHS3RequestStop,1),
            (Events.evtMinute1,7)
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3WestDoStop,
            evtHS3EastDoStop,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state",

            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            
            evtHS3HeatExTemp5,
            "heatsource/3/heatexbot",
            "heatsource/3/heatex",
            
            evtHS3PanelSouthTemp25,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",1),
            ("heatsource/3/availability","availability",1),
            
            evtHS3PanelSouthTemp95,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",2),
            ("heatsource/3/availability","availability",2),
            
            evtHS3RequestRun,
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3RequestStop,
            
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state"
            ]

        self.checkEvents(send, expect)    
        
    def testHeatSourceSolarWest(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceSolarWest" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSource3, (heatSource3FileList,) )

        # the events we send
        send = [ 
            (Events.evtMinute1,9),  # startup
            (evtHS3PanelWestTemp5,2),
            (evtHS3HeatExTemp5,3),
            (evtHS3PanelWestTemp25,4),
            (evtHS3PanelWestTemp95,4),
            (evtHS3RequestRun,1),
            (Events.evtMinute1,7),
            (Events.evtMinute1,7),
            (evtHS3RequestStop,1),
            (Events.evtMinute1,7),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3WestDoStop,
            evtHS3EastDoStop,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state",

            evtHS3PanelWestTemp5,
            "heatsource/3/elevation/west",
            
            evtHS3HeatExTemp5,
            "heatsource/3/heatexbot",
            "heatsource/3/heatex",
            
            evtHS3PanelWestTemp25,
            "heatsource/3/elevation/west",
            ("heatsource/3/west/availability","availability",1),
            ("heatsource/3/availability","availability",1),
            
            evtHS3PanelWestTemp95,
            "heatsource/3/elevation/west",
            ("heatsource/3/west/availability","availability",2),
            ("heatsource/3/availability","availability",2),
            
            evtHS3RequestRun,
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3WestDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3WestDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3RequestStop,
            
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3WestDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state"
            ]

        self.checkEvents(send, expect)
    
    def testHeatSourceSolarOverall(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceSolarOverall" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSource3, (heatSource3FileList,) )

        # the events we send
        send = [ 
            (Events.evtMinute1,9),  # startup
            (evtHS3HeatExTemp5,3),
            (evtHS3PanelEastTemp95,4),
            (evtHS3RequestRun,1),
            (Events.evtMinute1,7),
            (evtHS3PanelSouthTemp5,2),
            (Events.evtMinute1,7),
            (evtHS3PanelSouthTemp25,3),
            (Events.evtMinute1,7),
            (evtHS3PanelSouthTemp95,3),
            (Events.evtMinute1,8),
            (evtHS3PanelEastTemp25,3),
            (Events.evtMinute1,8),
            (evtHS3PanelSouthTemp25,4),
            (Events.evtMinute1,8),
            (evtHS3PanelSouthTemp95,4),
            (Events.evtMinute1,8),
            (evtHS3PanelSouthTemp5,4),
            (Events.evtMinute1,8),
            (evtHS3RequestStop,1),
            (Events.evtMinute1,7)
            ]
            
    
        
        
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3WestDoStop,
            evtHS3EastDoStop,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state",

            evtHS3HeatExTemp5,
            "heatsource/3/heatexbot",
            "heatsource/3/heatex",
            
            evtHS3PanelEastTemp95,
            "heatsource/3/elevation/east",
            ("heatsource/3/east/availability","availability",2),
            ("heatsource/3/availability","availability",2),
            
            evtHS3RequestRun,
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            #availability due to east elevation at 2
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp25,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",1),
            #availability due to east elevation at 2
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp95,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",2),
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelEastTemp25,
            "heatsource/3/elevation/east",
            ("heatsource/3/east/availability","availability",1),
            
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoStop,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp25,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",1),
            ("heatsource/3/availability","availability",1),

            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp95,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",2),
            ("heatsource/3/availability","availability",2),
            
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoStop,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",0),
            ("heatsource/3/availability","availability",1), #availability due to east elevation at 1
            

            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3EastDoRun,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3RequestStop,
            
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3EastDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state"
            ]

        self.checkEvents(send, expect)
        
        
        
        
        
        
    def testHeatSourceSolarAvailibility_1(self):
        # this is to test that a heatsource will start to run if it becomes available
        # initial conditions: 
        #       only heatsource for the zone is not available (i.e. avail == 0)
        #       zone is demanding heat, therefore zone and zonegroup are running, 
        # expected: 
        #       heatsource will start to run as soon as it becomes available
        # NOTE
        #       NOTE completed yet
        self._log.debug( "testHeatSourceSolarAvailibility_1" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACSolar, (heatSource3FileList, masterMultipleFileList, groupFileList, zone17FileList) )

        # the events we send
        send = [ 
            (Events.evtMinute1,12),  # startup

            (Events.evtRuntime30,6),
            (evtZone17Temp15,3),
            (evtHS3PanelSouthTemp5,2),
            (evtHS3HeatExTemp5,3),
            (evtZone17SetPoint18,13),
            (evtHS3PanelSouthTemp25,8),
            (Events.evtMinute1,7),
            (evtHS3PanelSouthTemp95,4),
            (Events.evtMinute1,7),
            (evtHS3PanelSouthTemp5,8),
            (Events.evtMinute1,7),

            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3SouthDoStop,
            "zone17/stop",
            "zonegroup/6/stop",
            "webbrick/903/DO/4",
            "zone17/stopped",
#            "zonegroup/6/stop",
            "webbrick/906/DO/1",
            evtHS3Stopped,
            "heatsource/3/state",
            "zonegroup/6/stopped",
            "heatsource/3/state",
#            "zonegroup/6/stopped",

            "time/runtime",
            "zone17/stop",
            "zone17/targetset",
            "zone17/state",
            "zone17/name",
            "zone17/stopped",
#11
            ("webbrick/17/CT/0","val",15.0),
            "zone17/sensor",
            ("zone17/state","cmdsource","Frost"),
#14
            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
#16
            evtHS3HeatExTemp5,
            "heatsource/3/heatexbot",
            "heatsource/3/heatex",
#19
            evtZone17SetPoint18,
            "zone17/schedulesetpoint",
            ("zone17/targetset","val",18.0),
            evtZone17Run,
            ("zone17/state","status","Demand"),
            "zone17/schedulesetpoint",
            evtZone17Running,
            evtZG6Run,
            "webbrick/906/DO/1",
            evtZG6Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
#
            evtHS3PanelSouthTemp25,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",1),
            ("heatsource/3/availability","availability",1),
            evtHS3RequestRun,
            "zonemaster/zonegroup6/heatsource3/run",
            ("zonegroup/6/heatsource","name", "Multi Solar"),
            ("zone17/heatsource","name", "Multi Solar"),
#34
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp95,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",2),
            ("heatsource/3/availability","availability",2),
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",0),
            ("heatsource/3/availability","availability",0),
            "zonemaster/zonegroup6/heatsource3/stop",
            evtHS3RequestStop,
            ("zonegroup/6/heatsource","name", 'Idle'),
            ("zone17/heatsource","name", 'Idle'),
            
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state"
            
            ]

        self.checkEvents(send, expect)    
        
    
    def testHeatSourceSolarAvailibility_2(self):
        # this is to test that a heatsource will start to run if it becomes available
        # initial conditions: 
        #       only heatsource for the zone is not available (i.e. avail == 0)
        #       zone is demanding heat, therefore zone and zonegroup are running, 
        # expected: 
        #       heatsource will start to run as soon as it becomes available
        # NOTE
        #       Focus of this test is to determine what happens if due to temperature fluctuations both request run and request stop 
        #       are issued within one minute (i.e. without a minute event inbetween)
        
        self._log.debug( "testHeatSourceSolarAvailibility_2" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACSolar, (heatSource3FileList, masterMultipleFileList, groupFileList, zone17FileList) )

        # the events we send
        send = [ 
            (Events.evtMinute1,12),  # startup

            (Events.evtRuntime30,6),
            (evtZone17Temp15,3),
            (evtHS3PanelSouthTemp5,2),
            (evtHS3HeatExTemp5,3),
            (evtZone17SetPoint18,13),
            (evtHS3PanelSouthTemp25,8), # results in requestrun 
            (evtHS3PanelSouthTemp5,8),  # results in requeststop 
            (Events.evtMinute1,1),      # nothing should happen since last command was requeststop, which overrides the requestrun
            (evtHS3PanelSouthTemp25,8), 
            (Events.evtMinute1,7),
            (evtHS3PanelSouthTemp5,8),  # results in requeststop 
            (evtHS3PanelSouthTemp25,8), # results in requestrun 
            (Events.evtMinute1,7),      # should continue to run (dorun) since last command was requestrun, which overrides the requetstop
            (evtHS3PanelSouthTemp5,8),
            (Events.evtMinute1,7),

            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3SouthDoStop,
            "zone17/stop",
            "zonegroup/6/stop",
            "webbrick/903/DO/4",
            "zone17/stopped",
#            "zonegroup/6/stop",
            "webbrick/906/DO/1",
            evtHS3Stopped,
            "heatsource/3/state",
            "zonegroup/6/stopped",
            "heatsource/3/state",
#            "zonegroup/6/stopped",

            "time/runtime",
            "zone17/stop",
            "zone17/targetset",
            "zone17/state",
            "zone17/name",
            "zone17/stopped",

            ("webbrick/17/CT/0","val",15.0),
            "zone17/sensor",
            ("zone17/state","cmdsource","Frost"),
            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            evtHS3HeatExTemp5,
            "heatsource/3/heatexbot",
            "heatsource/3/heatex",
            evtZone17SetPoint18,
            "zone17/schedulesetpoint",
            ("zone17/targetset","val",18.0),
            evtZone17Run,
            ("zone17/state","status","Demand"),
            "zone17/schedulesetpoint",
            evtZone17Running,
            evtZG6Run,
            "webbrick/906/DO/1",
            evtZG6Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,

            evtHS3PanelSouthTemp25,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",1),
            ("heatsource/3/availability","availability",1),
            evtHS3RequestRun,
            "zonemaster/zonegroup6/heatsource3/run",
            ("zonegroup/6/heatsource","name", "Multi Solar"),
            ("zone17/heatsource","name", "Multi Solar"),

            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",0),
            ("heatsource/3/availability","availability",0),
            "zonemaster/zonegroup6/heatsource3/stop",
            evtHS3RequestStop,
            ("zonegroup/6/heatsource","name", 'Idle'),
            ("zone17/heatsource","name", 'Idle'),

            Events.evtMinute1,

            evtHS3PanelSouthTemp25,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",1),
            ("heatsource/3/availability","availability",1),
            evtHS3RequestRun,
            "zonemaster/zonegroup6/heatsource3/run",
            ("zonegroup/6/heatsource","name", "Multi Solar"),
            ("zone17/heatsource","name", "Multi Solar"),
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",
            
            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",0),
            ("heatsource/3/availability","availability",0),
            "zonemaster/zonegroup6/heatsource3/stop",
            evtHS3RequestStop,
            ("zonegroup/6/heatsource","name", 'Idle'),
            ("zone17/heatsource","name", 'Idle'),
            
            evtHS3PanelSouthTemp25,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",1),
            ("heatsource/3/availability","availability",1),
            evtHS3RequestRun,
            "zonemaster/zonegroup6/heatsource3/run",
            ("zonegroup/6/heatsource","name", "Multi Solar"),
            ("zone17/heatsource","name", "Multi Solar"),
            
            Events.evtMinute1,
            evtHS3CommonDoRun,
            evtHS3SouthDoRun,
            "webbrick/903/DO/4",
            evtHS3Running,
            "heatsource/3/state",
            "heatsource/3/state",

            evtHS3PanelSouthTemp5,
            "heatsource/3/elevation/south",
            ("heatsource/3/south/availability","availability",0),
            ("heatsource/3/availability","availability",0),
            "zonemaster/zonegroup6/heatsource3/stop",
            evtHS3RequestStop,
            ("zonegroup/6/heatsource","name", 'Idle'),
            ("zone17/heatsource","name", 'Idle'),
            
            Events.evtMinute1,
            evtHS3CommonDoStop,
            evtHS3SouthDoStop,
            "webbrick/903/DO/4",
            evtHS3Stopped,
            "heatsource/3/state",
            "heatsource/3/state",
            
            ]

        self.checkEvents(send, expect)           
        
    def testHeatSourceGroundSource(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceGroundSource" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSource2, (heatSource2FileList,) )

        # the events we send
        send = [ (Events.evtRuntime20,2),
            (evtHS2Enable, 2),
            (evtHS2RequestRun,1),
            (Events.evtMinute1,6),
            (Events.evtMinute1,6),
            (evtHS2RequestStop,1),
            (Events.evtMinute1,6)
            
            ]
        # the events that we expect to be logged.
        expect = [ Events.evtRuntime20,
            ("heatsource/2/availability","availability",0),
            
            evtHS2Enable,
            ("heatsource/2/availability","enabled",1),
            evtHS2RequestRun,
            
            Events.evtMinute1,
            evtHS2DoRun,
            "webbrick/902/DO/4",
            evtHS2Running,
            "heatsource/2/state",
            "heatsource/2/state",
            
            Events.evtMinute1,
            evtHS2DoRun,
            "webbrick/902/DO/4",
            evtHS2Running,
            "heatsource/2/state",
            "heatsource/2/state",

            evtHS2RequestStop,
            
            Events.evtMinute1,
            evtHS2DoStop,
            "webbrick/902/DO/4",
            evtHS2Stopped,
            "heatsource/2/state",
            "heatsource/2/state"
            ]

        self.checkEvents(send, expect)

    def testHeatSourceGeneric_1(self):
        # tests that the heatsource is loaded with defualt parameters
        self._log.debug( "testHeatSourceGeneric_1" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSourceGeneric, (heatSourceGenericFileList,) )

        # the events we send
        send = [ 
            (Events.evtMinute1,7),  # startup
            (Events.evtRuntime20,3),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (evtHS1RequestRun,1),
            (evtHS2RequestRun,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,4),
            (Events.evtMinute1,4),
            (Events.evtMinute1,4),
            (evtHS1RequestStop,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,4),
            (Events.evtMinute1,1),
            ]
        # the events that we expect to be logged.
        expect = [ 
        
            Events.evtMinute1,
            evtHS1DoStop,
            evtHS2DoStop,
            "webbrick/91/DO/0", 
            "webbrick/92/DO/0", 
            evtHS1Stopped,
            evtHS2Stopped,

            Events.evtRuntime20,
            ("heatsource/1/availability","availability",2),
            ("heatsource/2/availability","availability",2),
            
            Events.evtMinute1,         
            Events.evtMinute1,           
            
            evtHS1RequestRun,
            
            evtHS2RequestRun, 
            
            Events.evtMinute1,
            Events.evtMinute1,
            Events.evtMinute1,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/91/DO/0",
            evtHS1Running,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/91/DO/0",
            evtHS1Running,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/91/DO/0",
            evtHS1Running,
            
            evtHS1RequestStop,
            
            Events.evtMinute1,
            
            Events.evtMinute1,    

            Events.evtMinute1,             
            
            Events.evtMinute1,
            evtHS1DoStop,
            "webbrick/91/DO/0",
            evtHS1Stopped,
            
            Events.evtMinute1,    
            ]

        self.checkEvents(send, expect)    
        
        
    def testHeatSourceGeneric_2(self):
        # tests that the heatsource is loaded with defualt parameters
        self._log.debug( "testHeatSourceGeneric_2" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSourceGeneric, (heatSourceGenericFileList,) )

        # the events we send
        send = [ 
            (Events.evtMinute1,7),  # startup
            (Events.evtRuntime20,3),
            (evtHS2Enable, 2),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (evtHS1RequestRun,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,4),
            (Events.evtMinute1,4),
            (Events.evtMinute1,4),
            (evtHS1RequestStop,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,1),
            (Events.evtMinute1,4),
            (Events.evtMinute1,1),
            ]
        # the events that we expect to be logged.
        expect = [ 
        
            Events.evtMinute1,
            evtHS1DoStop,
            evtHS2DoStop,
            "webbrick/91/DO/0", 
            "webbrick/92/DO/0", 
            evtHS1Stopped,
            evtHS2Stopped,

            Events.evtRuntime20,
            ("heatsource/1/availability","availability",2),
            ("heatsource/2/availability","availability",2),
            
            evtHS2Enable,
            ("heatsource/2/availability","enabled",1),
            
            Events.evtMinute1,         
            Events.evtMinute1,           
            
            evtHS1RequestRun,
            
            Events.evtMinute1,
            Events.evtMinute1,
            Events.evtMinute1,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/91/DO/0",
            evtHS1Running,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/91/DO/0",
            evtHS1Running,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/91/DO/0",
            evtHS1Running,
            
            evtHS1RequestStop,
            
            Events.evtMinute1,
            
            Events.evtMinute1,    

            Events.evtMinute1,             
            
            Events.evtMinute1,
            evtHS1DoStop,
            "webbrick/91/DO/0",
            evtHS1Stopped,
            
            Events.evtMinute1,    
            ]

        self.checkEvents(send, expect)    
        
        
    def testHeatSourceBoiler(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceBoiler" )
        self.loadPrimitive( "PersistZonesAll", TestHeatingVentilationACConfigHeatSource1, (heatSource1FileList,) )

        # the events we send
        send = [ 
            (Events.evtMinute1,6),  # startup
            (Events.evtRuntime20,2),
            (evtHS1RequestRun,1),
            (Events.evtMinute1,6),
            (Events.evtMinute1,6),
            (evtHS1RequestStop,1),
            (Events.evtMinute1,6),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS1DoStop,
            "webbrick/901/DO/4",
            evtHS1Stopped,
            "heatsource/1/state",
            "heatsource/1/state",

            Events.evtRuntime20,
            ("heatsource/1/availability","availability",2),
            
            evtHS1RequestRun,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/901/DO/4",                 
            evtHS1Running,
            "heatsource/1/state",
            "heatsource/1/state",
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/901/DO/4",
            evtHS1Running,
            "heatsource/1/state",
            "heatsource/1/state",
            
            evtHS1RequestStop,
            
            Events.evtMinute1,
            evtHS1DoStop,
            "webbrick/901/DO/4",
            evtHS1Stopped,
            "heatsource/1/state",
            "heatsource/1/state"
            ]

        self.checkEvents(send, expect)

    def testHeatSourceMultipleBoiler_1(self):
        # test the heat source logic
        self._log.debug( "testHeatSourceMultipleBoiler_1" )
        self.loadPrimitive( "PersistZonesAll", TestMultipleBoilerHeatSource, (heatSource5FileList,) )

        # the events we send
        send = [ 
            (Events.evtRuntime20,2),
            (evtHS5RequestRun,1),
            (evtHS5FlowTemp80,2),
            (evtHS5ReturnTemp60,2),
            (Events.evtMinute1,5),   # boiler 1 should start
            (Events.evtMinute1,4),
            (Events.evtMinute1,4),
            (Events.evtMinute1,7),   # boiler 2 should start
            (evtHS5RequestStop,1),
            (Events.evtMinute1,8),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtRuntime20,
            ("heatsource/5/availability","availability",2),
            
            evtHS5RequestRun,

            evtHS5FlowTemp80,
            "heatsource/5/flow",
            evtHS5ReturnTemp60,
            "heatsource/5/return",
            
            Events.evtMinute1,
            evtHS5_1DoRun,
            "webbrick/905/DO/4",                 
            evtHS5_1Running,
            evtHS5Running,
            
            Events.evtMinute1,
            evtHS5_1DoRun,
            "webbrick/905/DO/4",
            evtHS5_1Running,
            
            Events.evtMinute1,
            evtHS5_1DoRun,
            "webbrick/905/DO/4",
            evtHS5_1Running,
            
            Events.evtMinute1,
            evtHS5_1DoRun,
            evtHS5_2DoRun,
            "webbrick/905/DO/4",
            "webbrick/905/DO/5",
            evtHS5_1Running,
            evtHS5_2Running,
            
            evtHS5RequestStop,
            
            Events.evtMinute1,
            evtHS5_1DoStop,
            evtHS5_2DoStop,
            "webbrick/905/DO/4",
            "webbrick/905/DO/5",
            evtHS5_1Stopped,
            evtHS5_2Stopped,
            evtHS5Stopped,
            ]

        self.checkEvents(send, expect)

    def testHeatSourceMultipleBoiler_2(self):
        # test the heat source logic
        # handles stop and start of 2nd boiler, starting with boiler 2.
        self._log.debug( "testHeatSourceMultipleBoiler_2" )
        self.loadPrimitive( "PersistZonesAll", TestMultipleBoilerHeatSource, (heatSource5FileList,) )

        # the events we send
        send = [ 
            (Events.evtRuntime20,2),
            (evtHS5RequestRun,1),
            (evtHS5FlowTemp80,2),
            (evtHS5ReturnTemp60,2),
            (Events.evtMinute1Week3,5),   # boiler 2 should start
            (Events.evtMinute1Week3,4),
            (Events.evtMinute1Week3,4),
            (Events.evtMinute1Week3,7),   # boiler 1 should start
            (evtHS5ReturnTemp75,2),
            (Events.evtMinute1Week3,7),
            (Events.evtMinute1Week3,7),
            (Events.evtMinute1Week3,7),
            (Events.evtMinute1Week3,7),   # boiler 1 should stop

            (evtHS5RequestStop,1),
            (Events.evtMinute1Week3,5),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtRuntime20,
            ("heatsource/5/availability","availability",2),
            
            evtHS5RequestRun,
#3
            evtHS5FlowTemp80,
            "heatsource/5/flow",
            evtHS5ReturnTemp60,
            "heatsource/5/return",
#7
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            "webbrick/905/DO/5",
            evtHS5_2Running,
            evtHS5Running,
#12
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            "webbrick/905/DO/5",
            evtHS5_2Running,
#16
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            "webbrick/905/DO/5",
            evtHS5_2Running,
#20
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            evtHS5_1DoRun,
            "webbrick/905/DO/5",
            "webbrick/905/DO/4",
            evtHS5_2Running,
            evtHS5_1Running,
#27
            evtHS5ReturnTemp75,
            "heatsource/5/return",
#29
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            evtHS5_1DoRun,
            "webbrick/905/DO/5",
            "webbrick/905/DO/4",
            evtHS5_2Running,
            evtHS5_1Running,
#36
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            evtHS5_1DoRun,
            "webbrick/905/DO/5",
            "webbrick/905/DO/4",
            evtHS5_2Running,
            evtHS5_1Running,
#43
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            evtHS5_1DoRun,
            "webbrick/905/DO/5",
            "webbrick/905/DO/4",
            evtHS5_2Running,
            evtHS5_1Running,
#50
            Events.evtMinute1Week3,
            evtHS5_2DoRun,
            evtHS5_1DoStop,
            "webbrick/905/DO/5",
            "webbrick/905/DO/4",
            evtHS5_2Running,
            evtHS5_1Stopped,
#50
            evtHS5RequestStop,
            
            Events.evtMinute1Week3,
            evtHS5_2DoStop,
            "webbrick/905/DO/5",
            evtHS5_2Stopped,
            evtHS5Stopped,
            ]

        self.checkEvents(send, expect)

    def testZoneMasterDualGroup1(self):
        # This test should check that when group1 requires heat then the solar panal is fired 
        # up and connected to group1 
        self._log.debug( "testZoneMasterDualGroup1" )
        self.loadMasterDual()

        # the events we send
        send = [ 
            (evtZG1Running,8),
            (evtZG1Stop,8)
            ]
        # the events that we expect to be logged.
        expect = [ evtZG1Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG1HeatSource,   # tell group1 what heat source it uses
            evtZG1Stop,
            evtHS1RequestStop,
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            evtZG1HeatSource,   # tell group1 what heat source it uses, or not.
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)
            
    def testZoneMasterDualGroup2(self):
        # This test should check that when group2 requires heat then the solar panal is fired 
        # up and connected to group2. Note group1 inactive 
        self._log.debug( "testZoneMasterDualGroup2" )
        self.loadMasterDual()

        # the events we send
        send = [ (evtZG2Running,8),
            (evtZG2Stop,8)
            ]
        # the events that we expect to be logged.
        expect = [ evtZG2Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG2HeatSource,   # tell group1 what heat source it uses
            evtZG2Stop,
            evtHS1RequestStop,
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtMasterStop,
            evtZG2HeatSource,   # tell group1 what heat source it uses
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

    def testZoneMasterDualGroup1and2(self):
        # This test should check that when group1 requires heat then the solar panal is fired 
        # up and connected to group1 and group2 gets the boiler.
        self._log.debug( "testZoneMasterDualGroup1and2" )
        self.loadMasterDual()

        # the events we send
        send = [ (evtZG1Running,8),
            (evtZG2Running,4),
            (evtZG1Stop,4),
            (evtZG2Stop,7)
            ]
        # the events that we expect to be logged.
        expect = [ evtZG1Running,
            evtMasterRun,
            "webbrick/900/DO/3",
            evtMasterRunning,
            evtHS1RequestRun,
            "webbrick/90/DO/0",
            evtHS1Running,
            evtZG1HeatSource,   # tell group1 what heat source it uses
            evtZG2Running,
            evtHS4Run,
            "webbrick/91/DO/0",
            evtHS3Running,
            evtZG1Stop,
            evtHS1RequestStop,
            "webbrick/90/DO/0",
            evtHS1Stopped,
            evtZG2Stop,
            evtHS2Stop,
            "webbrick/91/DO/0",
            evtHS2Stopped,
            evtMasterStop,
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)

    def testZoneMasterMultipleGroup1(self):
        self._log.debug( "testZoneMasterMultipleGroup1" )
        self.loadMasterMultiple()

        # the events we send
        send = [ 
            (Events.evtMinute1,27),  # startup

            (Events.evtRuntime20,4),
            (Events.evtRuntime30,11),
            (evtHS4HeatExTemp5,3),
            (evtHS4PanelTemp95,3),
            (evtZone1Temp15,3),
            (evtZone1SetPoint18,18),
            (Events.evtMinute1,6),
            (Events.evtMinute1,6),
            (evtZone1SetPoint14,15),
            (Events.evtMinute1,9),
            (Events.evtMinute1,1),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS1DoStop,
            evtHS4DoStop,
            "zone2/stop",
            "zone1/stop",
            "zonegroup/1/stop",
            "zonegroup/2/stop",
            "webbrick/901/DO/4",
            "webbrick/904/DO/4",
            "zone2/stopped",
            "zone1/stopped",
            "webbrick/901/DO/1",
            "zonegroup/1/heatsource",
            "webbrick/902/DO/1",
            "zonegroup/2/heatsource",
            evtHS1Stopped,
            "heatsource/1/state",
            evtHS4Stopped,
            "heatsource/4/state",
            "zonegroup/1/stopped",
            "zone1/heatsource",
            "zonegroup/2/stopped",
            "zone2/heatsource",
            "heatsource/1/state",
            "heatsource/4/state",
            "zonegroup/1/heatsource",
            "zonegroup/2/heatsource",
#27
            Events.evtRuntime20,
            ("heatsource/1/availability","availability",2),
            ("heatsource/2/availability","availability",0),
            ("heatsource/4/availability","availability",0),

            Events.evtRuntime30,
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone1/stop",
            "zone1/targetset",
            "zone1/state",
            "zone1/name",
            "zone2/stopped",
            "zone1/stopped",

            evtHS4HeatExTemp5,
            "heatsource/4/heatexbot",
            "heatsource/4/heatex",
            
            evtHS4PanelTemp95,
            "heatsource/4/panel",
            ("heatsource/4/availability","availability",2),
            
            evtZone1Temp15,
            "zone1/sensor",
            "zone1/state",
            
            evtZone1SetPoint18,
            "zone1/schedulesetpoint",
            "zone1/targetset",
            evtZone1Run,
            "zone1/state",
            "zone1/schedulesetpoint",
            evtZone1Running,
            evtZG1Run,
            "webbrick/901/DO/1",
            ("zonegroup/1/heatsource","name", 'Idle'),
            evtZG1Running,
            evtMasterRun,
            evtHS4RequestRun,
            "zonemaster/zonegroup1/heatsource4/run",
            ("zonegroup/1/heatsource","name", "Solar"),
            "webbrick/900/DO/3",
            ("zone1/heatsource","name", "Solar"),
            evtMasterRunning,
            
            Events.evtMinute1,
            evtHS4DoRun,
            "webbrick/904/DO/4",
            evtHS4Running,
            "heatsource/4/state",
            "heatsource/4/state",
            
            Events.evtMinute1,
            evtHS4DoRun,
            "webbrick/904/DO/4",
            evtHS4Running,
            "heatsource/4/state",
            "heatsource/4/state",

            evtZone1SetPoint14,
            "zone1/schedulesetpoint",
            "zone1/targetset",
            evtZone1Stop,
            "zone1/state",
            "zone1/schedulesetpoint",
            evtZone1Stopped,
            evtZG1Stop,
            "webbrick/901/DO/1",
            evtHS4RequestStop,
            "zonemaster/zonegroup1/heatsource4/stop",
            ("zonegroup/1/heatsource","name", 'Idle'),
            evtZG1Stopped,
            ("zone1/heatsource","name", 'Idle'),
            ("zonegroup/1/heatsource","name", 'Idle'),
            
            Events.evtMinute1,
            evtHS4DoStop,
            "webbrick/904/DO/4",
            evtHS4Stopped,
            "heatsource/4/state",
            evtMasterStop,
            "heatsource/4/state",
            "webbrick/900/DO/3",
            evtMasterStopped,

            Events.evtMinute1,
            ]

        self.checkEvents(send, expect)

    def testZoneMasterMultipleGroup2(self):
        self._log.debug( "testZoneMasterMultipleGroup2" )
        self.loadMasterMultiple()

        # the events we send
        send = [ 
            (Events.evtMinute1,27),  # startup

            (Events.evtRuntime20,4),
            (Events.evtRuntime30,11),
            (evtHS4HeatExTemp5,3),
            (evtHS4PanelTemp95,3),
            
            (evtZone2Temp15,3),
            (evtZone2SetPoint18,18),
            
            (Events.evtMinute1,6),
            
            (evtZone2SetPoint14,15),
            (Events.evtMinute1,9),
            ]
        # the events that we expect to be logged.
        expect = [ 
            Events.evtMinute1,
            evtHS1DoStop,
            evtHS4DoStop,
            "zone2/stop",
            "zone1/stop",
            "zonegroup/1/stop",
            "zonegroup/2/stop",
            "webbrick/901/DO/4",
            "webbrick/904/DO/4",
            "zone2/stopped",
            "zone1/stopped",
            "webbrick/901/DO/1",
            "zonegroup/1/heatsource",
            "webbrick/902/DO/1",
            "zonegroup/2/heatsource",
            evtHS1Stopped,
            "heatsource/1/state",
            evtHS4Stopped,
            "heatsource/4/state",
            "zonegroup/1/stopped",
            "zone1/heatsource",
            "zonegroup/2/stopped",
            "zone2/heatsource",
            "heatsource/1/state",
            "heatsource/4/state",
            "zonegroup/1/heatsource",
            "zonegroup/2/heatsource",
#26
            Events.evtRuntime20,
            ("heatsource/1/availability","availability",2),
            ("heatsource/2/availability","availability",0),
            ("heatsource/4/availability","availability",0),
            
            Events.evtRuntime30,
            "zone2/stop",
            "zone2/targetset",
            "zone2/state",
            "zone2/name",
            "zone1/stop",
            "zone1/targetset",
            "zone1/state",
            "zone1/name",
            "zone2/stopped",
            "zone1/stopped",
            
            evtHS4HeatExTemp5,
            "heatsource/4/heatexbot",
            "heatsource/4/heatex",
            
            evtHS4PanelTemp95,
            "heatsource/4/panel",
            ("heatsource/4/availability","availability",2),
            
            
            evtZone2Temp15,
            "zone2/sensor",
            "zone2/state",
            
            evtZone2SetPoint18,
            "zone2/schedulesetpoint",
            "zone2/targetset",
            evtZone2Run,
            "zone2/state",
            "zone2/schedulesetpoint",
            evtZone2Running,
            evtZG2Run,
            "webbrick/902/DO/1",
            ("zonegroup/2/heatsource","name", 'Idle'),
            evtZG2Running,
            evtMasterRun,
            evtHS1RequestRun,
            "zonemaster/zonegroup2/heatsource1/run",
            ("zonegroup/2/heatsource","name","Boiler"),
            "webbrick/900/DO/3",
            ("zone2/heatsource","name","Boiler"),
            evtMasterRunning,
            
            Events.evtMinute1,
            evtHS1DoRun,
            "webbrick/901/DO/4",
            evtHS1Running,
            "heatsource/1/state",
            "heatsource/1/state",

            evtZone2SetPoint14,
            "zone2/schedulesetpoint",
            "zone2/targetset",
            evtZone2Stop,
            "zone2/state",
            "zone2/schedulesetpoint",
            evtZone2Stopped,
            evtZG2Stop,
            "webbrick/902/DO/1",
            evtHS1RequestStop,
            "zonemaster/zonegroup2/heatsource1/stop",
            ("zonegroup/2/heatsource","name", 'Idle'),
            evtZG2Stopped,
            ("zone2/heatsource","name", 'Idle'),
            ("zonegroup/2/heatsource","name", 'Idle'),

            Events.evtMinute1,
            evtHS1DoStop,
            "webbrick/901/DO/4",
            evtHS1Stopped,
            "heatsource/1/state",
            evtMasterStop,
            "heatsource/1/state",
            "webbrick/900/DO/3",
            evtMasterStopped
            ]

        self.checkEvents(send, expect)
            
    def testDummy(self):
        pass

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
            [ "testLoad"
            , "testLoadAll"
            # no occupancy and no weather tests
            , "testZone_2_start"
            , "testZone_2a"
            , "testZone_2b"
            , "testZone_2c"
            , "testZone_2d"
            
            # no running and stopped event comming back, i.e. simulating not responding actuator
            , "testZone_2e"
            , "testZone_2f"
            
            # testing that enable and disabling of zone invoke target temp to be set to forst stat. 
            , "testZone_2g"
            
            # testing that when changing forststat temperature the zone target temp is updated if required  
            , "testZone_2h"
            
            # occupancy and no weather tests
            , "testZone_3_start"
            , "testZone_3a"
            , "testZone_3b"
            #, "testZone_3c"
            
            # no occupancy and with weather tests
            , "testZone_4_start"
            , "testZone_4a"
            , "testZone_4b"
            , "testZone_4c"
            
            # occupancy and with weather tests
            , "testZone_5_start"
            , "testZone_5a"
            
            , "testZoneGroup1Zone1_a"
            , "testZoneGroup1Zone1_b"
            , "testZoneGroup1Zone1_c"
            , "testZoneGroup2Zone2"
            , "testZoneGroup2Zone3"
            , "testZoneGroup2Zone4"
            , "testZoneGroup2Zone5"
            , "testZoneGroup2Zone6"
            , "testZoneGroup2All"
            , "testZoneGroup3Zone7"
            , "testZoneGroup3Zone8"
            , "testZoneGroup3Zone9"
            , "testZoneGroup3Zone10"
            , "testZoneGroup3Zone11"
            , "testZoneGroup3All"
            , "testZoneGroup4Zone12"
            , "testZoneGroup4Zone13"
            , "testZoneGroup4Zone14"
            , "testZoneGroup4All"
            , "testZoneGroup5Zone15"
            , "testZoneGroup5Zone16"
            , "testZoneGroup5All"
            
            , "testHeatSourceSolarSingle"
            , "testHeatSourceSolarEast"
            , "testHeatSourceSolarSouth"
            , "testHeatSourceSolarWest"
            , "testHeatSourceSolarOverall"
            , "testHeatSourceSolarAvailibility_1"
            , "testHeatSourceSolarAvailibility_2"

            , "testHeatSourceBoiler"
            , "testHeatSourceMultipleBoiler_1"
            , "testHeatSourceMultipleBoiler_2"
            , "testHeatSourceGroundSource"
            
            , "testZoneMasterMultipleGroup1"
            , "testZoneMasterMultipleGroup2"
            
            , "testWeather1"
            , "testWeather2"
#            , "testWeather3"
#            , "testWeather4"
#            , "testWeather5"
#            , "testWeather6"
            

            ],
        "component":
            [ "testDummy"
            , "testMultiZone_1"

            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            
            , "testZoneGroup1AndMasterSingle"
            , "testZoneGroup2AndMasterSingle"
            , "testZoneGroup3AndMasterSingle"
            , "testZoneGroup4AndMasterSingle"
            , "testZoneGroup5AndMasterSingle"
            
            , "testZoneMasterSingleGroup1"
            , "testZoneMasterSingleGroup2"
            , "testZoneMasterSingleGroup3"
            , "testZoneMasterSingleGroup4"
            , "testZoneMasterSingleGroup5"
            
            
            , "testZoneMasterDualGroup1"
            , "testZoneMasterDualGroup2"
            , "testZoneMasterDualGroup1and2"
            
            , "testZoneMasterPair"
            , "testZoneMasterAll"
            
            ]
        }
    return TestUtils.getTestSuite(TestHeatingVentilationAC, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestHVAC.log", getTestSuite, sys.argv)

# $Id: TestHVAC.py 3201 2009-06-15 15:21:25Z philipp.schuster $
