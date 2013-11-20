<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("WebBrick Gateway Guide to basic operations")}

<body>
<!-- override some of the styles -->
<link href="/static/css/guide.css" rel="stylesheet" type="text/css" />

${output_nav("Guide basic operations")}

<h1>Appliances</h1>
  
<table>
 <colgroup span="5" width="15%"></colgroup>
  <tr>
    <td class="buttonOn">
     <p>This means the item is <b>On</b> - it is based on the international symbol for 'On'</p>
    </td> 

    <td class="buttonOff">
     <p>This means the item is <b>Off</b>  - it is based on the international symbol for 'Off'</p>
    </td> 

    <td class="buttonAbsent">
     <p>This means that the item is <b>Absent</b>, the Webbrick Gateway is searching for this item</p> 
    </td> 

    <td class="buttonLocked">
     <p>This means that the item is <b>Locked</b>, it is present but cannot be operated from this page</p>
    </td> 

    <td class="buttonPending">
     <p>This means that the Webbrick Gateway is <b>Waiting</b> for the item to report its current state</p>
    </td> 
  </tr>
  
  <tr>
    <td class="indicatorNotReady"><p>This means the item is <b>Not Ready</b></p></td>
    <td class="indicatorAlarm"><p>This means the item has an <b>Alarm</b> state</p></td>
  </tr>
</table>



${output_site_info_bar()}

</body>

</html>