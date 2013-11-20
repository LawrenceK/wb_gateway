#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Lawrence Klyne
#
#
import logging

from WbEvent import WbEvent, WbEventOther
from ParameterSet import ParameterSet

_log = logging.getLogger( "EventDespatch.WbEvBaseAction" )

def loadNameValuePairs( xmlDom ):
    params = None
    paramElem = getNamedElem(xmlDom, "params")
    if ( paramElem ) :
        params = dict()
        # There are parameters.
        for param in paramElem.childNodes:
            if param.nodeType == param.ELEMENT_NODE:
                isList = getAttrText(param, "type") == "list"
                txt = getElemText(param)
                self._log.debug( 'param %s %s - %s ' % (isList, param.tagName, txt) )
                # for each element in param create param entry
                if isList:
                    params[param.tagName] = txt.split(',')
                else:
                    params[param.tagName] = txt
    return params

def makeNewEvent( desc, oldEvent, xtra ):
    """
    Create a new event using the description in desc.
    The desc is a dictionary containing an event type and event source
    It may also contain
        initial other_data
        a command to copy data for the event other data from oldEvent or xtra
    oldEvent is the other_data from an existing event
    xtra is a dictionary of values from an arbitrary source.
    """
    newOd = None
    if desc.has_key("other_data"):
        newOd = dict(desc["other_data"])
    else:
        newOd = dict()  # empty.

    if desc.has_key("copy_other_data"):
        cpList = desc["copy_other_data"]
        for key in cpList:
            if xtra and xtra.has_key( cpList[key] ):
                newOd[key] = xtra[ cpList[key] ]
            elif oldEvent and oldEvent.has_key( cpList[key] ):
                newOd[key] = oldEvent[ cpList[key] ]

    # may be empty.
    if newOd and len(newOd) == 0:
        newOd = None

    return WbEventOther( desc["type"], desc["source"], newOd )

def validateNewEvent( desc ):
    """
    Validate the content of a new event description and log errors is invalid
    return True if valid else False
    It may also contain
        initial other_data
        a command to copy data for the event other data from oldEvent or xtra
    oldEvent is the other_data from an existing event
    xtra is a dictionary of values from an arbitrary source.
    """
    result = True
    errStr = ""
    if not desc.has_key("type"):
        result = False
        errStr.append( "no event type" )
    if not desc.has_key("source"):
        result = False
        errStr.append( "no event source" )

    if desc.has_key("other_data"):
        # other data should be a dictionary of name value pairs.
        od = desc["other_data"]
        if not isinstance( od, dict ):
            result = False
            errStr.append( "other data is not a dictionary (name value pairs)" )
        else:
            # what other tests
            pass

    if desc.has_key("copy_other_data"):
        # should be a sequence type, define better
        pass

    if not result:
        _log.error("newEvent invalid %s (%s)" % (errStr,desc) )

    return result

