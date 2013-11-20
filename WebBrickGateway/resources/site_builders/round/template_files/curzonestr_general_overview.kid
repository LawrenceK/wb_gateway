<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['left_title'] = "Zones"
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'sitelayout3.kid'" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">

        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        ${output_zone_links("curzonestr", "general")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>curzonetitle Overview</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px">Lighting:</div></td>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/curzonestr/lighting/main/off"
                            wbSource="/eventstate/to_ui/curzonestr/lighting/main/state">
                        Lights Off
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton wbTarget="/sendevent/from_ui/curzonestr/lighting/main/low">
                        Lights Low
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton wbTarget="/sendevent/from_ui/curzonestr/lighting/main/high">
                        Lights Full
                    </wb:simpleButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px">Heating:</div></td>
            </tr>
            <tr>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
            				wbSource="/eventstate/zonekey/sensor?attr=val" 
            				prefix="" 
            				format="##.#" 
                            minvalue="5"
                            maxvalue="45"
                            curvalue="0"
                            setlow="15"
                            sethigh="35"
                            width="100px"
                            height="100px"
                            labels="5,15,25,35,45"
                            flashMovie='MeterRadial270.swf'
            				postfix="&ordm;C">
            			Temp
            		</wb:flashMeter>
                </td>
                <td>
                    <wb:numericEntryButton 
                            wbSource="/eventstate/zonekey/state?attr=targetsetpoint"
                            wbTarget="/sendevent/zonekey/manual/set?type=http://id.webbrick.co.uk/events/zones/manual"
                            prefix="Target: " 
                            format="##.#" 
                            postfix="&ordm;C"
                            >
                        &nbsp;
                    </wb:numericEntryButton>
                </td>
            </tr>
        </table>
                       
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        ${output_functional_links( "curzonestr", "general", [availfunctionlist] )}
    </div>

</html>
