<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Home page for the Webbrick Gateway - Samples1")}
<!-- <link href="/static/css/wl-panel.css" rel="stylesheet" /> -->

<body>

${output_nav("Webbrick Gateway")}

<table class="navTable">
    <colgroup span="4" width="25%"></colgroup>

    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Rooms</td>
    </tr>

    <tr>
        <wb:simpleLink target="/template/downstairs">Kitchen and Lounge</wb:simpleLink>
        <wb:simpleLink target="/template/upstairs">Bedrooms</wb:simpleLink>
        <wb:simpleLink target="/template/garage">Garage</wb:simpleLink>
		<wb:flashMeter rowspan='4'
				wbSource="/eventstate/temperature/outside" 
				prefix="" 
				format="##.#" 
				postfix="&ordm;C"
                minvalue="-10"
                maxvalue="40"
                setlow="-10"
                sethigh="100"
                labels="-10, 0,10,20,30,40"
                flashMovie='MeterRadial270.swf'
                >
			Outside
		</wb:flashMeter>
<!--        
		<wb:flashMeter rowspan='4'
				wbSource="/eventstate/temperature/outside" 
				prefix="" 
				format="##.#" 
                minvalue="-10"
                maxvalue="40"
                curvalue="0"
                setlow="-10"
                sethigh="100"
                width="200px"
                height="200px"
                labels="-10, 0,10,20,30,40"
                flashMovie='MeterRadial270.swf'
				postfix="&ordm;C">
			Outside
		</wb:flashMeter>
-->        
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Heating</td>
    </tr>
    <tr>
        <wb:simpleLink target="/template/heating">Heating</wb:simpleLink>
        <wb:simpleLink target="/template/zones">Multi Zone</wb:simpleLink>
        <wb:simpleLink target="/template/homeInt">Home intelligence</wb:simpleLink>
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Audio/Video</td>
    </tr>
    <tr>
        <wb:simpleLink target="/media">Music</wb:simpleLink>
    </tr>
</table>

<table class="navTable">
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Tools</td>
    </tr>
    <tr>
        <wb:simpleLink target="/wbsts/known">Known WebBricks</wb:simpleLink>
        <wb:simpleLink target="/wbcnf">WebBrick Configuration manager</wb:simpleLink>
   </tr>

</table>

${output_site_info_bar()}

</body>
</html>
