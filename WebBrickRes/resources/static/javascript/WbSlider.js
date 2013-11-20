// $Id: WbSlider.js 2507 2009-06-16 07:00:45Z webbrick $


// ***********************************************************************************
//
//  Javascript to handle generic slider
//
//  This is a generic slider
//
// ***********************************************************************************


function loadWbSlider()
    {
    logDebug("loadSlider") ;
    return partial(initWbSlider) ;
    }

function initWbSlider(elm)
    {
    logDebug("initSlider: ", elm) ;
    elm.wbTarget = null ;    
    elm.wbSource = null ;    
    elm.orientation = "vertical" ; 
    elm.height = "200px" ;
    elm.sMax = 100 ;
    elm.sto = null ;
    // read attributes and create list
    v = elm.getAttribute("wbTarget");
    if ( v )
        {
        elm.wbTarget = v;
        }
    v = elm.getAttribute("wbSource");
    if ( v )
        {
        elm.wbSource = v;
        }
    v = elm.getAttribute("orientation");
    if ( v )
        {
        elm.orientation = v;
        }
    v = elm.getAttribute("height");
    if ( v )
        {
        elm.height = v;
        }    
    v = elm.getAttribute("sMax");
    if ( v )
        {
        elm.sMax = v;
        }        
    elm.source    = getEndPointSource(elm) ;
    if ( elm.source == null )
    {
        elm.source = ""
    }
    elm.callBack    = getEndPointTarget(elm) ;
    if ( elm.callBack == null )
    {
        elm.callBack = ""
    }
        
    /* now work out the children */
    
    elm.input = childNodeById(elm,"slider") ;
    elm.input.style.height = elm.height ;
    elm.slider = new Slider(childNodeById(elm,"slider"), childNodeById(elm,"slider-input"),elm.orientation); 
    elm.slider.setMaximum(elm.sMax);
    elm.slider.feedback = false ;  /* used to suppress updates when the slider is being operated */
    elm.slider.delayfeedback = 0;
    
    /* Now create the onchange */
    
    elm.numInput = childNodeById(elm,"num-input");
    elm.numInput.onchange = partial(WbSlider_num_onchange,elm) ;
    
    /* now create the outbound stuff */
    
    elm.slider.onchange = partial(WbSlider_onchange, elm);
    elm.sendUpdateFunc = partial(WbSlider_send,elm);

    /* now set up the value updates */
    
    elm.handle = setPoller(WbSlider_request, elm) ;
    }

function WbSlider_onchange(elm) 
{

    try 
    {
        elm.numInput.value = elm.slider.getValue();
        if (!elm.slider.feedback)
            {
            clearTimeout(elm.sto);
            elm.slider.delayfeedback = 2;
            elm.sto = setTimeout(elm.sendUpdateFunc,200) ;
            }
        else
            {
            elm.slider.feedback = false ;
            }       
	
	    if (typeof window.onchange == "function")
		    window.onchange();
    }
    catch( e )
    {
        logError("WbSlider_onchange: ", e) ;
    }
}

function WbSlider_send(elm)
{

  try
        {
        val = elm.slider.getValue()
        if ( elm.callBack != null )
            {
            if ( elm.callBack.endsWith('=') || elm.callBack.endsWith('/'))
            {
                url = elm.callBack+val;
            }
            else
            if ( elm.callBack.indexOf("?") < 0 )
            {
                url = elm.callBack+"?val="+val;
            }
            else
            {
                url = elm.callBack+"&val="+val;
            }
            logDebug("WbSlider_send: url ", url );
            var def = doTimedXMLHttpRequest(url, pollerTimeout);
            /* def.addBoth(pollSoon); */
            }
        else
            {
            logError("WbSlider_send (no target)") ;
            }
        }
    catch( e )
        {
        logError("WbSlider_send: ", e) ;
        }

}

function WbSlider_request(elm) 
{
    logDebug("WbSlider_request: ", elm.request, ", ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(WbSlider_received, elm) ;
        }
    else
        {
        logError("WbSlider (no source)") ;
        }
    return ;

}

function WbSlider_received(elm, req)
    {
    var sts ;
    try
        {
        sts = getWbStatusReal(req) ;
        logDebug("WbSlider_received (callback): elm: ", elm.source, ", req: ", req , ", sts", sts) ;
        if ( sts != null)
            {
            elm.slider.feedback = true ;
            if (!elm.slider.delayfeedback)
                {
                elm.slider.setValue(sts[2]) ;
                }
            else
                {
                elm.slider.delayfeedback--;
                }
            }
        else
            {
            /* nothing to do */
            }
        }
    catch( e )
        {
        sts = null ;
        logError("WbSlider_received: ", e) ;
        }
    return req ;    // Return request to next in callback chain
    }


function WbSlider_num_onchange (elm) {
	                   elm.slider.setValue(parseInt(this.value));
                       };


