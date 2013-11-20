<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">
    
${output_head("Webbrick Gateway Heating")}

<body>

${output_nav("Heating and Ventilation")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Stand Zone</td>
    </tr>
    <tr>  
        	<wb:simpleButton wbSource="/wbsts/mediawb/DO/0" wbTarget="/wbcmd/mediawb/DI/0">
        	Fan
        	</wb:simpleButton>

        	<wb:simpleButton wbSource="/wbsts/mediawb/DO/1" wbTarget="/wbcmd/mediawb/DI/1">
        	Zone Valve
        	</wb:simpleButton>

        	<wb:simpleButton wbSource="/wbsts/mediawb/DO/2" wbTarget="/wbcmd/mediawb/DI/2">
        	Radiator
        	</wb:simpleButton>

    </tr>
</table>



<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="4" wbType="Caption" wbLoad="loadCaption()">House Heating</td>
    </tr>
    <tr>  

        	<wb:simpleButton wbSource="/wbsts/house3/DO/3" wbTarget="/wbcmd/house3/DI/10">
        	CH Boiler
        	</wb:simpleButton>

        	<wb:simpleButton wbSource="/wbsts/house2/DO/6" wbTarget="/wbcmd/house2/DI/11">
        	HW Boiler
        	</wb:simpleButton>

        	<wb:simpleButton wbSource="/wbsts/house2/DO/7" wbTarget="/wbcmd/house2/DI/7">
        	HW Pilot
        	</wb:simpleButton>

    </tr>
</table>
  



<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="4" wbType="Caption" wbLoad="loadCaption()">House Underfloor Heating Zones</td>
    </tr>
    <tr>  

        	<wb:simpleButton wbSource="/wbsts/house1/DO/1" wbTarget="/wbcmd/house1/DI/1">
        	Kitchen
        	</wb:simpleButton>

        	<wb:simpleButton wbSource="/wbsts/house1/DO/2" wbTarget="/wbcmd/house1/DI/2">
        	Lounge
        	</wb:simpleButton>

        	<wb:simpleButton wbSource="/wbsts/house1/DO/3" wbTarget="/wbcmd/house1/DI/3">
        	Bedroom 1
        	</wb:simpleButton>

        	<wb:simpleButton wbSource="/wbsts/house1/DO/0" wbTarget="/wbcmd/house1/DI/0">
        	Bedroom 2
        	</wb:simpleButton>


    </tr>
    <tr>
    	<td />
    	<td />
    	<td />
      	<td>
		  	<img src="/static/images/Decorations/daffodil.png" />
      	</td>
  </tr>
</table>




${output_site_info_bar()}

</body>

</html>
