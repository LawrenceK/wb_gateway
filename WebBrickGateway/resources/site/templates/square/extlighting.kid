<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Webbrick Gateway External Lighting")}

<body>

${output_nav("External Lighting")}
  

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Direct Lighting Controls</td>
    </tr>
    <tr>	
	<td wbType="PushButton" wbLoad="loadButton()"
                wbSource="/eventstate/Garage/Door/1"
                stateVals="Ajar,Closed,Open,Error"
                baseClassName="door">
            Garage Door
        </td>
        <wb:simpleButton wbTarget="/sendevent/sunrise">Emulate Sunrise</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/sunset">Emulate Sunset</wb:simpleButton>
        <td wbType="Indicator" wbLoad="loadButton()"
			        wbSource="/eventstate/lighting/isDark"
		            stateVals="Day,Night"
		            baseClassName="indicator"
			        >
		   Day Phase
	    </td>

  </tr>
</table>

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Driveway Lighting</td>
    </tr>
    <tr>
        <wb:simpleButton wbSource="/wbsts/house2/DO/0" wbTarget="/wbcmd/house2/DI/0">Drive set 1</wb:simpleButton>
        <wb:simpleButton wbSource="/wbsts/house2/DO/1" wbTarget="/wbcmd/house2/DI/1">Drive set 2</wb:simpleButton>
        <wb:simpleButton wbSource="/wbsts/house2/DO/2" wbTarget="/wbcmd/house2/DI/2">Drive set 3</wb:simpleButton>
        <wb:simpleButton wbSource="/wbsts/house2/DO/3" wbTarget="/wbcmd/house2/DI/3">Drive Lamppost</wb:simpleButton>
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/sendevent/startdrive">Start Drive Seq</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/stopdrive">Stop Drive Seq</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/garage/on">Garage On</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/garage/off">Garage Off</wb:simpleButton>
    </tr>
</table>


<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Lighting Values</td>
    </tr>
	<tr>
        <wb:numericDisplay wbSource="/wbsts/house3/AO/0" prefix="Garage: " format="##.#" postfix="%">--</wb:numericDisplay>
	</tr>

</table>


${output_site_info_bar()}

</body>

</html>
