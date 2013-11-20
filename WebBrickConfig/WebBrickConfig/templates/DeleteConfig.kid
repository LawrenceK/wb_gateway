<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
  <title>WebBrick Configuration Manager - Delete configuration set</title>
  <!-- Template inputs: 
       ConfigSet, ConfigNode, ConfigName
    -->  
</head>

<body>
  <form name="DeleteConfig" action="/wbcnf/DeleteConfig" method="post">
    <input type="hidden" id="WbConfigSet"  name="WbConfigSet" value="${ConfigSet}" /> 
    <input type="hidden" id="WbConfigNode" name="WbConfigNode" value="${ConfigNode}" /> 
    <input type="hidden" id="WbConfigName" name="WbConfigName" value="${ConfigName}" /> 
    <p>
      This option will delete the specified WebBrick configuration file <b>${ConfigSet}/${ConfigNode} (${ConfigName})</b>.
    </p>
    <h3>
      Delete WebBrick configuration <b>${ConfigSet}/${ConfigNode}</b> -- ARE YOU SURE?
    </h3>
    <p>
      <button type="submit" name="Confirm">Delete</button>
      <button type="submit" name="Cancel" >Cancel</button>
    </p>
  </form>
</body>

</html>
