// $Id: WbDropDown.js 2507 2008-07-09 07:00:45Z webbrick $


// ***********************************************************************************
//
//  Javascript to handle DropDowns
//
//  This is a drop down selector that will sit in the middle of the page when requested
//
// ***********************************************************************************


function loadWbDropDown(pref,post)
    {
    logDebug("loadDropDown") ;
    return partial(initWbDropDown,pref,post) ;
    }

function initWbDropDown(pref,post,elm)
    {
    logDebug("initDropDown: ", elm) ;
    elm.pref      = pref ;
    elm.post      = post ;
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
    v = elm.getAttribute("options");
    if ( v )
        {
        eval ("elm.options" + "=" + unescape(v)) ;
        }
    v = elm.getAttribute("display");
    if ( v )
        {
        elm.display = v;
        }
    else
        {
        elm.display = "time" ;
        }
        
    connect( elm, "onclick", function() { WbDropDown_popover( elm, partial( WbDropDown_send, elm ) ); } );
    }

function WbDropDown_send(elm,val)
{
    var prev = window.url ;
    paramsArray(location.href,elm.wbTarget,val) ;
}

function paramsArray (prevURL,newParam,newVal)
{
    re = new RegExp ("[?&]");
    var found = false ;
    var bits = prevURL.split(re) ;
    for (i=0;i<bits.length;i++)
        {
        if (bits[i].indexOf(newParam)==0)
            {
            found=true ;
            bits[i] = newParam + "=" + newVal ;
            } 
        }
  
  // now reconstruct URL and 'replace' it
  
  if (found==false)
    {
    bits.push(newParam + "=" + newVal) ;  // add param if it was not found
    }
  
  var url = bits[0] ;  // the first part, the url
  if (bits[1])
    {
    url = url + "?" + bits[1] ; // first param
    }
  if (bits[2])
    {
    for (i=2;i<bits.length;i++)
        {
        url = url + "&" + bits[i] ;
        }
    } 
    location.replace(url) ;
}



function WbDropDown_popover(elm, callBack)
{
    logDebug("WbDropDown_popover: ", elm );
    // make popover because it does not yet exist
    var newSpan = SPAN(null,null) ;
    newSpan.innerHTML=buildOpts(elm.options,elm.display) ;
    var newDiv = DIV({'id': 'WbDropDown', 'class': 'dropDown'}, newSpan );
    appendChildNodes( currentDocument().body, newDiv );
    //Set the call back    
    $("WbDropDown").callBack = callBack;
    // hide a chart if there is one
    if ($("my_chart"))
        {
        $("my_chart").style.visibility = "hidden" ;
        }
  MochiKit.Visual.appear('WbDropDown') ;
}

function WbDropDown_CB( val ) {
    np = $("WbDropDown") ;
    np.callBack( val );
    MochiKit.Visual.fade('WbDropDown') ;
}

function cancelWbDropDown() {
    MochiKit.Visual.fade('WbDropDown');
    var t = setTimeout(document.body.removeChild($('WbDropDown')),1000); /* allow enough time to fade */
    // un-hide a chart if there is one
    if ($("my_chart"))
        {
        $("my_chart").style.visibility = "visible" ;
        }
    return false ;
}


// *****************************************************************************************************
//
//  Here are the helper routines that are used to manipulate the drop down
//
// *****************************************************************************************************


function buildOpts(optList, display)
{
    var oList = "" ;
    var cancelDef = "<span class=\"dropDownCancel\" onClick=\"cancelWbDropDown()\">Cancel</span>" ;
    var i = 0 ;
    var c = 0 ;
    oList = oList + "<table><colgroup span='3' width='33%' /><tr>";
    while (optList["options"][i])
        {
         var show = optList["options"][i] ;
         var param = optList["options"][i] ;
         if (display == 'isodate')
            {
            var bits = show.split(".") ;
            if (bits[2])
                {
                show = bits[2] ;
                param = bits[2] ;
                } 
            else
                {
                show = "Today" ;
                param = "Today" ;
                }
            }
         else if (display == 'names')
            {
                param = i;
            }
         opt = "<td class=\"dropDownEntry\" onClick=\"WbDropDown_CB('" + param + "')\">" + show + "</td>" ;  // dragons 
         oList = oList + opt ;
         i++ ;
         c++ ;
         if (c==3)
            {
            oList = oList + "</tr><tr>";
            c = 0 ;
            }
        }
    oList = oList + "</tr></table>";
    return oList + cancelDef ;  
}

