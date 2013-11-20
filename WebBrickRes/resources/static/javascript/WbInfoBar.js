// $Id: WbInfoBar.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript for info bar widget

// Change information bar content for the current document
// The information bar is a 1-row table with id "wbInfoBar"
// Supplied arguments are text values set into successive cells
// ('arguments' is a Javascript special variable.
function changeInfoBar()
    {
    var ib  = document.getElementById("wbInfoBar") ;
    var tr  = ib.rows[0] ;
    var tds = tr.cells ;
    for ( var i = 0 ; i < arguments.length ; i++ )
        {
        if ( i < tds.length )
            {
            tds[i].nodeValue = arguments[i] ;
            }
        }
    }
