// $Id: WbDayEntry.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for time display wdiget

// Initial load of a time display object
function loadWbDayEntry()
    {
    logDebug("loadWbDayEntry") ;
    return partial(WbDayEntry_init) ;
    }

function WbDayEntry_init(elm)
    {
    logDebug("WbDayEntry_init: ", elm) ;
    elm.title     = elm.getAttribute("wbTitle") ;
    elm.source    = getEndPointSource(elm) ;
    elm.target    = getEndPointTarget(elm) ;
    elm.textValue = elm.getAttribute("textValue");
    getWidgetBaseClass(elm,"numeric");
    var txt = strip(getElementText(elm))
    if ( txt.length > 0 )
    {
        
        setWidgetState( elm, "Info" );
    }
    else
    {
        setWidgetState( elm, "Pending" );
    }
    logDebug("WbDayEntry_init: ", txt,",", txt.length,",", elm.className) ;

    connect( elm, "onclick", function() { WbDayEntry_popup( elm, partial( WbDayEntry_send, elm ) ); } );

    elm.handle    = setPoller(WbDayEntry_request, elm) ;
    }

function WbDayEntry_send(elm, val)
    {
    logDebug("WbDayEntry_send: val; ", val );
    WbDayEntry_update(elm, val);
    try {
        if ( val || ( val == 0 ) )
            {
            if ( elm.target != null )
                {
                // Send update command, refresh selector state when done
                if ( elm.target.indexOf("?") < 0 )
                {
                    url = elm.target+"?day="+val;
                }
                else
                {
                    url = elm.target+"&day="+val;
                }

                logDebug("WbDayEntry_send: url ", url );
                var def = doTimedXMLHttpRequest(url, pollerTimeout);
                def.addBoth(pollSoon);
                }
            else
                {
                logError("WbDayEntry_send (no target)") ;
                }
            }
        }
    catch( e )
        {
        logError("WbDayEntry_send: ", e) ;
        }
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function WbDayEntry_request(elm)
    {
    logDebug("WbDayEntry_request: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(WbDayEntry_received, elm) ;
        }
    else
        {
        logError("WbDayEntry_request (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function WbDayEntry_received(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req) ;
        logDebug("WbDayEntry_received (callback): elm: ", elm, " req: ", req, ", sts: ", sts);
        if ( sts != null )
            {
            setWidgetState( elm, "Info" );
            elm.textValue = sts[2]
            WbDayEntry_update(elm, elm.textValue);
            }
        else
            {
            setWidgetState( elm, "Absent" );
            WbDayEntry_update(elm, "-------");
            }
        }
    catch( e )
        {
        sts = null ;
        logError("WbDayEntry_received: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

function WbDayEntry_update(elm, val)
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

function WbDayEntry_Done() 
{
    np = $("WbDayEntry");
    logDebug("WbDayEntry_Done: val ", np.textValue );
    np.callBack( np.textValue );
    np.style.visibility ='hidden';
}

function WbDayEntry_Cancel() 
{
    np = $("WbDayEntry");
    np.style.visibility ='hidden';
}

function WbDayEntry_setImage( dayNr, idx )
{
    WbDayEntry_imagesNames = [ "/static/images/numerals/blank.png",
        "/static/images/numerals/selected.png" ];

    idStr = "WbDayEntry_day"+dayNr;
    logDebug("WbDayEntry_setImage for : '"+idStr+"' to "+WbDayEntry_imagesNames[idx] );
    np = $(idStr);
    np.src = WbDayEntry_imagesNames[idx];
}

function WbDayEntry_toggle( dayNr ) 
{
    WbDayEntry_dayBase = "SMTWtFs"
    npd = $("WbDayEntry");
    if (npd.textValue.charAt(dayNr) == '-' )
    {
        npd.textValue = npd.textValue.substr( 0, dayNr ) + WbDayEntry_dayBase.charAt(dayNr) + npd.textValue.substr( dayNr+1 )
        WbDayEntry_setImage( dayNr, 1 );
    }
    else
    {
        npd.textValue = npd.textValue.substr( 0, dayNr ) + '-' + npd.textValue.substr( dayNr+1 )
        WbDayEntry_setImage( dayNr, 0 );
    }
    logDebug("npd.textValue : '"+npd.textValue+"'" );
}

var daysVertical = [
    [ {},
        [
            [ {'colSpan':'2'}, SPAN( {'id': 'daypadtitle'},"") ],
        ]
    ],
    [ { "onclick":"WbDayEntry_toggle( 0 )" },
        [
            [ {},IMG({ "src" : "/static/images/weekdays/sunday.png" } )],
            [ {},IMG({ "src" : "/static/images/numerals/selected.png", 'id':'WbDayEntry_day0' } ) ],
        ]
    ],
    [ { "onclick":"WbDayEntry_toggle( 1 )" },
        [
            [ {},IMG({ "src" : "/static/images/weekdays/monday.png" } )],
            [ {},IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day1" } )],
        ]
    ],
    [ { "onclick":"WbDayEntry_toggle( 2 )" },
        [
            [ {},IMG({ "src" : "/static/images/weekdays/tuesday.png" } )],
            [ {},IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day2" } )],
        ]
    ],
    [ { "onclick":"WbDayEntry_toggle( 3 )" },
        [
            [ {},IMG({ "src" : "/static/images/weekdays/wednesday.png" } )],
            [ {},IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day3" } )],
        ]
    ],
    [ { "onclick":"WbDayEntry_toggle( 4 )" },
        [
            [ {},IMG({ "src" : "/static/images/weekdays/thursday.png" } )],
            [ {},IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day4" } )],
        ]
    ],
    [ { "onclick":"WbDayEntry_toggle( 5 )" },
        [
            [ {},IMG({ "src" : "/static/images/weekdays/friday.png" } )],
            [ {},IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day5" } )],
        ]
    ],
    [ { "onclick":"WbDayEntry_toggle( 6 )" },
        [
            [ {},IMG({ "src" : "/static/images/weekdays/saturday.png" } )],
            [ {},IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day6" } )],
        ]
    ],
    [ {},
        [
            [ {},IMG({ "src" : "/static/images/numerals/cancel.png", "onclick":"WbDayEntry_Cancel()" } )],
            [ {},IMG({ "src" : "/static/images/numerals/set.png", "onclick":"WbDayEntry_Done()" } )],
        ]
    ],
];
        
var daysHorizontal = [
    [ {},
        [
            [ {'colSpan':'2'}, SPAN( {'id': 'daypadtitle'},"") ],
        ]
    ],
    [ {},
        [
            [ { "onclick":"WbDayEntry_toggle( 0 )" },
                IMG({ "src" : "/static/images/weekdays/sunday.png" } )],
            [ { "onclick":"WbDayEntry_toggle( 1 )" },
                IMG({ "src" : "/static/images/weekdays/monday.png" } )],
            [ { "onclick":"WbDayEntry_toggle( 2 )" },
                IMG({ "src" : "/static/images/weekdays/tuesday.png" } )],
            [ { "onclick":"WbDayEntry_toggle( 3 )" },
                IMG({ "src" : "/static/images/weekdays/wednesday.png" } )],
            [ { "onclick":"WbDayEntry_toggle( 4 )" },
                IMG({ "src" : "/static/images/weekdays/thursday.png" } )],
            [ { "onclick":"WbDayEntry_toggle( 5 )" },
                IMG({ "src" : "/static/images/weekdays/friday.png" } )],
            [ { "onclick":"WbDayEntry_toggle( 6 )" },
                IMG({ "src" : "/static/images/weekdays/saturday.png" } )],
        ]
    ],
    [ {},
        [
            [ {"onclick":"WbDayEntry_toggle(0)"},
                IMG({ "src" : "/static/images/numerals/selected.png", 'id':'WbDayEntry_day0' } ) ],
            [ {"onclick":"WbDayEntry_toggle(1)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day1" } )],
            [ {"onclick":"WbDayEntry_toggle(2)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day2" } )],
            [ {"onclick":"WbDayEntry_toggle(3)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day3" } )],
            [ {"onclick":"WbDayEntry_toggle(4)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day4" } )],
            [ {"onclick":"WbDayEntry_toggle(5)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day5" } )],
            [ {"onclick":"WbDayEntry_toggle(6)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day6" } )],
        ]
    ],
    [ {},
        [
            [ {},IMG({ "src" : "/static/images/numerals/cancel.png", "onclick":"WbDayEntry_Cancel()" } )],
            [ {},IMG({ "src" : "/static/images/numerals/set.png", "onclick":"WbDayEntry_Done()" } )],
        ]
    ],
];
        
var daysMixed = [
    [ {},
        [
            [ { "onclick":"WbDayEntry_toggle( 1 )" },
                IMG({ "src" : "/static/images/weekdays/monday.png" } )],
            [ {"onclick":"WbDayEntry_toggle(1)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day1" } )],
            [ { "onclick":"WbDayEntry_toggle( 6 )" },
                IMG({ "src" : "/static/images/weekdays/saturday.png" } )],
            [ {"onclick":"WbDayEntry_toggle(6)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day6" } )],
        ],
    ],
    [ {},
        [
            [ { "onclick":"WbDayEntry_toggle( 2 )" },
                IMG({ "src" : "/static/images/weekdays/tuesday.png" } )],
            [ {"onclick":"WbDayEntry_toggle(2)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day2" } )],
            [ { "onclick":"WbDayEntry_toggle( 0 )" },
                IMG({ "src" : "/static/images/weekdays/sunday.png" } )],
            [ {"onclick":"WbDayEntry_toggle(0)"},
                IMG({ "src" : "/static/images/numerals/selected.png", 'id':'WbDayEntry_day0' } ) ],
        ],
    ],
    [ {},
        [
            [ { "onclick":"WbDayEntry_toggle( 3 )" },
                IMG({ "src" : "/static/images/weekdays/wednesday.png" } )],
            [ {"onclick":"WbDayEntry_toggle(3)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day3" } )],
        ],
    ],
    [ {},
        [
            [ { "onclick":"WbDayEntry_toggle( 4 )" },
                IMG({ "src" : "/static/images/weekdays/thursday.png" } )],
            [ {"onclick":"WbDayEntry_toggle(4)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day4" } )],
            [ {}, ""],
            [ {"onclick":"WbDayEntry_Done()"},
                IMG({ "src" : "/static/images/numerals/set.png" } )],
        ],
    ],
    [ {},
        [
            [ { "onclick":"WbDayEntry_toggle( 5 )" },
                IMG({ "src" : "/static/images/weekdays/friday.png" } )],
            [ {"onclick":"WbDayEntry_toggle(5)"},
                IMG({ "src" : "/static/images/numerals/selected.png", "id" : "WbDayEntry_day5" } )],
            [ {}, ""],
            [ {"onclick":"WbDayEntry_Cancel()"},
                IMG({ "src" : "/static/images/numerals/cancel.png" } )],
        ]
    ]
];
        
