#
#  Class to handle mapping of an event to one or more new events
#
#  Lawrence Klyne
#
#
import logging

from EventLib.Event import Event, makeEvent

from EventLib.EventAgent import EventAgent
from EventLib.EventHandler import EventHandler

from EventHandlers.BaseHandler import BaseHandler
from EventHandlers.Utils import *

from WebBrickLibs.ParameterSet import ParameterSet

#
# WebBrick time event generator
#
class EventMapper( BaseHandler ):
    """
    A job is a set of events to send. This can also be analogous to a scene in that the job name 
    could be Scene1 and the targets are a set of lights to be switched. This also enables you
    to do simple aliasing.

    The configuration for an evMapper entry is as follows:

    <eventInterface module='EventMapper' name='EventMapper'>
        <eventtype type="http://id.webbrick.co.uk/events/webbrick/TD">
            <eventsource source="webbrick/100/TD/0" >
	        <event>
                    <params>
                    </params>
                    <newEvent type="local/url" source="local/HwOn">
                        <other_data val1="1"/>
                        <copy_other_data state="state"/>
                    </newEvent>
	        </event>
            </eventsource>
            <eventsource source="webbrick/100/TD/7" >
	        <event>
                    <params>
                    </params>
                    <newEvent type="local/url" source="local/NotToBeTriggerred">
                        <other_data val1="7"/>
                        <copy_other_data state="state"/>
                    </newEvent>
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

        eventtype, eventsource, event, params as as per BaseHandler.
        additonally is one or more newEvent elements that define the new event to be isssued. The type and source
        attributes of the newEvent element specify the event type and source. 
        
        The newEvent element may contain:
        an other_data element which specifies constant name value pairs for the other data in the new event.
        a copy_other_data element which is used to control copying of other_data attributes from the original event,
        within this each attribute name is used as an attribute name fro the new event and the attribute value 
        specifies an attribute name within the original event. This enables identity mapping or name changing.
    
    """

    def __init__ (self, localRouter):
        super(EventMapper,self).__init__( localRouter )

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

    def doActions( self, actions, inEvent ):
        if actions:
            for action in actions:
                # logged in BaseHandler.sendEvent
                #self._log.debug( 'Generate event %s' % ( action ) )
                self.sendEvent( makeNewEvent( action, inEvent, None ) )

