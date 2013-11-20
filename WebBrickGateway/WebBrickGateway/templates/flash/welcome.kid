<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Home page for the Webbrick Gateway")}
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
        <wb:simpleLink target="/template/heating">Heating</wb:simpleLink>
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Schedules and Overiew</td>
    </tr>

    <tr>
        <wb:simpleLink target="/heating/list" label='Schedules'>Schedules</wb:simpleLink>
        <wb:simpleLink target="/template/overflashmeter">Overview</wb:simpleLink>
        
        <!--
        		=============  Big Meter Here =================
        -->
        
        <td></td>
        
         <td rowspan="7" width='210px' height='200px'
                             wbType="FlashMeter" 
                             wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                             wbSource='/eventstate/temperature/outside'
                             minvalue="0"
                             maxvalue="40"
                             curvalue="0"
                             setlow="0"
                             sethigh="100"
                             metertitle="Outside"
                             labels="0,10,20,30,40"
                             flashMovie="/static/flash/MeterRadial270.swf"
                             >
         </td>
        
        
        
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Cameras and Door control</td>
    </tr>
    <tr>
        <wb:simpleLink target="/template/security">Security</wb:simpleLink>
        <wb:simpleLink target="/template/extlighting">External Lighting</wb:simpleLink>
        <wb:simpleLink target="/template/security2">Security Ext</wb:simpleLink>
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Entertainment</td>
    </tr>
    <tr>
        <wb:simpleLink target="/mediapanel?mediatitle=iTunes&amp;medianame=ITunesInDirect">iTunes</wb:simpleLink>
    </tr>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Tools</td>
    </tr>
    <tr>
        <wb:simpleLink target="/template/diag">Home Diagnostics</wb:simpleLink>
        <wb:simpleLink target="/template/homeInt">Day Controls</wb:simpleLink>
        <wb:simpleLink target="/template/LEControl">LE Control</wb:simpleLink>
   </tr>

</table>

${output_site_info_bar()}

</body>
</html>
