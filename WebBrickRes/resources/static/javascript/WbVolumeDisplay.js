// $Id: WbNumericDisplay.js 2807 2008-09-26 16:25:53Z lawrence.klyne $
//
// Javascript for Volume Display

// ----------------------------------------------------------------
// Volume value display functions
// ----------------------------------------------------------------
//
// Sample usage
// wbSource will rteunr the numeric to be inserted into the element.
//
//    <td width="20%" wbType="Numeric" wbLoad='loadNumericDisplay("House: ","##.#","&ordm;C")'
//        wbSource='/wbsts/lighting.webbrick/Tmp/0'>&nbsp;</td>
//  </tr>

// Initial load of a caption object
function loadVolumeDisplay(pref, patt, post)
    {
    logDebug("loadVolumeDisplay") ;
    if (!pref) pref = "" ;
    if (!patt) patt = "#.#" ;
    if (!post) post = "" ;
    return partial(initVolumeDisplay, pref, patt, post) ;
    }

function loadVolume()
    {
    logDebug("loadVolume") ;
    return loadVolumeDisplay("", "");
    }

function initVolumeDisplay(pref, patt, post, elm)
    {
    logDebug("initVolumeDisplay: ", pref, ", ", patt, ", ", post, ", ", elm) ;
    elm.pref      = pref ;
    elm.format    = numberFormatter(patt) ;
    elm.post      = post ;
    elm.source    = getEndPointSource(elm) ;
    getWidgetBaseClass(elm,"numeric");
    setWidgetState( elm, "Pending" );
    setPoller(requestVolumeState, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestVolumeState(elm)
    {
    logDebug("requestVolumeState: ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(updateVolumeStatus, elm) ;
        }
    else
        {
        logError("requestVolumeState (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function updateVolumeStatus(elm, req)
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
    logDebug("updateVolumeStatus (callback): elm: ", elm, 
             ", req: ", req, ", pref: ", elm.pref, ", sts: ", sts) ;
    if ( sts != null )
        {
        setWidgetState( elm, "Present" );
        elm.volume = sts[2] ;
        doElmWidth(elm,sts[2]) ;
        }
    else
        {
        setWidgetState( elm, "Absent" );
        setElementText(elm, elm.pref+"???"+elm.post) ;
        }
    return req ;    // Return request to next in callback chain
    }

function doElmWidth (elm, val)
    {
    // do maths on Val
    var iVal = Math.round((val*3.04)+280) ;  // scale numbers
    //alert("Called, for element:"+elm) ;
    elm.setAttribute("width",iVal+"px") ;
    //elm.setAttribute("height","58px") ;
    }


function doVol(devId,dir)
    {
    var ve = document.getElementById("volume") ;
    //alert("doVol Called:"+ve.volume) ;
    if (ve.volume == undefined)
        {
        ve.volume = 10 ;  // a safe initial value, should be set in event despatch at start up 
        }
    if (dir == "down")
        {
        vnew = ve.volume - 10 ;
        if (vnew < 1) vnew = 1 ;
        }
    else
        {
        vnew = ve.volume + 10 ;
        if (vnew > 99) vnew = 99 ;
        }
    var def = doTimedXMLHttpRequest("/sendevent/serial/send/action?type=serial/action&action=setvolume&cmd=send&id=" + devId + "&val="+vnew, pollerTimeout) ;
    def.addBoth(pollSoon) ;
    }
    

