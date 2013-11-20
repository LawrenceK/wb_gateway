# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TimeUtils.py 2989 2008-12-01 14:54:35Z philipp.schuster $
#

import logging



def parseTime( strVal ):

    try:
        prts = map( int, strVal.split(":") )
        return ((prts[0]*60)+ prts[1])*60+ prts[2]
    except: 
        _log = logging.getLogger('WebBrickLibs.MiscLib.TimeUtils')
        _log.debug("Unable to Parse time string, string is: %s" %(strVal))
        return 0
    

def formatTime(intVal):
    s = intVal
    h = intVal / 3600
    s = s - (h * 3600)
    m = s / 60
    s = s - (m * 60)
    return "%02u:%02u:%02u" % ( h,m,s )

# $Id: HVAC.py 2989 2008-12-01 14:54:35Z philipp.schuster $
# End.
