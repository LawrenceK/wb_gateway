<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master, 'zoneControl_embed.kid'">
    
<!-- zoneNumber would in as ${zoneNumber} -->

${output_head("Zone Control")}

<body>

${output_nav(output_zone_name("4"))}

${output_zone_control( "4" )}

${output_site_info_bar()}

</body>

</html>
