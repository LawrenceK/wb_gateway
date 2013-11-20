# $Id: MediaInterface.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# MediaInterface
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
from MiscLib.Enumeration import Enumeration
 
 
MediaState = Enumeration("MediaState",
    ["STOP",
     "PLAY",
     "PAUSED",
     "FASTFORWARD",
     "REVERSE",
     "ERROR",
     "UNKNOWN"
     ])
 
MediaErrors = Enumeration("MediaErrors",
    ["OK",
     "ERROR",
     "NOT_IMPLEMENTED"
     ])
 
class MediaInterface:
    """
    A generic interface to a media server. The aim is to abstract the basic operations we wish to perform
    through the home gateway.

    All strings returned will be in Unicode.

    """

    def configure( self, xml ):
        """
        configure this media access interface
        xml is part of an xml dom relevant to this media interface.
        the 'root' element will be what caused the module to be loaded.
        any other elements  and attributes are implementation dependant.
        any result other than None is an error condition.
        """
        # default implementation, transfer all attributes to locals?
        return None

    def getStatus( self ):
        """
        return an Xml blob with the current state if a media server
        <mediastatus name="name"><state></state><track></track><position>nn</position><duration>nn</duration></mediastatus>
        """
        return

    def setPosition( self, newPosition ):
        """
        change the current location in the current track.
        Format is variable, but should allow relative and absolute positioning.
        For now support 
          <nn> absolute in seconds.
          +-<nn> relative in seconds
          <nn>% absolute in percent
          +-<nn>% relative in percent
        """
        return

    def setVolume( self, newVolume ):
        """
        change the current volume.
        In range 0 to 100%
        Format is variable, but absolute is only used for now
        For now support 
          <nn> absolute in percent.
          +-<nn> relative in percent
        """
        return

    def stop( self ):
        """ 
        stop the media playing.
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def play( self ):
        """ 
        start the media playing at the current point, if state = paused does resume.
        if already playing does nothing.
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def togglePause( self ):
        """ 
        pause/unpause the sound
        """
        return

    def pause( self ):
        """ 
        pause media.
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def nextTrack( self ):
        """ 
        move to next track
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def prevTrack( self ):
        """ 
        move to previous track
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def fastForward( self ):
        """ 
        play forward fast.
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def fastReverse( self ):
        """ 
        play backwards fast.
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def getPlaylists( self ):
        """ 
        return list of known playlists.
        each entry consists of a displayable name and an internal Id that can be passed to selectPlaylist
        id should be treated as opaque, current exists only on the playlist that is current.
        result is an XmlBlob
        <playlists><playlist id="string" [current="yes"]>display text</playlist>....</playlists>
        """
        return

    def getPlaylistContents( self ):
        """ 
        return list of current playlist content.
        each entry consists of a displayable name and an internal Id that can be passed to selectTrack
        id should be treated as opaque, current exists only on the track that is current.
        result is an XmlBlob
        <playlist><track id="string" [current="yes"]>display text</track>....</playlist>
        """
        return

    def selectPlaylist( self, id ):
        """ 
        change to playlist identified by id.
        This id should be the id string from a getPlaylists
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def selectTrack( self, id ):
        """ 
        change to track in current playlist identified by id.
        The id should be the id string from getPlaylist
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

# End of mediaInterface.

class SoundInterface:
    """ 
    This class is an interface to a sound controller normally part of a media interface
    At present only volume is defined.
    """
    def volume( self ):
        """ 
        return the current volume as an xmlBlob between 0 and 100
        <vol>nnn</vol>
        """
        return

    def toggleMute( self ):
        """ 
        mute/umnute the sound
        """
        return

    def volUp( self, step = None ):
        """ 
        step volume up by an amount based on step
        step may be 1,2,3 where 1 is small step 1%, 2 is medium step 5% and 3 is large step 10%
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    def volDown( self, step = None ):
        """ 
        step volume down by an amount based on step
        step may be 1,2,3 where 1 is small step 1%, 2 is medium step 5% and 3 is large step 10%
        On failure returns a text string identifying error, otherwise None or no return value.
        """
        return

    # private helper to convert a step number to a % value
    def volStep( self, step ):
        if ( step == 1 ):
            return 1
        elif ( step == None ) or ( step == 2 ):
            return 5
        else:
            return 10

# End of SoundInterface.
