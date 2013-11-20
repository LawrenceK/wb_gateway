<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" 
      xmlns:py="http://purl.org/kid/ns#" 
      xmlns:ui="ui" 
      py:extends="sitetemplate">

<head py:def="output_head(title)">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${title}</title>
    <link href="/static/css/panel.css" rel="stylesheet" />
    <script src="/static/javascript/MochiKit.js"></script>
    <script src="/static/javascript/WebBrick.js"></script>
    <script src="/static/javascript/WbConfig.js"></script>
    <script src="/static/javascript/debug.js" type="text/javascript"></script>
</head>

<table py:def="output_nav( location )" class="navTable">
    <tr>
        <td width="12%" class="navBar" onClick="window.location='/'">Home Menu</td>
        <td class="infoBar" id="menuTitle">${location}</td>
        <td width="12%" class="navBar" onClick="history.back()">Back</td>
        <td width="12%" class="navBar" onClick="window.location='/template/guide'">Guide</td>
    </tr>
    <tr class="rule"><td colspan='4' class="ruleBar">&nbsp;</td></tr>
</table>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
    <div py:if="item.get('header')!='No'">
        <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>
    </div>
    <div py:replace="[item.text] + item[:]"/>
</body>

</html>
