# $Id: TestUtils.py 3222 2009-07-14 15:32:00Z simon.hughes $
#
# Some test helpers for testing event handlers. Uses a SuperGlobal to save state.
#
import sys
import unittest

from EventLib.Event import Event, makeEvent
from EventHandlers.Utils import *

class TestUtilsUnit(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestUtils" )
        self._log.debug( "\n\nsetUp" )

    def tearDown(self):
        self._log.debug( "\n\ntearDown" )

    # Actual tests follow

    def testMakeEvent(self):
        self._log.debug( "\ntestMakeEvent" )

        newEvent = makeNewEvent( 
                { 'type':'newtype', 
                        'source':'newsource', 
                        'other_data':{'data':'data','data1':'data1','data2':'data2' },
                        'copy_other_data':{'data1':'data1', 'data2':'data2' } 
                }, 
                makeEvent('oldType', 'oldSource', {'data1':'olddata1'} ), 
                {'data2':'xtradata2'} )

        self.assertNotEqual( newEvent, None)
        self.assertEqual( newEvent.getType(), "newtype" )
        self.assertEqual( newEvent.getSource(), "newsource" )
        od = newEvent.getPayload()
        self.assertEqual( od['data'], "data" )
        self.assertEqual( od['data1'], "olddata1" )
        self.assertEqual( od['data2'], "xtradata2" )
    
    def testMakeEventSubsitution(self):
        self._log.debug( "\ntestMakeEventSubsitution" )

        newEvent = makeNewEvent( 
                { 'type':'%(Newtype)s', 
                        'source':'%(Newsource)s', 
                        'other_data':{'data':'data','data1':'TEST%(Subdata)sTEST','data2':'data2' },                      
                }, 
                makeEvent('oldType', 'oldSource', {'data1':'olddata1','Newtype':'SubType','Newsource':'SubSource','Subdata':'SUBBEDDATA'} ), 
                {'data2':'xtradata2'} )
        print newEvent
        self.assertNotEqual( newEvent, None)
        self.assertEqual( newEvent.getType(), "SubType" )
        self.assertEqual( newEvent.getSource(), "SubSource" )
        od = newEvent.getPayload()
        self.assertEqual( od['data'], "data" )
        self.assertEqual( od['data1'], "TESTSUBBEDDATATEST" )
        
    def testDummy(self):
       return

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
            [ 
            "testMakeEvent",
            "testMakeEventSubsitution"
            ],
        "component":
            [ "testDummy"
            ],
        "integration":
            [ "testDummy"
            ],
        "pending":
            [ "testDummy"
            ]
        }
    return TestUtils.getTestSuite(TestUtilsUnit, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestUtils.log", getTestSuite, sys.argv)
