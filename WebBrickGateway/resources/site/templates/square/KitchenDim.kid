<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">


${output_head("Kitchen Dimmer Example")}

<body>

${output_nav("Kitchen Dimmers")}
  
<table>
    <tr>
        <td align='center' width='240px' height='240px'
                             wbType="FlashMeter" 
                             wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                             wbSource='/wbsts/house1/AO/0'
                             minvalue="0"
                             maxvalue="100"
                             curvalue="0"
                             setlow="0"
                             sethigh="100"
                             metertitle="Ceiling"
                             labels='/wbcmd/house1/AA/0/'
                             flashMovie="/static/flash/TestDimmer.swf"
                            >
        </td>
        <td align='center' width='240px' height='240px'
                             wbType="FlashMeter" 
                             wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                             wbSource='/wbsts/house1/AO/1'
                             minvalue="0"
                             maxvalue="100"
                             curvalue="0"
                             setlow="0"
                             sethigh="100"
                             metertitle="Wall"
                             labels='/wbcmd/house1/AA/1/'
                             flashMovie="/static/flash/TestDimmer.swf"
                            >
        </td>
    </tr>
</table>

${output_site_info_bar()}

</body>
</html>
