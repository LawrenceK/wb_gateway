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
                <td colspan="2" style="margin-left:5px; text-align:left"><h1>Heat Recovery Overview</h1></td>
            </tr>
            <tr>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
                            width="100px"
                            height="100px"
            				wbSource='/eventstate/general/ventilation/fan/stale/speed'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="65"
                            sethigh="85"
                            labels="0,25,50,75,100"
                            prefix="" 
            				format="##.#" 
            				postfix="%"
                            metertitle="Stale Air"
                            flashMovie='MeterRadial270.swf'
                            >
            			Stale Air
            		</wb:flashMeter>
                </td>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/general/ventilation/requestBoost">
                        Boost
                    </wb:simpleButton>
                </td>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
                            width="100px"
                            height="100px"
            				wbSource='/eventstate/general/ventilation/fan/fresh/speed'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="65"
                            sethigh="85"
                            labels="0,25,50,75,100"
                            prefix="" 
            				format="##.#" 
            				postfix="%"
                            metertitle="Fresh Air"
                            flashMovie='MeterRadial270.swf'
                            >
            			Fresh Air
            		</wb:flashMeter>
                </td>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/general/ventilation/fan/target/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=0"
                            wbSource="/eventstate/to_ui/general/ventilation/fan/speed/stop">
                        Stop
                    </wb:simpleButton>
                </td>
            </tr>    
            <tr>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/general/ventilation/fan/target/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=1"
                            wbSource="/eventstate/to_ui/general/ventilation/fan/speed/low">
                        Low Speed
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/general/ventilation/fan/target/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=2"
                            wbSource="/eventstate/to_ui/general/ventilation/fan/speed/medium">
                        Medium Speed
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/general/ventilation/fan/target/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=3"
                            wbSource="/eventstate/to_ui/general/ventilation/fan/speed/high">
                        High Speed
                    </wb:simpleButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Configuration:</div></td>
            </tr>

            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/general_heatrecovery_config"  
                            >
                        General Config
                    </wb:simpleLinkButton>
                </td>
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
