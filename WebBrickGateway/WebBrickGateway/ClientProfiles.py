# $Id: ClientProfiles.py 3193 2009-06-09 15:47:44Z philipp.schuster $

import pkg_resources
import turbogears
import cherrypy
import logging
import string
import copy

from MiscLib.Logging import debugLogDataStructure
from MiscLib.DomHelpers import getDictFromXmlFile, saveXmlToFile, getXmlDomFromDict, getElemPrettyXml, saveXmlToFilePretty

from Utils import getTemplateName

_log = logging.getLogger( "WebBrickGateway.ClientProfiles" )
_ClientProfiles = None

class ClientProfiles:
    def __init__( self, persistFile ):
        self.persistFile = persistFile
        self._persistData = None
        self._clients = dict()  # combination of specific and default entries.
        self._useragents = dict()  # cross reference to relevant entries

    def getBrowserId( self, ua ):
        """
        returns a short string that identifies the browser
        """

        if ua.find( "camino" ) >= 0:    # MAC
            return "camino"

        elif ua.find( "ipod" ) >= 0:  # MAC?
            return "ipod"

        elif ua.find( "nevo" ) >= 0:  # NEVO remote
            return "ipod"

        elif ua.find( "safari" ) >= 0:  # MAC?
            return "safari"

        elif ua.find( "chrome" ) >= 0:  # google chrome
            return "chrome"

        elif ua.find( "seamonkey" ) >= 0:
            return "seamonkey"

        elif ua.find( "windows ce" ) >= 0:   # also returns msie
            return "windowsce"

        elif ua.find( "konqueror" ) >= 0:   # also returns msie
            return "konqueror"

        elif ua.find( "minimo" ) >= 0:   # also returns msie
            return "minimo"

        elif ua.find( "mediacenter" ) >= 0:   # also returns msie
            return "windowsmc"

        elif ua.find( "snom" ) >= 0:   #  SNOM XML browser
            return "phonesnom"

        elif ua.find( "cisco" ) >= 0:   # CISCO XML browser
            return "phonecisco"

        elif ua.find( "aastra" ) >= 0:   # Aastra VOIP phones
            return "phoneastra"

        elif ua.find( "opera mini" ) >= 0:
            return "operamini"

        elif ua.find( "opera" ) >= 0:
            return "opera"

        elif ua.find( "firefox" ) >= 0:
            return "firefox"

        elif ua.find( "msie" ) >= 0:
            return "msie"

        elif ua.find( "netscape" ) >= 0:
            return "netscape"

        return "unknown"

    def clientKey( self, request ):
        """
        returns a client name key. If not recognised then updates persist profile 
        and returns unknown key.
        """
        uaStr = ""
        if request.headers.has_key("User-Agent"):
            uaStr = request.headers["User-Agent"].lower()

        if self._useragents.has_key( uaStr ):
            return self._useragents[ uaStr ]['client']
        else:
            client = self.getBrowserId( uaStr )
            newUa = { '': uaStr, 'client': client }
            uaS = self._persistData['userprofiles']['useragent'].append(newUa)  # add new
            self._useragents[ uaStr ] = newUa   # update cross reference

            if not self._clients.has_key(client):
                # create new entry.
                self._clients[client] = dict(self._clients['default'])

                self._persistData['userprofiles']['client'].append( { 'name':client, 'default': {} } )  # loads from default profile

            self.save()
            return client

    def load(self):
        """
        load from peristant storage
        """
        self._persistData = getDictFromXmlFile( "%s.xml" % self.persistFile )
        if not self._persistData:   # may not exist yet
            # create empty data sets
            # no ua strings and 2 profiles, default and unknown
            self._persistData =  {u'userprofiles': {u'useragent': [], 
                        u'client': [{u'name': u'default', u'default': {u'alinksonly': u'no', u'tg_format': u'xhtml', u'flash': u'yes', u'templateModule': u'templates', u'javascript': u'yes', u'flash': u'yes'}}, 
                                    {u'name': u'unknown', u'default': {u'alinksonly': u'no', u'tg_format': u'xhtml', u'flash': u'no', u'templateModule': u'templates', u'javascript': u'no', u'flash': u'no'}} ]}} 

        _log.debug( "profiles %s " % (self._persistData) )

        # build user agent cross ref
        uaS = self._persistData['userprofiles']['useragent']
        _log.debug( "useragents %s " % (uaS) )
        if not isinstance(uaS, list):
            # ensure it is a list of user agents.
            self._persistData['userprofiles']['useragent'] = list()
            self._persistData['userprofiles']['useragent'].append(uaS)
            uaS = self._persistData['userprofiles']['useragent']

        for ua in uaS:
            _log.debug( "useragent %s " % (ua) )
            uaStr = ''  # may be blank
            if ua.has_key(''):
                uaStr = ua[''].lower()
            self._useragents[uaStr] = ua

        _log.debug( "_clients %s " % (self._useragents) )

        # build client details
        for cl in self._persistData['userprofiles']['client']:
            # a dictionary
            _log.debug( "client %s " % (cl) )
            name = str(cl['name'])
            self._clients[name] = dict()
    
            for k in cl['default']:
                self._clients[name][str(k)] = str(cl['default'][k])

        if self._clients.has_key('default'):
            df = self._clients['default']
            for k in self._clients:
                if k <> 'default':
                    # apply defaults
                    cur = self._clients[k]
                    for k2 in df:
                        if not cur.has_key(k2):
                            cur[k2] = df[k2]

        _log.debug( "_clients %s " % (self._clients) )

    def save(self):
        """
        save to peristant storage
        """
        _log.debug( "_clients %s " % (self._clients) )
        try:
            _log.debug( "Dictionary to be saved %s " % (self._persistData) )

            xmlDom = getXmlDomFromDict( self._persistData, rootElem = None )
            _log.debug( "Xml %s" % (getElemPrettyXml(xmlDom)) )

            saveXmlToFilePretty( "%s.xml" % self.persistFile , xmlDom )

        except Exception, ex:
            # possibly read only storage
            _log.exception( "load" )

    def createDefault( self, request ):
        """
        Creates a client profile based on just the user agent.
        # NOT USED
        """

        # First time seen this client?
        _log.debug( "request %s " % request.requestLine )
        _log.debug( "remote_addr %s, remote_port %s, remote_host %s " % (request.remote_addr, request.remote_port,request.remote_host ) )
        _log.debug( "scheme %s, execute_main %s, closed %s " % (request.scheme, request.execute_main,request.closed ) )
        _log.debug( "simple_cookie %s, method %s, object_path %s " % (request.simple_cookie, request.method,request.object_path ) )
        _log.debug( "path %s, query_string %s, protocol %s " % (request.path, request.query_string,request.protocol ) )
        _log.debug( "version %s, base %s" % (request.version, request.base ) )
        debugLogDataStructure( _log, request.headers )

        result = dict()
        result["javascript"] = "yes"    # does client support java script
        result["alinksonly"] = "no"     # does client support onCliock handlers, needs Javascript

        # preference order.
        ac = request.headers["Accept"].lower()
        if ac.find( "application/xhtml" ) >= 0:
            result["tg_format"] = "xhtml"
        elif ac.find( "text/html" ) >= 0:
            result["tg_format"] = "html"
        elif ac.find( "text/xml" ) >= 0:
            result["tg_format"] = "xml"
        elif ac.find( "application/xml" ) >= 0:
            result["tg_format"] = "xml"

        ua = request.headers["User-Agent"].lower()
        if ua.find( "camino" ) >= 0:    # MAC
            result["templateModule"] = "templates"

        elif ua.find( "safari" ) >= 0:  # MAC?
            result["templateModule"] = "templates"

        elif ua.find( "seamonkey" ) >= 0:
            result["templateModule"] = "templates"

        elif ua.find( "windows ce" ) >= 0:   # also returns msie
            result["templateModule"] = "templates"

        elif ua.find( "konqueror" ) >= 0:   # also returns msie
            result["templateModule"] = "templates"

        elif ua.find( "minimo" ) >= 0:   # also returns msie
            result["javascript"] = "no"
            result["alinksonly"] = "yes"
            result["templateModule"] = "templates"

        elif ua.find( "mediacenter" ) >= 0:   # also returns msie
            result["javascript"] = "no"
            result["alinksonly"] = "yes"
            result["templateModule"] = "templates.simple"

        elif ua.find( "snom" ) >= 0:   #  SNOM XML browser
            result["javascript"] = "no"
            result["alinksonly"] = "yes"
            result["tg_format"] = "xml"
            result["templateModule"] = "templates.snom"

        elif ua.find( "cisco" ) >= 0:   # CISCO XML browser
            result["javascript"] = "no"
            result["alinksonly"] = "yes"
            result["tg_format"] = "xml"
            result["templateModule"] = "templates.cisco"

        elif ua.find( "aastra" ) >= 0:   # Aastra VOIP phones
            result["javascript"] = "no"
            result["alinksonly"] = "yes"
            result["tg_format"] = "xml"
            result["templateModule"] = "templates.aastra"

        elif ua.find( "opera mini" ) >= 0:
            result["templateModule"] = "templates"

        elif ua.find( "opera" ) >= 0:
            result["templateModule"] = "templates"

        elif ua.find( "firefox" ) >= 0:
            result["templateModule"] = "templates"

        elif ua.find( "msie" ) >= 0:
            result["templateModule"] = "templates"

        elif ua.find( "netscape" ) >= 0:
            result["templateModule"] = "templates"

        else:
            result["javascript"] = "no"
            result["alinksonly"] = "yes"
            result["templateModule"] = "templates.simple"

        # is it an XML only browser?
        # check headers.
    #    result["tg_format"] = "xml"

        return result

    def lookup( self, request ):
        """
        attempt to get client configuration.
        """
        k = self.clientKey( request )
        _log.debug( "client Key %s" % (k) )
        if not self._clients.has_key( k ):
            k = 'default'

        _log.debug( "lookup %s - %s" % (k, self._clients[k]) )
        return self._clients[k]

    def change( self, request ):
        """
        called to make changes to the client profile.

        We keep the DOM loaded structure as well as a processed copy.
        """

        # Is update for the generic browser or for the specific user.
        if request.params.has_key( "client" ):
            # update a specific client name. mainly for access to default and unknown
            k = request.params["client"]
            del request.params["client"]
        else:
            k = self.clientKey( request )

        ip = "default"
        if request.params.has_key( "address" ):
            if request.params["address"] == "yes":
                # update is for browser at the current client address
                ip = request.remote_addr # do I need to convert to string
            else:
                ip = request.params["address"]  # provided ip address.. verify address
            del request.params["address"]

        _log.debug( "change client %s address %s - %s" % (k, ip, str(request.params)) )

        # we need to modofy the local cache to have ip address and default entries.
        if self._clients.has_key(k):
            clientProfile = self._clients[k]
            # find Xml dictionary
            for clientProfileX in self._persistData['userprofiles']['client']:
                if clientProfileX["name"] == k:
                    break
        else:
            clientProfileX = dict()
            clientProfileX["name"] = k
            clientProfileX["default"] = dict()
            self._persistData['userprofiles']['client'].append( clientProfileX )
            clientProfile = dict(self._clients["default"])  # copy defaults
            self._clients[k] = clientProfile

        _log.debug( "changeClientProfile before %s - %s" % (k, clientProfile) )

        # now make the changes and update. Persist here.
        # should this be all parameters?

        # some parameters cannot be passed directly in the URI.
        for p in request.params:
            if p == "tgformat":
                clientProfile["tg_format"] = str(request.params[p]) # loose unicode
                clientProfileX[ip]["tg_format"] = request.params[p]
            else:
                clientProfile[p] = str(request.params[p])
                clientProfileX[ip][p] = request.params[p]

        _log.debug( "changeClientProfile after %s - %s" % (k, clientProfile) )

        self.save()    # write back to persist it.

