#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import logging

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from Utils import makeNewEvent

from WebBrickLibs.ParameterSet import ParameterSet

_log = None

class ACompound:
    def __init__( self, eventDict ):
        self._values = ParameterSet( eventDict["params"] )
        self._events = None
        self._state = None
        # do we want to reevaluate self on any of our events even if not changed
        self._alwaysReDo = eventDict.has_key( "redo" ) and (eventDict["redo"] == 'yes')

        if eventDict.has_key( "newEvent" ):
            if isinstance( eventDict["newEvent"], list ):
                self._events = eventDict["newEvent"]
            else:
                self._events = list()
                self._events.append( eventDict["newEvent"] )
            # TODO Validate newEvent data structure, suggest utility helper so can be used elsewhere
        if eventDict.has_key( "newState" ):
            if isinstance( eventDict["newState"], list ):
                self._state = eventDict["newState"]
            else:
                self._state = list()
                self._state.append( eventDict["newState"] )

    def uses( self, name ):
        """ quick check on whether a change means we should be scanned """
        return self._values.uses( name )

    def match( self, allValues ):
        """ allValues is a complete dictionary of name value pairs """
        return self._values.match( allValues )

    def keys(self):
        return self._values.keys()

    def events(self):
        return self._events

    def state(self):
        return self._state

    def __str__(self):
        return "ParameterSet %s Events %s StateUpdates %s" % ( self._values, self._events, self._state )

