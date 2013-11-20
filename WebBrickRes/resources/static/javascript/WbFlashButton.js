// $Id: WbFlashButton.js 1522 2007-03-15 22:45:34Z lawrence $
//
// Javascript for flash based button

function loadFlashButton()
    {
    logDebug("loadFlashButton") ;
    return partial(initFlashButton) ;
    }

function loadFlashLink()
    {
    logDebug("loadFlashButton") ;
    return partial(initFlashButton) ;
    }

function initFlashButton(btn)
    {
    logDebug("initFlashButton: ", btn);

    btn.source  = getEndPointSource(btn) ;
    btn.target  = getEndPointTarget(btn) ;

    getWidgetBaseClass(btn,"FlashButton");
    setWidgetState( btn, "" );

    // read these first.
    v = btn.getAttribute("labels");
    if ( v )
        {
        btn.labels = v;
        }
    
    // Create sub elements.
    movie = btn.getAttribute("flashMovie");
    if ( movie )
        {
        // create OBJECT and EMBED
        // TODO calculate containing element size to set flash size.
        var h = btn.getAttribute("height");
        var w = btn.getAttribute("width");
        var moviePar = '&ptitle=' + escape(btn.title) 
                +'&callBack=' + escape(btn.target) 
                +'&state=3';
        logDebug("flashVars: ", moviePar);
        // NOTE IE uses object values, firefox uses embed tag.
        var o = '<object'
                    +' classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"'
                    +' codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,65,0"'
                    +' width="'+w+'px"'
                    +' height="'+h+'px">' 
                    + '<param name="movie" value="'+ movie +'" />' 
                    + '<param name="FlashVars" value="'+ moviePar +'"/>' 
                    + '<param name="quality" value="high" />' 
                    + '<param name="wmode" value="transparent">'
                    + '<embed src="'+ movie +'"'
                        +' type="application/x-shockwave-flash"'
                        +' flashvars="' + moviePar +'"'
                        +' quality="high"'
                        +' width="'+w+'px"'
                        +' height="'+h+'px"'
                        +' swLiveConnect ="true"'
                        +' wmode="transparent"'
                        +' pluginspage="http://www.macromedia.com/go/getflashplayer">'
                    +'</embed>' 
                + '</object>';
        logDebug("object: ", o) ;
        btn.innerHTML = ''; // avoid known memory leak ? MSXML?
        btn.innerHTML = o;
        }
    setPoller(requestFlashButton, btn);
    }

function flashButton_doWbTarget( tgt )
    {
    logDebug("flashButton_doWbTarget: ", tgt );
    try
        {
        if ( (tgt.indexOf( '/template' ) >= 0) || (tgt == '/' ) )
        {
            window.location = tgt;
        }
        else
        {
            var def = doTimedXMLHttpRequest( tgt, pollerTimeout );
            def.addBoth(pollSoon);
        }
        }
    catch( e )
        {
        logError("flashButton_doWbTarget: ", e) ;
        }
    }
    
function flashButtonGetFlashObject( btn )
    {
    var nodes = btn.getElementsByTagName( "embed" );
    if ( nodes.length == 0 )
        {
        nodes = btn.getElementsByTagName( "object" );
        }
    var fl = nodes[0];
    return fl;
    }

function flashButtonSetState( btn, st )
    {
    var fl = flashButtonGetFlashObject( btn );
    if (fl)
        {
        logDebug("flashButtonSetState: ", fl, " ", st );
        fl.SetVariable('state', st );
        fl.TCallFrame('/', 0);  // trigger flash to update graphics
        }
    }

function flashButtonSetTitle( btn, st )
    {
    var fl = flashButtonGetFlashObject( btn );
    if (fl)
        {
        logDebug("flashButtonSetTitle: ", fl, " ", st );
        fl.SetVariable('ptitle', st);
//    fl.TCallFrame('/', 0);
        }
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestFlashButton(btn)
    {
    logDebug("requestFlashButton: ", btn.request, ", ", btn.source) ;
    if ( btn.source )
        {
        var def = doTimedXMLHttpRequest(btn.source, pollerTimeout) ;
        def.addBoth(updateFlashButton, btn) ;
        }
    else
        {
        flashButtonSetState(btn, 1);
        logError("requestFlashButton (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function updateFlashButton(btn, req)
    {
    try
        {
        sts = getWbStatusBoolInteger(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatusBoolInteger: ", e) ;
        }
    logDebug("updateFlashButton(callback): btn: ", btn, 
             ", req: ", req, ", sts: ", sts) ;
    if ( sts == null )
    {
        state = -1; // absent or unknown
    }
    else
    {
        state = sts[2];
    }
    flashButtonSetState(btn, state);

    setButtonState(btn, state);
    return req ;    // Return request to next in callback chain
    }


