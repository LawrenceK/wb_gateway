<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
import zone_embed

layout_params['selected_tab'] = 1
# This sets the pooling period of widgets to 30 sec
layout_params['custom_poller'] = 30
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="zone_embed,WebBrickGateway.templates.widgets_tabbed">


    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">

        <div class="controls_top_area" >
            
            ${output_system_status()}
            <div class="occupancy_buttons">
                <wb:simpleButton wbTarget="/sendevent/occupants/areaway">
                    Set Away
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/occupants/arehome">
                    Set at Home
                </wb:simpleButton>
            </div>
        </div>    
        <div class="controls_top_area" >
            ${output_zone_button( "zone2", "heating", "Central Heating"  )}
            ${output_zone_button( "zone1", "hotwater", "Hot Water"  )}
            ${output_zone_button( "zone3", "towelrail", "Towel Rail"  )}
        </div>
    </div>
    
</html>
