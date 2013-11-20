# $Id: PanelHtml.py 2610 2008-08-11 20:04:17Z graham.klyne $
#
"""
WebBrick control panel HTML conversion module.

This module uses Turbogears templates directly to perform the conversion.
Another module will be created to use the Turbogears expose decorator
to invoke the same rendering logic.
"""

#import sys
#from os.path  import exists
#from operator import concat

#from DomHelpers  import parseXmlFile, isElement
#from Combinators import curry1
#from Functions   import concatMap

import turbogears
from turbogears import view
from kid import XMLSerializer

from PanelDefinition import readPanelDefinition

class PanelHtmlException(Exception):
    """
    Exception class for panel HTML conversion  errors.
    """
    def __init__(self,*args):
        Exception.__init__(self,*args)

def makePanelHtml(pdDir,pdName):
    """
    Read a panel definition file and return it as an HTML string, 
    using the Tubogears template processor.
    """
    pdDict = readPanelDefinition(pdDir,pdName)
    output = XMLSerializer(encoding="UTF-8", decl=True, 
                doctype=("html",
                         "-//W3C//DTD XHTML, 1.0 Strict//EN", 
                         "http://www.w3.org/TR/xhtml1-strict-dtd"))
    pdHtml = render(pdDict,template="WebBrickGateway.templates.paneldef",formatter=output)
    return pdHtml

# Alternative version of view.render not relying on cherrypy request object
def render(info, formatter="xml", fragment=False, template=None):
    tclass = view.lookupTemplate(template)
    view.log.debug("Applying template %s" % (tclass.__module__))
    if not info.has_key("tg_flash"):
        info["tg_flash"] = None
    t = tclass(**info)
    t.std = view.attrdict \
        ( useragent="firefox"
        , selector=view.selector
        , tg_js="/" + turbogears.startup.webpath + "tg_js"
        , ipeek=view.ipeek
        , quote_plus=view.quote_plus
        , checker=view.checker
        , url = turbogears.url
        )
    return t.serialize(encoding="utf-8", output=formatter, fragment=fragment)

# End.
