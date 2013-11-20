<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">
    
${output_head("Webbrick Gateway Upstairs Control")}

<body>

${output_nav("Bedrooms")}
  

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="4" wbType="Caption" wbLoad="loadCaption()">Bedroom 1</td>
    </tr>
    <tr>  

        	<wb:simpleButton wbTarget="/wbcmd/house1/SC/8"
        		wbSource="/wbsts/house1/DO/6">
        	Lights Off
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/DI/7">
        	Scene Up
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/DI/9">
        	Scene Down
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house1/SC/11">
        	Lights Full
        	</wb:simpleButton>
    </tr>
	<tr>
			<td rowspan="2" width='80px' height='80px'
						wbType="FlashMeter" 
						wbLoad='loadFlashMeter("","##","%")'
						wbSource='/wbsts/house1/AO/2'
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
			<td>&nbsp;</td>

        	<wb:simpleButton wbSource="/wbsts/house1/DO/3" wbTarget="/wbcmd/house1/DI/3">
        	Underfloor Heating
        	</wb:simpleButton>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td colspan="3">&nbsp;</td>
		</tr>
    <tr>
			<td colspan="3">&nbsp;</td>    
    </tr>
</table>
  

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Bedroom 2</td>
    </tr>
    <tr>  
        	<wb:simpleButton wbTarget="/wbcmd/house2/SC/8"
        		wbSource="/wbsts/house2/DO/6">
        	Lights Off
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/DI/7">
        	Scene Up
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/DI/9">
        	Scene Down
        	</wb:simpleButton>

        	<wb:simpleButton wbTarget="/wbcmd/house2/SC/11">
        	Lights Full
        	</wb:simpleButton>

    </tr>
	<tr>
			<td rowspan="2" width='80px' height='80px'
						wbType="FlashMeter" 
						wbLoad='loadFlashMeter("","##","%")'
						wbSource='/wbsts/house2/AO/3'
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
			<td>&nbsp;</td>
        	<wb:simpleButton wbSource="/wbsts/house1/DO/0" wbTarget="/wbcmd/house1/DI/0">
        	Underfloor Heating
        	</wb:simpleButton>

		  <td class="NaN" rowspan="3">
			<img width="50%" src="/static/images/Decorations/Pillows.png" />
		  </td>
    </tr>
    <tr>
			<td colspan="4">&nbsp;</td>    
    </tr>
    <tr>
			<td colspan="4">&nbsp;</td>    
    </tr>
</table>





${output_site_info_bar()}

</body>

</html>
