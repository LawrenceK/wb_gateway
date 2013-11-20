<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.widgets_round">
    
<table py:def="output_schedule( name )" id="scheduleboxtable">
    <?python 
        from WebBrickGateway.Schedule import getSchedule
        mysched = getSchedule(name)
        if not mysched:
            # create null schedule
            mysched = {"devicesOnOff":[], "devicesValue":[], "timepoints":0 }
    ?>
    
    <tr>
        <th>&nbsp;</th>
        <th>Time</th>
        <th>Days</th>
        <!-- display strings for device names -->
        <th py:for='dev in mysched["devicesOnOff"]'>${mysched[dev]}</th>
        <th py:for='dev in mysched["devicesValue"]'>${mysched[dev]}</th>
        <th>&nbsp;</th>
    </tr>

    <!--  Boost is not appropriate for most scheduled items, for example lights, curtains
          ===============================================================================
    <tr>
        <td>
            <wb:caption colspan='2'>Current</wb:caption>
        </td>
        <td>
            <wb:simpleButton py:for='dev in mysched["devicesOnOff"]' 
                    wbTarget="/sendevent/schedule/${name}/${dev}?type=http://id.webbrick.co.uk/events/schedule/boost"
                    wbSource="/eventstate/schedule/${name}/${dev}/current?attr=state">Boost</wb:simpleButton>
        </td>
        <td>
            <wb:simpleButton py:for='dev in mysched["devicesValue"]' 
                    wbTarget="/sendevent/schedule/${name}/${dev}?type=http://id.webbrick.co.uk/events/schedule/boost"
                    wbSource="/eventstate/schedule/${name}/${dev}/current?attr=val">Boost</wb:simpleButton>
        </td>
    </tr>
    -->
    
    <tr py:for='tp in range(mysched["timepoints"])'  >
    
        <td class="buttoncapleft"/>
            
        <td class="buttonbody">
            <wb:timeEntry
                    noPolling="yes"
                    wbTarget="/sendevent/schedule/${name}/${tp}?type=http://id.webbrick.co.uk/events/config/set"
                    wbSource="/eventstate/schedule/${name}/${tp}?attr=time"/>
        </td>
        <td class="buttonbody" >
            <wb:dayEntry 
                    noPolling="yes"
                    wbTarget="/sendevent/schedule/${name}/${tp}?type=http://id.webbrick.co.uk/events/config/set"
                    wbSource="/eventstate/schedule/${name}/${tp}?attr=day"/>
        </td>
        <td py:for='dev in mysched["devicesOnOff"]' class="buttonbody">
            <wb:onoffEntry 
                    noPolling="yes"
                    wbTarget="/sendevent/schedule/${name}/${tp}/${dev}?type=http://id.webbrick.co.uk/events/config/set"
                    wbSource="/eventstate/schedule/${name}/${tp}/${dev}?attr=onoff" />
        </td>
        <td py:for='dev in mysched["devicesValue"]' class="buttonbody">
            <wb:numericEntry 
                    prefix="" format="##.#" postfix="&ordm;C"
                    noPolling="yes"
                    wbTarget="/sendevent/schedule/${name}/${tp}/${dev}?type=http://id.webbrick.co.uk/events/config/set"
                    wbSource="/eventstate/schedule/${name}/${tp}/${dev}" />
        </td>
        <td class="buttoncapright"/>
        
    </tr>
</table>

</html>
