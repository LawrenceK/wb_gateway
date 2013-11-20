// $Id: was_WebBrick.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript library to support WebBrick control panel interaction widgets

// ----------------------------------------------------------------
// General functions
// ----------------------------------------------------------------

// Apply a supplied function to every named element in a DOM tree or subtree
// Valis, if supplied, is a list of values that are supplied successively to 
// the dom elements walked.
function domWalk(domref,func,elemname,vals)
    {
    logDebug( "domWalk: ", domref, ", ", elemname, ", ", vals) ;
    if (elemname == null ) elemname = "*"
    var elems = domref.getElementsByTagName(elemname) ;
    for (var i = 0 ; i < elems.length ; i++)
        {
        if ( vals )
            {
            func(elems[i],i,vals) ;
            }
        else
            {
            func(elems[i],i) ;
            }
        
        }
    }

// Scan all DOM elements for wbLoad attributes, and call the indicated 
// function for each such element, supplying the element object as an
// argument.  This allows each element to perform its own onload 
// initialization, independently of all the other elements on a panel.
function InitPanelElements(window)
    {
    try
        {
        initPoller( 10.0 ) ;    // Init poller with 10 second interval
        domWalk(document,InitPanelElement) ;
        pollNow() ;             // Start poller now
        }
    catch( e )
        {
        logError("InitPanelElements: ", e) ;
        }
    }

function InitPanelElement(elm)
    {
    var fname = elm.getAttribute("wbLoad") ;
    if ( fname )
        {
        // Assume that 'eval' content executes in current function context
        // hence 'elm' accesses the argument to this function.
        // alert("InitPanelElement: "+fname) ;
        eval( fname+"(elm)" ) ;
        }
    }

// Return an source endpoint locator value (HGA query path), or null
function getEndPointSource(elem,attrname)
    {
    e = getEndPoint(elem,"WbSource","/webbrick/status?wbaddr=","&wbchan=","") ;
    if (e) { return e ; }
    e = getEndPoint(elem,"iTSource","/itunes/status?idaddr=","&itchan=","") ;
    return e ;
    }

// Return an target endpoint command URI, or null
// (value for sending to target must be appended)
function getEndPointTarget(elem,attrname)
    {
    e = getEndPoint(elem,"WbTarget","/webbrick/command?wbaddr=","&wbchan=","&wbval=") ;
    if (e) { return e ; }
    e = getEndPoint(elem,"iTTarget","/itunes/command?idaddr=","&itchan=","&wbval=") ;
    return e ;
    }

// Return endpoint locator URI, or null
// Helper function for getEndPointSource and getEndPointTarget
// p1 = uri path before adress
// p2 = uri path after address, before channel
// p3 = uri path after channel
function getEndPoint(elem,attrname,p1,p2,p3)
    {
    var attr = elem.getAttribute(attrname) ;
    var path = null ;
    if ( attr )
        {
        var i = attr.lastIndexOf(":") ;
        if ( i >= 0 )
            {
            var addr  = attr.slice(0,i) ;
            var chan  = attr.slice(i+1) ;
            path = p1+addr+p2+chan+p3
            }
        }
    return path ;
    }

// Function behaves a bit like 'doSimpleXMLHttpRequest', except that it 
// takes a timeout (seconds) argument and completes the request with a 
// CancelledError condition if the HTTP operation does not complete 
// within the specified time interval
function doTimedXMLHttpRequest(uripath, timeout)
    {
    logDebug("doTimedXMLHttpRequest: ", uripath, ", timeout: ", timeout) ;
    return addTimeout(doSimpleXMLHttpRequest(uripath), timeout) ;
    }

