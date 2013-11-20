<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway Overview")}

<body>

${output_nav("Overview")}
  
<table>
    <tr>
        <td width='200px' height='200px'
                            wbType="FlashButton" 
                            wbSource='/wbsts/test/DO/6/toggle'
                            wbTarget='/wbcmd/test/DI/6'
                            flashMovie="/static/flash/ButtonTemplate.swf"
                            >
        </td>
        <td width='200px' height='200px'
                            wbType="FlashButton" 
                            wbSource='/wbsts/test/DO/7/toggle'
                            wbTarget='/wbcmd/test/DI/7'
                            flashMovie="/static/flash/ButtonTemplate.swf"
                            >
        </td>
    </tr>
</table>

</body>

</html>
