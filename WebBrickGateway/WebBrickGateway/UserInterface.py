# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: UserInterface.py 2610 2008-08-11 20:04:17Z graham.klyne $

import turbogears
import cherrypy
import logging
import string

import ClientProfiles

class UserInterface:
    """
    Local class to handle requests for local state.
    """

    def __init__(self ):
        # init cache values
        self._log = logging.getLogger( "WebBrickGateway.UserInterface" )
        pass
    
    @turbogears.expose( template="WebBrickGateway.templates.userinterface" )
    def change(self, *args):
        ClientProfiles.changeClientProfile( cherrypy.request )
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "userinterface" )
        return result
    
    @turbogears.expose( template="WebBrickGateway.templates.userinterface" )
    def default(self, *args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "userinterface" )
        return result
                






