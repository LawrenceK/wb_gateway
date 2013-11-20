<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Webbrick Gateway guide to intelligent heating")}

<body>

${output_nav("Guide to Intelligent Heating")}
 
 
<table>
 <colgroup span="4" width="25%"></colgroup>
  <tr>
    <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Intelligent Heating</td>
  </tr>
  <tr>
    <td colspan="4">
        <p>
        The WebBrick Gateway manages your heating based on <b>Zones</b>.  
        A <b>Zone</b> can be related to an area of the home or a function, for example Hot Water
        </p>
        
        <p>
        <b>Zones</b> then call upon <b>ZoneGroups</b> to feed heat into them.
        A <b>ZoneGroup</b> is typically a manifold, valve or pump combination that connects the 
        <b>Zone</b> to a <b>HeatSource</b>
        </p>
        <p>
        A heating system can have one or more <b>HeatSources</b> these are the plant that actually
        gives the heat energy.  <b>HeatSources</b> can range from Boilers through Ground Source Heat Pumps
        and Solar Panels.  The heating module has these configured and monitored in terms of <b>cost</b>
        and <b>availability</b>.
        </p>
        <p>Solar panels are likely to be the cheapest form of heat, but, are not available all day.
        </p>
        <p><b>Weather Compensation</b> Is used to adjust or suppress <b>Zones</b>.  You can select a channel based on
        external temperature thresholds, so if it is warm outside a <b>Zone</b> may not run.
        </p>
        <p>
        <img width="50%" src="/static/images/Plant/HeatingSolution.png" />
        </p>
    </td>
  </tr>
</table>

${output_site_info_bar()}

</body>

</html>