// $Id: WbEnableEntry.js 2267 2008-05-26 12:02:35Z lawrence $
//
// Javascript for enable entry wdiget

// ----------------------------------------------------------------
// Enable entry functions
// ----------------------------------------------------------------
//
function loadWbEnableEntry(pref, post)
    {
    logDebug("loadWbEnableEntry") ;
    if (!pref) pref = "" ;
    if (!post) post = "" ;
    return partial(WbEnableEntry_init, pref, post) ;
    }

function WbEnableEntry_send(elm, val)
    {
    logDebug("WbEnableEntry_send: val; ", val, "source: ", elm.source, "target: ", elm.target );
    try {
        if ( val || ( val == 0 ) )
            {
            if ( elm.target != null )
                {
                // Send update command, refresh selector state when done
                WbEnableEntry_update(elm, val );
                if ( elm.target.indexOf("?") < 0 )
                {
                    url = elm.target+"?val="+val;
                }
                else
                {
                    url = elm.target+"&val="+val;
                }
                logDebug("WbEnableEntry_send: url ", url );
                var def = doTimedXMLHttpRequest(url, pollerTimeout);
                def.addBoth(pollSoon);
                }
            else
                {
                logError("WbEnableEntry_send (no target)") ;
                }
            }
        }
    catch( e )
        {
        logError("WbEnableEntry_send: ", e) ;
        }
}

function WbEnableEntry_init(pref, post, elm)
    {
    logDebug("WbEnableEntry_init: ", pref, ", ", post, ", ",elm) ;
    elm.mapval  = ["Off", "On"] ;
    // pick up mapval labels from the HTML file
    // (cf. push button selector object)        
    var attr = elm.getAttribute("stateVals") ;
    if (attr)
    {
        // comma separated list of values.
        var v = attr.split(",");
        if  (v.length >= 2)
        {
            elm.mapval  = v;
        }
    }
    elm.pref      = pref ;
    elm.post      = post ;
    elm.title     = elm.getAttribute("wbTitle") ;
    elm.source    = getEndPointSource(elm) ;
    elm.target    = getEndPointTarget(elm) ;
   
    getWidgetBaseClass(elm,"WbEnableEntry");
    var txt = strip(getElementText(elm))
    if ( txt.length > 0 )
        {
            setWidgetState(elm,txt);
        }
        else
        {
            setWidgetState(elm,"Pending");
            WbEnableEntry_update(elm," ")
        }

    
    
    connect( elm, "onclick", function() { WbEnableEntry_popup( elm, partial( WbEnableEntry_send, elm ) ); } );

    elm.handle = setPoller(WbEnableEntry_request, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function WbEnableEntry_request(elm)
    {
    logDebug("WbEnableEntry_request: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(WbEnableEntry_receive, elm) ;
        }
    else
        {
        logError("WbEnableEntry_request (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function WbEnableEntry_receive(elm, req)
    {
    try
        {
        logDebug("WbEnableEntry_receive (callback): elm: ", elm, ", req: ", req, ", pref: ", elm.pref ) ;
        sts = getWbStatus(req) ;
        if ( sts )
            {
            state = sts[2];
            logDebug("WbEnableEntry_receive : elm.mapval: ", elm.mapval, ", state: ", state ) ;
            WbEnableEntry_update(elm, elm.pref+elm.post );
            if ( (sts[2] < 0 ) || (sts[2] >= elm.mapval.length) )
                {
                // if index greater than length of state names then use last.
                state = elm.getAttribute("overValueState");
                if (!state)
                    {
                        state = elm.mapval[elm.mapval.length-1];
                    }
                }
            else
                {
                state = elm.mapval[sts[2]];
                }
            }
        else
            {
            state = "Absent";
            WbEnableEntry_update(elm, " " );
            }
        setWidgetState(elm,state);
        }
    catch( e )
        {
        sts = null ;
        logError("WbEnableEntry_receive: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

function WbEnableEntry_update(elm, val)
{
    valElm = getElementsByTagAndClassName("div", "buttonbodycontent", elm)[0];
    if (valElm)
    {
        valElm.innerHTML = val;
    }
    else
    {
        elm.innerHTML = val;
    }
}

function WbEnableEntry_CB( val ) 
{
    np = $("WbEnableEntry")
    np.callBack( val );
    np.style.visibility ='hidden';
}

function WbEnableEntry_popup( elm, callBack ) 
{
    logDebug("WbEnableEntry_popup: ", elm );
    if (!$("WbEnableEntry"))
    {
        logDebug("WbEnableEntry_popup: Create " );
        // Beware Internet Explorer generates objects for trailing comma
        var rows = [
            [   
                [ {'colSpan':'3'}, SPAN( {'id': 'enablepadtitle'},"") ]
            ],
            [   
                [ {},IMG({ "src" : "/static/images/numerals/makeOn.png", "onclick":"WbEnableEntry_CB( 1 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/makeOff.png", "onclick":"WbEnableEntry_CB( 0 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/cancel.png", "onclick":"WbEnableEntry_CB()" } )]
            ],
        ];
        cell_display = function (cell) 
            {
	    if (cell)
	        {
		return TD(cell[0], cell[1]);
	        }
            }
        row_display = function (row) 
            {
            if (row)
                {
                return TR(null, map(cell_display, row) );
                }
            }

        var newTable = TABLE(null,
            TBODY(null,
                createDOM('colgroup', {'span':'3', 'width':'30%'} ),
                map(row_display, rows)));

        var newDiv = DIV({'id': 'WbEnableEntry', 'class': 'dataEntry', 'opacity':'0.95'}, newTable );
        appendChildNodes( currentDocument().body, newDiv );
        newDiv.style.position ='absolute';
        newDiv.style.width ='50px';
        newDiv.style.height ='150px';
        newDiv.style.zIndex ='1010';
    }
    $("WbEnableEntry").style.top = '70px';
    $("WbEnableEntry").style.left = '15%';
    $("WbEnableEntry").callBack = callBack;
    $("WbEnableEntry").style.visibility ='visible';
    setElementText($("enablepadtitle"), elm.title );
};
