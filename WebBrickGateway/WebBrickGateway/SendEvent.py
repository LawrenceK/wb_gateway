# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: SendEvent.py 3138 2009-04-15 10:17:29Z philipp.schuster $

import turbogears
import cherrypy
import logging
import string

#from twisted.web import client
from WebBrickLibs.WbAccess import GetHTTPData
from EventLib.Event import Event, makeEvent

import ClientProfiles

# --------------------------------------------------
# WebBrick command and status access class
# --------------------------------------------------
class SendEventLocal:
    """
    Local class to forward events to the local event distributor, these are received from the
    user interface.
    """

    def __init__ (self, router):
        # no extra config as yet.
        self._log = logging.getLogger( "WebBrickGatewaySendEventLocal" )
        self._router = router

    @turbogears.expose(template="WebBrickGateway.templates.commanddone")
    def default(self, *args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "commanddone" )

        cherrypy.response.headerMap["cache-control"] = "no-cache"
        uri = string.join( args, "/" )
        type = u'http://id.webbrick.co.uk/events/uri'
        other_data = dict()

        for k in cherrypy.request.params:
            if k == "type":
                type = cherrypy.request.params[k]
            else:
                other_data[k] = cherrypy.request.params[k]

        if len(other_data) == 0:
            other_data = None
        self._router.publish( "SendEventLocal", Event( type, uri, other_data ) )

        return result

