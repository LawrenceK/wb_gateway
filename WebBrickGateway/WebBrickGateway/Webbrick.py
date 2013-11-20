
# $Id: Webbrick.py 3138 2009-04-15 10:17:29Z philipp.schuster $
#
import os.path
import turbogears
import cherrypy
import string
import logging
import time

import ClientProfiles

from WebBrickLibs.WbAccess  import SendHTTPCmd, HTTPTimeout, DoHTTPRequest
from WebBrickLibs.Wb6Status import Wb6Status

from EventLib.Event         import Event
from EventLib.Status        import StatusVal
from EventLib.SyncDeferred  import makeDeferred

from EventLib.EventHandler  import EventHandler

# --------------------------------------------------
# WebBrick command and status access class
# --------------------------------------------------

class WebbrickNodeNameCache( EventHandler ):
    """
    Local class to handle manage a cache of node names and there IP and webbrick node numbers

    These are all picked up from nodename events

    This monitors the event despatcher for the data and caches it for later return.
    """

    def __init__(self):
        # init cache values
        self._log = logging.getLogger( "WebBrickGateway.WebbrickNodeNameCache" )
        super(WebbrickNodeNameCache,self).__init__("http:\\id.webbrick.co.uk\handlers\WebbrickNodeNameCache", self.doHandleEvent)

        self._nameMap = dict()  # contains name to node number
        self._nodeMap = dict()  # contains node number to ip address
        self._IpMap = dict()  # contains ip address to node name map
        self._Versions = dict()  # contains ip address to node name map
        self.subscribeTimeout = 30

    def getNodeNameFromIpAdr( self, ipAdr ):
        result = None
        if self._IpMap.has_key( ipAdr ):
            result = self._IpMap[ ipAdr ]
            self._log.debug( 'lookup Ip %s,name  %s' % ( ipAdr, result ) )
        else:
            self._log.debug( 'lookup Ip %s,NOname' % ( ipAdr ) )
        return result

    def getNodeNumFromIpAdr( self, ipAdr ):
        result = None
        if self._IpMap.has_key( ipAdr ):
            name = self._IpMap[ ipAdr ]
            result = self.getNodeNumber(name)
            self._log.debug( 'lookup nodeNum %s,name  %s' % ( ipAdr, result ) )
        else:
            self._log.debug( 'lookup nodeNum %s,NOname' % ( ipAdr ) )
        return result


    def getNodeNumber( self, name ):
        result = None
        if isinstance( name, basestring ):
            name = name.lower()
        if self._nameMap.has_key( name ):
            result = self._nameMap[ name ]
            self._log.debug( 'lookup name %s:%s' % ( name, result ) )
        else:
            self._log.debug( 'lookup name %s,NOnumber' % ( name ) )
        return result

    def getNodeVersion( self, ipAdr ):
        result = None
        if self._Versions.has_key( ipAdr ):
            result = self._Versions[ ipAdr ]
            self._log.debug( 'lookup version %s:%s' % ( ipAdr, result ) )
        else:
            self._log.debug( 'lookup version %s,NOnumber' % ( ipAdr ) )
        return result

    def getIpAddress( self, nameOrNumber ):
        """
        Lookup nameOrNumber and attempt to get IP address for it.
        """
        result = None
        if isinstance( nameOrNumber, basestring ):
            nameOrNumber = nameOrNumber.lower()
        if self._nameMap.has_key( nameOrNumber ):
            nameOrNumber = self._nameMap[ nameOrNumber ]

        try:
            nameOrNumber  = int(nameOrNumber )
        except ValueError:
            pass # nameOrnumber not updated

        if self._nodeMap.has_key( nameOrNumber ):
            result = self._nodeMap[ nameOrNumber ]
            self._log.debug( 'lookup name %s:%s' % ( nameOrNumber, result ) )
        else:
            self._log.debug( 'lookup name %s NO entry' % ( nameOrNumber ) )
        return result

    def getAllIpAddresses(self):
        return self._IpMap.keys()

    def start( self, router ):
        # subscribe to all required events.
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/config/nodename", "" )

    def stop( self, router ):
        # unsubscribe to all events.
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/config/nodename", "" )

    def doHandleEvent( self, handler, event ):
        if ( event.getType() == "http://id.webbrick.co.uk/events/webbrick/config/nodename" ):
            self._log.debug( 'update name map %s' % ( ( event.getPayload() ) ) )
            if event.getPayload().has_key("fromNode"):
                self._log.info("fromNode is %s" % (event.getPayload()["fromNode"]))
				# in case set from XML config file
                nr = int(event.getPayload()["fromNode"])
                if event.getPayload().has_key("nodename"):
                    self._nameMap[event.getPayload()["nodename"].lower()] = nr
                if event.getPayload().has_key("ipAdr"):
                    self._nodeMap[nr] = event.getPayload()["ipAdr"]
                    if event.getPayload().has_key("nodename"):
                        self._IpMap[event.getPayload()["ipAdr"]] = event.getPayload()["nodename"].lower()
                    if event.getPayload().has_key("version"):
                        self._Versions[event.getPayload()["ipAdr"]] = event.getPayload()["version"].lower()
            self._log.debug( 'XXXXXXXXXXXXXXXXXX   self._nameMap %s' % ( ( self._nameMap ) ) )
            self._log.debug( 'self._nodeMap %s' % ( ( self._nodeMap ) ) )
            self._log.debug( 'self._IpMap %s' % ( ( self._IpMap ) ) )
        return makeDeferred(StatusVal.OK)

