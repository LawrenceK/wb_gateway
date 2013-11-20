<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">
${output_head("Weather Compensation")}

<body>

<link href="/static/css/weather.css" rel="stylesheet" type="text/css" />

${output_nav("Weather Compensation")}

<table>
    <colgroup span="3" width="33%" />
    <tr>
        <td>
        <!-- first set -->
            <table>
                <tr>
                    <td 
                        wbType="Indicator" 
                        wbLoad="loadButton()"
                        wbSource="/eventstate/weather/1/?attr=istate" 
                        stateVals="Suppress,WillRun"
                        baseClassName="status">
                    1
                    </td>
                </tr>
                <tr>
                    <td><hr/></td>
                </tr>
                <tr>
                    <td>Outside temperature thresholds</td>
                </tr>
                <tr>
                    <td 
                        type="numericEntry" 
                        wbSource="/eventstate/weather/1/rising/outsideThreshold" 
                        wbTarget="/sendevent/weather/1/rising/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        wbLoad="loadWbNumericEntry('Rising: ','##.#','&ordm;C')"/>
                </tr>
                <tr>
                    <td 
                        type="numericEntry" 
                        wbSource="/eventstate/weather/1/falling/outsideThreshold" 
                        wbTarget="/sendevent/weather/1/falling/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        wbLoad="loadWbNumericEntry('Falling: ','##.#','&ordm;C')"/>
                </tr>
            </table>
        </td>
        <td>
        <!-- second set -->
            <table>
                <tr>
                    <td 
                        wbType="Indicator" 
                        wbLoad="loadButton()"
                        wbSource="/eventstate/weather/2/?attr=istate" 
                        stateVals="Suppress,WillRun"
                        baseClassName="status">
                    2
                    </td>
                </tr>
                <tr>
                    <td><hr/></td>
                </tr>
                <tr>
                    <td>Outside temperature thresholds</td>
                </tr>
                <tr>
                    <td 
                        type="numericEntry" 
                        wbSource="/eventstate/weather/2/rising/outsideThreshold" 
                        wbTarget="/sendevent/weather/2/rising/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        wbLoad="loadWbNumericEntry('Rising: ','##.#','&ordm;C')"/>
                </tr>
                <tr>
                    <td 
                        type="numericEntry" 
                        wbSource="/eventstate/weather/2/falling/outsideThreshold" 
                        wbTarget="/sendevent/weather/2/falling/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        wbLoad="loadWbNumericEntry('Falling: ','##.#','&ordm;C')"/>
                </tr>
            </table>
        </td>
        <td>
        <!-- third set -->
            <table>
                <tr>         
                    <td 
                        wbType="Indicator" 
                        wbLoad="loadButton()"
                        wbSource="/eventstate/weather/3/?attr=istate" 
                        stateVals="Suppress,WillRun"
                        baseClassName="status">
                    3
                    </td>
                </tr>
                <tr>
                    <td><hr/></td>
                </tr>
                <tr>
                    <td>Outside temperature thresholds</td>
                </tr>
                <tr>
                    <td 
                        type="numericEntry" 
                        wbSource="/eventstate/weather/3/rising/outsideThreshold" 
                        wbTarget="/sendevent/weather/3/rising/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        wbLoad="loadWbNumericEntry('Rising: ','##.#','&ordm;C')"/>
                </tr>
                <tr>
                    <td 
                        type="numericEntry" 
                        wbSource="/eventstate/weather/3/falling/outsideThreshold" 
                        wbTarget="/sendevent/weather/3/falling/outsideThreshold?type=http://id.webbrick.co.uk/events/config/set"
                        wbLoad="loadWbNumericEntry('Falling: ','##.#','&ordm;C')"/>
                </tr>
            </table>
        </td>
    </tr>
    <!-- Debug UI to see which way the temperature is going -->
    <tr>
        <td colspan="3">&nbsp;</td>
    </tr>
    <tr>
        <td colspan="3">&nbsp;</td>
    </tr>
    <tr>
        <td colspan="3">Current weather situation, this can take some time to build</td>
    </tr>
    <tr>
        <wb:numericDisplay wbSource="/eventstate/weather/previous?attr=previousTemp" prefix="Previous:" format="##.#" postfix="&ordm;C">&nbsp;
        </wb:numericDisplay>
        <wb:numericDisplay wbSource="/eventstate/weather/outsideTemp" prefix="Current:" format="##.#" postfix="&ordm;C">&nbsp;
        </wb:numericDisplay>
        <td wbType="Indicator" 
            wbLoad="loadButton()"
            wbSource="/eventstate/weather/global?attr=tstate" 
            stateVals="Falling,Static,Rising"
            baseClassName="indicator">
        Trend
        </td>
    </tr>
</table>





${output_site_info_bar()}

</body>
</html>
