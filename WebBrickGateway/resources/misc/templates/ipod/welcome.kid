<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master_no_td
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master_no_td">

${output_head("Home page for the Webbrick Gateway - Samples1")}
<!-- <link href="/static/css/wl-panel.css" rel="stylesheet" /> -->

<body>

${output_nav("Webbrick Gateway")}

<table class="navTable">
    <colgroup span="4" width="25%"></colgroup>

    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Rooms</td>
    </tr>

    <tr>
        <td>
            <wb:simpleLink target="/template/downstairs">Kitchen and Lounge</wb:simpleLink>
        </td>
        <td>
            <wb:simpleLink target="/template/upstairs">Bedrooms</wb:simpleLink>
        </td>
        <td>
            <wb:simpleLink target="/template/garage">Garage</wb:simpleLink>
        </td>
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Heating</td>
    </tr>
    <tr>
        <td>
            <wb:simpleLink target="/template/heating">Heating</wb:simpleLink>
        </td>
        <td>
            <wb:simpleLink target="/template/zones">Multi Zone</wb:simpleLink>
        </td>
        <td>
            <wb:simpleLink target="/template/homeInt">Home intelligence</wb:simpleLink>
        </td>
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Audio/Video</td>
    </tr>
    <tr>
        <td>
            <wb:simpleLink target="/media">Music</wb:simpleLink>
        </td>
    </tr>
</table>

<table class="navTable">
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Tools</td>
    </tr>
    <tr>
        <td>
            <wb:simpleLink target="/wbsts/known">Known WebBricks</wb:simpleLink>
        </td>
        <td>
            <wb:simpleLink target="/wbcnf">WebBrick Configuration manager</wb:simpleLink>
        </td>
   </tr>

</table>

${output_site_info_bar()}

</body>
</html>
