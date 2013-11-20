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
        ${output_zone_links("", "lighting")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>External Lighting</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/outside/lighting/gardenpath"
                            wbSource="/eventstate/to_ui/outside/lighting/gardenpath"
                            >
                        Garden Path
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/outside/lighting/housepath"
                            wbSource="/eventstate/to_ui/outside/lighting/housepath"
                            >
                        House Path 
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/outside/lighting/decking"
                            wbSource="/eventstate/to_ui/outside/lighting/decking"
                            >
                        Decking
                    </wb:simpleButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/outside/lighting/kitchen"
                            wbSource="/eventstate/to_ui/outside/lighting/kitchen"
                            >
                        Kitchen Door
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/outside/lighting/office"
                            wbSource="/eventstate/to_ui/outside/lighting/office"
                            >
                        Office Door
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/outside/lighting/summerhouse"
                            wbSource="/eventstate/to_ui/outside/lighting/summerhouse"
                            >                            
                        Out House
                    </wb:simpleButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton 
                            wbTarget="/sendevent/from_ui/outside/lighting/mower"
                            wbSource="/eventstate/to_ui/outside/lighting/mower"
                            >
                        Mower Store
                    </wb:simpleButton>
                </td>
            </tr>
            
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- !Insert content for bottom right box in here -->
        ${output_functional_links( "", "lighting", [True,True,True,True,True] )}
    </div>

</html>
