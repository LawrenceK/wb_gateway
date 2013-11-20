// $Id: WbTimeEntry.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for time display wdiget

// Initial load of a time display object
function loadWbTimeEntry()
    {
    logDebug("loadWbTimeEntry") ;
    return partial(WbTimeEntry_init) ;
    }

function WbTimeEntry_init(elm)
    {
    logDebug("initTimeEntry: ", elm) ;
    elm.title     = elm.getAttribute("wbTitle") ;
    elm.source    = getEndPointSource(elm) ;
    elm.target    = getEndPointTarget(elm) ;
    elm.textValue = elm.getAttribute("textValue");
    getWidgetBaseClass(elm,"numeric");
    var txt = strip(getElementText(elm))
    if ( txt.length > 0 )
    {
        setWidgetState(elm, "Info");
    }
    else
    {
        setWidgetState(elm, "Pending");
    }
    logDebug("initTimeEntry: ", txt,",", txt.length,",", elm.className) ;

    connect( elm, "onclick", function() { WbTimeEntry_popup( elm, partial( WbTimeEntry_send, elm ) ); } );

    elm.handle    = setPoller(WbTimeEntry_request, elm) ;
    }

function WbTimeEntry_send(elm, val)
    {
    logDebug("WbTimeEntry_send: val; ", val );
    WbTimeEntry_update(elm, val);
    try {
        if ( val || ( val == 0 ) )
            {
            if ( elm.target != null )
                {
                // Send update command, refresh selector state when done
                if ( elm.target.indexOf("?") < 0 )
                {
                    url = elm.target+"?time="+val;
                }
                else
                {
                    url = elm.target+"&time="+val;
                }
                logDebug("WbTimeEntry_send: url ", url );
                var def = doTimedXMLHttpRequest(url, pollerTimeout);
                def.addBoth(pollSoon);
                }
            else
                {
                logError("WbTimeEntry_send (no target)") ;
                }
            }
        }
    catch( e )
        {
        logError("WbTimeEntry_send: ", e) ;
        }
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function WbTimeEntry_request(elm)
    {
    logDebug("WbTimeEntry_request: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(WbTimeEntry_received, elm) ;
        }
    else
        {
        logError("WbTimeEntry_request (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function WbTimeEntry_received(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req) ;
        logDebug("WbTimeEntry_received (callback): elm: ", elm, " req: ", req, ", sts: ", sts);
        if ( sts != null )
            {
            setWidgetState(elm, "Info");
            elm.textValue = sts[2]
            WbTimeEntry_update(elm, elm.textValue);
            }
        else
            {
            setWidgetState(elm, "Absent");
            WbTimeEntry_update(elm, "--:--");
            }
        }
    catch( e )
        {
        sts = null ;
        logError("WbTimeEntry_received: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

function WbTimeEntry_update(elm, val)
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

function WbTimeEntry_getValue(elm)
{
    valElm = getElementsByTagAndClassName("div", "buttonbodycontent", elm)[0];
    if (valElm)
    {
        return valElm.innerHTML;
    }
    return elm.innerHTML;
}

function WbTimeEntry_Done() 
{
//    val = ($("WbTimeEntry_TenHour").numericValue*36000)
//        + ($("WbTimeEntry_Hour").numericValue*3600)
//        + ($("WbTimeEntry_TenMinute").numericValue*600)
//        + ($("WbTimeEntry_Minute").numericValue*60);
    val = "" + $("WbTimeEntry_TenHour").numericValue
        + $("WbTimeEntry_Hour").numericValue
        + ":"
        + $("WbTimeEntry_TenMinute").numericValue
        + $("WbTimeEntry_Minute").numericValue
        + ":00";
    np = $("WbTimeEntry");
    logDebug("WbTimeEntry_Done: val ", val );
    np.callBack( val );
    np.style.visibility ='hidden';
}

function WbTimeEntry_Cancel() 
{
    np = $("WbTimeEntry");
    np.style.visibility ='hidden';
}

// in an array so we caan preload them as we bring up popup.
WbTimeEntry_imagesNames = [ "/static/images/numerals/0.png",
    "/static/images/numerals/1.png",
    "/static/images/numerals/2.png",
    "/static/images/numerals/3.png",
    "/static/images/numerals/4.png", 
    "/static/images/numerals/5.png",
    "/static/images/numerals/6.png",
    "/static/images/numerals/7.png",
    "/static/images/numerals/8.png",
    "/static/images/numerals/9.png" ];

function WbTimeEntry_SetImage( id, val ) 
{
    np = $(id);
    np.numericValue = val;
    logDebug("WbTimeEntry_SetImage: val ", val, "image ", WbTimeEntry_imagesNames[val] );
    np.src = WbTimeEntry_imagesNames[val]
}

function WbTimeEntry_TenHourInc( val ) 
{
    np = $("WbTimeEntry_TenHour");
    np.numericValue = np.numericValue + val;
    if ( np.numericValue > 2 ) np.numericValue = 2
    if ( np.numericValue < 0 ) np.numericValue = 0
    np.src = WbTimeEntry_imagesNames[np.numericValue];
    // if we select 20 something hours, limit lower to 3 or less.
    if ( np.numericValue == 2 )
    {
        np2 = $("WbTimeEntry_Hour");
        if ( np2.numericValue > 3 ) 
        {
            np2.numericValue = 3
            np2.src = WbTimeEntry_imagesNames[np2.numericValue];
        }
    }
}

function WbTimeEntry_HourInc( val ) 
{
    np = $("WbTimeEntry_Hour");
    np.numericValue = np.numericValue + val;
    np2 = $("WbTimeEntry_TenHour");
    if ( np2.numericValue > 1 ) 
    {
        if ( np.numericValue > 3 ) np.numericValue = 3
    }
    else
    {
        if ( np.numericValue > 9 ) np.numericValue = 9
    }
    if ( np.numericValue < 0 ) np.numericValue = 0

    np.src = WbTimeEntry_imagesNames[np.numericValue];
}

function WbTimeEntry_TenInc( np, val ) 
{
    np.numericValue = np.numericValue + val;
    if ( np.numericValue > 5 ) np.numericValue = 5
    if ( np.numericValue < 0 ) np.numericValue = 0
    np.src = WbTimeEntry_imagesNames[np.numericValue];
}

function WbTimeEntry_UnitInc( np, val ) 
{
    np.numericValue = np.numericValue + val;
    if ( np.numericValue > 9 ) np.numericValue = 9
    if ( np.numericValue < 0 ) np.numericValue = 0
    np.src = WbTimeEntry_imagesNames[np.numericValue];
}

function WbTimeEntry_TenMinuteInc( val ) 
{
    WbTimeEntry_TenInc( $("WbTimeEntry_TenMinute"), val );
}

function WbTimeEntry_MinuteInc( val ) 
{
    WbTimeEntry_UnitInc( $("WbTimeEntry_Minute"), val );
}

function WbTimeEntry_TenSecondInc( val ) 
{
    WbTimeEntry_TenInc( $("WbTimeEntry_TenSecond"), val );
}

function WbTimeEntry_SecondInc( val ) 
{
    WbTimeEntry_UnitInc( $("WbTimeEntry_Second"), val );
}

function charToIdx( ch )
{
    if ( ( ch >= '0' ) && ( ch <= '9' ) )
    {
        return ch - 0;  // to integer
    }
    else
    {
        return 0;
    }
}

function WbTimeEntry_popup( elm, callBack )
{
    val = WbTimeEntry_getValue(elm)
    logDebug("WbTimeEntry_popup: ", elm, val );
    if ( !val )
    {
        val = "00:00";
    }
    // TODO handle seconds.
    if (!$("WbTimeEntry"))
    {
        logDebug("WbTimeEntry_popup: Create " );
        var rowsHHMM = [
            [   
                [ {},IMG({ "src" : "/static/images/numerals/up.png", "onclick":"WbTimeEntry_TenHourInc( 1 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/up.png", "onclick":"WbTimeEntry_HourInc( 1 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/up.png", "onclick":"WbTimeEntry_TenMinuteInc( 1 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/up.png", "onclick":"WbTimeEntry_MinuteInc( 1 )" } )]
            ],
            [
                [ {},IMG({ "src" : "/static/images/numerals/0.png", 'id':'WbTimeEntry_TenHour' } )],
                [ {},IMG({ "src" : "/static/images/numerals/1.png", 'id':'WbTimeEntry_Hour' } )],
                [ {},IMG({ "src" : "/static/images/numerals/2.png", 'id':'WbTimeEntry_TenMinute' } )],
                [ {},IMG({ "src" : "/static/images/numerals/3.png", 'id':'WbTimeEntry_Minute' } )]
            ],
            [
                [ {},IMG({ "src" : "/static/images/numerals/down.png", "onclick":"WbTimeEntry_TenHourInc( -1 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/down.png", "onclick":"WbTimeEntry_HourInc( -1 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/down.png", "onclick":"WbTimeEntry_TenMinuteInc( -1 )" } )],
                [ {},IMG({ "src" : "/static/images/numerals/down.png", "onclick":"WbTimeEntry_MinuteInc( -1 )" } )]
            ],
            [   
                [ {},IMG({ "src" : "/static/images/numerals/cancel.png", "onclick":"WbTimeEntry_Cancel()" } )],
                [ {},IMG({ "src" : "/static/images/numerals/set.png", "onclick":"WbTimeEntry_Done()" } )]
            ]
        ];
        cell_display = function (aCell) 
            {
			if (aCell)
				{
	            return TD(aCell[0], aCell[1]);
				}
            }
        row_display = function (aRow) 
            {
			if (aRow)
				{
				return TR(null, map(cell_display, aRow) );
				}
            }

        var newTable = TABLE(null,
            TBODY(null,
				createDOM('colgroup', {'span':'4', 'width':'25%'} ),
                map(row_display, rowsHHMM)));

        var newDiv = DIV({'id': 'WbTimeEntry', 
                        'class': 'dataEntry', 
                        'opacity':'0.95'}, 
//                    SPAN( {'id': 'timepadtitle'},""),
                newTable );
        appendChildNodes( currentDocument().body, newDiv );
        newDiv.style.position ='absolute';
        newDiv.style.width ='50px';
        newDiv.style.height ='150px';
        newDiv.style.zIndex ='1010';
    }
    logDebug("elm title: ", elm.title ) ;
//    ePos = elementPosition( elm );
//    logDebug("elm position: ", ePos.x, ePos.y ) ;
    $("WbTimeEntry").style.top = '70px';
    $("WbTimeEntry").style.left = '15%';
//    $("WbTimeEntry").style.top = (ePos.y+10)+'px';
//    $("WbTimeEntry").style.left = (ePos.x+10)+'px';
    $("WbTimeEntry").callBack = callBack;
    $("WbTimeEntry").style.visibility ='visible';

//    setElementText($("timepadtitle"), elm.title );
    WbTimeEntry_SetImage( 'WbTimeEntry_TenHour', charToIdx( val[0]) ) 
    WbTimeEntry_SetImage( 'WbTimeEntry_Hour', charToIdx( val[1]) ) 
    WbTimeEntry_SetImage( 'WbTimeEntry_TenMinute', charToIdx( val[3]) ) 
    WbTimeEntry_SetImage( 'WbTimeEntry_Minute', charToIdx( val[4]) ) 
}