class WebbrickCommand:
    """
    Local class to handle commands that are forwarded to WebBricks.

    These are currently sent to /wbcmd/...
    Where everything else in the url is command darta
    first is the command/channle type
    then the channel number
    then extra parameters
    """

    def __init__(self, nameCache = None ):
        self._log = logging.getLogger( "WebBrickGateway.WebbrickCommand" )
        self._namecache = nameCache

    @turbogears.expose(template="WebBrickGateway.templates.commanddone")
    def default(self, *args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "commanddone" )

        cherrypy.response.headerMap["cache-control"] = "no-cache"

        wbaddr = args[0]    # Ip or DNS address
        # see whether we can map webbrick node names to ip address
        if self._namecache:
            ip = self._namecache.getIpAddress( wbaddr )
            if ip:
                wbaddr = ip

        wbtype = args[1]    # channel type? command code (should be 2 chars)
        wbchan = args[2]    # channel number
        wbval = ""
        if len(args) > 3:
            wbval = args[3]

        if wbtype == "DI":
            cmd = "DI"+wbchan
        elif wbtype == "DO":
            if wbval == "on":
                cmd = "DO"+wbchan+";N" # On
            elif wbval == "toggle":
                cmd = "DO"+wbchan+";T" # toggle
            else:
                cmd = "DO"+wbchan+";F" # Off
        else:
            # Default: channel is command, 
            # if value is non-empty: append to command
            cmd = wbtype
            if wbchan != "":
                cmd += wbchan
                for xtra in args[3:]:
                    cmd += ";" + xtra

        self._log.debug( "Sending Command %s" % cmd )
        result['wbtype'] = wbtype
        result['wbchan'] = wbchan
        result['wbval'] = wbval
        result['result'] = result

        try:
            h = SendHTTPCmd(wbaddr,cmd)
            if not h:
                raise cherrypy.HTTPError(400,"WebBrick command failed ("+wbaddr+","+wbchan+","+cmd+")")
        except Exception, ex:
            result['result'] = "Failed"
        # cherrypy.response.status = "204 WebBrick command accepted ("+wbaddr+","+wbchan+","+cmd+")"
        return result

