<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:ui="ui" 
    py:extends="'master.kid'">

${output_head( "Schedules" )}

<body>
    ${output_nav("Heating Schedule")}

<table class="rule"><tr><td class='ruleBar'></td></tr></table>

    <table>

        <tr>
            <th>Time</th>
            <th>Days</th>
	    <th py:for='dev in devicesOnOff'>${devicesOnOff[dev]}</th>
	    <th py:for='dev in devicesTemp'>${devicesTemp[dev][0]}</th>
        </tr>
        <tr>
            <td class='numericPresent' colspan='2'>Current</td>

	    <td py:for='dev in devicesOnOff' wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/heating/control/${dev}"
                wbSource="/heating/current/${dev}">&nbsp;
            </td>
	    <td py:for='dev in devicesTemp' wbType="NumericDisplay" wbLoad='loadNumericDisplay("","##.#","&ordm;C")'
                wbTarget="/heating/control/${dev}/${devicesTemp[dev][1]}"
                wbSource="/heating/current/${dev}">&nbsp;
            </td>
        </tr>
        <tr py:for="sched in schedules">
	    <td wbType="WbTimeEntry"
                noPolling="yes"
                wbTitle="${sched}/day ${sched}/time"
                wbSource="/heating/schedule/${sched}/time"
                wbTarget="/heating/configure/time/${sched}" >
                &nbsp;
            </td>
	    <td wbType="WbDayEntry"
                noPolling="yes"
                wbTitle="${sched}/day ${sched}/time"
                wbSource="/heating/schedule/${sched}/day"
                wbTarget="/heating/configure/day/${sched}" >
                &nbsp;
            </td>
	    <td py:for='dev in devicesOnOff' wbType="WbOnOffEntry"
                noPolling="yes"
                wbTitle="${sched} ${devicesOnOff[dev]}"
                wbTarget="/heating/configure/device/${sched}/${dev}"
                wbSource="/heating/action/${sched}/${dev}">
            </td>
	    <td py:for='dev in devicesTemp' wbType="WbNumericEntry" wbLoad='loadWbNumericEntry("","##.#","&ordm;C")'
                noPolling="yes"
                wbTitle="${sched} ${devicesTemp[dev][0]}"
                wbTarget="/heating/configure/device/${sched}/${dev}"
                wbSource="/heating/action/${sched}/${dev}">
            </td>
        </tr>

    </table>

    ${output_site_info_bar()}

<script language="javascript">
    pollerInterval = 10.0;
    pollerSoonDelay = 2.0;
</script>

</body>

</html>
