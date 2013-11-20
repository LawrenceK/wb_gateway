<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:py="http://purl.org/kid/ns#">

<head>
  <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
  <title>WebBrick Configuration Manager - Move/Rename configuration</title>
  <!-- Template inputs: 
       ConfigSet, ConfigNode, ConfigName, ConfigSets (list) 
    -->  
</head>

<body>
  <form name="CopyConfig" action="/wbcnf/MoveConfig" method="post">
    <table border="0" cellpadding="2" cellspacing="2">
    <tbody>
    <tr>
      <td colspan="2">
        <h3>Move from</h3>
      </td>
    </tr>
    <tr>
      <td>
        Configuration set&nbsp;&nbsp;
      </td>
      <td>
        <input type="text" name="ConfigSet" value="${ConfigSet}" 
               readonly="True"/>
      </td>
    </tr>
    <tr>
      <td>
        Node configuration
        &nbsp;&nbsp;
      </td>
      <td>
        Node:
        <input type="text" name="ConfigNode" value="${ConfigNode}" 
               size="4" readonly="True"/>
        Name:
        <input type="text" name="ConfigName" value="${ConfigName}" 
               size="12" readonly="True"/>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        <h3>Move to</h3>
      </td>
    </tr>
    <tr>
      <td>
        Configuration set&nbsp;&nbsp;
      </td>
      <td>
        <select id="ToConfigSet" name="ToConfigSet" size="1" >
          <option py:for="cs in ConfigSets" 
                  value="${cs}">${cs}</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>
        Node number&nbsp;&nbsp;
      </td>
      <td>
        <input type="text" id="ToConfigNode" name="ToConfigNode" 
               size="4" maxlength="3" value="${ConfigNode}"/>
      </td>
    </tr>
    </tbody>
    </table>
    <p>
      <button type="submit" name="Confirm">Move</button>
      <button type="submit" name="Cancel" >Cancel</button>
    </p>
  </form>
</body>

</html>
