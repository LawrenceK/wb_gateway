<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("This is the Page Title")}


<body>

${output_nav("This is displayed in the Gateway header")}


<!-- Any content for the page should go here (in between the header and footer) --> 


${output_site_info_bar()} <!-- This will display the Gateway footer-->

</body>
</html>
