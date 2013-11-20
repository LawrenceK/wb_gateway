// $Id:$
//
function loadImageIndicator()
    {
    logDebug("loadImageIndicator");
    return partial(ImageIndicator_init) ;
    }

function ImageIndicator_init(elm)
    {
	// elm should be an image element.
    elm.source    = getEndPointSource(elm);
    if ( elm.source )
		{
		setPoller(ImageIndicator_request, elm) ;
		}
    elm.imageList  = ["/static/images/off.png", "/static/images/on.png"] ;
    
    // pick up mapval labels from the HTML file
    // (cf. push button selector object)
    var attr = elm.getAttribute("imageUris") ;
    if (attr)
        {
        // comma separated list of values.
        var v = attr.split(",");
        if  (v.length >= 2)
            {
            elm.imageList  = v;
            }
        }
    logDebug("ImageIndicator imageUris: ", elm.imageList) ;
    }

// Polling callback function, 
// Request and eventually update background image
function ImageIndicator_request(elm)
    {
    logDebug("ImageIndicator_request: ", elm.source) ;
	var def = doTimedXMLHttpRequest(elm.source, pollerTimeout);
	def.addBoth(ImageIndicator_receive, elm) ;
    return;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function ImageIndicator_receive(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatusBoolInteger(req) ;
        logDebug("ImageIndicator_receive (callback): elm: ", elm, ", req: ", req, ", sts: ", sts);
        if ( ( sts != null ) && (sts[2] >= 0 ) && (sts[2] < elm.imageList.length) )
            {
            elm.src = elm.imageList[sts[2]];
            logDebug("ImageIndicator_receive src: ", elm.src);
            }
        else
            {
            logError("ImageIndicator_receive: ", sts);
            }
        }
    catch( e )
        {
        logError("ImageIndicator_receive: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

