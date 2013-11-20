<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
  <title>WebBrick Configuration Manager - Delete configuration set</title>
</head>

<body>
  <form name="DeleteConfigSet" action="/wbcnf/DeleteConfigSet" method="post">
    <input type="hidden" id="WbConfigSet" name="WbConfigSet" value="${ConfigSet}" /> 
    <p>
      This option will delete all WebBrick configuration files in configuration set <b>"${ConfigSet}"</b>.
    </p>
    <h3>
      Delete WebBrick configuration set <b>"${ConfigSet}"</b> -- ARE YOU SURE?
    </h3>
    <p>
      <button type="submit" name="Confirm">Delete</button>
      <button type="submit" name="Cancel" >Cancel</button>
    </p>
  </form>
</body>

</html>
