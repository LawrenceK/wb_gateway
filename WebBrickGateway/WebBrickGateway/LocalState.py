# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: LocalState.py 2610 2008-08-11 20:04:17Z graham.klyne $

import turbogears
import cherrypy
import logging
import string


from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred
from EventLib.EventHandler  import EventHandler

# --------------------------------------------------
# WebBrick command and status access class
# --------------------------------------------------

class LocalState( EventHandler ):
    """
    Local class to handle requests for local state.
    """

    def __init__(self ):
        # init cache values
        self._log = logging.getLogger( "WebBrickGateway.LocalState" )
        super(LocalState,self).__init__("http:\\id.webbrick.co.uk\handlers\LocalState", self.doHandleEvent)
        self._cache = dict()
        self.subscribeTimeout = 30
        pass

    def start( self, router ):
        # subscribe to all required events.
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/state", "" )

    def stop( self, router ):
        # unsubscribe to all events.
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/state", "" )

    def doHandleEvent( self, handler, event ):
        """ Update our cache of values """
        self._log.debug( 'update %s' % (event.getSource() ) )
        self._cache[event.getSource()] = event.getPayload()["val"]
        return makeDeferred(StatusVal.OK)

    def queryCache(self, source):
        if self._cache.has_key(source):
            s = self._cache[source]
            e = None
        else:
            s = None
            e = 'Not Known'

        self._log.debug( 'state %s:%s(%s)' % (source, s, e ) )
        return { 'stserr': e, 'stsval': s }
    
    @turbogears.expose(template="WebBrickGateway.templates.singleValue", format="xml", content_type="text/xml")
    def default(self, *args):
        cherrypy.response.headerMap["cache-control"] = "no-cache"
        return self.queryCache( string.join( args, "/" ) )






