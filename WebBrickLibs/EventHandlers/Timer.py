# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#
#  Generic On-Off timer
#
#  Andy Harris --- 24th September 2010
#
#
#    <eventInterface  module='EventHandlers.LightTimer' name='LightTimer' >
#        <presence type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/36/DO/6' key="state" invert="true"/>
#        <duration type='http://id.webbrick.co.uk/events/config/get' source='family_bathroom_on_time' />   
#        <enable type='http://id.webbrick.co.uk/events/config/get' source='family_bathroom_on' />  
#        <hold type='http://id.webbrick.co.uk/events/webbrick/DO' source='webbrick/36/DO/4' key="state" invert="true" />  
#        
#        <eventtype type="http://id.webbrick.co.uk/events/timer" >
#            <eventsource source="family/bathroom/timer">
#                <event>
#                    <params>
#                        <testEq name="dayphase" value='*:dark' />
#                        <testEq name="occupancy" value='home,away' />
#                        <testEq name="hold" value="0" />
#                    </params>
#                    <newEvent type='internal' source='familybath/lights/tryon' >
#                        <copy_other_data/>
#                    </newEvent>
#                </event>
#            </eventsource>
#        </eventtype>
#   </eventInterface>


import logging

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from EventHandlers.Utils import *

# make logging global to module.
_log = None

CONFIG_TYPE = "http://id.webbrick.co.uk/events/config/get"



