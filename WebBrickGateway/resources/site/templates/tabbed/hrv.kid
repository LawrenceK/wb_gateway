<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
import zone_embed

layout_params['selected_tab'] = 4
# This sets the pooling period of widgets to 30 sec
layout_params['custom_poller'] = 30
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid" 
        py:extends="zone_embed,WebBrickGateway.templates.widgets_tabbed">


    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">      
            <div class="hrv_mode">
            <br/>
            <b><div style="margin-bottom:-10px; font-size:20px"><wb:textDisplay wbSource="/eventstate/hrv/current/mode?attr=mode" prefix="Current Status: "></wb:textDisplay></div></b>
            <br/>
            <i><wb:textDisplay wbSource="/eventstate/hrv/normal/speed?attr=string" prefix="Normal Setpoint: "></wb:textDisplay></i>
                <wb:simpleButton wbTarget="/sendevent/hrv/normal/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=0">
                    Manual
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/normal/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=1">
                    Low
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/normal/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=2">
                    Medium
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/normal/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=3">
                    High
                </wb:simpleButton>
            </div>
            <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            <div class="hrv_mode">
            <i><wb:textDisplay wbSource="/eventstate/hrv/cooling/speed?attr=string" prefix="Cooling Setpoint: "></wb:textDisplay></i>
                <wb:simpleButton wbTarget="/sendevent/hrv/cooling/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=0">
                    Manual
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/cooling/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=1">
                    Low
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/cooling/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=2">
                    Medium
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/cooling/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=3">
                    High
                </wb:simpleButton>
            </div>
            <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            <div class="hrv_mode">
            <i><wb:textDisplay wbSource="/eventstate/hrv/night/speed?attr=string" prefix="Night Setpoint: "></wb:textDisplay></i>
                <wb:simpleButton wbTarget="/sendevent/hrv/night/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=0">
                    Manual
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/night/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=1">
                    Low
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/night/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=2">
                    Medium
                </wb:simpleButton>
                <wb:simpleButton wbTarget="/sendevent/hrv/night/speed?type=http://id.webbrick.co.uk/events/config/set&amp;val=3">
                    High
                </wb:simpleButton>
            </div>
    </div>
    
</html>
