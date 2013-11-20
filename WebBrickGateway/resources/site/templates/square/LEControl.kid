<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Low Energy Light Control")}

<body>

${output_nav("Low Energy Light Dimming")}
  
<table width="100%">
    <tr>
        <td width='360px' height='360px'
                            wbType="FlashButton" 
                            wbSource='/wbsts/house3/AO/3'
                            wbTarget='/wbcmd/house3/AA/3/'
							title='Light'
                            flashMovie="/static/flash/OrnateDimmer.swf"
                            >
        </td>
    </tr>
    <tr>
        <td width='280px' height='70px'
                            wbType="FlashButton" 
                            wbSource='/wbsts/house3/DO/0'
                            wbTarget='/wbcmd/house3/DO/0/toggle'
							title='LE Enable'
                            flashMovie="/static/flash/SimpleISOButton2.swf"
                            >
        </td>
    </tr>
</table>

${output_site_info_bar()}
</body>
</html>
