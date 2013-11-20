<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Meters Example")}

<body>

${output_nav("Meters")}
  
<table>
    <tr>
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/0'
                labels='a,b,c,d,e'
                title="MeterBar"
                flashMovie="MeterBar.swf"
            >MeterBar</wb:flashMeter>
                
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/1'
                labels='a,b,c,d,e'
                title="MeterRadial270"
                flashMovie="MeterRadial270.swf"
            >MeterRadial270</wb:flashMeter>
                
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/2'
                labels='a,b,c,d,e'
                title="MeterRadial270L"
                flashMovie="MeterRadial270L.swf"
            >MeterRadial270L</wb:flashMeter>
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/3'
                labels='a,b,c,d,e'
                title="Simple270"
                flashMovie="Simple270.swf"
            >Simple270</wb:flashMeter>
    </tr>
    <tr>
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/0'
                labels='a,b,c,d,e'
                title="SimpleBar"
                flashMovie="SimpleBar.swf"
            >SimpleBar</wb:flashMeter>
                
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/1'
                labels='a,b,c,d,e'
                title="SimpleBarV"
                flashMovie="SimpleBarV.swf"
            >SimpleBarV</wb:flashMeter>
                
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/2'
                labels='a,b,c,d,e'
                title="SimpleBarV-VText"
                flashMovie="SimpleBarV-VText.swf"
            >SimpleBarV-VText</wb:flashMeter>
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/3'
                labels='a,b,c,d,e'
                title="ControlRadial270"
                flashMovie="ControlRadial270.swf"
            >ControlRadial270</wb:flashMeter>
    </tr>
    <tr>
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/0'
                labels='a,b,c,d,e'
                title="SimpleDamper"
                flashMovie="SimpleDamper.swf"
            >SimpleDamper</wb:flashMeter>
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/1'
                labels='a,b,c,d,e'
                title="SimpleFan"
                flashMovie="SimpleFan.swf"
            >SimpleFan</wb:flashMeter>
                
        <wb:flashMeter
                width='200px' height='200px'
                wbSource='/wbsts/UnNamed/AI/2'
                labels='a,b,c,d,e'
                title="SimpleFanCircle"
                flashMovie="SimpleFanCircle.swf"
            >SimpleFanCircle</wb:flashMeter>
    </tr>
                
</table>

${output_site_info_bar()}

</body>
</html>
