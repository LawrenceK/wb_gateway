//********************************************************************************
//
//  Functions to do with Devices, like walking through sources,sinks etc
//
//  Andy Harris, WebBrick Systems, 30th July 2009
//
//********************************************************************************

//
//  Walk through a devices sources and display these
//
function walkButtons(id,devid)
    {
        //alert ("Called with:"+devid) ;
        // Clear the server message box
        //currentDocument().getElementById("serverMessage").innerHTML = "" ;

        function processXml(id, req)
            {
            var keypads = new Array();
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
                    devKeypads = rsp.getElementsByTagName('keypad') ; // returns array of source elements
                    //alert("devSources:"+devSources.length);
                    
                    for (i=0;i<devKeypads.length;i++)
                        {
                            processor = devKeypads.item(i).getElementsByTagName("processor").item(0).getAttribute('value') ;
                            link = devKeypads.item(i).getElementsByTagName("link").item(0).getAttribute('value') ;
                            number = devKeypads.item(i).getElementsByTagName("number").item(0).getAttribute('value') ;
                            xmlId = processor + link + number
                            if (xmlId  == id)
                            {
                            
                                keypad = devKeypads.item(i) ;
                                keypad.buttons = devKeypads.item(i).getElementsByTagName("button") ;
                                outputButtons(keypad) ;
                                break
                            }
                        }
                }
                
            catch(e)
                {
                alert("Error:"+e) ;
                }

            
        }    
            
            
        var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/Keypads/"+devid) ;
        req.addBoth(processXml, id) ;
    }
function outputButtons(keypad)
    {
        //alert("Called with:"+keypads) ;
        var src = "" ;
        for (i=0;i<keypad.buttons.length;i++)
            {
                buttonnumber = keypad.buttons.item(i).getElementsByTagName("number").item(0).getAttribute('value') ;
                buttonicon = keypad.buttons.item(i).getElementsByTagName("icon").item(0).getAttribute('value') ;
                dispClass = "notConnected" ;
                src += "<option id='" + buttonnumber +  "' class='"+dispClass+"'>"; 
                src += buttonnumber + " : " + buttonicon +  "</option>" ;
            }
        var keypadBox = currentDocument().getElementById("ButtonSelector") ;
        keypadBox.innerHTML = src ;
    }
function showKeyPadInfo(elm,devid)
    {
        //alert ("Called with:"+devid) ;
        // Clear the server message box
        //currentDocument().getElementById("serverMessage").innerHTML = "" ;

        function processXml(id, req)
            {
            //alert("called with id " + id)
            var keypads = new Array();
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
                devKeypads = rsp.getElementsByTagName('keypad') ; // returns array of source elements
                //alert("devSources:"+devSources.length);
                
                for (i=0;i<devKeypads.length;i++)
                    {
                        processor = devKeypads.item(i).getElementsByTagName("processor").item(0).getAttribute('value') ;
                        link = devKeypads.item(i).getElementsByTagName("link").item(0).getAttribute('value') ;
                        number = devKeypads.item(i).getElementsByTagName("number").item(0).getAttribute('value') ;
                        xmlId = processor + link + number
                        if (xmlId  == id)
                        {
                        
                            keypad = devKeypads.item(i) ;
                            keypad.processor = devKeypads.item(i).getElementsByTagName("processor").item(0).getAttribute('value') ;
                            keypad.link = devKeypads.item(i).getElementsByTagName("link").item(0).getAttribute('value') ;
                            keypad.number = devKeypads.item(i).getElementsByTagName("number").item(0).getAttribute('value') ;
                            keypad.buttons = devKeypads.item(i).getElementsByTagName("buttons") ;
                            outputKeypadInfo(keypad) ;
                            break
                        }
                    }
                }
            catch(e)
                {
                alert("Error:"+e) ;
                }
            }    
            
        s = elm.selectedIndex ;
        id = elm.options[s].id
        elm.options[s].setAttribute ("className","selected") ;  // change the highlight
        if (id != "")
        {
            var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/Keypads/"+devid) ;
            req.addBoth(processXml, id) ;
        }
    }

function outputKeypadInfo(keypad)
    {
    //alert("outputInfo called with:"+elm) ;
    var infoBox = currentDocument().getElementById("keypadInfoBox") ;
    var src = "" ;
    src += "<h3>Keypad - : " + keypad.processor + ":" + keypad.link + ":" + keypad.number + "</h3>" ;
    src += "<br/>" ;
    src+= "Buttons configured : " + keypad.buttons.length ; 
    infoBox.innerHTML = src ;
    }


