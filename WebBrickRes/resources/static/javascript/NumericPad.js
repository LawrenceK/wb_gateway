// Use an existing DIV or create one and then absolute position it.
function addChar( c )
{
    logDebug("addChar: ", c) ;
    $("numpadtext").value += c;
};

function PopUpDone()
{
    np = $("numberpad")
    npt = $("numpadtext").value;
    logDebug("PopUpDone: ", npt );
    var pat = /^[-]?\d+(.\d*)?$/ ;  // [-]digit digit* [ "." digit* ]
    if ( pat.test(npt) )
    {
        np.callBack( npt );
        np.style.visibility ='hidden';
    }
    else
    if ( npt == "" )
    {
        np.style.visibility ='hidden';
    }
    else
    {
        alert('invalid number');
    }
    $("numpadtext").value = "";
//    currentDocument().body.style.opacity = '1.0';
}

function PopUpCancel()
{
    np = $("numberpad")
    logDebug("PopUpCancel: ") ;
    np.style.visibility ='hidden';
//    currentDocument().body.style.opacity = '1.0';
}

function PopUpNumericEntry( elm, callBack ) 
{
    logDebug("PopUpNumericEntry: ", elm );
    // does the calendar DIV exist?
    // No create DIV and populate and locate.
    // show.
    if (!$("numberpad"))
    {
        logDebug("PopUpNumericEntry: Create " );
        var rows = [
            [   
                [ {},IMG({ "src" : "/static/images/numerals/7.png", "onclick":"addChar('7')" } )],
                [ {},IMG({ "src" : "/static/images/numerals/8.png", "onclick":"addChar('8')" } )],
                [ {},IMG({ "src" : "/static/images/numerals/9.png", "onclick":"addChar('9')" } )],
            ],
            [   
                [ {},IMG({ "src" : "/static/images/numerals/4.png", "onclick":"addChar('4')" } )],
                [ {},IMG({ "src" : "/static/images/numerals/5.png", "onclick":"addChar('5')" } )],
                [ {},IMG({ "src" : "/static/images/numerals/6.png", "onclick":"addChar('6')" } )],
            ],
            [   
                [ {},IMG({ "src" : "/static/images/numerals/1.png", "onclick":"addChar('1')" } )],
                [ {},IMG({ "src" : "/static/images/numerals/2.png", "onclick":"addChar('2')" } )],
                [ {},IMG({ "src" : "/static/images/numerals/3.png", "onclick":"addChar('3')" } )],
            ],
            [   
                [ {},IMG({ "src" : "/static/images/numerals/0.png", "onclick":"addChar('0')" } )],
                [ {}, SPAN( {'id': 'blank'},"") ],
                [ {},IMG({ "src" : "/static/images/numerals/dot.png", "onclick":"addChar('.')" } )],
            ],
            [   
                [ {'colSpan':'3'},INPUT({'id': 'numpadtext', 'len':'10', 'width':'100%'} )],
            ],
            [   
                [ {},IMG({ "src" : "/static/images/numerals/cancel.png", "onclick":"PopUpCancel()" } )],
                [ {},IMG({ "src" : "/static/images/numerals/set.png", "onclick":"PopUpDone()" } )],
//                [ {'colspan':'2'},INPUT({'type':'button', 'onclick': 'PopUpCancel()', 'value':'Cancel'} )],
//                [ {},INPUT({'type':'button', 'onclick': 'PopUpDone()', 'value':'Ok'} )],
            ],
        ];
        cell_display = function (cell) 
            {
			if (cell)
				{
				return TD(cell[0], cell[1]);
				}
            }
        row_display = function (row) 
            {
			if (row)
				{
				return TR(null, map(cell_display, row) );
				}
            }

        var newTable = TABLE(null,
            TBODY(null,
				// add a colgroup to the table.
				createDOM('colgroup', {'span':'3', 'width':'30%'} ),
                map(row_display, rows)));

        var newDiv = DIV({'id': 'numberpad', 
                            'class': 'dataEntry', 
                            'opacity':'0.95', 
                            "onfocuslost":"PopUpCancel()"}, 
//                    DIV( {'id': 'numpadtitle'},""),
                    newTable );
        appendChildNodes( currentDocument().body, newDiv );
        newDiv.style.position ='absolute';
        newDiv.style.width ='200px';
        newDiv.style.height ='200px';
        newDiv.style.zIndex ='1010';
        $("numpadtext").onkeypress=anyFloatInputOnly;
    }
//    ePos = elementPosition( elm );
//    logDebug("elm position: ", ePos.x, ePos.y ) ;
    logDebug("elm title: ", elm.title ) ;
    $("numberpad").style.top = '70px';
    $("numberpad").style.left = '15%';
//    $("numberpad").style.top = (ePos.y+10)+'px';
//    $("numberpad").style.left = (ePos.x+10)+'px';
    $("numberpad").callBack = callBack;
    $("numberpad").style.visibility ='visible';
    $("numpadtext").value = "";
    $("numpadtext").focus();
//    setElementText($("numpadtitle"), elm.title );
//    $("numberpad").style.opacity = '1.0';
//    currentDocument().body.style.opacity = '0.25';
};
