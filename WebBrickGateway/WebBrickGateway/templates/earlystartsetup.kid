<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Early Start Configuration")}

<body>

${output_nav("Early Start Configuration")}

&nbsp;

<table>
    
    <colgroup span='7'/>
    <tr>
        <wb:caption colspan='1'>
                Zone
        </wb:caption>
        <wb:caption colspan='1'>
                Include
        </wb:caption>
        <wb:caption colspan='1'>
                Target
        </wb:caption>
        <td width='5%'>
                &nbsp;
        </td>
        <wb:caption colspan='1'>
                Zone
        </wb:caption>
        <wb:caption colspan='1'>
                Include
        </wb:caption>
        <wb:caption colspan='1'>
                Target
        </wb:caption>
    </tr>
    <tr py:for='zoneBase in range(1,17,2)'>
        <span py:for='zoneNr in range(zoneBase,zoneBase+1,1)' py:strip='True'>
            <wb:caption colspan='1'>
                ${output_current_value( "/eventstate/zone%s/name?attr=name"%zoneNr ) }
            </wb:caption>
            <wb:enableEntry
                    colspan='1'
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbSource="/eventstate/zone${zoneNr}/earlystart/enabled"
                    wbTarget="/sendevent/zone${zoneNr}/earlystart/enabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Include"
                    />
            <wb:numericEntry 
                    colspan='1'
                    wbSource="/eventstate/zone${zoneNr}/earlystart/setpoint"
                    wbTarget="/sendevent/zone${zoneNr}/earlystart/setpoint?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="" 
                    format="##.#" 
                    postfix="&ordm;C">
                    wbTitle="Set Point"
                    Set Point
            </wb:numericEntry>
            
        </span>
        <span >
            <td width='5%'>
                &nbsp;
            </td>
        </span>
        <span py:for='zoneNr in range(zoneBase+1,zoneBase+2,1)' py:strip='True'>
            <wb:caption>${output_current_value( "/eventstate/zone%s/name?attr=name"%zoneNr ) }
            </wb:caption>
            <wb:enableEntry
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbSource="/eventstate/zone${zoneNr}/earlystart/enabled"
                    wbTarget="/sendevent/zone${zoneNr}/earlystart/enabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Enable"
                    />
            <wb:numericEntry 
                    wbSource="/eventstate/zone${zoneNr}/earlystart/setpoint"
                    wbTarget="/sendevent/zone${zoneNr}/earlystart/setpoint?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="" 
                    format="##.#" 
                    postfix="&ordm;C">
                    wbTitle="Set Point"
                    Set Point
            </wb:numericEntry>
        </span>
    </tr>
</table>



${output_site_info_bar()}

</body>

</html>
