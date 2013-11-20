<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Admin Stuff")}

<body>

${output_nav("Admin items not for Touch Screen")}

<table>
	<colgroup span="8" width="12%"></colgroup>
  <tr>
    <td colspan="4" wbType="Caption" wbLoad="loadCaption()">Information and Status</td>
	<td colspan="4" />
  </tr>
  <tr>
		<td colspan="1" wbType="Text" wbLoad='loadTextDisplay("Sunrise ","")'
				wbSource='/local/time?val=sunrise' />
		<td colspan="1" wbType="Text" wbLoad='loadTextDisplay("Sunset ","")'
				wbSource='/local/time?val=sunset' />
		<td colspan="1" wbType="Indicator" wbLoad="loadButton()"
			wbSource="/eventstate/lighting/isDark"
			stateVals="Day,Night"
			baseClassName="indicator"
			>
		&nbsp;
		</td>
    <wb:textDisplay colspan="2" wbSource="/eventstate/time/dayphasetext" prefix="Day Phase: " postfix="">Left</wb:textDisplay>
    <wb:textDisplay colspan="2" wbSource="/eventstate/time/dayphaseexttext" prefix="Day Phase: " postfix="">Left</wb:textDisplay>

	<td colspan="1" />

  </tr>
  <tr>
		<td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/time/sunrise?type=http://id.webbrick.co.uk/events/time/sunrise" >
            Do Sunrise
    	</td>
		<td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/time/sunset?type=http://id.webbrick.co.uk/events/time/sunset" >
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
	<td colspan="2" />
  </tr>
</table>


<table>
	<colgroup span="4" width="24%"></colgroup>
  <tr>
    <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Home Occupants</td>
    <td colspan="2" />
  </tr>
  <tr>
		<td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/arehome" >
            Set Home
    	</td>
		<td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/areaway" >
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
	<colgroup span="16" width="6%"></colgroup>
  <tr>
    <td colspan="16" wbType="Caption" wbLoad="loadCaption()">Intelligent Heating Controls</td>
  </tr>
  <tr>
		<td colspan="4" wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/CHCall/On" >
            Call for Heat
    	</td>
		<td colspan="4" wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/CHCall/Off" >
            Cancel Heat
    	</td>
		<td colspan="4" wbType="Indicator" wbLoad="loadButton()"
			wbSource="/eventstate/heating/compensation"
			stateVals="WillRun,Suppress,Idle,Vacation"
			baseClassName="indicator"
			>
		Status
		</td>
		<td colspan="4" />
  </tr>
  <tr>
		<td colspan="4" wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/HWCall/Boost" >
            Hot Water 46&ordm;C
    	</td>
		<td colspan="4" wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/HWCall/Reset" >
            Hot Water 30&ordm;C
    	</td>

		<td colspan="4" wbType="Indicator" wbLoad="loadButton()"
			wbSource="/eventstate/heating/inside/vacation"
			stateVals="Clear,Alert,Idle"
			baseClassName="indicator"
			>
		Frost Stat
		</td>
		<td colspan="4" />
  </tr>

</table>


<table>
	<colgroup span="4" width="25%"></colgroup>
  <tr>
    <td colspan="2" wbType="Caption" wbLoad="loadCaption()">Temporary Items - remove for show</td>
  </tr>

  <tr>
        <wb:simpleButton wbSource="/wbsts/mediawb/DO/5" wbTarget="/wbcmd/mediawb/DI/5">Media Amp</wb:simpleButton>
  </tr>

  <tr>
        <wb:simpleButton wbTarget="/sendevent/all/on">All Lights On</wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/sleep">Sleep House</wb:simpleButton>  
        <wb:simpleButton wbTarget="/template/templates/LEControl">LE 
Control</wb:simpleButton>  
  </tr>
</table>



${output_site_info_bar()}


</body>

</html>
