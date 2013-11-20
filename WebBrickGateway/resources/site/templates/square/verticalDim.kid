<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Vertical Dimmer Example")}

<body>

${output_nav("Vertical Dimmers")}
  
<table>
    <tr>
        <wb:flashDimmer
                width='90px' height='440px'
                wbSource='/wbsts/UnNamed/AO/0'
                labels='0,25,50,75,100'
                wbTarget='/wbcmd/UnNamed/AA/0/'
                title="VerticalSlider"
                flashMovie="VerticalSlider.swf"
            />
                
        <wb:flashDimmer
                width='90px' height='440px'
                wbSource='/wbsts/UnNamed/AO/1'
                labels='0,25,50,75,100'
                wbTarget='/wbcmd/UnNamed/AA/1/'
                title="VerticalSliderCirc"
                flashMovie="VerticalSliderCirc.swf"
            />
                
        <wb:flashDimmer
                width='90px' height='440px'
                wbSource='/wbsts/UnNamed/AO/2'
                labels='0,25,50,75,100'
                wbTarget='/wbcmd/UnNamed/AA/2/'
                title="VerticalSliderHeat"
                flashMovie="VerticalSliderHeat.swf"
            />
        <wb:flashDimmer
                width='90px' height='440px'
                wbSource='/wbsts/UnNamed/AO/3'
                labels='0,25,50,75,100'
                wbTarget='/wbcmd/UnNamed/AA/3/'
                title="default"
            />
    </tr>
</table>

${output_site_info_bar()}

</body>
</html>
