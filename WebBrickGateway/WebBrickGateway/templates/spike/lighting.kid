<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway Lighting")}

<body>

${output_nav("Lighting")}
  

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Direct Lighting Controls</td>
    </tr>
    <tr>	
        <wb:simpleButton wbSource="/wbsts/test/DO/3" wbTarget="/wbcmd/test/DI/7">Security Lighting</wb:simpleButton>
<!--
        <td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/DI/7" 
                wbSource="/wbsts/test/DO/3">
            Security Lighting
        </td>
-->
    </tr>
</table>

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Lighting Scenes</td>
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/0">All Off</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/1">Scene 2</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/2">Scene 3</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/3">Scene 4</wb:simpleButton>
<!--
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/0" >
            All Off
        </td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/1" >
            Scene 2
     	</td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/2" >
            Scene 3
    	</td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/3" >
            Scene 4
     	</td>
-->
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/4">Scene 5</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/5">Scene 6</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/6">Scene 7</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/7">Scene 8</wb:simpleButton>
<!--
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/4" >
            Scene 5
    	</td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/5" >
            Scene 6
    	 </td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/6" >
            Scene 7
    	</td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/7" >
            Scene 8
     	</td>
-->
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/8">Scene 9</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/9">Scene 10</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/10">Scene 11</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/11">Scene 12</wb:simpleButton>
<!--
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/8" >
            Scene 9
    	</td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/9" >
            Scene 10
    	 </td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/10" >
            Scene 11
    	</td>
	<td wbType="PushButton" wbLoad="loadButton()" 
                wbTarget="/wbcmd/test/SC/11" >
            All On
     	</td>
-->
    </tr>
</table>


${output_site_info_bar()}

</body>

</html>
