<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Webbrick Gateway General Information")}

<body>

${output_nav("General Information")}
  

<!--       This is where we work        -->

<table>
	<colgroup span="4" width="25%"></colgroup>
  <tr>
    <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Information and Status</td>
  </tr>
  <tr>

  </tr>
    <td wbType="Text" wbLoad='loadTextDisplay("Sunrise ","")'
            wbSource='/local/time?val=sunrise' />
    <td wbType="Text" wbLoad='loadTextDisplay("Sunset ","")'
            wbSource='/local/time?val=sunset' />
    	<td wbType="Indicator" wbLoad="loadButton()"
	        wbSource="/eventstate/lighting/isDark"
            stateVals="Day,Night"
            baseClassName="indicator"
	        >
	    Day Phase
	    </td>

        <wb:numericDisplay wbSource="/wbsts/house1/AO/3" prefix="Sun: " format="##.#" postfix="%">--</wb:numericDisplay>

  <tr>
  </tr>
  
  <tr>
        <wb:simpleButton wbTarget="/sendevent/sunrise">Emulate Sunrise</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/sunset">Emulate Sunset</wb:simpleButton>  
  </tr>
  
</table>


<table>
	<colgroup span="4" width="25%"></colgroup>
  <tr>
    <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Temporary Items - remove for show</td>
  </tr>

  <tr>
        <wb:simpleButton wbSource="/wbsts/mediawb/DO/5" wbTarget="/wbcmd/mediawb/DI/5">Media Amp</wb:simpleButton>
  </tr>

  <tr>
        <wb:simpleButton wbTarget="/sendevent/all/on">All Lights On</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/sleep">Sleep House</wb:simpleButton>  
  </tr>



</table>



${output_site_info_bar()}

</body>

</html>
