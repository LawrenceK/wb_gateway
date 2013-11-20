	<!--
	// ------- Private vars -------
	var jsReady = false;
	var volReady = false;
	var posReady = false;

	// ------- functions called by ActionScript -------
	// called to check if the page has initialized and JavaScript is available
	function isReady() {
		return jsReady;
	}

	// called to notify the page that the SWF has set it's callbacks
	function setSWFIsReady() {
		// record that the SWF has registered it's functions (i.e. that JavaScript
		// can safely call the ActionScript functions)
		volReady = true;
		posReady = true;
		
	//	updateStatus();
	}
	
	// ------- event handling -------
	// called by the onload event of the <body> tag
	function pageInit() {
		// record that JavaScript is ready to go.
		jsReady = true;
	}

	// called when the "Send" button is pressed; the value in the messageText text field
	// is passed in as a parameter.
	function setSongLength(value) {
		if (posReady)
		{
			getSWF("songpositionindicator").setSongLength(value);
		}
	}

	function setSongPosition(value) {
		if (posReady)
		{
			getSWF("songpositionindicator").setSongPosition(value);
		}
	}

	function updateSongPosition(value) {
		if (posReady)
		{
			getSWF("songpositionindicator").updateSongPosition(value);
		}
	}
	
	function setPlaying() {
		if (posReady)
		{
			getSWF("songpositionindicator").setPlaying();
		}
	}

	function setPaused() {
		if (posReady)
		{
			getSWF("songpositionindicator").setPaused();
		}
	}

	function setStopped() {
		if (posReady)
		{
			getSWF("songpositionindicator").setStopped();
		}
	}

	function setVolume(value) {
		if (volReady)
		{
			getSWF("volumecontrol").setVolume(value);
		}
	}

	function newVolume(id, value) {
        logDebug("newVolume ", id, " ", value);
        elm = getElement("volumecontrolcontainer");
        if (elm)
        {
            logDebug("volume control container ", elm);
            FlashVolume_send(elm, value*100);
        }
        else
        {
            logDebug("Cannot find volume control container");
        }
        //.setVolVal.value = value;
	}

	// Gets a reference to the specified SWF file by checking which browser is
	// being used and using the appropriate JavaScript.
	// Unfortunately, newer approaches such as using getElementByID() don't
	// work well with Flash Player/ExternalInterface.
	function getSWF(movieName) {
		if (navigator.appName.indexOf("Microsoft") != -1) {
			return window[movieName];
		} else {
			return document[movieName];
		}
	}
	//-->

function loadFlashVolumeControl()
    {
    logDebug("loadFlashVolumeControl");
    return partial(initFlashVolumeControl);
    }

function initFlashVolumeControl(elm)
    {
    // 
    pageInit();
    elm.source    = getEndPointSource(elm) ;
    elm.target    = getEndPointTarget(elm) ;
/*
        Inline in the widget as Adobe./Macromedia supplied code does things by write to document
    AC_FL_RunContent(
            'codebase', 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0',
            'width', '290',
            'height', '30',
            'src', 'volumecontrol',
            'quality', 'high',
            'pluginspage', 'http://www.macromedia.com/go/getflashplayer',
            'align', 'middle',
            'play', 'true',
            'loop', 'true',
            'scale', 'showall',
            'wmode', 'window',
            'devicefont', 'false',
            'id', 'volumecontrol',
            'bgcolor', '#f2f2f2',
            'name', 'volumecontrol',
            'menu', 'true',
            'allowScriptAccess','sameDomain',
            'movie', '/images/mediaplayer/volumecontrol.swf',
            'salign', ''
            ); //end AC code
*/            
    setPoller(requestFlashVolume, elm) ;
    }
    
