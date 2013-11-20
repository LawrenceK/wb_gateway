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

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="zone_lists, zoneControl_embed, WebBrickGateway.templates.widgets_round">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <!-- !Insert content for left box in here -->
        ${output_zone_links("", "heating")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <!-- !Insert content for top right box in here -->
        <?python 
            heatSourceLimit = WebBrickGateway.templates.widgets_round.getCurrentValue( "/eventstate/heatsource/count" )
            if heatSourceLimit == '':
                heatSourceLimit = 0
            else:
                heatSourceLimit = int(heatSourceLimit) + 1
        ?>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <td colspan="2" style="margin-left:5px;"><h1>Early Start Overview</h1></td>
            </tr>
            <tr>
                <td><div style="margin-left:16px">Basic Configuration:</div></td>
            </tr>
            <tr>
                <td>
                    <wb:timeEntryButton  
                        wbSource="/eventstate/earlystart/time?attr=time"
                        wbTitle="Earlystart Time" 
                        wbTarget="/sendevent/earlystart/time?type=http://id.webbrick.co.uk/events/config/set"
                        noPolling="yes">
                        &nbsp;
                    </wb:timeEntryButton>
                </td>
                <td>
                    <wb:simpleButton  
                        wbLoad="loadButton()"
                        wbTarget="/sendevent/earlyStart/enable" >
                        Enable
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton 
                        wbLoad="loadButton()"
                        wbTarget="/sendevent/earlyStart/disable" >
                        Disable
                    </wb:simpleButton>
                </td>
            </tr>
            <tr>
                <td>&nbsp;</td>
            </tr>
            <tr>
                <td><div style="margin-left:16px">Early Start Package:</div></td>
            </tr>
            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/earlystart_package"  
                            >
                        View Package
                    </wb:simpleLinkButton>
                </td>
            </tr>    
            
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "heating", [True,True,True,True,True] )}
    </div>

</html>
