# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestEventLogger.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Some test helpers for testing event handlers. Uses a SuperGlobal to save state.
#

import logging, time

from EventLib.Event import Event, makeEvent

from EventLib.EventAgent import EventAgent
from EventLib.EventHandler import EventHandler

from EventHandlers.BaseHandler import BaseHandler
from EventHandlers.Utils import *

from WebBrickLibs.ParameterSet import ParameterSet

# The events we have seen
_events = list()
_log = logging.getLogger( "EventHandlers.tests.TestEventLogger" )

def logEvents():
    idx = 0
    for ev in _events:
        _log.info( "%u: %s %s %s" % (idx, ev.getType(),ev.getSource(),ev.getPayload()) )
        idx = idx + 1

def clearEvents():
    global _events
    _events = list()

# Minimal event interface
class TestEventLogger( BaseHandler ):
    def __init__ (self, localRouter):
        self._log = logging.getLogger( "EventHandlers.tests.TestEventLogger" )
        super(TestEventLogger,self).__init__( localRouter )
        global _events
        _events = list()
        
    def doActions( self, actions, inEvent ):
        """
        Save it so we can see what happens.
        """
        global _events
        _events.append( inEvent )
           
def expectAtLeastNevents(cnt, maxtime=2):
    idx = int(maxtime/0.05)
    while (len(_events) < cnt) and (idx > 0):
        time.sleep(0.05)
        idx = idx - 1

    if ( len(_events) < cnt):
        logEvents()
        return False

    return True

def expectNevents(cnt, maxtime=2):
    idx = int(maxtime/0.05)
    while (len(_events) < cnt) and (idx > 0):
        time.sleep(0.05)
        idx = idx - 1

    if ( len(_events) != cnt):
        logEvents()
        return False

    return True
