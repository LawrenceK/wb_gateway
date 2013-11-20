<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import embedschedule
import WebBrickGateway.templates.widgets_round
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="embedschedule, WebBrickGateway.templates.widgets_round">



<span py:def="output_zone_name( zone_key )">
    ${output_current_value( "/eventstate/%s/name?attr=name"%(zone_key) )}
<!--
        <div wbSource="/eventstate/${zone_key}/name?attr=name"
             wbLoad='loadTextDisplay("Zone: ","")'>
        Zone Name
        </div>
-->        
</span>

<span py:def="output_heating_schedule( zone_key, cur_zone_str )" py:strip="True">
     ${output_schedule("%s" % (zone_key) )}
</span>

<span py:def="output_zone_schedule( zone_key, cur_zone_str )" py:strip="True">
     ${output_schedule("%s" % (zone_key) )}
</span>


<span py:def="output_heating_overview( zone_key, cur_zone_str)">

    
    <!-- the right hand side -->
    <table>
    <colgroup span="3" width="33%"/>
    <tr>
        <td colspan="2" style="margin-left:5px"><h1>${output_current_value( '/eventstate/%s/name?attr=name'%zone_key ) } Heating Overview</h1></td>
    </tr>
    <tr>
        <td><div style="margin-left:16px">Status:</div></td>
        <td><div style="margin-left:16px">Supplied By:</div></td>
        <td><div style="margin-left:16px">Target Set By:</div></td>
    </tr>
    <tr>
        <!-- changed to zone state, in the case of a valve we can see what this is doing
        <td>
            <wb:textDisplay colspan="2" wbSource="/eventstate/${zone_key}/name?attr=name" prefix="" format="" postfix="">Zone Name
            </wb:textDisplay>
        </td>
        -->
        <td>
            <wb:simpleIndicatorButton
                    wbSource="/eventstate/${zone_key}/state?attr=state" 
                    stateVals="Locked,Idle,WillRun"
                    >
                <wb:textDisplay 
                        wbSource="/eventstate/${zone_key}/state?attr=status" 
                        prefix="" 
                        format="" 
                        postfix=""
                        >
                    &nbsp;
                </wb:textDisplay>
            </wb:simpleIndicatorButton>
        </td>
        <td>
            <wb:textDisplayButton
                    wbSource="/eventstate/${zone_key}/heatsource?attr=name" 
                    prefix="" 
                    format="" 
                    postfix=""
                    >
                &nbsp;
            </wb:textDisplayButton>
        </td>
        <td>
            <wb:textDisplayButton
                    wbSource="/eventstate/${zone_key}/state?attr=cmdsource"
                    prefix="[" 
                    postfix="]"
                    >
                &nbsp;
            </wb:textDisplayButton>
        </td>
    </tr>
    <tr>
        <td><div style="margin-left:16px">Temperatures:</div></td>
        <td>&nbsp;</td>
        <td><div style="margin-left:16px">Weather Comp:</div></td>
    </tr>
    <tr>

        <td>
            <wb:numericDisplayButton 
                    wbSource="/eventstate/${zone_key}/sensor?attr=val" 
                    prefix="Currently: " 
                    format="##.#" 
                    postfix="&ordm;C"
                    >
                &nbsp;
            </wb:numericDisplayButton>
        </td>
        <td>
            <wb:numericEntryButton 
                    wbSource="/eventstate/${zone_key}/state?attr=targetsetpoint"
                    wbTarget="/sendevent/${zone_key}/manual/set?type=http://id.webbrick.co.uk/events/zones/manual"
                    prefix="Target: " 
                    format="##.#" 
                    postfix="&ordm;C"
                    >
                &nbsp;
            </wb:numericEntryButton>
        </td>
        <td >
            <wb:simpleIndicatorButton
                wbLoad="loadButton()"
                wbSource='/eventstate/weather/${output_current_value( "/eventstate/%s/wcselect?attr=val"%zone_key ) }/?attr=istate' 
                stateVals="Suppress,WillRun"
                baseClassName="indicator">
                ${output_current_value( "/eventstate/%s/wcselect?attr=val"%zone_key ) }
            </wb:simpleIndicatorButton>
        </td>
    </tr>
    <tr>
        <th>&nbsp;</th>           
    </tr>
    <tr>
        <td><div style="margin-left:16px">Other Options:</div></td>
        <td>&nbsp;</td>           
        <td>&nbsp;</td>           
    </tr>
    <tr>
        <td >
            <wb:simpleLinkButton 
                    target="/template/${cur_zone_str}_heating_config"  
                    >
                Configuration
            </wb:simpleLinkButton>
        </td>
        <td >
            <wb:simpleLinkButton 
                    target="/template/${cur_zone_str}_heating_schedule"  
                    >
                Edit Schedule
            </wb:simpleLinkButton>
        </td>
        
    </tr>
    </table>

