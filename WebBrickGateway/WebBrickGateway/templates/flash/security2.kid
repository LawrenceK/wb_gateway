<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway Security Page")}

<body>

${output_nav("Webbrick Gateway")}

<!-- the Webbrick Gateway will issue redirects to the cameras -->
<table>
    <tr>
        <td align="center"><iframe src="/redirect/camera9" width="600" height="400" frameborder="0" scrolling="no"></iframe></td>
    </tr>
</table>

${output_site_info_bar()}

</body>

</html>
