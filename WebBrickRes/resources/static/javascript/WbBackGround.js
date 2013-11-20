// $Id: WbBackGround.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript library panel background

// ----------------------------------------------------------------
// Panel functions
// ----------------------------------------------------------------

function changeBackground(theme)
{
    logDebug("changeBackground: theme " );
    document.body.className = theme ;
}

function changeBG()
{
    document.body.className = bimages[bindex] ;
    bindex++ ;
    if (bindex >= bimages.length)
    {
        bindex = 0 ;
    }
    setTimeout("changeBG()", 5000);
}


// Initial load of a caption object
function loadWbBackGround()
    {
    logDebug("loadWbBackGround") ;
    return partial(WbBackGround_init) ;
    }

function WbBackGround_init(elm)
    {
    logDebug("initTextDisplay: ", elm) ;
    elm.source    = getEndPointSource(elm) ;
    setPoller(WbBackGround_request, elm) ;
    }

// Polling callback function, 
// Request and eventually update background image
function WbBackGround_request(elm)
    {
    logDebug("WbBackGround_request: ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout);
        def.addBoth(WbBackGround_receive, elm) ;
        }
    else
        {
        logError("WbBackGround_request (no source)") ;
        }
    return;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function WbBackGround_receive(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req);
        logDebug("WbBackGround_receive (callback): elm: ", elm, ", req: ", req, ", sts: ", sts);
        if ( sts != null )
            {
            // verify contents
            logDebug("WbBackGround_receive sts[2]: ", sts[2]);
            elm.style.backgroundImage = "url("+sts[2]+")";
            elm.style.backgroundRepeat = "no-repeat";
            elm.style.backgroundPosition = "center";
            }
        }
    catch( e )
        {
        logError("WbBackGround_receive: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

