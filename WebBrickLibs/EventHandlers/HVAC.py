# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: HVAC.py 3201 2009-06-15 15:21:25Z philipp.schuster $
#
#  Heating, Ventilation and Air Conditioning File
#
#  This file includes the following classes to create a full HVAC solution
#       class HeatingVentilationAC( BaseHandler ):
#           class Zone(object):
#           class MultiZone(object):
#           class ZoneGroup(object):
#           class ZoneMaster(object):
#           class HeatSourceBoiler(object):
#           class HeatSourceMultipleBoiler(object):
#           class HeatSourceGround(object):
#           class HeatSourceSolar(object):
#           class HeatSourceMultiSolar(object):
#           class WeatherCompensation(object):
#
# Functional dependancies: 
#       - pair of input and output.xml filef for each zone
#       - pair of input and output.xml file for each zonegroupe
#       - pair of input and output.xml file for each heatsource
#       - pair of input and output.xml file for the zone master
#       - input.xml file for weather compensation
#
#  Author(s): LPK, PS
#
#  Last Edit: 19/07/2008
#  Last Edit: 01/08/2008
#       convert input temp values and settings to float. The event payloads are not always of correct data type.
#


import logging

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

# make logging global to module.
_log = None

#------------------------------------------------------------------------------------------------------------   
#
#   class Zone(object):
#       Class to manage a single heating zone
#           
#   Evaluates if a zone requires to be heated by comparing current temperature with a setpoint,
#   wich is set either by a scheduled event or a manual user input. 
#   If the zone requires heating a run event is issued, see sendRun(self)
#
#   Future Improvements: 
#       - 'Comfort Zone' setting to specify band of temperatures rather than a single setpoint
#       - PID controller to account for lead and lag of the zone hating dynamics and prevent overshoot
#               
#------------------------------------------------------------------------------------------------------------ 
ZONE_DISABLED = 0
ZONE_ENABLED = 1

ZONE_STATE_UNKNOWN = 0
ZONE_STATE_IDLE = 1
ZONE_STATE_DEMAND = 2

ZONEGROUP_STATE_UNKNOWN = 0
ZONEGROUP_STATE_STOPPED = 1
ZONEGROUP_STATE_RUNNING = 2

ZONEMASTER_STATE_UNKNOWN = 0
ZONEMASTER_STATE_STOPPED = 1
ZONEMASTER_STATE_RUNNING = 2

# values for state and request state
HEATSOURCE_UNKNOWN = 0
HEATSOURCE_STOP = 1
HEATSOURCE_RUN = 2

WEATHER_C_STATE_HOLDOFF = 0
WEATHER_C_STATE_RUN = 1

# LPK: As these are used as comparisons  against zone state
# lets make sure they stay the same values, or should they be the same literals as well.
#ACTUATOR_STATE_UNKNOWN = ZONE_STATE_UNKNOWN
#ACTUATOR_STATE_OFF = ZONE_STATE_IDLE
#ACTUATOR_STATE_ON = ZONE_STATE_DEMAND

class Zone(object):
    def __init__(self, parent, zone_cfg):
        self._started = False
        self._parent = parent
        self._zone_key = zone_cfg["key"]
        self._name = zone_cfg["name"]
        self._minzonetemp = 10.0
        self._target = self._minzonetemp
        self._schedulesetpoint = 0
        self._followOccupancy = 0
        self._occupied = 1
        self._wcselect = 0
        self._manualsetpoint = None
        self._zoneTemp = None
        self._enabled = ZONE_DISABLED
        self._cmdsource = 'Frost'
        self._status = 'Idle'
        self._hysteresis = 0.5  # half a degree
        # TODO PS: changed from '' to 'Idle' for UI reasons will have to consider if this is correct 
        self._heatsource = 'Idle'
        # start zone as stopped and actuator as unknown. Then stop issued.
        self._state = ZONE_STATE_IDLE
        self._actuatorstate = ZONE_STATE_UNKNOWN
        
    def zone_key(self):
        return self._zone_key
     
    def start(self):
        self._started = True
        self.sendStop()
        self._state = ZONE_STATE_IDLE
        self.sendTarget()
        self.sendState()
    
    
#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------    

    def doHandleGet(self, key, inEvent):
        if key == "enabled":
            self._enabled = int(inEvent.getPayload()["val"])
            self.doEvaluateZone()
            self.sendState()
        elif key == "matStat":
            self._minzonetemp = float(inEvent.getPayload()["val"])
            self.doEvaluateZone()
            self.sendState()
        elif key == "occupancy":
            self._followOccupancy = int(inEvent.getPayload()["val"])
            self.doEvaluateZone()
            self.sendState()
        elif key == "wcselect":
            self._wcselect = int(inEvent.getPayload()["val"])
            self.doEvaluateZone()
            self.sendState()
#        elif key == "manualsetpoint":
#            self._manualsetpoint = float(inEvent.getPayload()["val"])
#            self.doTargetManual(self._manualsetpoint)
#            self.sendState()
        elif key == "schedulesetpoint":
            if not self._started:
                self._schedulesetpoint = float(inEvent.getPayload()["val"])
                self.doEvaluateZone()
                self.sendState()
        else:
            _log.info( "Unexpected configuration value for zone %s - key %s value %s", self._zone_key, key, inEvent )

    def setOccupied(self, isOccupied):
        self._occupied = isOccupied
        self.doEvaluateZone()
        self.sendState()    
    
    def doHandleScheduleControl(self, newSetpoint):
        if self._schedulesetpoint <> newSetpoint or self._manualsetpoint is not None:
            self._manualsetpoint = None
            if self._schedulesetpoint <> newSetpoint:
                self._schedulesetpoint = newSetpoint 
                self.saveScheduleSetpoint(newSetpoint)
            self.doEvaluateZone()
            self.sendState()
                   
    def doHandleManual(self, newSetpoint):
        _log.debug( "doHandleManual %s %s", newSetpoint, self._manualsetpoint )
        if newSetpoint <> self._manualsetpoint:
            self._manualsetpoint = float(newSetpoint)
            self.doEvaluateZone()
            self.sendState()    
        
    def doHandleSensor(self, newTemp):
        self._zoneTemp = newTemp
        # LPK should we back this off so done on minute tick, achieves a minimum run time.
        self.checkRun()
        self.sendState()            
            
    def doHandleWeather(self, wNr):
        if self._wcselect == wNr:
            self.doEvaluateZone()
            #self.checkRun()
        if wNr <> 0:
            self.sendState()              
            
    def doHandleHeatSource(self, heatsource):
        self._heatsource = heatsource
        #self.sendState()
    
    def doHandleActuatorState(self, state):
        # sets the actuator state depending on running/stopped event which is triggerd by DO event from webbrick
        if state == "running":
            if self._actuatorstate <> ZONE_STATE_DEMAND:
                _log.debug( "zone %s - started", self._zone_key )
            self._actuatorstate = ZONE_STATE_DEMAND
        elif state == "stopped": 
            if self._actuatorstate <> ZONE_STATE_IDLE:
                _log.debug( "zone %s - stopped", self._zone_key )
            self._actuatorstate = ZONE_STATE_IDLE
        elif state == "stop": 
            # we normally create this
            pass
        elif state == "run": 
            # we normally create this
            pass
            
