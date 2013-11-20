<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">
    
${output_head("Webbrick Gateway guide to occupancy")}

<body>

<!-- override some of the styles -->
<link href="/static/css/guide.css" rel="stylesheet" type="text/css" />

${output_nav("Guide to occupancy")}
 
<span class="navTable>">
    <h1>Occupancy</h1> 

        <p>
        <b>Occupancy</b> is the way the home users tell the WebBrick Gateway about their relationship with their home.  
        The Webbrick Gateway uses this module to decide which schedules to use for heating, lighting and other controls.
        </p>
</span> 

<table>
 <colgroup span="2" width="50%"></colgroup>
  <tr>
      <td class="statusHome"><p>
        This shows that the Webbrick Gateway runs in the modes for home users <b>at Home</b>
        </p>
      </td>
      <td class="statusAway"><p>
        This shows that the Webbrick Gateway runs in the modes for home users <b> on Vacation </b>. In this mode the home would be maintained 
        at a minimum safe temperature and security lighting schedules will be run
        </p>
      </td>
  </tr>
</table>

${output_site_info_bar()}

</body>

</html>