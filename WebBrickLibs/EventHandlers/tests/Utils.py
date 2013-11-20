# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: Utils.py 3662 2010-07-12 15:46:14Z andy.harris $
#
# Some test helpers for testing event handlers.
#
from os import walk, mkdir, makedirs, listdir, remove
from os.path import join, split, abspath, exists, isfile, isdir
from shutil import copyfile, rmtree

import threading, sys, logging, time
import socket

from logging.handlers import MemoryHandler

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import StreamRequestHandler, TCPServer
import EventHandlers.tests.TestEventLogger as TestEventLogger

def showWorking():
    sys.stdout.write(".")

def showWait():
    sys.stdout.write("w")

class testLogHandler( MemoryHandler ):
    # retians logging records for later checks.
    def __init__( self ):
        self._LogRecords = list()
        MemoryHandler.__init__( self, 10000 )

    def count( self ):
        return len(self._LogRecords)

    def emit( self, record ):
        self._LogRecords.append( record )
        MemoryHandler.emit( self, record )

def addTestLogHandler(logHandler, name):
    log = logging.getLogger(name)
    log.addHandler(logHandler)
    logHandler.setLevel( logging.INFO )

def removeTestLogHandler(logHandler, name):
    log = logging.getLogger(name)
    log.removeHandler(logHandler)


# Minimal HTTP server to handle test requests
HttpRequests = []
class TestHttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            global HttpRequests
            HttpRequests.append(self.path)
            self.log_message("Request for %s", self.path)
            if self.path.lower().find(".spi") >= 0:
                # webbrick command request, return redirect response.
                self.send_response(302)
                self.send_header('Location','index.htm')
            else:
                self.send_response(200)
                self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write( "" )
        except Exception, ex:
            self._log.exception( ex )

    def log_message(self, format, *args):
        # default is write to screen
        logging.getLogger( "TestHttpHandler" ).debug("%s - %s\n" %
                         (self.address_string(),
                          format%args))

TestHttpServerPort = 20999
class TestHttpServer(threading.Thread):
    def __init__ (self, port=TestHttpServerPort):
        self._log = logging.getLogger( "TestHttpServer" )
        threading.Thread.__init__(self)
        self.running = True
        self.httpServer = None
        self.httpServerPort = port
        self.setDaemon( True ) # when main thread exits stop server as well

    # Terminate interface
    def stop(self):
        self.running = False
        self.httpServer.server_close()
        try:
            skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            skt.connect(("localhost", self.httpServerPort))
            skt.close()
        except Exception, ex:
            #self._log.exception( ex )
            # ignore errors
            pass

    def logRequests(self):
        for req in HttpRequests:
            self._log.debug( req )

    def requests(self):
        return HttpRequests

    def start(self):
        global HttpRequests
        HttpRequests = [] # empty list
        threading.Thread.start( self )
        time.sleep( 0.5 ) # allow startup to occur

    def run(self):
        self._log.debug( "run start" )
        try :
            self.httpServer = HTTPServer( ('',self.httpServerPort), TestHttpHandler)
            while ( self.running ):
                self._log.debug( "handle_request" )
                self.httpServer.handle_request() 
        except Exception, ex:
            self._log.exception( ex )
        self.running = False
        self._log.debug( "run exit" )

SmtpRequests = list()

# Minimal SMTP server
class TestSmtpHandler(StreamRequestHandler):

    def handle(self):
        self._log = logging.getLogger( "TestSmtpHandler" )
        self._log.debug( "TestSmtpHandler start" )
        self.wfile.write( "220 test\r\n" )
        # self.request is a socket
        try:
            lines = []
            while True:
                lines.append( self.rfile.readline() )
                self._log.debug( "TestSmtpHandler %s" % lines[-1] )
                if ( lines[-1] == "data\r\n"):
                    self.wfile.write( "354 test\r\n" )
                    while ( lines[-1] != ".\r\n"):
                        lines.append( self.rfile.readline() )
                        self._log.debug( "TestSmtpHandler %s" % lines[-1] )
                    self.wfile.write( "250 test\r\n" )
                    break;
                else:
                    self.wfile.write( "250 test\r\n" )

            self._log.debug( "TestSmtpHandler %s", lines )
            global SmtpRequests
            SmtpRequests.append(lines)

        except Exception, ex:
            #self._log.exception( ex )
            pass

