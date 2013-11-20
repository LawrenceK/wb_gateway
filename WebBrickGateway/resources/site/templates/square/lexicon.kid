<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">

${output_head("Lexicon")}

<body>

${output_nav("Lexicon")}

<table>
    <tr>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/power/on" >
            Power On
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/power/off" >
            Power Off
        </wb:simpleButton>
    </tr>
    <tr>
        <wb:caption>
            Main
        </wb:caption>
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/main/up" >
            Volume Up
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/main/down" >
            Volume Down
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/main/muteon" >
            Mute On
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/main/muteoff" >
            Mute Off
        </wb:simpleButton>
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/hd" >
            HD
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/dvd" >
            DVD
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/game" >
            Game
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/sat" >
            Satelite
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/cable" >
            Cable
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/dvr" >
            DVR
        </wb:simpleButton>
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/cd" >
            CD
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/dock" >
            Dock
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/pc" >
            PC
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/tuner" >
            Tuner
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/aux1" >
            Aux 1
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/main/aucx2" >
            Aux 2
        </wb:simpleButton>
    </tr>

    <tr>
        <wb:caption colspan="6">
            Zone 2
        </wb:caption>
    </tr>

    <tr>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/zone2/up" >
            Volume Up
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/zone2/down" >
            Volume Down
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/zone2/muteon" >
            Mute On
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/volume/zone2/muteoff" >
            Mute Off
        </wb:simpleButton>
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/hd" >
            HD
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/dvd" >
            DVD
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/game" >
            Game
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/sat" >
            Satelite
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/cable" >
            Cable
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/dvr" >
            DVR
        </wb:simpleButton>
    </tr>
    <tr>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/cd" >
            CD
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/dock" >
            Dock
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/pc" >
            PC
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/tuner" >
            Tuner
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/aux1" >
            Aux 1
        </wb:simpleButton>
        <wb:simpleButton wbTarget="/sendevent/lexicon/1/select/zone2/aucx2" >
            Aux 2
        </wb:simpleButton>
    </tr>
</table>

${output_site_info_bar()}


</body>

</html>
