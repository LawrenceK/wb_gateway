# $Id: LocalData.py 3504 2010-02-02 16:30:06Z philipp.schuster $

import turbogears
import cherrypy
import logging
import time 
from MiscLib.Sun import Sun

# --------------------------------------------------
# Gateway local data management.
# --------------------------------------------------

_currentMesages = []

class Message:
    def __init__( self, txt, tag, pri=4, validFor=None ):
        self._pri = int(pri)
        self._txt = txt
        self._tag = tag
        self._expires = time.time()
        if ( validFor ):
            if ( validFor == "allways" ):
                self._expires = None
            else:
                self._expires += int(validFor)
        else:
            self._expires += 300    # 5 minutes

def _cmpMessage( a, b ):
    """
    used when sorting the messages
    """
    if a._pri < b._pri: # lower value comes first
        return -1
    elif a._pri > b._pri:
        return 1
    else:
        # equal priority
        # if ._expires is None then long time in future so treat as greater than any other expiry.
        if a._expires is None:
            return 1
        elif b._expires is None:
            return -1
        elif a._expires < b._expires:
            return -1
        elif a._expires > b._expires:
            return 1
        # if here then equal
    return 0    # identical.
            
class LocalData:
    """
    Local class to handle queries for local data to the gateway, e.g. time of day.
    """

    def __init__( self ):
        self._logger = logging.getLogger( "WebBrickGateway.LocalData" )
        self.sunRise = Sun()
        self._timeFormat_12h = "%I:%M%p"   # 12 hour clock
        self._timeFormat_24h = "%H:%M"   # 24 hour clock
            #self._timeFormat = "%X"   # locale clock, includes seconds
        self._insertMessages( Message( "Started", "Started" ) )

    def _clearOldMessages(self):
        """
        Check for obsolete messages in the _currentMessages
        """
        cherrypy.response.headerMap["cache-control"] = "no-cache"
        global _currentMesages
        now = time.time()
        idx = len(_currentMesages)
        while idx > 0:
            idx -= 1
            msg = _currentMesages[idx]
            if msg._expires and ( msg._expires < now ):
                # remove from list
                self._logger.debug( "_clearOldMessages(delete) %i %s %s" % (msg._pri, msg._txt, msg._expires ) )
                del _currentMesages[idx]

    def _insertMessages(self, msg):
        """
        Adds message to _currentMesages based on priority. Lowest values come first.
        """
        self._logger.debug( "_insertMessages %i:%s %s %s" % (msg._pri, msg._tag, msg._txt, msg._expires ) )
        global _currentMesages
        _currentMesages.append( msg )
        _currentMesages.sort( _cmpMessage )

    @turbogears.expose(template="WebBrickGateway.templates.singleValue", format="xml", content_type="text/xml")
    def time(self, *args):
        """
        Return time at Gateway as string value in form HH:MM
        """
        cherrypy.response.headerMap["cache-control"] = "no-cache"
        
        len_args = len(args) 
        if len_args >= 1:
            
            # the below is left for backward compatibility
            if args[0] == "sunrise":
                riseSet = self.sunRise.sunRiseSetDST()
                # convert values, they are 
                if (len_args == 2) and (args[1] == "24h"):
                    res = time.strftime( self._timeFormat_24h, time.gmtime(riseSet[0] * 3600))   # 24 hour clock
                else:
                    res = time.strftime( self._timeFormat_12h, time.gmtime(riseSet[0] * 3600))   # 12 hour clock

            elif args[0] == "sunset":
                riseSet = self.sunRise.sunRiseSetDST()
                if (len_args == 2) and (args[1] == "24h"):
                    res = time.strftime( self._timeFormat_24h, time.gmtime(riseSet[1] * 3600))   # 24 hour clock
                else:
                    res = time.strftime( self._timeFormat_12h, time.gmtime(riseSet[1] * 3600))   # 12 hour clock
            
            elif args[0] == "24h":
                res = time.strftime( self._timeFormat_24h)   # 24 hour clock
                
            elif args[0] == "12h":
                res = time.strftime( self._timeFormat_12h)   # 12 hour clock
        else:
            res = time.strftime( self._timeFormat_12h)   # 12 hour clock

        return { 'stserr': None, 'stsval': res }

    @turbogears.expose(template="WebBrickGateway.templates.singleValue", format="xml", content_type="text/xml")
    def messages(self):
        """
        return a string containing recent messages. With CR between messages.
        """
        self._clearOldMessages()

        global _currentMesages
        nr = 0
        s = ""
        for msg in _currentMesages:
            s = s + "\n"+ msg._txt
            nr += 1
            if nr > 5:
                break   # stop at 5 messages

        return { 'stserr': None, 'stsval': s }

    @turbogears.expose()
    def removemessage(self, tag ):
        """
        update the messages list
        """
        self._clearOldMessages()
        # if no tag then do not attempt delete
        if tag:
            global _currentMesages
            idx = len(_currentMesages)
            while idx > 0:
                idx -= 1
                msg = _currentMesages[idx]
                if ( msg._tag == tag ):
                    # remove from list
                    self._logger.debug( "removemessage(delete) %i:%s %s" % (msg._pri, msg._tag, msg._txt ) )
                    del _currentMesages[idx]
        return ""

    @turbogears.expose()
    def postmessage(self, msg, tag="", priority=4, validFor=300 ):
        """
        update the messages list
        """
		# tag may be blank and this will be suppressed in removemessage
        self.removemessage(tag)

        self._insertMessages( Message( msg, tag, priority, validFor ) )
        return ""


