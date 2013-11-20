<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
import zone_lists
import zoneControl_embed

layout_params['left_title'] = "Zones"
layout_params['show_left'] = True
#layout_params['top_title'] = ""
layout_params['show_top'] = True
#layout_params['bottom_title'] = ""
layout_params['show_bottom'] = True
layout_params['itouch_icon'] = "funciconvideo.png"

?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="zone_lists, zoneControl_embed, WebBrickGateway.templates.widgets_round">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <!-- !Insert content for left box in here -->
        ${output_zone_links("", "video")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>Video Overview</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="3">
                    <div style="margin-left:16px; text-align:left ">
                        There are currently no global controls for Video control. Please discuss options for global Video controls with your installer.
                    </div>
                </td>
            </tr>
            
            
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "video", [True,True,True,True,True] )}
    </div>

</html>
