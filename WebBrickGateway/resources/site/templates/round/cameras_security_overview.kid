<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
import zone_lists
import zoneControl_embed

layout_params['left_title'] = "Zones"
layout_params['show_left'] = True
#layout_params['top_title'] = "Kitchen Heating Overview"
layout_params['show_top'] = True
#layout_params['bottom_title'] = "Kitchen Functions"
layout_params['show_bottom'] = True

?>

<!-- ! remove wbcmd from some parts of this page -->

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="zone_lists, zoneControl_embed, WebBrickGateway.templates.widgets_round">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <!-- !Insert content for left box in here -->
        ${output_zone_links("cameras", "security")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>Camera Overview</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera1"  
                            >
                        Gate
                    </wb:simpleLinkButton>
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera2"  
                            >
                        Drive
                    </wb:simpleLinkButton>
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera3"  
                            >
                        Front Garden
                    </wb:simpleLinkButton>
                </td>
            </tr>
           
            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera4"  
                            >
                        Rear Garden
                    </wb:simpleLinkButton>
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera5"  
                            >
                        Summer House
                    </wb:simpleLinkButton>
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera6"  
                            >
                        Front Door
                    </wb:simpleLinkButton>
                </td>
            </tr>
               
            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera7"  
                            >
                        Kitchen Door
                    </wb:simpleLinkButton>
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera8"  
                            >
                        Office
                    </wb:simpleLinkButton>
                </td>
            </tr>
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "cameras", "security", [True,True,True,True,True] )}
    </div>

</html>