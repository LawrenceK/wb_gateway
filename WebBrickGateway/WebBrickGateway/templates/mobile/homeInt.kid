<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="'master.kid'">

${output_head("Admin Stuff")}

<body>

${output_nav("Home Intelligence")}

<table>
	<colgroup span="3" width="33%"></colgroup>
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
  </tr>
  <tr>
		<td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/CHCall/On" >
            Call for Heat
    	</td>
		<td  wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/sendevent/CHCall/Off" >
            Cancel Heat
    	</td>
		<td  wbType="Indicator" wbLoad="loadButton()"
			wbSource="/eventstate/heating/compensation"
			stateVals="WillRun,Suppress,Idle,Vacation"
			baseClassName="indicator"
			>
		Status
		</td>
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
        <wb:numericDisplay wbSource="/wbsts/house2/Tmp/1" prefix="Hot Water: " format="##.#" postfix="&ordm;C">--</wb:numericDisplay>
  </tr>
</table>

</body>

</html>
