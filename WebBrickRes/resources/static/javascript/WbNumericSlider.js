// $Id: WbNumericSlider.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for numeric slider

// ----------------------------------------------------------------
// Slider/dial input functions
// ----------------------------------------------------------------
function loadNumericSlider()
    {
    logDebug("loadNumericSlider: ");
    return partial(initNumericSlider) ;
    }

// Initialize a Numeric Slider to pending state
function initNumericSlider(elm)
    {
    logDebug("initNumericSlider: ", elm, ", id: ", elm.getAttribute("id") ) ;
    elm.source    = getEndPointSource(elm);
    setPoller(requestNumericSliderState, elm) ;
    }

// Polling callback function, 
// Request and eventually display the status of a button,
function requestNumericSliderState(elm)
    {
    logDebug("requestNumericSliderState: ", elm.source) ;
    if ( elm.source )
        {
        var def = doTimedXMLHttpRequest(elm.source, pollerTimeout) ;
        def.addBoth(updateNumericSliderStatus, elm) ;
        }
    else
        {
        // No source:  just reflect button state selected
        //setButtonState(btn, btn.request) ;
        }
    return ;
    }

// Receive response to button status query
// The asynchronous callback supplies the HTTP request object
function updateNumericSliderStatus(elm, req)
    {
    try
        {
        sts = getWbStatusInt(req) ;
        }
    catch( e )
        {
        sts = null ;
        logError("getWbStatusInt: ", e) ;
        }
    logDebug("updateNumericSliderStatus(callback): elm: ", elm, 
             ", req: ", req, ", sts: ", sts[2]) ;
    if ( sts != null )
        {
        try
            {
            logDebug("updateNumericSliderStatus", sts[2]) ;
            var sl = w$(elm)
            logDebug("updateNumericSliderStatus set", sl) ;
            sl.setValue( sts[2] )
            logDebug("updateNumericSliderStatus exit", sts[2]) ;
            }
        catch( e )
            {
            logError("updateNumericSliderStatus: ", e) ;
            }
        }
    return req ;    // Return request to next in callback chain
    }

