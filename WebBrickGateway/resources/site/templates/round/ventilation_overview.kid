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
layout_params['itouch_icon'] = "funciconventilation.png"

?>

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
                <td colspan="2" style="margin-left:5px; text-align:left"><h1>Ventilation Overview</h1></td>
            </tr>
            <tr>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
            				wbSource="/eventstate/temperature/outside" 
            				prefix="" 
            				format="##.#" 
                            minvalue="-10"
                            maxvalue="40"
                            curvalue="0"
                            setlow="-10"
                            sethigh="100"
                            width="100px"
                            height="100px"
                            labels="-10, 0,10,20,30,40"
                            flashMovie='MeterRadial270.swf'
            				postfix="&ordm;C">
            			Outside
            		</wb:flashMeter>
                </td>
                <td>
                    <wb:enableEntryButton
                            baseClassName="entry"
                            stateVals="Blank,Tick"
                            wbTitle="Enable HRV"
                            wbSource='/eventstate/general/ventilation/fan/enabled'
                            wbTarget='/sendevent/general/ventilation/fan/enabled?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="HRV Enabled"
                            >
                        &nbsp;
                    </wb:enableEntryButton>
                </td>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
                            width="100px"
                            height="100px"
            				wbSource='/eventstate/general/ventilation/fan/speed'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="65"
                            sethigh="85"
                            labels="0,25,50,75,100"
                            prefix="" 
            				format="##.#" 
            				postfix="%"
                            metertitle="Fan Speed"
                            flashMovie='MeterRadial270.swf'
                            >
            			Fan Speed
            		</wb:flashMeter>
                </td>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/general/ventilation/boost"
                            wbSource="/eventstate/to_ui/general/ventilation/boost">
                        Boost
                    </wb:simpleButton>
                </td>
            </tr>    
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Further Information:</div></td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="3">
                    <div style="margin-left:16px; text-align:left ">
                        Your installer can configure this page to show details of single Ventilation Zones, if you do not have a HRV Unit installed.
                    </div>
                </td>
            </tr>
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "ventilation", [True,True,True,True,True] )}
    </div>

</html>
