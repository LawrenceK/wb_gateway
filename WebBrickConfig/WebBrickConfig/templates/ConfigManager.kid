<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:py="http://purl.org/kid/ns#" py:extends="'WebBrickConfigMaster.kid'">

${output_head("WebBrick Configuration Mananger")}

<!--
    Note: all event handlers are invoked via MochiKit's Signal module.
    File WebBrick.js invokes the initial window.onload handler that scans
    the entire DOM looking for wbLoad attributes and calling the corresponding 
    functions when the page has been loaded.

    DO NOT specify an onload handler on the <body> element.
-->

<body>
${output_nav("WebBrick Configuration Manager")}

<style type="text/css">
.OptNorm { font-family: monospace; }
.OptAttn { font-family: monospace; color: red; }
.OptNull { font-family: monospace; color: blue; }
.Message { text-align: center; color: blue; }
.Error   { text-align: center; color: red; }
</style>

<!--
<p>Network=${Network}, ConfigSet=${ConfigSet}, Password=${Password}</p>
-->

<form name="ConfigManager" action="/wbcnf/ConfigAction" method="post">
<table style="width: 100%;" border="0" cellpadding="2" cellspacing="2">
<tbody>

<tr>
  <td halign="right" style="width: 42%; text-align: right;">
  <h3>WebBricks on Network</h3>
  </td>
  <td>
  </td>
  <td style="width: 42%;">
  <h3>Stored WebBrick Configurations</h3>
  </td>
</tr>
<tr>
  <td style="text-align: right;">
    Network address:&nbsp;&nbsp;
    <select id="WbIpNetworks" name="WbIpNetworks" size="1" wbLoad="loadWbIpNetworks('${Network}')" >
      <option value="waiting" class="OptAttn">(Waiting for server)</option>
    </select>
  </td>
  <td>
  </td>
  <td>
    Configuration set: 
    <select id="WbConfigSets" name="WbConfigSets" size="1" wbLoad="loadConfigSetSelector('${ConfigSet}')" >
      <option class="OptAttn" value="waiting">(Waiting for server)</option>
    </select>
    <!-- space in IE -->
    <button id="WbNewCs" name="action" value="WbNewCs">New...</button>
    <!-- space in IE -->
    <button id="WbDeleteCs" name="action" value="WbDeleteCs" >Delete...</button>
    <!-- space in IE -->
  </td>
</tr>
<tr>
  <td style="text-align: right;"> 
    <pre>MAC address&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Node&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</pre>
    <select id="WbSelector" name="WbSelector" size="12" wbLoad="loadActiveWebBricksSelector()">
      <option class="OptAttn" value="waiting">(Waiting for WebBrick discovery)</option>
    </select>
    <input id="WbNodeList" name="WbNodeList" type="hidden" value="" />
  </td>
  <td>
    <p style="text-align: center;">
      <button id="WbLoadConfig" name="action" value="WbLoadConfig" 
              wbLoad="loadLoadButton()" >&lt;&lt; Load</button>
    </p>
    <p style="text-align: center;">
      <button id="WbSaveConfig" name="action" value="WbSaveConfig" 
              wbLoad="loadSaveButton()" >Save &gt;&gt;</button>
    </p>
    <p style="text-align: center;">
      <button id="WbSaveAllConfigs" name="action" value="WbSaveAllConfigs" 
              wbLoad="loadSaveAllButton()" >Save all &gt;&gt;</button>
    </p>
  </td>
  <td>
    <pre>Node&nbsp;&nbsp;Name</pre>
    <select id="WbConfigs" name="WbConfigs" size="12" wbLoad="loadWebBrickConfigurationSelector()" >
      <option class="OptAttn" node="---" name="------------"   value="waiting">(Waiting for server)</option>
    </select>
    <input type="hidden" id="WbConfigNode" name="WbConfigNode" value="nnn"      wbLoad="loadWbConfigNode()" />
    <input type="hidden" id="WbConfigName" name="WbConfigName" value="somename" wbLoad="loadWbConfigName()" />
    <input type="hidden" id="WbIpAddress"  name="WbIpAddress"  value="x.x.x.x"  wbLoad="loadWbIpAddress()"  />
    <!-- updated by javascript -->
    <input type="hidden" id="buttonAction" name="buttonAction" value="" />
  </td>
</tr>
<tr>
</tr>
  <td style="text-align: right;">
    WebBrick password:&nbsp;&nbsp;
    <input type="input" id="WbPassword" name="WbPassword" value="${Password}" wbLoad="loadWbPassword()" />
  </td>
  <td>
  </td>
<tr>
  <td style="text-align: right;">
    New IP address:&nbsp;&nbsp;
    <input id="WbNewIpAdrs" name="WbNewIpAdrs" value="111.222.333.444" wbLoad="loadWbNewIpAdrs()" />
    <input type="hidden" id="WbMacAddress" name="WbMacAddress" value="yy:xx:xx:xx:xx:xx" wbLoad="loadWbMacAddress()" />
  </td>
  <td>
  </td>
  <td style="text-align: left;">
    <!-- space in IE - - >
    <button id="WbNewConfig"    name="action" value="WbNewConfig"    >New...</button>
    < !- - space in IE - - >
    <button id="WbShowConfig"   name="action" value="WbShowConfig"   >Show...</button>
    < !- - space in IE - - >
    <button id="WbEditConfig"   name="action" value="WbEditConfig"   >Edit...</button>
    < !- - space in IE -->
    <button id="WbDeleteConfig" name="action" value="WbDeleteConfig" >Delete...</button>
    <!-- space in IE -->
  </td>
</tr>
<tr>
  <td style="text-align: right;">
    <!-- space in IE -->
    <button type="submit" id="WbDiscover" wbLoad="loadWbDiscoverButton()"
            name="action" value="WbDiscover">Discover</button>
    <!-- space in IE -->
    <button type="submit" id="WbRemoveWebBrick"   wbLoad="loadWbRemoveButton()"
            name="action" value="WbRemoveWebBrick"  >Remove</button>
    <!-- space in IE -->
    <button type="submit" id="WbAddIpAddress"      wbLoad="loadWbAddButton()"
            name="action" value="WbAddIpAddress"     >Add IP</button>
    <!-- space in IE -->
    <button type="submit" id="WbIpUpdate" wbLoad="loadWbUpdateIpButton()"
            name="action" value="WbIpUpdate">Update IP</button>
  </td>
  <td>
  </td>
  <td style="text-align: left;">
    <!-- space in IE -->
    <button id="WbCopyConfig"     name="action" value="WbCopyConfig"     >Copy...</button>
    <!-- space in IE -->
    <button id="WbMoveConfig"     name="action" value="WbMoveConfig"     >Move...</button>
    <!-- space in IE -->
    <button id="WbUploadConfig"   name="action" value="WbUploadConfig"   >Upload...</button>
    <!-- space in IE -->
    <button id="WbDownloadConfig" name="action" value="WbDownloadConfig" >Download</button>
    <!-- space in IE -->
  </td>
</tr>
</tbody>
</table>
</form>

<h2 class="Message" id="Message"></h2>

<p>Internet Explorer's handling of &lt;button&gt; elements is 
broken, so this form does not currently work in IE.
</p>

</body>
</html>
