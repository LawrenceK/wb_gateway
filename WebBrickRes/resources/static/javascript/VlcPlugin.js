// $Id: VlcPlugin.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript library to support VLC plugin

function getVlc()
    {
    result = null;
    logDebug( "getVlc" );
    try
        {
        result = document.getElementById('video1');
        logDebug( "found Vlc" );
//        document.embeds['video1'];
        }
    catch( e )
        {
        logError("getVlc: ", e) ;
        }
    return result;
    }

function fixupVlcTarget()
    {
    logDebug( "fixupVlcTarget" );
    try
        {
        vlc = getVlc();
        tgt = vlc.target;
        logDebug( "vlc.tgt ", tgt );
        svr = location.protocol+'//'+location.host;
        newtgt = svr+tgt;
        logDebug( "fixupVlcTarget ", newtgt );
        vlc.setAttribute("target", newtgt );
        }
    catch( e )
        {
        logError("fixupVlcTarget: ", e) ;
        }
    logDebug( "fixupVlcTarget exit" );
    }

function VLCplay()
    {
    // play() : Start playing media in the plugin.
    logDebug( "VLC play" );
    try
        {
        getVlc().play();
        }
    catch( e )
        {
        logError("VLC play: ", e) ;
        }
    }

function VLCcheckForPlay()
    {
    logDebug( "VLC play" );
//      isplaying() : return true if the plugin is playing something.
    try
        {
        if ( !getVlc().isplaying() )
            {
            getVlc().play();
            }
        }
    catch( e )
        {
        logError("VLC play: ", e) ;
        }
    }

function VLCpause()
    {
//      pause() : Pause playback.
    logDebug( "VLC pause" );
    try
        {
        getVlc().pause();
        }
    catch( e )
        {
        logError("VLC pause: ", e) ;
        }
    }

function VLCskipForward()
    {
    logDebug( "VLC skip forward" );
    try
        {
        getVlc().seek( 5, true );
//      seek(seconds,is_relative) : If is_relative is true, seek relatively to current time, else seek from beginning of the stream. Seek time is specified in seconds.
        }
    catch( e )
        {
        logError("VLC skip forward: ", e) ;
        }
    }

function VLCskipBackwards()
    {
    logDebug( "VLC skip backwards" );
    try
        {
        getVlc().seek( -5, true );
//      seek(seconds,is_relative) : If is_relative is true, seek relatively to current time, else seek from beginning of the stream. Seek time is specified in seconds.
        }
    catch( e )
        {
        logError("VLC skip backwards: ", e) ;
        }
    }

function VLCvolumeUp()
    {
    logDebug( "VLC volume Up" );
    try
        {
//      set_volume(vol) : Set the volume. vol has to be an int in the 0-200 range.
//      get_volume() : Get the current volume setting.
        var c = getVlc().get_volume();
        c += 5;
        if (c > 100)
            {
            c = 100;
            }
        getVlc().set_volume( c );
        }
    catch( e )
        {
        logError("VLC volume Up: ", e) ;
        }
    }

function VLCvolumeDown()
    {
    logDebug( "VLC volume Down" );
    try
        {
//      set_volume(vol) : Set the volume. vol has to be an int in the 0-200 range.
//      get_volume() : Get the current volume setting.
        var c = getVlc().get_volume();
        c -= 5;
        if (c < 0)
            {
            c = 0;
            }
        getVlc().set_volume( c );
        }
    catch( e )
        {
        logError("VLC volume Down: ", e) ;
        }
    }

function VLCmute()
    {
    logDebug( "VLC volume Mute" );
//      mute() : Toggle volume muting.
    try
        {
        getVlc().mute();
        }
    catch( e )
        {
        logError("VLC volume Mute: ", e) ;
        }
    }

function VLCstop()
    {
//      stop() : Stop media playback.
    logDebug( "VLC stop" );
    try
        {
        getVlc().stop();
        }
    catch( e )
        {
        logError("VLC stop: ", e) ;
        }
    }
/*
+++++++++++++++ This is only valid up to 0.8.5 for 0.8.5.1 and later
see http://www.videolan.org/doc/play-howto/en/ch04.html#id294365

//      fullscreen() : Switch the video to full screen.
//      set_int_variable(var_name, value) :
//      set_bool_variable(var_name, value) :
//      set_str_variable(var_name, value) :
//      get_int_variable(var_name) :
//      get_bool_variable(var_name) :
//      get_str_variable(var_name) :
//      clear_playlist() : Clear the playlist.
//      add_item(mrl>) : Append an item whose location is given by the Media Resource Locator to the playlist.
//      next()
//      previous()
//      get_length() : Get the media's length in seconds.
//      get_position() : Get the current position in the media in percent.
//      get_time() : Get the current position in the media in seconds.


*/
//connect(window, "onload", fixupVlcTarget ); 
