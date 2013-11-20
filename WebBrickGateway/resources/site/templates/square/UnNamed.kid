<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Page to access an UnNamed webbrick")}

<body>

${output_nav("UnNamed webbrick")}

<table class="navTable">
    <tr>
        <wb:simpleLink target="/template/verticalDim">verticalDim</wb:simpleLink>
        <wb:simpleLink target="/template/meters">meters</wb:simpleLink>
        <wb:simpleLink target="/template/buttons">buttons</wb:simpleLink>
        <wb:simpleLink target="/template/analogueControl">analogueControl</wb:simpleLink>
    </tr>
</table>

${output_site_info_bar()}

</body>
</html>