TestSmtpServer_PORT = 12345
class TestSmtpServer(threading.Thread):
    def __init__ (self, port=TestSmtpServer_PORT):
        self._log = logging.getLogger( "TestSmtpServer" )
        threading.Thread.__init__(self)
        self.running = False
        self.smtpServerPort = port
        self.smtpServer = None
        self.setDaemon( True ) # when main thread exits stop server as well

    # Terminate interface
    def stop(self):
        self.running = False
        try:
            if self.smtpServer:
                self.smtpServer.server_close()
                skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                skt.connect(("localhost", self.smtpServerPort))
                skt.close()
        except Exception, ex:
            self._log.exception( ex )
            pass

    def logRequests(self):
        for req in SmtpRequests:
            self._log.debug( req )

    def requests(self):
        return SmtpRequests

    def start(self):
        global SmtpRequests
        SmtpRequests = [] # empty list
        self.running = True
        threading.Thread.start( self )

    def run(self):
        self._log.debug( "run start" )
        try :
            self.smtpServer = TCPServer( ('',self.smtpServerPort), TestSmtpHandler)
            while ( self.running ):
                self.smtpServer.handle_request() 
            self.smtpServer.server_close()
        except Exception, ex:
            self._log.exception( ex )
        self.running = False
        self.smtpServer = None
        self._log.debug( "run exit" )


def expectNevents(parent, cnt ):
    idx = 20
    while (len(TestEventLogger._events) < cnt) and (idx > 0):
        time.sleep(0.05)
        idx = idx - 1

    if ( len(TestEventLogger._events) != cnt):
        TestEventLogger.logEvents()

    parent.assertEqual( len(TestEventLogger._events), cnt)


def verifyEvents( expectedEvents, haveEvents ):
    # go through and see what events we have
    # return a tuple of (true|false, notSeen) as a result.
    # can check against multiple attributes in the events
    """
            expectedEvents = { 
                    "http://id.webbrick.co.uk/events/config/set" : 
                            [
                                ("schedule/room2/0" , "attr1name", "attr1value"),
                                ("schedule/room2/0" , "attr1name", "attr1value", "attr2name", "attr2value"),
                            ],
                    "http://id.webbrick.co.uk/events/time/hour" : 
                            [   ("time/hour")
                            ],
                    "test/entryCount" : 
                            [   ("test/entryCount",'val', 2)
                            ],
                     }
    """

    haveErr = False

    _log = logging.getLogger( "verifyEvents" )

    for ev in haveEvents:
        found = False   # do we find this event in the expect list
        if expectedEvents.has_key( ev.getType() ):
#            _log.info("found type %s", ev.getType())
            inner = expectedEvents[ ev.getType() ]

            for idx in range(len(inner)):
                ntry = inner[idx]
#                _log.info("check source %s %s", ev.getSource(), ntry[0])
                if ntry[0] == ev.getSource():
#                    _log.info("found type/source %s %s", ev.getType(), ev.getSource())
#                    _log.info("attributes %s payload %s", ntry, ev.getPayload())
                    attrCheck = True
                    if len(ntry) > 1 and ev.getPayload():
                        # has attributes to check against
                        od = ev.getPayload()
                        for idx2 in range(1,len(ntry),2):
                            if ntry[idx2]:
                                if (idx2+1) < len(ntry) and ntry[idx2+1] is not None:
                                    # if attrvalue is present
                                    if not od.has_key(ntry[idx2] or od[ntry[idx2]] != ntry[idx2+1]):
                                        # mismatch
                                        attrCheck = False
                                else:
                                    # if attrvalue is missing or None 
                                    if not od.has_key(ntry[idx2]):
                                        # mismatch
                                        attrCheck = False
                            else:
                                # no pair to check against
                                pass
                    # all attributes are valid
                    if attrCheck:
                        found = True
                        break

            if found:
                del inner[idx]
                if not inner:
                    del expectedEvents[ ev.getType() ]

        if not found:
            # not expecting this one
            _log.info( "Extra event seen %s" % (ev) )
            haveErr = True

    return ( haveErr or len(expectedEvents) > 0, expectedEvents)

