<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway guide to various indicators")}

<body>

<!-- override some of the styles -->
<link href="/static/css/guide.css" rel="stylesheet" type="text/css" />


${output_nav("Guide to indicators")}
 
<h1>Indicators</h1>
            <p>There are a range of indicators used within the WebBrick Gateway, here are some and their general meanings</p>
  
<table>
 <colgroup span="4" width="25%"></colgroup>
  <tr>
      <td class="indicatorAlert">
        <p>This shows that an item is in an <b>Alert</b> state and that some attention is needed, i.e. oil level low
        </p>
      </td>
      <td class="indicatorClear">
        <p>This shows that an item is in an <b>Clear</b> state, nothing to worry about here</p>
      </td>
      <td class="indicatorOff">
        <p>This shows that an item is in an <b>Off</b> state i.e. loft lights are off</p>
      </td>
      <td class="indicatorNotReady">
         <p>This shows that an item is <b>Not Ready</b> state i.e. the coffee machine is on but not yet ready to serve</p>
      </td>
  </tr>
  <tr>
      <td class="indicatorDay">
        <p><b>Day</b> this shows that the WebBrick Gateway has considered that it is between sunrise and sunset</p>
      </td>
      <td class="indicatorNight">
        <p><b>Night</b> this hows that the WebBrick Gateway has considered that it is between sunset and surise</p>
      </td>
      <td class="buttonCooling">
        <p><b>Cooling</b> this shows that a HVAC item is providing cooling</p>
      </td>
      <td class="buttonRecycle">
        <p><b>Recycle</b> this shows that a HVAC item is providing heat recycling</p>
      </td>
  </tr>
</table>

${output_site_info_bar()}

</body>

</html>