function walkKeypads(elm,devid)
    {
        //alert ("Called with:"+devid) ;
        // Clear the server message box
        //currentDocument().getElementById("serverMessage").innerHTML = "" ;

        function processXml(elm, req)
            {
            var keypads = new Array();
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
                devKeypads = rsp.getElementsByTagName('keypad') ; // returns array of source elements
                //alert("devSources:"+devSources.length);
                for (i=0;i<devKeypads.length;i++)
                    {
                    keypads[i] = devKeypads.item(i) ;
                    keypads[i].processor = devKeypads.item(i).getElementsByTagName("processor").item(0).getAttribute('value') ;
                    keypads[i].link = devKeypads.item(i).getElementsByTagName("link").item(0).getAttribute('value') ;
                    keypads[i].number = devKeypads.item(i).getElementsByTagName("number").item(0).getAttribute('value') ;
                    keypads[i].location = devKeypads.item(i).getElementsByTagName("location").item(0).getAttribute('value') ;
                    keypads[i].buttons = devKeypads.item(i).getElementsByTagName("buttons").item(0).getAttribute('value') ;
                    
                    }
                }
            catch(e)
                {
                alert("Error:"+e) ;
                }
            //
            // Now output to the options field
            //
            
            outputKeypads(keypads) ;
            
        }    
            
            
        var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/Keypads/"+devid) ;
        req.addBoth(processXml, elm) ;
    }
function outputKeypads(keypads)
    {
        //alert("Called with:"+keypads) ;
        var src = "" ;
        for (i=0;i<keypads.length;i++)
            {
               
            if (keypads[i].buttons !="0")
                {
                dispClass = "connected" ;
                }
            else
                {
                dispClass = "notConnected" ;
                }
                            
            src += "<option id='" + keypads[i].processor + keypads[i].link + keypads[i].number + "' class='"+dispClass+"'>"; 
            src += keypads[i].processor + " : " + keypads[i].link + " : " + keypads[i].number + " : " + keypads[i].location + "</option>" ;
            }
        var keypadBox = currentDocument().getElementById("KeypadSelector") ;
        keypadBox.innerHTML = src ;
    }
function walkSources(elm,devid)
    {
    //alert ("Called with:"+devid) ;
    // Clear the server message box
    currentDocument().getElementById("serverMessage").innerHTML = "" ;

    function processXml(elm, req)
        {
        var sources = new Array();
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
            devSources = rsp.getElementsByTagName('source') ; // returns array of source elements
            //alert("devSources:"+devSources.length);
            for (i=0;i<devSources.length;i++)
                {
                sources[i] = devSources.item(i) ;
                sources[i].type = devSources.item(i).getElementsByTagName("type").item(0).getAttribute('value') ;
                sources[i].name = devSources.item(i).getElementsByTagName("name").item(0).getAttribute('value') ;
                sources[i].status = devSources.item(i).getElementsByTagName("status").item(0).getAttribute('value') ;
                sources[i].conn = devSources.item(i).getElementsByTagName("id").item(0).getAttribute('value') ;
                sources[i].connectedto = devSources.item(i).getElementsByTagName("connectedto").item(0).getAttribute('value') ; 
                }
            }
        catch(e)
            {
            alert("Error:"+e) ;
            }
        //
        // Now output to the options field
        //
        outputSources(sources) ;    
        }
    
    var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/Sources/"+devid) ;
    req.addBoth(processXml, elm) ;
    }

//
// Given an array of sources, output these
//    
function outputSources(sources)
    {
    //alert("Called with:"+sources) ;
    var src = "" ;
    for (i=0;i<sources.length;i++)
        {
        // output an option
        if (sources[i].connectedto!="")
            {
            dispClass = "connected" ;
            connId = " : " + sources[i].connectedto ;
            }
        else
            {
            dispClass = "notConnected" ;
            connId = "" ;
            }            
        src += "<option id='"+sources[i].conn+"' class='"+dispClass+"'>"; 
        src += sources[i].conn+" : "+sources[i].name+" : "+sources[i].type+connId+"</option>" ;
        }
    var connBox = currentDocument().getElementById("DevConnSelector") ;
    connBox.innerHTML = src ;
    }    

//
//  Attach a device and its properties to an element
//
function attachDevice(elm,devid)
    {
    //alert("attachDevice called with:"+elm+" and "+devid);
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
            elm.devName = rsp.getElementsByTagName('name').item(0).getAttribute('value') ;
            elm.devLoc = rsp.getElementsByTagName('location').item(0).getAttribute('value') ;
            elm.devSrcCount = rsp.getElementsByTagName('sourcecount').item(0).getAttribute('value') ;
            elm.devCnfStatus = rsp.getElementsByTagName('confstatus').item(0).getAttribute('value') ;
            }
        catch(e)
            {
            alert("Error:"+e) ;
            }
        outputInfo(elm) ;    
        }
    
    var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/DeviceInfo/"+devid) ;
    req.addBoth(processXml, elm) ;    
    }

function outputInfo(elm)
    {
    //alert("outputInfo called with:"+elm) ;
    var infoBox = currentDocument().getElementById("deviceInfoSynopsis") ;
    var src = "" ;
    infoBox.innerHTML = "<b>Name: </b>"+elm.devName+" <b>Location: </b>"+elm.devLoc+" <b>Status: </b>"+elm.devCnfStatus ;
    }


