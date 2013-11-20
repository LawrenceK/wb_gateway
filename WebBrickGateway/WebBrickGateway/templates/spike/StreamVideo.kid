<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:ui="ui" 
    py:extends="'master.kid'">


${output_head( mediatitle )}

<body>
    ${output_nav(mediatitle)}
    <div class="objCenter">
    <embed type="application/x-vlc-plugin"
             name="video1"
             id="video1"
             autoplay="yes" loop="yes" width="${width}" height="${height}"
             target="${server}${mediaUrl}" />
    </div>
    <table class="infoTable">
        <tr>
            <td class='playButton' onclick='VLCplay()'>
                Play
            </td>
            <td class='pauseButton' onclick='VLCpause()'>
                Pause
            </td>
            <td class='forwardButton' onclick='VLCskipForward()'>
                Forward
            </td>
            <td class='backButton' onclick='VLCskipBackwards()'>
                Rewind
            </td>
            <td class='stopButton' onclick='VLCstop()'>
                Stop
            </td>
        </tr>
    </table>
</body>

</html>
