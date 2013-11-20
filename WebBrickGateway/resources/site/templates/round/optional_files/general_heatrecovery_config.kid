<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
import zone_lists
import zoneControl_embed

layout_params['left_title'] = "Zones"
layout_params['show_left'] = True
layout_params['show_top'] = True
layout_params['show_bottom'] = True
layout_params['itouch_icon'] = "funciconventilation.png"

?>

<!-- !  This requires HRV to be setup in event despatch, with the following files:
            heatrecovery_ventilation_inputs.xml
            heatrecovery_ventilation_outputs.xml 
            -->

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="zone_lists, zoneControl_embed, WebBrickGateway.templates.widgets_round">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <!-- !Insert content for left box in here -->
        ${output_zone_links("", "ventilation")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <!-- !Insert content for top right box in here -->
        
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <td colspan="2" style="margin-left:5px; text-align:left"><h1>Heat Recovery Configuration</h1></td>
            </tr>
            <tr>
                <td><div style="margin-left:16px">Operating Options:</div></td>
                <td> </td>           
                <td><div style="margin-left:16px"></div></td>        
            </tr>

            <tr>
                <td>
                    <wb:enableEntryButton
                            baseClassName="entry"
                            stateVals="Blank,Tick"
                            wbTitle="Enable HRV"
                            wbSource='/eventstate/general/ventilation/hrv/enabled'
                            wbTarget='/sendevent/general/ventilation/hrv/enabled?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="HRV Enabled"
                            >
                        &nbsp;
                    </wb:enableEntryButton>
                </td>
                <td>
                    <wb:enableEntryButton
                            baseClassName="entry"
                            stateVals="Blank,Tick"
                            wbTitle="Enable Stale Air"
                            wbSource='/eventstate/general/ventilation/fan/stale/enabled'
                            wbTarget='/sendevent/general/ventilation/fan/stale/enabled?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="Stale Air Fan"
                            >
                        &nbsp;
                    </wb:enableEntryButton>
                </td>
                <td>
                    <wb:numericEntryButton 
                            wbSource='/eventstate/general/ventilation/boost/runtime'
                            wbTarget='/sendevent/general/ventilation/boost/runtime?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="Run Time: " 
                            format="#" 
                            postfix=" sec"
                            >
                        &nbsp;
                    </wb:numericEntryButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Further Configuration:</div></td>
            </tr>

            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/general_heatrecovery_pirconfig"  
                            >
                        PIR Config
                    </wb:simpleLinkButton>
                </td>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/general_heatrecovery_humconfig"  
                            >
                        Humidity Config
                    </wb:simpleLinkButton>
                </td>
                
            </tr>
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "ventilation", [True,True,True,True,True] )}
    </div>

</html>
