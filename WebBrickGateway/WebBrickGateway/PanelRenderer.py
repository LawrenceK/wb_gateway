# $Id: PanelRenderer.py 3138 2009-04-15 10:17:29Z philipp.schuster $

import turbogears
from turbogears import controllers
import cherrypy
import re
import time

from PanelDefinition import readPanelDefinition, PanelDefinitionException
from MiscLib.ScanFiles  import CollectFiles
from MiscLib.Functions  import fst, snd

# --------------------------------------------------
# Panel rendering class
# --------------------------------------------------

class PanelRenderer:

    @turbogears.expose(template="WebBrickGateway.templates.paneldef")
    def default(self,*args):
        if len(args) != 1:
            raise cherrypy.HTTPRedirect(turbogears.url("/panels"))
        panelname=args[0]
        print "panel renderer: "+panelname+"\n"
        try:
            panelDef = readPanelDefinition("../resources/paneldef/",panelname)
        except PanelDefinitionException, e:
            turbogears.flash(str(e))
            raise cherrypy.HTTPRedirect(turbogears.url("/panels"))
        panelDef['now']=time.ctime()
        return panelDef
        # return dict(now=time.ctime(),panel=panelDef)
