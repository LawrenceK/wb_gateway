// $Id: WbPushSelect.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for push slect widget.

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
    sel.source  = getEndPointSource(sel) ;
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
    btn.target    = getEndPointTarget(btn) ;
    btn.targetVal = vals[0][i] ;
    if ( btn.target )
    {
        connect(btn, "onclick", clickPushSelectBtn ); 
    }
    logDebug("initPushSelectBtn: [", i, "], ", btn, 
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
//        var def = doTimedXMLHttpRequest(this.target+this.targetVal, pollerTimeout) ;
        var def = doTimedXMLHttpRequest(this.target, pollerTimeout) ;
        def.addBoth(pollSoon) ;
//        def.addBoth(pollNow) ;
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
        var def = doTimedXMLHttpRequest(sel.source, pollerTimeout) ;
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
        sts = getWbStatusBoolInteger(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatusBoolInteger: ", e) ;
        }
    logDebug("updateSelectorStatus (callback): sel: ", sel, 
             ", req: ", req, ", sts: ", sts) ;
    if ( sts != null )
        {
        // This allows wbSource to be a numeric value.
        if ( (sts[2] < 0 ) || (sts[2] > btn.mapval.length) )
            {
            // if index greater than length of state names thenuse last.
            state = btn.getAttribute("overValueState");
            if (!state)
                {
                state = btn.mapval[btn.mapval.length];
                }
            }
        else
            {
            state = btn.mapval[sts[2]];
            }
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
    // logDebug("showPushSelectBtn: ", btn, ", ", btn.selectVal, ", ", state) ;
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


