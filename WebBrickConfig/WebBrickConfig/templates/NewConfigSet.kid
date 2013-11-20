<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
  <title>WebBrick Configuration Manager - New configuration set</title>
</head>

<body>
  <form name="NewConfigSet" action="/wbcnf/NewConfigSet" method="post">
  <h3>Create WebBrick configuration set</h3>
    <p>Name for new configuration set:
      <input id="WbConfigSet" name="WbConfigSet" value="${ConfigSet}" />
    </p>
    <p>
      <button type="submit" name="Confirm">Create</button>
      <button type="submit" name="Cancel" >Cancel</button>
    </p>
  </form>
</body>

</html>