#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#------------------------------------------------------------------------------------------------------------      
            
    def doEvaluateZone(self):
        _log.debug( "doEvaluateZone self._manualsetpoint %s", self._manualsetpoint )
        if self._manualsetpoint is None:
            # there is no manual setpoint
            if self._schedulesetpoint > self._minzonetemp:
                # the scheduled setpoint is above the min zone temp
                if self._enabled:
                    # zone is enabled
                    if self._parent._weathercompensation[self._wcselect]._istate == WEATHER_C_STATE_RUN:
                        if self._followOccupancy:
                            # does follow occupancy
                            if self._occupied:
                                # Home is occupied
                                if self._target <> self._schedulesetpoint:
                                    self._target = self._schedulesetpoint
                                    self._cmdsource = 'Schedule'
                                    self.sendTarget()
                                    self.checkRun()
                            elif self._target <> self._minzonetemp:
                                self._target = self._minzonetemp
                                self._cmdsource = 'Frost'
                                self.sendTarget()
                                self.checkRun()
                        elif self._target <> self._schedulesetpoint:
                            # does not follow occupancy (do not care if occupied) 
                            self._target = self._schedulesetpoint
                            self._cmdsource = 'Schedule'     
                            self.sendTarget()
                            self.checkRun()
                    elif self._schedulesetpoint < self._target:
                        self._target = self._schedulesetpoint
                        self.sendTarget()
                        
                elif self._target <> self._minzonetemp: 
                    self._target = self._minzonetemp
                    self._cmdsource = 'Frost'
                    self.sendTarget()
                    self.checkRun()
                
            elif self._target <> self._minzonetemp: 
                self._target = self._minzonetemp
                self._cmdsource = 'Frost'
                self.sendTarget()
                self.checkRun()
        
        elif self._manualsetpoint > self._minzonetemp:
            _log.debug( "doEvaluateZone.2 %s %s", self._manualsetpoint, self._minzonetemp )
            if self._enabled:
                if self._parent._weathercompensation[self._wcselect]._istate == WEATHER_C_STATE_RUN:
                    _log.debug( "doEvaluateZone.3 %s %s", self._manualsetpoint, self._minzonetemp )
                    if self._followOccupancy:
                        _log.debug( "doEvaluateZone.4 %s %s", self._manualsetpoint, self._minzonetemp )
                        # does follow occupancy
                        if self._occupied:
                            # Need to set new target
                            if self._target <> self._manualsetpoint:
                                self._target = self._manualsetpoint
                                self._cmdsource = 'Manual'
                                self.sendTarget()
                                self.checkRun()
                        elif self._target <> self._minzonetemp:
                            self._target = self._minzonetemp
                            self._cmdsource = 'Frost'
                            self.sendTarget()
                            self.checkRun()
                    elif self._target <> self._manualsetpoint:
                        _log.debug( "doEvaluateZone.5 %s %s", self._manualsetpoint, self._minzonetemp )
                        # does not follow occupancy (do not care if occupied) 
                        self._target = self._manualsetpoint
                        self._cmdsource = 'Manual'     
                        self.sendTarget()
                        self.checkRun()
                elif self._manualsetpoint < self._target:
                    self._target = self._manualsetpoint
                    self.sendTarget()
            
            elif self._target <> self._minzonetemp: 
                self._target = self._minzonetemp
                self._cmdsource = 'Frost'
                self.sendTarget()
                self.checkRun()
                
        elif self._target <> self._minzonetemp: 
            self._target = self._minzonetemp
            self._cmdsource = 'Frost'
            self.sendTarget()
            self.checkRun()
                   
    def checkRun(self):
        # hold off zone start until zone temp is a little below target
        if self._zoneTemp is not None and (self._target - self._hysteresis) > self._zoneTemp:
            if self._parent._weathercompensation[self._wcselect]._istate == WEATHER_C_STATE_RUN:
                if self._state <> ZONE_STATE_DEMAND:
                    self._status = 'Demand'
                    self._state = ZONE_STATE_DEMAND
            elif self._state <> ZONE_STATE_IDLE:
                # PS
                # Code now accessable, no test case for checking if code works correctly!!! 
                # required to respond to 'hold off' state in weather compensation
                self._status = 'Idle'
                self._state = ZONE_STATE_IDLE

        # hold off zone stop until zone temp is a little above target
        elif self._zoneTemp is not None and (self._target + self._hysteresis) < self._zoneTemp:
            if self._state == ZONE_STATE_DEMAND:
                self._status = 'Idle'
                self._state = ZONE_STATE_IDLE

        # moved out of tests above to make clearer
        if self._state <> self._actuatorstate:
            if self._state == ZONE_STATE_DEMAND:
                self.sendRun()
            else:
                self.sendStop()
        
        
#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------     

    def saveScheduleSetpoint(self, newSetpoint):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/events/config/set",
            "%s/schedulesetpoint"%self._zone_key, {'val': newSetpoint} ) )
                       
    def sendTarget(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/zone",
            "%s/targetset"%self._zone_key, {'val': self._target} ) )
        
    def sendRun(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/zone",
            "%s/run"%self._zone_key, None ) )
     
    def sendStop(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/zone",
            "%s/stop"%self._zone_key, None ) )

    def sendName(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zone/name",
            "%s/name"%self._zone_key, 
            {'name': self._name} ) )        
            
    def sendState(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/zone",
            "%s/state"%self._zone_key,
            {'status': self._status, 
                'manualsetpoint': self._manualsetpoint, 
                'zoneTemp': self._zoneTemp, 
                'weather1': self._parent._weathercompensation[1]._state,
                'weather2': self._parent._weathercompensation[2]._state,
                'weather3': self._parent._weathercompensation[3]._state,
                'weathercompensation': self._parent._weathercompensation[self._wcselect]._istate, 
                'cmdsource': self._cmdsource, 
                'enabled': self._enabled, 
                'wcselect': self._wcselect, 
                'schedulesetpoint': self._schedulesetpoint, 
                'state': self._state, 
                'actuatorstate': self._actuatorstate,
                'targetsetpoint': self._target, 
                'zonesource': self._heatsource, 
                'minzonetemp': self._minzonetemp, 
                'occupied': self._occupied, 
                'zoneenabled': '', 
                'followoccupancy': self._followOccupancy } ) )
#


#------------------------------------------------------------------------------------------------------------   
#
#   class MultiZone(object):
#       Class to manage cases where there is a single area in a house that has 2 heating zones
#       this may be the case if there is a single room that has underfloor heating and radiators or     
#       this may be the case when there is a water vessle that has a top and botom coil
#           
#   Acts as a container for multiple zones. 
#
#   Note: only one zoneControl page is shown for a MultiZone, hence there are differnt kid 
#   templates required to set these MultiZones up
#               
#------------------------------------------------------------------------------------------------------------ 


class MultiZone(object):

    def __init__(self, parent, mz_cfg):
        self._started = False
        self._parent = parent
        self._mz_key = mz_cfg["key"]
        self._name = mz_cfg["name"]
        self._zones = []
        for zone_cfg in mz_cfg["parts"]:
            newZone = Zone(parent, zoneCfg)
            self._zones[newZone.zone_key()] = newZone
        
        # PS: 
        # some of the below may be used at a later stage
        # self._occupied = 1
        # self._wcselect = 0
        # self._manualsetpoint = None
        # self._zoneTemp = None
        # self._enabled = 0
        # self._cmdsource = 'Frost'
        # self._status = 'Idle'
        # self._state = ZONE_STATE_UNKNOWN
        # self._heatsource = 'Idle'
        # self._actuatorstate = ZONE_STATE_UNKNOWN

    def mz_key(self):
        return self._mz_key
     
    def start(self):
        self._started = True
        self.sendStop()
        self._state = ZONE_STATE_IDLE
        self.sendTarget()
        self.sendState()    
        
        
        
#------------------------------------------------------------------------------------------------------------   
#
#   class ZoneGroup(object):
#       Class to group zones
#           
#   Zones are combined in a Zone Groups. If a single Zone that belongs to a Zone Groups is 'running' 
#   the Zone group will issue a 'run' event. If none of the zones in a zone group are running the zonegroup 
#   will issue a 'stop' event
#   Zone groups are used to control actuators that are common to multiple zones, such as:
#       - Circulation Pumps 
#       - Manifold Valves etc.  
#
#------------------------------------------------------------------------------------------------------------ 
class ZoneGroup(object):
    def __init__(self, parent, zg_cfg):
        self._parent = parent
        self._zg_key = zg_cfg["key"]
        self._zones = {}
        # TODO PS: changed from '' to 'Idle' for UI reasons will have to consider if this is correct 
        # LK - changed back let zonemaster notify us.
        self._heatsource = ''
        self._state = ZONEGROUP_STATE_STOPPED
        self._actuatorstate = ZONEGROUP_STATE_UNKNOWN # Has to be modified to start in unkown state, same with _state
     
    def start(self):
        self.sendStop()

    def zg_key(self):
        return self._zg_key
   

