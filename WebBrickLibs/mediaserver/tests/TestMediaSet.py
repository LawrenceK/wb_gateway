# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestMediaSet.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for VLC access library functions (VlcAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#

import sys
import types
import logging
import time
import unittest

sys.path.append("../..")

from mediaserver.MediaInterface import *
from mediaserver.MediaSet       import MediaSet

from MiscLib.DomHelpers import *

testConfigMediaSet = """<?xml version="1.0" encoding="iso-8859-1"?>
    <mediaaccess>
        <AccessGood module="AccessGood" >Access Good</AccessGood>
        <AccessBad module="AccessBad" >Access Bad</AccessBad>
    </mediaaccess>
"""

class TestMediaSet(unittest.TestCase):

    def setUp(self):
        self._mediaSet = MediaSet()
        self._mediaSet.configure( parseXmlString(testConfigMediaSet) )
        return

    def tearDown(self):
        return

    def assertUnicode( self, str, match ):
        self.assertEqual( type(str), types.UnicodeType )
        self.assertEqual( type(match), types.UnicodeType )
        self.assertEqual( str, match )

    # Actual tests follow
    def testGetStatus(self):
        self.assertUnicode( self._mediaSet.status( "AccessGood" ), u'<status name="AccessGood"><state>1</state><track>Test Track</track><position>119</position><duration>500</duration></status>' )
        self.assertEqual( self._mediaSet.status( "AccessBad" ), None )
        self.assertUnicode( self._mediaSet.status( "noKnownInterface" ), u'<error>No Such Interface noKnownInterface</error>' )

        self.assertUnicode( self._mediaSet.volume( "AccessGood" ), u'<vol>40</vol>' )
        self.assertEqual( self._mediaSet.volume( "AccessBad" ), None )
        self.assertUnicode( self._mediaSet.volume( "noKnownInterface" ), u'<error>No Such Interface noKnownInterface</error>' )

    def testCommands(self):
        self.assertEqual( self._mediaSet.command("AccessGood", "stop"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "stop"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "play"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "play"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "pause"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "pause"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "togglePause"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "togglePause"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "next"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "next"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "prev"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "prev"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "forward"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "forward"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "rewind"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "rewind"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.setPosition( "AccessGood", 100), None )
        self.assertUnicode( self._mediaSet.setPosition("AccessBad", 100), u'Error' )

        self.assertEqual( self._mediaSet.setVolume( "AccessGood", 100), None )
        self.assertUnicode( self._mediaSet.setVolume("AccessBad", 100), u'Error' )

        self.assertEqual( self._mediaSet.selectPlaylist("AccessGood", '1.1'), None )
        self.assertUnicode( self._mediaSet.selectPlaylist("AccessBad",'1.1'), u'Error' )

        self.assertEqual( self._mediaSet.selectTrack("AccessGood", '1.1.1'), None )
        self.assertUnicode( self._mediaSet.selectTrack("AccessBad", '1.1.1'), u'Error' )

        self.assertEqual( self._mediaSet.command("AccessGood", "toggleMute"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "toggleMute"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "volup"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "volup"), u'<error>Error</error>' )

        self.assertEqual( self._mediaSet.command("AccessGood", "voldown"), None )
        self.assertUnicode( self._mediaSet.command("AccessBad", "voldown"), u'<error>Error</error>' )

        self.assertUnicode( self._mediaSet.command("AccessGood", "xxCommand"), u"<error>No Such Command xxCommand</error>" )
        self.assertUnicode( self._mediaSet.command("AccessBad", "xxCommand"), u"<error>No Such Command xxCommand</error>" )

    def testPlaylist(self):
        # first the playlists array
        self.assertUnicode( self._mediaSet.playlists("AccessGood"), u'<playlists><playlist id="1.1" current="yes">Playlist 1</playlist><playlist id="1.2">Playlist 2</playlist></playlists>' )
        self.assertEqual( self._mediaSet.playlists("AccessBad"), None )
       
        self.assertUnicode( self._mediaSet.playlist("AccessGood"), u'<playlist><track id="1.1.1" current="yes">Track 1</track><track id="1.1.2">Track 2</track><track id="1.1.3">Track 3</track></playlist>' )
        self.assertEqual( self._mediaSet.playlist("AccessBad"), None )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestMediaSet("testGetStatus"))
    suite.addTest(TestMediaSet("testCommands"))
    suite.addTest(TestMediaSet("testPlaylist"))
    return suite

if __name__ == "__main__":
#    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner()
    runner.run(getTestSuite())
    