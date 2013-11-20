// $Id: WbFlashMeter.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// ----------------------------------------------------------------
//  The Xml returned should have a Val and Limit element
//  If Limit is not present it defaults to 100.
//  The wbType for this widget is "FlashMeter".
// ----------------------------------------------------------------
//
// This is the interface to a flash meter and analogue control i.e. dimmers
// These are the varaiables that are set ina flash movie to control it.
//
// var currentPosition; This is updated with the current value by the javascript/webpage
// var setPointLow; This is updated with the current low set point by the javascript/webpage
// var setPointHigh; This is updated with the current high set point by the javascript/webpage
// var displayText; This is updated with the current display text by the javascript/webpage
// var state; This is updated with the current state of the javascript/webpage
// var ptitle; This is the title for the widget set by the javascript/webpage
// var meteMin; This is initialised by the javascript/webpage
// var meterMax; This is initialised by the javascript/webpage
// var labels; These are a set of labels for the meter
// var callBack; This is a URL which is called by the flash env to send a requested setting back to the gateway
// var backgroundColor; This is initalised by the javascrip/webpage to show the current background colour for the widgets area.
//		This is to enable workaround for the lack of transparency.

function loadFlashMeter(pref, patt, post)
    {
    logDebug("loadFlashMeter") ;
    if (!pref) pref = "" ;
    if (!patt) patt = "#.#" ;
    if (!post) post = "" ;
    return partial(initFlashMeter, pref, patt, post) ;
    }

function loadFlashDimmer(pref, patt, post)
    {
    logDebug("loadFlashDimmer") ;
    if (!pref) pref = "" ;
    if (!patt) patt = "#.#" ;
    if (!post) post = "" ;
    return partial(initFlashMeter, pref, patt, post) ;
    }

function FlashMeterAdjustValue(elm, val)
    {
    // convert input value from user units to a 0-100 range
    var r = 0;
    if ( val >= elm.minvalue )
    {
        if ( val > elm.maxvalue )
        {
            r = 100;
        }
        else
        {
            r = ( ( val - elm.minvalue ) * ( 100/(elm.maxvalue - elm.minvalue) ) );
        }
    }
    logDebug("FlashMeterAdjustValue min -", elm.minvalue, " min -", elm.maxvalue, " val - ", val, " r -", r);
    return r;
    }

function initFlashMeter(pref, patt, post, elm)
    {
    logDebug("initFlashMeter: ", elm) ;
    try {
        elm.pref      = pref ;
        elm.format    = numberFormatter(patt) ;
        elm.post      = post ;
        elm.curvalue  = 0;
        elm.minvalue  = 0;
        elm.maxvalue  = 100;
        elm.setlow    = 0;
        elm.sethigh   = 100;
        elm.title     = "";
        elm.labels    = "";
        getWidgetBaseClass(elm,"FlashMeter");
        setWidgetState( elm, "" );
        // read these first.
        v = elm.getAttribute("minvalue");
        if ( v )
            {
            elm.minvalue = v;
            }
        v = elm.getAttribute("maxvalue");
        if ( v )
            {
            elm.maxvalue = v;
            }
        v = elm.getAttribute("curvalue");
        if ( v )
            {
            elm.curvalue = v;
            }
        v = elm.getAttribute("setlow");
        if ( v )
            {
            elm.setlow = v;
            }
        v = elm.getAttribute("sethigh");
        if ( v )
            {
            elm.sethigh =  v;
            }
        v = elm.getAttribute("metertitle");
        if ( v )
            {
            elm.title = v;
            }
        v = elm.getAttribute("labels");
        if ( v )
            {
            elm.labels = v;
            }

        elm.source    = getEndPointSource(elm) ;
        if ( elm.source == null )
        {
            elm.source = ""
        }
        elm.callBack    = getEndPointTarget(elm) ;
        if ( elm.callBack == null )
        {
            elm.callBack = ""
        }

        // Create sub elements.
        movie = elm.getAttribute("flashMovie");
        var elmCol = Color.fromBackground(elm);

        if ( movie )
            {
            // create OBJECT and EMBED
            // TODO calculate containing element size to set flash size.
            var h = elm.getAttribute("height");
            var w = elm.getAttribute("width");
            var moviePar = '&ptitle=' + escape(elm.title)
                    +'&meterMin='+ escape(elm.minvalue)
                    +'&meterMax='+ escape(elm.maxvalue)
                    +'&currentPosition='+ FlashMeterAdjustValue(elm, elm.curvalue)
                    +'&setPointLow='+ FlashMeterAdjustValue(elm, elm.setlow)
                    +'&setPointHigh='+ FlashMeterAdjustValue(elm, elm.sethigh)
                    +'&labels=' + escape(elm.labels)
                    +'&callBack=' + escape(elm.callBack)
                    //+'&backGroundColour=' + elmCol.toHexString()
                    +'&displayText='+ escape(elm.pref+elm.format(elm.curvalue)+elm.post)
                    +'&state=0';
            logDebug("flashVars: ", moviePar) ;
            
            // NOTE IE uses object values, firefox uses embed tag.
            var o = '<object'
                        +' classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"'
                        +' codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,65,0"'
                        +' width="'+w+'px"'
                        +' height="'+h+'px">'
                        + '<param name="movie" value="'+ movie +'" />'
                        + '<param name="FlashVars" value="'+ moviePar +'"/>'
                        + '<param name="quality" value="high" />'
                        + '<param name="wmode" value="transparent">'
                        + '<embed src="'+ movie +'"'
                            +' type="application/x-shockwave-flash"'
                            +' flashvars="' + moviePar +'"'
                            +' quality="high"'
                            +' width="'+w+'px"'
                            +' height="'+h+'px"'
                            +' swLiveConnect ="true"'
                            +' wmode="transparent"'
                            +' pluginspage="http://www.macromedia.com/go/getflashplayer">'
                        +'</embed>'
                    + '</object>';
            logDebug("object: ", o) ;
            elm.innerHTML = '';
            elm.innerHTML = o;

//        elm.appendChild( IMG( {'src':imageFile, 'hspace':'0', 'height': v } ) );
            }

        setPoller(requestFlashMeter, elm);
        }
    catch( e )
        {
        logError("initFlashMeter: ", e) ;
        }
    }

