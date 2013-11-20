# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
import logging
from random import randint

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from twisted.web import client
from twisted.web.error import PageRedirect

_log = None

# ensure ntry is a list, make one of s single entry if not.
def toList( ntry ):
    if isinstance( ntry, list ):
        return ntry
    lst = list()
    lst.append(ntry)
    return lst

class Egg:
    """
    container for egg details
    """
    def __init__ (self, details):
        """
        <egg name="lower" adr="localhost:20998" 
                redChn="0" greenChn="1" blueChn="2" 
                cmdTemplate="SM%(redChn)i;%(red)i;%(greenChn)i;%(green)i;%(blueChn)i;%(blue)i;"/>
        """
        self._details = dict(details)
        self._activeSteps = dict()  # indexed by priority, list of active scenes
        self._activePriority = 0    # current highest priority
        self._activeStep = 0       # indexed to current entry in
        _log.info( 'addEgg %s' % (self._details) )

    def name( self ):
        return self._details['name']

    def addStep( self, step, pri, timeout ):
        _log.info( '%s addStep %i [%i] : %s' % (self._details['name'], pri, timeout, step) )
        # passed a scene dictionary
        if not self._activeSteps.has_key( pri ):
            self._activeSteps[pri] = list()
        self._activeSteps[pri].append( step )
        if pri > self._activePriority:
            self._activePriority = pri
            self._activeStep = 0
        _log.debug( '%s pri %i : allSteps %s' % (self._details['name'], pri, self._activeSteps[pri]) )

    def locateTopPriority( self ):
        # called when we delete all the steps in the current priority level.
        self._activePriority = 0
        for k in self._activeSteps:
            if k > self._activePriority:
                self._activePriority = k
        self._activeStep = 0
        _log.info( '%s new priority %i' % (self._details['name'], self._activePriority) )

    def deleteStep( self, step, pri ):
        # passed a scene dictionary
        _log.info( '%s deleteStep %i : %s' % (self._details['name'], pri, step) )
        if self._activeSteps.has_key( pri ):
            # locate step in self._activeSteps[pri] and remove
            # if length now 0 then calculate next priority and reset index
            for idx in range( len(self._activeSteps[pri]) ):
                stp = self._activeSteps[pri][idx]
                if stp['id'] == step['id']:
                    # found it.
                    _log.debug( 'step %s found' % (stp['id'] ) )
                    del self._activeSteps[pri][idx]
                    break;
            _log.debug( '%s pri %i : allSteps %s' % (self._details['name'], pri, self._activeSteps[pri]) )
            if len(self._activeSteps[pri]) == 0:
                # no steps left
                del self._activeSteps[pri]
                self.locateTopPriority()

    def actionSuccess( self, data, url ):
        # we do nothing with the response.
        lines = data
        _log.debug("HTTP %s success targetUrl %s %s" % (url,lines) )

    def actionError( self, failure, url ):
        if isinstance(failure.value, PageRedirect):
            _log.debug("redirect targetUrl %s", url)
        else:
            _log.error("error %s targetUrl %s", failure,url )

    def sendRequest( self, cmdStr ):
        _log.debug( 'cmdStr %s' % ( cmdStr ) )
        # send command.
        # TODO use twisted for access see HttpAction
        url = str("http://%s%s" % (self._details['adr'],cmdStr))
        client.getPage( url, followRedirect=0 ).addCallback( self.actionSuccess, url ).addErrback( self.actionError, url )

    def doNextStep( self ):
        # sends the command for the next step.
        if self._activeSteps.has_key( self._activePriority ):
            _log.debug( '%s doNextStep' % (self._details['name'] ) )
            # we have this priority
            # calulate values
            if self._activeStep >= len( self._activeSteps[self._activePriority] ) :
                self._activeStep = 0
            # we should not have empty scene but bullet proof time.
            if self._activeStep < len( self._activeSteps[self._activePriority] ) :
                stp = self._activeSteps[self._activePriority][self._activeStep]
                _log.debug( 'step %s' % ( stp ) )
                # calulate RGB
                if stp['redMin'] < stp['redMax']:
                    self._details['red'] = randint( stp['redMin'], stp['redMax'] )
                else:
                    self._details['red'] = stp['redMin']
                    
                if stp['greenMin'] < stp['greenMax']:
                    self._details['green'] = randint( stp['greenMin'], stp['greenMax'] )
                else:
                    self._details['green'] = stp['greenMin']
                    
                if stp['blueMin'] < stp['blueMax']:
                    self._details['blue'] = randint( stp['blueMin'], stp['blueMax'] )
                else:
                    self._details['blue'] = stp['blueMin']
                    
                # convert to command string
                cmdStr = self._details['cmdTemplate'] % self._details
                self.sendRequest( cmdStr )
            self._activeStep = self._activeStep + 1   # ready for next step

