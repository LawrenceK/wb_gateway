// $Id: WbNumericBar.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for numeric bar display

// ----------------------------------------------------------------
// Bar display of a numeric value.
//  The Xml returned should have a Val and Limit element
//  If Limit is not present it defaults to 100.
//  The wbType for this widget is "NumericBar".
// ----------------------------------------------------------------

// Initial load of a caption object
function loadNumericBar()
    {
    logDebug("loadNumericBar") ;
    return partial(initNumericBar) ;
    }

var defaultNumericBarGraphics = [ '/static/images/green.png', '/static/images/red.png' ,'/static/images/green.png' ];
function initNumericBar(elm)
    {
    logDebug("initNumericBar: ", elm) ;
    try {
        elm.curvalue  = 0;
        elm.minvalue  = 0;
        elm.maxvalue  = 100;
        var v = elm.getAttribute("curvalue");
        if ( v )
            {
            elm.curvalue = v;
            }
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

        elm.source    = getEndPointSource(elm) ;
        //elm.className = "textPending" ;
        // Create sub elements.
        // need a div with three graphics.
        var nodes = elm.getElementsByTagName("img");
        if ( nodes.length <= 0 )    // this test allows the graphics to be already created
            {
            // Create the 3 elements that make up a bar.
            logDebug("initNumericBar: addElements", elm) ;
            v = elm.getAttribute("height");
            if (v == 0)
                {
                v = 10;
                }
            for ( idx = 0; idx < 3; ++idx )
                {
                var imageFile = defaultNumericBarGraphics[idx];
                var attrNode = elm.getAttributeNode("graphic"+idx );
                if ( attrNode != null )
                    {
                    imageFile = attrNode.value;
                    if ( ( imageFile == "" ) && (idx == 0 ) )
                        {
                        // must always have first graphic.
                        // all others are optional
                        imageFile = defaultNumericBarGraphics[idx];
                        }
                    }
                logDebug("initNumericBar: addElements", elm, " image: ", imageFile );
                if ( imageFile != "" )
                    {
                    elm.appendChild( IMG( {'src':imageFile, 'hspace':'0', 'height': v, 'width': 1 } ) );
                    }
                }
            }

        // go through and remove text elements between images.
        var idx = elm.childNodes.length
        while ( idx > 0 )
            {
            --idx;
            if ( elm.childNodes[idx].nodeType == 3 )   // #TEXT node
                {
                removeElement( elm.childNodes[idx] );
                ++idx;  // so we do not skip next element.
                }
            }

        // if we have three graphics, the middle one is a cursor.
        nodes = elm.getElementsByTagName("img");
        if ( nodes.length > 2 )
            {
            nodes[1].width = 10;
            }
        resizeNumericBar(elm);
        
        updateNumericBarWidths(elm);    // use defaults.
        setPoller(requestNumericBar, elm);
        // onresize does not seem to trigger unless connected elsehwre other than element.
        //connect(elm, "onresize", resizeNumericBar ); 
        connect(window, "onresize", partial(resizeNumericBar,elm) ); 
        }
    catch( e )
        {
        logError("initNumericBar: ", e) ;
        }

    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestNumericBar(elm)
    {
    logDebug("requestNumericBar: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(updateNumericBar, elm) ;
        }
    else
        {
        logError("requestNumericBar (no source)") ;
        }
    return ;
    }

function resizeNumericBar(elm)
    {
    logDebug("resizeNumericBar: ", elm) ;
    var nodes = elm.getElementsByTagName("img");
    if ( nodes.length > 0 )
        {
        // set small so the size is of the overall element
        // better effect when we resize the browser.
        nodes[0].width = 1;
        var tw = 0;
        var ew = 0;
        var v = elm.getAttribute("width");
        if ( v )
            {
            ew = v;
            }
        else
            {
            ew = computedStyle(elm, 'width');
            if ( ew != "auto" )
                {
                ew = parseInt(ew, 10);
                }
            else
                {
                ew = 100; // arbitrary
                }
            }
        logDebug("resizeNumericBar: ", elm, ", ew: ", ew );
        if ( nodes.length > 2 )
            {
//            nodes[1].width = 2; // cursor graphic
            nodes[2].width = 1;
            tw = ew - nodes[1].width ;
            }
        else
        if ( nodes.length > 1 )
            {
            // no cursor
            nodes[1].width = 1;
            tw = ew;
            }
        elm.totalWidth = tw - 1;
        logDebug("resizeNumericBar: ", elm, ", totalWidth: ", elm.totalWidth );
        }
    }

// 
// Update the widths of the numeric bars.
function updateNumericBarWidths(elm)
    {
    logDebug("updateNumericBarWidths: elm: ", elm );
    var nodes = elm.getElementsByTagName("img");
    if ( nodes.length > 0 )
        {
        var valueRange = elm.maxvalue - elm.minvalue;
        var valueOs = elm.curvalue - elm.minvalue;
        var totalWidthPx = elm.totalWidth;

        var left;
        var right;
        // first element width is based on current value
        // multiply first.
//        alert("updateNumericBarWidths " + totalWidthPx + " " + valueOs + " " + valueRange);
        left = ( totalWidthPx * valueOs ) / valueRange;
        right = ( totalWidthPx * (valueRange-valueOs) ) / valueRange
//        alert("updateNumericBarWidths " + left + " " + right);

        logDebug("updateNumericBarWidths: elm: ", elm, 
             ", min: ", elm.minvalue, "cur: ", elm.curvalue, "max: ", elm.maxvalue, 
             ", totalWidthPx: ", totalWidthPx,", valueRange: ", valueRange,", valueOs: ", valueOs ) ;
        logDebug("updateNumericBarWidths: elm: ", elm, 
                 ", left: ", left,", right: ", right ) ;
        nodes[0].width = left;
        if ( nodes.length > 1 )
            {
            if ( nodes.length > 2 )
                {
                // the third graphic should only be 1 pixel (for now)
                nodes[2].width = right;
//                nodes[2].width = right - nodes[1].width;
                }
            else
                {
                nodes[1].width = right;
                }
            }
        }
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function updateNumericBar(elm, req)
    {
    logDebug("updateNumericBar (callback): elm: ", elm, 
             ", req: ", req ) ;
    try
        {
        var response = null ;    
        try
            {
            response = req.responseXML.documentElement ;
            }
        catch(e)
            {
            logWarning( "updateNumericBar: no response: ", e) ;
            }
        if ( response != null )
            {
            var curvalue = getElementFloatByTagName(response, "val");
            var minvalue = getElementFloatByTagName(response, "minvalue");
            var maxvalue = getElementFloatByTagName(response, "maxvalue");

            logDebug("updateNumericBar: elm: ", elm, 
                     ", min: ", minvalue, "cur: ", curvalue, "max: ", maxvalue ) ;

            if ( curvalue != null )
                {
                if ( minvalue != null )
                    {
                    elm.minvalue = minvalue;
                    }
                if ( maxvalue != null )
                    {
                    elm.maxvalue = maxvalue;
                    }
                if ( curvalue > elm.maxvalue )
                    {
                    elm.curvalue = elm.maxvalue;
                    }
                else if ( curvalue < elm.minvalue )
                    {
                    elm.curvalue = elm.minvalue;
                    }
                else
                    {
                    elm.curvalue = curvalue;
                    }
                updateNumericBarWidths(elm);
                }
            }
        }
    catch( e )
        {
        sts = null ;
        logError("updateNumericBar: ", e) ;
        }

    return req ;    // Return request to next in callback chain
    }


