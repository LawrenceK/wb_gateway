# $Id: controllers.py 2696 2008-09-05 09:33:43Z graham.klyne $
#
# TestSerrver controller module
#

import time
import httplib
from   urlparse import urljoin

from turbogears import controllers, expose, flash
import cherrypy
from cherrypy.filters import basefilter

import logging
log = logging.getLogger("testserver.controllers")

from EventLib.Status            import StatusVal
from EventLib.SyncDeferred      import makeDeferred
from EventLib.Event             import Event, makeEvent
from EventLib.EventHandler      import EventHandler, makeEventHandler
from EventLib.EventRouterHTTPS  import EventRouterHTTPS
from EventLib.URI               import EventBaseUri

from widgets.SimpleButton.SimpleButton import SimpleButton
from widgets.SimpleButton.SimpleButton import ButtonClickEvent, SetButtonStateEvent, SetButtonTextEvent
from widgets.NumericDisplay     import NumericDisplay
from widgets.NumericDisplay     import SetNumericDisplayValueEvent, SetNumericDisplayStateEvent
from widgets.CountdownDisplay   import CountdownDisplay
from widgets.TempSetPoint       import TempSetPoint
from widgets.ModeSelector       import ModeSelector

def makeQuery(kwargs):
    """
    Make query element of URI from a supplied dictionary
    """
    return (kwargs and "?"+"&".join([ k+"="+v for (k,v) in kwargs.iteritems()])) or ""

def makePath(path):
    """
    Make path element of URI from a supplied list of segments.
    The leadfing '/' is not included.
    """
    return "/".join(path)

class TestButtonClickResponder(object):
    """
    Test class to respond to incoming button-click events
    """

    def __init__(self, router):
        """
        Initialize responder logic: receive a buttonclick event and respond
        by generating set button state, set button text and set numeric text
        events with predictable values.
        """
        self._count  = 0
        self._router = router
        router.subscribe(32000, 
            makeEventHandler(handler=self.clickhandler, uri="TestButtonClickResponder"),
            evtype=ButtonClickEvent)
        router.subscribe(32000, 
            makeEventHandler(handler=self.resethandler, uri="TestButtonClickReset"),
            evtype=urljoin(EventBaseUri, "reset"))

    def clickhandler(self, h, e):
        """
        On receiving a button-click, bump the counter and generate some more events
        """
        log.info("clickhandler %s", e)
        buttonstates  = ('up', 'down', 'waiting', 'unknown')
        displaystates = ('normal', 'low', 'high', 'unknown')
        if e.getPayload() == "click":
            self._count += 1
            e1 = makeEvent(SetButtonTextEvent, h.getUri(), "Button:%i"%(self._count))
            self._router.publish(h, e1)
            e2 = makeEvent(SetButtonStateEvent, h.getUri(), buttonstates[self._count%4])
            self._router.publish(h, e2)
            e3 = makeEvent(SetNumericDisplayValueEvent, h.getUri(), str(self._count))
            self._router.publish(h, e3)
            e4 = makeEvent(SetNumericDisplayStateEvent, h.getUri(), displaystates[self._count%4])
            self._router.publish(h, e4)
        return makeDeferred(StatusVal.OK)

    def resethandler(self, h, e):
        """
        On receiving a reset event, reset the response counter
        """
        log.info("resethandler %s", e)
        self._count = 0
        return makeDeferred(StatusVal.OK)

class LeavePostDataFilter(basefilter.BaseFilter):
    """
    Filter supresses parsing of request body - I'm not sure why I have to do this,
    as CherryPy isn't supposed to try and parse field values unless the content-type 
    indicates a suitable form response.
    
    Er, it seems that 'application/x-www-form-urlencoded' is the default content-type
    generated by CURL, or maybe supplied in absence of given content-type?
    """
    def before_request_body(self):
        if cherrypy.request.path[0:6] == '/Proxy':
            # if you don't check that it is a post method the server might lock up
            # we also check to make shour something was submitted
            if not 'Content-Length' in cherrypy.request.headerMap or cherrypy.request.method != 'POST':
                """ the file is empty you might want to redirect"""
            else:
                # Tell CherryPy not to parse the POST data itself for this URL
                cl = cherrypy.request.headers["Content-Length"]
                if cl:
                    cherrypy.request.body = cherrypy.request.rfile.read(int(cl))
                    cherrypy.request.processRequestBody = False

class Proxy:
    """
    Requests proxied to servers on other ports

    Here is a Curl command for testing this:

    curl -H "Content-type: text/plain" -i -d "[\"idle\",[]]" http://localhost:8080/Proxy/8082
    """

    ### Filter not needed if content-type is OK?
    ### _cp_filters = [LeavePostDataFilter()]

    @expose()
    def default(self, *args, **kwargs):
        body = getattr(cherrypy.request, "body", None)
        body = body and body.read()
        logRequest(body, args, kwargs)
        headers = cherrypy.request.headers
        port = int(args[0])
        path = args[1:]
        htc = httplib.HTTPConnection("localhost", port)
        adr = "http://localhost:"+str(port)+"/"
        uri = adr+makePath(path)+makeQuery(kwargs)
        log.debug("Proxy uri %s", uri)
        # request( method, url[, body[, headers]])
        # htc.request("GET", uri, body, headers)
        htc.request(cherrypy.request.method, uri, body)
        rsp = htc.getresponse()
        if not rsp:
            cherrypy.response.status = "500 No response from GET "+adr+uri
            return "500 No response from GET "+adr+uri
        if rsp.status != 200:
            logResponse(rsp)
            cherrypy.response.status = str(rsp.status)+" "+rsp.reason
            return str(rsp.status)+" "+rsp.reason
        cherrypy.response.headers["Cache-control"] = "no-cache"
        cherrypy.response.headers["Pragma"]        = "no-cache"
        cherrypy.response.status = str(rsp.status)+" "+rsp.reason
        rspbody = rsp.read()
        logResponse(rsp, rspbody)
        return rspbody

