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
layout_params['itouch_icon'] = "funciconheating.png"

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
                
            HVR = True
        ?>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <td colspan="2" style="margin-left:5px; text-align:left"><h1>Heating Overview</h1></td>
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
                    <wb:simpleLinkButton 
                            target="/template/earlystart_overview"  
                            >
                        Early Start
                    </wb:simpleLinkButton>
                </td>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
            				wbSource="/eventstate/zone1/sensor" 
            				prefix="" 
            				format="##.#" 
                            minvalue="5"
                            maxvalue="65"
                            curvalue="0"
                            setlow="5"
                            sethigh="65"
                            width="100px"
                            height="100px"
                            labels="5,20,35,50,65"
                            flashMovie='MeterRadial270.swf'
            				postfix="&ordm;C">
            			Hot Water
            		</wb:flashMeter>
                </td>
            </tr>
            <tr>
                <td>
                    <wb:simpleLinkButton 
                            target="/template/weathercomp_overview"  
                            >
                        Weather Comp
                    </wb:simpleLinkButton>
                </td>
            </tr>    
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Heatsource Status:</div></td>
            </tr>
            <span py:for='hsBase in range(1,heatSourceLimit,3)' py:strip='True'>
                <tr>
                    <td py:for='hs in range(hsBase,min( (hsBase+3),heatSourceLimit),1)'>
                        <wb:simpleIndicatorButton
                            wbLoad="loadButton()"
                            wbSource='/eventstate/heatsource/${hs}/state?attr=val' 
                            baseClassName="indicator">
                            ${output_current_value( "/eventstate/heatsource/%s/availability?attr=name"%hs ) }
                        </wb:simpleIndicatorButton> 
                    </td>  
                    <!-- ! This is for HVR display, set HVR to false to disable -->
                    <td py:if='hsBase+3 &gt; heatSourceLimit and HVR'>
                        <wb:simpleLinkButton 
                                target="/template/heatrecovery_overview"  
                                >
                            Heat Recovery
                        </wb:simpleLinkButton>
                    </td>
                </tr>
                <!-- ! This is for HVR display, set HVR to false to disable -->
                <tr py:if='hsBase+3 == heatSourceLimit and HVR'>
                    <td >
                        <wb:simpleLinkButton 
                                target="/template/heatrecovery_overview"  
                                >
                            Heat Recovery
                        </wb:simpleLinkButton>
                    </td>
                </tr>     
                
            </span>
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "heating", [True,True,True,True,True] )}
    </div>

</html>
