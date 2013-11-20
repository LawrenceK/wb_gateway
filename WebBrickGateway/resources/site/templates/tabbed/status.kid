<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
import status_embed

layout_params['selected_tab'] = 2
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="status_embed,WebBrickGateway.templates.widgets_tabbed">

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">
        <!--             zone_key ,  css_id     ,  zone_name  -->
        ${output_status( "zone2"  ,  "heating"  ,  "Heating"   )}
        ${output_status( "zone1"  ,  "hotwater" ,  "Hot Water" )}
    </div>
    
</html>
