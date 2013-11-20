// $Id: WbTimeDisplay.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for time display wdiget

// Initial load of a time display object
function loadWbTimeDisplay(pref, post)
{
    logDebug("loadWbTimeDisplay") ;
    return partial(WbTimeDisplay_init) ;
}

function WbTimeDisplay_init(elm)
{
    logDebug("initTimeDisplay: ", elm) ;
    elm.source    = getEndPointSource(elm) ;
    getWidgetBaseClass(elm,"numeric");
    setWidgetState( elm, "Pending" );
    setPoller(WbTimeDisplay_request, elm) ;
}

// Polling callback function, 
// Request and eventually display the status of a button,
function WbTimeDisplay_request(elm)
    {
    logDebug("WbTimeDisplay_request: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(WbTimeDisplay_received, elm) ;
        }
    else
        {
        logError("WbTimeDisplay_request (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
// value is returned as formatted string.
function WbTimeDisplay_received(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req) ;
        logDebug("WbTimeDisplay_received(callback): elm: ", elm, " req: ", req, ", sts: ", sts);
        if ( sts != null )
            {
            elm.className = "numericInfo" ;
            setElementText(elm, sts[2]);
            }
        else
            {
            elm.className = "numericAbsent" ;
            setElementText(elm, "???");
            }
        }
    catch( e )
        {
        sts = null ;
        logError("WbTimeDisplay_received: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }
