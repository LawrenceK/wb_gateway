<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['page_title'] = "Lounge"
layout_params['itouch_icon'] = "zoneiconlounge.png"

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'sitelayout_itouch.kid'" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">

    
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}itouchboxcontent'" id="itouchboxcontent">
        
        <div style="width:100%; text-align:center; font-weight:bold; margin-bottom:10px;">Lounge</div>
        <div style="margin-left:46px;">
         
            <wb:simpleButton 
                    wbTarget="/sendevent/from_ui/lounge/lighting/main/off"
                    wbSource="/eventstate/to_ui/lounge/lighting/main/state">
                Lights Off
            </wb:simpleButton>
        
            <wb:simpleButton wbTarget="/sendevent/from_ui/lounge/lighting/main/low">
                Lights Low
            </wb:simpleButton>
       
            <wb:simpleButton wbTarget="/sendevent/from_ui/lounge/lighting/main/high">
                Lights Full
            </wb:simpleButton>
            
            <div style="float:left;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            </div>
            
            <wb:simpleButton wbTarget="/sendevent/from_ui/lounge/lighting/main/scene_up">
                Scene Up
            </wb:simpleButton>
   
            <wb:simpleButton wbTarget="/sendevent/from_ui/lounge/lighting/main/scene_down">
                Scene Down
            </wb:simpleButton>
            
        </div>
        

    </div>

    

</html>