function WbDayEntry_popup( elm, callBack )
{
    logDebug("WbDayEntry_popup: ", elm );
    if (!$("WbDayEntry"))
    {
        logDebug("WbDayEntry_popup: Create " );
        cell_display = function (cell) 
            {
			if (cell)
				{
                logDebug("WbDayEntry_popup: ", cell );
				return TD(cell[0], cell[1]);
				}
            }
        row_display = function (row) 
            {
			if (row)
			{
                logDebug("WbDayEntry_popup: ", row );
				return TR(row[0], map(cell_display, row[1]) );
			}
            }

        var newTable = TABLE(null,
            TBODY(null,
				// add a colgroup to the table.
				//createDOM('colgroup', {'span':'7', 'width':'10%'} ),
                map(row_display, daysMixed)
                )
            );

        var newDiv = DIV({'id': 'WbDayEntry', 'class': 'dataEntry', 'position':'absolute', 'z-index': '1010', 'opacity':'0.95'}, newTable );
        appendChildNodes( currentDocument().body, newDiv );
        newDiv.style.position ='absolute';
        newDiv.style.width ='50px';
        newDiv.style.height ='150px';
    }
//    ePos = elementPosition( elm );
//    logDebug("elm position: ", ePos.x, ePos.y ) ;
//    setElementText($("daypadtitle"), elm.title );
    de = $("WbDayEntry");
    de.style.top = '70px';
    de.style.left = '15%';
//    de.style.top = (ePos.y+10)+'px';
//    de.style.left = (ePos.x+10)+'px';
    de.callBack = callBack;
    de.style.visibility ='visible';

    // now set initial value
    // elm.textValue
    if (!elm.textValue)
    {
        de.textValue = elm.getAttribute("textValue");
    }
    else
    {
        de.textValue = elm.textValue;
    }

    if ( !de.textValue || ( de.textValue == "" ) )
    {
        de.textValue = "-------";
    }
    logDebug("textValue: ", de.textValue );

    for (i = 0; i < 7;i++)
    {
        if (de.textValue.charAt(i) == '-')
        {
            WbDayEntry_setImage( i, 0 );
        }
        else
        {
            WbDayEntry_setImage( i, 1 );
        }
    }
}
