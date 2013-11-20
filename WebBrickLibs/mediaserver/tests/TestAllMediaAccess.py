# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: TestAllMediaAccess.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for VLC access library functions (VlcAccess.py)
# See http://pyunit.sourceforge.net/pyunit.html
#

# NOTES
# odities, albums sometimes apear as play list entries and cannot be setplaylist
# needs the remote server running.

import sys
import types
import logging
import time
import unittest
import re
from xml.dom import *

sys.path.append("../..")

import TestMediaSet
import TestMediaAccess

from mediaserver.MediaInterface import *
from mediaserver.MediaSet       import MediaSet

from MiscLib.DomHelpers         import *

configMediaAccess="""
<mediaaccess>
    <VlcAccess module="VlcAccess" location="vlcplayer:8082" >VlcAccess</VlcAccess>
    <ITunesDirect module="ITunesAccess" >ITunes Direct</ITunesDirect>
    <ITunesInDirect module="HttpAccess" remoteName="ITunesDirect" location="itunesserver:8081" >ITunes In Direct</ITunesInDirect>
    <AccessGood module="AccessGood" >Access Good</AccessGood>
    <AccessBad module="AccessBad" >Access Bad</AccessBad>
    <AccessGoodInDirect module="HttpAccess" remoteName="AccessGood" location="localhost:8081" >Access Good InDirect</AccessGoodInDirect>
</mediaaccess>
"""

class TestAllMediaAccess(unittest.TestCase):

    def setUp(self):
        self._mediaSet = MediaSet()
        self.testNumeric = re.compile("\d*")        
        self._mediaSet.configure( parseXmlString(configMediaAccess))
        return

    def tearDown(self):
        return

    def assertUnicodeType( self, str ):
        self.assertEqual( type(str), types.UnicodeType )

    def assertUnicodeEqual( self, str, match ):
        self.assertUnicodeType( str )
        self.assertUnicodeType( match )
        self.assertEqual( str, match )

    def verifyXml( self, xmlStr ):
        # expect error if load fails
        self.assertUnicodeType( xmlStr )

        try:
            xmlDom = parseXmlString( xmlStr )
        except Exception, e:
            logging.exception( "bad Xml %s " % xmlStr )
            self.assert_( False, "Bad Xml" )

    def verifyNumeric( self, node ):
        numStr = getElemText( node )
        self.assert_( self.testNumeric.match(numStr), numStr )

    def verifyStatus( self, xmlStr ):
        self.assertUnicodeType( xmlStr )
        xmlDom = parseXmlString(xmlStr)

        self.assertEqual( xmlDom.nodeType, Node.DOCUMENT_NODE )
        subnodes = xmlDom.getElementsByTagName('status')
        self.assertEqual( len(subnodes), 1 )
        statusNode = subnodes[0]

        subnodes = statusNode.getElementsByTagName('state')
        self.assertEqual( len(subnodes), 1 )
        subnode = subnodes[0]
        self.assertEqual( subnode.nodeType, Node.ELEMENT_NODE )
        self.verifyNumeric( subnode )

        subnodes = statusNode.getElementsByTagName('track')
        self.assertEqual( len(subnodes), 1 )
        subnode = subnodes[0]
        self.assertEqual( subnode.nodeType, Node.ELEMENT_NODE )

        subnodes = statusNode.getElementsByTagName('position')
        self.assertEqual( len(subnodes), 1 )
        subnode = subnodes[0]
        self.assertEqual( subnode.nodeType, Node.ELEMENT_NODE )
        self.verifyNumeric( subnode )
        # should also be numeric or blank

        subnodes = statusNode.getElementsByTagName('duration')
        self.assertEqual( len(subnodes), 1 )
        subnode = subnodes[0]
        self.assertEqual( subnode.nodeType, Node.ELEMENT_NODE )
        self.verifyNumeric( subnode )

    def verifyVolume( self, xmlStr ):
        self.assertUnicodeType( xmlStr )

        # <status name="AccessGood"><state>1</state><track>Test Track</track><position>119</position></status>
        # expect error if load fails
        xmlDom = parseXmlString(xmlStr)
        self.assertEqual( xmlDom.nodeType, Node.DOCUMENT_NODE )

        subnodes = xmlDom.getElementsByTagName('vol')
        self.assertEqual( len(subnodes), 1 )
        subnode = subnodes[0]
        self.assertEqual( subnode.nodeType, Node.ELEMENT_NODE )
        # should also be numeric
        self.verifyNumeric( subnode )

    # Actual tests follow
    def testAny( self, name ):
        self.verifyStatus( self._mediaSet.status( name ) )
        self.verifyVolume( self._mediaSet.volume( name ) )

        self.assertEqual( self._mediaSet.command( name, "stop"), None )
        self.assertEqual( self._mediaSet.command( name, "play"), None )
        self.assertEqual( self._mediaSet.command( name, "pause"), None )
        self.assertEqual( self._mediaSet.command( name, "play"), None )

        self.assertEqual( self._mediaSet.command( name, "togglePause"), None )
        self.assertEqual( self._mediaSet.command( name, "togglePause"), None )

        self.assertEqual( self._mediaSet.command( name, "next"), None )
        self.assertEqual( self._mediaSet.command( name, "prev"), None )
        self.assertEqual( self._mediaSet.command( name, "forward"), None )
        self.assertEqual( self._mediaSet.command( name, "rewind"), None )
        self.assertEqual( self._mediaSet.setPosition( name, 100 ), None )
        self.assertEqual( self._mediaSet.setVolume( name, 50 ), None )

        self.assertEqual( self._mediaSet.command( name, "toggleMute"), None )
        self.assertEqual( self._mediaSet.command( name, "toggleMute"), None )

        self.assertEqual( self._mediaSet.command( name, "volup"), None )
        self.assertEqual( self._mediaSet.command( name, "voldown"), None )
        self.assertUnicodeEqual( self._mediaSet.command( name, "xxCommand"), u"<error>No Such Command xxCommand</error>" )

        playlists = self._mediaSet.playlists( name )
        self.assertUnicodeType( playlists )
        self.verifyXml( playlists )

        # look for first entry in playlists
        xmlDom = parseXmlString(playlists)
        id = getNamedNodeAttrText( xmlDom, 'playlist', 'id' )
        self.assertNotEqual( id, None )
        self.assertEqual( self._mediaSet.selectPlaylist( name, id), None )
        time.sleep(10)
        self.assertEqual( self._mediaSet.command( name, "stop"), None )

        playlist = self._mediaSet.playlist( name )
        self.assertUnicodeType( playlist )
        self.verifyXml( playlist )

        # look for first entry in playlist
        xmlDom = parseXmlString(playlist)

        id = None
        tracks = xmlDom.getElementsByTagName('track')
        if tracks and len(tracks) > 0:
            track = tracks[2]
            id = track.getAttribute('id')

