<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Webbrick Gateway Overview")}

<body class='plainWhite'>

${output_nav("Overview")}
  
<table>
    <tr>
        <td rowspan='2' width='220px' height='220px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/house2/Tmp/1'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="0"
                            sethigh="100"
                            metertitle="Hot Water"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
        <td width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/house2/Tmp/2'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="0"
                            sethigh="100"
                            metertitle="HW Flow"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
   </tr>
   <tr>
        <td width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/house2/Tmp/0'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="0"
                            sethigh="100"
                            metertitle="HW Return"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
   </tr>


   <tr>
        <td rowspan='2' width='220px' height='220px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/eventstate/temperature/outside'
                            minvalue="-20"
                            maxvalue="60"
                            curvalue="0"
                            setlow="-5"
                            sethigh="35"
                            metertitle="Outside"
                            labels="-20,0,20,40,60"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
         </td>

        <td width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/house2/Tmp/4'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="0"
                            sethigh="100"
                            metertitle="CH Flow"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>

   </tr>
   <tr>

        <td width='100px' height='100px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/house2/Tmp/3'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="0"
                            sethigh="100"
                            metertitle="CH Return"
                            labels="0,25,50,75,100"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>


    </tr>
</table>
${output_site_info_bar()}

</body>

</html>