// Accepts a deferred value, and returns a deferred that behaves
// just like the original except that it is cancelled if it fails
// to complete in the specified number of seconds.
function addTimeout(deferred, timeout)
    {
    logDebug("addTimeout: ", timeout) ;
    // Define local canceller function, bound to deferred
    var canceller = callLater(timeout,
        function ()
            {
            // Cancel the deferred after timeout seconds
            logDebug("** Timeout") ;
            deferred.cancel() ;
            } ) ;
    deferred.addBoth(
        function (res) 
            {
            // If the deferred fires, cancel the timeout
            logDebug("** Cancel timeout") ;
            canceller.cancel() ;
            return res;
            } ) ;
    return deferred
    }

// Function to extract status value as string from asynchronously
// completed HTTP request.  
// Returns a triple of address, channel and value string.
//
// Response template:
// <wbStatus wbAddr="${wbAddr}" wbChan="${wbChan}">${stsval}</wbStatus>
//
function getWbStatus(req)
    {
    logDebug("getWbStatus: ", req) ;
    var response = null ;    
    try
        {
        response = req.responseXML.documentElement ;
        }
    catch(e)
        {
        logWarning( "getWbStatus: no WebBrick status: ", e) ;
        }
    if ( response != null )
        {
        var sts = [null,null,null] ;
        sts[0] = response.getAttribute("wbAddr") ;
        logDebug("getWbStatus: sts[0]: ", sts[0]) ;
        sts[1] = response.getAttribute("wbChan") ;
        logDebug("getWbStatus: sts[1]: ", sts[1]) ;
        var n  = getFirstChildElem(response)
        sts[2] = getElementText(n) ;
        logDebug("getWbStatus: n: ", n, ", sts[2]: ", sts[2]) ;
        if ( n != null )
            {
            if (n.nodeName == "val")
                {           
                logDebug("getWbStatus: addr", sts[0], ", chan: ", sts[1], ", val: ", sts[2]) ;
                return sts ;
                }
            logDebug("getWbStatus: addr", sts[0], ", chan: ", sts[1], ", err: ", sts[2]) ;
            }
        }
    logDebug("getWbStatus (null return)") ;
    return null ;
    }

// Function to extract status value as integer from asynchronously
// completed HTTP request.  
// Returns a triple of address, channel and value.
function getWbStatusInt(req)
    {
    logDebug("getWbStatusInt: ", req) ;
    var sts = getWbStatus(req) ;
    if ( sts != null )
        {
        var pat = /^\d+$/ ;         // digit digit*
        if ( pat.test(sts[2]) )
            {
            sts[2] = sts[2] - 0 ;   // Force to numeric
            return sts ;
            }
        }
    return null ;
    }

// Function to extract status value as a real number from 
// an asynchronously completed HTTP request.  
// Returns a triple of address, channel and value.
function getWbStatusReal(req)
    {
    logDebug("getWbStatusReal: ", req) ;
    var sts = getWbStatus(req) ;
    if ( sts != null )
        {
        var pat = /^\d+(.\d*)?$/ ;  // digit digit* [ "." digit* ]
        if ( pat.test(sts[2]) )
            {
            sts[2] = sts[2] - 0 ;   // Force to numeric
            return sts ;
            }
        }
    return null ;
    }

// Function to extract Boolean status value as integer from asynchronously
// completed HTTP request.  
// Returns a triple of address, channel and value.
// For False, return 0, for True, return 1.
function getWbStatusBool(req)
    {
    logDebug("getWbStatusBool: ", req) ;
    var sts = getWbStatus(req) ;
    if ( sts != null )
        {
        switch (sts[2])
            {
            case "False":   sts[2] = 0 ;    break ;
            case "True":    sts[2] = 1 ;    break ;
            default:                        return null ;
            }
        return sts ;
        }
    return null ;
    }

// Find the first child element of a node (i.e. skip any text nodes)
function getFirstChildElem(elem)
    {
    logDebug("getFirstChildElem: ", elem.nodeName, ", len: ", elem.childNodes.length) ;
    for ( var i = 0 ; i < elem.childNodes.length ; i++ )
        {
        var n = elem.childNodes[i] ;
        if (n.nodeType == 1) return n ;
        }
    return null ;
    }