#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------ 

    def doHandleGet(self, key, inEvent):
        if key == "groupnumber":
            src = inEvent.getSource().split("/")
            idx = inEvent.getPayload()["val"]
            if idx == self._zg_key:
                if src[0] not in self._zones:
                    _log.debug("Adding to zonegroup %s zone %s", self._zg_key, src[0])
                    self._zones[src[0]] = ZONE_STATE_IDLE
            elif src[0] in self._zones:
                _log.debug("Removing from zonegroup %s zone %s", self._zg_key, src[0])
                del self._zones[src[0]]
    
    def doHandleHeatSource(self, heatsource):
        # only handle if changed
        if self._heatsource <> heatsource:
            self._heatsource = heatsource
            for zkey in self._zones:
                # TODO PS: changed from '' to 'Idle' for UI reasons will have to consider if this is correct 
                if self._heatsource <> 'Idle':
                    # The line below can significantly reduce the number of events being sent
                    #if self._zones[zkey] == ZONE_STATE_DEMAND: 
                        self.sendHeatSource(zkey)
                else:
                    self.sendHeatSource(zkey)  
    
    def doState(self, key, cmd):
        if key in self._zones and cmd in ["running","stop","stopped"]:
            if cmd == "running":
                _log.debug("zonegroup %s zone %s running", self._zg_key, key)
                if self._zones[key] <> ZONE_STATE_DEMAND:
                    self._zones[key] = ZONE_STATE_DEMAND
                    self.checkRun()
            elif cmd == "stop" or cmd == "stopped":
                _log.debug("zonegroup %s zone %s stop", self._zg_key, key)
                if self._zones[key] <> ZONE_STATE_IDLE:
                    self._zones[key] = ZONE_STATE_IDLE
                    self.checkRun()
               
    def doHandleActuatorState(self, state):
        # sets the actuator state depending on running/stopped event which is triggerd by DO event from webbrick
        if state == "running":
            _log.debug("zonegroup %s actuator running", self._zg_key)
            self._actuatorstate = ZONEGROUP_STATE_RUNNING
        elif state == "stopped": 
            _log.debug("zonegroup %s actuator stopped", self._zg_key)
            self._actuatorstate = ZONEGROUP_STATE_STOPPED
               
#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#------------------------------------------------------------------------------------------------------------
               
    def checkRun(self):
        if ZONE_STATE_DEMAND in self._zones.values():
            self._state = ZONEGROUP_STATE_RUNNING
        else:
            self._state = ZONEGROUP_STATE_STOPPED

        if self._state <> self._actuatorstate: 
            if self._state == ZONEGROUP_STATE_RUNNING:
                self.sendRun()
            else:
                self.sendStop()

        # LPK Up logging to track a problem
        for k in self._zones:
            zon = self._parent._zones[k]
            if self._zones[k] == ZONE_STATE_DEMAND:
                if zon._state <> ZONE_STATE_DEMAND or zon._actuatorstate <> ZONE_STATE_DEMAND:
                    _log.info("zonegroup %s thinks zone active and zone thinks not state %s actuatorstate %s", self._zg_key, zon._state, zon._actuatorstate)
            else:
                if zon._state <> ZONE_STATE_IDLE or zon._actuatorstate <> ZONE_STATE_IDLE:
                    _log.info("zonegroup %s thinks zone inactive and zone thinks otherwise state %s actuatorstate %s", self._zg_key, zon._state, zon._actuatorstate)
    

#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------ 
    
    def sendRun(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/zonegroup",
            "zonegroup/%s/run"%self._zg_key, None ) )
    
    def sendStop(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/zonegroup",
            "zonegroup/%s/stop"%self._zg_key, None ) )

    def sendHeatSource(self, zkey):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/zone/heatsource",
            "%s/heatsource"%zkey,  {'name': self._heatsource} ) )
#


#------------------------------------------------------------------------------------------------------------   
#
#   class ZoneMaster(object):
#       Class to create link between zonegroups and heatsources 
#           
#   The Zone Master uses persited data (heatsource priorities, heatsource enabled) and heatsource 
#   availibility infortmation to reques the run of the best heatsource on a zonegroup basis, i.e. it responds to 
#   zone group running events, to start a heatsource.  
#   The Zone Master is used to control actuators that are specific to a mapping of heatsource and zonegroup:
#       - 3 way valves
#       - circulation pumps  
#
#------------------------------------------------------------------------------------------------------------ 
class ZoneMaster(object):
    
    def __init__(self, parent):
        self._parent = parent
        self._availability = 0  
        self._enabled = ZONE_ENABLED
        #self._requeststate = 0
        self._state = ZONEMASTER_STATE_STOPPED # 0=Stopped; 1=Running
        self._heatsourceavailibilities = {}
        self._zonegrouppriorities = {}
        self._bestheatsourceforzonegroup = {}
        self._zonegroupstate = {}

        
#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------ 

    def configure( self, cfgDict ):  
        if cfgDict.has_key("zonegroups"):
            for ZGCfg in cfgDict["zonegroups"]:
                try:
                    newZG = {}
                    for HSCfg in cfgDict["heatsources"]:
                        #newHS = {newHS.hs_key():newHS._availability}
                        newZG[HSCfg["key"]] = 0
                    self._zonegrouppriorities[ZGCfg["key"]] = newZG     
                    self._bestheatsourceforzonegroup[ZGCfg["key"]] = None   # Not decided yet
                    self._zonegroupstate[ZGCfg["key"]] = ZONEGROUP_STATE_STOPPED
                except:
                    _log.exception("ZoneMaster zonegroup error %s", ZGCfg)
            
        if cfgDict.has_key("heatsources"):
            for HSCfg in cfgDict["heatsources"]:
                try:    
                    self._heatsourceavailibilities[HSCfg["key"]] = 0
                except:
                    _log.exception("ZoneMaster heatsource error %s", HSCfg)
            
    def doHandleGet(self, key, inEvent):
        if key == "priority":
            src = inEvent.getSource().split("/")
# -------------- This is very likely to change once the xml version of zone heating is phased out, only for backwanrds compatibility done in this way!!!             
            zg_key = src[0][9:]
            hs_key = src[1][10:]
            
            if zg_key in self._zonegrouppriorities: 
                if hs_key in self._zonegrouppriorities[zg_key]:
                    self._zonegrouppriorities[zg_key][hs_key] = int(inEvent.getPayload()["val"])       
            self.doBestHeatSource()

    def anyHeatSourceActive(self):
        for hs_key in self._parent._heatsources:
            if self._parent._heatsources[hs_key]._state == HEATSOURCE_RUN:
                return True
        return False

    def anyZoneGroupActive(self):
        return ZONEGROUP_STATE_RUNNING in self._zonegroupstate.values()
                
    def doHandleHeatSource(self, key, inEvent):
        if key == "availability":
            src = inEvent.getSource().split("/")
            if src[1] in self._heatsourceavailibilities:
                self._heatsourceavailibilities[src[1]] = int(inEvent.getPayload()["availability"])
                _log.debug("ZoneMaster doHandleHeatSource %s %s", src[1], self._heatsourceavailibilities[src[1]])
                self.doBestHeatSource()
        
        elif key == "running":
            # No longer needed rely on heat sources them selves
            pass
        
        elif key == "stopped":
            if not self.anyHeatSourceActive() and not self.anyZoneGroupActive() and self._state <> ZONEMASTER_STATE_STOPPED: 
                self._state = ZONEMASTER_STATE_STOPPED
                self.sendStop()
                    
    def doHandleZoneGroup(self, key, cmd):
        if key in self._zonegroupstate:
            if cmd == "running":
                self._zonegroupstate[key] = ZONEGROUP_STATE_RUNNING
            elif cmd == "stop" or cmd == "stopped":
                self._zonegroupstate[key] = ZONEGROUP_STATE_STOPPED
            self.checkRun(key)
        else:
            _log.info("Unrecognised zonegroup %s (%s)", key, cmd )
            

