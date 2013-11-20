# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestMediaAccess.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for VLC access library functions (VlcAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#

import sys
import logging
import time
import unittest

sys.path.append("../..")

from MiscLib.DomHelpers import *

from mediaserver.AccessGood     import *
from mediaserver.AccessBad      import *
from mediaserver.MediaInterface import *

class TestMediaAccess(unittest.TestCase):

    def setUp(self):
        self._mediaAccessGood = AccessGood()
        self._mediaAccessBad = AccessBad()
        return

    def tearDown(self):
        return

    # Actual tests follow
    def testConfigure(self):
        xml = parseXmlString('<mediaaccess name="testName" attr1="attr1" attr2="attr2">display name</mediaaccess>')
        self.assertEqual( self._mediaAccessGood.configure(xml), None )
        self.assertEqual( self._mediaAccessBad.configure(xml), 'Error' )

    def testGetStatus(self):
        st = self._mediaAccessGood.getStatus()
        self.assertEqual( st, '<status name="AccessGood"><state>1</state><track>Test Track</track><position>119</position><duration>500</duration></status>' )
        st = self._mediaAccessBad.getStatus()
        self.assertEqual( st, None )
        self.assertEqual( self._mediaAccessGood.volume(), '<vol>40</vol>' )
        self.assertEqual( self._mediaAccessBad.volume(), None )

    def testCommands(self):
        self.assertEqual( self._mediaAccessGood.stop(), None )
        self.assertEqual( self._mediaAccessBad.stop(), 'Error' )

        self.assertEqual( self._mediaAccessGood.play(), None )
        self.assertEqual( self._mediaAccessBad.play(), 'Error' )

        self.assertEqual( self._mediaAccessGood.pause(), None )
        self.assertEqual( self._mediaAccessBad.pause(), 'Error' )

        self.assertEqual( self._mediaAccessGood.togglePause(), None )
        self.assertEqual( self._mediaAccessBad.togglePause(), 'Error' )

        self.assertEqual( self._mediaAccessGood.nextTrack(), None )
        self.assertEqual( self._mediaAccessBad.nextTrack(), 'Error' )

        self.assertEqual( self._mediaAccessGood.prevTrack(), None )
        self.assertEqual( self._mediaAccessBad.prevTrack(), 'Error' )

        self.assertEqual( self._mediaAccessGood.fastForward(), None )
        self.assertEqual( self._mediaAccessBad.fastForward(), 'Error' )

        self.assertEqual( self._mediaAccessGood.fastReverse(), None )
        self.assertEqual( self._mediaAccessBad.fastReverse(), 'Error' )

        self.assertEqual( self._mediaAccessGood.setPosition( 100), None )
        self.assertEqual( self._mediaAccessBad.setPosition(100), 'Error' )

        self.assertEqual( self._mediaAccessGood.setVolume( 100), None )
        self.assertEqual( self._mediaAccessBad.setVolume(100), 'Error' )

        self.assertEqual( self._mediaAccessGood.selectPlaylist('1.1'), None )
        self.assertEqual( self._mediaAccessBad.selectPlaylist('1.1'), 'Error' )

        self.assertEqual( self._mediaAccessGood.selectTrack('1.1.1'), None )
        self.assertEqual( self._mediaAccessBad.selectTrack('1.1.1'), 'Error' )

        self.assertEqual( self._mediaAccessGood.toggleMute(), None )
        self.assertEqual( self._mediaAccessBad.toggleMute(), 'Error' )

        self.assertEqual( self._mediaAccessGood.volUp(), None )
        self.assertEqual( self._mediaAccessBad.volUp(), 'Error' )

        self.assertEqual( self._mediaAccessGood.volDown(), None )
        self.assertEqual( self._mediaAccessBad.volDown(), 'Error' )

    def testPlaylist(self):
        # first the playlists array
        self.assertEqual( self._mediaAccessGood.getPlaylists(), '<playlists><playlist id="1.1" current="yes">Playlist 1</playlist><playlist id="1.2">Playlist 2</playlist></playlists>' )
        self.assertEqual( self._mediaAccessBad.getPlaylists(), None )
       
        self.assertEqual( self._mediaAccessGood.getPlaylistContents(), '<playlist><track id="1.1.1" current="yes">Track 1</track><track id="1.1.2">Track 2</track><track id="1.1.3">Track 3</track></playlist>' )
        self.assertEqual( self._mediaAccessBad.getPlaylistContents(), None )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestMediaAccess("testGetStatus"))
    suite.addTest(TestMediaAccess("testConfigure"))
    suite.addTest(TestMediaAccess("testCommands"))
    suite.addTest(TestMediaAccess("testPlaylist"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    runner = unittest.TextTestRunner()
    runner.run(getTestSuite())
    