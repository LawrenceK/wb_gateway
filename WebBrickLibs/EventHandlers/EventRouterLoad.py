# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: EventRouterLoad.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
import sys, logging, string
from os import listdir
from os.path import isdir, exists

from MiscLib.DomHelpers import parseXmlFile, getDictFromXml

from EventLib.EventRouter import EventPubSub, EventRouter
from EventLib.EventRouterThreaded import EventRouterThreaded

_log = logging.getLogger( "EventHandlers.EventRouterLoad" )

def mEnabled( m ):
    # is this m enabled
    # look in cherrypy config - prod.cfg
    import turbogears
    cfgStr = turbogears.config.get(m, "true", False, "eventhandlers" )
    if isinstance(cfgStr,basestring):
        cfgStr = cfgStr.lower()
        return cfgStr == "true" or cfgStr == "1"
    elif isinstance(cfgStr,bool):
        return cfgStr
    elif isinstance(cfgStr,int):
        return cfgStr != 0
    return True

class EventRouterLoader(object):

    def __init__( self ):
        # TODO select event router at load time.
        self._interfaces = []
        self._eventRouters = {}

    def loadRouter( self, cfgDict ):
        rtype = "EventRouterThreaded"
        rname = "default"
        if cfgDict.has_key("eventRouter"):
            rdict = cfgDict["eventRouter"]
            if rdict.has_key("type"):
                rtype = rdict["type"]
            if rdict.has_key("name"):
                rname = rdict["name"]
        if not self._eventRouters.has_key(rname):
            if rtype == "EventRouter":
                self._eventRouters[rname] = EventRouter()
            elif rtype == "EventPubSub":
                self._eventRouters[rname] = EventPubSub()
            elif rtype == "EventRouterThreaded":
                self._eventRouters[rname] = EventRouterThreaded()
            elif rtype == "EventRouterHTTPS":
                self._eventRouters[rname] = EventRouterHTTPS()
            elif rtype == "EventRouterHTTPC":
                self._eventRouters[rname] = EventRouterHTTPC()
            else:
                self._eventRouters[rname] = EventRouterThreaded()
            _log.debug( 'loadRouter %s' % (self._eventRouters) )
        return self._eventRouters[rname]

    def loadHandlers( self, cfgDict ):
        """
        called with a dictionary that contains the configuration for the task
        """
        errCount = 0
        _log.debug( 'configuration %s' % (cfgDict) )
        thisRouter = self.loadRouter( cfgDict )

        # This jiggery pockery is so that we can be called with top level?
        # short term fix.
        eis = None
        if cfgDict.has_key("eventInterfaces"):
            eis = cfgDict["eventInterfaces"]
        else:
            # in case nested.
            if cfgDict.has_key("eventRouter"):
                eis = cfgDict["eventRouter"]["eventInterfaces"]

        if eis and isinstance( eis, list ):
            for eiCfg in eis:
                try:
                    # dynamic load.
                    if mEnabled(eiCfg["module" ]):
                        _log.debug( 'attempting to load %s from %s' %(eiCfg["name"], eiCfg["module" ]) )
                        newModule = __import__( eiCfg["module" ], globals(), locals(), [eiCfg["name"]] )
                        ei = getattr( newModule, eiCfg["name"] )(thisRouter )
                        try:
                            _log.info( '%s loaded %s from %s' %(ei.getUri(), eiCfg["name"], eiCfg["module" ]) )
                            ei.configure( eiCfg )
                            self._interfaces.append(ei)
                        except Exception, ex:
                            _log.exception( 'error configuring %s' % (eiCfg) )
                            errCount = errCount + 1
                    else:
                        # intentionally at debug level.
                        _log.debug( 'not enabled %s', eiCfg["module" ])

                except Exception, ex:
                    _log.exception( 'error loading %s from %s' %(eiCfg["name"], eiCfg["module" ]) )
                    errCount = errCount + 1

        else:
            _log.error( 'No event interfaces in %s' % (cfgDict,) )

        return errCount

    def loadFromFile( self, fileName ):
        """
        Load any handlers specified in the file.
        """
        errCount = 0

        if fileName.endswith( ".xml" ):
            _log.info( "load from file %s" % fileName )
            try:
                xmlDom = parseXmlFile( fileName )
                cfgDict = getDictFromXml( xmlDom )
                thisCount = self.loadHandlers( cfgDict )
                if thisCount > 0:
                    errCount = errCount + thisCount
                    _log.error( "Error configuring event routing using %s" % (fileName) )
            except Exception, ex :
                _log.exception( "Error in %s" % (fileName) )
                errCount = errCount + 1
        return errCount

    def loadFromDirectories( self, dirList ):
        """
        For each entry in dirList,
        If the directory exists and there is one or more configuration files then use them 
        to configure event routing.
        """
        errCount = 0
        if isinstance( dirList, basestring):
            dirList = string.split(dirList, ":")

        for dir in dirList:
            if isdir( dir ):
                _log.debug( "%s is a directory" % dir )
                cfgFiles = listdir( dir )
                if cfgFiles and len(cfgFiles) > 0 :
                    for fil in cfgFiles:
                        if fil.endswith( ".xml" ):
                            errCount += self.loadFromFile( "%s/%s" % (dir, fil) )
                        
        if errCount:
            _log.error( "%i Error(s) configuring despatch" % (errCount) )

    def start( self ):
        _log.debug( 'start' )
        for ei in self._interfaces:
            ei.start()
    
    def stop( self ):
        for ei in self._interfaces:
            try:
                ei.stop()
            except Exception, ex:
                _log.exception( ex )

        for rtr in self._eventRouters:
            self._eventRouters[rtr].close()

    def getEventRouter( self, name="default" ):
        return self._eventRouters[name]
