# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestBaseHandler.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Some test helpers for testing event handlers. Uses a SuperGlobal to save state.
#
import sys
import unittest

from EventLib.Event import Event, makeEvent
from EventHandlers.BaseHandler import *
from DummyRouter import *

testCfg = {
    'module':'EventHandlers.BaseHandler',
    'name':'BaseHandler',
    'eventtype':
        {
        'type':"local/url",
            'eventsource':
            [
                {
                'source':"local/BoilerOn",
	        'event':
                    {
		    'url':
                        {
                            'cmd':"GET",
                            'address':"localhost:20999",
                            'uri':"/BoilerOn",
                        }
                    }
                },
                {
                'source':"local/HwOn",
	        'event':
                    {
		    'params':
                        [
                        ],
		    'url':
                        {
                            'cmd':"GET",
                            'address':"localhost:20999",
                            'uri':"/HwOn",
                        }
                    }
                }
            ]
        }
    }

class DummyHandler(BaseHandler):
    def __init__ (self, localRouter):
        super(DummyHandler,self).__init__( localRouter )
        self._actionCount = 0
        self._actions = list()

    def configureActions( self, eventDict ):
        self._log.debug( 'configureActions %s' % ( eventDict ) )
        self._actionCount = self._actionCount + 1
        return self._actionCount
        
    def doActions( self, actions, inEvent ):
        self._actions.append(actions)
        self._log.debug( 'doActions %s %s' % ( actions, inEvent ) )

class TestBaseHandler(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestBaseHandler" )
        self._log.debug( "\n\nsetUp" )
        self._router = DummyRouter()

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    # helpers, these are event router functions used to log the calls from the base handler.

    # Actual tests follow

    def testCreate(self):
        self._log.debug( "\ntestCreate" )

        bh = BaseHandler(self._router)
        self.assertNotEqual( bh, None)

    def testConfigure(self):
        self._log.debug( "\ntestConfigure" )

        bh = BaseHandler(self._router)
        self.assertNotEqual( bh, None)
        bh.configure(testCfg)
        bh.start()
        bh.stop()
        # check subs and unsubs.
        self.assertNotEqual( len(self._router._subs), 0 )
        self.assertNotEqual( len(self._router._unsubs), 0 )

    def testPublish(self):
        self._log.debug( "\ntestPublish" )

        dh = DummyHandler(self._router)
        self.assertNotEqual( dh, None)
        dh.configure(testCfg)
        dh.start()
        # check subs and unsubs.
        self.assertNotEqual( len(self._router._subs), 0 )

        # send an event and check for action
        dh.handleEvent( Event("local/url", "local/BoilerOn", {'payload':'payload'} ) )

        self.assertNotEqual( len(dh._actions), 0 )

        dh.stop()
        self.assertNotEqual( len(self._router._unsubs), 0 )

from MiscLib import TestUtils
def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testCreate"
            , "testConfigure"
            , "testPublish"
            ],
        "zzcomponent":
            [ "testComponents"
            ],
        "zzintegration":
            [ "testIntegration"
            ],
        "zzpending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestBaseHandler, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestBaseHandler.log", getTestSuite, sys.argv)
