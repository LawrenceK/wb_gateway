
// Javascript for hiding the address bar on the iTouch
// Or rather scrolling down the page to hide it


addEventListener
(
    "load", 
    function()
    {
        setTimeout(hideURLbar, 0);
    }
    , false
);

function hideURLbar()
{
    window.scrollTo(0, 1);
}