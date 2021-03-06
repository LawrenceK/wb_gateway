<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" >

<table py:def="output_nav( location )" class="navTable">
    <tr>
        <td class="objCenter">
            <wb:simpleLink class="objCenter" target="/">Home</wb:simpleLink>
        </td>
        <td class="infoBar" id="menuTitle">${location}</td>
        <!-- !Needs conversion for non javascript -->
        <td class="objCenter">
            <wb:simpleLink class="objCenter" target="/template/guide">Guide</wb:simpleLink>
        </td>
        <td class="objCenter">
            <wb:simpleLink class="objCenter" >Back</wb:simpleLink>
        </td>
    </tr>
    <tr class="rule"><td colspan='4' class="ruleBar">&nbsp;</td></tr>
</table>

<!-- The default site/location info bar -->
<table py:def="output_site_info_bar()" class="infoTable">
  <tr>
    <td>
        <wb:textDisplay width='8%' wbSource="/local/time" prefix="" postfix="">Left</wb:textDisplay>
    </td>
    <td class="messageBar">
            <span 
                 wbType='textDisplay' 
                 wbSource="/local/messages" 
                 wbLoad='loadTextDisplay("&nbsp;","&nbsp;")'>
                 Messages
            </span>
            <span class="iconBar">
                <wb:imageIndicator wbSource="/eventstate/occupants/home"
                    imageUris="/static/images/vacation.png,/static/images/atHome.png"/>
                <wb:imageIndicator wbSource="/eventstate/zone1/state?attr=state"
                imageUris="/static/images/notReady.png,/static/images/clear.png,/static/images/HWActive.png"/>
                <wb:imageIndicator wbSource="/eventstate/earlyStart/enabled"
                    imageUris="/static/images/clear.png,/static/images/earlyBird.png"/>
        </span>
    </td>
    <td>
        <wb:numericDisplay width='18%' wbSource="/eventstate/temperature/outside" prefix="Outside:" format="##.#" postfix="&ordm;C">Right</wb:numericDisplay>
    </td>
  </tr>
</table>

</html>
