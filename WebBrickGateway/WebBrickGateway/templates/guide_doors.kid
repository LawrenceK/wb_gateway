<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway help index page")}

<body>

${output_nav("Guide to Door Operation")}
 
 
<table>
 <colgroup span="5" width="15%"></colgroup>
  <tr>
    <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Garage Doors</td>
  </tr>
  <tr>
      <td class="doorOpen">Open</td>
      <td class="doorClosed">Closed</td>
      <td class="doorAjar">Ajar</td>
      <td class="doorError">Error</td>
      <td class="doorPending">Pending</td>
  </tr>
    <td><p>The door is <b>Open</b></p></td>
    <td><p>The door is <b>Closed</b></p></td>
    <td><p>The door is <b>Ajar</b></p></td>
    <td><p>The door is in a <b>Error</b> or <b>Unknown</b> state</p></td>
    <td><p>The Webbrick Gateway is <b>waiting</b> for the door to report its state</p></td>
  <tr>
  </tr>
</table>

${output_site_info_bar()}

</body>

</html>