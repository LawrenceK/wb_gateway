<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed


from WebBrickGateway.templates.widgets_tabbed import getCurrentValue
from WebBrickGateway.Schedule import getSchedule

def returnDay(s):
    #
    #  find the first non '-' in the string
    #
    for i in range(len(s)):
        if s[i] != '-' :
            return (i+6)%7
    return None

def timeToMinutes (s) :
    #
    #  return time in minutes
    #
    try:
        parts = s.split(':')
        return (int(parts[0])*60)+int(parts[1])
    except:
        return None


def jsSchedule(sname):
    schedule={}
    newSched = {'index': 0, 't': 10.0, 'day': 0, 'smod': 0}
    outstr = ""
    schedSize = str(getSchedule(sname)["timepoints"])
    valid = True
    tp =0
    while(valid):
        smod = timeToMinutes(getCurrentValue("/eventstate/schedule/%s/%s?attr=time" % (sname,tp)))
        day = returnDay(getCurrentValue("/eventstate/schedule/%s/%s?attr=day" % (sname,tp)))
        t = getCurrentValue("/eventstate/schedule/%s/%s/%s" % (sname,tp,sname))

        if (smod!=None) and (day!=None) and (t!='') :
            schedule[tp] = {}
            schedule[tp]["index"] = tp
            schedule[tp]["smod"] = smod
            schedule[tp]["day"] = day
            schedule[tp]["t"] = float(t)
            outstr += str(schedule[tp]) + ","
        else:
            valid = False

        tp = tp +1
        if tp > int(schedSize):
            valid = False

    if (outstr==""):
        st = getCurrentValue("/sendevent/schedule/%s/0?type=http://id.webbrick.co.uk/events/config/set&time=00:00:00&day=-M-----" % sname)
        sp = getCurrentValue("/sendevent/schedule/%s/0/%s?type=http://id.webbrick.co.uk/events/config/set&val=11"  % (sname,sname) ) 
        print "New Schedule Created"
        return str(newSched)
    else:
        return outstr[0:len(outstr)-1]

