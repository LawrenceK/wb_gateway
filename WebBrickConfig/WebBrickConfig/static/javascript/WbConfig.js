// $Id: WbConfig.js 1410 2008-05-23 01:24:35Z webbrick $
//
// Javascript library to support WebBrick configuration panel

// --------------------------------
// Helper functions
// --------------------------------

// Callback to initialize the content of a <SELECT> element from the response
// to a doSimpleXMLHttpRequest.
//
// elm      is the <Select> element to be initialized
// soname   is the name of the elements in the XML response that provide the
//          <Option> values with which the selector is populated.
// soinit   is the value of the element that is to be initially selected, or null
//          if no initial selection is to be made.
// soattr   is a function that is used to extract an attribute dictionary from 
//          each element selected by soname.
// defattr  attributes to be used for empty list indicator option.
// soelem   is a function that is used to extract option content text from 
//          each element selected by soname.
// width    is a width to which the 
// req      is the doSimpleXMLHttpRequest request object whose response
//          is used to populate the selector.
//
// ----
//
// Initially, I preferred having the initSelector function to be local to the
// function initializing the selector element, but then realized the logic could
// be re-used for multiple selectors.  The following comments are my thoughts
// about the potential for memory leaks in the original design, which I'm keeping
// here for future reference.
//
// Having the initSelector function local to the element initialization callback
// risks exporting a closure via the Deferred object, which in turn can potentially 
// lead to memory leaks.  If this is the case, the function could be made global, 
// but must be given a name that is unique in the global scope.
//
// I think that if the closure is referenced by the deferred object, which itself 
// is discarded when all the references have been lost and the callbacks executed, 
// I think the memory will be recoverable once the selector initialization is done.
//
// (I don't know if the fact that function does not reference the containing 
// scope would be sufficient to avoid the leak.)
//
// There is some detailed explanation of javascript closures and memory usage
// at: [http://www.jibbering.com/faq/faq_notes/closures.html]
//
// It is said that constructing the DOM tree top-down reduces memory leaks
// cf. [http://msdn.microsoft.com/library/default.asp?url=/library/en-us/IETechCol/dnwebgen/ie_leak_patterns.asp]
// "Cross-page leaks".  According to this article, the problem does not exist of the
// dynamically created objects do not have event handler scripts attached.
// MochiKit's "replaceChildNodes" is assumed to take care of this.
//
function initSelectorExt(elm, soname, soinit, soattr, soelem, defattr, width, req)
    {
    //logDebug("initSelectorExt: ", elm, ", ", soname, ", ", /* soattr, ", ", sofunc, ", ", */ req) ;
    //logDebug("initSelectorExt: req.responseText ", req.responseText ) ;
    //logDebug("initSelectorExt: req.responseXML ", req.responseXML ) ;
    //logDebug("initSelectorExt: req.getAllResponseHeaders() ", req.getAllResponseHeaders() ) ;

    // Construct attributes for option element
    function mkattr(e)
        {
        var a = soattr(e)
        //a["test1"] = "True"
        //a["test2"] = soinit
        //a["test3"] = soelem(e)
        //a["test4"] = getElementText(e)
        if ( soinit && soinit == soelem(e) )
            {
            a["selected"] = "True"
            }
        return a
        }

    // Construct text for option content
    function mktext(e)
        {
        var t = soelem(e) ;
        if (width > 0) t = mkFixedWidthOptionText(t, width) ;
        return t ;
        }

    // Selector initialization main function
    var rsp = null ;
    var msg = null ;
    if ( req instanceof Error )
        {
        msg = "Server returned error: "+req ;
        }
    else
        {
        try
            {
            rsp = req.responseXML.documentElement ;
            }
        catch(e)
            {
            msg = "No XML document in server response"+e ;
            logWarning("initSelectorExt: "+msg) ;
            showError(msg) ;
            replaceChildNodes(elm, [OPTION(defattr, "-- (Error) --")]) ;
            throw e ;   // Ensure the deferred returns an error
            }
        }
    if ( rsp == null )
        {
        msg = "No server response (initSelectorExt): " ;
        }
    if ( msg != null )
        {
        logWarning("initSelectorExt: "+msg) ;
        showError(msg) ;
        replaceChildNodes(elm, [OPTION(defattr, "-- (Error) --")]) ;
        return null ;
        }
    var elms = rsp.getElementsByTagName(soname) ;
    var opts = map(OPTION, map(mkattr, elms), map(mktext, elms)) ;
    if (opts.length == 0)
        {
        // Ensure at least one entry in list
        opts[0] = OPTION( defattr, mkFixedWidthOptionText("-- (none) --",width) ) ;
        }
    replaceChildNodes(elm, opts) ;
    return elm ;
    }

