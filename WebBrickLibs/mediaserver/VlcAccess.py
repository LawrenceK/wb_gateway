# $Id: VlcAccess.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Copyright L.P.Klyne 2013
#
#
#   The purpose of this class is to define a standard interface to any media player.
#   this could be video, audio or other.
#
#   The aim is to make it simple to add new media players to the Gateway without needing to
#   modify the Gateway, just add a new python module and update configuration.
#
#
import logging

from WebBrickLibs.WbAccess import *
from MiscLib.DomHelpers    import *
from MediaInterface        import *

from xml.sax.saxutils import escape

_log = logging.getLogger( "WebBrickLibs.MediaServer.VlcAccess" )
 
 
#
# VLC interface
# Uses TELNET/socket interface
#
class VlcAccess(MediaInterface, SoundInterface):

    # where is VLC running
    _VLC_HTTP   = "localhost:8082"

    def __init__(self):
        self.state = MediaState.ERROR
        self.vlc_status = None
        self.vlc_playlist = None
        self.unMuteVol = 0

    # send a command to VLC, XML dom of the current status is retrived and cached
    def doVlcCommand( self, command ):
        cmd = "/requests/status.xml"
        if ( command and (len(command) > 0 ) ):
            cmd = cmd + "?command=" + command
        cmd = cmd + " HTTP/1.1"

        try:
            # does this need escaping?
            _log.debug( 'Command %s' % cmd )
            self.vlc_status = GetHTTPXmlDom( self._VLC_HTTP, cmd)
            _log.debug( 'Status %s' % self.vlc_status )
        except Exception, e:
            _log.exception( 'doVlcCommand Error' )
            return MediaState.ERROR

        # Locate state entry
        if self.vlc_status:
            s = getNamedNodeText( self.vlc_status, "state" )
            if ( s == "playing" ):
                return MediaState.PLAY
            elif ( s == "paused" ):
                return MediaState.PAUSED
            elif ( s == "stop" ):
                return MediaState.STOP

        return MediaState.UNKNOWN

    #
    # return in range 0 to 100
    #
    def convertVolume( self ):
        s = getNamedNodeText( self.vlc_status, "volume" )
        _log.debug( 'Player Volume %s' % s )
        return (int(s) * 100) / 512

    # MediaInterface:

    def configure( self, xml ):
        loc = xml.getAttribute( "location" )
        _log.debug( "configure location = %s" % loc )
        if ( loc ):
            self._VLC_HTTP = loc
        else:
            return "VLC access location not configured"
        return None

    def getStatus( self ):
        return u'<status><state>%i</state><track>%s</track><position>%s</position><duration>%s</duration></status>' % \
                ( self.doVlcCommand( None ),self.currentTrack(),getNamedNodeText( self.vlc_status, "time"),getNamedNodeText( self.vlc_status, "length" ) )

    def currentTrack( self ):
        # return a string describing the current track
        # Need to locate "current" in playlist

        self.vlc_playlist = GetHTTPXmlDom( self._VLC_HTTP, "/requests/playlist.xml")
        for node in self.vlc_playlist.getElementsByTagName("leaf"):
            if node.getAttribute("current"):
                return node.getAttribute("name")
        return u""

    def setPosition( self, newPosition ):
        # change the current location in the current track.
        # Format is variable, but should allow relative and absolute positioning.
        #   <nn> absolute in seconds.
        #   +-<nn> relative in seconds
        #   <nn>% absolute in percent
        #   +-<nn>% relative in percent
        self.doVlcCommand( "seek&val="+str(newPosition) )

    def stop( self ):
        # stop the media playing at the current point.
        # if already playing does nothing.
        self.doVlcCommand( "pl_stop" )

    def play( self ):
        # start the media playing at the current point, if state = paused does resume.
        # if already playing does nothing.
        if ( not self.vlc_playlist ):
            self.getPlaylistContents()
        entries = self.vlc_playlist.getElementsByTagName("leaf")
        if ( len(entries) > 0 ):
            state = self.doVlcCommand( None )
            if state == MediaState.PAUSED:
                # resume
                self.doVlcCommand( "pl_pause&id=" + entries[0].getAttribute("id") )
            elif state != MediaState.PLAY:
                self.doVlcCommand( "pl_play&id=" + entries[0].getAttribute("id") )

    def nextTrack( self ):
        # move to next track
        self.doVlcCommand( "pl_next" )

    def prevTrack( self ):
        # move to previous track
        self.doVlcCommand( "pl_previous" )

    def pause( self ):
        # pause media.
        if self.doVlcCommand( None ) != MediaState.PAUSED:
            self.doVlcCommand( "pl_pause" )

    def togglePause( self ):
        self.doVlcCommand( "pl_pause" )

    def fastForward( self ):
        # play forward fast.
        pass

    def fastReverse( self ):
        # play backwards fast.
        pass

    def getPlaylists( self ):
        # return list of known playlists.
        # each entry consists of a displayable name and an internal Id that can be passed to selectPlaylist
        return u"<playlists><playlist name='VLC default' id='1' /></playlists>"

    def getPlaylistContents( self ):
        # return list of current playlist content.
        # each entry consists of a displayable name and an internal Id that can be passed to selectTrack
        self.vlc_playlist = GetHTTPXmlDom( self._VLC_HTTP, "/requests/playlist.xml")
        # turn playlist into array
        result = u'<playlist>'
        for node in self.vlc_playlist.getElementsByTagName("leaf"):
            result = result + u'<track name ="%s" id="%s" />\n' % \
                    ( node.getAttribute("name"), node.getAttribute("id") )
        result = result + u'</playlist>'
        return result

    def selectPlaylist( self, id ):
        # change to playlist identified by id.
        # There is only a single playlist for VLC.
        if ( id != '1' ):
            return "No Such PlayList"
        return None

    def selectTrack( self, id ):
        # change to track in current playlist identified by id.
        # id should be taken from the results of getPlayListContents
        if id:
            self.doVlcCommand( "pl_play&id=" + id )

    # End of mediaInterface.

    # SoundInterface:
    def volume( self ):
        # return the current volume as a number between 0 and 100

        # retrive current status.
        self.doVlcCommand( None )
        return u'<vol>%i</vol>' % self.convertVolume()

    def toggleMute( self ):
        self.doVlcCommand( None )
        cur = self.convertVolume()
        self.doVlcCommand( "volume&val=%s" % self.unMuteVol )
        self.unMuteVol = cur
#        return u'<vol>%i</vol>' % self.convertVolume()

    def volUp( self, step = None ):
        # step volume up by an amount based on step
        # step may be None, 1,2,3 where None & 1 is small step 1%, 2 is medium step 5% and 3 is large step 10%
        self.doVlcCommand( "volume&val=%2B" + str(5*self.volStep(step)))

    def volDown( self, step = None ):
        # step volume down by an amount based on step
        # step may be 1,2,3 where 1 is small step 1%, 2 is medium step 5% and 3 is large step 10%
        self.doVlcCommand( "volume&val=%2D" + str(5*self.volStep(step)))

    def setVolume( self, newVolume ):
        # step volume down by an amount based on step
        # step may be 1,2,3 where 1 is small step 1%, 2 is medium step 5% and 3 is large step 10%
        self.doVlcCommand( "volume&val=" + str(newVolume))

    # End of SoundInterface.

# End of ITunesInterface.
