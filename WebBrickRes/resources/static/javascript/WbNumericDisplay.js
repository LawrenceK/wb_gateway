// $Id: WbNumericDisplay.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for numeric display wdiget

// ----------------------------------------------------------------
// Numeric value display functions
// ----------------------------------------------------------------
//
// Sample usage
// wbSource will rteunr the numeric to be inserted into the element.
//
//    <td width="20%" wbType="Numeric" wbLoad='loadNumericDisplay("House: ","##.#","&ordm;C")'
//        wbSource='/wbsts/lighting.webbrick/Tmp/0'>&nbsp;</td>
//  </tr>

// Initial load of a caption object
function loadNumericDisplay(pref, patt, post)
    {
    logDebug("loadNumericDisplay") ;
    if (!pref) pref = "" ;
    if (!patt) patt = "#.#" ;
    if (!post) post = "" ;
    return partial(initNumericDisplay, pref, patt, post) ;
    }

function loadNumeric()
    {
    logDebug("loadNumeric") ;
    return loadNumericDisplay("", "");
    }

function initNumericDisplay(pref, patt, post, elm)
    {
    logDebug("initNumericDisplay: ", pref, ", ", patt, ", ", post, ", ", elm) ;
    elm.pref      = pref ;
    elm.format    = numberFormatter(patt) ;
    elm.post      = post ;
    elm.source    = getEndPointSource(elm) ;
    getWidgetBaseClass(elm,"numeric");
    setWidgetState( elm, "Pending" );
    setPoller(requestNumericState, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestNumericState(elm)
    {
    logDebug("requestNumericState: ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(updateNumericStatus, elm) ;
        }
    else
        {
        logError("requestNumericState (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function updateNumericStatus(elm, req)
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
    logDebug("updateNumericStatus (callback): elm: ", elm, 
             ", req: ", req, ", pref: ", elm.pref, ", sts: ", sts) ;
    if ( sts != null )
        {
        setWidgetState( elm, "Present" );
        setElementText(elm, elm.pref+elm.format(sts[2])+elm.post) ;
        }
    else
        {
        setWidgetState( elm, "Absent" );
        setElementText(elm, elm.pref+"???"+elm.post) ;
        }
    return req ;    // Return request to next in callback chain
    }