</span>

<span py:def="output_heating_config( zone_key, cur_zone_str  )">

    
    <!-- the right hand side -->
    <table>
    <colgroup span="3" width="33%"/>
    <tr>
        <td colspan="2" style="margin-left:5px"><h1>${output_current_value( '/eventstate/%s/name?attr=name'%zone_key ) } Heating Configuration</h1></td>
    </tr>
    <tr>
        <td><div style="margin-left:16px">Operating Options:</div></td>
        <td>&nbsp;</td>           
        <td><div style="margin-left:16px">Frost Stat:</div></td>        
    </tr>
    <tr>
        <td>
            <wb:enableEntryButton
                    baseClassName="entry"
                    stateVals="Locked,Tick"
                    wbTitle="Enable Zone"
                    wbSource="/eventstate/${zone_key}/enabled"
                    wbTarget="/sendevent/${zone_key}/enabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Zone Enable"
                    >
            </wb:enableEntryButton>
        </td>
        <td>
            <wb:enableEntryButton
                baseClassName="entry"
                stateVals="Blank,Tick"
                wbTitle="Follow Occupancy"
                wbSource="/eventstate/${zone_key}/occupancy"
                wbTarget="/sendevent/${zone_key}/occupancy?type=http://id.webbrick.co.uk/events/config/set"
                prefix="Occupancy"
                >
            </wb:enableEntryButton>
        </td>
        <td>
            <wb:numericEntryButton 
                wbSource="/eventstate/${zone_key}/matStat"
                wbTarget="/sendevent/${zone_key}/matStat?type=http://id.webbrick.co.uk/events/config/set"
                prefix="" 
                format="#" 
                postfix="&ordm;C">
            &nbsp;
            </wb:numericEntryButton>
        </td>
        
    </tr>
    <tr>
        <th>&nbsp;</th>           
    </tr>
    <tr>
        <td><div style="margin-left:16px">Weather Comp:</div></td>
    </tr>
    <tr>
        <td>
            <wb:numericEntryButton 
                width="200px"
                wbSource="/eventstate/${zone_key}/wcselect" 
                wbTarget="/sendevent/${zone_key}/wcselect?type=http://id.webbrick.co.uk/events/config/set"
                prefix="Weather Comp: " 
                format="#" 
                postfix="">
            &nbsp;
            </wb:numericEntryButton>
        </td>
        
        
    </tr>
    <tr>
        <th>&nbsp;</th>           
    </tr>
    <tr>
        <td><div style="margin-left:16px">Early Start Settings:</div></td>
    </tr>
    <tr>
        <td>
            <wb:enableEntryButton
                    baseClassName="entry"
                    stateVals="Blank,Tick"
                    wbTitle="Include in Early Start"
                    wbSource="/eventstate/${zone_key}/earlystart/enabled"
                    wbTarget="/sendevent/${zone_key}/earlystart/enabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Included"
                    >
            </wb:enableEntryButton>
        </td>
        <td>
            <wb:numericEntryButton
                    colspan='1'
                    wbSource="/eventstate/${zone_key}/earlystart/setpoint"
                    wbTarget="/sendevent/${zone_key}/earlystart/setpoint?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Target: " 
                    format="##.#" 
                    postfix="&ordm;C"
                    wbTitle="Set Point">
                    Set Point
            </wb:numericEntryButton>
        </td>
        <td >
            <wb:BackButton>
                Done
            </wb:BackButton>
        </td>
    </tr>
    </table>

</span>


</html>
