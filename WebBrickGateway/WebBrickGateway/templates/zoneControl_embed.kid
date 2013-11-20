<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.embedschedule
import WebBrickGateway.templates.widgets
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.embedschedule, WebBrickGateway.templates.widgets">

<!-- zoneNumber would in as ${zoneNr} -->

<span py:def="output_zone_name( zoneNr )">
    ${output_current_value( "/eventstate/zone%s/name?attr=name"%(zoneNr) )}
<!--
        <div wbSource="/eventstate/zone${zoneNr}/name?attr=name"
             wbLoad='loadTextDisplay("Zone: ","")'>
        Zone Name
        </div>
-->        
</span>

<span py:def="output_zone_control( zoneNr )">

    <table>
        <colgroup span="2" width="50%"/>
        <tr>
        <td>
            <div>
            ${output_schedule("zone%s" % (zoneNr) )}
            </div>
        </td>
        <td>
            <!-- the right hand side -->
            <table>
            <colgroup span="4" width="25%"/>
            <tr>
                <td colspan="4" class="NaN">Status</td>
            </tr>
            <tr>
                <!-- changed to zone state, in the case of a valve we can see what this is doing
                <wb:textDisplay colspan="2" wbSource="/eventstate/zone${zoneNr}/name?attr=name" prefix="" format="" postfix="">Zone Name
                </wb:textDisplay>
                -->
                <wb:simpleIndicator colspan="2"
                    wbSource="/eventstate/zone${zoneNr}/state?attr=state" 
                    stateVals="Locked,Idle,WillRun">
                    Zone
                </wb:simpleIndicator>

                <td colspan="2"
                    wbType="Indicator" 
                    wbLoad="loadButton()"
                    wbSource="/eventstate/zone${zoneNr}/source?attr=state" 
                    stateVals="Off,On"
                    baseClassName="indicator">
                        <div wbType="mediumText"
                             wbSource="/eventstate/zone${zoneNr}/heatsource?attr=name"
                             wbLoad='loadTextDisplay("","")'>
                        Source
                        </div>
                </td>
            </tr>
            <tr>
                <wb:textDisplay colspan="2" wbSource="/eventstate/zone${zoneNr}/sensor?attr=name" prefix="Current: " format="" postfix="">&nbsp;
                </wb:textDisplay>
                <wb:numericDisplay colspan="2" wbSource="/eventstate/zone${zoneNr}/sensor?attr=val" prefix="" format="##.#" postfix="&ordm;C">&nbsp;
                </wb:numericDisplay>
            </tr>
            <tr>
                <wb:numericEntry 
                        wbSource="/eventstate/zone${zoneNr}/state?attr=targetsetpoint"
                        wbTarget="/sendevent/zone${zoneNr}/manual/set?type=http://id.webbrick.co.uk/events/zones/manual"
                        prefix="Target: " 
                        format="##.#" 
                        postfix="&ordm;C">
                        wbTitle="Set Point"
                    Set Point
                </wb:numericEntry>
                
                <wb:textDisplay 
                        wbSource="/eventstate/zone${zoneNr}/state?attr=cmdsource"
                        prefix="[" 
                        postfix="]">
                    Source
                </wb:textDisplay>

                <wb:textDisplay colspan="2" wbSource="/eventstate/zone${zoneNr}/state?attr=status" prefix="Action: " format="" postfix="">&nbsp;
                </wb:textDisplay>
            </tr>
            <tr>
                <td colspan="2" class="NaN">Options</td>
                <td>&nbsp;</td>           
                <td>&nbsp;</td>           
            </tr>
            <tr>
                <wb:enableEntry
                    colspan="2"
                    baseClassName="entry"
                    stateVals="Locked,OK"
                    wbTitle="Enable Zone"
                    wbSource="/eventstate/zone${zoneNr}/enabled"
                    wbTarget="/sendevent/zone${zoneNr}/enabled?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Zone Enable"
                    />

                <wb:enableEntry
                    colspan="2"
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbTitle="Follow Occupancy"
                    wbSource="/eventstate/zone${zoneNr}/occupancy"
                    wbTarget="/sendevent/zone${zoneNr}/occupancy?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Follow Occupancy"
                    />
            </tr>
            <tr>
                <wb:numericEntry colspan="4"
                        wbSource="/eventstate/zone${zoneNr}/matStat"
                        wbTarget="/sendevent/zone${zoneNr}/matStat?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Lowest Temperature: " 
                        format="#" 
                        postfix="&ordm;C">
                        wbTitle="Minimum Zone Temperature"
                    &nbsp;
                </wb:numericEntry>
            </tr>
            <tr>
                <wb:numericEntry colspan="2"
                        wbSource="/eventstate/zone${zoneNr}/wcselect" 
                        wbTarget="/sendevent/zone${zoneNr}/wcselect?type=http://id.webbrick.co.uk/events/config/set"
                        prefix="Weather Compensation: " 
                        format="#" 
                        postfix="">
                        wbTitle="Weather Compensation"
                    &nbsp;
                </wb:numericEntry>
                
                
                
                
                <wb:simpleIndicator colspan="2" 
                        wbLoad="loadButton()"
                        wbSource='/eventstate/weather/${output_current_value( "/eventstate/zone%s/wcselect?attr=val"%zoneNr ) }/?attr=istate' 
                        stateVals="Suppress,WillRun"
                        baseClassName="status">
                    ${output_current_value( "/eventstate/zone%s/wcselect?attr=val"%zoneNr ) }
                    </wb:simpleIndicator>
                
                
                
               
            </tr>

            </table>
        </td>
        </tr>
    </table>
</span>

</html>
