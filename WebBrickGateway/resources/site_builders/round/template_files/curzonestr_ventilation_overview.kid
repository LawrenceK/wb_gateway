<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round

layout_params['left_title'] = "Zones"
?>

<!-- ! curzonestr ventialtion template -->
<!--    This is a tempalte file for ventilation, and has the following placeholder strings that need 
        to be replaced by sensible strings: 
        
            curzonestr      -> this should be the same as the first part of the filename
            curzonetitle    -> this is the title displayed on the page
            
        Related files: 
            curzonestr_ventilation_gateway.xml
                Sensors (PIR/Hum) and acctuators (fans) split over multiple webbricks
                
                    --- OR ---
                
            curzonestr_ventilation_webbrick.xml
                All  Sensors (PIR/Hum) and acctuators (fans) on one webbrick

-->

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:layout="'sitelayout3.kid'" 
        py:extends="WebBrickGateway.templates.widgets_round, 'zone_lists' ">

        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        ${output_zone_links("curzonestr", "general")}
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <h1>curzonetitle Ventilation</h1>
            
        <table style="width:100%;">
            <colgroup span="3" width="33%"/>
            <tr>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
                            width="100px"
                            height="100px"
            				wbSource="/eventstate/curzonestr/ventilation/temp" 
                            minvalue="5"
                            maxvalue="45"
                            curvalue="0"
                            setlow="15"
                            sethigh="35"
                            labels="5,15,25,35,45"
            				prefix="" 
            				format="##.#" 
                            postfix="&ordm;C"
                            flashMovie='MeterRadial270.swf'
                            >
            			Temp
            		</wb:flashMeter>
                </td>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
                            width="100px"
                            height="100px"
            				wbSource='/eventstate/curzonestr/ventilation/hum/level'
                            minvalue="20"
                            maxvalue="60"
                            curvalue="0"
                            setlow="30"
                            sethigh="50"
                            labels="20,30,40,50,60"
                            prefix="" 
            				format="##.#" 
            				postfix="%"
                            metertitle="Humidity"
                            flashMovie='MeterRadial270.swf'
                            >
            			Humidity
            		</wb:flashMeter>
                </td>
                <td rowspan="2" style="text-align:center">
                    <wb:flashMeter
                            width="100px"
                            height="100px"
            				wbSource='/eventstate/curzonestr/ventilation/fan/speed'
                            minvalue="0"
                            maxvalue="100"
                            curvalue="0"
                            setlow="65"
                            sethigh="85"
                            labels="0,25,50,75,100"
                            prefix="" 
            				format="##.#" 
            				postfix="%"
                            metertitle="Fan Speed"
                            flashMovie='MeterRadial270.swf'
                            >
            			Fan Speed
            		</wb:flashMeter>
                </td>
            </tr>
            <tr>
                &nbsp;
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td colspan="1"><div style="margin-left:16px">Ventilation Settings: </div></td>
            </tr>
            <tr>
                <td>
                    <wb:enableEntryButton
                            baseClassName="entry"
                            stateVals="Blank,Tick"
                            wbTitle="Enable Fan"
                            wbSource='/eventstate/curzonestr/ventilation/fan/enabled'
                            wbTarget='/sendevent/curzonestr/ventilation/fan/enabled?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="Fan Enabled"
                            >
                        &nbsp;
                    </wb:enableEntryButton>
                </td>
                <td>
                    <wb:numericEntryButton 
                            wbSource='/eventstate/curzonestr/ventilation/hum/threshold'
                            wbTarget='/sendevent/curzonestr/ventilation/hum/threshold?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="Threshold: " 
                            format="#" 
                            postfix="%"
                            >
                        &nbsp;
                    </wb:numericEntryButton>
                </td>
                <td>
                    <wb:numericEntryButton 
                            wbSource='/eventstate/curzonestr/ventilation/fan/runtime'
                            wbTarget='/sendevent/curzonestr/ventilation/fan/runtime?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="Run Time: " 
                            format="#" 
                            postfix=" sec"
                            >
                        &nbsp;
                    </wb:numericEntryButton>
                </td>
            </tr>
            <tr>
                 <td>
                    <wb:enableEntryButton
                            baseClassName="entry"
                            stateVals="Blank,Tick"
                            wbTitle="Enable PIR"
                            wbSource='/eventstate/curzonestr/ventilation/pir/enabled'
                            wbTarget='/sendevent/curzonestr/ventilation/pir/enabled?type=http://id.webbrick.co.uk/events/config/set'
                            prefix="PIR Enabled"
                            >
                        &nbsp;
                    </wb:enableEntryButton>
                </td>
             </tr>
        </table>
                       
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        ${output_functional_links( "curzonestr", "general", [True,True,True,True,True] )}
    </div>

</html>
