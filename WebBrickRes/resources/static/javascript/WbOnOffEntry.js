// $Id: WbOnOffEntry.js 3749 2010-10-21 13:26:55Z andy.harris $
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
//    <td width="20%" wbType="Numeric" wbLoad='loadOnOffEntry("House: ","##.#","&ordm;C")'
//        wbSource='/wbsts/lighting.webbrick/Tmp/0'
//        wbTarget='/heating/schedule/id/val'
//          >&nbsp;</td>
//  </tr>
// Initial load of a caption object
function loadWbOnOffEntry(pref, patt, post)
    {
    logDebug("loadWbOnOffEntry") ;
    return partial(WbOnOffEntry_init, pref, patt, post) ;
    }

function WbOnOffEntry_send(elm, val)
    {
    logDebug("WbOnOffEntry_send: val; ", val, "source: ", elm.source, "target: ", elm.target );
    try {
        if ( val || ( val == 0 ) )
            {
            if ( elm.target != null )
                {
                // Send update command, refresh selector state when done
                WbOnOffEntry_update(elm, val );
                if ( elm.target.indexOf("?") < 0 )
                {
                    url = elm.target+"?onoff="+val;
                }
                else
                {
                    url = elm.target+"&onoff="+val;
                }
                logDebug("WbOnOffEntry_send: url ", url );
                var def = doTimedXMLHttpRequest(url, pollerTimeout);
                def.addBoth(pollSoon);
                }
            else
                {
                logError("WbOnOffEntry_send (no target)") ;
                }
            }
        }
    catch( e )
        {
        logError("WbOnOffEntry_send: ", e) ;
        }
}

function WbOnOffEntry_init(pref, patt, post, elm)
    {
    logDebug("initOnOffEntry: ", pref, ", ", patt, ", ", post, ", ", elm) ;

    if (pref) {
        elm.pref = pref ;
        }
    else {
        elm.pref = ''
        }
    if (post) {
        elm.post = post ;
        }
    else {
        elm.post = ''
        }

    elm.title     = elm.getAttribute("wbTitle") ;
    elm.source    = getEndPointSource(elm) ;
    elm.target    = getEndPointTarget(elm) ;
   
    getWidgetBaseClass(elm,"WbOnOffEntry");
    var txt = strip(getElementText(elm))
    if ( txt.length > 0 )
    {
        setWidgetState(elm,txt);
    }
    else
    {
        setWidgetState(elm,"Pending");
        WbOnOffEntry_update(elm," ")
    }

    connect( elm, "onclick", function() { WbOnOffEntry_popup( elm, partial( WbOnOffEntry_send, elm ) ); } );

    elm.handle = setPoller(WbOnOffEntry_request, elm) ;
    }


// Polling callback function, 
// Request and eventually display the status of a button,
function WbOnOffEntry_request(elm)
    {
    logDebug("WbOnOffEntry_request: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(WbOnOffEntry_receive, elm) ;
        }
    else
        {
        logError("WbOnOffEntry_request (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function WbOnOffEntry_receive(elm, req)
    {
    try
        {
        logDebug("WbOnOffEntry_receive (callback): elm: ", elm, ", req: ", req ) ;
        sts = getWbStatus(req) ;
        if ( sts )
            {
            state = sts[2];
            WbOnOffEntry_update(elm, elm.pref+sts[2]+elm.post );
            }
        else
            {
            state = "Absent";
            WbOnOffEntry_update(elm, "-" );
            }
        setWidgetState(elm,state);
        }
    catch( e )
        {
        sts = null ;
        logError("WbOnOffEntry_receive: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

function WbOnOffEntry_update(elm, val)
{
    logDebug("WbOnOffEntry_update: elm: ", elm, ", val: ", val ) ;
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

function WbOnOffEntry_CB( val ) 
{
    np = $("WbOnOffEntry")
    np.callBack( val );
    np.style.visibility ='hidden';
}

function WbOnOffEntry_popup( elm, callBack ) 
{
    logDebug("WbOnOffEntry_popup: ", elm );
    if (!$("WbOnOffEntry"))
    {
        logDebug("WbOnOffEntry_popup: Create " );
        //
        //  Change background to increase contrast with panel 
        //
		// Beware Internet Explorer generates objects for trailing comma
        var rows = [
            [   
                [ {'colSpan':'4'}, SPAN( {'id': 'onoffpadtitle'},"") ]
            ],
            [   
                [ {},IMG({ "src" : "/static/images/numerals/makeOn.png", "onclick":"WbOnOffEntry_CB( 'On' )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/makeOff.png", "onclick":"WbOnOffEntry_CB( 'Off' )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/makeIgnore.png", "onclick":"WbOnOffEntry_CB( 'Ignore' )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/cancel.png", "onclick":"WbOnOffEntry_CB()" } )]
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
				createDOM('colgroup', {'span':'4', 'width':'25%'} ),
                map(row_display, rows)));

        var newDiv = DIV({'id': 'WbOnOffEntry', 'class': 'dataEntry', 'opacity':'0.95'}, newTable );
        appendChildNodes( currentDocument().body, newDiv );
        newDiv.style.position ='absolute';
        newDiv.style.width ='50px';
        newDiv.style.height ='150px';
        newDiv.style.zIndex ='1010';
    }
//    ePos = elementPosition( elm );
//    logDebug("elm position: ", ePos.x, ePos.y ) ;
//    $("WbOnOffEntry").style.top = (ePos.y+10)+'px';
//    $("WbOnOffEntry").style.left = (ePos.x+10)+'px';
    $("WbOnOffEntry").style.top = '70px';
    $("WbOnOffEntry").style.left = '15%';
    $("WbOnOffEntry").callBack = callBack;
    $("WbOnOffEntry").style.visibility ='visible';
    setElementText($("onoffpadtitle"), elm.title );
};
