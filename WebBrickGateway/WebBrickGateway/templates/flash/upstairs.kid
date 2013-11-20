<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">
    
${output_head("Webbrick Gateway Upstairs Control")}

<body>

${output_nav("Bedrooms")}
  

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="4" wbType="Caption" wbLoad="loadCaption()">Bedroom 1</td>
    </tr>
    <tr>  

        	<wb:simpleButton wbTarget="/wbcmd/house1/SC/7">
        	Lights Off
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/DI/0">
        	Scene Up
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/DI/1">
        	Scene Down
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/SC/11">
        	Lights Full
        	</wb:simpleButton>
    </tr>
    <tr>
        <wb:numericDisplay wbSource="/wbsts/house1/AO/3" prefix="Bedroom 1: " format="##.#" postfix="%">--</wb:numericDisplay>
	</tr>
	<tr>
			<td width='80px' height='80px'
						wbType="FlashMeter" 
						wbLoad='loadFlashMeter("","##","%")'
						wbSource='/wbsts/house1/AO/3'
						minvalue="0"
						maxvalue="100"
						curvalue="0"
						setlow="0"
						sethigh="100"
						metertitle="Bedroom 1"
						labels="0,25,50,75,100"
						flashMovie="/static/flash/Simple270.swf"
						>
			</td>
			<td></td>

        	<wb:simpleButton wbSource="/wbsts/house1/DO/3" wbTarget="/wbcmd/house1/DI/3">
        	Underfloor Heating
        	</wb:simpleButton>
			<td></td>
		</tr>
</table>
  

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Bedroom 2</td>
    </tr>
    <tr>  
        	<wb:simpleButton wbTarget="/wbcmd/house2/SC/7">
        	Lights Off
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/DI/0">
        	Scene Up
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/DI/1">
        	Scene Down
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/SC/11">
        	Lights Full
        	</wb:simpleButton>

    </tr>
    <tr>
        <wb:numericDisplay wbSource="/wbsts/house2/AO/0" prefix="Bedroom 2: " format="##.#" postfix="%">--</wb:numericDisplay>
	</tr>
	<tr>
			<td width='80px' height='80px'
						wbType="FlashMeter" 
						wbLoad='loadFlashMeter("","##","%")'
						wbSource='/wbsts/house1/AO/0'
						minvalue="0"
						maxvalue="100"
						curvalue="0"
						setlow="0"
						sethigh="100"
						metertitle="Bedroom 2"
						labels="0,25,50,75,100"
						flashMovie="/static/flash/Simple270.swf"
						>
			</td>
			<td></td>
        	<wb:simpleButton wbSource="/wbsts/house1/DO/0" wbTarget="/wbcmd/house1/DI/0">
        	Underfloor Heating
        	</wb:simpleButton>
			  <td align="center">
				<img width="100" height="100" src="/static/images/Decorations/orangeFish.png" />
			  </td>
    </tr>
</table>





${output_site_info_bar()}

</body>

</html>