// This is a common case version of initSelectorExt that uses the getElementText
// function to retrieve the textual content of each element selected, and provides
// no <Option> attribute values.
function initSelector(elm, soname, soinit, req)
    {
    return initSelectorExt(
        elm, soname, soinit, constempty, getElementText, {}, 0, req) ;
    }

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

// Return a fix-width text for an <Option> element (to ensure columns in a selactor 
// can line up, regardless of left- or right-alignment of the containing <Select>.
// Spaces are converted to non-breaking spaces, which are in turn rendered as
// &nbsp; in the resulting XHTML document.
function mkFixedWidthOptionText(txt,width)
    {
    while ( txt.length < width ) txt = txt + " " ;
    return txt.replace(/ /g, "\u00a0") ;    // "\u00A0" is non-breaking space
    }

// Display a message
function showMessage(msg)
    {
    msgelm = currentDocument().getElementById("Message") ;
    setNodeAttribute(msgelm, "class", "Message" ) ;
    if ( msgelm )
        {
        replaceChildNodes(msgelm, msg) ;
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
    showMessage(null) ;
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


// --------------------------------
// Active network WebBricks column
// --------------------------------

// loadWbIpNetworks
// ----------------

// Initialize input box with IP network address 'x.x.x.x/maskbits'
function loadWbIpNetworks(initnet)
    { 
    return function(elm) 
        {
        var d = doSimpleXMLHttpRequest("/wbcnf/Networks/") ;
        d.addBoth(initSelector, elm, "Network", initnet) ;
        d.addBoth(reloadActiveWebBricksSelector) ;
        connect(elm, 'onchange', showMessageCB("Performing WebBrick discovery ...")) ;
        connect(elm, 'onchange', reloadActiveWebBricksSelector) ;
        }
    }

// WbSelector
// ----------

// Load WebBrick selector
function loadActiveWebBricksSelector()
    {
    return function (elm) 
        {
        // logDebug("loadActiveWebBricksSelector (callback)", elm) ;
        // --- don't initialize on load: leave network selector to trigger init
        // --- initActiveWebBricksSelector(elm) ;
        connect(elm, 'onchange', reloadWbIpAddress) ;
        connect(elm, 'onchange', reloadWbNewIpAdrs) ;
        connect(elm, 'onchange', reloadWbMacAddress) ;
        } 
    }

// Reload list of active WebBricks: 
// event handler to initiate reload
function reloadActiveWebBricksSelector(req)
    {
    // logDebug("reloadActiveWebBricksSelector:", req) ;
    var wbs = currentDocument().getElementById("WbSelector") ;
    initActiveWebBricksSelector(wbs) ;
    }

// Initialize selector to display a list of active WebBricks
function initActiveWebBricksSelector(elm)
    {
    // logDebug("initActiveWebBricksSelector", elm) ;
    var ipnets = currentDocument().getElementById("WbIpNetworks") ;
    var net    = "10.0.0.0/8" ;    // Default network
    var i      = ipnets.selectedIndex ;
    if (i >= 0 && i < ipnets.length) net = getElementText(ipnets.options[i]) ;
    var opts = [ OPTION( {'class': "OptAttn", 'value': "waiting"}, 
                         "(Waiting for WebBrick list)") ] ;
    replaceChildNodes(elm, opts) ;
    var d   = doSimpleXMLHttpRequest("/wbcnf/Discover/"+net) ;
    d.addBoth(clearMessage) ;
    d.addBoth(initSelectorExt, elm, "WebBrick", null, 
        mkWebBrickOptionAttr, mkWebBrickOptionText,
        { 'class': 'OptNull' }, 36) ;
    d.addBoth(reloadNodeList) ;
    d.addBoth(reloadWbIpAddress) ;
    d.addBoth(reloadWbNewIpAdrs) ;
    d.addBoth(reloadWbMacAddress) ;
    }

function mkWebBrickOptionText(elm)
    {
    // return getElementText(elm) ;
    var m = elm.getAttribute("mac") ;
    var v = elm.getAttribute("node") ;
    var n = elm.getAttribute("name") ;
    while (v.length < 3) v = "0"+v ;
    return m+"  "+v+"  "+n
    }

function mkWebBrickOptionAttr(elm)
    {
    var v = elm.getAttribute("node") ;
    var c = ( elm.getAttribute("attn") == "Yes" ? "OptAttn" : "OptNorm" ) ;
    var n = elm.getAttribute("name") ;
    var a = elm.getAttribute("adrs") ;
    var m = elm.getAttribute("mac") ;
    return { "class": c, "value" : v, "name": n, "adrs": a, "mac": m } ;
    }

// WbNodeList
// ----------

// A hidden field containing a list of node numbers and IP addresses from WbSelector
// The server may use this when performing a save-all operation.

function reloadNodeList(evt)
    {
    // logDebug("reloadNodeList:", evt) ;
    var nls = currentDocument().getElementById("WbNodeList") ;
    initNodeList(nls) ;
    }

function initNodeList(elm)
    {
    var wbs = currentDocument().getElementById("WbSelector") ;
    ns = ""
    for ( var i = 0 ; i < wbs.length ; i++ )
        {
        ns += wbs.options[i].getAttribute("value") + "," ;
        ns += wbs.options[i].getAttribute("adrs")  + ";" ;
        // ns += getElementText(wbs.options[i])       + "\n" ;
        }
    elm.value = ns ;
    }


// WbPassword
// -----------

// Currently, no active value.  Initialized in HTML to default value.
function loadWbPassword()
    {
    return function (elm) 
        {
        } 
    }


// WbIpAddress
// -----------

// Initialize hidden field with IP address of currently selected WebBrick
function loadWbIpAddress()
    {
    return function (elm) 
        {
        // --- defer initialization to selector
        // --- initWbIpAddress(elm) ;
        } 
    }

// Reload current WebBrick IP address
function reloadWbIpAddress(req)
    {
    // logDebug("reloadWbIpAddress:", req) ;
    var elm = currentDocument().getElementById("WbIpAddress") ;
    initWbIpAddress(elm) ;
    }

// Initialize input box with IP address of currently selected WebBrick
function initWbIpAddress(elm)
    {
    var wbs = currentDocument().getElementById("WbSelector") ;
    var adr = "(None)" ;
    var i   = wbs.selectedIndex ;
    if (i >= 0 && i < wbs.length) adr = wbs.options[i].getAttribute("adrs") ;
    elm.value = adr ;
    }


// WbNewIpAdrs
// -----------

// Initialize input box with IP address of currently selected WebBrick
function loadWbNewIpAdrs()
    {
    return function (elm) 
        {
        // --- defer initialization to selector
        // --- initWbNewIpAdrs(elm) ;
        } 
    }

// Reload current WebBrick IP address
function reloadWbNewIpAdrs(req)
    {
    // logDebug("reloadWbIpAddress:", req) ;
    var elm = currentDocument().getElementById("WbNewIpAdrs") ;
    initWbNewIpAdrs(elm) ;
    }

// Initialize input box with IP address of currently selected WebBrick
function initWbNewIpAdrs(elm)
    {
    var wbs = currentDocument().getElementById("WbSelector") ;
    var adr = "(None)" ;
    var i   = wbs.selectedIndex ;
    if (i >= 0 && i < wbs.length) adr = wbs.options[i].getAttribute("adrs") ;
    elm.value = adr ;
    }


// WbMacAddress
// -----------

// Initialize input box with Mac address of currently selected WebBrick
function loadWbMacAddress()
    {
    return function (elm) 
        {
        // --- defer initialization to selector
        // --- initWbMacAddress(elm) ;
        } 
    }

// Reload current WebBrick MAC address
function reloadWbMacAddress(req)
    {
    // logDebug("reloadWbMacAddress:", req) ;
    var elm = currentDocument().getElementById("WbMacAddress") ;
    initWbMacAddress(elm) ;
    }

// Initialize input box with Mac address of currently selected WebBrick
function initWbMacAddress(elm)
    {
    var wbs = currentDocument().getElementById("WbSelector") ;
    var mac = "(None)" ;
    var i   = wbs.selectedIndex ;
    if (i >= 0 && i < wbs.length) mac = wbs.options[i].getAttribute("mac") ;
    elm.value = mac ;
    }


// ----------buttons -------------

// Initialize button to update IP address of selected WebBrick
function loadWbUpdateIpButton()
    {
    return function (elm) 
        {
        connect(elm, 'onclick', showMessageCB("Updaing WebBrick IP address ...") ) ;
        } 
    }

// Initialize button to discover active Webbricks on network
function loadWbDiscoverButton()
    {
    return function (elm) 
        {
        connect(elm, 'onclick', showMessageCB("Performing WebBrick discovery ...") ) ;
        } 
    }

// Initialize button to remove Webbrick from list of active WebBricks
function loadWbRemoveButton()
    {
    // logDebug("loadWbRemoveButton") ;
    return function (elm)
        {
        // logDebug("loadWbRemoveButton (callback): ", elm) ;
        connect(elm, 'onclick', removeWebBrickSelection) ;
        } 
    }

// Callback function to remove currently selected WebBrick from list
function removeWebBrickSelection(evt)
    {
    // logDebug("removeWebBrickSelection:", evt) ;
    showMessage("Removing WebBrick ...")
    }

// Initialize button to add Webbrick to list of active WebBricks
function loadWbAddButton()
    {
    // logDebug("loadWbAddButton") ;
    return function (elm)
        {
        // logDebug("loadWbRemoveButton (callback): ", elm) ;
        connect(elm, 'onclick', addWebBrick) ;
        } 
    }

// Callback function to add currently WebBrick to list
function addWebBrick(evt)
    {
    // logDebug("removeWebBrickSelection:", evt) ;
    showMessage("Adding WebBrick ...")
    }

// --------------------------------
// Load/save column
// --------------------------------

// Initialize button to load selected configuration to selected webBrick
function loadLoadButton()
    {
    return function (elm) 
        {
        connect(elm, 'onclick', showMessageCB("Loading configuration to WebBrick ...") ) ;
        } 
    }

// Initialize button to save configuration from selected WebBrick
function loadSaveButton()
    {
    return function (elm) 
        {
        connect(elm, 'onclick', showMessageCB("Saving WebBrick configuration ...") ) ;
        } 
    }

// Initialize button to save configurations from all WebBricks
function loadSaveAllButton()
    {
    return function (elm) 
        {
        connect(elm, 'onclick', showMessageCB("Saving configuration for all listed WebBricks ...") ) ;
        } 
    }

// --------------------------------
// Configuration sets column
// --------------------------------

// WbConfigSets
// ------------

// Initialize configuration set selector
function loadConfigSetSelector(initset)
    {
    return function (elm) 
        {
        // logDebug("loadConfigSetSelector (callback)", elm) ;
        var d = doSimpleXMLHttpRequest("/wbcnf/Config/") ;
        d.addBoth(initSelector, elm, "ConfigSet", initset) ;
        d.addBoth(reloadWebBrickConfigurationSelector) ;
        connect(elm, 'onchange', reloadWebBrickConfigurationSelector) ;
        } 
    }

// Buttons
// -------

/*
// Initialize button to create a new configuration set on the server
function loadConfigSetNewButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to delete a configuration set from the server
function loadConfigSetDeleteButton()
    {
    return function (elm) 
        {
        } 
    }
*/

// WbConfigs
// ---------

// Initialize selector to display a list of WebBrick configurations from
// the currently selected Configuration Set
function loadWebBrickConfigurationSelector()
    {
    return function (elm) 
        {
        // logDebug("loadActiveWebBricksSelector (callback)", elm) ;
        // ---
        // --- try not initializing this on load: wait for confoig selector
        //     to be initialized
        // --- initWebBrickConfigurationSelector(elm) ;
        // ---
        connect(elm, 'onchange', reloadWbConfigNode) ;
        connect(elm, 'onchange', reloadWbConfigName) ;
        } 
    }

function reloadWebBrickConfigurationSelector(req)
    {
    // logDebug("reloadWebBrickConfigurationSelector", req) ;
    var elm = currentDocument().getElementById("WbConfigs") ;
    initWebBrickConfigurationSelector(elm) ;
    }

// Initialize selector to display a list of available WebBrick configurations
function initWebBrickConfigurationSelector(elm)
    {
    // logDebug("initWebBrickConfigurationSelector", elm) ;
    var cfs = currentDocument().getElementById("WbConfigSets") ;
    var net = "" ;       // Default config set
    var i   = cfs.selectedIndex ;
    if (i >= 0 && i < cfs.length) cfg = getElementText(cfs.options[i]) ;
    var d   = doSimpleXMLHttpRequest("/wbcnf/Config/"+cfg) ;
    d.addBoth(initSelectorExt, elm, "Config", null, 
        mkWebBrickConfigAttr, mkWebBrickConfigText, 
        { 'class': 'OptNull' }, 25) ;
    d.addBoth(reloadWbConfigNode)
    d.addBoth(reloadWbConfigName)
    }

function mkWebBrickConfigAttr(elm)
    {
    var n = elm.getAttribute("node") ;
    var t = elm.getAttribute("name") ;
    return { "node" : n, "name":t, "class": "OptNorm"} ;
    }

function mkWebBrickConfigText(elm)
    {
    var t = elm.getAttribute("node") + "  " + elm.getAttribute("name") ;
    return mkFixedWidthOptionText(t, 25) ;
    }


// WbConfigNode
// ------------
//
// Hidden field with node number of currently selected configuration file

// Initial load
function loadWbConfigNode()
    {
    return function (elm) 
        {
        // --- defer initialization to selector
        // --- initWbConfigNode(elm) ;
        } 
    }

// Reload
function reloadWbConfigNode(req)
    {
    // logDebug("reloadWebBrickConfigNum:", req) ;
    var elm = currentDocument().getElementById("WbConfigNode") ;
    initWbConfigNode(elm) ;
    }

// Initialization logic
function initWbConfigNode(elm)
    {
    var csel = currentDocument().getElementById("WbConfigs") ;
    var node = "(None)" ;
    var i    = csel.selectedIndex ;
    if (i >= 0 && i < csel.length)
        {
        node = csel.options[i].getAttribute("node") ;
        }
    elm.value = node ;
    }


// WbConfigName
// ------------
//
// Hidden field with node name of currently selected configuration file

// Initial load
function loadWbConfigName()
    {
    return function (elm) 
        {
        // --- defer initialization to selector
        // --- initWbConfigName(elm) ;
        } 
    }

// Reload
function reloadWbConfigName(req)
    {
    var elm = currentDocument().getElementById("WbConfigName") ;
    initWbConfigName(elm) ;
    }

// Initialization logic
function initWbConfigName(elm)
    {
    var csel = currentDocument().getElementById("WbConfigs") ;
    var name = "(None)" ;
    var i    = csel.selectedIndex ;
    if (i >= 0 && i < csel.length)
        {
        name = csel.options[i].getAttribute("name") ;
        }
    elm.value = name ;
    }


// Buttons
// -------

/*
// Initialize button to create new webbrick configuration in the current set
function loadWbNewButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to show the selected webbrick configuration
function loadWbShowButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to edit the selected webbrick configuration
function loadWbEditButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to delete the selected webbrick configuration
function loadWbDeleteButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to copy selected configuration to another Configuration Set
function loadWbCopyButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to move selected configuration to another Configuration Set
function loadWbMoveButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to upload new configuration to the current Configuration Set
function loadWbUploadButton()
    {
    return function (elm) 
        {
        } 
    }

// Initialize button to download the selected configuration
function loadWbDownloadButton()
    {
    return function (elm) 
        {
        } 
    }
*/

// End.
