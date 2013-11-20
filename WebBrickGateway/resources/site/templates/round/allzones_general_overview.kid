<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
layout_params['left_title'] = "Zones"
layout_params['top_title'] = ""
?>
<!-- ! This is a secondary Welcome page, but with all zones being displayed! Only difference to welcome.kid is in line 15-->
<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'sitelayout3.kid'" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        ${output_zone_links_all("", "general")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>Welcome to your WebBrick Systems Gateway</h1>
            
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <td colspan="3">
                    <div style="margin-left:16px; ">
                        This is your home page and it can be customised by your installer to show you the information that is most important to you.
                    </div>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Global Controls:</div></td>
            </tr>
            <tr>
                <td>
                    <wb:simpleButton wbTarget="/sendevent/occupants/areaway">
                        Sleep House
                    </wb:simpleButton>
                </td>
                <td>
                    <wb:simpleButton wbTarget="/sendevent/occupants/arehome">
                        Wake House
                    </wb:simpleButton>
                </td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="2"><div style="margin-left:16px; text-align:left ">Temperature:</div></td>
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
                
            </tr>
            
        </table>
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        ${output_functional_links( "", "",[True,True,True,True,True] )}
    </div>

</html>
