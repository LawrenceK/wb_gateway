// $Id:$
//
// Javascript for a hideable box that has an open/close button
// i.e. ContextMenus etc.
//
function WbHideableBox_open(content, up, down )
{
    down.style.display = 'none';
    blindUp(content,{afterFinish: function () 
            {
                up.style.display = '';
            } } );
}

function WbHideableBox_close(content, up, down )
{
    up.style.display = 'none';
    blindDown(content,{afterFinish: function () 
            {
                down.style.display = '';
            } } );
}

function WbHideableBox_make(elmid, location, title, doHide)
{
    // make a div hidden
    logDebug("WbHideableBox_make: ", elm);
    try {
        // get image list
        var elm = $(elmid);

        var ctrls = DIV();
        var up = DIV( {'class':location + 'isclosed'} );
        up.style.display = 'none';
        up.appendChild( SPAN( "Open" ) );
        ctrls.appendChild( up );

        var down = DIV( {'class':location + 'isopen'} );
        down.appendChild( SPAN( "Close" ) );
        down.style.display = 'none';
        ctrls.appendChild( down );

        var newcontent = DIV();

        // move content to new DIV
        while ( elm.childNodes.length > 0 )
        {
            newcontent.appendChild( removeElement(elm.childNodes[0] ) );  // moved down a bit
        }

        if ( location[0] == 'b' )
        {
            elm.appendChild( newcontent );
            elm.appendChild( ctrls );
        }
        else
        {
            elm.appendChild( ctrls );
            elm.appendChild( newcontent );
        }

        if (doHide)
        {
            WbHideableBox_close(newcontent, up, down);
        }
        else
        {
            WbHideableBox_open(newcontent, up, down);
        }

        connect( down, "onclick", partial(WbHideableBox_open, newcontent, up, down) );
        connect( up, "onclick", partial(WbHideableBox_close, newcontent, up, down) );
        }
    catch( e )
        {
        logError("WbHideableBox_make: ", e) ;
        }
    
    logDebug("WbHideableBox_make: ", elm.source, ", ", elm.target, ", ", elm.title);
    }


