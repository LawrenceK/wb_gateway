// $Id: WbTextDisplay.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript library for WebBrick control panel interaction widgets

// ----------------------------------------------------------------
// Text value display functions
// ----------------------------------------------------------------
//
// sample use
//
// wbSource is the URL for the text content and will replace the &nbsp;
//
//    <td wbType="Text" wbLoad='loadTextDisplay("","")'
//            wbSource="/local/messages">
//        &nbsp;
//    </td>

// Initial load of a caption object
function loadTextDisplay(pref, post)
    {
    logDebug("loadTextDisplay") ;
    if (!pref) pref = "" ;
    if (!post) post = "" ;
    return partial(initTextDisplay, pref, post) ;
    }

function loadText()
    {
    logDebug("loadText") ;
    return loadTextDisplay("", "");
    }

function initTextDisplay(pref, post, elm)
    {
    logDebug("initTextDisplay: ", pref, ", ", post, ", ", elm) ;
    elm.pref      = pref ;
    elm.post      = post ;
    elm.source    = getEndPointSource(elm) ;
    getWidgetBaseClass(elm,"text");
    setWidgetState( elm, "Pending" );
    setPoller(requestTextState, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestTextState(elm)
    {
    logDebug("requestTextState: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(updateTextStatus, elm) ;
        }
    else
        {
        logError("requestTextState (nop source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function updateTextStatus(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatus: ", e) ;
        }
    logDebug("updateTextStatus (callback): elm: ", elm, 
             ", req: ", req, ", pref: ", elm.pref, ", sts: ", sts) ;
    if ( sts != null )
        {
        setWidgetState( elm, "Present" );
        setElementText(elm, elm.pref+sts[2]+elm.post) ;
        }
    else
        {
        setWidgetState( elm, "Absent" );
        setElementText(elm, elm.pref+"???"+elm.post) ;
        }
    return req ;    // Return request to next in callback chain
    }
