# $Id: TestWbEvent.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for WebBrick library functions (WbAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address
#
# It also assumes that the webbrick has been factory reset

import sys
import time
import unittest
import types

sys.path.append("../..")

from WebBrickLibs.WbEvent        import *

from MiscLib.DomHelpers  import *

xmlEventStr = """<newEvent type="http://id.webbrick.co.uk/events/time/delta" source="delta">
    <delaySeconds>4</delaySeconds>
    <!-- After the timer a new event is created -->
    <eventType>delta/delay</eventType>
    <eventSource>delta/delay</eventSource>
</newEvent>
"""

xmlMatch1 = """<eventMatch type="typeStr" source="sourceStr">
    <params><key>value</key></params>
</eventMatch>
"""

class TestWbEvent(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    # Actual tests follow
    def testWbEvent(self):
        evt = WbEvent( 'typeStr', 'sourceStr' )
        self.assertEqual( evt.type(), 'typeStr' )
        self.assertEqual( evt.source(), 'sourceStr' )

    def testWbEventOther(self):
        other = { 'key':'value' }
        evt = WbEventOther( 'typeStr', 'sourceStr', other )
        self.assertEqual( evt.type(), 'typeStr' )
        self.assertEqual( evt.source(), 'sourceStr' )
        self.assertEqual( evt.other_data()['key'], 'value' )

    def testWbEventXml(self):
        xml = parseXmlString( xmlEventStr )
        evt = WbEventFromXml( getNamedElem(xml, 'newEvent') )
        self.assertEqual( evt.type(), 'http://id.webbrick.co.uk/events/time/delta' )
        self.assertEqual( evt.source(), 'delta' )
        self.assertEqual( evt.other_data()['delaySeconds'], '4' )
        self.assertEqual( evt.other_data()['eventType'], 'delta/delay' )
        self.assertEqual( evt.other_data()['eventSource'], 'delta/delay' )

    def testWbEventMatch(self):
        evt1 = WbEventOther( 'typeStr', 'sourceStr', { 'key':'value' } )
        evt2 = WbEventOther( 'typeStr', 'sourceStr2', { 'key':'value' } )
        evt3 = WbEventOther( 'typeStr2', 'sourceStr', { 'key':'value' } )
        evt4 = WbEventOther( 'typeStr', 'sourceStr', { 'key':'value2' } )

        match1 = WbEventMatch( 'typeStr', 'sourceStr' )
        self.assert_( match1.test( evt1 ) )
        self.assert_( not match1.test( evt2 ) )
        self.assert_( not match1.test( evt3 ) )
        self.assert_( match1.test( evt4 ) )
        self.assertEqual( match1.type(), 'typeStr' )
        self.assertEqual( match1.source(), 'sourceStr' )

        match2 = WbEventMatch( 'typeStr' )
        self.assert_( match2.test( evt1 ) )
        self.assert_( match2.test( evt2 ) )
        self.assert_( not match2.test( evt3 ) )
        self.assert_( match2.test( evt4 ) )

        match3 = WbEventMatch( '', 'sourceStr' )
        self.assert_( match3.test( evt1 ) )
        self.assert_( not match3.test( evt2 ) )
        self.assert_( match3.test( evt3 ) )
        self.assert_( match3.test( evt4 ) )

        match4 = WbEventMatch( 'typeStr', 'sourceStr',  { 'key':'value' } )
        self.assert_( match4.test( evt1 ) )
        self.assert_( not match4.test( evt2 ) )
        self.assert_( not match4.test( evt3 ) )
        self.assert_( not match4.test( evt4 ) )

    def testWbEventMatchXml(self):
        match = WbEventMatch()
        match.configure( getNamedElem( parseXmlString( xmlMatch1 ), "eventMatch" ) )

        self.assert_( match.test( WbEventOther( 'typeStr', 'sourceStr', { 'key':'value' } ) ) )
        self.assert_( not match.test( WbEvent( 'typeStr', 'sourceStr' ) ) )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestWbEvent("testWbEvent"))
    suite.addTest(TestWbEvent("testWbEventOther"))
    suite.addTest(TestWbEvent("testWbEventXml"))
    suite.addTest(TestWbEvent("testWbEventMatch"))
    suite.addTest(TestWbEvent("testWbEventMatchXml"))
    return suite

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner()
    runner.run(getTestSuite())
    