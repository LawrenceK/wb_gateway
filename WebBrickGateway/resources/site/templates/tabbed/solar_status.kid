<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
import zone_embed

layout_params['selected_tab'] = 4
# This sets the pooling period of widgets to 30 sec
layout_params['custom_poller'] = 30

hs_key = 3

hs_name = "solar"

hs_number = 1

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="status_embed,WebBrickGateway.templates.widgets_tabbed">


    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">
    <h1> Solar Heating System </h1>
    
        
        <div class="plant_status" >    
            ${output_solar_status( "" , hs_key , hs_name , hs_number)}
        </div>
        <div class="solar_image"/>
    </div>
    
</html>
