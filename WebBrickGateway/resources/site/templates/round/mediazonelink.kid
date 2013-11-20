<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['left_title'] = ""
layout_params['top_title'] = " "
layout_params['show_bottom'] = False
?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="WebBrickGateway.templates.widgets_round">
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <ul class="divider29px">
            <li>
                <wb:simpleLinkList target="/media/client?rid=${rid}" 
                    iconimage="funcicons/funciconaudio.png"
                    py:content='"Sonos %s" %(name)'/>
            </li>
            <li py:for='k in clients'>
                <wb:simpleLinkList target="/media/client?rid=${k}" 
                    iconimage="funcicons/funciconaudio.png"
                    py:content='"Sonos %s" %(clients[k])'/>
            </li>
<!--    
            <li py:for='k in clients'>
                <wb:simpleLinkList target="/media/zonelink?rid=${k}"
                    py:content='"Sonos %s" %(clients[k])'/>
            </li>
-->        
        </ul>
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1 py:content='"Link zones to %s" %(name)'>Zone Name</h1>
        <table>
            <tr py:for='k in clients'>
                <wb:simpleButton py:for='k in clients'
                    wbTarget='/media/dozonelink?rid=${rid}&amp;target=${k}'
                    py:content='clients[k]'/>
            </tr>
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
    </div>


</html>
