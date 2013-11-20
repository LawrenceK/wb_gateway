# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Lawrence Klyne
#
#
import logging

from EventLib.Event import Event, makeEvent
from EventLib.EventAgent import EventAgent
from EventLib.EventHandler import EventHandler

from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from WebBrickLibs.ParameterSet import ParameterSet

handlerIdx = 0
def makeUri( cls ):
    global handlerIdx
    handlerIdx = handlerIdx + 1
    pfx = "%s.%u" % ( cls.__module__, handlerIdx)
    uri = "http://id.webbrick.co.uk/%s" % (pfx.replace(".","/"))
    return (uri, pfx)

#
# WebBrick base for event interfaces
#
class BaseHandler(EventHandler):
    """
    Base event handler for the despatch task.

    This is configured using a dictionary that contains the following entries:
        'name': name of class, used by DespatchTask for dynamic loading.
        'module': name of oython module, used by DespatchTask for dynamic loading.
        'category' : optional may be used when multiple copies of a handler are loaded.
        'eventtype': the event type or types the handler is interested in. This is a dictionary or a list of dictionaries.
            each 'eventtype' contains
                'type' : event type handled
                'eventsource' : the event source or sources for the event type we are interested in.
                This is a dictionary or a list of dictionaries.
                    each eventsource contains
                        'source': the name of the event source
                        'event': one or more possible configurations for the type and source
                            each 'event' may contain
                                'params' a dictionary of name value pairs that are matched against the other_data in an event
                                handler specific entries.

        for example:
        {'name': 'BaseHandler',
         'modulename':'BaseHandler',
         'category': 'Generic'
         'eventtype': [ 
            { 'type': 'http://id.webbrick.co.uk/events/time/minute',
              'eventsource': [
                { 'source': 'time',
                  'event': [ 
                    { 'params': { 'minutes': '0' }
                      ...handler specific entries.
                    } ]
                } ]
            } ]
        }

        When configured from XML, using the loadDictFromXml functions. The XML is like this.

        <EventInterface name='BaseHandler' modulename='BaseHandler' category='Generic'>
            <eventtype type='http://id.webbrick.co.uk/events/time/minute'>
                <eventsource source='time'>
                    <event>
                        <params>
                            <minutes>0</minutes>
                            <!-- handler specific entries. -->
                        </params>
                    </event>
                </eventsource>
            <eventtype>
        </EventInterface>
    """

    def __init__ (self, localRouter):
        # generate a URI and logname
        uri,logname = makeUri(self.__class__)
        self._log = logging.getLogger( logname )
        EventHandler.__init__(self, uri, self.doHandleEvent)
        # no extra config as yet.
        self.__running = False
        # this is a 3 level structure.
        # dictionary (key - type) of dictionaries (key - source) of lists(events)
        self._typeConfig = dict()
        self._localRouter = localRouter
        self._subscribeTime = 30

    def __str__(self):
        return "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
