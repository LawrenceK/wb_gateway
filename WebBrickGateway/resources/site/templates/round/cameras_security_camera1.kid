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
        <h1>Gate Camera</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <td colspan="2" rowspan="3">
                     <img src="/redirect/FrontGateCam" width="220" height="180" />
                </td>
                <td>
                    <wb:simpleButton 
                            wbSource="/eventstate/gate/state" 
                            stateVals="Ajar,Closed,Open,Error"
                            wbTarget="/wbcmd/maincab2/DI/4" 
                            baseClassName="gate"> 
                            Open Gate
                    </wb:simpleButton>    
                </td>
            </tr>
            <tr>
                <td>
                    <wb:enableEntryButton
                            baseClassName="entry"
                            stateVals="Blank,OK"
                            wbTitle="Auto Override"
                            wbSource="/eventstate/gate/enabled"
                            wbTarget="/sendevent/gate/enabled?type=http://id.webbrick.co.uk/events/config/set"
                            prefix="Auto Override"
                            />
                </td>
            </tr>
            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/gate_general_schedule"  
                            >
                        Edit Schedule
                    </wb:simpleLinkButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Further Cameras:</div></td>
            </tr>
            <tr>
                <td>
                    &nbsp;
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_overview"  
                            >
                        Camera Overview
                    </wb:simpleLinkButton>
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/cameras_security_camera2"  
                            >
                        Drive
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
