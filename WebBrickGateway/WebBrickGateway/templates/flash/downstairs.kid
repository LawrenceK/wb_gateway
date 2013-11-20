<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">
    
${output_head("Webbrick Gateway Downstairs Control")}

<body>

${output_nav("Lounge and Kitchen")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Kitchen</td>
    </tr>
    <tr>  
        	<wb:simpleButton wbTarget="/wbcmd/house1/SC/0">
        	Lights Off
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/DI/0">
        	Scene Up
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/DI/1">
        	Scene Down
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/SC/5">
        	Lights Full
        	</wb:simpleButton>

    </tr>
    <tr>
        <wb:numericDisplay wbSource="/wbsts/house1/AO/0" prefix="Kitchen 1: " format="##.#" postfix="%">--</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/house1/AO/1" prefix="Kitchen 2: " format="##.#" postfix="%">--</wb:numericDisplay>
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
					metertitle="Uplights"
					labels="0,25,50,75,100"
					flashMovie="/static/flash/Simple270.swf"
					>
		</td>
		<td width='80px' height='80px'
					wbType="FlashMeter" 
					wbLoad='loadFlashMeter("","##","%")'
					wbSource='/wbsts/house1/AO/0'
					minvalue="0"
					maxvalue="100"
					curvalue="0"
					setlow="0"
					sethigh="100"
					metertitle="Kitchen"
					labels="0,25,50,75,100"
					flashMovie="/static/flash/Simple270.swf"
					>
		</td>
    </tr>
</table>



<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="4" wbType="Caption" wbLoad="loadCaption()">Lounge</td>
    </tr>
    <tr>  

        	<wb:simpleButton wbTarget="/wbcmd/house2/SC/0">
        	Lights Off
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/DI/0">
        	Scene Up
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/DI/1">
        	Scene Down
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/SC/6">
        	Lights Full
        	</wb:simpleButton>
    </tr>
    <tr>
        <wb:numericDisplay wbSource="/wbsts/house2/AO/0" prefix="Lounge 1: " format="##.#" postfix="%">--</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/house2/AO/1" prefix="Lounge 2: " format="##.#" postfix="%">--</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/house2/AO/2" prefix="Lounge 3: " format="##.#" postfix="%">--</wb:numericDisplay>
    </tr>
    <tr>
		<td width='80px' height='80px'
					wbType="FlashMeter" 
					wbLoad='loadFlashMeter("","##","%")'
					wbSource='/wbsts/house2/AO/0'
					minvalue="0"
					maxvalue="100"
					curvalue="0"
					setlow="0"
					sethigh="100"
					metertitle="Lounge"
					labels="0,25,50,75,100"
					flashMovie="/static/flash/Simple270.swf"
					>
		</td>
		<td width='80px' height='80px'
					wbType="FlashMeter" 
					wbLoad='loadFlashMeter("","##","%")'
					wbSource='/wbsts/house2/AO/1'
					minvalue="0"
					maxvalue="100"
					curvalue="0"
					setlow="0"
					sethigh="100"
					metertitle="Uplights"
					labels="0,25,50,75,100"
					flashMovie="/static/flash/Simple270.swf"
					>
		</td>
		<td width='80px' height='80px'
					wbType="FlashMeter" 
					wbLoad='loadFlashMeter("","##","%")'
					wbSource='/wbsts/house2/AO/2'
					minvalue="0"
					maxvalue="100"
					curvalue="0"
					setlow="0"
					sethigh="100"
					metertitle="Standard"
					labels="0,25,50,75,100"
					flashMovie="/static/flash/Simple270.swf"
					>
		</td>
		  <td align="center">
			<img src="/static/images/Decorations/smallFish.png" />
		  </td>

    </tr>
</table>
  

${output_site_info_bar()}

</body>

</html>
