<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway Security Page")}

<body>

${output_nav("Webbrick Gateway")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Security Controls</td>
    </tr>

    <tr>  

        <wb:simpleButton wbSource="/wbsts/house3/DO/5" wbTarget="/wbcmd/house3/DI/5">
        Open
        </wb:simpleButton>
        <wb:simpleButton wbSource="/wbsts/house3/DO/4" wbTarget="/wbcmd/house3/DI/4">
        Close
        </wb:simpleButton>

    </tr>
</table>

<!-- the Webbrick Gateway will issue redirects to the cameras -->
<table>
    <tr>
        <td><iframe src="/redirect/camera11" width="340" height="280" frameborder="0" scrolling="no"></iframe></td>
    </tr>
</table>

${output_site_info_bar()}

</body>

</html>
