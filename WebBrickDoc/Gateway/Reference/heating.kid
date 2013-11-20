<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Webbrick Gateway Heating")}

<body>

${output_nav("Heating")}
  
<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <wb:caption>Upstairs Zone</wb:caption>
    </tr>
    <tr>  
        <wb:simpleButton wbTarget="/wbcmd/test/DI/0" wbSource="/wbsts/test/DO/0">
            Ensuite Fan
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/DI/1" wbSource="/wbsts/test/DO/1">
            Zone Valve
        </td>
    </tr>
</table>



<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <wb:caption colspan="4">Heating and Ventilation</wb:caption>
    </tr>
    <tr>  
        <wb:simpleButton wbTarget="/wbcmd/test/DI/5" wbSource="/wbsts/test/DO/5">
            Boiler
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/DI/2" wbSource="/wbsts/test/DO/2">
            Radiator Valve
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/wbcmd/test/DI/3" wbSource="/wbsts/test/DO/3">
            Radiator
        </wb:simpleButton>
    </tr>
</table>
  
<table>
    <tr>
        <wb:caption>Key Temperatures</wb:caption>
    </tr>
    <tr>
        <td width='50%'>
            <table class='compositeWidget'>
                <tr>
                    <wb:numericDisplay prefix="CH Flow: " format="##.#" postfix="&ordm;C"
                            wbSource='/wbsts/test/Tmp/4' width='20%'>
                        &nbsp;
                    </wb:numericDisplay>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/>
                    </td>
                </tr>
                <tr>
                    <td class='NumericBar' id='ambientTemp'
                            wbType="NumericBar" 
                            wbSource='/wbsts/test/Tmp/4'
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
                    <wb:numericDisplay prefix="CH Return: " format="##.#" postfix="&ordm;C"
                            wbSource='/wbsts/test/Tmp/0' width='20%'>
                        &nbsp;
                    </wb:numericDisplay>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/>
                    </td>
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
    </tr>
    <tr>
        <td width='50%'>
            <table class='compositeWidget'>
                <tr>
                    <wb:numericDisplay prefix="HW Flow: " format="##.#" postfix="&ordm;C"
                            wbSource='/wbsts/test/Tmp/2' width='20%'>
                        &nbsp;
                    </wb:numericDisplay>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/>
                    </td>
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
                    <wb:numericDisplay prefix="HW Return: " format="##.#" postfix="&ordm;C"
                            wbSource='/wbsts/test/Tmp/1' width='20%'>
                        &nbsp;
                    </wb:numericDisplay>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/>
                    </td>
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
        <td>
            <table class='compositeWidget'>
                <tr>
                    <wb:numericDisplay prefix="Ambient: " format="##.#" postfix="&ordm;C"
                            wbSource='/wbsts/test/Tmp/3' width='20%'>
                        &nbsp;
                    </wb:numericDisplay>
                </tr>
                <tr>
                    <td class='NumericBar'><img src="/static/images/tempfade.png" width="100%" height="10"/>
                    </td>
                </tr>
                <tr>
                    <td class='NumericBar' id='ambientTemp'
                            wbType="NumericBar" 
                            wbSource='/wbsts/test/Tmp/3'
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
