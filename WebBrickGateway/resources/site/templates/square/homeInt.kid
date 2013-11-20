<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Admin Stuff")}

<body>

${output_nav("Home Intelligence")}

<table>
    <colgroup span="6" width="15%"></colgroup>
    <tr>
        <td colspan="4" wbType="Caption" wbLoad="loadCaption()">Information and Status</td>
	<td colspan="2" />
    </tr>
    <tr>
        <td colspan="1" wbType="Text" wbLoad='loadTextDisplay("Sunrise ","")'
                wbSource='/local/time?val=sunrise' />
        <td colspan="1" wbType="Text" wbLoad='loadTextDisplay("Sunset ","")'
                wbSource='/local/time?val=sunset' />
        <td colspan="1" wbType="Indicator" wbLoad="loadButton()"
                wbSource="/eventstate/time/isDark?attr=state"
                stateVals="Day,Night"
                baseClassName="indicator"
            >
            &nbsp;
        </td>
        <wb:textDisplay colspan="2" wbSource="/eventstate/time/dayphase?attr=dayphasetext" prefix="Day Phase: " postfix="">Left</wb:textDisplay>
        <wb:textDisplay colspan="2" wbSource="/eventstate/time/dayphaseext?attr=dayphasetext" prefix="Day Phase: " postfix="">Left</wb:textDisplay>
        <td colspan="1" />
    </tr>
    <tr>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/sunrise" >
            Do Sunrise
    	</td>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/sunset" >
            Do Sunset
    	</td>		
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/dayphase/night" >
            Do Night
    	</td>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/dayphase/morning" >
            Do Morning
    	</td>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/dayphase/day" >
            Do Day
    	</td>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/dayphase/evening" >
            Do Evening
    	</td>
  </tr>
</table>


<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Home Occupants</td>
        <td colspan="2" />
    </tr>
    <tr>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/occupants/arehome" >
            Set Home
        </td>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/occupants/areaway" >
            Set Vacation
        </td>
        <td wbType="Indicator" wbLoad="loadButton()"
                wbSource="/eventstate/occupants/home"
                stateVals="Away,Home"
                baseClassName="indicator"
            >
            People
        </td>
        <td>&nbsp;</td>
    </tr>

</table>


<table>
    <colgroup span="4" width="25%"></colgroup>
    <tr>
        <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Intelligent Heating Controls</td>
    </tr>
    <tr>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/CHCall/On" >
            Call for Heat
    	</td>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/CHCall/Off" >
            Cancel Heat
    	</td>
<!-- TODO update to multi zone etc.
        <td wbType="Indicator" wbLoad="loadButton()"
                wbSource="/eventstate/heating/compensation"
                stateVals="WillRun,Suppress,Idle,Vacation"
                baseClassName="indicator"
                >
            Status
        </td>
-->
        <td colspan="1" />
    </tr>
    <tr>
        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/HWCall/Boost" >
            Hot Water 46&ordm;C
    	</td>

        <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/HWCall/Reset" >
            Hot Water 30&ordm;C
    	</td>

<!-- TODO update to multi zone etc.
        <td wbType="Indicator" wbLoad="loadButton()"
                wbSource="/eventstate/heating/inside/vacation"
                stateVals="Clear,Alert,Idle"
                baseClassName="indicator"
                >
            Frost Stat
        </td>
-->
        <td colspan="1" />
  </tr>

</table>

${output_site_info_bar()}


</body>

</html>
