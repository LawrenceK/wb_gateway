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
layout_params['itouch_icon'] = "funciconsecurity.png"

?>

<!-- ! remove wbcmd from some parts of this page -->

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="zone_lists, zoneControl_embed, WebBrickGateway.templates.widgets_round">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <!-- !Insert content for left box in here -->
        ${output_zone_links("", "security")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>Security Overview</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <td colspan="1"><div style="text-align:left ">Gate: </div></td>
                <td colspan="1"><div style="text-align:left ">Drive:</div></td>
                <td colspan="1"><div style="text-align:left ">Front:</div></td>
            </tr>
            <tr>
                <td>
            		<img src="/redirect/FrontGateCam" width="160" height="131" />
            	</td>
            	<td>
            		<img src="/redirect/SharedDriveCam" width="160" height="131" />
            	</td>
            	<td>
            		<img src="/redirect/FrontofHouseCam" width="160" height="131" />
            	</td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Gate:</div></td>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton 
                            wbSource="/eventstate/gate/state" 
                            stateVals="Ajar,Closed,Open,Error"
                            wbTarget="/wbcmd/maincab2/DI/4" 
                            baseClassName="gate"> 
                            Open Gate
                    </wb:simpleButton>    
                </td>
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
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "security", [True,True,True,True,True] )}
    </div>

</html>