function requestFlashVolume(elm)
    {
    logDebug("requestFlashVolume: ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(updateFlashVolume, elm) ;
        }
    else
        {
        logError("requestFlashVolume (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function updateFlashVolume(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatusReal(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatusReal: ", e) ;
        }
    logDebug("updateFlashVolume (callback): elm: ", elm, 
             ", req: ", req, ", sts: ", sts) ;
    if ( sts != null )
        {
        vol = sts[2]/100;
        if (vol > 1)
            vol = 1;
        setVolume(vol);
        }
    else
        {
        setVolume(0);
        }
    return req ;    // Return request to next in callback chain
    }

function FlashVolume_send(elm, val)
{
    logDebug("FlashVolume_send: ", val );
    
    try
        {
        if ( elm.target != null )
            {
            // Send update command, refresh selector state when done
            url = elm.target+val;
            logDebug("FlashVolume_send: url ", url );
            var def = doTimedXMLHttpRequest(url, pollerTimeout);
            def.addBoth(pollSoon);
            }
        else
            {
            logError("FlashVolume_send (no target)") ;
            }
        }
    catch( e )
        {
        logError("FlashVolume_send: ", e) ;
        }
}
function loadFlashPositionIndicator()
    {
    logDebug("loadFlashPositionIndicator");
    return partial(initFlashPositionIndicator);
    }

function initFlashPositionIndicator(elm)
    {
    // 
    pageInit();
    
    elm.wbDuration = elm.getAttribute("wbDuration") ;
    elm.wbTrack = elm.getAttribute("wbTrack") ;
    elm.curTrack = '';
    elm.wbState = elm.getAttribute("wbState") ;
    elm.wbCurPosition = elm.getAttribute("wbCurPosition") ;
    
    setPoller(requestFlashPositionIndicator, elm) ;
    }
    
function requestFlashPositionIndicator(elm)
    {
    logDebug("requestFlashPositionIndicator: ", elm.wbTrack);
    try
        {
        var def = doTimedXMLHttpRequest(elm.wbDuration, pollerTimeout) ;
        def.addBoth(updateFlashDuration, elm) ;
        def = doTimedXMLHttpRequest(elm.wbTrack, pollerTimeout) ;
        def.addBoth(updateFlashTrack, elm) ;
        def = doTimedXMLHttpRequest(elm.wbState, pollerTimeout) ;
        def.addBoth(updateFlashState, elm) ;

        def = doTimedXMLHttpRequest(elm.wbCurPosition, pollerTimeout) ;
        def.addBoth(updateFlashPosition, elm) ;
        }
    catch( e )
        {
        logError("requestPositionIndicator: ", e) ;
        }
    return ;
    }

function updateFlashDuration(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatusInt(req) ;
        if (sts != null )
        {
            setSongLength( sts[2] );
        }
        }
    catch( e )
        {
        sts = null ;
        logError("updateFlashDuration: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

function updateFlashPosition(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatusInt(req) ;
        if (sts != null )
        {
            setSongPosition( sts[2] );
        }
        }
    catch( e )
        {
        sts = null ;
        logError("updateFlashPosition: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

function updateFlashTrack(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req) ;
        if (sts != null )
        {
            //sts[2] is duration as hh:mm:ss
            if (elm.curTrack != sts[2] )
            {
                // reset position to 0.
                setSongPosition(0);
                elm.curTrack = sts[2];
            }
        }
        }
    catch( e )
        {
        sts = null ;
        logError("updateFlashTrack: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }
    
function updateFlashState(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req) ;
        if (sts != null )
            {
            //sts[2] is duration as hh:mm:ss
            // TODO map within gateway to an integer state value and then simpler.
            if (sts[2] == "PLAYING" )
                {
                setPlaying();
                }
            else
            if (sts[2] == "PAUSED_PLAYBACK" )
                {
                setPaused();
                }
            else
            if (sts[2] == "STOPPED" )
                {
                setStopped();
                }
            else
                {
                }
            }
        }
    catch( e )
        {
        sts = null ;
        logError("updateFlashState: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }
