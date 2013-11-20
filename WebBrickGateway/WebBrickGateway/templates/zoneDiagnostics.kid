<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Zone Diagnostics")}

<body>

${output_nav("Zone Status")}

    <?python 
        zoneLimit = WebBrickGateway.templates.widgets.getCurrentValue( "/eventstate/zone/count" )
        if zoneLimit == '':
            zoneLimit = 0
        else:
            zoneLimit = int(zoneLimit) + 1

    ?>

<table>
    <tr>
    <th>Name</th>
    <th>status</th>
    <th>target setpoint</th>
    <th>zone temp</th>
    </tr>
    <tr py:for='zoneNr in range(1,zoneLimit,1)' onClick='window.location=&apos;/template/templates/zoneControl${zoneNr}&apos;' >
    <div py:if='1'>
    <wb:textDisplay wbSource="/eventstate/zone${zoneNr}/name?attr=name">Name
    </wb:textDisplay>
    <wb:textDisplay wbSource="/eventstate/zone${zoneNr}/state?attr=status">status
    </wb:textDisplay>
    <wb:numericDisplay wbSource="/eventstate/zone${zoneNr}/state?attr=targetsetpoint" prefix="" format="##.#" postfix="&ordm;C">zoneSetpoint
    </wb:numericDisplay>
    <wb:numericDisplay wbSource="/eventstate/zone${zoneNr}/state?attr=zoneTemp" prefix="" format="##.#" postfix="&ordm;C">zoneTemp
    </wb:numericDisplay>
    </div>
    </tr>
</table>


<!--
  This page can get big and therefore get scroll bars
  Therefore the site info bar is commented out
${output_site_info_bar()}
-->
</body>

</html>
