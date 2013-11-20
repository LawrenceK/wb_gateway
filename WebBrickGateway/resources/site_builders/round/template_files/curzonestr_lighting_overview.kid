<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
import zone_lists

layout_params['left_title'] = "Zones"

?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="zone_lists, WebBrickGateway.templates.widgets_round">
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <!-- Insert content for left box in here -->
        ${output_zone_links("curzonestr", "general")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>curzonetitle Lighting</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
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
                <td>
                    <wb:simpleButton wbTarget="/sendevent/from_ui/curzonestr/lighting/main/scene_up">
                        Scene Up
                    </wb:simpleButton>
                </td>
                <td colspan='2' rowspan='3' style="text-align:center">
                    <wb:flashDimmer width='150px' height='150px' 
                                wbSource='/eventstate/to_ui/curzonestr/lighting/main/level?attr=val'
                                wbTarget='/sendevent/from_ui/curzonestr/lighting/main/level?val='
                                meterTitle='Ceiling'
                                flashMovie="/static/flash/TestDimmer.swf">
                                Ceiling
                    </wb:flashDimmer>            
                </td>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton wbTarget="/sendevent/from_ui/curzonestr/lighting/main/scene_down">
                        Scene Down
                    </wb:simpleButton>
                </td>
                
                 
            </tr>
            
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <!-- Insert content for bottom right box in here -->
        ${output_functional_links( "curzonestr", "lighting",[availfunctionlist] )}
    </div>

</html>