#        id = getNamedNodeAttrText( xmlDom, 'track', 'id' )
        self.assertNotEqual( id, None ) # if no playlist loaded this will fail (i.e. VLC)
        self.assertEqual( self._mediaSet.selectTrack( name, id), None ) # Itunes has a problem with selectTrack

#        self.assertEqual( self._mediaSet.command( name, "stop"), None )

    def testVlcAccess(self):
        # VLC needs to be running and have a playlist setup.
        self.testAny( "VlcAccess" )

    def testITunesAccess(self):
        self.testAny( "ITunesDirect" )

    def testITunesAccessInDirect(self):
        # TaskRunner needs to be running with the MediaOverHttpServer Task.
        self.testAny( "ITunesInDirect" )

    def testGood(self):
        self.testAny( "AccessGood" )

    def testGoodInDirect(self):
        # TaskRunner needs to be running with the MediaOverHttpServer Task.
        self.testAny( "AccessGoodInDirect" )

# Code to run unit tests directly from command line.
# Constructing the suite manually allows control over the order of tests.
def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestMediaSet.getTestSuite())
    suite.addTest(TestMediaAccess.getTestSuite())
    suite.addTest(TestAllMediaAccess("testGood"))
    suite.addTest(TestAllMediaAccess("testGoodInDirect"))
    suite.addTest(TestAllMediaAccess("testVlcAccess"))
    suite.addTest(TestAllMediaAccess("testITunesAccess"))
    suite.addTest(TestAllMediaAccess("testITunesAccessInDirect"))
    return suite

if __name__ == "__main__":
#    logging.basicConfig(level=logging.DEBUG)


    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestAllMediaAccess( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.INFO)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)
