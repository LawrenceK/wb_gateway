<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>

<!-- TODO change SampleWb to target correct webbrick 
    Related Event Despatch files are: 
            - fanconversions.xml
            - fansglobal.xml
            - fanslocal.xml
            -->



<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Bathroom Ventilation")}

<body>

${output_nav("Bathroom Ventilation")}

<table>
	<colgroup span="5" width="20"></colgroup>
    
    <tr>
        <td colspan="3" wbType="Caption" wbLoad="loadCaption()">Downstairs Temp, Humidy and Fan Control</td>
    </tr>
    <tr>
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/SampleWb/Tmp/0'
                            minvalue="0"
                            maxvalue="40"
                            curvalue="0"
                            setlow="19"
                            sethigh="24"
                            metertitle="Temp"
                            labels="0,10,20,30,40"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>      
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","%")'
                            wbSource='/eventstate/HumDownWC'
                            minvalue="20"
                            maxvalue="60"
                            curvalue="0"
                            setlow="30"
                            sethigh="50"
                            metertitle="Humidity"
                            labels="20,30,40,50,60"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
        
        
        <!-- 
-->
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","%")'
                            wbSource='/wbsts/SampleWb/AO/0'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="65"
                            sethigh="85"
                            metertitle="Fan Speed"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>     
        
        <wb:simpleButton 
            colspan="1"
            wbTarget="/sendevent/fans/downstairs/10Min">10 Minute Run
        </wb:simpleButton>        
        <wb:numericEntry 
            colspan="1"
            prefix="Run Time: " 
            format="##" 
            postfix=" sec"
            wbSource="/eventstate/fans/downstairs/dwDuration" 
            wbTarget="/sendevent/fans/downstairs/dwDuration?type=http://id.webbrick.co.uk/events/config/set">
            fanspeed
        </wb:numericEntry>
    </tr>
    <tr>
        
        <wb:enableEntry
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbSource="/eventstate/fans/downstairs/PIRenabled"
                    wbTarget="/sendevent/fans/downstairs/PIRenabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="PIR Enable"
                    />
        <wb:numericEntry 
            colspan="1"
            prefix="Humidity Threshold: " 
            format="##" 
            postfix="%"
            wbSource="/eventstate/hum/downstairs/threshold" 
            wbTarget="/sendevent/hum/downstairs/threshold?type=http://id.webbrick.co.uk/events/config/set">
            humidity threshold
        </wb:numericEntry>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td colspan="3" wbType="Caption" wbLoad="loadCaption()">Upstairs Temp, Humidy and Fan Control</td>
    </tr>
    <tr>
        <!--   -->
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/SampleWb/Tmp/1'
                            minvalue="0"
                            maxvalue="40"
                            curvalue="0"
                            setlow="19"
                            sethigh="24"
                            metertitle="Temp"
                            labels="0,10,20,30,40"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","%")'
                            wbSource='/eventstate/HumUpWC'
                            minvalue="20"
                            maxvalue="60"
                            curvalue="0"
                            setlow="30"
                            sethigh="50"
                            metertitle="Humidity"
                            labels="20,30,40,50,60"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
        <!--wbSource='/wbsts/SampleWb/AO/3' -->
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","%")'
                            wbSource='/wbsts/SampleWb/AO/1'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="65"
                            sethigh="85"
                            metertitle="Fan Speed"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
        
        <wb:simpleButton 
            colspan="1"
            wbTarget="/sendevent/fans/upstairs/10Min">10 Minute Run
        </wb:simpleButton>
        
        <wb:numericEntry 
            colspan="1"
            prefix="Run Time: " 
            format="##" 
            postfix=" sec"
            wbSource="/eventstate/fans/upstairs/dwDuration" 
            wbTarget="/sendevent/fans/upstairs/dwDuration?type=http://id.webbrick.co.uk/events/config/set">
            fanspeed
        </wb:numericEntry>
    </tr>
    <tr>
        
        <wb:enableEntry
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbSource="/eventstate/fans/upstairs/PIRenabled"
                    wbTarget="/sendevent/fans/upstairs/PIRenabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="PIR Enable"
                    />
        <wb:numericEntry 
            colspan="1"
            prefix="Humidity Threshold: " 
            format="##" 
            postfix="%"
            wbSource="/eventstate/hum/upstairs/threshold" 
            wbTarget="/sendevent/hum/upstairs/threshold?type=http://id.webbrick.co.uk/events/config/set">
            fanspeed
        </wb:numericEntry>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td colspan="3" wbType="Caption" wbLoad="loadCaption()">Ensuite Temp, Humidy and Fan Control</td>
    </tr>
    <tr>
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/SampleWb/Tmp/2'
                            minvalue="0"
                            maxvalue="40"
                            curvalue="0"
                            setlow="19"
                            sethigh="24"
                            metertitle="Temp"
                            labels="0,10,20,30,40"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>        
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","%")'
                            wbSource='/eventstate/HumEnSuite'
                            minvalue="20"
                            maxvalue="60"
                            curvalue="0"
                            setlow="30"
                            sethigh="50"
                            metertitle="Humidity"
                            labels="20,30,40,50,60"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
        <!-- Need to create conversion of some kind to map 0-> 0 and 1 -> 100-->
        <td rowspan='3' width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","%")'
                            wbSource='/eventstate/fans/ensuite/speed'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="65"
                            sethigh="85"
                            metertitle="Fan Speed"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
         
         
         
         
         <wb:simpleButton 
            colspan="1"
            wbTarget="/sendevent/fans/ensuite/10Min">10 Minute Run
        </wb:simpleButton>        
        <wb:numericEntry 
            colspan="1"
            prefix="Run Time: " 
            format="##" 
            postfix=" sec"
            wbSource="/eventstate/fans/ensuite/dwDuration" 
            wbTarget="/sendevent/fans/ensuite/dwDuration?type=http://id.webbrick.co.uk/events/config/set">
            fanspeed
        </wb:numericEntry>
    </tr>
    <tr>
        
        <wb:enableEntry
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbSource="/eventstate/fans/ensuite/PIRenabled"
                    wbTarget="/sendevent/fans/ensuite/PIRenabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="PIR Enable"
                    />
        <wb:numericEntry 
            colspan="1"
            prefix="Humidity Threshold: " 
            format="##" 
            postfix="%"
            wbSource="/eventstate/hum/ensuite/threshold" 
            wbTarget="/sendevent/hum/ensuite/threshold?type=http://id.webbrick.co.uk/events/config/set">
            humidity threshold
        </wb:numericEntry>
    </tr>
    <tr>
        <td>&nbsp;</td>
    </tr>
    
</table>

${output_site_info_bar()}

</body>

</html>
