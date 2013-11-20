<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Halogen Light Control")}

<body>

${output_nav("Halogen Light Dimming")}
  
<table>
    <tr>
        <wb:flashButton width='360px' height='360px'
                wbSource='/wbsts/house1/AO/3'
                wbTarget='/wbcmd/house1/AA/3/'
                title='Light'
                flashMovie="/static/flash/OrnateDimmer.swf">
        </td>
    </tr>
</table>

${output_site_info_bar()}

</body>
</html>
