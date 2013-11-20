<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("WebBrick Gateway Day Phase")}
<!-- <link href="/static/css/wl-panel.css" rel="stylesheet" /> -->

<body>

${output_nav("Phases of your day")}

<table width="70%">
	<colgroup>
		<col width="20%" />
		<col width="60%" />
		<col width="20%" />
	</colgroup>
    <tr>
        <td colspan="3" class="infoBar">Weekday Day Phases</td>
    </tr>

    <tr>
        <td>Morning</td>
        <td>Getting up, getting ready to go out</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekday/morning?attr=time" 
            wbTarget="/sendevent/dayphase/weekday/morning?type=http://id.webbrick.co.uk/events/config/set"/>
    </tr>

    <tr>
        <td>Day</td>
        <td>Out at school, work, etc.</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekday/day?attr=time" 
            wbTarget="/sendevent/dayphase/weekday/day?type=http://id.webbrick.co.uk/events/config/set"/>
    </tr>

    <tr>
        <td>Evening</td>
        <td>Coming home, eating, recreation, etc.</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekday/evening?attr=time" 
            wbTarget="/sendevent/dayphase/weekday/evening?type=http://id.webbrick.co.uk/events/config/set"/>
    </tr>

    <tr>
        <td>Night</td>
        <td>Sleeping</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekday/night?attr=time" 
            wbTarget="/sendevent/dayphase/weekday/night?type=http://id.webbrick.co.uk/events/config/set"/>
    </tr>


    <tr>
        <td colspan="3" class="infoBar">Weekend Day Phases</td>
    </tr>


    <tr>
        <td>Morning</td>
        <td>Getting up, breakfast, showers etc</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekend/morning?attr=time" 
            wbTarget="/sendevent/dayphase/weekend/morning?type=http://id.webbrick.co.uk/events/config/set"/>
    </tr>

    <tr>
        <td>Day</td>
        <td>Recreation, Lunch</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekend/day?attr=time" 
            wbTarget="/sendevent/dayphase/weekend/day?type=http://id.webbrick.co.uk/events/config/set"/>
    </tr>

    <tr>
        <td>Evening</td>
        <td>Supper etc</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekend/evening?attr=time" 
            wbTarget="/sendevent/dayphase/weekend/evening?type=http://id.webbrick.co.uk/events/config/set" />
    </tr>

    <tr>
        <td>Night</td>
        <td>Sleeping</td>
        <wb:timeEntry wbSource="/eventstate/dayphase/weekend/night?attr=time" 
            wbTarget="/sendevent/dayphase/weekend/night?type=http://id.webbrick.co.uk/events/config/set" />
    </tr>
    <tr>
        <td><img width="80%" src="/static/images/Decorations/sun.png"/></td>
        <td>&nbsp;</td>
        <td><img width="80%" src="/static/images/Decorations/moon.png"/></td>
    </tr>

</table>

<!--
<table>


    <tr>
        <td>Example Day</td>
        <wb:timeEntry wbSource="/eventstate/example/day" 
            wbTarget="/sendevent/example/day?type=http://id.webbrick.co.uk/events/config/set" />
    </tr>

    <tr>
        <td>Example SetPoint</td>
        <wb:numericEntry wbSource="/eventstate/heating/compensation/outsideThreshold" 
            wbTarget="/sendevent/heating/compensation/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set" />
    </tr>


</table>
-->
${output_site_info_bar()}

</body>
</html>