class WebbrickStatus:
    """
    Local class to handle requests for status from WebBricks.

    These are requested from /wbsts/... 
    Where everything else in the uri is parameters
    first is the data type
    second is the channel number.
    """

    def __init__(self):
        self._log = logging.getLogger( "WebBrickGateway.WebbrickStatus" )

    def getStatusVal(self,wbsts,wbtype,wbchan):
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

    @turbogears.expose(template="WebBrickGateway.templates.status", format="xml", content_type="text/xml")
    def default(self, *args):
    
        cherrypy.response.headerMap["cache-control"] = "no-cache"

        if len(args) > 2:
            wbaddr = args[0]    # Ip or DNS address
            wbtype = args[1]    # channel type
            wbchan = args[2]    # channel number

            self._log.debug( 'WebBrickStatus Address %s Channel%s%s' % (wbaddr, wbtype, wbchan ) )

            try:
                wbsts = Wb6Status(wbaddr)
            except HTTPTimeout:
                raise cherrypy.HTTPError(408,"WebBrick response timeout: "+wbaddr)
            except Exception, e:
                return { 'wbAddr' : wbaddr, 'wbChan': wbchan, 
                         'stserr': str(e), 'stsval': None }

            # extract wb channel information
            try:
                s = self.getStatusVal( wbsts, wbtype, int(wbchan) )
            except ValueError, e:
                raise cherrypy.HTTPError(404,"WebBrick channel not present: "+str(e))
            # return simple xml value to caller
            self._log.debug( 'WebBrickStatus %s Channel %s:%s %s' % (wbaddr, wbtype, wbchan, s ) )
            return { 'wbAddr' : wbaddr, 'wbChan': wbchan, 
                     'stserr': None, 'stsval': s }
                     
        return {}
    # AH - PS we think this is redundant, other known function published
    def known(self, *args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "knownWebbricks" )

        known = list()
        result['webbricks'] = known
        return result
        
class WebbrickProxy:
    """
    Local class to proxy access to webbricks.

    With a couple od additions.
    The handler may hold alternate files for requests, so the approach is check local cache
    first for a file and then access the webbrick. This enables alternate webbrick UIs as the local 
    cache will contain html files and js files, whilsts the .inc and .xml files will be accessed from the
    webbrick it self.

    URI format is ..../nameOrAddress/uri

    Where .../ is the location on this server for the proxy
    nameOrAddress is the host name or address for the webbrick
    uri is the item required, in most cases this will be a single part.
    
    """

    def __init__(self):
        self._log = logging.getLogger( "WebBrickGateway.WebbrickProxy" )
        self.proxyDir = turbogears.config.get("default", None, False, "webbrickProxy" )
        self._webbrickVers = {}	# keyed by IP address? contains the UI version string for the named webbrick

    @turbogears.expose()    # no template etc.
    def default(self, *args):
        # and request parameters as well.
        self._log.debug( 'WebBrickProxy args (%i) Uri %s' % (len(args), args ) )

        if len(args) == 0:
            ## no webbrick to handle.
            pass
        elif len(args) == 1:
            # no local part, redirect to index page
            raise cherrypy.HTTPRedirect( "%s/index.htm" % args[0] )
        else:
            wbaddr = args[0]    # Ip or DNS address
            reqUri = string.join( args[1:], '/' )

        # TODO should we use twisted or this is already worker thread so no issue
        self._log.debug( 'WebBrickProxy Address %s Uri %s' % (wbaddr, reqUri) )
        if not self._webbrickVers.has_key(wbaddr):
            # retrieve interface version string.
            r = DoHTTPRequest(wbaddr, "GET", "/ver")
            if r and (r.status == 200):
                self._webbrickVers[wbaddr] = r.read().strip()
            else:
                self._webbrickVers[wbaddr] = 'default'

        # is wbUri in local directory?
        # first look in default webbrick group.
        # TODO allow configuring webbrick UI by address/name
        # TODO list files that must be proxied to webbrick, i.e. .spi files
        localdir = os.path.join( self.proxyDir, self._webbrickVers[wbaddr] )
        if not os.path.exists( localdir ):
            os.makedirs(localdir)

        localpath = os.path.join( localdir, reqUri )
        if os.path.exists( localpath ):
            # yes then return.
            return cherrypy.lib.cptools.serveFile(localpath)
        else:
            # do not cache stuff from webbricks.
            cherrypy.response.headerMap["cache-control"] = "no-cache"
            # retrieve from remote webbrick and serve
            wbUri = '/' + reqUri + '?' + cherrypy.request.query_string

            self._log.debug( 'WebBrickProxy Retrieve %s Uri %s' % (wbaddr, wbUri) )
                
            r = DoHTTPRequest(wbaddr, "GET", wbUri)
            if r:
                if (r.status == 200):
                    txt = r.read()
                    self._log.debug( 'WebBrickProxy %s return (%s)' % (wbaddr, txt) )
                    # if extension is not .inc, .xml then cache locally.
                    if not localpath.endswith('.inc') and not localpath.endswith('.xml'):
                        f = open(localpath,"wb")
                        f.write(txt)
                        f.close()
                    return txt
                elif (r.status == 302):
                    # redirect by webbrick
                    self._log.debug("HTTP redirect %s" % ( r.getheaders() ) )
                    raise cherrypy.HTTPRedirect( r.getheader('Location') )
                else:
                    self._log.debug("HTTP error %i : %s %s " % ( r.status,r.reason,r.getheaders() ) )
                # TODO error handling
                # TODO error
        
        return {}

