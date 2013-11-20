<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master

#graphbase = "".join(file("/home/webbrick/graph.prop").readlines())
    
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

<script src="/static/javascript/graphs/swfobject.js" type="text/javascript"></script>
<script src="/static/javascript/graphs/json2.js" type="text/javascript"></script>


${output_head("WebBricks - powering the BASF Eco Home")}

<body>

${output_nav("WebBrick Gateway")}

<table class="navTable">
    <colgroup span="3" width="33%"></colgroup>

    <tr>
        
        <wb:flashGraph 
                width="800"
                height="600"
                minYval="0"
                maxYval="50"
                graphStyle="graph.prop"
                activeSeries="0,1,2,3"
                dataset="/home/webbrick/graph.prop">  
            
            Graph Title
        </wb:flashGraph>
        
    </tr>
</table>

${output_site_info_bar()}

</body>
</html>
