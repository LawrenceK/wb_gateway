<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python 
kid.enable_import()
import WebBrickGateway.templates.master_no_td
import urllib, string
from urllib import quote

# helper to turn a media item into a display string.
def item_string( itm ):
    return string.join( [itm[k] for k in ('artist','creator','album','title') if itm.has_key(k) and itm[k] ], "/" )
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="WebBrickGateway.templates.master_no_td" xmlns:wb="http://id.webbrick.co.uk/">

${output_head( name )}

<body height='100%'>

<!-- override some of the styles -->
<link href="/static/css/media.css" rel="stylesheet" type="text/css" />


    ${output_nav(name)}
    <table>
        <tr>
            <!-- top sub menu -->
        </tr>
    </table>
    <table>
        <col width="400px"/>
        <col width="400px"/>
        <tr>
            <td>
                <!-- status display -->
                <table>
                    <col width="200px"/>
                    <col width="200px"/>
                    <tr>
                        <td colspan='2' >
                            <wb:dynamicImage width='180px' height='180px'
                                wbSource="/eventstate/av/transport/state/${udn}?attr=albumarturi"
                                default_image="/static/images/noalbumart.png"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td colspan='2' >
                        <wb:textDisplay wbSource="/eventstate/av/transport/state/${udn}?attr=album"/>
                        </td>
                    </tr>
                    <tr>
                        <td colspan='2' >
                        <wb:textDisplay wbSource="/eventstate/av/transport/state/${udn}?attr=title"/>
                        </td>
                    </tr>
                    <tr>
                        <td>
                        <wb:textDisplay wbSource="/eventstate/av/transport/state/${udn}?attr=CurrentTrackDuration"/>
                        </td>
                        <td>
                        <wb:textDisplay wbSource="/eventstate/av/transport/state/${udn}?attr=TransportState"/>
                        </td>
                    </tr>
                    <tr>
                        <td>
                        </td>
                    </tr>
                </table>
            </td>
            <td>
                <!-- Controls -->
                <table>
                    <colgroup>
                    </colgroup>
                    <col width="80px"/>
                    <col width="80px"/>
                    <col width="80px"/>
                    <col width="80px"/>
                    <col width="80px"/>
                    <tr>
                        <td colspan='4'>
                        <wb:flashDimmer width='180px' height='180px'
                                            wbSource='/eventstate/av/render/state/${udn}?attr=Volume'
                                            wbTarget='/sendevent/av/render/control?type=http://id.webbrick.co.uk/events/av/render/control&amp;udn=${udn}&amp;action=volume&amp;volume='
                                            metertitle='Volume'
                                            flashMovie="/static/flash/TestVolumeControl.swf"
                                            />
                        </td>
                        <td>
                        <wb:simpleButton
                                baseClassName="muteButton"
                                wbTarget='/sendevent/av/render/control?type=http://id.webbrick.co.uk/events/av/render/control&amp;udn=${udn}&amp;action=toggleMute'
                                wbSource='/eventstate/av/render/state/${udn}?attr=Mute'
                            ></wb:simpleButton>
                        </td>
                    </tr>
                    <tr>
                        <td>
                        <wb:simpleButton
                            baseClassName="prevButton"
                            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=prev"
                        />
                        </td>
                        <td>
                        <wb:simpleButton
                            baseClassName="playButton"
                            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=play"
                        />
                        </td>
                        <td>
                        <wb:simpleButton
                            baseClassName="pauseButton"
                            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=pause"
                        />
                        </td>
                        <td>
                        <wb:simpleButton
                            baseClassName="nextButton"
                            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=next"
                        />
                        </td>
                        <td>
                        <wb:simpleButton
                            baseClassName="stopButton"
                            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=stop"
                        />
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    <table>
        <tr>
            <!-- bottom sub menu -->
            <td>
                <wb:simpleLink target="/media/clients">Show Zones</wb:simpleLink>
            </td>
            <td>
                <wb:simpleLink target="/media/list?rid=${rid}&amp;id=&amp;offset=0&amp;limit=${limit}">Music Library</wb:simpleLink>
            </td>
            <td>
                <wb:simpleLink target="/media/list?rid=${rid}&amp;id=${def_folder}&amp;offset=0&amp;limit=${limit}">Current Queue (C)</wb:simpleLink>
            </td>
            <td>
                <wb:simpleLink target="/media/showqueue?rid=${rid}&amp;id=${def_folder}">Current Queue</wb:simpleLink>
            </td>
        </tr>
    </table>
    
    ${output_site_info_bar()}

</body>

</html>