#
# WebBrick eggnunciate driver
#
class EggNunciate( BaseHandler ):
    """
    A EggNunciate monitors avents and sends mimic commands to a webbrick.

    The configuration for this event handler is as follows

    <eventInterface module='TestUtils' name='TestEventLogger'>
        <!-- This saves all events -->
        <eventtype type="">
            <eventsource source="" >
	        <event>
                    <!-- interested in all events -->
	        </event>
            </eventsource>
        </eventtype>
    </eventInterface>

    <eventInterface module='EggNunciate' name='EggNunciate'>

        <eventtype type="">
            <!-- setup default scene -->
            <eventsource source="time/runtime" >
	        <event>
                    <params>
                        <testEq name="elapsed">
                            <value>5</value>
                        </testEq>
                    </params>
		    <add name="defaultLow" egg="upper" pri="0" timeout="0"/>
		    <add name="defaultLow" egg="kitchen" pri="0" timeout="0"/>
		    <add name="defaultLow" egg="kitchen" pri="0" timeout="0"/>
		    <add name="defaultHigh" egg="lower" pri="0" timeout="0"/>
		    <add name="defaultHigh" egg="upper" pri="0" timeout="0"/>
		    <add name="defaultLow" egg="lower" pri="0" timeout="0"/>
	        </event>
            </eventsource>
        </eventtype>

        <eventtype type="">
            <!-- setup default scene -->
            <eventsource source="time/second" >
	        <event>
		    <next/>
	        </event>
            </eventsource>
        </eventtype>

        <eventtype type="">
            <!-- events from a source of a specific type -->
            <eventsource source="webbrick/100/DO/0" >
	        <event>
                    <params>
                        <testEq name="state">
                            <value>1</value>
                        </testEq>
                    </params>
		    <add name="garageOpenLow" egg="lower" pri="1" timeout="0"/>
		    <add name="garageOpenHigh" egg="lower" pri="1" timeout="0"/>
		    <add name="somethingActive" egg="lower" pri="1" timeout="0"/>
	        </event>
	        <event>
                    <params>
                        <testEq name="state">
                            <value>0</value>
                        </testEq>
                    </params>
		    <delete name="garageOpenLow" egg="lower" pri="1"/>
		    <delete name="garageOpenHigh" egg="lower" pri="1"/>
		    <delete name="somethingActive" egg="lower" pri="1"/>
	        </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <step id="defaultHigh" redMin="16" redMax="16" blueMin="16" blueMax="16"  greenMin="16" greenMax="16"/>
        <step id="defaultLow" redMin="8" redMax="8" blueMin="8" blueMax="8"  greenMin="8" greenMax="8"/>

        <step id="garageOpenLow" redMin="32" redMax="32" blueMin="32" blueMax="32"  greenMin="32" greenMax="32"/>
        <step id="garageOpenHigh" redMin="48" redMax="48" blueMin="48" blueMax="48"  greenMin="48" greenMax="48"/>

        <step id="somethingActive" redMin="4" redMax="4" blueMin="4" blueMax="4"  greenMin="4" greenMax="4"/>

        <!-- the cmdTemplate and adr are mandatory, the cmdTemplate will be filled using a combination of the dictionary with all
            these attributes and the red,green,blue attributes calculated for a scene -->
        <egg name="lower" adr="localhost:20998" 
                redChn="0" greenChn="1" blueChn="2" 
                cmdTemplate="SM%(redChn)s;%(red)s;%(greenChn)s;%(green)s;%(blueChn)s;%(blue)s;"/>
        <egg name="upper" adr="localhost:20998" 
                redChn="3" greenChn="4" blueChn="5" 
                cmdTemplate="SM%(redChn)s;%(red)s;%(greenChn)s;%(green)s;%(blueChn)s;%(blue)s;"/>
        <egg name="kitchen" adr="localhost:20998" 
                redChn="6" greenChn="7" blueChn="8" 
                cmdTemplate="SM%(redChn)s;%(red)s;%(greenChn)s;%(green)s;%(blueChn)s;%(blue)s;"/>

    </eventInterface>

    """

    def __init__ (self, localRouter):
        super(EggNunciate,self).__init__(localRouter)
        global _log
        _log = self._log
        self._Eggs = dict()     # keyed by egg name
        self._Steps = dict()   # keyed by scene name

    def configureActions( self, eventDict ):
        result = list()
        # TODO verify and process dictionaries
        # make sure add/delete are lists
        if eventDict.has_key( "add" ):
            lst = toList(eventDict["add"])
            for ntry in lst:
                if not ntry.has_key("timeout"):
                    ntry["timeout"] = 0 # no timeout
            result.append( ( 'add', lst ) )
        if eventDict.has_key( "delete" ):
            lst = toList(eventDict["delete"])
            result.append( ( 'delete', lst ) )
        if eventDict.has_key( "next" ):
            result.append( ( 'next', ) )
        return result

    def doCfgEgg( self, eg ):
        newEgg = Egg( eg )
        self._Eggs[newEgg.name()] = newEgg

    def doCfgStep( self, st ):
        self._Steps[st['id']] = st
        st['redMin'] = int(st['redMin'])
        st['redMax'] = int(st['redMax'])
        st['greenMin'] = int(st['greenMin'])
        st['greenMax'] = int(st['greenMax'])
        st['blueMin'] = int(st['blueMin'])
        st['blueMax'] = int(st['blueMax'])
        _log.info( 'doCfgStep %s' % (st ) )

    def configure( self, cfgDict ):
        super(EggNunciate,self).configure( cfgDict )

        # load the steps into a dictionary
        # each scene is a list of dictionaries
        if isinstance( cfgDict["step"], list ):
            for st in cfgDict["step"]:
                self.doCfgStep( st )
        else:
            self.doCfgStep( cfgDict["step"] )

        if isinstance( cfgDict["egg"], list ):
            for eg in cfgDict["egg"]:
                self.doCfgEgg( eg )
        else:
            self.doCfgEgg( cfgDict["egg"] )

    def doAddStep( self, toAdd ):
	# <add name="defaultHigh" egg="lower" pri="0" timeout="0"/>
        if self._Steps.has_key( toAdd['name']) and self._Eggs.has_key( toAdd['egg']):
            # we can add it
            self._Eggs[toAdd['egg']].addStep( self._Steps[toAdd['name']], int(toAdd['pri']), int(toAdd['timeout']))

    def doAdd( self, toAdd ):
        # toAdd is a possible list of dictionaries or a dictionary
        for nt in toAdd:
            self.doAddStep( nt )

    def doDeleteStep( self, toDelete ):
	# <delete name="defaultHigh" egg="lower" pri="0"/>
        if self._Steps.has_key( toDelete['name']) and self._Eggs.has_key( toDelete['egg']):
            # we can add it
            self._Eggs[toDelete['egg']].deleteStep( self._Steps[toDelete['name']], int(toDelete['pri']))

    def doDelete( self, toDel ):
        # toAdd is a possible list of dictionaries or a dictionary
        for nt in toDel:
            self.doDeleteStep( nt )

    def doNext( self ):
        # for each egg
        # send next scene.
        for eg in self._Eggs:
            self._Eggs[eg].doNextStep()

    def doActions( self, actions, inEvent ):

        _log.debug( 'doActions %s' % (actions) )
        for action in actions:
            try:
                if ( action[0] == "add" ):
                    self.doAdd( action[1] )

                elif ( action[0] == "delete" ):
                    self.doDelete( action[1] )

                elif ( action[0] == "next" ):
                    # we need to handle this on the reactor thread as it will
                    # make network calls twisted is not thread safe!
                    # defer import to here so we can install alternate reactors.
                    from twisted.internet import reactor
                    reactor.callFromThread( self.doNext )

            except Exception, ex:
                _log.exception( "doActions %s" % str(action) )