// Extract all child text from DOM element node
function getElementText(elem)
    {
    if ( elem == null ) return "" ;
    logDebug("getElementText: ", elem.childNodes) ;
    var txt = "" ;
    for ( var i = 0 ; i < elem.childNodes.length ; i++ )
        {
        if ( elem.childNodes[i].nodeType == 3 )
            {
            txt += elem.childNodes[i].nodeValue ;
            }
        }
    return txt ;
    }

// Set text value in DOM element node:  
// Replaces all children of the node with just one containing the supplied text.
function setElementText(elem, text)
    {
    logDebug("setElementText: ", elem, ", ", text) ;
    replaceChildNodes(elem,text) ;
    return elem ;
    }


// ----------------------------------------------------------------
// Panel functions

// Change the background theme for the current document
function changeBackground(theme)
    {
    document.body.className = theme ;
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
// Analog value display functions
// ----------------------------------------------------------------

// Initial load of a caption object
function loadNumericDisplay(pref, patt, post)
    {
    logDebug("loadNumericDisplay") ;
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
        logError("requestNumericState (nop source)") ;
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
             ", req: ", req, ", label: ", elm.label, ", sts: ", sts) ;
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
function loadButton()
    {
    logDebug("loadButton") ;
    return initButton ;
    }

// Initialize a button to pending state
function initButton(btn)
    {
    logDebug("initButton: ", btn) ;
    // TODO: pick up mapval labels from the HTML file
    // (cf. push button selector object)
    btn.mapval  = ["Off", "On"] ;
    btn.request = "Dormant"
    btn.source  = getEndPointSource(btn,"wbSource") ;
    btn.target  = getEndPointTarget(btn,"wbTarget") ;
    btn.onclick = clickButton ;
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
    var setval = "0" ;
    switch (btn.request)
        {
        case "Off":     btn.request = "On" ;    setval = "F" ;  break ;
        case "On":      btn.request = "Off" ;   setval = "N" ;  break ;
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
    btn.onclick   = clickPushSelectBtn ;
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
        var def = doTimedXMLHttpRequest(this.target+this.targetVal, 5.2) ;
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



// ------------------------------------------------
// Framework for refreshing displayed values
// ------------------------------------------------

// This framework uses the simple publish-subscribe event framework to periodically
// request a new value to be displayed.  Further, it allows an explicit request
// to be used to immediately refresh the displayed value, rather than waiting for 
// the next polling interval to come around.
//
// To use this framework:
// (a) call initPoller once when a panel is first initialized
// (b) when all initialization code is complete, call pollNow to start the poller.
// (c) for each item whose display requires periodic updating, create an event
//     handler for performing the update.  The event handler should require no
//     additional parameters.
// (d) in the item's initialization phase, call the setPoller function to
//     establish that the refresh function will be called periodically, or
//     more frequently if other events so dictate.
// (e) [optional] when the item is no longer required to be updated, call
//     cancellPoller to stop the periodic updates.  Normally, this would be
//     when the panel is being removed, so should be unnecessary.

function initPoller(interval)
    {
    pollerEvent    = new Event( "PollerEvent", this, { interval: interval } ) ;
    pollerDeferred = null ;
    //// return pollNow(this) ; // let caller do this
    }

// This function is intenbded to be used as a deferred callback function:  
// it's supplied argument is returned for the next callback in the chain.
// The supplied request object is also used as the event source value.
function pollNow(req)
    {
    //// logDebug("pollNow: event:", pollerEvent, ", req: ", req) ;
    // Cancel any outstanding timer, ignore any errors
    try
        { 
        pollerDeferred.cancel() ;
        }
    catch(e)
        {
        logDebug("Cancelled timer: ", e) ;
        }
    // Start new timer
    pollerDeferred = callLater(pollerEvent.interval, pollNow) ;
    // Invoke any listeners
    trigger(pollerEvent, req) ;
    // Note: new timer is started before event is triggered, so that further immediate
    // pollNow calls from the event trigger don't leave multiple timers outstanding.
    return req ;    // Return request to next in callback chain
    }

function setPoller(func)
    {
    logDebug("setPoller") ;
    if (arguments.length > 1)
        {
        // Partial application of func to remaining arguments:
        func = MochiKit.Base.partial.apply(null, arguments) ;
        }
    handle = subscribe("PollerEvent", partial(callPoller, func)) ;
    return handle ;
    }

function callPoller(func, handle, event, source)
    {
    logDebug("callPoller") ;
    func() ;
    }

function cancelPoller(handle)
    {
    logDebug("cancelPoller") ;
    unsubscribe(handle, "PollerEvent") ;
    }


// ------------------------------------------------
// Simple publish-subscribe framework for events
// ------------------------------------------------

// Event propagation allows any number of event targets to subscribe to be notified
// when any component triggers an event of a specified type.
//
// The basic operations provided are:
//   handle = subscribe(eventType, target) ;
//   unsubscribe(handle, eventType) ;
//   trigger(event, source) ;
//
// 'target' is a function that is called when an event is triggered, with three arguments:
//   - the event subscription handle for which the target is being activated
//   - an instance of the event type
//   - the source that triggered this event
//
// 'handle' is an opaque value, used to cancel a particular subscription.
//
// 'source' is a string that can be used to locate or identify the event source.
// In principle, 'source' is a URI, but this framework does nothing to enforce that.
//
// An event has a type, a source and some other unspecified values based on its type.
//

EventSubscriberList = [] ;        // An array of event subscriptions

function subscribe(eventType, target)
    {
    logDebug("subscribe: ", eventType) ;
    h = getNewHandle(EventSubscriberList) ;
    enrollSubscription(EventSubscriberList, h, eventType, target) ;
    return h ;
    }

function unsubscribe(handle, eventType)
    {
    logDebug("unsubscribe: ", handle, ", ", eventType) ;
    cancelSubscription(EventSubscriberList, handle, eventType) ;
    }

function trigger(event, source)
    {
    //// logDebug("trigger: ", event) ;
    publishEvent(EventSubscriberList, event, source)
    }


// Internal publish-subscribe helper functions
function getNewHandle(sublist)
    {
    for ( var i = 0 ; i < sublist.length ; i++ )
        {
        if ( sublist[i] == null ) return i ;
        }
    return sublist.length ;
    }

function enrollSubscription(sublist, handle, eventType, target)
    {
    logDebug("enrollSubscription: ", eventType) ;
    sublist[handle] = {eventType:eventType, target:target} ;
    }

function cancelSubscription(sublist, handle, eventType)
    {
    logDebug("cancelSubscription: ", eventType) ;
    if ( sublist[handle].eventType == eventType )
        {
        sublist[handle] = null ;
        }
    else
        {
        throw new EventError( this, "cancelSubscription event type mismatch" ) ;
        }
    }

function publishEvent(sublist, event, source)
    {
    //// logDebug("publishEvent: ", event.eventType) ;
    for ( var h = 0 ; h < sublist.length ; h++ )
        {
        if ( sublist[h].eventType == event.eventType )
            {
            sublist[h].target(h, event, source) ;
            }
        }
    }

// Construct a new event
// Specifies a type value, a source value and an object with additional values
// that are added to the event object.
function Event(type, source, obj)
    {
    this.eventType   = type ;
    this.eventSource = source ;
    for (var key in obj)
        {
        this[key] = obj[key] ;
        }
    return this ;
    }

// TODO: figure out how to create a hierarchy of event values.  
// Javascript prototype-based inheritance is pretty confusing.

// Define EventError constructor/class...
// This is an event object with a message value
// TODO: refine as we better understand Javascript classes.
function EventError( source, msg )
    {
    return Event( "EventError", source, { message : msg } ) ;
    }
