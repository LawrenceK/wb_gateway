// $Id: WbGwConfig.js 1455 2008-05-23 01:34:46Z webbrick $
//
// Javascript library to support Gateway configuration panel
// 
// Authors: Andy Harris 
//          Philipp Schuster 
//
// Note:    Derived from Graham Klyne's work on the WebBrick configurator
//
//

// ************************************************************************************
//      Helper functions
// ************************************************************************************

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
        msg = "No server response" ;
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

function mkConfigAttr(elm)
    {
    var n = elm.getAttribute("id") ;
    var t = elm.getAttribute("name") ;
    return { "id" : n, "name":t, "class": "OptNorm"} ;
    }

function mkConfigText(elm)
    {
    var t = elm.getAttribute("id") + "  " + elm.getAttribute("name") ;
    return mkFixedWidthOptionText(t, 25) ;
    }



// ************************************************************************************
//      Main Functions that directly interact with pages
// ************************************************************************************

function initKnownDevicesSelector(elm)
    {
    logDebug("initKnownDevicesSelector", elm) ;
    var d   = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/KnownDevices") ;
    d.addBoth(initSelectorExt, elm, "item", null, 
        mkConfigAttr, mkConfigText, 
        { 'class': 'OptNull' }, 25) ;
    }

// ********************************************************
//  This has an optional parameter to set onchange handler
//  ******************************************************
function loadKnownDevicesSelector(reqOnChange)
    {
    return function (elm) 
        {
        logDebug("loadKnownDevicesSelector (callback)", elm) ;
        initKnownDevicesSelector(elm) ;
        if (reqOnChange != undefined)
            {
            connect(elm, 'onchange', reqOnChange) ;
            } 
        } 
    }

    
    
function initNewDevicesSelector(elm)
    {
    logDebug("initNewDevicesSelector", elm) ;
    var d   = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/NewDevices") ;
    d.addBoth(initSelectorExt, elm, "item", null, 
        mkConfigAttr, mkConfigText, 
        { 'class': 'OptNull' }, 25) ;
    }


function loadNewDevicesSelector()
    {
    return function (elm) 
        {
        logDebug("loadNewDevicesSelector (callback)", elm) ;
        initNewDevicesSelector(elm) ; 
        } 
    }


function showInfo(req)
    {
    s = req.src().selectedIndex ;
    id = req.src().options[s].id ;
    
    //alert ("Show Info Called with:"+id) ;
    
    showDeviceInfo(req.src(), id) ;
    }

//
//  Show a synopsis of device info by walking through the device
//
function showDeviceInfo(elm, devId)
    {
    
    function processXml(elm, req)
        {
        if ( req instanceof Error )
            {
            msg = "Server returned error: "+req ;
            }
        else
            {
            try
                {
                msg = "Must be OK:"+req.readyState ;
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
        try
            {
            var src = "<h3>Information on Device:"+devId+"</h3>" ;
            var devBox = currentDocument().getElementById("deviceInfoBox") ;
            devName = rsp.getElementsByTagName('name').item(0).getAttribute('value') ;
            src += "Name: "+devName+"<br/>" ;
            devLoc = rsp.getElementsByTagName('location').item(0).getAttribute('value') ;
            src += "Location: "+devLoc+"<br/>" ;
            devType = rsp.getElementsByTagName('type').item(0).getAttribute('value') ;
            src += "Type: "+devType+"<br/>" ;
            if ((devType != "Lutron") && (devType != "WebBrick"))
                {
                    devSrcCount = rsp.getElementsByTagName('sourcecount').item(0).getAttribute('value') ;
                    src += "Sources: "+devSrcCount+", " ;
                    devSrcTypes = rsp.getElementsByTagName('sourcetypes').item(0).getElementsByTagName('value') ;
                    src += "Type: <ul>" ;
                    for (i=0;i<devSrcTypes.length;i++)
                        {
                            src += "<li>"+devSrcTypes.item(i).textContent+"</li>" ;
                        }
                    
                    src += "</ul>" ;
                    devSnkCount = rsp.getElementsByTagName('sinkcount').item(0).getAttribute('value') ;
                    src += "Sinks: "+devSnkCount+", " ;

                    devSnkTypes = rsp.getElementsByTagName('sinktypes').item(0).getElementsByTagName('value') ;
                    src += "Type: <ul>" ;
                    for (i=0;i<devSnkTypes.length;i++)
                        {
                            src += "<li>"+devSnkTypes.item(i).textContent+"</li>" ;
                        }
                    src += "</ul>" ;
                    devCnfStatus = rsp.getElementsByTagName('confstatus').item(0).getAttribute('value') ;
                    src += "Configuration Status: "+devCnfStatus+"<br/>" ;
                }
            
            devBox.innerHTML = src ;
            }
        catch(e)
            {
            alert("Error:"+e) ;
            }
        }
    
    var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/DeviceInfo/"+devId) ;
    req.addBoth(processXml, elm)
    }


function doSources(elm,devid)
    {
    walkSources(elm,devid) 
    }      

function doSinks(devid)
    {
    alert("Not Implemented, would do the converse of sources, i.e. display sinks not yet connected.") ;
    }      

       
// End.
