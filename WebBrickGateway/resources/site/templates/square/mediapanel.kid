<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head( mediatitle )}

<body>

    ${output_nav(mediatitle)}
    <table>
<!--        
        <tr>
            <td colspan="2" wbType="Caption" wbLoad="loadCaption()">${mediatitle}</td>
        </tr>
-->
        <tr>	
            <td wbType="PushButton" wbLoad="loadButton()"
                baseClassName="stopButton"
                wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=stop">
                Stop
            </td>
            <td wbType="PushButton" wbLoad="loadButton()" 
                baseClassName="pauseButton"
                wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=pause">
                Pause
            </td>
            <td wbType="PushButton" wbLoad="loadButton()" 
                baseClassName="playButton"
                wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=play">
                Play
            </td>
<!--
            <td wbType="PushButton" wbLoad="loadButton()" 
                baseClassName="nextTrackButton"
                wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=next">
                Next Track
            </td>
            <td wbType="PushButton" wbLoad="loadButton()" 
                baseClassName="prevTrackButton"
                wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=prev">
                Previous Track
            </td>
-->
        </tr>
        <tr>	
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setVolume?medianame=${medianame}&amp;newVolume=0">
                vol 0
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setVolume?medianame=${medianame}&amp;newVolume=25">
                vol 25
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setVolume?medianame=${medianame}&amp;newVolume=50">
                vol 50
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setVolume?medianame=${medianame}&amp;newVolume=75">
                vol 75
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setVolume?medianame=${medianame}&amp;newVolume=100">
                vol 100
            </td>
        </tr>
        <tr>	
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setPosition?medianame=${medianame}&amp;newPosition=0">
                Start
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setPosition?medianame=${medianame}&amp;newPosition=25%25">
                25%
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setPosition?medianame=${medianame}&amp;newPosition=50%25">
                50%
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setPosition?medianame=${medianame}&amp;newPosition=75%25">
                75%
            </td>
            <td wbType="PushButton" wbLoad="loadButton()"
                wbTarget="/mediaaccess/setPosition?medianame=${medianame}&amp;newPosition=100%25">
                100%
            </td>
        </tr>
    </table>
    <table>
        <tr>
	    <td colspan='2' wbType="Text" wbLoad='loadTextDisplay("","")'
                    wbSource="/mediaaccess/status?medianame=${medianame}&amp;status=track">
                (track text here)
            </td>
        </tr>
        <tr>
<!--
            <td colspan='2'>
                <div class='uislider' id='trackPosition' 
                    wbType="NumericSlider" 
                    wbLoad='loadNumericSlider()'
                    wbSource="/mediaaccess/status?medianame=${medianame}&amp;status=position"
                    style="width: 150px;" 
                    ui:minvalue="0" 
                    ui:maxvalue="500">&nbsp;Position</div> 
                <position colspan='2' wbType="Text" wbLoad='loadTextDisplay("Elapsed: "," seconds")'
                    wbSource="/mediaaccess/status?medianame=${medianame}&amp;status=position">
                    (time text here)
                </position>
            </td>
-->
            <td width='48%'>
                <table class='compositeWidget'>
                    <tr>
                        <td width='50%'>
                            Position:
                        </td>
                        <td wbType="Numeric" wbLoad='loadTimeDisplay("","")'
                                wbSource="/mediaaccess/status?medianame=${medianame}&amp;status=position">
                            (Time text here)
                        </td>
                    </tr>
                    <tr>
                        <td class='NumericBar' id='positionControl' colspan='2'
                                wbType="NumericBar" 
                                wbSource="/mediaaccess/status?medianame=${medianame}&amp;status=position"
                                minvalue="0" 
                                maxvalue="300"
                                curvalue="0"
                                height="20px" >
                        </td> 
                    </tr>
                    <tr>
                        <td wbType="PushButton" wbLoad="loadButton()" 
	                    baseClassName="prevTrackButton"
                            wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=prev">
                            Previous Track
                        </td>
                        <td wbType="PushButton" wbLoad="loadButton()" 
                            baseClassName="nextTrackButton"
                            wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=next">
                            Next Track
                        </td>
                    </tr>
                </table>
            </td>

            <td width='48%'>
                <table class='compositeWidget'>
                    <tr>
                        <td width='50%'>
                            Volume:
                        </td>
                        <td wbType="Numeric" wbLoad='loadNumericDisplay("","","")'
                                wbSource="/mediaaccess/status?medianame=${medianame}&amp;status=vol">
                            (Volume text here)
                        </td>
                    </tr>
                    <tr>
                        <td class='NumericBar' id='volControl' colspan='2'
                                wbType="NumericBar" 
                                wbSource="/mediaaccess/status?medianame=${medianame}&amp;status=vol"
                                minvalue="0" 
                                maxvalue="100"
                                curvalue="45"
                                height="20px" >
                        </td> 
                    </tr>
                    <tr>
                        <td wbType="PushButton" wbLoad="loadButton()" 
                            baseClassName="volDown"
                            wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=voldown">
                            Volume Down
                        </td>
                        <td wbType="PushButton" wbLoad="loadButton()" 
                            baseClassName="volUp"
                            wbTarget="/mediaaccess/command?medianame=${medianame}&amp;mediacmd=volup">
                            Volume Up
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td colspan="2">&nbsp;</td>
        </tr>
        <tr>
            <td colspan="1">&nbsp;</td>
            <td class="NaN"><img width="20%" src="/static/images/Decorations/notes.png"/></td>
        </tr>
    </table>
<!--
The passed data is an Xml dom with lots of elements in it.
    <table class="playlist">
        <tr>
	    <td wbType="Text" wbLoad='loadTextDisplay("","")'
                medianame="${medianame}" status="playlist">(playlist here)</td>
        </tr>
    </table>
-->

    ${output_site_info_bar()}

</body>

</html>
