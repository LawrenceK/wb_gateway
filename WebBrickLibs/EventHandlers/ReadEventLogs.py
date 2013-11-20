#
#  code to handle reading event logs and doing stuff with them.
#
#  Lawrence Klyne
#
#
import logging, glob
from datetime import datetime

from EventLib.Event         import Event
from EventLib.Status        import StatusVal
from EventLib.SyncDeferred  import makeDeferred
from EventLib.EventAgent    import EventAgent

#from EventHandlers.BaseHandler import BaseHandler
#_log = logging.getLogger( "EventHandlers.LogEvents" )
_log = logging.getLogger("EventHandlers.ReadEventLogs")
#
# WebBrick time event generator
#
# Keys reserved by logging sub system and cannot be in extra
class EventFromString( Event ):
    def __init__(self,str):
        # extract type, source and payload from string.
        # form of string is along these lines.
        #2008-10-26 18:18:23,086 temperature,temperature/outside,{u'name': u'Outside', u'val': 11.4}
        #2008-10-26 18:18:23,717 http://id.webbrick.co.uk/events/webbrick/1,webbrick/3/1,{'seqNr': 80, 'pktType': '1', 'ipAdr': '192.168.1.63', 'fromNode': 3, 'data': '\xfe\x04\x14\x08 22\x07\x06\x07\x00\x04'}
        #2008-10-26 18:18:23,735 http://id.webbrick.co.uk/events/webbrick/1,webbrick/3/1,{'seqNr': 81, 'pktType': '1', 'ipAdr': '192.168.1.63', 'fromNode': 3, 'data': '\x00\x02\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x12\x0f'}
        #2008-10-26 18:18:23,833 http://id.webbrick.co.uk/events/webbrick/ST,webbrick/6,{'uptime': 693, 'resetCode': 92, 'hour': 18, 'fromNode': 6, 'udpType': 'G', 'second': 0, 'version': 6, 'pktType': 'ST', 'ipAdr': '192.168.1.66', 'day': 0, 'minute': 19}
        #2008-10-26 18:18:23,908 http://id.webbrick.co.uk/events/webbrick/ST,webbrick/2,{'uptime': 31309, 'resetCode': 15, 'hour': 18, 'fromNode': 2, 'udpType': 'G', 'second': 0, 'version': 6, 'pktType': 'ST', 'ipAdr': '192.168.1.62', 'day': 0, 'minute': 19}
        #2008-10-26 18:18:24,014 http://id.webbrick.co.uk/events/webbrick/ST,webbrick/7,{'uptime': 36004, 'resetCode': 15, 'hour': 18, 'fromNode': 7, 'udpType': 'G', 'second': 0, 'version': 6, 'pktType': 'ST', 'ipAdr': '192.168.1.67', 'day': 0, 'minute': 19}
        #2008-10-26 18:18:24,182 http://id.webbrick.co.uk/events/webbrick/ST,webbrick/4,{'uptime': 23768, 'resetCode': 92, 'hour': 18, 'fromNode': 4, 'udpType': 'G', 'second': 0, 'version': 6, 'pktType': 'ST', 'ipAdr': '192.168.1.64', 'day': 0, 'minute': 19}
        #2008-10-26 18:18:24,184 http://id.webbrick.co.uk/events/webbrick/CT,webbrick/9/CT/3,{'srcChannel': 3, 'curhi': 100.0, 'val': 19.600000000000001, 'fromNode': 9, 'curlo': -50.0, 'defhi': 100.0, 'deflo': -50.0}
        #2008-10-26 18:18:24,186 http://id.webbrick.co.uk/events/webbrick/AI,webbrick/9/AI/0,{'srcChannel': 0, 'curhi': 100.0, 'val': 24.0, 'fromNode': 9, 'curlo': 0.0, 'defhi': 100, 'deflo': 0}
        # first split the time stamp off
        _log.debug( "Event string %s", str )
        ts = str.split(" ", 2)
        # then split the 3 parts of the event log.
        prts = ts[2].split(",", 2)
        etype = prts[0]
        # prts[1] contains source, with possible preamble.
        esource = prts[1]
        # prts[2] contains payload, with possible preamble.
        od = None
        if prts[2].startswith("{") and prts[2].endswith("}"):
            od = dict()
            # dictionary
            prs = prts[2][1:-1].split(",")
            for pr in prs:
                k,v = pr.strip().split(":",1)
                # loose quotes from k
                k = k[1:-1]
                od[k] = v.strip()
        else:
            od = prts[2]
        super(EventFromString,self).__init__( etype, esource, od )
        _log.debug( "Event %s %s %s", self.getType(), self.getSource(), self.getPayload() )

class ReadLogFile( object ):
    """
    Read log file.
    """
    def __init__ (self, fname=None ):
        self._fname = fname
        self._file = open(fname, "r")
        _log.debug( "ReadLogFile %s %s", self._fname, self._file )

    def next( self ):
        # return next event.
        # handle end of file.
        str = self._file.readline()
        _log.debug( "ReadLogFile %s", str )
        return str

class LineReader( object ):
    """
    return LF separated lines from the contained buffer.
    """
    def __init__ (self, bytes ):
        self._bytes = bytes
        self._idx = 0
        _log.debug( "LineReader %s", len(self._bytes) )

    def next( self ):
        # find next LF
        str = None
        if self._bytes:
            nextidx = self._bytes.find("\n", self._idx)
            if nextidx < 0:
                str = self._bytes[self._idx:]
                self._bytes = None # finished
            else:
                str = self._bytes[self._idx:nextidx+1]
                self._idx = nextidx+1
                
        return str

# internal method
def ReadAndSendEvents( rdr, router ):
    ln = rdr.next()
    while ln:
        evt = EventFromString(ln)
        router.publish( EventAgent("ReadLogFileSendEvents"), evt )
        ln = rdr.next()

def ReadLogFileSendEvents( fname, router ):
    ReadAndSendEvents( ReadLogFile(fname), router )

def ReadLogFilesSendEvents( afname, router ):
    # ambiguous name
    fnames = glob.glob(afname)
    for fname in fnames:
        ReadLogFileSendEvents( fname, router )

def ReadZipFileSendEvents( zipname, router ):
    # zip file name
    # only process files thaat start with 'EventLog'
    zipFile = ZipFile( zipname, "r")
    fnames = zipFile.namelist()
    for fname in fnames:
        if fname.startswith("EventLog"):
            ReadAndSendEvents( LineReader(zipFile.read(fname)), router )

def ReadZipFilesSendEvents( afname, router ):
    # ambiguous name
    fnames = glob.glob(afname)
    for fname in fnames:
        if is_zipfile( fname ):
            ReadZipFileSendEvents( fname, router )
