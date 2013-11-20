// $Id: WbDynamicClass.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
function loadDynamicClass()
    {
    logDebug("loadDynamicClass");
    return partial(DynamicClass_init) ;
    }

function DynamicClass_init(elm)
    {
    // elm should point to object
    elm.source    = getEndPointSource(elm);
    elm.default_class = elm.getAttribute("default_class");
    elm.className = ""
    if ( elm.source )
        {
        setPoller(DynamicClass_request, elm) ;
        }
    }

// Polling callback function, 
// Request and eventually update background image
function DynamicClass_request(elm)
    {
    logDebug("DynamicClass_request: ", elm.source) ;
    var def = doTimedXMLHttpRequest(elm.source, pollerTimeout);
    def.addBoth(DynamicClass_receive, elm) ;
    return;
    }

// Receive response to analogue value status query
// The asynchronous callback supplies the HTTP request object
function DynamicClass_receive(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatus(req);
        logDebug("DynamicClass_receive (callback): elm: ", elm, ", req: ", req, ", sts: ", sts);
        if ( sts != null )
            {
            // verify contents
	    className = unescape(sts[2]);
            if (elm.className != className)
                {
                // suppress update if the same.
                logDebug("DynamicClass_receive src: ", elm.src);
                elm.className = className;    // so we can test
                }
            else
            if (!elm.src)
                {
                elm.src = elm.default_class;
                }
            }
        else
        if ( elm.default_class != elm.className )
            {
            elm.className = elm.default_class;    // so we can test
            }
        }
    catch( e )
        {
        logError("DynamicClass_receive: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }

