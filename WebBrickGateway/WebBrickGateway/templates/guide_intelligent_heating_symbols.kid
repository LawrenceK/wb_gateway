<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway guide to intelligent heating")}

<body>

${output_nav("Guide to Intelligent Heating")}
 
 
<table>
 <colgroup span="4" width="25%"></colgroup>
  <tr>
    <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Intelligent Heating Message Bar Symbols</td>
  </tr>
  <tr>
    <td colspan="4">
        <p>
        The WebBrick Gateway manages your heating based on four main inputs, these are 
        <b>Schedules</b>, - when the heating should run, 
        <b>Occupancy</b>, - who is in the home, are the users on vacation etc,
        <b>Weather</b>,  - what is the outside temperature and windspeed,
        <b>Intention</b>, - have the home users decided to call for heating
        </p>
    </td>
  </tr>
  <tr>
      <td class="statusWillRun">&nbsp;</td>
      <td class="statusSuppress">&nbsp;</td>
      <td class="statusIdle">&nbsp;</td>
      <td class="statusVacation">&nbsp;</td>
  </tr>
    <td><p>The heating system will <b>run</b></p></td>
    <td><p>The heating system will <b>hold off</b>, for example the outside temperature is high</p></td>
    <td><p>The heating system is <b>idle</b>, waiting for either a scheduled event or user request</p></td>
    <td><p><b>Vacation</b> mode, the system will ignore scheduled events and user requests, the heating will only start if the home
    goes below the minimum temperature</p></td>
  <tr>
  </tr>
</table>

${output_site_info_bar()}

</body>

</html>