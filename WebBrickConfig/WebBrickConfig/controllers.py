# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: controllers.py 3138 2009-04-15 10:17:29Z philipp.schuster $

"""
Controller for WebBrick configuration server

This is a separate server for WebBrick configuration functions.
The web resources referenced by this server may also be used by
a Home Gateway server.
"""

import turbogears
from turbogears import controllers
import re
import time

import WbCfgManagerForm
import MockWbConfig
import Discovery

from EventHandlers.EventRouterLoad import EventRouterLoader

# --------------------------------------------------
# Root controller
# --------------------------------------------------

despatchConfig = {'eventInterfaces': [{
    'module':'EventHandlers.WebbrickUdpEventReceiver', 
    'name':'WebbrickUdpEventReceiver'},]
    }

class Root(controllers.Root):

    # Class attributes overridden by instance value in start() method
    # (tested by stop() method below.)
    despatch = None
    discover = None

    def start(self):
        # Load and start the event dispatcher, 
        # and associated logic that performs WebBrick discovery

        self.eventloader = EventRouterLoader()
        # system files first.
        self.eventloader.loadHandlers( despatchConfig )
        if self.eventloader:
            self.eventloader.start()
        # now disovery handler.
        self.discover = Discovery.DiscoverHandler()
        self.discover.start(self.eventloader.getEventRouter())

        # wbtst     = WebBrick.WebBrickTest()
        # Assignments to the controller instance (or class) are used to define handing 
        # of URIs.  See cherrypy_cputil.get_object_trail() for some of the details.
        # (TODO: consider how this is affected by local instance attributes like
        #        'despatch' and 'discover' above.)
        if 0:
            # Local testing
            self.wbcnf = MockWbConfig.MockWebBrickCfgEdit()
        else:
            # Production / live WebBricks
            self.wbcnf = WbCfgManagerForm.WbCfgManagerForm(self.discover )
        self.testwbcnf = MockWbConfig.MockWebBrickCfgEdit()
#        self._log.warning( "**** System Configured ****" )

    def stop(self):
        """
        helper to shut down some class stuff.
        """
        if self.despatch:
            self.discover.stop(self.despatch)
            self.despatch.stop()

    @turbogears.expose(template="WebBrickConfig.templates.WbCfgWelcome")
    def index(self):
        return dict(now=time.ctime())

    @turbogears.expose(template="WebBrickConfig.templates.quiet")
    def quiet(self):
        return dict()

    # @turbogears.expose()
    def default(self,*args):
        raise cherrypy.HTTPRedirect(turbogears.url("/panels"))

