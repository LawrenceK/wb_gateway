<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">
    
${output_head("MultiZone Setup")}

<body>

${output_nav("MultiZone Setup")}

<table>

    <?python 
        zoneLimit = WebBrickGateway.templates.widgets.getCurrentValue( "/eventstate/zone/count" )
        if zoneLimit == '':
            zoneLimit = 0
        else:
            zoneLimit = int(zoneLimit) + 1
        
        zoneGroupLimit = WebBrickGateway.templates.widgets.getCurrentValue( "/eventstate/zonegroup/count" )
        if zoneGroupLimit == '':
            zoneGroupLimit = 0
        else:
            zoneGroupLimit = int(zoneGroupLimit) + 1
            
        heatSourceLimit = WebBrickGateway.templates.widgets.getCurrentValue( "/eventstate/heatsource/count" )
        if heatSourceLimit == '':
            heatSourceLimit = 0
        else:
            heatSourceLimit = int(heatSourceLimit) + 1
            heatSourceTableWidth = int(100/heatSourceLimit)
    ?>

    <colgroup span='8' width='25%' />
    <tr>
        <wb:caption colspan='4'>Zone to Zone Group mapping</wb:caption>
    </tr>
    <tr py:for='zoneBase in range(1,zoneLimit,2)'>
        <span py:for='zoneNr in range(zoneBase,min( (zoneBase+2),zoneLimit),1)' py:strip='True'>
            <wb:caption>Zone ${zoneNr} (${output_current_value( "/eventstate/zone%s/name?attr=name"%zoneNr ) })</wb:caption>
            <wb:numericEntry 
                    prefix="" 
                    format="##" 
                    postfix=""
                    wbSource="/eventstate/zone${zoneNr}/groupnumber" 
                    wbTarget="/sendevent/zone${zoneNr}/groupnumber?type=http://id.webbrick.co.uk/events/config/set"
                    wbTitle="Zone ${zoneNr}"
                >&nbsp;
            </wb:numericEntry>
        </span>
    </tr>
</table>
&nbsp;
<table>
    <colgroup span='heatSourceLimit' width='25%'/>
    <tr>
        <wb:caption colspan='4'>Zone Group heatsource priority</wb:caption>
    </tr>
    <tr>
        <wb:caption>&nbsp;</wb:caption>
        <span py:for='hs in range(1,heatSourceLimit,1)'>
            <wb:caption>Heatsource ${hs} (${output_current_value( "/eventstate/heatsource/%s/availability?attr=name"%hs ) })</wb:caption>
        </span>
    </tr>
    <tr py:for='zg in range(1,zoneGroupLimit,1)'>
        <wb:caption>Zone Group ${zg}</wb:caption>
        <span py:for='hs in range(1,heatSourceLimit,1)' py:strip='True'>
            <wb:numericEntry 
                    prefix="" 
                    format="##" 
                    postfix=""
                    wbSource="/eventstate/zonegroup${zg}/heatsource${hs}/priority" 
                    wbTarget="/sendevent/zonegroup${zg}/heatsource${hs}/priority?type=http://id.webbrick.co.uk/events/config/set"
                    wbTitle="Zone Group ${zg}"
                >&nbsp;
            </wb:numericEntry>
        </span>
    </tr>
</table>
&nbsp;
<table>
    <colgroup span='heatSourceLimit' width='25%'/>
    <tr>
        <wb:caption colspan='3'>Heatsource enable</wb:caption>
    </tr>
    <tr>
        <wb:caption>&nbsp;</wb:caption>
        <span py:for='hs in range(1,heatSourceLimit,1)' py:strip='True'>
            <wb:enableEntry
                    prefix="Heatsource ${hs}" 
                    format="##" 
                    postfix=""
                    wbSource="/eventstate/zoneheatsource/${hs}/enabled" 
                    wbTarget="/sendevent/zoneheatsource/${hs}/enabled?type=http://id.webbrick.co.uk/events/config/set"
                    wbTitle="Heat Source ${hs}"
                >&nbsp;
            </wb:enableEntry>
        </span>
    </tr>
</table>

</body>

</html>
