// $Id: WbTextEntry.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript library for WebBrick control panel interaction widgets

// ----------------------------------------------------------------
// Text entry display functions
// ----------------------------------------------------------------
//
// sample use
//
// wbSource is the URL for the text content and will replace the &nbsp;
//
//    <td wbType="Text" wbLoad='loadTextEntry("","")'
//            wbSource="/local/messages">
//        &nbsp;
//    </td>

// Initial load of a caption object
function loadTextEntry(pref, post)
    {
    logDebug("loadTextEntry") ;
    if (!pref) pref = "" ;
    if (!post) post = "" ;
    return partial(initTextEntry, pref, post) ;
    }

function initTextEntry(pref, post, elm)
    {
    logDebug("initTextEntry: ", pref, ", ", post, ", ", elm) ;
    elm.pref      = pref ;
    elm.post      = post ;
    elm.source    = getEndPointSource(elm) ;
    elm.className = "textPending" ;
    setPoller(requestTextState, elm) ;
    }
