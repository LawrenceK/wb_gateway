/*
 *	Utility functions for OFC2 graphing
 *  and getting command line params
 */


function findSWF(movieName) {
  if (navigator.appName.indexOf("Microsoft")!= -1) {
    return window[movieName];
  } else {
    return document[movieName];
  }
}



function ofc_ready()
{
	
}

function gTitle(t)
{
	chartData["title"]["text"] =  t ;
}



function gYMaxMin(yMax,yMin)  /* yMin is an optional parameter */
{
	chartData["y_axis"]["max"] = yMax ;
    if (yMin != undefined)
    {
        chartData["y_axis"]["min"] = yMin ;
    }
}



function gName(o,n,c)  /* c is an optional parameter */
{
    chartData["elements"][o]["text"] = n ;
    if (c != undefined)
    {
        chartData["elements"][o]["colour"] = c ;
    }
}

function gLabels(l)
{
	chartData["x_axis"]["labels"]["labels"] =  l ;
}


function gSetBGColor(col)
{
    chartData["bg_colour"] = col ;   /* watch out for british spelling */
}

function gSetAxisColor(acol,gcol)    /* Axis Color, Grid Color */
{
    chartData["x_axis"]["colour"] = acol ;   
    chartData["y_axis"]["colour"] = acol ;   
    chartData["x_axis"]["grid-colour"] = gcol ;   
    chartData["y_axis"]["grid-colour"] = gcol ;   
}    


function gSetAxisNames(yName,xName)    /* xName is second because it is an optional parameter */
{
    chartData["y_legend"]["text"] = yName ;   
    if (xName != undefined)
    {
        chartData["x_legend"]["text"] = xName ;   
    }
}    



function getParam( name )
{
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}

function writeOpts(sel)
{
	for (i=0;i<datanames.length;i++)
        {
        if (i != sel)
            {
            opt = "<option value='" + i + "'>" + datanames[i] + "</option>" ;
            document.write(opt)
            }
        else
            {
            opt = "<option selected='true' value='" + i + "'>" + datanames[i] + "</option>" ;
            document.write(opt)
            }
        }
}

