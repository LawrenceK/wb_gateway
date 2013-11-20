// $Id:$
//
function loadDynamicImage()
    {
    logDebug("loadDynamicImage");
    return partial(DynamicImage_init) ;
    }

function DynamicImage_init(elm)
    {
    // elm should be an image element.
    elm.source    = getEndPointSource(elm);
    elm.default_image = elm.getAttribute("default_image");
    elm.image_uri = ""
    if ( elm.source )
        {
        setPoller(DynamicImage_request, elm) ;
        }
    }

// Polling callback function, 
// Request and eventually update background image
function DynamicImage_request(elm)
    {
    logDebug("DynamicImage_request: ", elm.source) ;
    var def = doTimedXMLHttpRequest(elm.source, pollerTimeout);
    def.addBoth(DynamicImage_receive, elm) ;
    return;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function DynamicImage_receive(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req);
        logDebug("DynamicImage_receive (callback): elm: ", elm, ", req: ", req, ", sts: ", sts);
        if ( sts != null )
            {
            // verify contents
	    uri = unescape(sts[2]);
            if (elm.image_uri != uri)
                {
                // suppress update if the same.
                logDebug("DynamicImage_receive src: ", elm.src);
                elm.src = sts[2];
                elm.image_uri = uri;    // so we can test
                }
            else
            if (!elm.src)
                {
                elm.src = elm.default_image;
                }
            }
        else
        if ( elm.default_image != elm.image_uri )
            {
            elm.src = elm.default_image;
            elm.image_uri = elm.default_image;    // so we can test
            }
        }
    catch( e )
        {
        logError("DynamicImage_receive: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

