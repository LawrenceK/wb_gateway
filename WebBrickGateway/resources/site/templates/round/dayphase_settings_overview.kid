<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
import zone_lists
import zoneControl_embed

layout_params['left_title'] = "Categories"
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
        <ul class="divider29px">
            <li>
                <wb:simpleLinkList 
                        target="/template/sunrise_settings_overview" 
                        iconimage="zoneicons/zoneiconlivingroom.png"
                        >
                    Sunrise / Sunset
                </wb:simpleLinkList>
            </li>
            <li>
                <wb:simpleLinkList 
                        target="/template/dayphase_settings_overview" 
                        iconimage="zoneicons/zoneiconlivingroom.png"
                        >
                    Day Phase
                </wb:simpleLinkList>
            </li>
            <li>
                <wb:simpleLinkList 
                        target="/template/occupancy_settings_overview" 
                        iconimage="zoneicons/zoneiconlivingroom.png"
                        >
                    Occupancy
                </wb:simpleLinkList>
            </li>
            <li>
                <wb:simpleLinkList 
                        target="/template/installertools_settings_overview" 
                        iconimage="zoneicons/zoneiconlivingroom.png"
                        >
                    Installer Tools
                </wb:simpleLinkList>
            </li>
            <li>
                <wb:simpleLinkList 
                        target="/template/reboot_settings_overview" 
                        iconimage="zoneicons/zoneiconlivingroom.png"
                        >
                    Reboot
                </wb:simpleLinkList>
            </li>
        </ul>
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <!-- !Insert content for top right box in here -->
        <h1>Day Phase Settings</h1>    
        <table id="scheduleboxtable">
            <tr>
                <th>&nbsp;</th>
                <th>Phase</th>
                <th>Description</th>
                <th>Time</th>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td class="buttoncapleft"/>
                <td class="buttonbody" >
                    Morning
                </td>
                <td class="buttonbody" >
                    Getting up, getting ready to go out
                </td>
                <td class="buttonbody">
                    <wb:timeEntry
                            wbSource="/eventstate/dayphase/weekday/morning?attr=time" 
                            wbTarget="/sendevent/dayphase/weekday/morning?type=http://id.webbrick.co.uk/events/config/set"
                            noPolling="yes">
                        &nbsp;
                    </wb:timeEntry>
                </td>
                <td class="buttoncapright"/>
                
            </tr>
            <tr>
                <td class="buttoncapleft"/>
                <td class="buttonbody" >
                    Day
                </td>
                <td class="buttonbody" >
                    Out at school, work, etc.
                </td>
                <td class="buttonbody">
                    <wb:timeEntry
                            wbSource="/eventstate/dayphase/weekday/day?attr=time" 
                            wbTarget="/sendevent/dayphase/weekday/day?type=http://id.webbrick.co.uk/events/config/set"
                            noPolling="yes">
                        &nbsp;
                    </wb:timeEntry>
                </td>
                <td class="buttoncapright"/>
                
            </tr>
            <tr>
                <td class="buttoncapleft"/>
                <td class="buttonbody" >
                    Evening
                </td>
                <td class="buttonbody" >
                    Coming home, eating, recreation, etc.
                </td>
                <td class="buttonbody">
                    <wb:timeEntry
                            wbSource="/eventstate/dayphase/weekday/evening?attr=time" 
                            wbTarget="/sendevent/dayphase/weekday/evening?type=http://id.webbrick.co.uk/events/config/set"
                            noPolling="yes">
                        &nbsp;
                    </wb:timeEntry>
                </td>
                <td class="buttoncapright"/>
                
            </tr>
            <tr>
                <td class="buttoncapleft"/>
                <td class="buttonbody" >
                    Night
                </td>
                <td class="buttonbody" >
                    Sleeping
                </td>
                <td class="buttonbody">
                    <wb:timeEntry
                            wbSource="/eventstate/dayphase/weekday/night?attr=time" 
                            wbTarget="/sendevent/dayphase/weekday/night?type=http://id.webbrick.co.uk/events/config/set"
                            noPolling="yes">
                        &nbsp;
                    </wb:timeEntry>
                </td>
                <td class="buttoncapright"/>
            </tr>
            <tr>
                <td>&nbsp;</td>
            </tr>
            <tr>
                <td>&nbsp;</td>
            </tr>
            <tr>
                <td class="buttoncapleft"/>
                <td class="buttonbody">&nbsp;</td>
                <td class="buttonbody">
                    <wb:textDisplay 
                        colspan="2" 
                        wbSource="/eventstate/time/dayphaseext?attr=dayphasetext" 
                        prefix="Current Day Phase: " postfix=""
                        >Left
                    </wb:textDisplay>
                </td>
                <td class="buttonbody">&nbsp;</td>
                <td class="buttoncapright"/>
            </tr>
        </table>
        
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "", [True,True,True,True,True] )}
    </div>

</html>

