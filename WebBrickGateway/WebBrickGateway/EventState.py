# $Id: EventState.py 2753 2008-09-18 14:42:13Z lawrence.klyne $

import turbogears
import cherrypy
import logging
import string

from EventLib.Event         import Event
from EventLib.Status        import StatusVal
from EventLib.SyncDeferred  import makeDeferred

from EventLib.EventHandler  import EventHandler

# --------------------------------------------------
# WebBrick command and status access class
# --------------------------------------------------

_log = logging.getLogger( "WebBrickGateway.EventState" )

class EventState( EventHandler ):
    """
    Local class to handle requests for contents of events
    """

    def __init__(self):
        super(EventState,self).__init__("http:\\id.webbrick.co.uk\handlers\EventState", self.doHandleEvent)
        # init cache values
        self._cache = dict()
        self.subcribeTimeout = 30

    def start( self, despatch ):
        # subscribe to all events.
        despatch.subscribe( self.subcribeTimeout, self, "", "" )
#        despatch.subscribe( self.subcribeTimeout, self, "http://id.webbrick.co.uk/events/config/get", "" )

    def stop( self, despatch ):
        # unsubscribe from all events.
        despatch.unsubscribe( self, "", "" )

    def doHandleEvent( self, handler, event ):
        """ Update our cache of values """
        dc = None
        od = event.getPayload()
        # handle events with no payload.
        if od:
            _log.debug( 'update %s %s ' % (event.getSource(), od ) )
            if not self._cache.has_key(event.getSource()):
                self._cache[event.getSource()] = dict()
                
            dc = self._cache[event.getSource()]
            for k in od:
                dc[k] = od[k]
        else:
            # treat no payload as instruction to clear the cache
            if self._cache.has_key(event.getSource()):
                del self._cache[event.getSource()]

        return makeDeferred(StatusVal.OK)

    def queryCache(self, source, attr):
        if self._cache.has_key(source) and self._cache[source].has_key(attr):
            s = self._cache[source][attr]
            e = None
        else:
            s = None
            e = 'Not Known'

        _log.debug( 'event %s:%s - %s(%s)' % (source, attr, s, e ) )
        return { 'stserr': e, 'stsval': s }
    
    @turbogears.expose(template="WebBrickGateway.templates.singleValue", format="xml", content_type="text/xml")
    def default(self, *args):
        cherrypy.response.headerMap["cache-control"] = "no-cache"
        uri = string.join( args, "/" )
        if cherrypy.request.params.has_key('attr'):
            res = self.queryCache( uri, cherrypy.request.params['attr'] )
        else:
            res = self.queryCache( uri, 'val' )
        _log.debug("eventstate %s", res)
        return res