class Tests:
    """
    A generic dispatch class that executes and formats a template whose name
    appears as the next URI path segment (e.g. /Tests/TemplateName") and
    with arguments provided as URI query values.
    """

    @expose(template="testserver.templates.TestSimpleButton")
    def TestSimpleButton(self, *args, **kwargs):
        kwargs['name'] = kwargs.get("name","sbname")
        sb = SimpleButton(**kwargs)
        return dict(
            now=time.ctime(), 
            simplebutton=sb)

    @expose(template="testserver.templates.TestNumericDisplay")
    def TestNumericDisplay(self, *args, **kwargs):
        kwargs['name'] = kwargs.get("name","ndname")
        nd = NumericDisplay(**kwargs)
        return dict(
            now=time.ctime(), 
            numericdisplay=nd
            )

    @expose(template="testserver.templates.TestButtonAndDisplay")
    def TestButtonAndDisplay(self, *args, **kwargs):
        buttonname  = kwargs.pop("buttonname",  "button_name")
        buttonid    = kwargs.pop("buttonid",    "button_id")
        displayname = kwargs.pop("displayname", "display_name")
        displayid   = kwargs.pop("displayid",   "display_id")
        # Instantiate SimpleButton widget
        kwargs.update( 
            { 'name' : buttonname
            , 'id'   : buttonid
            })
        sb = SimpleButton(**kwargs)
        # Instantiate NumericDisplay widget
        kwargs.update(
            { 'name' : displayname
            , 'id'   : displayid
            })
        nd = NumericDisplay(**kwargs)
        # Return values for page construction by template
        return dict(
            now=time.ctime(), 
            simplebutton=sb,
            numericdisplay=nd
            )

    @expose(template="testserver.templates.TestCountdownDisplay")
    def TestCountdownDisplay(self, *args, **kwargs):
        kwargs['name'] = kwargs.get("name","cdname")
        cd = CountdownDisplay(**kwargs)
        return dict(
            now=time.ctime(), 
            countdowndisplay=cd
            )

    @expose(template="testserver.templates.TestTempSetPoint")
    def TestTempSetPoint(self, *args, **kwargs):
        # Force id, name to 'spname' ...
        kwargs['name'] = kwargs.get("name","spname")
        sp = TempSetPoint(**kwargs)
        return dict(
            now=time.ctime(), 
            tempsetpoint=sp
            )

    @expose(template="testserver.templates.TestTempSetPointParameterized")
    def TestTempSetPointParameterized(self, *args, **kwargs):
        # Allow URI query parameters to override page template and widget values
        sp = TempSetPoint(**kwargs)
        return dict(
            now=time.ctime(), 
            tempsetpoint=sp
            )

    @expose(template="testserver.templates.TestModeSelector")
    def TestModeSelector(self, *args, **kwargs):
        # Allow URI query parameters to override page template and widget values
        ms = ModeSelector(**kwargs)
        return dict(
            now=time.ctime(), 
            modeselector=ms
            )

    @expose(template="testserver.templates.default")
    def default(self, *args, **kwargs):
        flash("Displaying: /Tests/%s %s" % (args[0], str(kwargs)) )
        templatename = "testserver.templates.%s" %args[0]
        return dict(now=time.ctime(), tg_template=templatename, **kwargs)

class Root(controllers.RootController):
    Proxy = Proxy()
    Tests = Tests()

    def __init__(self):
        """
        Perform additional server initialization
        """
        super(Root,self).__init__()
        self.Router    = EventRouterHTTPS("TestBrowserEvents","localhost",8081)
        self.Responder = TestButtonClickResponder(self.Router)
        return

    @expose(template="testserver.templates.Home")
    def index(self):
        logRequest(None, [], {})
        import time
        # log.debug("Happy TurboGears Controller Responding For Duty")
        flash("Your application is now running")
        return dict(now=time.ctime())

    @expose()
    def default(self, *args, **kwargs):
        body = getattr(cherrypy.request, "body", None)
        body = body and body.read()
        logRequest(body, args, kwargs)
        line = cherrypy.request.requestLine
        body = getattr(cherrypy.request, "body", None)
        headers = cherrypy.request.headers
        return "<h1>Default response</h1>\n<p>%s</p><p>%s</p><p>%s, %s</p>\n"%(line,headers,args,kwargs)

def logRequest(body, *args, **kwargs):
    log.debug("Request %s", cherrypy.request.requestLine)
    log.debug("Method %s, path %s", cherrypy.request.method, cherrypy.request.path)
    log.debug("Args %s, %s", str(args), str(kwargs))
    headers = cherrypy.request.headers.copy()
    strip_headers = ('Remote-Addr', 'Accept-Language', 'Accept-Encoding', 
        'Keep-Alive', 'Remote-Host', 'Host', 'Accept', 'User-Agent', 
        'Accept-Charset', 'Connection', 'Pragma', 'Cache-Control',
        'X-Requested-With', 'referer')
    for k in strip_headers:
        if k in headers: del headers[k]
    log.debug("Headers '%s'", headers)
    log.debug("Request body '%s'", body)
    return

def logResponse(rsp, body=""):
    log.debug("Response %i, %s", rsp.status, rsp.reason)
    log.debug("Headers %s", repr(rsp.getheaders()))
    log.debug("Response body '%s'", body)
    return

# End.