def changeClientProfile( request ):
    _ClientProfiles.change( request )

def makeStandardResponse( request, templateName = None ):
    """

    create a dictionary that will be passed to a template for processing.
    fill in standard values, i.e. debug and javascript
    
    The inbound is a cherry py request object.

    If the templateName is passed then it should be qualified by prepending a package name to it,
    this package will be selected on a per client basis.

    The default template package name is templates.

    """
    result = dict()

    clientProfile = _ClientProfiles.lookup( request )

    _log.debug( "makeStandardResponse params % s" % (request.params))

    def trySetTemplateName( templatePath ):
        if templateName and not result.has_key("tg_template"):
            tmpl = getTemplateName( templatePath, templateName )
            if tmpl:
                result["tg_template"] = tmpl
    
    for key in request.params:
        result[key] = request.params[key]
                
    if request.params.has_key( "debug" ):
        result["debug"] = "yes"
    
        
    # need to filter some out
    for k in clientProfile:
        if k not in ["templateModule","skinTemplateModule"]:
            # copy atributes over
            result[k] = clientProfile[k]
            
    if clientProfile.has_key("templateModule"):
        trySetTemplateName(clientProfile["templateModule"])
    if clientProfile.has_key("skinTemplateModule"):
        trySetTemplateName(clientProfile["skinTemplateModule"])
    # default handling of template name
    trySetTemplateName("templates")
    # Final fallback handling of template name
    # So returns system templates if no user templates.
    trySetTemplateName("WebBrickGateway.templates")

    _log.debug( "makeStandardResponse %s " % result )

    return result

def load( persistFile ):
    global _ClientProfiles
    _ClientProfiles = ClientProfiles( persistFile )
    _ClientProfiles.load()


# $Id: ClientProfiles.py 3193 2009-06-09 15:47:44Z philipp.schuster $
