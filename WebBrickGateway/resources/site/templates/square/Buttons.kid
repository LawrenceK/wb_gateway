<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Buttons Example")}

<body>

${output_nav("Buttons")}
  
<table>
    <tr>
        <wb:flashButton
                width='200px' height='200px'
                wbTarget='/wbcmd/UnNamed/DI/0'
                wbSource='/wbsts/UnNamed/DO/0'
                title="SimpleISOButton"
                flashMovie="SimpleISOButton.swf"
            />
        <wb:flashButton
                width='200px' height='200px'
                wbTarget='/wbcmd/UnNamed/DI/1'
                wbSource='/wbsts/UnNamed/DO/1'
                title="SimpleISOButton2"
                flashMovie="SimpleISOButton2.swf"
            />
        <wb:flashButton
                width='200px' height='200px'
                wbTarget='/wbcmd/UnNamed/DI/2'
                wbSource='/wbsts/UnNamed/DO/2'
                title="ButtonTemplate"
                flashMovie="ButtonTemplate.swf"
            />
    </tr>
</table>

${output_site_info_bar()}

</body>
</html>
