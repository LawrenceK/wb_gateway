// $Id: WbCaption.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for caption display

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