def verifyEvents2( expectedEvents, haveEvents ):
    #  have been updating and generalising better the above
    return verifyEvents( expectedEvents, haveEvents )

def verifyEventsSave( expectedEvents, haveEvents ):
    # go through and see what events we have
    # return a tuple of (true|false, notSeen) as a result.
    haveErr = False

    _log = logging.getLogger( "verifyEvents" )

    for ev in haveEvents:
        found = False   # do we find this event in the expect list
        if expectedEvents.has_key( ev.getType() ):
            inner = expectedEvents[ ev.getType() ]

            for idx in range(len(inner)):
                ntry = inner[idx]
                if ntry[0] == ev.getSource():
                    od = ev.getPayload()
                    if not ntry[1] or (od and od.has_key(ntry[1]) and od[ntry[1]] == ntry[2]):
                        found = True
                        break

            if found:
                del inner[idx]
                if not inner:
                    del expectedEvents[ ev.getType() ]

        if not found:
            # not expecting this one
            _log.info( "Extra event seen %s" % (ev) )
            haveErr = True

    return ( haveErr or len(expectedEvents) > 0, expectedEvents)

def testEventInSet( expectedEvents, testEvent ):

    if expectedEvents.has_key( ev.getType() ):
        inner = expectedEvents[ ev.getType() ]

        if inner.has_key( ev.getSource() ):
            return True

    return False

def ClearDirectory( dname ):
    """
    Copy a set of files from one directory to another, create target if needed.
    """
    _log = logging.getLogger( "ClearDirectory" )
    for fn in listdir( dname ):
        if ( fn == '.svn' ):
            # skip
            pass
        else:
            fnf = "%s/%s" % (dname,fn)
            if isfile(fnf):
                _log.debug( "remove file %s", fnf )
                remove( fnf )
            elif isdir(fnf):
                _log.debug( "remove directory %s", fnf )
                rmtree(fnf)
            else:
                _log.debug( "Cannot remove %s", fnf )

def CopyDirectory( sourceDir, targetDir ):
    """
    Copy a set of files from one directory to another, create target if needed.
    """
    _log = logging.getLogger( "CopyDirectory" )
    if not exists( targetDir):
        mkdir(targetDir)

    sourceDirLen = len(sourceDir)

    for root, dirs, files in walk(sourceDir):
        _log.debug( "walk: %s dirs %s files %s" % (root, dirs, files) )

        tgtRoot = join(targetDir, root[sourceDirLen+1:])  # we loose the original path to get the relative path
        _log.debug( "From: '%s' To: '%s'" % (root,tgtRoot) )

        # Create target directory?
        if not exists( tgtRoot):
            mkdir(tgtRoot)

        for name in files:
            fromName = abspath(join(root, name))
            toName = abspath(join( tgtRoot,name))
            if name[0] != '.' :
                if not exists( toName ):
                    _log.debug( "Copy: %s To: %s" % (fromName,toName) )
                    copyfile( fromName, toName )
                else:
                    _log.info( "Skipped: %s already exists" % (fromName) )
            else:
                _log.debug( "Skip: %s" % (fromName) )

        i = len(dirs)-1
        while i >= 0:
            _log.debug( "directory name %s (%i)" % (dirs[i], i) )
            if ( dirs[i][0] == '.' ):
                # remove as not to be copied.
                _log.debug( "directory name removed %s " % (dirs[i]) )
                del dirs[i]
            i = i - 1
