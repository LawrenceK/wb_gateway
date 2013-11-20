<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>"Quiet" test menu without Javascript</title>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <link href="/static/css/panel.css" rel="stylesheet" />
</head>

<body>

${output_nav("Quiet")}

    <table class="navTable">
        <tr>
            <wb:simpleLink target="/static/security.xhtml">Security</wb:simpleLink>
            <wb:simpleLink target="/static/heating.xhtml">Heating</wb:simpleLink>
            <wb:simpleLink target="/mediapanel?mediatitle=iTunes&amp;medianame=ITunesInDirect">iTunes</wb:simpleLink>
            <wb:simpleLink target="/static/lighting.xhtml">Lighting</wb:simpleLink>
        </tr>
    </table>

${output_site_info_bar()}

</body>

</html>