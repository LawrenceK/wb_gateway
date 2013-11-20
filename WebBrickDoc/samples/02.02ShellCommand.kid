<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Shell Command")}

<body>

${output_nav("Shell Command")}

<table>
	<colgroup span="4" width="25%"></colgroup>
	<tr>
        <wb:caption colspan="2">Shell Command</wb:caption>
	</tr>
	<tr>
        <wb:simpleButton wbTarget="/sendevent/command/restart" >
            Restart gateway
        </wb:simpleButton>
	</tr>
</table>

${output_site_info_bar()}

</body>

</html>
