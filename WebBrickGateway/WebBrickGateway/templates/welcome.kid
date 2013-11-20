<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Home page for the Webbrick Gateway")}
<!-- <link href="/static/css/wl-panel.css" rel="stylesheet" /> -->

<body>

${output_nav("Webbrick Gateway")}

<table class="navTable">
    <colgroup span="4" width="25%"></colgroup>

    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Hello</td>
    </tr>

    <tr>
        <wb:simpleLink target="/userinterface">Select User Interface</wb:simpleLink>
    </tr>
</table>
<table class="navTable">
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Tools</td>
    </tr>
    <tr>
        <wb:simpleLink target="/template/templates/diag">Home Diagnostics</wb:simpleLink>
   </tr>

</table>

${output_site_info_bar()}

</body>
</html>
