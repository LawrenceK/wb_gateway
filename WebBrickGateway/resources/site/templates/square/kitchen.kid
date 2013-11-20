<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Kitchen")}

<body>

${output_nav("Kitchen")}

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Lights</td>
    </tr>
    <tr>

        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen2/SC/0" >
            Lights Off
        </wb:simpleButton>
        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen2/SC/1" >
            Lights Low
        </wb:simpleButton>
        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen2/SC/0" >
            Lights Full
        </wb:simpleButton>
    </tr>
    <tr>
        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen2/SC/2" >
            Cooking
        </wb:simpleButton>
        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen2/SC/3" >
            Entertain
        </wb:simpleButton>
    </tr>

    <tr>
        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen/DI/0"
                wbSource="/wbsts/kitchen/DO/0">
            Heated Floor
        </wb:simpleButton>
        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen2/DI/4" >
            Door
        </wb:simpleButton>
    </tr>

    <tr>
        <wb:simpleButton 
                baseClassName="indicator"
                stateVals="Clear,NotReady"
                wbSource="/wbsts/kitchen/DI/3">
	    Coffee Ready
        </wb:simpleButton>

        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen/DI/1"
                wbSource="/wbsts/kitchen/DO/1">
            Coffee On
        </wb:simpleButton>

        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen/DI/2"
                wbSource="/wbsts/kitchen/DO/2">
            Coffee Expresso
        </wb:simpleButton>

        <wb:simpleButton 
                wbTarget="/wbcmd/kitchen/DI/10"
                wbSource="/wbsts/kitchen/DO/2">
            Coffee Longio
        </wb:simpleButton>
    </tr>
</table>

${output_site_info_bar()}

</body>

</html>
