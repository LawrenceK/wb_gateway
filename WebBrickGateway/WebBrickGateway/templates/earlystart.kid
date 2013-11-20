<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Early Start")}

<body>

${output_nav("Early Start")}

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="4" wbType="Caption" wbLoad="loadCaption()">One off early start</td>
    </tr>
    <tr>
        <wb:timeEntry   
            wbSource="/eventstate/earlystart/time?attr=time"
            wbTitle="earlystart time" 
            wbTarget="/sendevent/earlystart/time?type=http://id.webbrick.co.uk/events/config/set"
            noPolling="yes">
            &nbsp;
        </wb:timeEntry>
        <wb:simpleButton  
            wbLoad="loadButton()"
            wbTarget="/sendevent/earlyStart/enable" >
            Enable
        </wb:simpleButton>
        <wb:simpleButton 
            wbLoad="loadButton()"
            wbTarget="/sendevent/earlyStart/disable" >
            Disable
        </wb:simpleButton>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td rowspan="5"><img src="/static/images/Decorations/daffodil.png"/></td>
    </tr>
    <tr>
        <td>&nbsp;</td> 
    </tr>
    <tr>
        <wb:simpleLink target="/template/earlystartsetup">Early Start Package</wb:simpleLink>
    </tr>
    <tr>
        <td>&nbsp;</td> 
    </tr>
    <tr>
        <td>&nbsp;</td> 
    </tr>

</table>

${output_site_info_bar()}

</body>

</html>
