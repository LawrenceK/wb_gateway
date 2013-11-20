// $Id: WbNumericEntry.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for numeric entry wdiget

// ----------------------------------------------------------------
// Numeric value entry functions
// ----------------------------------------------------------------
//
// Sample usage
// wbSource will return the numeric to be inserted into the element.
// wbTarget is where a new value entered will be sent.
//
//    <td width="20%" wbType="Numeric" wbLoad='WbNumericEntry("House: ","##.#","&ordm;C")'
//        wbSource='/wbsts/lighting.webbrick/Tmp/0'
//        wbTarget='/heating/schedule/id/val'
//          >&nbsp;</td>
//  </tr>

// Initial load of a caption object
function loadWbNumericEntry(pref, patt, post)
    {
    return partial(WbNumericEntry_init, pref, patt, post) ;
    }

function loadWbNudgeNumericEntry(pref, patt, post)
{
    return partial(WbNudgeNumericEntry_init, pref, patt, post) ;
}

function WbNudgeNumericEntry_up(elm)
{
    var val = WbNumericEntry_getValue(elm);
    if ( val < 100)
    {
        val = val + 1;
        WbNumericEntry_send(elm, val);
    }
}

function WbNudgeNumericEntry_down(elm)
{
    var val = WbNumericEntry_getValue(elm);
    if ( val > 0 )
    {
        val = val - 1;
        WbNumericEntry_send(elm, val);
    }
}

function WbNudgeNumericEntry_init(pref, patt, post, elm)
{
    // Create up and down buttons and a span for the text value
    var h = elm.getAttribute("height");
    if (h == 0)
        {
        h = 10;
        }
    var up = IMG( {'src':'/static/images/numerals/up.png', 'hspace':'0', 'height': h } );
    var down = IMG( {'src':'/static/images/numerals/down.png', 'hspace':'0', 'height': h } );
    var value = SPAN( {'class':'buttonbodycontent'} );
    value.innerHTML = elm.innerHTML;
    elm.innerHTML = "";
    elm.appendChild( down );
    elm.appendChild( value );
    elm.appendChild( up );
    connect( down, "onclick", partial(WbNudgeNumericEntry_down, elm) );
    connect( up, "onclick", partial(WbNudgeNumericEntry_up, elm) );

    WbNumericEntry_init(pref, patt, post, elm);
}

function WbNumericEntry_getContentField(elm)
{
    valElm = getElementsByTagAndClassName("div", "buttonbodycontent", elm)[0];
    if (valElm)
    {
        return valElm;
    }
    valElm = getElementsByTagAndClassName("span", "buttonbodycontent", elm)[0];
    if (valElm)
    {
        return valElm;
    }
    return elm;
}

function WbNumericEntry_update(elm, val)
{
    valElm = WbNumericEntry_getContentField(elm).innerHTML = val;
}

function WbNumericEntry_getValue(elm)
{
    return parseFloat(WbNumericEntry_getContentField(elm).innerHTML);
}

function WbNumericEntry_send(elm, val)
{
    logDebug("WbNumericEntry_send: txt ", val );
    
    WbNumericEntry_update(elm, val);
    
    try
        {
        if ( elm.target != null )
            {
            // Send update command, refresh selector state when done
            elm.className = "numericPending" ;
            if ( elm.target.endsWith('=') )
            {
                url = elm.target+val;
            }
            else
            if ( elm.target.indexOf("?") < 0 )
            {
                url = elm.target+"?val="+val;
            }
            else
            {
                url = elm.target+"&val="+val;
            }
            logDebug("WbNumericEntry_send: url ", url );
            var def = doTimedXMLHttpRequest(url, pollerTimeout);
            def.addBoth(pollSoon);
            }
        else
            {
            logError("WbNumericEntry_send (no target)") ;
            }
        }
    catch( e )
        {
        logError("WbNumericEntry_send: ", e) ;
        }
}

function WbNumericEntry_init(pref, patt, post, elm)
    {
    logDebug("WbNumericEntry_init: ", pref, ", ", patt, ", ", post, ", ", elm) ;
    elm.pref      = pref ;
    elm.post      = post ;
    var attr = elm.getAttribute("wbPrefix") ;
    if (attr)
    {
        elm.pref = attr;
    }
    else
    if ( pref )
    {
        elm.pref = pref;
    }
    else
    {
        elm.pref = "";
    }

    attr = elm.getAttribute("wbPostfix") ;
    if (attr)
    {
        elm.post = attr;
    }
    else
    if ( post )
    {
        elm.post = post;
    }
    else
    {
        elm.post = "";
    }

    attr = elm.getAttribute("wbFormat") ;
    if (attr)
    {
        elm.format    = numberFormatter(attr);
    }
    else
    if ( patt )
    {
        elm.format    = numberFormatter(patt);
    }
    else
    {
        elm.format    = numberFormatter("##");
    }

    elm.source    = getEndPointSource(elm) ;
    elm.target    = getEndPointTarget(elm) ;
    getWidgetBaseClass(elm,"numeric");
    setWidgetState( elm, "Pending" );
    elm.title     = elm.getAttribute("wbTitle") ;
    logDebug("WbNumericEntry_init: ", elm.source, ", ", elm.target, ", ", elm.title);
//    var attr = elm.getAttribute("noPolling") ;
//    elm.noPolling = attr && (attr == "yes" )

    connect( WbNumericEntry_getContentField(elm), "onclick", function() { PopUpNumericEntry( elm, partial( WbNumericEntry_send, elm ) ); } );

    elm.handle = setPoller(WbNumericEntry_request, elm) ;
    }


// Polling callback function, 
// Request and eventually display the status of a button,
function WbNumericEntry_request(elm)
    {
    logDebug("WbNumericEntry_request: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(WbNumericEntry_received, elm) ;
        }
    else
        {
        logError("WbNumericEntry_request (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function WbNumericEntry_received(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatusReal(req) ;
        logDebug("WbNumericEntry_received (callback): elm: ", elm, 
                 ", req: ", req, ", pref: ", elm.pref, ", sts: ", sts) ;
        if ( sts != null )
            {
            setWidgetState( elm, "Info" );
            WbNumericEntry_update(elm, elm.pref+elm.format(sts[2])+elm.post) ;
//            if (elm.noPolling)
//                {
//                h = elm.handle;
//                elm.handle = null;
//                cancelPoller(h);
//                }
            }
        else
            {
            setWidgetState( elm, "Absent" );
            WbNumericEntry_update(elm, "0");   // need something to click on
            }
        }
    catch( e )
        {
        sts = null ;
        logError("WbNumericEntry_received: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }
