<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
layout_params['left_title'] = "ZonePlayers"
layout_params['show_top'] = True
layout_params['show_bottom'] = False
?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="WebBrickGateway.templates.widgets_round">
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <ul class="divider29px">
            <li py:for='k in clients'>
                <wb:simpleLinkList target="/media/client?rid=${k}" iconimage="funcicons/funciconaudio.png">
                    ${clients[k]}
                </wb:simpleLinkList>

            </li>
        </ul>
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <!-- Insert content for top right box in here -->
        &nbsp;
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- Insert content for bottom right box in here -->
        &nbsp;
    </div>

</html>
