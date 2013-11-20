<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway")}

<body>

${output_nav("Overview")}
  
<table>
    <tr>
        <td width='200px' height='200px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/ControlRadial270.swf"
                            >
        </td>
        <td width='200px' height='200px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/MeterRadial270.swf"
                            >
        </td>
    </tr>
</table>
<table>
    <tr>
        <td width='200px' height='200px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/MeterRadial270L.swf"
                            >
        </td>
        <td width='200px' height='200px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/Simple270.swf"
                            >
        </td>
    </tr>
</table>
<table>
    <tr>
        <td width='200px' height='200px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/SimpleBar.swf"
                            >
        </td>
        <td width='200px' height='200px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/ButtonTemplate.swf"
                            >
        </td>
    </tr>
</table>
<table>
    <tr>
        <td width='50px' height='250px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/SimpleBarV.swf"
                            >
        </td>
        <td width='50px' height='250px'
                            wbType="FlashMeter" 
                            wbLoad='loadFlashMeter("","##.#","&ordm;C")'
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            curvalue="0"
                            setlow="20"
                            sethigh="80"
                            flashMovie="/static/flash/SimpleBarV-VText.swf"
                            >
        </td>
    </tr>
</table>

</body>

</html>
