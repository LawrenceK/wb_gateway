<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Webbrick Gateway Overview")}

<body>

${output_nav("Overview")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Lights and Levels</td>
    </tr>
    <tr>
        <wb:numericDisplay wbSource="/wbsts/test/AO/0" prefix="An Out 1: " format="##.#" postfix="%">(AO0 value here)</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/test/AO/1" prefix="An Out 2: " format="##.#" postfix="%">(AO1 value here)</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/test/AO/2" prefix="An Out 3: " format="##.#" postfix="%">(AO2 value here)</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/test/AO/3" prefix="An Out 4: " format="##.#" postfix="%">(AO3 value here)</wb:numericDisplay>
    </tr>

    <tr>
        <td class='NumericBar'><img src="/static/images/whitefade.png" width="100%" height="10"/></td>
        <td class='NumericBar'><img src="/static/images/whitefade.png" width="100%" height="10"/></td>
        <td class='NumericBar'><img src="/static/images/whitefade.png" width="100%" height="10"/></td>
        <td class='NumericBar'><img src="/static/images/whitefade.png" width="100%" height="10"/></td>
    </tr>
  
    <tr>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AO/0'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AO/1'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AO/2'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AO/3'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
    </tr>
</table>

<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <wb:numericDisplay wbSource="/wbsts/test/AI/0" prefix="An In 1: " format="##.#" postfix="%">(In0 value here)</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/test/AI/1" prefix="An In 2: " format="##.#" postfix="%">(In1 value here)</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/test/AI/2" prefix="An In 3: " format="##.#" postfix="%">(In2 value here)</wb:numericDisplay>
        <wb:numericDisplay wbSource="/wbsts/test/AI/3" prefix="An In 4: " format="##.#" postfix="%">(In3 value here)</wb:numericDisplay>
    </tr>

    <tr>
        <td class='NumericBar'><img src="/static/images/whitefade.png" width="100%" height="10"/></td>
        <td class='NumericBar'><img src="/static/images/bluefade.png" width="100%" height="10"/></td>
        <td class='NumericBar'><img src="/static/images/redfade.png" width="100%" height="10"/></td>
        <td class='NumericBar'><img src="/static/images/blackfade.png" width="100%" height="10"/></td>
    </tr>

    <tr>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AI/0'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AI/1'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AI/2'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
        <td class='NumericBar' id='ambientTemp'
            wbType="NumericBar" 
            wbSource='/wbsts/test/AI/3'
            graphic0="/static/images/clear.png"
            graphic1="/static/images/WhiteVPointer.png"
            graphic2="/static/images/clear.png"
            curvalue="0"
            height="10px">
	</td>
    </tr>
</table>


<table>
    <tr>
        <td colspan="1" wbType="Caption" wbLoad="loadCaption()">Temperatures</td>
    </tr>
    <tr>
        <td width='50%'>
            <table class='compositeWidget'>
                <tr>
                    <td wbType="Numeric" wbLoad='loadNumericDisplay("Sensor 1: ","##.#","&deg;C")'
                        wbSource='/wbsts/test/Tmp/0' width='20%'>&nbsp;</td>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/></td>
                </tr>
                <tr>
                    <td class='NumericBar' id='ambientTemp'
                            wbType="NumericBar" 
                            wbSource='/wbsts/test/Tmp/0'
                            minvalue="-5"
                            maxvalue="70"
                            graphic0="/static/images/clear.png"
                            graphic1="/static/images/WhiteVPointer.png"
                            graphic2="/static/images/clear.png"
                            curvalue="0"
                            height="10px" width='80%' >
                    </td> 
                </tr>
            </table>
        </td>
        <td width='50%'>
            <table class='compositeWidget'>
                <tr>
                    <td wbType="Numeric" wbLoad='loadNumericDisplay("Sensor 2: ","##.#","&deg;C")'
                        wbSource='/wbsts/test/Tmp/1' width='20%'>&nbsp;</td>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/></td>
                </tr>
                <tr>
                    <td class='NumericBar' id='ambientTemp'
                            wbType="NumericBar" 
                            wbSource='/wbsts/test/Tmp/1'
                            minvalue="-5"
                            maxvalue="70"
                            graphic0="/static/images/clear.png"
                            graphic1="/static/images/WhiteVPointer.png"
                            graphic2="/static/images/clear.png"
                            curvalue="0"
                            height="10px" width='80%' >
                    </td> 
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td width='50%'>
            <table class='compositeWidget'>
                <tr>
                    <td wbType="Numeric" wbLoad='loadNumericDisplay("Sensor 3: ","##.#","&deg;C")'
                        wbSource='/wbsts/test/Tmp/2' width='20%'>&nbsp;</td>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/></td>
                </tr>
                <tr>
                    <td class='NumericBar' id='ambientTemp'
                            wbType="NumericBar" 
                            wbSource='/wbsts/test/Tmp/2'
                            minvalue="-5"
                            maxvalue="70"
                            graphic0="/static/images/clear.png"
                            graphic1="/static/images/WhiteVPointer.png"
                            graphic2="/static/images/clear.png"
                            curvalue="0"
                            height="10px" width='80%' >
                    </td> 
                </tr>
            </table>
        </td>
        <td width='50%'>
            <table class='compositeWidget'>
                <tr>
                    <td wbType="Numeric" wbLoad='loadNumericDisplay("Sensor 4: ","##.#","&deg;C")'
                        wbSource='/wbsts/test/Tmp/3' width='20%'>&nbsp;</td>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/></td>
                </tr>
                <tr>
                    <td class='NumericBar' id='ambientTemp'
                            wbType="NumericBar" 
                            wbSource='/wbsts/test/Tmp/3'
                            minvalue="-5"
                            maxvalue="70"
                            graphic0="/static/images/clear.png"
                            graphic1="/static/images/WhiteVPointer.png"
                            graphic2="/static/images/clear.png"
                            curvalue="0"
                            height="10px" width='80%' >
                    </td> 
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td>
            <table class='compositeWidget'>
                <tr>
                    <td wbType="Numeric" wbLoad='loadNumericDisplay("Sensor 5: ","##.#","&deg;C")'
                        wbSource='/wbsts/test/Tmp/4' width='20%'>&nbsp;</td>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/></td>
                </tr>
                <tr>
                    <td class='NumericBar' id='ambientTemp'
                            wbType="NumericBar" 
                            wbSource='/wbsts/test/Tmp/4'
                            minvalue="-5"
                            maxvalue="40"
                            graphic0="/static/images/clear.png"
                            graphic1="/static/images/WhiteVPointer.png"
                            graphic2="/static/images/clear.png"
                            curvalue="0"
                            height="10px" width='80%' >
                    </td> 
                </tr>
            </table>
        </td>
        <td>&nbsp;</td>
    </tr>
</table>


${output_site_info_bar()}

</body>

</html>
