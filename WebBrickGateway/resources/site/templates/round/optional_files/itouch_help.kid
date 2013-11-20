<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['page_title'] = "WBS Help"
layout_params['itouch_icon'] = ""

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'sitelayout_itouch.kid'" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">

    
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}itouchboxcontent'" id="itouchboxcontent">
        
        <h1>Help Page</h1>
        <div> 
            This is just an example of a few controls that can be 
            made available on your iPhone or iTouch. Please discuss 
            details with your installer. <br/><br/>           
        </div>
        <wb:simpleLinkButton
                target="/template/itouch_welcome" 
                >
                Welcome Page
        </wb:simpleLinkButton>
                
        
    </div>

    

</html>
