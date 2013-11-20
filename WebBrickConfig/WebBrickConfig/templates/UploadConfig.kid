<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
  <title>WebBrick Configuration Manager - Upload WebBrick Configuration(s)</title>
</head>

<body>
  <form name="UploadConfig" action="/wbcnf/UploadConfig" 
        method="post" enctype="multipart/form-data">
    <table border="0" cellpadding="2" cellspacing="2">
    <tbody>
    <tr>
      <td colspan="2">
        <h3>Upload to</h3>
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
      <td colspan="2">
        <h3>Upload from</h3>
      </td>
    </tr>
    <tr>
      <td>
        Configuration file&nbsp;&nbsp;
      </td>
      <td>
        <input type="file" name="ConfigFile" size="60" maxlength="1024" />
      </td>
    </tr>
    </tbody>
    </table>
    <p>
      <button type="submit" name="Confirm">Upload</button>
      <button type="submit" name="Cancel" >Cancel</button>
    </p>
  </form>
</body>

</html>
