# $Id: MockWbConfig.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
This is a test module for handling requests for WebBrick configuration 
resources.  It is built in to the WebBrickConfig server to provide a
means to test configuration clients in the absence of a real network
of WebBricks.
"""

import turbogears
import cherrypy
import logging

from WebBrickLibs.WbAccess  import SendHTTPCmd, GetHTTPXmlDom, GetHTTPData, HTTPTimeout
from WebBrickLibs.Wb6Status import Wb6Status

from MiscLib.DomHelpers import getNamedNodeText

# --------------------------------------------------
# WebBrick command invocation class
# --------------------------------------------------

class MockWebBrickCfgEdit:
    """
    Mock class to handle requests for WebBrick configuration management 
    resources, for testing purposes.
    """

    @turbogears.expose()
    def wbNetworks(self):
        cherrypy.response.headerMap["Content-Type"] = "application/xml"
        return """<?xml version="1.0" encoding="utf-8" ?>
            <Networks>
              <Network>193.123.216.64/26</Network>
              <Network>10.0.0.0/8</Network>
              <Network>0.0.0.0/32</Network>
            </Networks>
            """

    @turbogears.expose()
    def wbDiscover(self, netadrs, netmask):
        cherrypy.response.headerMap["Content-Type"] = "application/xml"
        wbs1 = """<?xml version="1.0" encoding="utf-8" ?>
            <WebBricks>
              <WebBrick mac="00:03:75:0F:87:F1" node="000" name="node 1 name" adrs="193.123.216.121" attn="No" />
              <WebBrick mac="aa:bb:cc:dd:ee:01" node="001" name="node 1 test" adrs="193.123.216.101" attn="No" />
              <WebBrick mac="aa:bb:cc:dd:ee:02" node="002" name="node 2 name" adrs="193.123.216.102" attn="Yes"/>
              <WebBrick mac="aa:bb:cc:dd:ee:03" node="003" name="node 3 name" adrs="193.123.216.103" attn="No" />
              <WebBrick mac="aa:bb:cc:dd:ee:04" node="004" name="node 4 name" adrs="193.123.216.104" attn="Yes"/>
            </WebBricks>
            """
        wbs2 = """<?xml version="1.0" encoding="utf-8" ?>
            <WebBricks>
              <WebBrick mac="aa:bb:cc:dd:10:01" node="001" name="node 1 test" adrs="10.0.0.1" attn="No" />
              <WebBrick mac="aa:bb:cc:dd:10:02" node="002" name="node 2 name" adrs="10.0.0.2" attn="No" />
              <WebBrick mac="aa:bb:cc:dd:10:03" node="003" name="node 3 name" adrs="10.0.0.3" attn="Yes"/>
              <WebBrick mac="aa:bb:cc:dd:10:04" node="004" name="node 4 name" adrs="10.0.0.4" attn="Yes"/>
            </WebBricks>
            """
        wbs3 = """<?xml version="1.0" encoding="utf-8" ?>
            <WebBricks>
              <WebBrick mac="00:00:00:00:00:00" node="000" name="No WebBrick" adrs="0.0.0.0" attn="No"/>
            </WebBricks>
            """
        if   netadrs=="193.123.216.64":  return wbs1
        elif netadrs=="10.0.0.0":        return wbs2
        else:                            return wbs3

    @turbogears.expose()
    def wbConfigSets(self):
        cherrypy.response.headerMap["Content-Type"] = "application/xml"
        return """<?xml version="1.0" encoding="utf-8" ?>
            <ConfigSets>
              <ConfigSet>Example-1</ConfigSet>
              <ConfigSet>Example-2</ConfigSet>
              <ConfigSet>Example-3</ConfigSet>
            </ConfigSets>
            """

    @turbogears.expose()
    def wbConfigSet(self, nam):
        cherrypy.response.headerMap["Content-Type"] = "application/xml"
        cfs1 = """<?xml version="1.0" encoding="utf-8" ?>
            <Configs>
              <Config node="000" name="Example-1.0" />
              <Config node="001" name="Example-1.1" />
              <Config node="002" name="Example-1.2" />
              <Config node="003" name="Example-1.3" />
              <Config node="004" name="Example-1.4" />
              <Config node="005" name="Example-1.5" />
              <Config node="006" name="Example-1.6" />
              <Config node="007" name="Example-1.7" />
              <Config node="008" name="Example-1.8" />
              <Config node="009" name="Example-1.9" />
              <Config node="010" name="Example-1.10" />
              <Config node="011" name="Example-1.11" />
              <Config node="012" name="Example-1.12" />
              <Config node="013" name="Example-1.13" />
              <Config node="014" name="Example-1.14" />
              <Config node="015" name="Example-1.15" />
            </Configs>
            """
        cfs2 = """<?xml version="1.0" encoding="utf-8" ?>
            <Configs>
              <Config node="000" name="Example-2.0" />
              <Config node="001" name="Example-2.1" />
              <Config node="002" name="Example-2.2" />
              <Config node="003" name="Example-2.3" />
              <Config node="004" name="Example-2.4" />
              <Config node="005" name="Example-2.5" />
            </Configs>
            """
        cfs3 = """<?xml version="1.0" encoding="utf-8" ?>
            <Configs />
            """
        if   nam=="Example-1": return cfs1
        elif nam=="Example-2": return cfs2
        else:                  return cfs3

    @turbogears.expose()
    def wbConfigAction(self):
        req = cherrypy.request
        paramlist = "<dl>\n"
        for k in req.paramMap.keys():
            paramlist += "<dt>"+k+"</dt><dd>"+req.paramMap[k]+"</dd>\n"
        paramlist += "</dl>\n"
        return ("<h1>Form parameters returned</h1>"+
                paramlist+
                """
                <p>
                <a href="/static/ConfigManager.xhtml">Return to main config page</a>
                </p>
                """)
        raise cherrypy.HTTPRedirect("/static/ConfigManager.xhtml")  # Redisplay main form

    @turbogears.expose()
    def index(self, *args):
        """
        Index page for configuration resources
        """
        requri = cherrypy.request.browserUrl
        raise cherrypy.HTTPError(404, "Unrecognized index URI: "+requri )
        return ""

    @turbogears.expose()
    def default(self, *args):
        """
        Analyze request URI and invoke the corresponding configuration resource
        """
        requri  = cherrypy.request.browserUrl
        if len(args) > 0:
            if args[0] == "Networks": return self.wbNetworks()
            if args[0] == "Discover": return self.wbDiscover(args[1], args[2])
            if args[0] == "Config": 
                if len(args) == 1: 
                    return self.wbConfigSets()
                else:
                    return self.wbConfigSet(args[1])
            if args[0] == "ConfigAction": return self.wbConfigAction()
        raise cherrypy.HTTPError(404, "Unrecognized URI: "+requri+", args[0] "+args[0] )
        # cherrypy.response.status = "204 WebBrick command accepted ("+wbaddr+","+wbchan+","+cmd+")"
        return ""

# End: $Id: MockWbConfig.py 2612 2008-08-11 20:08:49Z graham.klyne $