#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#------------------------------------------------------------------------------------------------------------
            
    def doHSName(self, hs_key):
        for zg_key in self._zonegroupstate:
            if self._zonegroupstate[zg_key] == 1 and self._bestheatsourceforzonegroup[zg_key] == hs_key:
                self.sendHSName(zg_key, self._parent._heatsources[hs_key]._name)
             
    def doBestHeatSource(self):  
        
        for zg_key in self._zonegrouppriorities:
            currenths = self._bestheatsourceforzonegroup[zg_key]
            higestpriority = 0
            self._bestheatsourceforzonegroup[zg_key] = None
            for hs_key in self._heatsourceavailibilities:
                if self._heatsourceavailibilities[hs_key] <> 0:
                    if self._zonegrouppriorities[zg_key][hs_key] > higestpriority:
                        higestpriority = self._zonegrouppriorities[zg_key][hs_key]
                        self._bestheatsourceforzonegroup[zg_key] = hs_key

            _log.debug("doBestHeatSource %s old heatsource %s new heatsource %s",zg_key,currenths,self._bestheatsourceforzonegroup[zg_key])

            # check if there has been a change
            if self._bestheatsourceforzonegroup[zg_key] <> currenths:
                # best heatsource for a zonegroup has changed, is the zonegroup running
                if self._zonegroupstate[zg_key] == ZONEGROUP_STATE_RUNNING:
                    # check if current hs is None
                    if currenths is not None:
                        #stop the actuators associated with the the combo of ZG and current HS
                        self.sendZoneGroupHeatSourceStop(zg_key, currenths)
                        # is the HS used soley by this ZG and can be switched off? 
                        inUse = 0
                        for zonegroup in self._bestheatsourceforzonegroup: 
                            if self._bestheatsourceforzonegroup[zonegroup] == currenths and self._zonegroupstate[zonegroup] == ZONEGROUP_STATE_RUNNING:
                                _log.debug("doBestHeatSource %s heatsource in use by", currenths, zonegroup )
                                inUse = 1
                        if inUse == 0 and self._parent._heatsources[currenths]._requeststate == HEATSOURCE_RUN:
                            self.sendHSRequestStop(currenths)
                        else:
                            _log.debug("doBestHeatSource leave %s heatsource running", currenths )

                        # TODO PS: changed from '' to 'Idle' for UI reasons will have to consider if this is correct     
                        self.sendHSName(zg_key, 'Idle')    
                    self.checkRun(zg_key)    
                
    def checkRun(self, key):
        # PS
        # self._zonegroupstate is a dictonary containing the state of the  zonegroups, i.e. running or stoped. 
        if ZONEGROUP_STATE_RUNNING in self._zonegroupstate.values():
            if self._state == ZONEMASTER_STATE_STOPPED:
                self._state = ZONEMASTER_STATE_RUNNING
                self.sendRun()

        hs_key = self._bestheatsourceforzonegroup[key]
        if hs_key is None:
            # PS: 
            # NOTE: this may be due to heatsource being no longer available (example: Solar)
            # changed logging priority to debug since there being no suitable heatsource is nto nessecarily an error (eample: Solar)
            _log.debug("No suitable heatsource for zonegroup %s", key)
            
        elif self._zonegroupstate[key] == ZONEGROUP_STATE_RUNNING:
            if self._parent._heatsources[hs_key]._requeststate == HEATSOURCE_STOP:
                # heatsource coudl be running because another zones also requests it
                self.sendHSRequestRun(hs_key)
                
            # have to adjust linking actuators (three way valves etc)
            self.sendZoneGroupHeatSourceRun(key, hs_key)
            # have to send zonegorup heatsource name
            self.sendHSName(key, self._parent._heatsources[hs_key]._name)
                
        else: 
            # have to check if no other zonegroups needs the heatsource
            inUse = 0
            for zonegroup in self._bestheatsourceforzonegroup: 
                if self._bestheatsourceforzonegroup[zonegroup] == hs_key and self._zonegroupstate[zonegroup] == ZONEGROUP_STATE_RUNNING:
                    inUse = 1
            if inUse == 0 and self._parent._heatsources[hs_key]._requeststate == HEATSOURCE_RUN:
                self.sendHSRequestStop(hs_key)
                self.sendZoneGroupHeatSourceStop(key, hs_key)
            # TODO PS: changed from '' to 'Idle' for UI reasons will have to consider if this is correct 
            self.sendHSName(key, 'Idle')    
    
    def sanityCheck(self):
        # called once a minute to perform some sanity checks.

        # LPK Up logging to track a problem
        for k in self._zonegroupstate:
            zg = self._parent._zonegroups[k]
            if self._zonegroupstate[k] == ZONEGROUP_STATE_RUNNING:
                if zg._state <> ZONEGROUP_STATE_RUNNING or zg._actuatorstate <> ZONEGROUP_STATE_RUNNING:
                    _log.info("zonemaster thinks zonegroup %s active and zonegroup thinks not state %s actuatorstate %s", k, zg._state, zg._actuatorstate)
            else:
                if zg._state <> ZONEGROUP_STATE_STOPPED or zg._actuatorstate <> ZONEGROUP_STATE_STOPPED:
                    _log.info("zonemaster thinks zonegroup %s inactive and zonegroup thinks otherwise state %s actuatorstate %s", k, zg._state, zg._actuatorstate)

#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------ 
    
    def sendHSName(self, zg_key, hs_key):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/group/heatsource",
            "zonegroup/%s/heatsource"%zg_key,  
            {'name': hs_key}) )  

    def sendRun(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/master",
            "zonemaster/run",  None ) )  
    
    def sendStop(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/master",
            "zonemaster/stop",  None ) )          
            
    def sendHSRequestRun(self, hs_key):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/requestrun"%hs_key,  None ) )  
           
    def sendHSRequestStop(self, hs_key):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/requeststop"%hs_key,  None ) ) 

    def sendZoneGroupHeatSourceRun(self, zg_key, hs_key):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/master",
            "zonemaster/zonegroup%s/heatsource%s/run"% (zg_key, hs_key),  None ) )     
            
    def sendZoneGroupHeatSourceStop(self, zg_key, hs_key):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/master",
            "zonemaster/zonegroup%s/heatsource%s/stop"% (zg_key, hs_key),  None ) )  
#


#------------------------------------------------------------------------------------------------------------   
#   
#   class HeatSourceBoiler(object):    
#       Class to manage Oil or Gas Boiler
#           
#   The Boiler is the simplest heatsource, it is always available. 
#   When requested to run (requestrun event) it will start within a minute and issue a 'dorun' event 
#   every minute. When requested to stop, it wil stop withon a minute and issue a 'dostop' event.
#           
#------------------------------------------------------------------------------------------------------------ 
class HeatSourceBoiler(object):

    def __init__(self, parent, hs_cfg):
        self._parent = parent
        self._hs_key = hs_cfg["key"]
        self._name = hs_cfg["name"]
        self._type = hs_cfg["type"]
        self._availability = 2
        self._enabled = ZONE_ENABLED
        self._requeststate = HEATSOURCE_STOP
        self._state = HEATSOURCE_UNKNOWN
 
    def hs_key(self):
        return self._hs_key
    
    def getType(self):
        return self._type
    
    
#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------  

    def doHandleGet(self, key, inEvent):
        if key == "enabled":
            self._enabled = int(inEvent.getPayload()["val"])
            self.sendState()
    
    def doHandleSensor(self, key, inEvent):    
        # Does not have input from sensors
        pass
         
    def doHandleHeatSource(self, part, cmd, inEvent):
        if cmd == "requestrun": 
            self._requeststate = HEATSOURCE_RUN
        elif cmd == "requeststop":
            self._requeststate = HEATSOURCE_STOP
     
     
#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#------------------------------------------------------------------------------------------------------------
     
    def checkRun(self, minuteEvent):
        # currently ignores availibility!
        if self._enabled == ZONE_ENABLED:
            if self._requeststate == HEATSOURCE_RUN:
                self.sendRun()
                self._state = HEATSOURCE_RUN
            elif self._state <> HEATSOURCE_STOP:
                self.sendStop()
                self._state = HEATSOURCE_STOP
    
    
