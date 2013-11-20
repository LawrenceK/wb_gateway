<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
import zone_embed

layout_params['selected_tab'] = 4
# This sets the pooling period of widgets to 30 sec
layout_params['custom_poller'] = 30

hs_key = 1

hs_name = "boiler"

hs_number = 1

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="status_embed,WebBrickGateway.templates.widgets_tabbed">


    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">
    <h1> Boiler </h1>
    
        <div class="plant_control" >         
            <wb:simpleButton wbTarget="/sendevent/heatsource/$hs_name/$hs_number/availability?type=http://id.webbrick.co.uk/events/config/set&amp;text=yes&amp;val=1">
                Make Available
            </wb:simpleButton>
            <wb:simpleButton wbTarget="/sendevent/heatsource/$hs_name/$hs_number/availability?type=http://id.webbrick.co.uk/events/config/set&amp;text=no&amp;val=0">
                Make Unavailable
            </wb:simpleButton>
        </div>
        <div class="plant_status" >    
            ${output_boiler_ashp_status( "" , hs_key , hs_name , hs_number)}
        </div>
        <div class="boiler_image"/>
    </div>
    
</html>
