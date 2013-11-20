# $Id: ITunesAccess.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Copyright L.P.Klyne 2013
#
#   The purpose of this class is to define a standard interface to any media player.
#   this could be video, audio or other.
#
#   The aim is to make it simple to add new media players to the Gateway without needing to
#   modify the Gateway, just add a new python module and update configuration.
#
#
import pythoncom
import win32com.client

import logging, string

from xml.sax.saxutils import escape

from MediaInterface import *

_log = logging.getLogger( "WebBrickLibs.MediaServer.ITunesAccess" )
 
#
# ITunes interface
# Uses COM and ONLY works on windows.
#
class ITunesAccess(MediaInterface, SoundInterface):

    def __init__(self):
        
        pythoncom.CoInitialize()    # need to initialize for all processing threads?
        # may need to be able to redo this.
        self.iTunes = win32com.client.Dispatch("iTunes.Application")
        _log.debug( "ITunesAccess %s" % self.iTunes )

    def _getITunesState( self ):
        iState = self.iTunes.PlayerState
        _log.debug( 'iTunes.PlayerState %i' % iState )
        if iState == 0:
            return MediaState.STOP
        elif iState == 1:
            return MediaState.PLAY
        elif iState == 2:
            return MediaState.FASTFORWARD
        elif iState == 3:
            return MediaState.REVERSE
        else:
            return MediaState.UNKNOWN

    # MediaInterface:

    def _position( self ):
        try:
            iState = self.iTunes.PlayerState
            if ( iState >= 1 ) and ( iState <= 3 ):
                # needs to be playing to do anything.
                return self.iTunes.PlayerPosition
        except Exception, e:
            _log.exception ( e )
        return 0

    def _currentTrackLength( self ):
        try:
            ct = self.iTunes.CurrentTrack
            if ct != None:
                return ct.Duration
        except Exception, e:
            _log.exception ( e )
        return 0

    def _currentTrack( self ):
        # return a string describing the current track
        _log.debug( 'currentTrack' )
        try:
            ct = self.iTunes.CurrentTrack
            if ct != None:
                return escape(u"%s : %s : %s" % (ct.Name,ct.Album,ct.Artist))
        except Exception, e:
            _log.exception ( e )
        return u""

    def getStatus( self ):
        return u'<status><state>%i</state><track>%s</track><position>%i</position><duration>%i</duration></status>' % \
            ( self._getITunesState(), self._currentTrack(), self._position(), self._currentTrackLength() )

    def setPosition( self, newPosition ):
        # change the current location in the current track.
        # Format is variable, but should allow relative and absolute positioning.
        #   <nn> absolute in seconds.
        #   +-<nn> relative in seconds
        #   <nn>% absolute in percent
        #   +-<nn>% relative in percent
        _log.debug( 'setPosition' )
        len = self.iTunes.CurrentTrack.Duration
        pc = newPosition[-1] == "%"
        if pc:
            newPosition = newPosition[:-1]  # loose last char
        #pc = True   # assume percentaage positioning.
        
        rel = (newPosition[0] == "+") or (newPosition[0] == "-")
        if ( rel ):
            neg = (newPosition[0] == "-")
            newPosition = newPosition[1:]  # loose first char

        newPosition = int(newPosition)  # convert to numeric

        if ( pc ):
            val = newPosition * len / 100
        else :
            val = newPosition

        if ( rel ):
            if neg :
                self.iTunes.PlayerPosition = self.iTunes.PlayerPosition - val
            else:
                self.iTunes.PlayerPosition = self.iTunes.PlayerPosition + val
        else:
            self.iTunes.PlayerPosition = val

        return None

    def stop( self ):
        # stop the media playing at the current point.
        # if already playing does nothing.
        self.iTunes.Stop()
        return

    def nextTrack( self ):
        # move to next track
        _log.debug( 'nextTrack' )
        self.iTunes.NextTrack()

    def prevTrack( self ):
        # move to previous track
        _log.debug( 'prevTrack' )
        self.iTunes.PreviousTrack()

    def play( self ):
        # start the media playing at the current point, if state = paused does resume.
        # if already playing does nothing.
        _log.debug( 'play' )
        self.iTunes.Play()

    def pause( self ):
        # pause media.
        _log.debug( 'pause' )
        self.iTunes.Pause()

    def togglePause( self ):
        # pause media.
        _log.debug( 'togglePause' )
        self.iTunes.PlayPause()

    def fastForward( self ):
        # play forward fast.
        _log.debug( 'FastForward' )
        self.iTunes.FastForward()

    def fastReverse( self ):
        # play backwards fast.
        _log.debug( 'Rewind' )
        self.iTunes.Rewind()

    def getPlaylists( self ):
        # return list of known playlists.
        # each entry consists of a displayable name and an internal Id that can be passed to selectPlaylist
        result = u'<playlists>'

        _log.debug( 'getPlaylists' )
        sources = self.iTunes.Sources
        for source in sources:
            _log.debug( 'Source %s' % source.Name )
            playlists = source.Playlists
            for playlist in playlists:
                # add to result.
                try:
                    result = result + u'<playlist name ="%s" id="%i.%i.%i.%i" />\n' % ( escape(playlist.Name), playlist.sourceID, playlist.playlistID, playlist.trackID, playlist.TrackDatabaseID )
