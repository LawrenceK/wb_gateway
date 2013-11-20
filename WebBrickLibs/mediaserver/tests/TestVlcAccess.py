# $Id: TestVlcAccess.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for VLC access library functions (VlcAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires VLC to be
# running on the test host.

import sys
import logging
import time
import unittest

sys.path.append("../..")

from mediaserver.VlcAccess      import *
from mediaserver.MediaInterface import *

class TestVlcAccess(unittest.TestCase):

    def setUp(self):
        self._mediaAccess = VlcAccess()
        return

    def tearDown(self):
        return

    # Actual tests follow
    def testGetStatus(self):
        st = self._mediaAccess.getState()
        logging.debug( "position %s" % st )
        assert st != MediaState.UNKNOWN

        ct = self._mediaAccess.getCurrentTrack()
        if ( ct != None ):
            logging.debug( "currentTrack %s %s" % ct )
        assert ct != None

        pos = self._mediaAccess.getPosition()
        logging.debug( "position %i" % pos )
        assert pos != None

    def testCommands(self):
        self._mediaAccess.stop()
        time.sleep( 1.0 )
        assert self._mediaAccess.getState() == MediaState.STOP

        self._mediaAccess.play()
        time.sleep( 5.0 )
        assert self._mediaAccess.getState() == MediaState.PLAY

        self._mediaAccess.pause()
        time.sleep( 2.0 )
        state = self._mediaAccess.getState() 
        assert (state == MediaState.PAUSED) or (state == MediaState.STOP)

        self._mediaAccess.play()
        time.sleep( 5.0 )
        assert self._mediaAccess.getState() == MediaState.PLAY

        logging.debug( "currentTrack %s %s" % self._mediaAccess.getCurrentTrack() )

        self._mediaAccess.nextTrack()
        time.sleep( 5.0 )
        assert self._mediaAccess.getState() == MediaState.PLAY
        logging.debug( "currentTrack %s %s" % self._mediaAccess.getCurrentTrack() )

        self._mediaAccess.play()
        time.sleep( 5.0 )
        assert self._mediaAccess.getState() == MediaState.PLAY

        self._mediaAccess.prevTrack()
        time.sleep( 5.0 )
        assert self._mediaAccess.getState() == MediaState.PLAY
        logging.debug( "currentTrack %s %s" % self._mediaAccess.getCurrentTrack() )

        self._mediaAccess.play()
        time.sleep( 5.0 )
        assert self._mediaAccess.getState() == MediaState.PLAY

        self._mediaAccess.stop()
        time.sleep( 2.0 )
        assert self._mediaAccess.getState() == MediaState.STOP

    def testPlaylist(self):
        # check that vlc is stopped.
        self._mediaAccess.stop()
        time.sleep( 1.0 )
        assert self._mediaAccess.getState() == MediaState.STOP

        # first the playlists array
        playlists = self._mediaAccess.getPlaylists()
        assert playlists != None
        assert len(playlists) == 1
        logging.debug( "playlists %s" % playlists )
       
        playlist = self._mediaAccess.getPlaylistContents()
        assert playlist != None
        assert len(playlist) > 0
        logging.debug( "playlist %s" % str(playlist) )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestVlcAccess("testGetStatus"))
    suite.addTest(TestVlcAccess("testCommands"))
    suite.addTest(TestVlcAccess("testPlaylist"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner()
    runner.run(getTestSuite())
    