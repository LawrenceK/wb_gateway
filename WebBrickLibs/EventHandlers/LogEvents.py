#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Lawrence Klyne
#
#
import logging
from datetime import datetime

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler
_log = logging.getLogger( "EventHandlers.LogEvents" )

#
# WebBrick time event generator
#
# Keys reserved by logging sub system and cannot be in extra
res_keys = ("message", "asctime", 
    "name", "msg", "args", 
    "levelname", "levelno", 
    "pathname", "filename", "module", 
    "exc_info", "exc_text", 
    "lineno", "funcName",
    "created", "msecs", "relativeCreated",
    "thread", "threadName",
    "process")

class LogEvents( BaseHandler ):
    """
    Log all events.
    """
    def __init__ (self, localRouter):
        self._log = _log
        super(LogEvents,self).__init__(localRouter)

    def configureActions( self, cfgDict ):
        _log.debug( "configureActions %s" % str(cfgDict) )
        if ( cfgDict.has_key("exclude") ):
            action = "exclude"
        else:
            action = "include"
        return action

    def doActions( self, action, inEvent ):
        if action == "include":
            #typ = inEvent.type()
            #if typ.startswith( "http://id.webbrick.co.uk/events/" ):
            #    typ = "EventLog." + typ[32:]
            #else:
            #    typ = "EventLog." + typ

            typ = "EventLog.%s" % inEvent.getSource()
            typ = typ.replace( "/", "." )
            _log.debug( "EventLog %s" % typ )
            log = logging.getLogger( typ )
            if log.isEnabledFor( logging.INFO ):    # as str of an event may be heavy operation.
                extra = {'source':inEvent.getSource(),
                         'type':inEvent.getType() }
                # TODO confirm is a dictionary
                if inEvent.getPayload():
                    for k in inEvent.getPayload():
                        if k not in res_keys:
                            extra[k] = inEvent.getPayload()[k]
                        
                if inEvent.getPayload():
                    log.info( "%s,%s,%s", inEvent.getType(), inEvent.getSource(), inEvent.getPayload(), extra=extra )
                else:
                    log.info( "%s,%s", inEvent.getType(), inEvent.getSource() )

