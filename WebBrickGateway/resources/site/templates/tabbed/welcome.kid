<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
import zone_embed
layout_params['selected_tab'] = 0
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="zone_embed,WebBrickGateway.templates.widgets_tabbed">



    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">
        ${output_zone_spinner( "zone2", "heating" , "Heating"  , 10, 25)}
        ${output_zone_spinner( "zone1", "hotwater", "Hot Water", 10, 65)}

    </div>
    
</html>