#        return "%s %s" % ( __name__, self._typeConfig )

    def configureActions( self, eventDict ):
        """
        must be implemented by derived class. returns an actions entity that
        is passed to doActions.
        """
        self._log.debug( 'configureActions not Implemented %s' % ( eventDict ) )

    def subscribeAll( self ):
        if self._localRouter:
            for typeStr in self._typeConfig:
                for sourceStr in self._typeConfig[typeStr]:
                    self._log.info( '%s:%s actions "%s" ' %(typeStr, sourceStr, self._typeConfig[typeStr][sourceStr]) )
                    self._localRouter.subscribe( self._subscribeTime, self, typeStr, sourceStr )

    def unSubscribeAll( self ):
        if self._localRouter:
            for typeStr in self._typeConfig:
                for sourceStr in self._typeConfig[typeStr]:
                    self._log.debug( '%s:%s actions "%s" ' %(typeStr, sourceStr, self._typeConfig[typeStr][sourceStr]) )
                    self._localRouter.unsubscribe( self, typeStr, sourceStr )

    def configureEvent( self, cfgEvent ):
        paramSet = None
        actions = None
        if isinstance( cfgEvent, dict ):
            actions = self.configureActions( cfgEvent )
            if cfgEvent.has_key( "params" ):
                params = cfgEvent["params"]
                if len(params) > 1 or ( len(params) == 1 and not params.has_key('') ):
                    paramSet = ParameterSet( params )
        return ( (paramSet, actions) )

    def configureSource( self, cfgSource ):
        """
        called with a dictionary that contains the configuration for a single event source
        """
        # sourceDict is an eventSource
        # we look for events, each event may have parameters
        # we return a list of events, an event is a tuple of params and actions
        eventList = list()

        # if sourceDict.has_key("event"):
        if isinstance( cfgSource[ "event" ], list ):
            # enumerate list of dictionaries
            for ntry in cfgSource[ "event" ]:
                eventList.append( self.configureEvent( ntry ) )
        else:
            # otherwise sourceDict[ "event" ] shoudl be a dictionary
            eventList.append( self.configureEvent( cfgSource[ "event" ] ) )
        return eventList

    def configureType( self, cfgDict ):
        """
        called with a dictionary that contains the configuration for a single type.
        """
        # cfgDict is an eventType
        # Do we already have this type.
        if not self._typeConfig.has_key( cfgDict['type'] ):
            self._typeConfig[cfgDict['type']] = dict()  # no
        srcDict = self._typeConfig[cfgDict['type']]

        # if cfgDict.has_key("eventsource"):
        if isinstance( cfgDict[ "eventsource" ], list ):
            # enumerate list of dictionaries
            for ntry in cfgDict[ "eventsource" ]:
                nevents = self.configureSource( ntry )
                if srcDict.has_key(ntry['source']):
                    for evt in nevents:
                        srcDict[ntry['source']].append(evt)
                else:
                    srcDict[ntry['source']] = nevents
        else:
            # otherwise cfgDict[ "eventsource" ] shoudl be a dictioanry
            nevents = self.configureSource( cfgDict[ "eventsource" ] )
            if srcDict.has_key(cfgDict[ "eventsource" ]['source']):
                for evt in nevents:
                    srcDict[cfgDict[ "eventsource" ]['source']].append(evt)
            else:
                srcDict[cfgDict[ "eventsource" ]['source']] = nevents

    def configure( self, cfgDict ):
        """
        called with a dictionary that contains the configuration for self
        """
        # cfgDict is an eventInterface
        self._category = cfgDict["name"]
        if cfgDict.has_key("category"):
            self._category = cfgDict["category"]

        # some handlers do not have any extra configuration 
        if cfgDict.has_key("eventtype"):
            if isinstance( cfgDict[ "eventtype" ], list ):
                # enumerate list
                for ntry in cfgDict[ "eventtype" ]:
                    self.configureType( ntry )
            else:
                self.configureType( cfgDict[ "eventtype" ] )

    # Terminate interface
    def stop(self):
        self._log.debug( 'stop' )
        self.__running = False
        self.unSubscribeAll()

    def start(self):
        self._log.debug( 'start' )

        # let event despatch know we are interested
        self.subscribeAll()

        self.__running = True

    def alive(self):
        return self.__running

    def doActions( self, actions, inEvent ):
        """
        must be implemented by derived class. Passed the actions list generated
        by configuraActions
        """
        self._log.debug( 'doActions not Implemented %s %s' % ( actions, inEvent ) )

    def sendEvent( self, inEvent ):
        self._log.debug( "Handler Generates event '%s' '%s' '%s'", inEvent.getType(), inEvent.getSource(), inEvent.getPayload() )
        if self._localRouter:
            try:
                self._localRouter.publish( inEvent.getSource(), inEvent )
            except Exception, ex:
                self._log.exception( "Error in publishing event %s", (inEvent) )

    def doHandleEvent( self, handler, inEvent ):
        # note handler should be self.
#        self._log.debug( 'handleEvent %s' % inEvent )
        try:
            # Any match on event type.
            typeDict = None
            if self._typeConfig.has_key( inEvent.getType() ):
                typeDict = self._typeConfig[ inEvent.getType() ]
            elif self._typeConfig.has_key( "" ):
                typeDict = self._typeConfig[ "" ]

            if typeDict:
                #self._log.debug( 'typeDict %s' % ( typeDict ) )
                # Any match on event source.
                source = None
                if typeDict.has_key( inEvent.getSource() ):
                    source = typeDict[inEvent.getSource()]
                elif typeDict.has_key( "" ):
                    source = typeDict[""]

                if source:
                    #self._log.debug( 'source %s' % ( source ) )
                    # Look through all possible event targets.
                    for eventEntry in source:
                        # now match params.
                        # basically anything in the param 
                        paramSet = eventEntry[0]
                        isMatched = True # in case no parameters
                        if ( paramSet ):   # if no parameters assume match
                            isMatched = paramSet.match( inEvent.getPayload() )

                        if isMatched:
                            self._log.debug( 'Handler Matches %s' % (eventEntry,) )
                            try:
                                self.doActions( eventEntry[1], inEvent )
                            except Exception, ex:
                                self._log.exception( ex )
                        # not matched this time.
                    # for eventEntry in typeDict[ inEvent.type() ]:

        except Exception, ex:
            self._log.exception( ex )

        return makeDeferred(StatusVal.OK)