#
# WebBrick time event generator
#
class Compound( BaseHandler ):
    """
    A compound event generates new events based on the status of other events.

    The configuration for this event handler is as follows

            <eventInterface module='Compound' name='Compound'>
                <!-- The events are used to set name/value pairs.
                    The action's part can have two variants. Both have the name attribute.
                    One has a value attribute to make the name/value pair.
                    The other has a param attribute which names one of the events other_data components.
                    This impies that other_data is a dictionary object.
                    Multiple actions can be given.
                 -->
                <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
                    <!-- events from a source of a specific type -->
                    <eventsource source="webbrick/100/DI/0" >
	                <event>
                            <params>
                                <state>0</state>
                            </params>
		            <action name="Sensor1" value="0"/>
	                </event>
	                <event>
                            <params>
                                <state>1</state>
                            </params>
		            <action name="Sensor1" value="1"/>
	                </event>
                    </eventsource>
                    <eventsource source="webbrick/100/DI/1" >
	                <event>
		            <action name="Sensor2" key="state"/>
	                </event>
                    </eventsource>
                    <eventsource source="webbrick/100/DI/1" >
	                <event>
		            <action name="Sensor2" key="state"/>
	                </event>
                    </eventsource>
                    <eventsource source="webbrick/100/TD/7" >
	                <event>
		            <action name="AnInput" value="do" transient/>
	                </event>
                    </eventsource>
                </eventtype>
                <initialState name="aName" value="aValue"/>

                <!-- The second part of the configuration uses the name value pairs to 
                    specify new events to be generated. -->
                <compound>
                    <params>
                        <Sensor1>=0</Sensor1>
                        <Sensor2>=0</Sensor2>
                    </params>
                    <newEvent type="http://simple" source="garage1/Error">
                    <newState name="AName" value="newValue">
                </compound>
                <compound>
                    <params>
                        <Sensor1>=0</Sensor1>
                        <Sensor2>=1</Sensor2>
                    </params>
                    <newEvent type="http://simple" source="garage1/Open">
                </compound>
                <compound>
                    <params>
                        <Sensor1>=1</Sensor1>
                        <Sensor2>=0</Sensor2>
                    </params>
                    <newEvent type="http://simple" source="garage1/Closed">
                </compound>
                <compound>
                    <params>
                        <Sensor1>=1</Sensor1>
                        <Sensor2>=1</Sensor2>
                    </params>
                    <newEvent type="http://simple" source="garage1/Ajar">
                </compound>
                <--  thoughts for future, use explicitly named elements for tests -->
                <compound>
                    <params>
                        <testEq name="Sensor1"><value>1</value></testEq>
                        <testNe name="Sensor1"><value>1</value></testNe>
                        <testGt name="Sensor1"><value>1</value></testGt>
                        <testGe name="Sensor1"><value>1</value></testGe>
                        <testLt name="Sensor1"><value>1</value></testLt>
                        <testLe name="Sensor1"><value>1</value></testLe>
                    </params>
                    <newEvent type="http://simple" source="garage1/Ajar">
                </compound>

            </eventInterface>

    """

    def __init__ (self, localRouter):
        super(Compound,self).__init__(localRouter)
        global _log
        _log = self._log
        self._values = dict()   # the name value pairs
        self._compounds = list()

    def configureActions( self, eventDict ):
        result = list()
        if eventDict.has_key( "action" ):
            if isinstance( eventDict["action"], list ):
                result = eventDict["action"]
            else:
                result.append( eventDict["action"] )
        return result

    def configure( self, cfgDict ):
        super(Compound,self).configure( cfgDict )
        if isinstance( cfgDict["compound"], list ):
            for cmp in cfgDict["compound"]:
                # extract name/value pairs
                # load new event
                ne = ACompound(cmp)
                self._compounds.append( ne )
                self._log.debug( "compound %s" % ne )
        else:
            ne = ACompound(cfgDict["compound"])
            self._compounds.append( ne )
            self._log.debug( "compound %s" % ne )

        # preload all values as blank, i.e. not known.
        for cmp in self._compounds:
            # values() is a dictionary
            self._log.debug( "compound %s" % ne )
            for nv in cmp.keys():
                self._values[nv] = ""
                
        # now set initial values
        if cfgDict.has_key( "initialState" ):
            if isinstance( cfgDict["initialState"], list ):
                for init in cfgDict["initialState"]:
                    self._values[init["name"]] = init["value"]
            else:
                # only one inital state entry.
                self._values[cfgDict["initialState"]["name"]] = cfgDict["initialState"]["value"]
                
        # now set initial values
        if cfgDict.has_key( "persistState" ):
            self._log.error( "persistState not supported %s" % ( cfgDict ) )

    def doUpdate( self, name, value, transient = False ):
        """
        Update the state and check for conditions to be performed.
        """
        
        # We may want to recheck the compounds every time the event arrives or only when it changes.
        # This may need to be compound specific.
        valueChanged = not self._values.has_key(name) or self._values[name] <> value
        
        self._log.debug( "update %s : %s %s" % ( name, value, transient ) )
        self._values[name] = value
        
        return valueChanged
    
    def stringSub(self,oldPayload,string):
        newString = string
        if oldPayload != '':     
            if '%' in string:
                newString = string % oldPayload
        return newString
                   
    def doActions( self, actions, inEvent ):
        #self._log.debug( "doActions %s : %s" % ( actions, inEvent ) )
        od = inEvent.getPayload()
        
        # first do all updates
        newEvents = list()
        updated = dict() # keys are updated values, content is whether value changed.
        for action in actions:
            variableName = self.stringSub(inEvent.getPayload(),action["name"])
            if action.has_key("value"):
                # has value
                updated[variableName] = self.doUpdate( variableName, action["value"], action.has_key("transient") )
            elif od.has_key( action["key"] ):
                # has key
                updated[variableName] = self.doUpdate( variableName, od[ action["key"] ], action.has_key("transient") )
        #self._log.debug( "doActions %s" % ( self._values ) )

        # then check the compounds.
        # TODO may be need to reevaluate the compounds based on the newState updates.
        #
        for cmp in self._compounds:
            # test to see whether we always retest compound even if no change in value
            for key in updated:
                if cmp.uses(key) and (updated[key] or cmp._alwaysReDo):
                    #self._log.debug( "cmp uses %s : %s (%s)" % ( name, cmp, str(self._values) ) )
                    if cmp.match(self._values):
                        self._log.debug( "compound matches %s" % ( cmp ) )
                        if cmp.state():
                            for ns in cmp.state():
                                if ns.has_key("value"):
                                    self._values[ns["name"]] = ns["value"]
                                elif ns.has_key("key"):
                                    # update from event or localstate
                                    if self._values.has_key(ns["key"]):
                                        self._values[ns["name"]] = self._values[ns["key"]]
                                    elif od and od.has_key(ns["key"]):
                                        self._values[ns["name"]] = od[ns["key"]]
                                else:
                                    # error
                                    self._log.error( "newState missing value or key2 %s" % ( ns ) )
                        if cmp.events():
                            for ne in cmp.events():
                                #pass in incoming event so we can support string substitution in our variable names
                                newEvents.append( makeNewEvent( ne, inEvent, self._values ) )
                    # and then break from for loop.
                    break
            
        # finally remove transients
        for action in actions:
            # may of allready been deleted?
            if action.has_key("transient") and self._values.has_key(action["name"]):
                del self._values[action["name"]]

        for evnt in newEvents:
            self.sendEvent( evnt )