class Timer( BaseHandler ):
    """
    Timer class that subscribes to events and generates timer events
    """
    
    def __init__ (self, localRouter):
        super(Timer,self).__init__(localRouter)
        global _log
        _log = self._log    # make global

        self._debug = True  # 
        self._counter = 0   #  Will be used for counting
        self._timer_event = None
        self._light_state_event = None

        self._timer_evt_type = 'http://id.webbrick.co.uk/events/timer'
        self._timer_evt_source = self._log.name

        self._duration = 120
        self._duration_event = None
        self._enable = True
        self._enable_event = None
        self._hold = 0
        self._hold_event = None
        self._presence = -1        # -1: Unknown  0: No Presence 1: Presence Detected
        self._p_presence = -2      # -1: Unknown  0: No Presence 1: Presence Detected -2: Initial
        self._light_state = -1     # -1: Unknown  0: Off 1: On -2: Initial
        self._p_light_state = -2   # -1: Unknown  0: Off 1: On
        self._threshold = 50.0     # default to mid point
        
        self._occupancy = "Home"   # a default value
        self._isDark = 0           # a default value
        self._dayphasetext = "Unknown"  # a default value

    def start(self):
        self._log.debug( 'start' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/config/get' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/dayphaseext' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/isDark' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/second', 'time/second' )
        #
        #  Subscribe to the presence, enable and hold event type
        #
        self._localRouter.subscribe( self._subscribeTime, self, self._presence_event['type'] )
        if self._enable_event :
            self._localRouter.subscribe( self._subscribeTime, self, self._enable_event['type'] )
        if self._duration_event :
            self._localRouter.subscribe( self._subscribeTime, self, self._duration_event['type'] )
        if self._hold_event :
            self._localRouter.subscribe( self._subscribeTime, self, self._hold_event['type'] )
        if self._light_state_event :
            self._localRouter.subscribe( self._subscribeTime, self, self._light_state_event['type'] )

        self.subscribeAll()


    def stop(self):
        self._log.debug( 'stop' )
        if self._debug:
            self._log.debug ("--------- Variables Were ----------------")
            self._log.debug ("MyType %s" % str(self._timer_evt_type))    
            self._log.debug ("MySource %s" % str(self._timer_evt_source))    
            self._log.debug ("Enabled %s" % str(self._enable))    
            self._log.debug ("Duration %s" % str(self._duration))    
            self._log.debug ("Occupancy %s" % str(self._occupancy))    
            self._log.debug ("DayPhase %s" % str(self._dayphasetext))    
            self._log.debug ("Dark %s" % str(self._isDark))    
            self._log.debug ("Presence %s" % str(self._presence))    
            self._log.debug ("Light_State %s" % str(self._light_state))    
            self._log.debug ("-----------------------------------------")
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/config/get' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/dayphaseext' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/isDark' )
        self._localRouter.unsubscribe( self, self._presence_event['type'] )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/second', 'time/second' )
        if self._enable_event :
            self._localRouter.unsubscribe( self, self._enable_event['type'] )
        if self._duration_event :
            self._localRouter.unsubscribe( self, self._duration_event['type'] )
        if self._hold_event :
            self._localRouter.unsubscribe( self, self._hold_event['type'] )
        if self._light_state_event :
            self._localRouter.unsubscribe( self, self._light_state_event['type'] )

        self.unSubscribeAll()


    def configure( self, cfgDict ):
        from string import upper
        super(Timer,self).configure(cfgDict)

        self._log.debug(cfgDict)

        if cfgDict.has_key('presence'):
            self._presence_event = cfgDict['presence']
            if self._presence_event.has_key('invert'):
                if upper(self._presence_event['invert']) not in ("TRUE","1"):
                    del self._presence_event['invert']  # remove the key for a non true or 1 value
        else:
            _log.error( 'No presence event defined for Timer')

        if cfgDict.has_key('light_state'):
            self._light_state_event = cfgDict['light_state']
            if self._light_state_event.has_key('invert'):
                if upper(self._light_state_event['invert']) not in ("TRUE","1"):
                    del self._light_state_event['invert']  # remove the key for a non true or 1 value
            if self._light_state_event.has_key('threshold'):
                self._threshold = float(self._light_state_event['threshold'])


        if cfgDict.has_key('enable'):
            self._enable_event = cfgDict['enable']
        
        if cfgDict.has_key('duration'):
            self._duration_event = cfgDict['duration']

        if cfgDict.has_key('hold'):
            self._hold_event = cfgDict['hold']
            if self._hold_event.has_key('invert'):
                if upper(self._hold_event['invert']) not in ("TRUE","1"):
                    del self._hold_event['invert']  # remove the key for a non true or 1 value

        if cfgDict.has_key('eventtype'):
            if cfgDict['eventtype'].has_key('type'):
                self._timer_evt_type = cfgDict['eventtype']['type']
            
            if cfgDict['eventtype'].has_key('eventsource'):
                if cfgDict['eventtype']['eventsource'].has_key('source'):
                    self._timer_evt_source = cfgDict['eventtype']['eventsource']['source']
           
        if self._debug:
            self._log.debug ("--------- Config Debug ----------------")
            self._log.debug ("presence event %s" % str(self._presence_event))    
            self._log.debug ("duration event %s" % str(self._duration_event))    
            self._log.debug ("enable event %s" % str(self._enable_event))
            self._log.debug ("hold event %s" % str(self._hold_event))
            self._log.debug ("light_state event %s" % str(self._light_state_event))
            self._log.debug ("---------------------------------------")

    def doActions( self, actions, inEvent ):
        if actions:
            for action in actions:
                # logged in BaseHandler.sendEvent
                self._log.debug( 'Generate event %s' % ( action ) )
                self.sendEvent( makeNewEvent( action, inEvent, None ) )
                
    def configureActions( self, cfgDict ):
        self._log.debug("configureActions %s" % (cfgDict) )
        result = None
        if cfgDict.has_key("newEvent"):
            if isinstance( cfgDict["newEvent"], list ):
                result = cfgDict["newEvent"]
            else:
                result = list()
                result.append(cfgDict["newEvent"])
        self._log.debug("configureActions %s" % (result) )
        return result


    def indexTimer(self):
        if self._timer_event :
            #
            #  An event exists therefore index the counter
            #
            self._counter += 1
            if (self._counter >= self._duration):
                self.sendTimerEvent()

    def setTimerEvent(self):
        self._log.debug ("Setting Timer Event ....")
        self._timer_event = Event(self._timer_evt_type,self._timer_evt_source, {'hold': self._hold, 'occupancy': self._occupancy, 'isDark': self._isDark, 'dayphase': self._dayphasetext, 'presence': self._presence, 'light_state': self._light_state} ) 
        self._counter = 0         # reset


    def sendTimerEvent(self):
        self._log.debug ("Sending Timer Event ....")
        self._timer_event = Event(self._timer_evt_type,self._timer_evt_source, {'hold': self._hold, 'occupancy': self._occupancy, 'isDark': self._isDark, 'dayphase': self._dayphasetext, 'presence': self._presence, 'light_state': self._light_state} ) 
        self.sendEvent( self._timer_event)
        self._timer_event = None  # reset


    def doHandleConfig( self, inEvent ):
        from string import upper
        src = inEvent.getSource()
        #self._log.debug ("Found Event: %s"  % str(inEvent))
        #self._log.debug ("Handle Config Event SRC %s" % str(src))
        #
        #  Now see if this matches anything we need
        #
        if self._enable_event:
            if self._enable_event['type'] == CONFIG_TYPE:
                if self._enable_event['source'] == src:
                    en = inEvent.getPayload()['val']
                    if en == "1":
                        self._enable = True
                    if upper(en) == "TRUE":
                        self._enable = True
                    else:
                        self._enable = False
            if self._duration_event['type'] == CONFIG_TYPE:
                if self._duration_event['source'] == src:
                    self._duration = int(inEvent.getPayload()['val'])
                    
            if src == 'occupants/home':
                self._occupancy = int(inEvent.getPayload()['val'])                    


    def doHandleHold( self, inEvent ):
        #
        #  What sense is Hold in
        #
        lstate = int(inEvent.getPayload()['state'])
        if self._hold_event.has_key('invert'):
            self._log.debug ("Handle invert for hold: %s" % inEvent.getPayload()['state'])
            if lstate == 1:
                self._hold = 0
            else:
                self._hold = 1
        else:
            if lstate == 1:
                self._hold = 1
            else:
                self._hold = 0
        self._log.debug ("hold set to: %s" % self._hold)
        

    def doHandleLightState( self, inEvent ):
        self._log.debug ("Found Event for Light_State: %s"  % str(inEvent))
        #
        #  light_state may come in from a DO,AO or AI
        #  these need to be treated slightly differently
        #
        #  PREPROCESS to derive lstate
        if inEvent.getType() == 'http://id.webbrick.co.uk/events/webbrick/DO' :
            # digital Output
            lstate = inEvent.getPayload()['state']
        elif (inEvent.getType() == 'http://id.webbrick.co.uk/events/webbrick/AI') or (inEvent.getType() == 'http://id.webbrick.co.uk/events/webbrick/AI'):
            # Analogue In or Out 
            lval = inEvent.getPayload()['val']
            if float(lval) >= self._threshold :
                lstate = 1
            else:
                lstate = 0
        else:
            # not a state we recognise
            self._log.error ("Wrong Event Type for light_state: %s"  % str(inEvent))
        
        if self._light_state_event.has_key('invert'):
            if lstate == 1:
                doit = False
                self._light_state = 0
            else:
                doit = True
                self._light_state = 1
        else:
            if lstate == 1:
                doit = True
                self._light_state = 1
            else:
                doit = False
                self._light_state = 0

        if doit:        
            if not self._hold:
                if self._enable:
                    if not (self._p_light_state == self._light_state) :
                        self._log.debug ("Setting Timer due to light_state" )
                        self.setTimerEvent()
        self._p_light_state = self._light_state



    def doHandlePresence( self, inEvent ):
        lstate = int(inEvent.getPayload()['state'])
        self._log.debug ("Found Event for Presence: %s previous %s"  % (lstate, self._p_presence) )
        if self._presence_event.has_key('invert'):
            self._log.debug ("Processing Presence for invert")
            if lstate == 1:
                doit = False
                self._presence = 0
            else:
                doit = True
                self._presence = 1
        else:
            if lstate == 1:
                doit = True
                self._presence = 1
            else:
                doit = False
                self._presence = 0

        self._log.debug ("Process Presence: %s Previous %s Hold %s Enable %s"  % (self._presence, self._p_presence, self._hold, self._enable) )

        if doit:        
            if not self._hold:
                if self._enable:
                    if not (self._presence == self._p_presence):
                        self._log.debug ("Setting Timer due to Presence" )
                        self.setTimerEvent()
        self._p_presence = self._presence


    def doHandleDayPhase( self, inEvent ):
        src = inEvent.getSource()
        #self._log.debug ("Found Event: %s"  % str(inEvent))
        #self._log.debug ("Handle DayPhase Event SRC %s" % str(src))
        if src == 'time/dayphaseext':
            self._dayphasetext = inEvent.getPayload()['dayphasetext']


    def doHandleDark( self, inEvent ):
        src = inEvent.getSource()
        #self._log.debug ("Found Event: %s"  % str(inEvent))
        #self._log.debug ("Handle Dark Event SRC %s" % str(src))
        if src == 'time/isDark':
            self._isDark = inEvent.getPayload()['state']


    def doHandleEvent( self, handler, inEvent ):
    
        if inEvent.getType() == 'http://id.webbrick.co.uk/events/config/get':
            self.doHandleConfig( inEvent )
            return makeDeferred(StatusVal.OK)    
        
        elif inEvent.getType() == 'http://id.webbrick.co.uk/events/time/dayphaseext':
            self.doHandleDayPhase( inEvent ) 
            return makeDeferred(StatusVal.OK)   
        
        elif inEvent.getType() == 'http://id.webbrick.co.uk/events/time/isDark':
            self.doHandleDark( inEvent )
            return makeDeferred(StatusVal.OK)    
        
        elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/second":
            self.indexTimer()
            return makeDeferred(StatusVal.OK)

        elif inEvent.getType() == self._presence_event['type'] and inEvent.getSource() == self._presence_event['source']:
            self.doHandlePresence( inEvent )
            return makeDeferred(StatusVal.OK)    
        
        elif self._hold_event and inEvent.getType() == self._hold_event['type'] and inEvent.getSource() == self._hold_event['source']:
            self.doHandleHold( inEvent )
            return makeDeferred(StatusVal.OK)    

        elif self._light_state_event and inEvent.getType() == self._light_state_event['type'] and inEvent.getSource() == self._light_state_event['source']:
            self.doHandleLightState( inEvent )
            return makeDeferred(StatusVal.OK)    

        else: 
            return super(Timer,self).doHandleEvent( handler, inEvent)
            
