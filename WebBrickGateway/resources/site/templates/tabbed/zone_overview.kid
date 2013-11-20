<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python

kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
import zone_embed

layout_params['selected_tab'] = 1

?>

<html   xmlns="http://www.w3.org/1999/xhtml"
        xmlns:py="http://purl.org/kid/ns#"
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="sitelayout.kid"
        py:extends="zone_embed,WebBrickGateway.templates.widgets_tabbed">

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}tabcontent'" id="tabcontent">

<?python
from WebBrickGateway.templates.widgets_tabbed import getCurrentValue
if not 'zone_key' in locals(): zone_key = 'zone1' 
zone_string = zone_key
zone_name = getCurrentValue("/eventstate/%s/name?attr=name"%zone_key) 
max_temp = getCurrentValue("/eventstate/%s/params?attr=max_temp"%zone_key)
min_temp = getCurrentValue("/eventstate/%s/params?attr=min_temp"%zone_key)
cool_point = getCurrentValue("/eventstate/%s/params?attr=cool_point"%zone_key)
hot_point = getCurrentValue("/eventstate/%s/params?attr=hot_point"%zone_key)
?>
        ${output_zone_spinner( zone_key, zone_string, zone_name, min_temp, max_temp  )}
        <!-- the right hand side -->

        ${output_zone_status( zone_key, zone_string, zone_name )}

        <div class="zone_control_buttons">
            <wb:simpleButton wbTarget="/sendevent/${zone_key}/enabled?type=http://id.webbrick.co.uk/events/config/set&amp;val=1">
                Enable &nbsp; Zone
            </wb:simpleButton>
            <wb:simpleButton wbTarget="/sendevent/${zone_key}/enabled?type=http://id.webbrick.co.uk/events/config/set&amp;val=0">
                Disable Zone
            </wb:simpleButton>
        </div>
    </div>

</html>

