# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: Event.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
"""
Define a type for basic events, and associated functions.
"""

from URI import EventDefaultType

class Event(object):
    """
    Represents a basic event.
    """

    def __init__(self, evtype, source, payload):
        """
        Initialize a new event object
        """
        self._evtype  = evtype
        self._source  = source
        self._payload = payload

    def __eq__(self,other):
        return  ( other
            and  isinstance(other, Event)
            and  (self._evtype  == other._evtype)
            and  (self._source  == other._source)
            and  (self._payload == other._payload))

    def __str__(self):
        return """Event(evtype="%s", source="%s")"""%(self._evtype, self._source)

    def getType(self):
        return self._evtype

    def getSource(self):
        return self._source

    def getPayload(self):
        return self._payload

def makeEvent(evtype=EventDefaultType,source="",payload=None):
    """
    Construct a new event object from the supplied values
    """
    return Event(evtype,source,payload)

# End.
