<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['left_title'] = ""
layout_params['show_left'] = True
layout_params['top_title'] = ""
layout_params['show_top'] = True
layout_params['show_bottom'] = True

?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <!-- Insert content for left box in here -->
        Left Content
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <!-- Insert content for top right box in here -->
        Top Content
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- Insert content for bottom right box in here -->
        Bottom Content
    </div>

</html>
