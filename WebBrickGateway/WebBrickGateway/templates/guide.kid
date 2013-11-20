<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway help index page")}

<body>

${output_nav("WebBrick Gateway Help Index")}
  

<table class="navTable">
	<colgroup span="4" width="25%"></colgroup>
	<tr>
		<td colspan="2" wbType="Caption" wbLoad="loadCaption()">Here is an index to the guides available</td>
	</tr>
	<tr>
		<td class="navBarSmall" onClick="window.location='/template/guide_basic_operations'">Basic Operations</td>
		<td class="navBarSmall" onClick="window.location='/template/guide_occupancy'">Occupancy</td>
		<td class="navBarSmall" onClick="window.location='/template/guide_intelligent_heating'">Intelligent Heating</td>
		<td class="navBarSmall" onClick="window.location='/template/guide_doors'">Garage Doors</td>
	</tr>
	<tr>
		<td class="navBarSmall" onClick="window.location='/template/guide_indicators'">Indicators</td>
	</tr>
</table>

${output_site_info_bar()}

</body>

</html>