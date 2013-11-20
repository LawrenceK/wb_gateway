// $Id: WbPanel.js 1406 2008-05-23 01:22:58Z webbrick $
//
// Javascript library for WebBrick control panel interaction widgets

// ----------------------------------------------------------------
// Panel functions
// ----------------------------------------------------------------

function changeBackground(theme)
    {
    document.body.className = theme ;
    }

function changeBG(){
	document.body.className = bimages[bindex] ;
	bindex++ ;
	if (bindex >= bimages.length)
		{
		bindex = 0 ;
		}
	setTimeout("changeBG()", 5000);
}




// Change information bar content for the current document
// The information bar is a 1-row table with id "wbInfoBar"
// Supplied arguments are text values set into successive cells
// ('arguments' is a Javascript special variable.
function changeInfoBar()
    {
    var ib  = document.getElementById("wbInfoBar") ;
    var tr  = ib.rows[0] ;
    var tds = tr.cells ;
    for ( var i = 0 ; i < arguments.length ; i++ )
        {
        if ( i < tds.length )
            {
            tds[i].nodeValue = arguments[i] ;
            }
        }
    }

// ----------------------------------------------------------------
// Caption functions
// ----------------------------------------------------------------

// Initial load of a caption object
function loadCaption()
    {
    logDebug("loadCaption") ;
    return initCaption ;
    }

function initCaption(elm)
    {
    logDebug("initCaption: ", elm) ;
    elm.className = "caption"
    }



// ----------------------------------------------------------------
// Text value display functions
// ----------------------------------------------------------------

// Initial load of a caption object
function loadTextDisplay(pref, post)
    {
    logDebug("loadTextDisplay") ;
    if (!pref) pref = "" ;
    if (!post) post = "" ;
    return partial(initTextDisplay, pref, post) ;
    }

