# $Id: Schedule.py 3138 2009-04-15 10:17:29Z philipp.schuster $
#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Lawrence Klyne
#
#
import logging, string

import turbogears
import cherrypy

import ClientProfiles

_log = logging.getLogger( "WebBrickGateway.Schedule" )

# a dictionary keyed by schedule name
# each entry is a dictionary containing
# onoff device names
# value device names
# timepoint count
# a default is always created
defaultschedule = { "default": {"devicesOnOff": [], "devicesValue": [], "timepoints": 8} }

# go direct to the turbogears config object
# better for future dynamic reload.
def getSchedule(name):
    _schedules = cherrypy.config.configs["schedules"]
#    _schedules = turbogears.config.get("schedules" )
    if not _schedules:
        _schedules = defaultschedule
    if _schedules.has_key(name):
        return _schedules[name]
    return defaultschedule["default"]

class Schedule(object):
    """
    Local class to handle queries for data specific to the Schedule system.

    Listens for pertinant events.

    """
    def __init__( self):
        pass

    def start( self ):
        # load self._schedules from cherrypy config
        _schedules = cherrypy.config.configs["schedules"]
#        _schedules = turbogears.config.get("schedules")
        for k in _schedules:
            # ensure these are lists of devices.
            if isinstance(_schedules[k]["devicesOnOff"], basestring):
                if _schedules[k]["devicesOnOff"]:
                    _schedules[k]["devicesOnOff"] = (_schedules[k]["devicesOnOff"],)
                else:
                    _schedules[k]["devicesOnOff"] = ()
            if isinstance(_schedules[k]["devicesValue"], basestring):
                if _schedules[k]["devicesValue"]:
                    _schedules[k]["devicesValue"] = (_schedules[k]["devicesValue"],)
                else:
                    _schedules[k]["devicesValue"] = ()

            _log.debug( 'schedule %s : %s' % (k, _schedules[k]) )
        
    def stop( self ):
        _log.debug( 'stop' )

    @turbogears.expose(template="WebBrickGateway.templates.schedule")
    def list(self, *args):
        """
        return a schedule, single parameter as name, if not given return "default"
        """
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "schedule" )

        result["scheduleName"] = "default"
        if len(args) > 0:
            result["scheduleName"] = args[0]

        _log.debug( "list result %s" % ( result ) )

        return result

    @turbogears.expose(template="WebBrickGateway.templates.schedulelist")
    def index(self,*args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "schedulelist" )

        result["schedules"] = cherrypy.config.configs["schedules"]

        return result
