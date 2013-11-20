// $Id: EditConfig.js 1406 2008-05-23 01:22:58Z webbrick $
//
// Javascript library to support WebBrick configuration editing form

// --------------------------------
// Helper functions
// --------------------------------

// Returns a function that swallows an argument and returns a constant value.
// Modelled on Haskell's 'const' function.
function constval(k)
    {
    return function(x) { return k ; }
    }

// Declare 'constnull' to avoid creating closures each time it is used
var constnull  = constval(null) ;

// Function returns a new object each time it is used
function constempty()
    {
    return new Object() ;
    }

// Return a fix-width text for an <Option> element (to ensure columns in a selector 
// can line up, regardless of left- or right-alignment of the containing <Select>.
// Spaces are converted to non-breaking spaces, which are in turn rendered as
// &nbsp; in the resulting XHTML document.
function mkFixedWidthOptionText(txt,width)
    {
    while ( txt.length < width ) txt = txt + " " ;
    return txt.replace(/ /g, "\u00a0") ;    // "\u00A0" is non-breaking space
    }

// Display a message

var curmsg = ""

function showMessage(msg)
    {
    curmsg = msg ;
    var msgelm = currentDocument().getElementById("Message") ;
    setNodeAttribute(msgelm, "class", "Message" ) ;
    if ( msgelm )
        {
        replaceChildNodes(msgelm, curmsg) ;
        }
    }

function appendMessage(msg)
    {
    curmsg = curmsg + " ; " + msg ;
    var msgelm = currentDocument().getElementById("Message") ;
    setNodeAttribute(msgelm, "class", "Message" ) ;
    if ( msgelm )
        {
        replaceChildNodes(msgelm, curmsg) ;
        }
    }

// Display an error
function showError(msg)
    {
    msgelm = currentDocument().getElementById("Message") ;
    setNodeAttribute(msgelm, "class", "Error" ) ;
    if ( msgelm )
        {
        replaceChildNodes(msgelm, "Error: "+msg) ;
        }
    }

// Callback function that can be used to clear message area
function clearMessage(req)
    {
    showMessage("") ;
    return req
    }

// Callback function that can be used to display a message
function showMessageCB(msg)
    {
    return function(req)
        {
        showMessage(msg) ;
        return req
        }
    }

// Callback function that can be used to append a message
function appendMessageCB(msg)
    {
    return function(req)
        {
        appendMessage(msg) ;
        return req
        }
    }

// Show or hide an element
// show is True to display the element, else False to hide it
function exposeElement(elm, show)
    {
    if (show)
        {
        showElement(elm) ;
        }
    else
        {
        hideElement(elm) ;
        }
    }

function showElement(elm)
    {
    elm.style.display = '' ;
    }

function hideElement(elm)
    {
    elm.style.display = 'none' ;
    }

// Show elements in the list that satisfy the supplied predicate,
// anbd hide the others
function exposeElements(elms, showp)
    {
    for (var i = 0; i < elms.length; i++)
        {
        logDebug("exposeElements", i, elms[i], getNodeAttribute(elms[i], "id")) ;
        exposeElement(elms[i], showp(elms[i])) ;
        }
    }

// Return a predicate that tests a named attribute of a supplied 
// element for equality with a supplied value.  Always returns
// false is the supplied value evaluates to false.
function attrEq(attrname,attrval)
    {
    return function (elm)
        {
        logDebug("attrEq", elm, attrname, attrval, getNodeAttribute(elm, attrname) ) ;
        return attrval && (getNodeAttribute(elm, attrname) == attrval) ;
        }
    }

// Return a predicate that tests the id of a supplied element 
// for equality with a supplied value
function idEq(testid)
    {
    return attrEq("id", testid) ;
    }

// Function to list properties of an object
function propertyNames(obj)
    {
    var ps = [] ;
    for (var p in obj)
        {
        ps.push(p) ;
        }
    return ps ;
    }

