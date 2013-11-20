<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['page_title'] = "WBS Welcome"
layout_params['itouch_icon'] = ""

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'sitelayout_itouch.kid'" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">

    
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}itouchboxcontent'" id="itouchboxcontent">
        
        <div style="width:100%; text-align:center; font-weight:bold; margin-bottom:10px;">Public Gateway</div>
        <div style="margin-left:46px;">
            <wb:simpleLinkButton
                    target="/template/itouch_kitchen" 
                    >
                Kitchen
            </wb:simpleLinkButton>
        
            <wb:simpleLinkButton 
                    target="/template/itouch_dining"
                    >
                Dining Room
            </wb:simpleLinkButton>
            
            <wb:simpleLinkButton
                    target="/template/itouch_lounge" 
                    >
                Lounge
            </wb:simpleLinkButton>
        
            <wb:simpleLinkButton 
                    target="/template/itouch_office"
                    >
                Office
            </wb:simpleLinkButton>
            <div style="float:left;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            </div>
            <wb:simpleButton 
                    wbTarget="/sendevent/sleep">
                Sleep House
            </wb:simpleButton>
        </div>
        

    </div>

    

</html>
