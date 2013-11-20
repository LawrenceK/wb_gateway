<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("Mobile Menu")}

<body>

${output_nav("Mobile Menu")}

<table class="navTable">
	<colgroup span="2" width="50%"></colgroup>
    <tr>
        <td class="navBarSmall" onClick="window.location='/template/templates/mobile/homeInt'">Home Intelligence</td>
        <td class="navBarSmall" onClick="window.location='/template/templates/mobile/garage'">Garage</td>
    </tr>
</table>

</body>

</html>
