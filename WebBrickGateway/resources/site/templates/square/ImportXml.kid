<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Xml Import")}

<body>

${output_nav("Xml Import")}
<h1>/o2m8/svn/HomeGateway2/Trunk/WebBrickGateway/resources/samples1/templates/import.html</h1>
<div py:content="document('/o2m8/svn/HomeGateway2/Trunk/WebBrickGateway/resources/samples1/templates/import.html')"></div>

<h1>./resources/samples1/templates/import.html</h1>
<div py:content="document('./resources/samples1/templates/import.html')"></div>

${output_site_info_bar()}

</body>
</html>
