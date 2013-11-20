<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">
    
${output_head("Webbrick Gateway Garage")}

<body>

${output_nav("Garage")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
  <tr>
  	<td colspan="3">&nbsp;</td>
  	<td><img width="100%" src="/static/images/Decorations/beetle.png"/></td>
  </tr>
  <tr>
        <wb:simpleButton wbSource="/wbsts/house3/DO/5" wbTarget="/wbcmd/house3/DI/5">Open</wb:simpleButton>
        <wb:simpleButton wbSource="/wbsts/house3/DO/4" wbTarget="/wbcmd/house3/DI/4">Close</wb:simpleButton>

	<td wbType="PushButton" wbLoad="loadButton()"
                wbSource="/wbsts/house3/DI/7"
                stateVals="Open,Closed,Ajar,Error"
                baseClassName="door">
            Garage Door
        </td>
  </tr>
  <tr>
        <wb:simpleButton wbTarget="/wbcmd/house3/DI/3">Lights</wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/house3/AA/0/50">Lights Half</wb:simpleButton>
        <wb:numericDisplay wbSource="/wbsts/house3/AO/0" prefix="Garage: " format="##.#" postfix="%">--</wb:numericDisplay>
        
  </tr>
  
</table>

${output_site_info_bar()}

</body>

</html>