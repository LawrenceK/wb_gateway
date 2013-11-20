<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
zoneNr = 1
zoneNrBottom = 17
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master, 'zoneControl_embed.kid'">
    
<!-- zoneNumber would in as ${zoneNumber} -->

${output_head("Zone Control")}

<body>

    <?python 
        automatic = int(WebBrickGateway.templates.widgets.getCurrentValue( "/eventstate/solar/automatic" ))
        if automatic == '':
            automatic = 1
    ?>

${output_nav(output_zone_name(zoneNr))}

<div id="left" style="
    width: 49%;
    top: 70px;
    z-index: 0;
    float: left;">
    
    ${output_schedule("zone%s" % (zoneNr) )}
    <table>
        <colgroup span="4" width="25%"/>
        <tr>
            <th style="text-align: left;">&nbsp;</th>
        </tr>
        <tr>
            <th style="text-align: left;">Options</th>
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
                    postfix="&ordm;C"
                    wbTitle="Minimum Zone Temperature">
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
</div>
<div id="right" style="
    width: 49%;
    top: 70px;
    z-index: 0;
    margin-right: 5px;
    float: right;">
    
    <div id="right-left" style="
        width: 10%;
        top: 70px;
        z-index: 2;
        float: left;">
        <table>
            <colgroup span="2" width="50%"/>
            
            <tr>
                <td>&nbsp;</td>
            </tr>
            <tr>
                <td>&nbsp;</td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <th style="text-align: left;">Status</th>
            </tr>
            
            <tr>
                <wb:simpleIndicator colspan="2"
                    wbSource="/eventstate/zone${zoneNr}/state?attr=state" 
                    stateVals="Locked,Idle,WillRun">
                    Zone
                </wb:simpleIndicator>
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
            </tr>
        </table>
    </div>
    <div id="right-right" style="
        width: 90%;
        top: 70px;
        z-index: 0;
        float: right;
        index: 0;
        text-align: right;">
        
        <img src="/static/images/Plant/Tank2.png" />
        
        <div id="foreground" style="
            position: absolute;
            width: 44%;
            top: 60px;
            z-index: 1;
            text-align: right;
            font-size:medium;
            font-weight: bolder;">  
            <div id="box" style="
                margin-top:60px;">
                <span wbType="mediumText"
                    wbSource="/eventstate/zone${zoneNr}/heatsource?attr=name"
                    wbLoad='loadTextDisplay("","")'
                    style="
                    margin-right:120px;">
                    Source
                </span>
                <span id="heatextop" style="
                    margin-right:70px;">
                    <wb:numericDisplay 
                        wbSource="/eventstate/heatsource/3/heatextop?attr=val" 
                        prefix="" 
                        format="##.#" 
                        postfix="&ordm;C">&nbsp;
                    </wb:numericDisplay>
                </span>  
            </div>
            <div id="box" style="
                margin-top:180px;">
                <span wbType="mediumText"
                    wbSource="/eventstate/zone${zoneNrBottom}/heatsource?attr=name"
                    wbLoad='loadTextDisplay("","")'
                    style="
                    margin-right:120px;">
                    Source
                </span>
                <span id="heatexbot" style="
                    margin-right:70px;">
                    <wb:numericDisplay 
                        wbSource="/eventstate/heatsource/3/heatexbot?attr=val" 
                        prefix="" 
                        format="##.#" 
                        postfix="&ordm;C">&nbsp;
                    </wb:numericDisplay>
                </span>  
            </div>   
        </div>   
    </div>
</div>
<div id="right-bottom" style="
        width: 49%;
        z-index: 0;
        float: right;">
        <table>
            <colgroup span="3" width="33%"/>
            <tr>
                <th style="text-align: left;">Solar</th>
            </tr>
            <tr py:if='automatic == 1'>
                <wb:textDisplay colspan="1" wbSource="/eventstate/heatsource/3/availability?attr=availability" prefix="Availability: " format="" postfix="">&nbsp;
                </wb:textDisplay>
                <td wbType="Indicator" 
                    wbLoad="loadIndicator()"
                    wbSource="/wbsts/9/DO/4"
                    stateVals="Off,On"
                    baseClassName="indicator">
                    Pump Status
                </td>
                <wb:enableEntry
                    colspan="2"
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbTitle="Automatic"
                    wbSource="/eventstate/solar/automatic"
                    wbTarget="/sendevent/solar/automatic?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Automatic"
                    />
            </tr>
            <tr py:if='automatic == 0'>
                <wb:textDisplay colspan="1" wbSource="/eventstate/heatsource/3/availability?attr=availability" prefix="Availability: " format="" postfix="">&nbsp;
                </wb:textDisplay>
                <wb:simpleButton  
                    wbSource="/wbsts/9/DO/4" 
                    wbTarget="/wbcmd/loft2/DI/4">
                    Pump
                </wb:simpleButton>
                <wb:enableEntry
                    colspan="2"
                    baseClassName="entry"
                    stateVals="Blank,OK"
                    wbTitle="Automatic"
                    wbSource="/eventstate/solar/automatic"
                    wbTarget="/sendevent/solar/automatic?type=http://id.webbrick.co.uk/events/config/set"
                    prefix="Automatic"
                    />
            </tr>
        </table>
</div>
    


${output_site_info_bar()}

</body>

</html>