#
# WebBrick base for event interfaces
#
class WbEvBaseAction:
    """
    Base event handler for the despatch task.

    This is configured using a dictionary that contains the following entries:
        'name': name of class, used by DespatchTask for dynamic loading.
        'module': name of oython module, used by DespatchTask for dynamic loading.
        'category' : optional may be used when multiple copies of a handler are loaded.
        'eventtype': the event type or types the handler is interested in. This is a dictionary or a list of dictionaries.
            each 'eventtype' contains
                'type' : event type handled
                'eventsource' : the event source or sources for the event type we are interested in. This is a dictionary or a list of dictionaries.
                    each eventsource contains
                        'source': the name of the event source
                        'event': one or more possible configurations for the type and source
                            each 'event' may contain
                                'params' a dictionary of name value pairs that are matched against the other_data in an event
                                handler specific entries.

        for example:
        {'name': 'WbEvBaseAction',
         'modulename':'WbEvBaseAction',
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

        <EventInterface name='WbEvBaseAction' modulename='WbEvBaseAction' category='Generic'>
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

    def __init__ (self, despatch):
        # no extra config as yet.
        self.__running = False
        # this is a 3 level structure.
        # dictionary (key - type) of dictionaries (key - source) of lists(events)
        self._typeConfig = dict()
        self._despatch = despatch
        pass

    def __str__(self):
        return "%s %s" % ( __name__, self._typeConfig )

    def configureActions( self, eventDict ):
        """
        must be implemented by derived class. returns an actions entity that
        is passed to doActions.
        """
        pass

    def subscribeAll( self ):
        for typeStr in self._typeConfig:
            for sourceStr in self._typeConfig[typeStr]:
                self._log.debug( '%s:%s actions "%s" ' %(typeStr, sourceStr, self._typeConfig[typeStr][sourceStr]) )
                self._despatch.subscribe( self, typeStr, sourceStr, 0 )

    def configureEvent( self, eventDict ):
        paramSet = None
        actions = None
        if isinstance( eventDict, dict ):
            actions = self.configureActions( eventDict )
            if eventDict.has_key( "params" ):
                params = eventDict["params"]
                if len(params) > 1 or ( len(params) == 1 and not params.has_key('') ):
                    paramSet = ParameterSet( params )

#                # ensure we do not have blank key or params with no entries in it.
#                if params.has_key(''):
#                    del params['']
#                if len(params) <= 0:
#                    params = None

        return ( (paramSet, actions) )

    def configureSource( self, sourceDict ):
        """
        called with a dictionary that contains the configuration for a single event source
        """
        # sourceDict is an eventSource
        # we look for events, each event may have parameters
        # we return a list of events, an event is a tuple of params and actions
        eventList = list()

        # if sourceDict.has_key("event"):
        if isinstance( sourceDict[ "event" ], list ):
            # enumerate list of dictionaries
            for ntry in sourceDict[ "event" ]:
                eventList.append( self.configureEvent( ntry ) )
        else:
            # otherwise sourceDict[ "event" ] shoudl be a dictionary
            eventList.append( self.configureEvent( sourceDict[ "event" ] ) )
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
        called with a dictiopnary that contains the configuration for self
        """
        # cfgDict is an eventInterface
        self._category = cfgDict["name"]
        if cfgDict.has_key("category"):
            self._category = cfgDict["category"]
#        self._log.debug( 'configure start for %s ' % self._category )

        # if cfgDict.has_key("eventtype"):
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
        pass

    def sendEvent( self, inEvent ):
        self._log.debug( 'Handler Generates event %s' % ( inEvent ) )
        self._despatch.handleEvent( inEvent )

    def handleEvent( self, inEvent ):
#        self._log.debug( 'handleEvent %s' % inEvent )
        try:
            # Any match on event type.
            typeDict = None
            if self._typeConfig.has_key( inEvent.type() ):
                typeDict = self._typeConfig[ inEvent.type() ]
            elif self._typeConfig.has_key( "" ):
                typeDict = self._typeConfig[ "" ]

            if typeDict:
                #self._log.debug( 'typeDict %s' % ( typeDict ) )
                # Any match on event source.
                source = None
                if typeDict.has_key( inEvent.source() ):
                    source = typeDict[inEvent.source()]
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
                            isMatched = paramSet.match( inEvent.other_data() )
#                            if inEvent.other_data():
#                                self._log.debug( 'paramSet %s' % ( paramSet ) )
#                                for p in paramDict:
#                                    # if all paramaters match the inEvent parameters
#                                    if inEvent.other_data().has_key(p):
#                                        toMatch = paramDict[p]
#                                        if isinstance( toMatch, list ):
#                                            isMatched = unicode(inEvent.other_data()[p]) in toMatch
#                                        else:
#                                            isMatched = unicode(inEvent.other_data()[p]) == unicode(toMatch)
#                                        if not isMatched:
#                                            break # skip rest of loop, mismatch
#                                    else:
#                                        isMatched = False
#                                        break # skip rest of loop, mismatch
#                            else:
#                                isMatched = False # event does not have parameters
#                            # for p in paramDict:

                        if isMatched:
                            self._log.info( 'Handler Matches %s' % (eventEntry,) )
                            try:
                                self.doActions( eventEntry[1], inEvent )
                            except Exception, ex:
                                self._log.exception( ex )
                        # not matched this time.
                    # for eventEntry in typeDict[ inEvent.type() ]:

        except Exception, ex:
            self._log.exception( ex )
