<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
import WebBrickGateway.templates.embedschedule
import WebBrickGateway.templates.widgets
val = "unset"
test = "unset"
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master, WebBrickGateway.templates.embedschedule, WebBrickGateway.templates.widgets">

<!-- Replace SampleWb/DI/4 with relevant webbrick 
    Related Event Despatch files are: 
            - gate.xml
            -->
    
${output_head("Template_Test")}

<body>


<table>
    <colgroup span="2" width="50%"/>
    <tr>
        <td>
            <div>
                ${val}
            </div>
        </td>
        <td>
            <div>
                ${test}
            </div>
        </td>
   </tr>
</table>
</body>
</html>
