import turbogears
import cherrypy
import logging

from WbAccess   import SendHTTPCmd, GetHTTPXmlDom, GetHTTPData, HTTPTimeout
from DomHelpers import getNamedNodeText
from Wb6Status  import Wb6Status

# --------------------------------------------------
# WebBrick command invocation class
# --------------------------------------------------

class WebBrickCommand:
    """
    Class to handle commands that are forwarded to WebBricks.

    These are currently received as /wbcmd/...
    Where everything else in the url is command data
    first is the command/channel type
    then the channel number
    then extra parameters
    """

    @turbogears.expose()
    def default(self, *args):
        """
        Analyze URI and issue corresponding command to the WebBrick
        """

        wbaddr = args[0]    # IP or DNS address
        wbtype = args[1]    # channel type,  command code (should be 2 chars)
        wbchan = args[2]    # channel number
        wbval = ""
        if len(args) > 3:
            wbval = args[3]

        if wbtype == "DI":
            cmd = "DI"+wbchan
        elif wbtype == "DO":
            if wbval == "on":
                cmd = "DO"+wbchan+";N" # On
            else:
                cmd = "DO"+wbchan+";F" # Off
        else:
            # Default: channel is command, 
            # if value is non-empty: append to command
            cmd = wbtype
            if wbchan != "":
                cmd += wbchan
                for xtra in args[3:]:
                    cmd += ";" + wbchan
                    
        h = SendHTTPCmd(wbaddr,cmd)
        if not h:
            raise cherrypy.HTTPError(400,"WebBrick command failed ("+wbaddr+","+wbchan+","+cmd+")")
        # cherrypy.response.status = "204 WebBrick command accepted ("+wbaddr+","+wbchan+","+cmd+")"
        return ""

# --------------------------------------------------
# WebBrick status access class
# --------------------------------------------------

class WebBrickStatus:
    """
    Class to handle requests for status values from WebBricks.

    These are requested from /wbsts/... 
    Where everything else in the uri is parameters
    first is the channel type
    second is the channel number.
    """

    def getStatusVal(self,wbsts,wbtype,wbchan):
        """
        Helper function to extract value from WebBrick status response
        """
        if   wbtype == "DI":
            return wbsts.getDigIn(wbchan)
        elif wbtype == "DO":
            return wbsts.getDigOut(wbchan)
        elif wbtype == "AI":
            return wbsts.getAnIn(wbchan)
        elif wbtype == "AO":
            return wbsts.getAnOut(wbchan)
        elif wbtype == "Tmp":
            return wbsts.getTemp(wbchan)
        raise ValueError, "Unrecognized channel: %s:%s" % ( wbtype, wbchan )

    @turbogears.expose(template="WebBrickConfig.templates.status", format="xml", content_type="text/xml")
    def default(self, *args):
        """
        Analyse URI and return WebBrick status value request
        """

        wbaddr = args[0]    # Ip or DNS address
        wbtype = args[1]    # channel type
        wbchan = args[2]    # channel number

        logging.debug( 'WebBrickStatus Address %s Channel%s%s' % (wbaddr, wbtype, wbchan ) )

        # Fetch status values from designated WebBrick
        try:
            wbsts = Wb6Status(wbaddr)
        except HTTPTimeout:
            raise cherrypy.HTTPError(408,"WebBrick response timeout: "+wbaddr)
        except Exception, e:
            return { 'wbAddr' : wbaddr, 'wbChan': wbchan, 
                     'stserr': str(e), 'stsval': None }

        # Extract WebBrick channel information
        try:
            s = self.getStatusVal( wbsts, wbtype, int(wbchan) )
        except ValueError, e:
            raise cherrypy.HTTPError(404,"WebBrick channel not present: "+str(e))

        # Return simple XML value to caller
        logging.debug( 'WebBrickStatus %s Channel %s:%s %s' % (wbaddr, wbtype, wbchan, s ) )
        return { 'wbAddr' : wbaddr, 'wbChan': wbchan, 
                 'stserr': None, 'stsval': s }

# --------------------------------------------------
# URL handling test class
# --------------------------------------------------
#
#  Display all supplied arguments, and any other values that may be useful

class WebBrickTest:
    """
    Class to display details of incoming request
    """

    @turbogears.expose()
    def default(self, *args, **kwargs):
        """
        Display details of request
        """

        return (
            "<h2>WebBrick request</h2>\n"+
            "<p>Args:<ol>\n"+
            "\n".join([("<li>%s</li>"%(a)) for a in args])+
            "\n</ol></p>\n"+
            "<p>KwArgs:<ul>\n"+
            "\n".join([("<li>%s=%s</li>"%(k,kwargs[k])) for k in kwargs.keys()])+
            "\n</ul></p>\n"+
            "<p>Request base: %s</p>\n"%(repr(cherrypy.request.base))+
            "<p>Request path: %s</p>\n"%(repr(cherrypy.request.path))+
            "<p>Request params: %s</p>\n"%(repr(cherrypy.request.params))+
            "<p>Request query: %s</p>\n"%(repr(cherrypy.request.query_string))+
            "<p>Request headers: %s</p>\n"%(repr(cherrypy.request.headers))+
            "<p>Request object_path: %s</p>\n"%(repr(cherrypy.request.object_path))+
            # "<p>Request virtualPath: %s</p>\n"%(repr(cherrypy.request.virtualPath))+
            "<p>Request user: %s</p>\n"%(repr(cherrypy.request.user))+
            "<p>Request scheme: %s</p>\n"%(repr(cherrypy.request.scheme))+
            "<p>Request rfile: %s</p>\n"%(repr(cherrypy.request.rfile))+
            "<p>Request method: %s</p>\n"%(repr(cherrypy.request.method))+
            "<p>Request version: %s</p>\n"%(repr(cherrypy.request.version))+
            "<p>Request remoteHost: %s</p>\n"%(repr(cherrypy.request.remoteHost))+
            "<p>Request remoteAddr: %s</p>\n"%(repr(cherrypy.request.remoteAddr))+
            "<p>Request remotePort: %s</p>\n"%(repr(cherrypy.request.remotePort))+
            # "<p>Request paramList: %s</p>\n"%(repr(cherrypy.request.paramList))+
            "<p>Request execute_main: %s</p>\n"%(repr(cherrypy.request.execute_main))
            )