#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------  
   
    def sendState(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/availability"%self._hs_key, 
            {'availability': self._availability
            ,'enabled': self._enabled
            ,'name': self._name} ) )
    
    def sendRun(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dorun"%self._hs_key, None ) )
    
    def sendStop(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dostop"%self._hs_key, None ) )
#


#------------------------------------------------------------------------------------------------------------   
#   
#   class HeatSourceMultipleBoiler(object):    
#       Class to manage multiple Oil or Gas Boiler
#           
#   When requested to run (requestrun event) it will start within a minute and issue a 'dorun' event 
#   every minute. When requested to stop, it wil stop withon a minute and issue a 'dostop' event.
#
#   It manages multiple boilers, the choice of initial boiler depends on the week of the year so as to
#   rotate the usage. After a configued interval the flow and return temperature are compared and
#   if too high an additional boiler will be started if they are too small then a boiler may be stopped.
#   The aim is to keep the boilers working in there most efficient range.
#           
#------------------------------------------------------------------------------------------------------------ 
class Boiler(object):
    def __init__(self, bl_cfg):
        self._key = bl_cfg["key"]
        self._name = bl_cfg["name"]
        self._active = False

    def set_active(self):
        self._active = True

    def set_inactive(self):
        self._active = False

    def isactive(self):
        return self._active

class HeatSourceMultipleBoiler(object):

    def __init__(self, parent, hs_cfg):
        self._parent = parent
        self._hs_key = hs_cfg["key"]
        self._name = hs_cfg["name"]
        self._type = hs_cfg["type"]
        # TODO may want to process this better
        # such as use the boiler keys
        self._boilers = []
        if hs_cfg.has_key("boilers"):
            for bl_cfg in hs_cfg["boilers"]:
                self._boilers.append(Boiler(bl_cfg))
        else:
            _log.error("No boilers defined in %s", hs_cfg )

        self._frmin = 5.0
        self._frmax = 15.0
        self._checkinterval = 5

        if hs_cfg.has_key("flowreturnmin"):
            self._frmin = float(hs_cfg["flowreturnmin"])
        if hs_cfg.has_key("flowreturnmax"):
            self._frmax = float(hs_cfg["flowreturnmax"])
        if hs_cfg.has_key("checkinterval"):
            self._checkinterval = float(hs_cfg["checkinterval"])

        self._availability = 2
        self._enabled = ZONE_ENABLED
        self._requeststate = HEATSOURCE_STOP
        self._state = HEATSOURCE_UNKNOWN
        self._flow_temp = 0
        self._return_temp = 0
        self._check_counter = 0
        self._active_count = 0
 
    def hs_key(self):
        return self._hs_key
    
    def getType(self):
        return self._type
    
    
#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------  

    def doHandleGet(self, key, inEvent):
        if key == "enabled":
            self._enabled = int(inEvent.getPayload()["val"])
            self.sendState()
    
    def doHandleSensor(self, key, inEvent):
        _log.debug("doHandleSensor %s", inEvent)
        # save for later evaluation
        if key == "flow":
            self._flow_temp = float(inEvent.getPayload()["val"])
        elif key == "return":
            self._return_temp = float(inEvent.getPayload()["val"])   
         
    def doHandleHeatSource(self, part, cmd, inEvent):
        if cmd == "requestrun": 
            if self._requeststate <> HEATSOURCE_RUN:
                self._requeststate = HEATSOURCE_RUN
                self._active_count = 1
                self._check_counter = self._checkinterval
        elif cmd == "requeststop":
            self._requeststate = HEATSOURCE_STOP
        elif cmd == "running":
            self._boilers[int(part)-1].set_active()
            if self._state <> HEATSOURCE_RUN:
                self._state = HEATSOURCE_RUN
                self.sendRunning()
        elif cmd == "stopped":
            self._boilers[int(part)-1].set_inactive()
            self._state = HEATSOURCE_STOP # assume all stopped
            for idx in range(0,len(self._boilers)):
                if self._boilers[idx].isactive():
                    self._state = HEATSOURCE_RUN

            if self._state == HEATSOURCE_STOP:
                self.sendStopped()
     
     
#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#------------------------------------------------------------------------------------------------------------
     
    def checkRun(self, minuteEvent):
        # Called once a minute

        # currently ignores availibility!
        # TODO re-evaluate and decide how many boilers to request
        # 
        if self._enabled == ZONE_ENABLED:

            if self._requeststate == HEATSOURCE_RUN:
                if self._check_counter > 0:
                    self._check_counter = self._check_counter - 1
                if self._check_counter <= 0:
                    self._check_counter = self._checkinterval
                    delta = self._flow_temp - self._return_temp
                    _log.debug("checkRun delta %s", delta)
                    if delta > self._frmax and self._active_count < len(self._boilers):
                        # start another boiler
                        self._active_count = self._active_count+1
                    elif delta > self._frmin and self._active_count > 0:
                        # stop boiler
                        self._active_count = self._active_count-1

                _log.debug("checkRun %s", self._active_count)
                base = minuteEvent.getPayload()["week"] % len(self._boilers)
                for idx in range(0,self._active_count):
                    self.sendRun((base+idx)%len(self._boilers))
                for idx in range(self._active_count, len(self._boilers)):
                    self.sendStop((base+idx)%len(self._boilers))

            elif self._state <> HEATSOURCE_STOP:
                for idx in range(0,len(self._boilers)):
                    self.sendStop(idx)
                self._state = HEATSOURCE_STOP
    
    
#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------  
   
    def sendState(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/availability"%self._hs_key, 
            {'availability': self._availability
            ,'enabled': self._enabled
            ,'name': self._name} ) )
    
    def sendRun(self, idx):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/%s/dorun"%(self._hs_key,idx+1), None ) )
    
    def sendRunning(self):
        # we need to amalgamate multiple running
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/running"%self._hs_key, None ) )
    
    def sendStop(self, idx):
        if self._boilers[idx].isactive():
            self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
                "heatsource/%s/%s/dostop"%(self._hs_key,idx+1), None ) )
    
    def sendStopped(self):
        # we need to amalgamate multiple stopped
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/stopped"%self._hs_key, None ) )
#

#------------------------------------------------------------------------------------------------------------   
#   
#   class HeatSourceGround(object):    
#       Class to manage Ground Source Heatpump
#           
#   Currently operates exactly like a Boiler, in future however it should use further inputs to adjust its availibility. 
#   Default availibility is 0, i.e. at them moment the zone master will not consider it as a viable heatsource!!! 
#           
#------------------------------------------------------------------------------------------------------------          
class HeatSourceGround(object):

    def __init__(self, parent, hs_cfg):
        self._parent = parent
        self._hs_key = hs_cfg["key"]
        self._name = hs_cfg["name"]
        self._type = hs_cfg["type"]
        self._availability = 0  
        self._enabled = ZONE_DISABLED
        self._requeststate = HEATSOURCE_STOP
        self._state = HEATSOURCE_UNKNOWN
        self._manifoldTemp = None
        self._heatexTemp = None
 
    def hs_key(self):
        return self._hs_key
    
    def getType(self):
        return self._type
        

#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------   

    def doHandleGet(self, key, inEvent):
        if key == "enabled":
            self._enabled = int(inEvent.getPayload()["val"])
            self.sendState()
    
    def doHandleSensor(self, key, inEvent):
        if key == "manifold":
            self._manifoldTemp = float(inEvent.getPayload()["val"])
        elif key == "heatex":
            self._heatexTemp = float(inEvent.getPayload()["val"])   
        # is Ground Source availibility really dependant on these temperatures (taken from xml) ....
        # self.doAvailability()
        self.sendState()

    def doHandleHeatSource(self, part, cmd, inEvent):
        if cmd == "requestrun": 
            self._requeststate = HEATSOURCE_RUN
        elif cmd == "requeststop":
            self._requeststate = HEATSOURCE_STOP
    
#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#------------------------------------------------------------------------------------------------------------

    def doAvailability(self):
        # to be implemented once it is clear what influences the availability
        pass 
   
    def checkRun(self, minuteEvent):
        # currently ignors availibility!
        if self._enabled == ZONE_ENABLED:
            if self._requeststate == HEATSOURCE_RUN:
                self.sendRun()
                if self._state <> HEATSOURCE_RUN:
                    self._state = HEATSOURCE_RUN
            elif self._state <> HEATSOURCE_STOP:
                self.sendStop()
                self._state = HEATSOURCE_STOP