// --------------------------------
// Functions for specific controls
// --------------------------------

// --------------------------------
// Expose/hide callouts
// --------------------------------
//
// Functions to expose or hide the callout table sections as corresponding
// cells are clicked.

var CalloutList = [] ;

// loadNoCallout
// -------------
//
// Initialize element whose selection causes all callouts to be hidden

function loadNoCallout()
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("NoCallout") ) ;
        connect(elm, 'onclick', showCallout(null) ) ;
        } 
    }

// loadDOCallout
// -------------
//
// Display the callout for Digital Output n

function loadDOCallout(n)
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("DOCallout("+n+")") ) ;
        connect(elm, 'onclick', showCallout("DOCallout_"+n) ) ;
        } 
    }

// loadAOCallout
// -------------
//
// Display the callout for Analog Output n

function loadAOCallout(n)
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("AOCallout("+n+")") ) ;
        connect(elm, 'onclick', showCallout("AOCallout_"+n) ) ;
        } 
    }

// loadDICallout
// -------------
//
// Display the callout for Digital Input n

function loadDICallout(n)
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("DICallout("+n+")") ) ;
        connect(elm, 'onclick', showCallout("DICallout_"+n) ) ;
        } 
    }

// loadAICallout
// -------------
//
// Display the callout for Analog Input n

function loadAICallout(n)
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("AICallout("+n+")") ) ;
        connect(elm, 'onclick', showCallout("AICallout_"+n) ) ;
        } 
    }

// loadTICallout
// -------------
//
// Display the callout for Temperature Input n

function loadTICallout(n)
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("TICallout("+n+")") ) ;
        connect(elm, 'onclick', showCallout("TICallout_"+n) ) ;
        } 
    }

// loadSceneCallout
// -------------
//
// Display the callout for Scene n

function loadSceneCallout(n)
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("SceneCallout("+n+")") ) ;
        connect(elm, 'onclick', showCallout("SceneCallout_"+n) ) ;
        } 
    }

// loadScheduleCallout
// -------------
//
// Display the callout for Schedule n

function loadScheduleCallout(n)
    {
    return function (elm) 
        {
        // connect(elm, 'onclick', showMessageCB("ScheduleCallout("+n+")") ) ;
        connect(elm, 'onclick', showCallout("ScheduleCallout_"+n) ) ;
        } 
    }

// showCallout
// -----------
//
// Make a specified callout visible.  All others are hidden.
//
// 'cid' identified the callout to be made visible

function showCallout(cid)
    {
    return function (elm, evt)
        {
        logDebug("showCallout: ", cid) ;
        exposeElements(CalloutList, idEq(cid)) ;
        }
    }


// regsiterCallout
// ---------------
//
// Register an element as a callout.

function registerCallout()
    {
    return function (elm)
        {
        n = CalloutList.push(elm) ;
        hideElement(elm) ;
        }
    }



// --------------------------------
// xxxx
// --------------------------------

// xxxx
// ----------------

// xxxx
function xxx()
    { 
    }


// WbConfigNode
// ------------
//
// Hidden field with node number of currently selected configuration file

// Initial load
function loadWbzzzzzz()
    {
    return function (elm) 
        {
        // --- defer initialization to selector
        // --- initWbConfigNode(elm) ;
        } 
    }

// Reload
function reloadWbzzzzzz(req)
    {
    // logDebug("reloadWbzzzzzz:", req) ;
    var elm = currentDocument().getElementById("Wbzzzzzz") ;
    initWbzzzzzz(elm) ;
    }

// Initialization logic
function initWbzzzzzz(elm)
    {
    //var csel = currentDocument().getElementById("WbConfigs") ;
    //var node = "(None)" ;
    //var i    = csel.selectedIndex ;
    //if (i >= 0 && i < csel.length)
    //    {
    //    node = csel.options[i].getAttribute("node") ;
    //    }
    //elm.value = node ;
    }

// End.