?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:extends="WebBrickGateway.templates.widgets_tabbed">


    <div py:def="output_zone_button(zone_key, zone_string, zone_name )" class="button">
        <a href="/template/tabbed/zone_overview?zone_key=${zone_key}">
            <div class="left"/>
            <div class="center">
                <div class="text">
                    ${zone_name}
                </div>
            </div>
            <div class="right_box">
                <div class="temp">
                    <wb:numericDisplay
                            wbSource="/eventstate/${zone_key}/state?attr=targetsetpoint"
                            prefix=""
                            format="##.#"
                            postfix=""
                            baseClassName="actual_value">
                    </wb:numericDisplay>
                </div>
                <div class="temp">
                    <wb:numericDisplay
                            wbSource="/eventstate/${zone_key}/sensor?attr=val"
                            prefix=""
                            format="##.#"
                            postfix=""
                            baseClassName="actual_value">
                    </wb:numericDisplay>
                </div>
            </div>
        </a>
    </div>

    <div py:def="output_zone_spinner(zone_key, zone_string, zone_name, min_temp, max_temp )">

        <div id="waitingBox">
            <div id="loading">Loading Schedule</div>
        </div>


        <!-- BEGIN: Temporary spinner Control-->
        <div id="${zone_key}" class="spinner_control">
            <img src='/static/tabbedskin/images/heatingcontrolbg.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
            <div class="title">${zone_name}</div>
            <div class="minvalue">${min_temp}&deg;C</div>
            <div class="maxvalue">${max_temp}&deg;C</div>
            <div class="controlvalue spinner_value">
            </div>
            <div class="actual_value">
                    <wb:numericDisplay
                            wbSource="/eventstate/${zone_key}/sensor?attr=val"
                            prefix=""
                            format="##.#"
                            postfix=""
                            baseClassName="actual_value">
                    </wb:numericDisplay>
            </div>
            <div class='spinner_controls'>
                <a href="#" class='spinner_up'>
                    <img src='/static/tabbedskin/images/spinnerupicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
                <a href="#" class='spinner_down'>
                    <img src='/static/tabbedskin/images/spinnerdownicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
            </div>
            <div class="schedulelink">
                <a href="/template/show_schedule?zone_key=${zone_key}">
                    <img src='/static/tabbedskin/images/calendaricon.png' onmousedown="curs_wait(this,event);" onclick="curs_clicked();"/>
                </a>
            </div>
        </div>
        <!-- END: Temporary  -->

        <script language="JavaScript" defer="defer">

            var heatingSpinner = new Proto.Spinner({
                spinner_container_id: '${zone_key}',
                live: true,
                initial_value: 20,
                min_value: ${min_temp},
                max_value: ${max_temp},
                small_increment: 0.5,
                onChange: function(new_value) {
                    return new_value;
                },
                format_value: function(val) {
                    return parseInt(val) + '.' + Math.round(val % 1 * 10)
                }
            });

        </script>



    </div>
    <div py:def="output_zone_schedule(zone_key, zone_string, zone_name, min_temp, max_temp, cool_point, hot_point )">
        <?python
        listBlob = jsSchedule(zone_key)
        ?>



        <h1>${zone_name} Schedule</h1>

        <script language="JavaScript">
        <![CDATA[
            var tryBack = function() {
                if (timeWinEditor.unsavedChanges()) {
                    if (confirm("You have unsaved changes.  Are you sure you want to navigate away?")) {
                        history.back();
                    }
                } else {
                    history.back();
                }
            }
        ]]>
        </script>

        <div class="backbutton" id="backbutton" onclick="tryBack()">back</div>

        <div id="scheduler">
        </div>

        <div id="tempslider">
            <div class="temp_bar"></div>
        </div>

        <div id='leftroundbuttons'>
            <div class="roundbutton"><a href="#" onclick='timeWinEditor.newSlot();return false;' onmousedown="if (event.preventDefault) event.preventDefault()">new</a></div>
        </div>

        <div id='dow_spinner' class='timespinner'>
            <div class='spinner_label'>Day</div>
            <div class='spinner_value whitevaluebox'></div>
            <div class='spinner_controls'>
                <a href="#" class='spinner_down'>
                    <img src='/static/tabbedskin/images/spinnerupicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
                <a href="#" class='spinner_up'>
                    <img src='/static/tabbedskin/images/spinnerdownicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
            </div>
        </div>

        <div id='starttime_spinner' class='timespinner'>
            <div class='spinner_label'>Start</div>
            <div class='spinner_value whitevaluebox'></div>
            <div class='spinner_controls'>
                <a href="#" class='spinner_up'>
                    <img src='/static/tabbedskin/images/spinnerupicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
                <a href="#" class='spinner_down'>
                    <img src='/static/tabbedskin/images/spinnerdownicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
            </div>
        </div>

        <div id='setpoint_spinner'>
            <div class='spinner_label'>Set point</div>
            <div class='spinner_value' id='setpointbox'></div>
            <div class='spinner_controls'>
                <a href="#" class='spinner_up'>
                    <img src='/static/tabbedskin/images/spinnerupicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
                <a href="#" class='spinner_down'>
                    <img src='/static/tabbedskin/images/spinnerdownicon.png' onmousedown="if (event.preventDefault) event.preventDefault()"/>
                </a>
            </div>
        </div>

        <div id='rightroundbuttons'>
            <div class="roundbutton"><a href="#" onclick='timeWinEditor.delSlot();return false;'>delete</a></div>
            <div class="roundbutton"><a href="#" onclick='timeWinEditor.commitChanges();return false;'>done</a></div>
            <div class="roundbutton"><a href="#" onclick='timeWinEditor.undoChanges();return false;'>cancel</a></div>
        </div>
        <script language="JavaScript" defer="defer">
        <![CDATA[



        schedule = [${listBlob}] ;

        sname='${zone_key}';

        var timeWinEditor = new Proto.Scheduler({
            editor_id: 'scheduler',
            gradient: {coolpoint:${cool_point},hotpoint:${hot_point}},
            window_data: [${listBlob}]}) ;

        timeWinEditor.drawControl();
        var updateUserControlData = function() {
            // called when data changes
            dowSpinner.setValue_orig(timeWinEditor.cur_slot.day);
            smodSpinner.setValue_orig(timeWinEditor.cur_slot.smod);
            spointSpinner.setValue_orig(timeWinEditor.cur_slot.t);
            spointSlider.setValue(timeWinEditor.cur_slot.t);
        }

        document.observe('scheduler:timeslot_selected', updateUserControlData);
        document.observe('scheduler:timeslot_updated', updateUserControlData);

        var dowSpinner = new Proto.Spinner({
            spinner_container_id: 'dow_spinner',
            initial_value: timeWinEditor.cur_slot.day,
            min_value: 0,
            max_value: 6,
            small_increment: 1,
            onChange: function(new_value) {
                return timeWinEditor.setDOW(new_value);
            },
            format_value: function(val) {
                var dows = ['mon','tue','wed','thu','fri','sat','sun'];
                return dows[val];
            }
        });

        var smodSpinner = new Proto.Spinner({
            spinner_container_id: 'starttime_spinner',
            initial_value: timeWinEditor.cur_slot.smod,
            min_value: 0,
            max_value: 1425,
            small_increment: 15,
            onChange: function(new_value) {
                return timeWinEditor.setSMod(new_value);
            },
            format_value: formatTime
        });

        var spointSpinner = new Proto.Spinner({
            spinner_container_id: 'setpoint_spinner',
            initial_value: timeWinEditor.cur_slot.t,
            min_value: ${min_temp},
            max_value: ${max_temp},
            small_increment: 0.5,
            onChange: function(new_value) {
                timeWinEditor.setT(new_value);
                return new_value;
            },
            format_value: function(val) {
                return parseInt(val) + '.' + Math.round(val % 1 * 10)
            }
        });

        var spointSlider = new Proto.Tempslider({
            container_id: 'tempslider',
            initial_value: timeWinEditor.cur_slot.t,
            min_value: ${min_temp},
            max_value: ${max_temp},
            onChange: function(new_value) {
                timeWinEditor.setT(new_value);
                return new_value;
            }
        });

        ]]>
        </script>


    </div>

    <div py:def="output_zone_status(zone_key, zone_string, zone_name)" class="zonestatus">
        <div class="statusbox">
            <table class='bluebox'>
                <tr>
                    <td class='tl'></td>
                    <td class='t'></td>
                    <td class='tr'></td>
                </tr>
                <tr>
                    <td class='l'></td>
                    <td class='m'>
                        <div class='statusboxcontent'>
                            <div class="label1">Enabled</div>
                            <div class="label2">Status</div>
                            <div class="label3">Set By:</div>
                            <div class="value1">
                                <wb:textDisplay
                                        wbSource="/eventstate/${zone_key}/enabled/state?attr=val"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                            <div class="value2">
                                <wb:textDisplay
                                        wbSource="/eventstate/${zone_key}/state?attr=status"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                            <div class="value3">
                                <wb:textDisplay
                                        wbSource="/eventstate/${zone_key}/set/by?attr=val"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                        </div>
                    </td>
                    <td class='r'></td>
                </tr>
                <tr>
                    <td class='bl'></td>
                    <td class='b'></td>
                    <td class='br'></td>
                </tr>
            </table>
        </div>
    </div>

    <div py:def="output_system_status()" class="systemstatus">
        <div class="statusbox">
            <table class='bluebox'>
                <tr>
                    <td class='tl'></td>
                    <td class='t'></td>
                    <td class='tr'></td>
                </tr>
                <tr>
                    <td class='l'></td>
                    <td class='m'>
                        <div class='statusboxcontent'>
                            <div class="label1">Occupancy</div>
                            <div class="label2">Boiler</div>
                            <div class="label3">ASHP</div>
                            <div class="value1">
                                <wb:textDisplay
                                        wbSource="/eventstate/occupants/state?attr=val"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                            <div class="value2" baseclassname="status">
                                <wb:textDisplay
                                        wbSource="/eventstate/hvac/boiler/alarm?attr=text"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                            <div class="value3" baseclassname="status">
                                <wb:textDisplay
                                        wbSource="/eventstate/hvac/ashp/alarm?attr=text"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                        </div>
                    </td>
                    <td class='r'></td>
                </tr>
                <tr>
                    <td class='bl'></td>
                    <td class='b'></td>
                    <td class='br'></td>
                </tr>
            </table>
        </div>
    </div>


    <div py:def="output_alarm_status()" class="systemstatus">
        <div class="statusbox">
            <table class='bluebox'>
                <tr>
                    <td class='tl'></td>
                    <td class='t'></td>
                    <td class='tr'></td>
                </tr>
                <tr>
                    <td class='l'></td>
                    <td class='m'>
                        <div class='statusboxcontent'>
                            <div class="label1">Pressure</div>
                            <div class="label2">Boiler</div>
                            <div class="label3">ASHP</div>
                            <div class="value1">
                                <wb:textDisplay
                                        wbSource="/eventstate/hvac/pressure/alarm?attr=text"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                            <div class="value2" baseclassname="status">
                                <wb:textDisplay
                                        wbSource="/eventstate/hvac/boiler/alarm?attr=text"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                            <div class="value3" baseclassname="status">
                                <wb:textDisplay
                                        wbSource="/eventstate/hvac/ashp/alarm?attr=text"
                                        prefix=""
                                        postfix=""
                                        baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
                            </div>
                        </div>
                    </td>
                    <td class='r'></td>
                </tr>
                <tr>
                    <td class='bl'></td>
                    <td class='b'></td>
                    <td class='br'></td>
                </tr>
            </table>
        </div>
    </div>



</html>