#                    nm = ""
#                    s = 0
#                    p = 0
#                    t = 0
#                    d = 0
#                    playlist.GetITObjectIDs (s,p,t,d) 
#                    nm = escape(playlist.Name)
#                    result = result + u'<playlist name ="%s" id="%i.%i" />\n' % ( nm, s, p )
                except Exception, e:
                    _log.exception( e )
#                    _log.error( "Details %s %i %i" % ( nm, s, p ) )
        result = result + u'</playlists>'

        _log.debug( 'getPlaylists %s' % result)
        return result

    def getPlaylistContents( self ):
        # return list of current playlist content.
        # each entry consists of a displayable name and an internal Id that can be passed to selectTrack
        _log.debug( 'getPlaylistContents' )
        result = ''

        playlist = self.iTunes.CurrentPlaylist
        if playlist:
            result = u'<playlist>'
            for track in playlist.Tracks:
                # add to result.
                result = result + u'<track name ="%s" id="%i.%i.%i.%i" />\n' % ( escape(track.Name), track.sourceID, track.playlistID, track.trackID, track.TrackDatabaseID )
            result = result + u'</playlist>'
        _log.debug( 'getPlaylistContents %s' % result)
        return result

    def selectPlaylist( self, idStr ):
        # change to playlist identified by id.
        _log.debug( 'selectPlaylist %s ' % idStr)
        id = string.split( idStr, '.' )
        try:
            playlist = self.iTunes.GetITObjectByID( id[0], id[1], 0, 0 )
            if playlist:
                playlist = win32com.client.CastTo(playlist, 'IITPlaylist')
                playlist.PlayFirstTrack()
                _log.debug( 'playList first track %s %s' % (id[0], id[1]) )
                return None
        except Exception, e:
            _log.exception ( e )
        return u"No Such Playlist"

    def selectTrack( self, idStr ):
        # change to track identified by id.
        # This may cause change of playlist
        _log.debug( 'selectTrack %s ' % idStr)
        id = string.split( idStr, '.' )
        id[0] = int(id[0])
        id[1] = int(id[1])
        id[2] = int(id[2])
        id[3] = int(id[3])
        _log.debug( 'id %i, %i, %i, %i' % ( id[0], id[1], id[2], id[3] ) )
        try:
            track = self.iTunes.GetITObjectByID( id[0], id[1], id[2], id[3] )
            if track:
                track = win32com.client.CastTo(track, 'IITTrack')
#                    track = win32com.client.CastTo(track, 'IITFileOrCDTrack')
                _log.debug( 'selectTrack %s %i.%i.%i.%i' % ( track.Name, track.sourceID, track.playlistID, track.trackID, track.TrackDatabaseID ) )
                track.Play()
                return None
        except Exception, e:
            _log.exception ( e )
        return u"No Such Track"

    # End of mediaInterface.

    # SoundInterface:
    def volume( self ):
        # return the current volume as a number between 0 and 100
        return u'<vol>%i</vol>' % self.iTunes.SoundVolume

    def toggleMute( self ):
        # pause media.
        _log.debug( 'toggleMute' )
        self.iTunes.Mute = not self.iTunes.Mute;

    def volUp( self, step = None ):
        # step volume up by an amount based on step
        # step may be 1,2,3 where 1 is small step, 2 is medium step and 3 is large step.    def up()
        cur = self.iTunes.SoundVolume
        self.iTunes.SoundVolume = cur + self.volStep(step)
        _log.debug( 'volUp %i:%i' % (cur, self.iTunes.SoundVolume) )

    def volDown( self, step = None ):
        # step volume down by an amount based on step
        # step may be 1,2,3 where 1 is small step, 2 is medium step and 3 is large step.
        cur = self.iTunes.SoundVolume
        self.iTunes.SoundVolume = cur - self.volStep(step)
        _log.debug( 'volDown %i:%i' % (cur, self.iTunes.SoundVolume) )

    def setVolume( self, newVolume ):
        """
        change the current volume.
        In range 0 to 100%
        Format is variable, but absolute is only used for now
        For now support 
          <nn> absolute in percent.
          +-<nn> relative in percent
        """
        newVolume = int(newVolume)
        if newVolume < 0:
            newVolume = 0
        elif newVolume > 100:
            newVolume = 100
        self.iTunes.SoundVolume = newVolume
        return

    # End of SoundInterface.

# End of ITunesInterface.
