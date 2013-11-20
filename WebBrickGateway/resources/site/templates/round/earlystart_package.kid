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
            zoneLimit = WebBrickGateway.templates.widgets_round.getCurrentValue( "/eventstate/zone/count" )
            if zoneLimit == '':
                zoneLimit = 0
            else:
                zoneLimit = int(zoneLimit) + 1
        ?>


        <h1>Early Package</h1> 
        <table id="scheduleboxtable">
            <span py:for='zoneNr in range(1,zoneLimit,1)' py:strip='True'>
                <tr py:if='WebBrickGateway.templates.widgets_round.getCurrentValue( "/eventstate/zone%s/earlystart/enabled"%zoneNr ) == "1"' >
                    <td class="buttoncapleft"/>
                        
                    <td class="buttonbody">
                        ${output_current_value( '/eventstate/zone%s/name?attr=name'%zoneNr ) }
                    </td>
                    <td class="buttonbody">
                        <wb:numericEntry
                                colspan='1'
                                wbSource="/eventstate/zone${zoneNr}/earlystart/setpoint"
                                wbTarget="/sendevent/zone${zoneNr}/earlystart/setpoint?type=http://id.webbrick.co.uk/events/config/set"
                                prefix="Target: " 
                                format="##.#" 
                                postfix="&ordm;C"
                                wbTitle="Set Point">
                                Set Point
                        </wb:numericEntry>
                    </td>
                        
                    
                    <td class="buttoncapright"/>
                </tr>
            </span>   
        </table>
           
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "heating", [True,True,True,True,True] )}
    </div>

</html>