#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------  
   
    def sendState(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/availability"%self._hs_key, 
            {'availability': self._availability
            ,'enabled': self._enabled
            ,'name': self._name} ) )
    
    def sendRun(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dorun"%self._hs_key, None ) )
    
    def sendStop(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dostop"%self._hs_key, None ) )
#


#------------------------------------------------------------------------------------------------------------   
#   
#   class HeatSourceSolar(object):    
#       Class to manage single solar panel elevation
#           
#   Uses the difference between a the panel temperature and the temperature at the heatexchagner to 
#   calculate its availibility. 
# If the temperature difference is greater than 8C the availibility will be 1, if the panel temperature
#   is also above 50C the availibility will be 2. If the temperatre differenc edrops below 4C the availibility is 
#   set to 0.
#           
#------------------------------------------------------------------------------------------------------------      
class HeatSourceSolar(object):

    def __init__(self, parent, hs_cfg):
        self._parent = parent
        self._hs_key = hs_cfg["key"]
        self._name = hs_cfg["name"]
        self._type = hs_cfg["type"]
        self._availability = 0  
        self._enabled = ZONE_ENABLED
        self._requeststate = HEATSOURCE_STOP
        self._state = HEATSOURCE_UNKNOWN
        self._panelTemp = None
        self._heatexTemp = None
 
    def hs_key(self):
        return self._hs_key
    
    def getType(self):
        return self._type
        
    def doHandleGet(self, key, inEvent):
        if key == "enabled":
            self._enabled = int(inEvent.getPayload()["val"])
            self.sendState()
        
    def doHandleSensor(self, key, inEvent):
        if key == "panel":
            self._panelTemp = float(inEvent.getPayload()["val"])
        elif key == "heatex":
            self._heatexTemp = float(inEvent.getPayload()["val"])   
        self.doAvailability()
    
    def doAvailability(self):
        if not None in (self._panelTemp, self._heatexTemp):
            oldavailability = self._availability 
            if (self._panelTemp - self._heatexTemp) > 8.0: # Solar will be available 
                if self._panelTemp > 50:
                    self._availability = 2
                else:
                    self._availability = 1
            elif (self._panelTemp - self._heatexTemp) < 4.0: # Solar will not be available 
                self._availability = 0
            
            if oldavailability <> self._availability :
                self.sendState()        
    
    def doHandleHeatSource(self, part, cmd, inEvent):
        if cmd == "requestrun": 
            self._requeststate = HEATSOURCE_RUN
        elif cmd == "requeststop":
            self._requeststate = HEATSOURCE_STOP
     
    def checkRun(self, minuteEvent):
        # currently ignors availibility! (Availability should be processed by zone master, not internally??? Other thoughts??)
        if self._enabled == ZONE_ENABLED:
            if self._requeststate == HEATSOURCE_RUN:
                self.sendRun()
                if self._state <> HEATSOURCE_RUN:
                    self._state = HEATSOURCE_RUN
            elif self._state <> HEATSOURCE_STOP:
                self.sendStop()
                self._state = HEATSOURCE_STOP
    
    def sendState(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/availability"%self._hs_key, 
            {'availability': self._availability
            ,'enabled': self._enabled
            ,'name': self._name} ) )
    
    def sendRun(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dorun"%self._hs_key, None ) )
    
    def sendStop(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dostop"%self._hs_key, None ) )
#

#------------------------------------------------------------------------------------------------------------   
#   
#   class SolarElevation(object):    
#       Class to manage a Soalr Elevation that is part of a Multi Solar Heatsource
#           
#   Uses the difference between a the panel temperature and the temperature at the heatexchagner to 
#   calculate its availibility. 
#   If the temperature difference is greater than 8C the availibility will be 1, if the panel temperature
#   is also above 50C the availibility will be 2. If the temperatre differenc edrops below 4C the availibility is 
#   set to 0.
#           
#------------------------------------------------------------------------------------------------------------      
class SolarElevation(object):

    def __init__(self, parent, el_cfg):
        self._parent = parent
        self._el_key = el_cfg["key"]
        self._name = el_cfg["name"]
        self._type = el_cfg["type"]
        self._availability = 0  
        self._enabled = ZONE_ENABLED
        self._requeststate = HEATSOURCE_STOP
        self._state = HEATSOURCE_UNKNOWN
        self._panelTemp = None
        self._heatexTemp = None
 
    def el_key(self):
        return self._el_key
    
    def getType(self):
        return self._type
        
    def doHandleGet(self, key, inEvent):
        if key == "enabled":
            self._enabled = int(inEvent.getPayload()["val"])
            self.sendState()
    
    def setElevationTemp(self, value):
        self._panelTemp = float(value)
        self.doAvailability()
        
    def setHeatexTemp(self, value):
        self._heatexTemp = float(value)
        self.doAvailability()
    
    def doAvailability(self):
        if not None in (self._panelTemp, self._heatexTemp):
            oldavailability = self._availability 
            if (self._panelTemp - self._heatexTemp) > 8.0: # Solar will be available 
                if self._panelTemp > 50:
                    self._availability = 2
                else:
                    self._availability = 1
            elif (self._panelTemp - self._heatexTemp) < 4.0: # Solar will not be available 
                self._availability = 0
            
            if oldavailability <> self._availability :
                # only used to update the UI value passes internally using lines below
                self.sendState()      
                # function call to update availability sotred in multiSolar class
                self._parent.setElevationAvailability(self._el_key, self._availability)                
    
    def doHandleHeatSource(self, part, cmd, inEvent):
        if cmd == "requestrun": 
            self._requeststate = HEATSOURCE_RUN
        elif cmd == "requeststop":
            self._requeststate = HEATSOURCE_STOP
     
    def checkRun(self, minuteEvent):
        # PS: 
        # currently ignors availibility! (Availability should be processed by zone master, not internally??? Other thoughts??)
        if self._enabled == ZONE_ENABLED:
            if self._requeststate == HEATSOURCE_RUN:
                self.sendRun()
                if self._state <> HEATSOURCE_RUN:
                    self._state = HEATSOURCE_RUN
            elif self._state <> HEATSOURCE_STOP:
                self.sendStop()
                self._state = HEATSOURCE_STOP

                
#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------  
                
    def sendState(self):
        self._parent.sendElevationState(self._el_key, self._availability, self._enabled, self._name)
    
    def sendRun(self):
        self._parent.sendElevationRun(self._el_key)
    
    def sendStop(self):
        self._parent.sendElevationStop(self._el_key)
#


#------------------------------------------------------------------------------------------------------------   
#   
#   class HeatSourceMultiSolar(object):    
#       Class to manage multiple solar panel elevation
#           
#------------------------------------------------------------------------------------------------------------         
class HeatSourceMultiSolar(object):

    def __init__(self, parent, hs_cfg):
        self._parent = parent
        self._hs_key = hs_cfg["key"]
        self._name = hs_cfg["name"]
        self._type = hs_cfg["type"]
        self._elevations = {}
        self._elevationavailabilities = {}
        for el_cfg in hs_cfg["elevations"]:
            self.addElevation(SolarElevation(self, el_cfg))    
        self._availability = 0  
        self._enabled = ZONE_ENABLED
        self._requeststate = HEATSOURCE_STOP
        self._state = HEATSOURCE_UNKNOWN
        

    def hs_key(self):
        return self._hs_key

    def getType(self):
        return self._type
  
    def addElevation(self, elevation):
        self._elevations[elevation.el_key()] = elevation
        newElevation = {elevation.el_key():0}
        self._elevationavailabilities.update(newElevation)
       
    def setElevationAvailability(self, el_key, value):
        _log.debug("setElevationAvailability %s %s", el_key, value)
        if el_key in self._elevations:
            self._elevationavailabilities[el_key] = int(value)
            self.doAvailability()
            
#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------   

    def doHandleGet(self, key, inEvent):
        if key == "enabled":
            self._enabled = int(inEvent.getPayload()["val"])
            for el_key in self._elevations:
                self._elevations[el_key].doHandleGet(key, inEvent)
            self.sendState()
        
    def doHandleSensor(self, key, inEvent):
        if key == "elevation":
            src = inEvent.getSource().split("/")
            if src[3] in self._elevations:
                self._elevations[src[3]].setElevationTemp(inEvent.getPayload()["val"])
        elif key == "heatex":
            for el_key in self._elevations:
                self._elevations[el_key].setHeatexTemp(inEvent.getPayload()["val"])
         
    def doHandleHeatSource(self, part, cmd, inEvent):
        if cmd == "requestrun": 
            self._requeststate = HEATSOURCE_RUN
            for elevation in self._elevationavailabilities: 
                if self._elevationavailabilities[elevation] == self._availability:
                    self._elevations[elevation]._requeststate = self._requeststate
        
        elif cmd == "requeststop":
            self._requeststate = HEATSOURCE_STOP
            for elevation in self._elevationavailabilities: 
                self._elevations[elevation]._requeststate = self._requeststate
            

#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#----------------------------------------------------------------------------------------------------------
            
    def doAvailability(self):
        oldavailability = self._availability
        if 2 in self._elevationavailabilities.values():
            self._availability = 2
        elif 1 in self._elevationavailabilities.values():
            self._availability = 1
        else:
            self._availability = 0
        
        # reevaluate if a panel shoudl still be running if its 
        for elevation in self._elevationavailabilities: 
            if self._elevationavailabilities[elevation] == self._availability:
                self._elevations[elevation]._requeststate = self._requeststate
            else:
                self._elevations[elevation]._requeststate = HEATSOURCE_STOP
        # has overall availability changed?
        if oldavailability <> self._availability :
            _log.debug("doAvailability %s %s", self._hs_key, self._availability)
            self.sendState()  
        
    def checkRun(self, minuteEvent):
        # currently ignors availibility! (Availability should be processed by zone master, not internally??? Other thoughts??)
        if self._enabled == ZONE_ENABLED:
            if self._requeststate == HEATSOURCE_RUN:
                self.sendRun()
                if self._state <> HEATSOURCE_RUN:
                    self._state = HEATSOURCE_RUN
            elif self._state <> HEATSOURCE_STOP:
                self.sendStop()
                self._state = HEATSOURCE_STOP
        for elevation in self._elevations:
            self._elevations[elevation].checkRun(minuteEvent)
            

#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------  
            
    def sendState(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/availability"%self._hs_key, 
            {'availability': self._availability
            ,'enabled': self._enabled
            ,'name': self._name} ) )
    
    def sendRun(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dorun"%self._hs_key, None ) )
    
    def sendStop(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/dostop"%self._hs_key, None ) )
            
    def sendElevationState(self, el_key, availability, enabled, name):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/%s/availability"%(self._hs_key, el_key), 
            {'availability': availability
            ,'enabled': enabled
            ,'name': name} ) )
            
    def sendElevationRun(self, el_key):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/%s/dorun"%(self._hs_key, el_key), None ) )
    
    def sendElevationStop(self, el_key):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/%s/%s/dostop"%(self._hs_key, el_key), None ) )    
         
#    


#------------------------------------------------------------------------------------------------------------   
#   
#   class WeatherCompensation(object):    
#       Class to provide weather compensation 
#           
#   Evaluates the temperature trend over the past 10 minutes and sets state/istate variable 
#   based on high and low thresholds to indicate if heating should run or be held off 
#   Operates on a Zone basis, i.e.  a zone will have to be configured to follow a set of weather 
#   compensation, with associated thresholds. Weather compensation 0 is a special case, which is 
#   effectifely no weather compensation
#           
#   Future Improvements:
#       - RSS Feed interface for weather forecast 
#
#------------------------------------------------------------------------------------------------------------ 
class WeatherCompensation(object):
    def __init__(self, parent, wkey):
        self._parent = parent
        self._started = False
        self._weatherkey = wkey
        self._trend = '' 
        self._state = "Run"
        self._istate = WEATHER_C_STATE_RUN    # 0 = HoldOff; 1 = Run
        self._tstate = 1    # 0=Down; 1=Level; 2=Up
        self._previousTemp = None
        self._currentTemp = None
        self._risingThres = None
        self._fallingThres = None
        
    def start(self):
        self._started = True
        self.sendState()
  
    def istate(self):
        return self._istate    
        
        
#------------------------------------------------------------------------------------------------------------   
#           Functions to handle relevant incomming events 
#------------------------------------------------------------------------------------------------------------   
    
    def doHandleWeather(self, key, inEvent):
        if key == "outsideTemp":
            self._currentTemp = float(inEvent.getPayload()["val"])

    def doHandleGet(self, key, inEvent):
        if key == "rising":
            self._risingThres = float(inEvent.getPayload()["val"])
            self.doTrend()
            self.sendState()
        elif key == "falling":
            self._fallingThres = float(inEvent.getPayload()["val"])
            self.doTrend()
            self.sendState()
            
            
#------------------------------------------------------------------------------------------------------------   
#           Functions to evaluate actions based on internal states
#------------------------------------------------------------------------------------------------------------  
    def doTrend(self):
        if not None in (self._currentTemp, self._previousTemp, self._risingThres, self._fallingThres):
            if self._currentTemp > self._previousTemp:
                self._trend = 'Up'
                if self._currentTemp > self._risingThres: 
                    self._state = 'HoldOff'
                    self._istate = WEATHER_C_STATE_HOLDOFF
                else: 
                    self._state = 'Run'
                    self._istate = WEATHER_C_STATE_RUN
            else: 
                self._trend = 'Down'
                if self._currentTemp > self._fallingThres: 
                    self._state = 'HoldOff'
                    self._istate = WEATHER_C_STATE_HOLDOFF
                else: 
                    self._state = 'Run'
                    self._istate = WEATHER_C_STATE_RUN
            self.sendState()
        #Sepcial Case to create 'global/trend' this is only created by weather 0
        if self._weatherkey == '0': 
            if not None in (self._currentTemp, self._previousTemp):
                if self._currentTemp > self._previousTemp :
                    self._trend = 'Up'
                    self._tstate = 2
                elif self._currentTemp < self._previousTemp: 
                    self._trend = 'Down'
                    self._tstate = 0
                else: 
                    self._trend = 'Level'
                    self._tstate = 1
                self.sendGlobalTrend()
            
        self._previousTemp = self._currentTemp
      
#------------------------------------------------------------------------------------------------------------   
#           Functions to send/publish Events for external interaction
#------------------------------------------------------------------------------------------------------------          
     
    #does this even need to be sent out???  atm YES indirectly triggers checkRun for Zones
    def sendState(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/weather",
            "weather/%s"%self._weatherkey,
            {'state': self._state, 
                'trend': self._trend,
                'istate': self._istate, 
                } ) )
    
    def sendGlobalTrend(self):
        self._parent.sendEvent( Event("http://id.webbrick.co.uk/zones/weather",
            "weather/global",
            {'trend': self._trend, 
                'tstate': self._tstate,
                'curtemp': self._currentTemp,
                'prevtemp': self._previousTemp
                } ) )
#


#------------------------------------------------------------------------------------------------------------   
#
#           HeatingVentialtionAC class 
#
#------------------------------------------------------------------------------------------------------------ 

class HeatingVentilationAC( BaseHandler ):
    """
    This event interface is used to create a full heating, ventialtion and air conditioning solution, 
    that evaluates the demand of 'heating zones' and triggers actuators and heatsources to fullfil the 
    demand where appropriate. 

    The configuration for an HeatingVentilationAC entry is as follows:

    <eventInterface module='EventHandlers.hvac' name='HeatingVentilationAC'>
    
    </eventInterface>

        eventtype, eventsource, event, params as as per BaseHandler.
        additonally is one or more newEvent elements that define the new event to be isssued. The type and source
        attributes of the newEvent element specify the event type and source. 
        
    """

    def __init__ (self, localRouter):
        super(HeatingVentilationAC,self).__init__(localRouter)
        global _log
        _log = self._log    # make global

        self._subscribeTime = 30
        self._zones = {}
        self._zonegroups = {}
        self._heatsources = {}
        self._weathercompensation = [ 
            WeatherCompensation(self, '0'), 
            WeatherCompensation(self, '1'), 
            WeatherCompensation(self, '2'), 
            WeatherCompensation(self, '3') ]
        self._zonemaster = ZoneMaster(self)

    def start(self):
        self._log.debug( 'start' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/config/get' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/minute' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/runtime' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/weather' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/schedule/control' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/zones/manual' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/sensor' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/zone/heatsource' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/group/heatsource' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/zone' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/heatsource' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/heatsource/sensor' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/zones/zonegroup' )
        
    def stop(self):
        self._log.debug( 'stop' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/config/get' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/minute' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/runtime' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/weather' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/schedule/control' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/zones/manual' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/sensor' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/zone/heatsource' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/group/heatsource' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/zone' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/heatsource' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/heatsource/sensor' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/zones/zonegroup' )
        
    def getWCState(wc_key):
        return self._weathercompensation[wc_key].istate()
        
    def configure( self, cfgDict ):
        super(HeatingVentilationAC,self).configure(cfgDict)
        
        if cfgDict.has_key("zones"):
            for zoneCfg in cfgDict["zones"]:
                try:
                    if not zoneCfg.has_key("type") or zoneCfg["type"] == "single":
                        newZone = Zone(self, zoneCfg)
                        self._zones[newZone.zone_key()] = newZone
                    elif zoneCfg["type"] == "multi":
                        newMultiZone = MultiZone(self, zoneCfg)
                        self._zones[newMultiZone.mz_key()] = newMultiZone
                except: 
                    _log.exception("Error configuring zone %s", zoneCfg)
        
        if cfgDict.has_key("zonegroups"):
            for ZGCfg in cfgDict["zonegroups"]:
                try:
                    newZG = ZoneGroup(self, ZGCfg)
                    self._zonegroups[newZG.zg_key()] = newZG
                except: 
                    _log.exception("Error configuring zonegroup %s", ZGCfg)
            
        if cfgDict.has_key("heatsources"):
            for HSCfg in cfgDict["heatsources"]:
                try:
                    if HSCfg["type"] == "boiler":
                        newHS = HeatSourceBoiler(self, HSCfg)
                        self._heatsources[newHS.hs_key()] = newHS
                
                    elif HSCfg["type"] == "multiboiler":
                        newHS = HeatSourceMultipleBoiler(self, HSCfg)
                        self._heatsources[newHS.hs_key()] = newHS
                
                    elif HSCfg["type"] == "ground":
                        newHS = HeatSourceGround(self, HSCfg)
                        self._heatsources[newHS.hs_key()] = newHS
                    
                    elif HSCfg["type"] == "solar":
                        newHS = HeatSourceSolar(self, HSCfg)
                        self._heatsources[newHS.hs_key()] = newHS
                    
                    elif HSCfg["type"] == "multisolar":
                        newHS = HeatSourceMultiSolar(self, HSCfg)
                        self._heatsources[newHS.hs_key()] = newHS
                        # for ElevationCfg in HSCfg["elevations"]:
                            # newElevation = HeatSourceSolar(self, ElevationCfg)
                            # self._heatsources[newHS.hs_key()].addElevation(newElevation)
            
                except: 
                    _log.exception("Error configuring heatsource %s", HSCfg)
        
         
        if cfgDict.has_key("zonemaster"):    
            try:
                if int(cfgDict["zonemaster"]["active"]) == 1:
                    self._zonemaster.configure(cfgDict)
            except:
                _log.exception("Error configuring zonemaster %s", cfgDict["zonemaster"])

    def doHandleRuntime( self, inEvent ):
        od = inEvent.getPayload()
        if int(od["elapsed"]) == 10:
            for weather in self._weathercompensation:
                weather.start()
        elif int(od["elapsed"]) == 20:    
            for heatsource in self._heatsources:
                self._heatsources[heatsource].sendState()
        elif int(od["elapsed"]) == 30:
            for zone in self._zones:
                self._zones[zone].start()
                self._zones[zone].sendName()
        elif int(od["elapsed"]) == 45:
            self.sendNumberOfZones(len(self._zones))
            self.sendNumberOfZoneGroups(len(self._zonegroups))
            self.sendNumberOfHeatsources(len(self._heatsources))
            for zone in self._zones:
                self._zones[zone].sendName()
                
        elif int(od["elapsed"]) == 60:
            self.sendNumberOfZones(len(self._zones))
            self.sendNumberOfZoneGroups(len(self._zonegroups))
            self.sendNumberOfHeatsources(len(self._heatsources))
            for zone in self._zones:
                self._zones[zone].sendName()
               
        
    def doHandleMinute( self, inEvent ):
        od = inEvent.getPayload()
        curMin = od["minute"]
        for heatsource in self._heatsources: 
            self._heatsources[heatsource].checkRun(inEvent)
        for zone in self._zones: 
            self._zones[zone].checkRun()
        for zonegroup in self._zonegroups: 
            self._zonegroups[zonegroup].checkRun()
            
        if (curMin % 10) == 0:
            for wc in self._weathercompensation:
                wc.doTrend()
        self._zonemaster.sanityCheck()
             
    def doHandleGet( self, inEvent ):
        src = inEvent.getSource().split("/")
        if src[0] in self._zones:
            if src[1] == "groupnumber":
                for zonegroup in self._zonegroups:
                    self._zonegroups[zonegroup].doHandleGet(src[1], inEvent)
            else:
                self._zones[src[0]].doHandleGet(src[1], inEvent)

        elif src[0] == "weather":
            idx = int(src[1])
            self._weathercompensation[idx].doHandleGet(src[2], inEvent)

        #legacy zoneheatsource should be heatsource....             
        elif src[0] == "zoneheatsource": 
            if src[1] in self._heatsources: 
                self._heatsources[src[1]].doHandleGet(src[2], inEvent)
                
        elif inEvent.getSource() == "occupants/home":
            for zkey in self._zones:
                self._zones[zkey].setOccupied(int(inEvent.getPayload()["val"]))

        if len(src) > 2 and src[2] == "priority":
            try: 
                self._zonemaster.doHandleGet(src[2], inEvent)
            except: 
                _log.exception("ZoneMaster doHandleGet %s", inEvent)
        
    def doHandleWeather( self, inEvent ):
        src = inEvent.getSource().split("/")
        if src[1] in ["previous","global","current","outsideTemp"]:
            for wc in self._weathercompensation:
                wc.doHandleWeather(src[1], inEvent)
        else:
            w_key = int(src[1])
            for zkey in self._zones:
                self._zones[zkey].doHandleWeather(w_key)
        
    def doHandleScheduleControl( self, inEvent ):
        src = inEvent.getSource().split("/")
        if src[0] in self._zones:
            self._zones[src[0]].doHandleScheduleControl(float(inEvent.getPayload()["val"]))
        
    def doHandleManual( self, inEvent ):
        src = inEvent.getSource().split("/")
        if src[0] in self._zones:
            self._zones[src[0]].doHandleManual(float(inEvent.getPayload()["val"]))
        
    def doHandleSensor( self, inEvent ):
        src = inEvent.getSource().split("/")
        if src[0] in self._zones:
            self._zones[src[0]].doHandleSensor(float(inEvent.getPayload()["val"]))
        elif src[0] == "heatsource":
            if src[1] in self._heatsources:
                self._heatsources[src[1]].doHandleSensor(src[2], inEvent)
        
    def doHandleGroupHeatSource( self, inEvent ):
        src = inEvent.getSource().split("/")
        if src[1] in self._zonegroups:
            self._zonegroups[src[1]].doHandleHeatSource(inEvent.getPayload()["name"])
    
    def doHandleZoneHeatSource( self, inEvent ):
        src = inEvent.getSource().split("/")
        if src[0] in self._zones:
            self._zones[src[0]].doHandleHeatSource(inEvent.getPayload()["name"])
            
    def doHandleZone( self, inEvent ):
        src = inEvent.getSource().split("/")      
        if src[0] in self._zones:
            # let the zone make decsion on whether valid
            self._zones[src[0]].doHandleActuatorState(src[1])
            for zonegroup in self._zonegroups:                
                self._zonegroups[zonegroup].doState(src[0], src[1])

    def doHandleZoneGroup( self, inEvent ):
        src = inEvent.getSource().split("/") 
        if src[1] in self._zonegroups:
            self._zonegroups[src[1]].doHandleActuatorState(src[2])
            self._zonemaster.doHandleZoneGroup(src[1], src[2])

    def doHandleHeatSource(self, inEvent):
        # TODO this could be tidied up more.
        src = inEvent.getSource().split("/")
        if len(src) > 3:
            # This is a multipart heat source
            # They see the distinct running, stopped and generate the overall running/stopped events
            if src[1] in self._heatsources:
                self._heatsources[src[1]].doHandleHeatSource(src[2], src[3], inEvent)
        elif src[1] in self._heatsources:
            if src[2] in ["requestrun","requeststop"]:
                self._heatsources[src[1]].doHandleHeatSource(None, src[2], inEvent)
            elif src[2] in ["availability", "running", "stopped"]:
                self._zonemaster.doHandleHeatSource(src[2], inEvent)

    def doHandleEvent( self, handler, inEvent ):
        try: 
            
            if inEvent.getType() == 'http://id.webbrick.co.uk/zones/sensor':
                self.doHandleSensor( inEvent )

            elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/minute" :
                self.doHandleMinute( inEvent )
                
            elif inEvent.getType() == "http://id.webbrick.co.uk/zones/zone" :
                self.doHandleZone( inEvent )
                
            elif inEvent.getType() == 'http://id.webbrick.co.uk/zones/weather':
                self.doHandleWeather( inEvent )

            elif inEvent.getType() == 'http://id.webbrick.co.uk/events/schedule/control':
                self.doHandleScheduleControl( inEvent )

            elif inEvent.getType() == 'http://id.webbrick.co.uk/events/zones/manual':
                self.doHandleManual( inEvent )
            
            elif inEvent.getType() == 'http://id.webbrick.co.uk/zones/heatsource':
                self.doHandleHeatSource( inEvent )
                
            elif inEvent.getType() == 'http://id.webbrick.co.uk/zones/heatsource/sensor':
                self.doHandleSensor( inEvent )
                
            elif inEvent.getType() == 'http://id.webbrick.co.uk/zones/zone/heatsource':
                self.doHandleZoneHeatSource( inEvent )
            
            elif inEvent.getType() == 'http://id.webbrick.co.uk/zones/group/heatsource':
                self.doHandleGroupHeatSource( inEvent )

            elif inEvent.getType() == 'http://id.webbrick.co.uk/events/config/get':
                self.doHandleGet( inEvent )
            
            elif inEvent.getType() == 'http://id.webbrick.co.uk/zones/zonegroup':
                self.doHandleZoneGroup( inEvent )
            
            elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/runtime" :
                self.doHandleRuntime( inEvent )

            else:
                # unexpected 
                self._log.error( "Not expecting this event %s", inEvent.getType() )
        except Exception, ex: 
            self._log.exception(ex)

        return makeDeferred(StatusVal.OK)
        
    def sendNumberOfZones(self, count):
        self.sendEvent( Event("http://id.webbrick.co.uk/zones/zone",
            "zone/count",
            {'val': count} ) )    
        
    def sendNumberOfZoneGroups(self, count):
        self.sendEvent( Event("http://id.webbrick.co.uk/zones/zonegroup",
            "zonegroup/count",
            {'val': count} ) )    
        
    def sendNumberOfHeatsources(self, count):
        
        self.sendEvent( Event("http://id.webbrick.co.uk/zones/heatsource",
            "heatsource/count",
            {'val': count} ) )
    
# $Id: HVAC.py 3201 2009-06-15 15:21:25Z philipp.schuster $
