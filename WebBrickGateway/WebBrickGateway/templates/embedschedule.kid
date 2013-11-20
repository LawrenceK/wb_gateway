<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/">

<table py:def="output_schedule( name )">
    <?python 
        from WebBrickGateway.Schedule import getSchedule
        mysched = getSchedule(name)
        if not mysched:
            # create null schedule
            mysched = {"devicesOnOff":[], "devicesValue":[], "timepoints":0 }
    ?>

    <tr>
        <th>Time</th>
        <th>Days</th>
        <!-- display strings for device names -->
    <th py:for='dev in mysched["devicesOnOff"]'>${mysched[dev]}</th>
    <th py:for='dev in mysched["devicesValue"]'>${mysched[dev]}</th>
    </tr>

    <!--  Boost is not appropriate for most scheduled items, for example lights, curtains
          ===============================================================================
    <tr>
        <wb:caption colspan='2'>Current</wb:caption>
    <wb:simpleButton py:for='dev in mysched["devicesOnOff"]' 
            wbTarget="/sendevent/schedule/${name}/${dev}?type=http://id.webbrick.co.uk/events/schedule/boost"
            wbSource="/eventstate/schedule/${name}/${dev}/current?attr=state">Boost</wb:simpleButton>
    <wb:simpleButton py:for='dev in mysched["devicesValue"]' 
            wbTarget="/sendevent/schedule/${name}/${dev}?type=http://id.webbrick.co.uk/events/schedule/boost"
            wbSource="/eventstate/schedule/${name}/${dev}/current?attr=val">Boost</wb:simpleButton>
    </tr>
    -->
    
    <tr py:for='tp in range(mysched["timepoints"])'>
    <wb:timeEntry
            noPolling="yes"
            wbTarget="/sendevent/schedule/${name}/${tp}?type=http://id.webbrick.co.uk/events/config/set"
            wbSource="/eventstate/schedule/${name}/${tp}?attr=time"/>
    <wb:dayEntry wbType="WbDayEntry"
            noPolling="yes"
            wbTarget="/sendevent/schedule/${name}/${tp}?type=http://id.webbrick.co.uk/events/config/set"
            wbSource="/eventstate/schedule/${name}/${tp}?attr=day"/>
    <wb:onoffEntry py:for='dev in mysched["devicesOnOff"]'
            noPolling="yes"
            wbTarget="/sendevent/schedule/${name}/${tp}/${dev}?type=http://id.webbrick.co.uk/events/config/set"
            wbSource="/eventstate/schedule/${name}/${tp}/${dev}?attr=onoff" />
    <wb:numericEntry py:for='dev in mysched["devicesValue"]' 
            prefix="" format="##.#" postfix="&ordm;C"
            noPolling="yes"
            wbTarget="/sendevent/schedule/${name}/${tp}/${dev}?type=http://id.webbrick.co.uk/events/config/set"
            wbSource="/eventstate/schedule/${name}/${tp}/${dev}" />
    </tr>

</table>

</html>
