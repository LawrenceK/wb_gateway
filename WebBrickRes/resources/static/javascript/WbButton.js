// $Id: WbButton.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for button input
// Also manages indicator display as target may be null.


// ----------------------------------------------------------------
// Button functions
// ----------------------------------------------------------------

// Initial load of a button object
// If 'toggle' is not True, the button does not attempt to toggle its state,
// and remains dormant unless the specified source value reads as true.
function loadButton(toggle)
    {
    return loadPushButton(toggle);
    }

function loadPushButton(toggle)
    {
    logDebug("loadPushButton: ", toggle) ;
    if (!toggle) toggle = false ;
    return partial(initButton, "button", toggle);
    }

function loadIndicator(toggle)
    {
    logDebug("loadPushButton: ", toggle) ;
    if (!toggle) toggle = false ;
    return partial(initButton, "indicator", toggle);
    }

// Initialize a button to pending state
function initButton(baseClassName, toggle, btn)
    {
    logDebug("initButton: ", btn) ;
    btn.mapval  = ["Off", "On"] ;
    
    // pick up mapval labels from the HTML file
    // (cf. push button selector object)
    var attr = btn.getAttribute("stateVals") ;
    if (attr)
    {
        // comma separated list of values.
        var v = attr.split(",");
        if  (v.length >= 2)
        {
            btn.mapval  = v;
        }
    }
   
    getWidgetBaseClass(btn,baseClassName);
    btn.toggle  = toggle ;
    btn.request = "Dormant"
    btn.source  = getEndPointSource(btn) ;
    btn.target  = getEndPointTarget(btn) ;
    btn.pagelink  = null;
    attr = btn.getAttribute("wbPageLink") ;
    if (attr)
        {
        btn.pagelink = attr;
        }
    if (btn.target)
    {
        connect(btn, "onclick", clickButton ); 
    }
    if (btn.source)
    {
        setWidgetState(btn, "Pending") ;
        setPoller(requestButtonState, btn) ;
    }
    else
    {
        setWidgetState(btn, "Dormant");
    }
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
        setWidgetState(btn, "Pending") ;
        var def = doTimedXMLHttpRequest(btn.target+setval, pollerTimeout) ;
        if ( btn.pagelink )
            {
            def.addBoth(changePage, btn);
            }
        else
            {
            def.addBoth(pollSoon) ;
            if ( !btn.source )
                {
                callLater(1.0, resetButtonState, btn );
                }
            }
        }
    else
        {
        logError("clickButton (no target)") ;
        }
    return false ;      // Suppresss any default onClick action
    }

function changePage(btn)
    {
    if ( btn.pagelink )
        {
        window.location=btn.pagelink;
        }
    }

function resetButtonState(btn)
{
    setWidgetState(btn, "Dormant") ;
}

// Polling callback function, 
// Request and eventually display the status of a button,
function requestButtonState(btn)
    {
    logDebug("requestButtonState: ", btn.request, ", ", btn.source) ;
    // Not called if no wbSource, so irrelevant test
    if ( btn.source )
        {
        var def = doTimedXMLHttpRequest(btn.source, pollerTimeout) ;
        def.addBoth(updateButtonStatus, btn) ;
        }
    else
        {
        // No source:  just reflect button state selected
        setWidgetState(btn, btn.request) ;
        }
    return ;
    }

// Receive response to button status query
// The asynchronous callback supplies the HTTP request object
function updateButtonStatus(btn, req)
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
    logDebug("updateButtonStatus (callback): btn: ", btn, 
             ", req: ", req, ", sts: ", sts) ;
    if ( sts != null )
        {
        // Use numeric status value as index to get state name
        // This allows wbSource to be a numeric value.
        if ( (sts[2] < 0 ) || (sts[2] > btn.mapval.length) )
            {
            // if index greater than length of state names then use last.
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
        state = "Absent";
        }
    setWidgetState(btn, state) ;
    return req ;    // Return request to next in callback chain
    }
