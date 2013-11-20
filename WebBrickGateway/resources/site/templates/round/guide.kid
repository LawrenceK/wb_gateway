<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['left_title'] = ""
layout_params['show_left'] = True
layout_params['top_title'] = ""
layout_params['show_top'] = True
layout_params['show_bottom'] = False

?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <div>
            <ul class="divider29px">
                <li>
                    <wb:simpleLinkList 
                            target="/template/guide_basic_operations" 
                            iconimage="">
                        Basic Operations
                    </wb:simpleLinkList>
                </li>
                <li>
                    <wb:simpleLinkList 
                            target="/template/guide_occupancy" 
                            iconimage="">
                        Occupancy
                    </wb:simpleLinkList>
                </li>
                <li>
                    <wb:simpleLinkList 
                            target="/template/guide_intelligent_heating" 
                            iconimage="">
                        Intelligent Heating
                    </wb:simpleLinkList>
                </li>
                <li>
                    <wb:simpleLinkList 
                            target="/template/guide_doors" 
                            iconimage="">
                        Garage Doors
                    </wb:simpleLinkList>
                </li>
            </ul>
        </div>
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
         <h1>WebBrick Systems Gateway Users Guide</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="3">
                    <div style="margin-left:16px">
                        An updated User Guide for the Gateway will be made available with the next formal release. 
                    </div>
                </td>
            </tr>
            
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
    </div>

</html>
