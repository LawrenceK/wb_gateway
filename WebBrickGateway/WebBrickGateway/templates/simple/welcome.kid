<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway Home page")}
<!-- <link href="/static/css/wl-panel.css" rel="stylesheet" /> -->

<body>

${output_nav("Webbrick Gateway")}

<table class="navTable">
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <wb:simpleLink target="/template/overview">Overview</wb:simpleLink>
        <wb:simpleLink target="/template/garage">Garage</wb:simpleLink>
        <wb:simpleLink target="/template/lighting">Lighting</wb:simpleLink>
        <wb:simpleLink target="/template/heating">Heating</wb:simpleLink>
    </tr>
    <tr>
        <wb:simpleLink target="/userinterface">Configure UI</wb:simpleLink>
    </tr>
    <tr>
        <wb:simpleLink target="http://www.WebBrickSystems.com"><img src='/static/images/OH2M8-logoSmall.png'/></wb:simpleLink>
    </tr>
</table>
${output_site_info_bar()}
</body>

</html>
