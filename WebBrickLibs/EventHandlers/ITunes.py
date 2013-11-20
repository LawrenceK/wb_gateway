#
#
import logging, threading, time, sys
from Queue import Queue, Empty

import pythoncom
initFlags = pythoncom.COINIT_MULTITHREADED
sys.coinit_flags = initFlags

import win32com.client

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from EventHandlers.BaseHandler import BaseHandler

from mediaserver.ITunesAccess import ITunesAccess

_log = logging.getLogger( "EventHandlers.ITunes" )

# TODO make sure we get the latest type library instead
#iTunes 1.8 Type Library
# {9E93C96F-CF0D-43F6-8BA8-B807A3370712}, lcid=0, major=1, minor=8
from win32com.client import gencache
gencache.EnsureModule('{9E93C96F-CF0D-43F6-8BA8-B807A3370712}', 0, 1, 8)

#
# WebBrick ITunes event interface
#
#
# this will replace the coherence base class.
class ITunes( BaseHandler ):
    """
    """
    def __init__ (self, localRouter):
        self._log = _log
        super(ITunes,self).__init__(localRouter)
        self._thread = None
        self.iTunes = None
        pythoncom.CoInitializeEx(initFlags)    # need to initialize for all processing threads?
        # may need to be able to redo this.
        self.udn = "ITunes:127.0.0.1"
        self.name = "ITunes"
        # events are sent to worker thread as itunes interface needs to be used
        # on the thread the interface is created.
        self._taskList = Queue()

    def configure( self, cfgDict ):
        self.udn = "ITunes:127.0.0.1"
        if cfgDict.has_key("friendlyName"):
            self.name = cfgDict["friendlyName"]

    def start(self):
        _log.debug( 'start' )
        BaseHandler.start(self)
        # subscribe to media control events
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/render/control' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/transport/control' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/connection/control' )

        self.running = True
        self._thread = threading.Thread( target=self.run )
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        _log.debug( 'stop' )
        self.running = False

        self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/client", 
                "upnp/%s"%(self.name), { 'udn':self.udn, 'name': self.name, 'active': 'False' } ) )

        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/render/control' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/transport/control' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/connection/control' )

        BaseHandler.stop(self)

    def alive(self):
        return self._thread and self._thread.isAlive()

    def handleTransportControl( self, inEvent ):
        od = inEvent.getPayload()
        if od.has_key("udn") and self.udn == od["udn"]:
            if od.has_key("action"):
                action = od["action"]
                if action == "play":
                    self.doPlay()
                elif action == "pause":
                    self.doPause()
                elif action == "stop":
                    self.doStop()
                elif action == "next":
                    self.nextTrack()
                elif action == "prev":
                    self.prevTrack()

    def handleRenderControl( self, inEvent ):
#        if inEvent.getSource() == "http://id.webbrick.co.uk/events/av/control" :
        od = inEvent.getPayload()
        if od.has_key("udn") and self.udn == od["udn"]:
            if od.has_key("volume"):
                volume = od["volume"]
                self.setVolume(int(volume))

    def handleConnectionControl( self, inEvent ):
#        if inEvent.getSource() == "http://id.webbrick.co.uk/events/av/control" :
        od = inEvent.getPayload()
        if od.has_key("udn") and self.udn == od["udn"]:
            if od.has_key("action"):
                action = od["action"]
                if action == "play":
                    self.doPlay()
                elif action == "pause":
                    self.doPause()
                elif action == "stop":
                    self.doStop()
                elif action == "next":
                    self.nextTrack()
                elif action == "prev":
                    self.prevTrack()

    def doHandleEvent( self, handler, inEvent ):
        _log.debug( 'doHandleEvent %s', inEvent )
        self._taskList.put( inEvent )

        return makeDeferred(StatusVal.OK)

    def doDecodeEvent( self, inEvent ):
        _log.debug( 'doHandleEvent %s', inEvent )
        try:
            if inEvent.getType() == "http://id.webbrick.co.uk/events/av/render/control" :
                self.handleRenderControl( inEvent )
            if inEvent.getType() == "http://id.webbrick.co.uk/events/av/transport/control" :
                self.handleTransportControl( inEvent )
            if inEvent.getType() == "http://id.webbrick.co.uk/events/av/connection/control" :
                self.handleConnectionControl( inEvent )
        except Exception, ex:
            _log.exception(ex)

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

    def doStop( self ):
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

    def doPlay( self ):
        # start the media playing at the current point, if state = paused does resume.
        # if already playing does nothing.
        _log.debug( 'play' )
        self.iTunes.Play()

    def doPause( self ):
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
        return self.iTunes.SoundVolume

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

    def run(self):
        pythoncom.CoInitializeEx(initFlags)    # need to initialize for all processing threads?
        time.sleep(5)
        self.iTunes = win32com.client.Dispatch("iTunes.Application")
        oldvol = -1
        oldpos = -1
        oldname = ""
        oldalbum = ""
        oldartist = ""

        self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/client", 
                "upnp/%s"%(self.name), { 'udn':self.udn, 'name': self.name, 'active': 'True' } ) )

        while self.alive():
            try:
                inEvent = self._taskList.get( True, 1.0 )
                self.doDecodeEvent( inEvent )

            except Empty, ex:
                # look for state chnage in ITunes
                # get current volume
                newvol = self.iTunes.SoundVolume
                if newvol != oldvol:
                    # generate event
                    oldvol = newvol
                    self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/render/state", 
                            "av/render/state/%s"%(self.udn), { 'udn':self.udn, 'volume':newvol } ) )

                # get current position
                newpos = self.iTunes.PlayerPosition
                if newpos != oldpos:
                    # generate event
                    oldpos = newpos
                    self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/render/state", 
                            "av/render/state/%s"%(self.udn), { 'udn':self.udn, 'position':newpos } ) )

                # get current track
                ct = self.iTunes.CurrentTrack
                if ct != None:
                    if oldname != ct.Name or oldalbum != ct.Album or oldartist != ct.Artist:
                        oldartist = ct.Artist
                        oldname = ct.Name
                        oldalbum = ct.Album
                        self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/render/state", 
                                "av/render/state/%s"%(self.udn), { 'udn':self.udn, 'artist':oldartist, 'album':oldalbum, 'track':oldname  } ) )

            except Exception, ex:
                _log.exception( ex )

        # release ITunes interface
        self.iTunes = None