function initTextDisplay(pref, post, elm)
    {
    logDebug("initTextDisplay: ", pref, ", ", post, ", ", elm) ;
    elm.pref      = pref ;
    elm.post      = post ;
    elm.source    = getEndPointSource(elm) ;
    elm.className = "textPending" ;
    setPoller(requestTextState, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestTextState(elm)
    {
    logDebug("requestTextState: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, 5.0) ;
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
        elm.className = "textPresent" ;
        setElementText(elm, elm.pref+sts[2]+elm.post) ;
        }
    else
        {
        elm.className = "textAbsent" ;
        setElementText(elm, elm.pref+"???"+elm.post) ;
        }
    return req ;    // Return request to next in callback chain
    }


// ----------------------------------------------------------------
// Numeric value display functions
// ----------------------------------------------------------------

// Initial load of a caption object
function loadNumericDisplay(pref, patt, post)
    {
    logDebug("loadNumericDisplay") ;
    if (!pref) pref = "" ;
    if (!patt) patt = "#.#" ;
    if (!post) post = "" ;
    return partial(initNumericDisplay, pref, patt, post) ;
    }

function initNumericDisplay(pref, patt, post, elm)
    {
    logDebug("initNumericDisplay: ", pref, ", ", patt, ", ", post, ", ", elm) ;
    elm.pref      = pref ;
    elm.format    = numberFormatter(patt) ;
    elm.post      = post ;
    elm.source    = getEndPointSource(elm,"wbSource") ;
    elm.className = "numericPending" ;
    setPoller(requestNumericState, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestNumericState(elm)
    {
    logDebug("requestNumericState: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, 5.0) ;
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
        elm.className = "numericPresent" ;
        setElementText(elm, elm.pref+elm.format(sts[2])+elm.post) ;
        }
    else
        {
        elm.className = "numericAbsent" ;
        setElementText(elm, elm.pref+"???"+elm.post) ;
        }
    return req ;    // Return request to next in callback chain
    }


// ----------------------------------------------------------------
// Button functions
// ----------------------------------------------------------------

// Initial load of a button object
// If 'toggle' is not True, the button does not attempt to toggle its state,
// and remains dormant unless the specified source value reads as true.
function loadButton(toggle)
    {
    logDebug("loadButton: ", toggle) ;
    if (!toggle) toggle = false ;
    return partial(initButton,toggle) ;
    }

// Initialize a button to pending state
function initButton(toggle, btn)
    {
    logDebug("initButton: ", btn) ;
    // TODO: pick up mapval labels from the HTML file
    // (cf. push button selector object)
    btn.mapval  = ["Off", "On"] ;
    btn.toggle  = toggle ;
    btn.request = "Dormant"
    btn.source  = getEndPointSource(btn,"wbSource") ;
    btn.target  = getEndPointTarget(btn,"wbTarget") ;
    connect(btn, "onclick", clickButton ); 
    setButtonState(btn, "Pending") ;
    setPoller(requestButtonState, btn) ;
    //// requestButtonState(btn) ;
    }

// Respond to click of a push button
//
// This function contains logic to toggle locally as well as to allow remote
// toggling on the WebBrick.  This will be effective only if the button target
// is a DO value.
function clickButton()
    {
    // Update requested value
    var btn    = this ;
    var setval = "" ;
    if ( btn.toggle )
        {
        switch (btn.request)
            {
            case "Off":     btn.request = "On" ;    setval = "F" ;  break ;
            case "On":      btn.request = "Off" ;   setval = "N" ;  break ;
            }
        }
    logDebug("clickButton: ", btn, 
             ", target: ", btn.target, ", request: ", btn.request) ;
    // Now proceed to set requested value
    if ( btn.target != null )
        {
        // Send update command, refresh selector state when done
        setButtonState(btn, "Pending") ;
        var def = doTimedXMLHttpRequest(btn.target+setval, 4.9) ;
        def.addBoth(pollNow) ;
        }
    else
        {
        logError("clickButton (no target)") ;
        }
    return false ;      // Suppresss any default onClick action
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestButtonState(btn)
    {
    logDebug("requestButtonState: ", btn.request, ", ", btn.source) ;
    if ( btn.source )
        {
        var def = doTimedXMLHttpRequest(btn.source, 4.8) ;
        def.addBoth(updateButtonStatus, btn) ;
        }
    else
        {
        // No source:  just reflect button state selected
        setButtonState(btn, btn.request) ;
        }
    return ;
    }

// Receive response to button status query
// The asynchronous callback supplies the HTTP request object
function updateButtonStatus(btn, req)
    {
    try
        {
        sts = getWbStatusBool(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatusBool: ", e) ;
        }
    logDebug("updateButtonStatus (callback): btn: ", btn, 
             ", req: ", req, ", sts: ", sts) ;
    if ( sts != null )
        {
        // Use numeric status value as index to get state name
        state = btn.mapval[sts[2]]
        }
    else
        {
        state = "Absent"
        }
    setButtonState(btn, state) ;
    return req ;    // Return request to next in callback chain
    }

// Set button state for display
function setButtonState(btn,state)
    {
    logDebug("setButtonState: ", btn.firstChild.data, " := ", state) ;
    btn.state     = state ;
    btn.className = "button"+state ;
    }

// ----------------------------------------------------------------
// Selector functions
// ----------------------------------------------------------------

// This higher order function returns a function to initialize a
// selector control that uses an array of pushbuttons to perform a 
// selection from two or more alternatives.  The pushbuttons are 
// presumed to be child <td> elements of the display element to
// which the returned function is applied.
//
// The values consist of a 2-element array, the first containing an
// correspodning WebBrick selector value for each successive button in
// the selector, and the second being a mapping from selector value to
// the state name used to decide which button is to be active.
// Buttons (1=On,0=Off) would be represented as [[1,0],["Off","On"]],
//
function loadPushSelect(vals)
    {
    logDebug("loadPushSelect: ", vals) ;
    return partial(initPushSelect,vals) ;
    }

function initPushSelect(vals,sel)
    {
    logDebug("initPushSelect: ", sel, ", vals: ", vals) ;
    sel.source  = getEndPointSource(sel,"wbSource") ;
    logDebug("initPushSelect: ", sel, ", vals: ", vals, ", source: ", sel.source) ;
    sel.mapval  = vals[1] ;
    sel.request = "Off" ;
    // TODO: build list of buttons to avoid further domWalks
    domWalk(sel,partial(initPushSelectBtn,sel),"td",vals) ;
    setPoller(requestSelectorState, sel) ;
    //// requestSelectorState(sel) ;
    }

function initPushSelectBtn(sel,btn,i,vals)
    {
    btn.selector  = sel ;
    btn.selectVal = vals[1][vals[0][i]] ;
    btn.target    = getEndPointTarget(btn,"wbTarget") ;
    btn.targetVal = vals[0][i] ;
    connect(btn, "onclick", clickPushSelectBtn ); 
    logDebug("initPushSelectBtn: [", i, "], ", btn.firstChild.data, 
             ", ", btn.selectVal, ", ", btn.target) ;
    setButtonState(btn, "Pending") ;
    }

// Respond to click of selector button
function clickPushSelectBtn()
    {
    // Update requested value
    var sel     = this.selector ;
    sel.request = this.selectVal ;
    logDebug("clickPushSelectBtn: ", this, ", selectVal: ", this.selectVal, 
             ", target: ", this.target, ", targetVal: ", this.targetVal) ;
    // Now proceed to set requested value
    if ( this.target != null )
        {
        // Send update command, refresh selector state when done
        domWalk(sel,(function (btn) { setButtonState(btn, "Pending") })) ;
/// LPK why add targetval
//        var def = doTimedXMLHttpRequest(this.target+this.targetVal, 5.2) ;
        var def = doTimedXMLHttpRequest(this.target, 5.2) ;
        def.addBoth(pollNow) ;
        }
    else
        {
        logError("clickPushSelectBtn (no target)") ;
        }
    return false ;      // Suppresss any default onClick action
    }

// Poller callback function, 
// Request and eventually display the status of a selector
// sel - the HTML element to which the request relates
// req - the request object supplied by the asynchronous callback
function requestSelectorState(sel)
    {
    logDebug("requestSelectorState: ", sel.request, ", ", sel.source) ;
    if ( sel.source )
        {
        var def = doTimedXMLHttpRequest(sel.source, 5.3) ;
        def.addBoth(updateSelectorStatus, sel) ;
        }
    else
        {
        // No source:  just reflect button state selected
        setSelectorState(sel, sel.request) ;
        }
    }


// Display-update callback function:
// Receive response to selector status query
// sel - the HTML element to which the request relates
// req - the request object supplied by the asynchronous callback
function updateSelectorStatus(sel, req)
    {
    try
        {
        sts = getWbStatusBool(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatusBool: ", e) ;
        }
    logDebug("updateSelectorStatus (callback): sel: ", sel, 
             ", req: ", req, ", sts: ", sts) ;
    if ( sts != null )
        {
        // Use numeric status value as index to get state name
        state = sel.mapval[sts[2]]
        }
    else
        {
        state = "Absent"
        }
    setSelectorState(sel, state) ;
    return req ;    // Return request to next in callback chain
    }

// Set selector state for display
function setSelectorState(sel, state)
    {
    logDebug("setSelectorState: ", state) ;
    sel.state     = state ;
    sel.className = "select"+state ;
    domWalk(sel,showPushSelectBtn,"td",state) ;
    }

// Set display of single selector pushbutton
function showPushSelectBtn(btn, i, state)
    {
    // logDebug("showPushSelectBtn: ", btn.firstChild.data, ", ", btn.selectVal, ", ", state) ;
    if ( (state != "Absent") && (state != "Pending") && (state != "Locked") )
        {
        if (state == btn.selectVal)
            {
            state = "Selected"
            }
        else
            {
            state = "Dormant"
            }
        }
    setButtonState(btn, state) ;
    }


// ----------------------------------------------------------------
// Slider/dial input functions
// ----------------------------------------------------------------
function loadNumericSlider()
    {
    logDebug("loadNumericSlider: ");
    return partial(initNumericSlider) ;
    }

// Initialize a Numeric Slider to pending state
function initNumericSlider(elm)
    {
    logDebug("initNumericSlider: ", elm, ", id: ", elm.getAttribute("id") ) ;
    elm.source    = getEndPointSource(elm);
    setPoller(requestNumericSliderState, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestNumericSliderState(elm)
    {
    logDebug("requestNumericSliderState: ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, 4.8) ;
        def.addBoth(updateNumericSliderStatus, elm) ;
        }
    else
        {
        // No source:  just reflect button state selected
        //setButtonState(btn, btn.request) ;
        }
    return ;
    }

// Receive response to button status query
// The asynchronous callback supplies the HTTP request object
function updateNumericSliderStatus(elm, req)
    {
    try
        {
        sts = getWbStatusInt(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatusInt: ", e) ;
        }
    logDebug("updateNumericSliderStatus(callback): elm: ", elm, 
             ", req: ", req, ", sts: ", sts[2]) ;
    if ( sts != null )
        {
        try
            {
            logDebug("updateNumericSliderStatus", sts[2]) ;
            var sl = w$(elm)
            logDebug("updateNumericSliderStatus set", sl) ;
            sl.setValue( sts[2] )
            logDebug("updateNumericSliderStatus exit", sts[2]) ;
            }
        catch( e )
            {
            logError("updateNumericSliderStatus: ", e) ;
            }
        }
    return req ;    // Return request to next in callback chain
    }

