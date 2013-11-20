// $Id: WbFlashGraph.js 2507 2008-07-09 07:00:45Z webbrick $


// ***********************************************************************************
//
//  Global Data Defnition
//
//  TODO -- some day, tie this to the element
//
// ***********************************************************************************


function loadFlashGraph()
    {
    logDebug("loadFlashGraph") ;
    return partial(initFlashGraph) ;
    }

function initFlashGraph(elm)
    {
    logDebug("initFlashGraph: ", elm) ;
    try {

        v = elm.getAttribute("minYval");
        if ( v )
            {
            elm.minYval = v;
            gYMin(v) ;
            }
        else
            {
            elm.minYval  = 0;
            }
        v = elm.getAttribute("maxYval");
        if ( v )
            {
            elm.maxvalue = v;
            gYMax(v) ;
            }
        else 
            {
            elm.maxYval  = 50;
            }
        v = elm.getAttribute("xLabels");
        if ( v )
            {
            elm.xLabels = v;
            gXLabels(v) ;
            }
        v = elm.getAttribute("gTitle");
        if ( v )
            {
            elm.title = v;
            gTitle(v);
            }
        else
            {
            elm.title = "Not Set";
            }
        v = elm.getAttribute("activeSets");
        if ( v )
            {
            elm.activeSets = v;
            gActiveSets(eval(v));
            }
        else
            {
            elm.activeSets = "0,1,2,3";
            }
        v = elm.getAttribute("height");
        if ( v )
            {
            elm.height = v;
            }
        else
            {
            elm.height   = 600;            
            }
        v = elm.getAttribute("width");
        if ( v )
            {
            elm.width = v;
            }
        else
            {
            elm.width    = 800;
            }
        v = elm.getAttribute("yLabelStyle");
        if (v)
            {
            gSetYLabelStyle(v) ;
            } 
           
        
        // Create sub elements.
        movie = elm.getAttribute("flashMovie");
        gSetBGColor(-1);  // this will make the movie transparent

        
        if ( movie )
            {
            elm.innerHTML = '<span id="my_chart" />';
            // now populate what has been created
            swfobject.embedSWF("/static/flash/open-flash-chart.swf", "my_chart", elm.width, elm.height, "9.0.0","expressinstall.swf",{},{},{wmode : "transparent"});

            }

        }
    catch( e )
        {
        logError("initFlashGraph: ", e) ;
        }
    }


// *****************************************************************************************************
//
//  Here are the routines that are used to manipulate the data withing the graph
//
//  o = object
//  a = array
//  c = colour       [Note the British Spelling]
//
//
// *****************************************************************************************************

// Called from open flashchart



function open_flash_chart_data()
{
	//where prototype and JSON are about, stringify runs into problems, try the prototype version first then fail to stringify
	try {
        return Object.toJSON(chartData);
    }
    catch(e){
	    return JSON.stringify(chartData);
	}
}


function gReload()   /* causes the graph to reload */
{
    tmp = findSWF("my_chart") ;
    try {
        x = tmp.load(Object.toJSON(chartData)) ;
    }
    catch(e) {
    x = tmp.load(JSON.stringify(chartData)) ;
    }
}

function gTitle(t)
{
	chartData["title"]["text"] =  t ;
}

function gYMin(yMin) 
{
	chartData["y_axis"]["min"] = yMin ;
}

function gYMax(yMax) 
{
	chartData["y_axis"]["max"] = yMax ;
}

function truncateTimes(a)
{
    for (i=0;i<a.length;i++) {
    a[i] = a[i].slice(0,5);
    }
}


function gXLabels(lType)
{
    if (lType=="date") 
        {
    	chartData["x_axis"]["labels"]["labels"] =  chartData["x_axis"]["labels"]["dates"] ;
        chartData["x_legend"]["text"] = "Date" ;   
        }
    else
        {
        truncateTimes(chartData["x_axis"]["labels"]["times"]) ;
    	chartData["x_axis"]["labels"]["labels"] =  chartData["x_axis"]["labels"]["times"] ;
        chartData["x_legend"]["text"] = "Time" ;   
        }
}


function gValues(depth)
{
	/* attempt to replace missing values with null, depth is the number of datasets that are in the graph */
		
	for (i=0;i<depth;i++) {
	    for (j=0;j<chartData["elements"][i]["values"].length;j++) {
	        if (chartData["elements"][i]["values"][j].length==0) {
	            chartData["elements"][i]["values"][j]= null ;
	        }
	    }
	}
	
}


function gActiveSets(sList)
{
    for (i=0;i<sList.length;i++)
        {
        j = sList[i] 
        chartData["elements"][i]["values"] = chartData["datasets"][j]["values"] ;
        chartData["elements"][i]["text"] = chartData["datasets"][j]["text"] ;
        }
    gValues(sList.length);
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

function gSetYLabelStyle(s)   /* set y label style in the form size,color */
{

    chartData["y_label__label_style"] = s ;

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

