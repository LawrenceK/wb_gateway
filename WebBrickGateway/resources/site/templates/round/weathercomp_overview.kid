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
        <h1>Weather Compensation</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            
            <tr>
                <td><div style="margin-left:16px">Basic Configuration:</div></td>
            </tr>
            <tr>
                <td >
                    <wb:simpleIndicatorButton
                        wbLoad="loadButton()"
                        wbSource="/eventstate/weather/1/?attr=istate"  
                        stateVals="Suppress,WillRun"
                        baseClassName="indicator">
                        Weather 1
                    </wb:simpleIndicatorButton>
                </td>
                <td >
                    <wb:simpleIndicatorButton
                        wbLoad="loadButton()"
                        wbSource="/eventstate/weather/2/?attr=istate" 
                        stateVals="Suppress,WillRun"
                        baseClassName="indicator">
                        Weather 2
                    </wb:simpleIndicatorButton>
                </td>
                <td >
                    <wb:simpleIndicatorButton
                        wbLoad="loadButton()"
                        wbSource="/eventstate/weather/3/?attr=istate"  
                        stateVals="Suppress,WillRun"
                        baseClassName="indicator">
                        Weather 3
                    </wb:simpleIndicatorButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px">Outside Temperature Thresholds:</div></td>
            </tr>
            <tr>
                <td>
                    <wb:numericEntryButton 
                        wbSource="/eventstate/weather/1/rising/outsideThreshold" 
                        wbTarget="/sendevent/weather/1/rising/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Rising: " 
                        format="##.#" 
                        postfix="&ordm;C">
                    &nbsp;
                    </wb:numericEntryButton>
                </td>
                <td>
                    <wb:numericEntryButton 
                        wbSource="/eventstate/weather/2/rising/outsideThreshold" 
                        wbTarget="/sendevent/weather/2/rising/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Rising: " 
                        format="##.#" 
                        postfix="&ordm;C">
                    &nbsp;
                    </wb:numericEntryButton>
                </td>
                <td>
                    <wb:numericEntryButton 
                        wbSource="/eventstate/weather/3/rising/outsideThreshold" 
                        wbTarget="/sendevent/weather/3/rising/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Rising: " 
                        format="##.#" 
                        postfix="&ordm;C">
                    &nbsp;
                    </wb:numericEntryButton>
                </td>
            </tr>
            <tr>
                <td>
                    <wb:numericEntryButton 
                        wbSource="/eventstate/weather/1/falling/outsideThreshold" 
                        wbTarget="/sendevent/weather/1/falling/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Falling: " 
                        format="##.#" 
                        postfix="&ordm;C">
                    &nbsp;
                    </wb:numericEntryButton>
                </td>
                <td>
                    <wb:numericEntryButton 
                        wbSource="/eventstate/weather/2/falling/outsideThreshold" 
                        wbTarget="/sendevent/weather/2/falling/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Falling: " 
                        format="##.#" 
                        postfix="&ordm;C">
                    &nbsp;
                    </wb:numericEntryButton>
                </td>
                <td>
                    <wb:numericEntryButton 
                        wbSource="/eventstate/weather/3/falling/outsideThreshold" 
                        wbTarget="/sendevent/weather/3/falling/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Falling: " 
                        format="##.#" 
                        postfix="&ordm;C">
                    &nbsp;
                    </wb:numericEntryButton>
                </td>
            </tr>                
            
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "heating", [True,True,True,True,True] )}
    </div>

</html>
