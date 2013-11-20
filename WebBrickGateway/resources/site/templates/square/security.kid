<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Security and Cameras")}

<body>

${output_nav("Security and Cameras")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Security Controls</td>
    </tr>

    <tr>  

        <wb:simpleButton wbSource="/wbsts/mediawb/DO/3" wbTarget="/wbcmd/mediawb/DI/3">
        Open Door
        </wb:simpleButton>

        <td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/7">
            Full Lights
        </td>
        <td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/1">
            Sleep System
        </td>
    </tr>
  
    <tr>
        <td wbType="PushButton" wbLoad="loadButton()" 
                    wbTarget="/sendevent/security/alarm/set" > 
                  Set Alarm
        </td>
        <td wbType="PushButton" wbLoad="loadButton()" 
                    wbTarget="/sendevent/security/alarm/unset" > 
                  Unset Alarm
        </td>

    </tr>
</table>

<!-- the hga will issue redirects to the cameras -->
<table>
    <tr>
        <td class="NaN"><iframe src="/redirect/camera6" width="340" 
height="280" frameborder="0" scrolling="no" id="camera1" 
name="camera1"></iframe></td>
    </tr>
</table>

${output_site_info_bar()}

<script type="text/javascript">
function reloadFrame()
{
	var f = document.getElementById('camera1');
//	f.contentWindow.location.reload(true);
	f.contentWindow.location = "/redirect/camera6";
}
setInterval("reloadFrame()", 3000); 
</script>
</body>

</html>
