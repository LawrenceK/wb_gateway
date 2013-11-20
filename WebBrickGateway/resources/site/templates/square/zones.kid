<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Zone Controls")}

<body>

${output_nav("Zone Controls")}

    <?python 
        zoneCount= WebBrickGateway.templates.widgets.getCurrentValue( "/eventstate/zone/count" )
        if zoneCount == '':
            zoneLimit = 0
        else:
            zoneLimit = int(zoneCount) + 1

    ?>

<table class="navTable">
    <colgroup span="8" width="12.5%"/>

    <loop py:for='zoneBase in range(1,zoneLimit,8)' py:strip='True'>
        <tr py:if='zoneBase+8 &lt; zoneLimit'>
            <wb:caption 
                py:content='"Zones %s - %s" %(zoneBase, zoneBase+7)' 
                colspan="2" >Dummy</wb:caption>
        </tr>
        <tr py:if='zoneBase+8 &gt;= zoneLimit'>
            <wb:caption py:content='"Zones %s - %s" %(zoneBase, zoneLimit-1)' colspan="2">Dummy</wb:caption>
        </tr>
        <tr>
            <loop2 py:for='zoneNr in range(zoneBase,min( (zoneBase+8),zoneLimit),1)' py:strip='True'>
                
                <wb:simpleLink 
                    target="/template/templates/zoneControl${zoneNr}" 
                    
                    py:content='output_current_value( "/eventstate/zone%s/name?attr=name"%zoneNr )'>
                    Dummy
                </wb:simpleLink>
            </loop2>
        </tr>
    </loop>
    
</table>

<table class="navTable">
    <colgroup span="4" width="25%"/>
    <tr>
        <wb:caption colspan="2">Zone Diagnostics</wb:caption>
    </tr>
    <tr>
        <wb:simpleLink target="/template/templates/zoneDiagnostics">Zone Diagnostics</wb:simpleLink>
        <wb:simpleLink target="/template/templates/zoneGroupSetup">Zone Setup</wb:simpleLink>
        <wb:simpleLink target="/template/templates/weather">Weather Compensation</wb:simpleLink>
    </tr>
</table>

${output_site_info_bar()}

</body>
</html>