//
// Show the user the available connection options
//
//  The incoming element is the select 
//    
function showConnOptions(elm)
    {
    s = elm.selectedIndex ;
    id = elm.options[s].id ;
    //alert("showConnOptions called with:"+id) ;
    // Clear the server message box
    currentDocument().getElementById("serverMessage").innerHTML = "" ;
     
    function processXml(elm, req)
        {
        elm.devices = new Array();
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
            // Process stuff here
            compDevices=rsp.getElementsByTagName('device') ;
            for (i=0;i<compDevices.length;i++)
                {
                elm.devices[i] = compDevices.item(i) ;
                elm.devices[i].name = compDevices.item(i).getElementsByTagName("name").item(0).getAttribute('value') ;
                elm.devices[i].sinks = compDevices.item(i).getElementsByTagName("sinks");
                //alert("Found Sinks:"+elm.devices[i].sinks[0].getElementsByTagName("id").item(0).getAttribute('value'));
                for (j=0;j<elm.devices[i].sinks.length;j++)
                    {
                    elm.devices[i].sinks[j].id = elm.devices[i].sinks[j].getElementsByTagName("id").item(0).getAttribute('value') ;
                    elm.devices[i].sinks[j].name = elm.devices[i].sinks[j].getElementsByTagName("name").item(0).getAttribute('value') ;
                    elm.devices[i].sinks[j].connectedto = elm.devices[i].sinks[j].getElementsByTagName("connectedto").item(0).getAttribute('value') ;
                    }
                }
            }
        catch(e)
            {
            alert("Error:"+e) ;
            }
        outputCompatibleSinks(elm,id) ;  // we pass the id so we can determine the self connection status  
        }
    
    var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/compatible/sinks/"+id) ;
    req.addBoth(processXml, elm) ;    
    }    
    
    
// should be called with an array of devices attached to the element that could be connected to    
function outputCompatibleSinks(elm,sourceConnId)
    {
    //alert("outputCompatibleSinks called with:"+elm.devices.length+" and id:"+sourceConnId) ;
    var connOptionBox = currentDocument().getElementById("connOptions") ;
    var src = "" ;
    var dispClass = "" ;
    var dispConn = "";
    for (i=0;i<elm.devices.length;i++)
        {
        // start to output connection options
        for (j=0;j<elm.devices[i].sinks.length;j++)
            {
            if (elm.devices[i].sinks[j].connectedto==sourceConnId)
                {
                dispClass = "connectedToThis" ;
                }
            else if (elm.devices[i].sinks[j].connectedto!="")
                {
                dispClass = "connected" ;
                }
            else
                {
                dispClass = "notConnected" ;
                }
            dispConn = "' sinkConn='"+elm.devices[i].sinks[j].connectedto ;                
            src += "<option id='"+elm.devices[i].sinks[j].id+"' class='"+dispClass+dispConn+"'>" ;
            src += elm.devices[i].sinks[j].id+" : " ;
            src += elm.devices[i].name+" : "+elm.devices[i].sinks[j].name+"</option>" ;
            }
        }
    connOptionBox.innerHTML = src ;    
    }    
    
    
function showSinkDetails(elm)
    {
    s = elm.selectedIndex ;
    id = elm.options[s].getAttribute("sinkconn") ;
    elm.options[s].setAttribute ("className","selected") ;  // change the highlight
    //alert("showSinkStatus called with:"+id) ;
    function processXml(elm, req)
        {
        elm.devices = new Array();
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
            // Process stuff here
            // alert ("Response for sink is:"+rsp.getElementsByTagName("device").length);
            elm.sink = rsp.getElementsByTagName('device').item(0) ;
            elm.sink.devName = elm.sink.getElementsByTagName('name').item(0).getAttribute('value') ;
            elm.sink.source = rsp.getElementsByTagName('source').item(0) ;
            elm.sink.sourceName = elm.sink.source.getElementsByTagName('name').item(0).getAttribute('value') ;
            elm.sink.sourceId = elm.sink.source.getElementsByTagName('id').item(0).getAttribute('value') ;
            }
        catch(e)
            {
            alert("Error:"+e) ;
            }
        outputSinkDetail(elm) ;  
        }
    
    // don't do anything for non connected sinks
    if (id!="")
        {
        var req = doSimpleXMLHttpRequest("/wbgwcnf/GetXml/Source/"+id) ;
        req.addBoth(processXml, elm) ;
        }
    else
        {
        currentDocument().getElementById("sinkDetail").innerHTML = "Not Connected" ;        
        }    
    }    
    
    
// elm has a sink attack to it, display the properties
function outputSinkDetail(elm)
    {
    //alert("outputSinkDetail called with:"+elm) ;
    var sinkBox = currentDocument().getElementById("sinkDetail") ;
    var src = "" ;
    sinkBox.innerHTML = "<b>Device: </b>"+elm.sink.devName+" <b>Connection: </b>"+elm.sink.sourceName+" <b>ID: </b>"+elm.sink.sourceId ;
    }    
