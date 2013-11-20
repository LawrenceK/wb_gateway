# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: DummyRouter.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Some test helpers for testing event handlers. Uses a SuperGlobal to save state.
#
import logging
import sys
import unittest

from EventLib.Event import Event, makeEvent
from EventHandlers.BaseHandler import *

# a dummy router to log data
class DummyRouter(object):
    def __init__( self ):
        self._log = logging.getLogger( "DummyRouter" )
        self._subs = list()
        self._unsubs = list()
        self._pubs = list()

    def logMe(self):
        # write all stuff to the log
        self._log.debug( "logMe" )

    def subscribe(self, interval, handler, evtype=None, source=None):
        self._subs.append( (interval,handler,evtype,source) )
        self._log.debug( "subscribe: %i, %s, %s, %s" % (interval,handler,evtype,source) )

    def unsubscribe(self, handler, evtype=None, source=None):
        self._unsubs.append( (handler,evtype,source) )
        self._log.debug( "unsubscribe: %s, %s, %s" % (handler,evtype,source) )

    def publish(self, source, event):
        self._pubs.append( (source,event) )
        self._log.debug( "publish: %s, %s" % (source,event) )

