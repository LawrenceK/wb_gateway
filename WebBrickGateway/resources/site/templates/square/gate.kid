<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
import WebBrickGateway.templates.embedschedule
import WebBrickGateway.templates.widgets
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master, WebBrickGateway.templates.embedschedule, WebBrickGateway.templates.widgets">

<!-- Replace SampleWb/DI/4 with relevant webbrick 
    Related Event Despatch files are: 
            - gate.xml
            -->
    
${output_head("Gate Control")}

<body>

${output_nav("Gate Control")}

<table>
    <colgroup span="2" width="50%"/>
    <tr>
        <td>
            <div>
                ${output_schedule("gate")}
            </div>
        </td>
        <td>
            <div>
                
                <table>
                    <colgroup span="2" width="50%"/>
                    <tr>
                        <td colspan="2" class="NaN">Status</td>
                    </tr>
                    <tr>
                        <wb:simpleButton 
                            wbSource="/eventstate/gate/state" 
                            stateVals="Ajar,Closed,Open,Error"
                            wbTarget="/wbcmd/SampleWb/DI/4"
                            baseClassName="gate">
                            Open Gate
                        </wb:simpleButton>
                        <wb:enableEntry
                            baseClassName="entry"
                            stateVals="Blank,OK"
                            wbTitle="Auto Open Override"
                            wbSource="/eventstate/gate/enabled"
                            wbTarget="/sendevent/gate/enabled?type=http://id.webbrick.co.uk/events/config/set"
                            prefix="Auto Open Override"
                            />
                    </tr>  
                    <tr>
                        <td rowspan="5">
                            &nbsp;
                        </td>
                    </tr>
                </table>
            </div>
        </td>
   </tr>
</table>

${output_site_info_bar()}

</body>
</html>
