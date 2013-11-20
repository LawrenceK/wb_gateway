<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Security and Cameras")}

<body>

${output_nav("Security and Cameras")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Security Controls</td>
    </tr>

    <tr>  
        <wb:simpleButton wbSource="/wbsts/mediawb/DO/3" wbTarget="/wbcmd/mediawb/DI/3">Open Door</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/7">Full Lights</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/SC/1">Sleep System</wb:simpleButton>
    </tr>
  
    <tr>
        <wb:simpleButton wbTarget="/sendevent/security/alarm/set" >Set Alarm</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/security/alarm/unset" >Unset Alarm</wb:simpleButton>
    </tr>
</table>

<!-- the Webbrick Gateway will issue redirects to the cameras -->
<table>
    <tr>
        <td align="center"><iframe src="/redirect/camera6" width="340" 
height="280" frameborder="0" scrolling="no"></iframe></td>
    </tr>
</table>

${output_site_info_bar()}

</body>

</html>
