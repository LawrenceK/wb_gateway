// $Id: WbPanel.js 3709 2010-09-10 09:41:08Z philipp.schuster $
//
// Javascript library for WebBrick control panel interaction widgets

// ----------------------------------------------------------------
// Panel functions
// ----------------------------------------------------------------

function changeBackground(theme)
    {
    document.body.className = theme ;
    }

function changeBG(){
	document.body.className = bimages[bindex] ;
	bindex++ ;
	if (bindex >= bimages.length)
		{
		bindex = 0 ;
		}
	setTimeout("changeBG()", 5000);
}



