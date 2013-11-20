<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" 
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
	    <wb:timeEntry
                noPolling="yes"
                wbTitle="${sched}/day ${sched}/time"
                wbTarget="/sendevent/schedule/heating/${sched}?type=http://id.webbrick.co.uk/events/config/set"
                wbSource="/eventstate/schedule/heating/${sched}?attr=time"/>
	    <wb:dayEntry wbType="WbDayEntry"
                noPolling="yes"
                wbTitle="${sched}/day ${sched}/time"
                wbTarget="/sendevent/schedule/heating/${sched}?type=http://id.webbrick.co.uk/events/config/set"
                wbSource="/eventstate/schedule/heating/${sched}?attr=day"/>
	    <wb:onoffEntry py:for='dev in devicesOnOff'
                noPolling="yes"
                wbTitle="${sched} ${devicesOnOff[dev]}"
                wbTarget="/sendevent/schedule/heating/${sched}/${dev}?type=http://id.webbrick.co.uk/events/config/set"
                wbSource="/eventstate/schedule/heating/${sched}/${dev}?attr=onoff" />
	    <wb:numericEntry py:for='dev in devicesTemp' 
                prefix="" format="##.#" postfix="&ordm;C"
                noPolling="yes"
                wbTitle="${sched} ${devicesTemp[dev][0]}"
                wbTarget="/sendevent/schedule/heating/${sched}/${dev}?type=http://id.webbrick.co.uk/events/config/set"
                wbSource="/eventstate/schedule/heating/${sched}/${dev}" />
        </tr>

    </table>

    ${output_site_info_bar()}

<script language="javascript">
    pollerInterval = 10.0;
    pollerSoonDelay = 2.0;
</script>

</body>

</html>