class WebbrickStatusCache( EventHandler ):
    """
    Local class to handle requests for status from WebBricks.

    These are requested from /wbsts/... 
    Where everything else in the uri is parameters
    first is the data type
    second is the channel number.

    This variant monitors the event despatcher for the data and caches it for later return.
    """

    def __init__(self, nameCache ):
        # init cache values
        self._log = logging.getLogger( "WebBrickGateway.WebbrickStatusCache" )
        super(WebbrickStatusCache,self).__init__("http:\\id.webbrick.co.uk\handlers\WebbrickStatusCache", self.doHandleEvent)
        self._cache = dict()
        self._wbActiveTS = dict()   # indexed by IP address contains time stamp of last seen event.
        self._namecache = nameCache
        self.subscribeTimeout = 30

    def start( self, router ):
        # subscribe to all required events.
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/AI", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/AO", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/CT", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/DI", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/DO", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/ST", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/NN", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/AA", "" )
        router.subscribe( self.subscribeTimeout, self, "http://id.webbrick.co.uk/events/webbrick/AT", "" )

    def stop( self, router ):
        # unsubscribe to all events.
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/AI", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/AO", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/CT", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/DI", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/DO", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/ST", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/NN", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/AA", "" )
        router.unsubscribe( self, "http://id.webbrick.co.uk/events/webbrick/AT", "" )

    def doHandleEvent( self, handler, event ):
        """ Update our cache of values, if the value is not provided for an event then
            we delete the key from our cache """
        self._log.debug( 'WebBrickStatus cache update %s' % (event.getSource() ) )
        if ( event.getType() == "http://id.webbrick.co.uk/events/webbrick/AO" ) :
            # need ipaddr, node number.
            if event.getPayload().has_key("val"):
                self._cache[ event.getSource() ] = event.getPayload()["val"]
            elif self._cache.has_key( event.getSource() ):
                del self._cache[ event.getSource() ]
        elif ( event.getType() == "http://id.webbrick.co.uk/events/webbrick/AI" ) :
            if event.getPayload().has_key("val"):
                self._cache[ event.getSource() ] = event.getPayload()["val"]
            elif self._cache.has_key( event.getSource() ):
                del self._cache[ event.getSource() ]
        elif ( event.getType() == "http://id.webbrick.co.uk/events/webbrick/DI" ) :
            if event.getPayload().has_key("state"):
                if event.getPayload()["state"] == 1:
                    self._cache[ event.getSource() ] = "True"
                else:
                    self._cache[ event.getSource() ] = "False"
            elif self._cache.has_key( event.getSource() ):
                del self._cache[ event.getSource() ]
        elif ( event.getType() == "http://id.webbrick.co.uk/events/webbrick/DO" ) :
            if event.getPayload().has_key("state"):
                if event.getPayload()["state"] == 1:
                    self._cache[ event.getSource() ] = "True"
                else:
                    self._cache[ event.getSource() ] = "False"
            elif self._cache.has_key( event.getSource() ):
                del self._cache[ event.getSource() ]
        elif ( event.getType() == "http://id.webbrick.co.uk/events/webbrick/CT" ) :
            if event.getPayload().has_key("val"):
                self._cache[ event.getSource() ] = event.getPayload()["val"]
            elif self._cache.has_key( event.getSource() ):
                del self._cache[ event.getSource() ]

        if event.getPayload() and event.getPayload().has_key("ipAdr"):
            # update last seen cache
            self._wbActiveTS[event.getPayload()["ipAdr"]] = (time.time(),event.getSource()) # in seconds etc.
        return makeDeferred(StatusVal.OK)

    def queryCache( self, wbName, wbtype, wbchan ):
        # is this a name in our cache of names?
        wbaddr = wbName
        if self._namecache:
            wbaddr = self._namecache.getNodeNumber( wbName )
            if wbaddr == None:  # it may be zero.
                wbaddr = wbName

        if ( wbtype == "Tmp" ):
            source = "webbrick/%s/CT/%s" % (wbaddr,wbchan)
        else:
            source = "webbrick/%s/%s/%s" % (wbaddr,wbtype,wbchan)

        self._log.debug( 'WebBrickStatus query %s' % source )
        if self._cache.has_key(source):
            s = self._cache[source]
            e = None
        else:
            s = None
            e = 'Not Known'

        self._log.debug( 'WebBrickStatus %s Channel %s:%s %s (%s)' % (wbaddr, wbtype, wbchan, s, e ) )
        return { 'wbAddr' : wbaddr, 'wbName' : wbName, 'wbChan': wbchan, 
                 'stserr': e, 'stsval': s }

    # return known webbricks and recent time stamps.
    @turbogears.expose()
    def known(self, *args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "knownWebbricks" )
        return self.knownWebBricksStatus(result)

        
    #@turbogears.expose()  -- old version
    @turbogears.expose(template="WebBrickGateway.templates.walkwb")
    def walkwb(self, *args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "walkwb" )
        return self.knownWebBricksStatus(result)

    def knownWebBricksStatus(self, result, *args):
        known = list()
        thresh = time.time() - 300  # 5 minutes
        # for each IP address return formatted time stamp and flag if older than 5 minutes.
        for ipAdr in self._namecache.getAllIpAddresses():
            if self._wbActiveTS.has_key(ipAdr):
                known.append( { 'ipAdr':ipAdr, 
                    'name' : self._namecache.getNodeNameFromIpAdr(ipAdr), 
                    'node' :  self._namecache.getNodeNumFromIpAdr(ipAdr),
                    'version' : self._namecache.getNodeVersion(ipAdr), 
                    'time': time.strftime("%a %H:%M:%S", time.localtime(self._wbActiveTS[ipAdr][0])),
                    'event': self._wbActiveTS[ipAdr][1],
                    'status': self._wbActiveTS[ipAdr][0] < thresh } )
            else:
                known.append( { 'ipAdr':ipAdr, 
                    'name' : self._namecache.getNodeNameFromIpAdr(ipAdr), 
                    'node' : '',
                    'version' : '', 
                    'time': '',
                    'event': '',
                    'status': True } )
        result['webbricks'] = known
        return result

    @turbogears.expose(template="WebBrickGateway.templates.status", format="xml", content_type="text/xml")
    def default(self, *args):
        cherrypy.response.headerMap["cache-control"] = "no-cache"
        if len(args) > 2:
            return self.queryCache( args[0], args[1], args[2] )
        return {}


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
