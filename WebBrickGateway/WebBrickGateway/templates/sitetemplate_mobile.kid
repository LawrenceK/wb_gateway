<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" >

<!--  This is the MOBILE version, therefore it has a different homepage -->


<table py:def="output_nav( location )" class="navTable">
    <tr>
        <wb:simpleLink width="20%" target="/template/mobile/welcome">Home</wb:simpleLink>
        <td class="infoBar" id="menuTitle">${location}</td>
        <!-- !Needs conversion for non javascript -->
        <td width="12%" class="navBarSmall" onClick="history.back()">Back</td>
        <wb:simpleLink width="12%" target="/template/guide">Guide</wb:simpleLink>
    </tr>
    <tr class="rule"><td colspan='4' class="ruleBar">&nbsp;</td></tr>
</table>

<!-- The default site/location info bar -->
<table py:def="output_site_info_bar()" class="infoTable">
  <tr>
    <wb:textDisplay width='8%' wbSource="/local/time" prefix="" postfix="">Left</wb:textDisplay>
    <wb:textDisplay wbSource="/local/messages" prefix="" postfix="&nbsp;">Middle</wb:textDisplay>
    <td width="1px" wbType="Indicator" wbLoad="loadButton()"
        wbSource="/eventstate/occupants/home"
        stateVals="Away,Home"
        baseClassName="status"
        >
        &nbsp;
    </td>
    <td width="1px" wbType="Indicator" wbLoad="loadButton()"
        wbSource="/eventstate/zone1?attr=state"
        stateVals="Idle,WillRun,Suppress,Vacation,Locked"
        baseClassName="status"
        >
        &nbsp;
    </td>
    <td width="1px" wbType="Indicator" wbLoad="loadButton()"
        wbSource="/eventstate/earlyStart/enabled"
        stateVals="Blank,Bird"
        baseClassName="status"
        >
        <img width="0px" src='/static/images/clear.png' />
    </td>
    <wb:numericDisplay width='18%' wbSource="/eventstate/temperature/outside" prefix="Outside:" format="##.#" postfix="&ordm;C">Right</wb:numericDisplay>
  </tr>
</table>

</html>