function flashMeter_doWbTarget( tgt )
    {
    logDebug("flashMeter_doWbTarget: ", tgt );
    try
        {
        var def = doTimedXMLHttpRequest( tgt, pollerTimeout );
        def.addBoth(pollSoon);
        }
    catch( e )
        {
        logError("flashButton_doWbTarget: ", e) ;
        }
    }
    
function flashMeterGetFlashObject( elm )
    {
    var nodes = elm.getElementsByTagName( "embed" );
    if ( nodes.length == 0 )
        {
        nodes = elm.getElementsByTagName( "object" );
        }
    var fl = nodes[0];
    return fl;
    }

function flashMeterSetCurrentPosition( elm, pos )
    {
    var fl = flashMeterGetFlashObject( elm );
    if (fl)
        {
        logDebug("flashMeterSetCurrentPosition: ", fl, " ", pos );
        fl.SetVariable('currentPosition', FlashMeterAdjustValue(elm, pos));
        fl.SetVariable('displayText', elm.pref+elm.format(pos)+elm.post );
        fl.SetVariable('state', 1 );    // Ok state
        fl.TCallFrame('/', 0);  // trigger flash to update graphics
        }
    }

function flashMeterSetLow( elm, lo )
    {
    var fl = flashMeterGetFlashObject( elm );
    if (fl)
        {
        logDebug("flashMeterSetLow: ", fl, " ", lo );
        fl.SetVariable('setPointLow', FlashMeterAdjustValue(elm, lo));
        fl.TCallFrame('/', 0);  // trigger flash to update graphics
        }
    }

function flashMeterSetHigh( elm, hi )
    {
    var fl = flashMeterGetFlashObject( elm );
    if (fl)
        {
        logDebug("flashMeterSetHigh: ", fl, " ", hi );
        fl.SetVariable('setPointHigh', FlashMeterAdjustValue(elm, hi) );
        fl.TCallFrame('/', 0);  // trigger flash to update graphics
        }
    }

function flashMeterSetState( elm, st )
    {
    var fl = flashMeterGetFlashObject( elm );
    if (fl)
        {
        logDebug("flashMeterSetState: ", fl, " ", st );
        fl.SetVariable('state', st );
        fl.TCallFrame('/', 0);  // trigger flash to update graphics
        }
    }

function flashMeterSetTitle( elm, st )
    {
    var fl = flashMeterGetFlashObject( elm );
    if (fl)
        {
        logDebug("flashMeterSetTitle: ", fl, " ", st );
        fl.SetVariable('ptitle', st);
//    fl.TCallFrame('/', 0);
        }
    }

// Polling callback function,
// Request and eventually display the status of a button,
function requestFlashMeter(elm)
    {
    logDebug("requestFlashMeter: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(updateFlashMeter, elm) ;
        }
    else
        {
        logError("requestFlashMeter (no source)") ;
        }
    return ;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function updateFlashMeter(elm, req)
    {
    logDebug("updateFlashMeter (callback): elm: ", elm,
             ", req: ", req ) ;
    try
        {
        response = req.responseXML.documentElement ;
        var curvalue = getElementFloatByTagName(response, "val");
        if ( curvalue != null )
            {
            elm.curvalue = curvalue;
            flashMeterSetCurrentPosition(elm, elm.curvalue);
            }

        var v = getElementFloatByTagName(response, "setlow");
        if ( v )
            {
            elm.setlow = FlashMeterAdjustValue(elm, v);
            }

        v = getElementFloatByTagName(response, "sethigh");
        if ( v )
            {
            elm.sethigh = FlashMeterAdjustValue(elm, v);
            }
        logDebug("updateFlashMeter: elm: ", elm,
                 "cur: ", curvalue, ", setLow: ", elm.setlow, "setHigh: ", elm.sethigh );
        }
    catch( e )
        {
        sts = null ;
        logError("updateFlashMeter: ", e) ;
        flashMeterSetState( elm, 0 );
        }
    return req ;    // Return request to next in callback chain
    }


