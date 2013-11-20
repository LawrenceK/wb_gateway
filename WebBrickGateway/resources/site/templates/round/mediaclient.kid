<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_round
?>

<html py:layout="'sitelayout3.kid'" xmlns:py="http://purl.org/kid/ns#"  xmlns:wb="http://id.webbrick.co.uk/" 
        py:extends="WebBrickGateway.templates.widgets_round">
        
    <div py:match="item.tag == '{http://id.webbrick.co.uk/}leftboxcontent'" id="leftboxcontent">
        <div>
            <ul class="divider29px">
<!--            
                <li py:for='k in clients'>
                    <wb:simpleLinkList target="/media/client?rid=${k}" iconimage="funcicons/funciconaudio.png">
                        Sonos ${clients[k]}
                    </wb:simpleLinkList>
                </li>
-->                
                <li>
                    <wb:simpleLinkList 
                            target="/media/list?rid=${rid}&amp;id=&amp;offset=0&amp;limit=${limit}" 
                            iconimage="funcicons/funciconaudio.png">
                        Browse Library
                    </wb:simpleLinkList>
                </li>
                <li>
                    <wb:simpleLinkList 
                            target="/media/list?rid=${rid}&amp;id=${def_folder}&amp;offset=0&amp;limit=${limit}"
                            iconimage="funcicons/funciconaudio.png"
                            >
                        Current Queue
                    </wb:simpleLinkList>
                </li>
                <li>
                    <wb:simpleAction wbTarget="/media/playqueue?rid=${rid}"
                            iconimage="funcicons/funciconaudio.png"
                            baseClassName="action"
                            >
                        Play Queue
                    </wb:simpleAction>
                </li>
                <li>
                    <wb:simpleAction wbTarget="/media/clearqueue?rid=${rid}"
                            iconimage="funcicons/funciconaudio.png"
                            baseClassName="action"
                            >
                        Clear Queue
                    </wb:simpleAction>
                </li>
                <li>
                    <wb:simpleLinkList target="/media" iconimage="funcicons/funciconaudio.png">
                        Sonos Zones
                    </wb:simpleLinkList>
                </li>
                <li>
                    <wb:simpleLinkList target="/media/zonelink?rid=${rid}"
                        iconimage="funcicons/funciconaudio.png"
                        py:content='"Link Zones"'/>
                </li>
                <li>
                    <wb:simpleAction
                            iconimage="funcicons/funciconaudio.png"
                            wbTarget='/media/dozoneunlink?target=${rid}'
                            baseClassName="action"
                            py:content='"Unlink"'>
                    </wb:simpleAction>
                </li>
                <li>
                    <wb:simpleAction
                            iconimage="funcicons/funciconaudio.png"
                            wbTarget='/media/dozonelinkall?rid=${rid}'
                            baseClassName="action"
                            py:content='"Link All"'>
                    </wb:simpleAction>
                </li>
                <li>
                    <wb:simpleAction
                            iconimage="funcicons/funciconaudio.png"
                            wbTarget='/media/dozoneunlinkall'
                            baseClassName="action"
                            py:content='"UnLink All"'>
                    </wb:simpleAction>
                </li>
<!--                
            <wb:simpleButton wbTarget='/media/dozoneunlink?target=${k}'
                py:content='"UnLink %s from ZoneGroup" % (clients[k])'/>
            <wb:simpleButton wbTarget='/media/dozonelinkall?rid=${k}'
                py:content='"Link All Zones To %s" % (clients[k])' />
-->                
            </ul>
        </div>
        <script type="text/javascript" >
            connect( window, "onload", partial(WbHideableBox_make, "leftbox", "left", "", true) ); 
        </script>
    </div>

    <div py:match="item.tag == '{http://id.webbrick.co.uk/}topboxcontent'" id="topboxcontent">
        <div id="nowplayingtracktitle">
            <h1>
                <wb:textDisplay wbSource="/eventstate/av/transport/state/${udn}?attr=AVTransporttitle"/>
                <wb:textDisplay wbSource="/eventstate/av/transport/state/${udn}?attr=album"/>
                <wb:textDisplay wbSource="/eventstate/av/transport/state/${udn}?attr=title"/>
            </h1>
        </div>
        <div id="albumartbox">
            <div id="albumartframe">
            </div>
            <wb:dynamicImage
                wbSource="/eventstate/av/transport/state/${udn}?attr=albumarturi"
                default_image="/static/images/noalbumart.png"
            />
        </div>
        <div id="transportbar">
            <wb:positionIndicator
                wbDuration='/eventstate/av/transport/state/${udn}?attr=CurrentTrackDuration'
                wbCurPosition='/eventstate/av/transport/state/${udn}?attr=RelativeTimePosition'
                wbTrack='/eventstate/av/transport/state/${udn}?attr=CurrentTrackURI'
                wbState='/eventstate/av/transport/state/${udn}?attr=TransportState'
                width='200'
                height='10'
                >
            </wb:positionIndicator>
            <wb:textDisplay wbSource='/eventstate/av/transport/state/${udn}?attr=TransportState' />
        </div>
<!--                        
        <div id="comingsoon">
            <h2>Coming soon</h2>
            <ul>
                <li>Saltwater - Chicane</li>
                <li>Into the Dawn - Accadia</li>
            </ul>
        </div>
-->                        
    </div>

    <div py:match="item.tag=='{http://id.webbrick.co.uk/}botboxcontent'" id="botboxcontent">
        <wb:imageButton
            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=prev"
            baseClassName="trans"
            iconimage="mediaplayer/trackprevious.png"
        />
        <wb:imageButton
            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=play"
            baseClassName="trans"
            iconimage="mediaplayer/trackplay.png"
        />
        <wb:imageButton
            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=pause"
            baseClassName="trans"
            iconimage="mediaplayer/trackpause.png"
        />
        <wb:imageButton
            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=next"
            baseClassName="trans"
            iconimage="mediaplayer/trackadvance.png"
        />
        <wb:imageButton
                baseClassName="mute"
                wbTarget='/sendevent/av/render/control?type=http://id.webbrick.co.uk/events/av/render/control&amp;udn=${udn}&amp;action=toggleMute'
                wbSource='/eventstate/av/render/state/${udn}?attr=Mute'
                iconimage="mediaoverviewcontrols/muteall.png"
        />
<!-- !        
        <wb:imageButton
            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=prev"
            baseClassName="trans"
            iconimage="mediaplayer/trackrepeat.png"
        />
        <wb:imageButton
            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=prev"
            baseClassName="trans"
            iconimage="mediaplayer/trackrepeatone.png"
        />
        <wb:imageButton
            wbTarget="/sendevent/av/transport/control?type=http://id.webbrick.co.uk/events/av/transport/control&amp;udn=${udn}&amp;action=prev"
            baseClassName="trans"
            iconimage="mediaplayer/trackshuffle.png"
        />
-->        
        <wb:volumeControl
            wbSource='/eventstate/av/render/state/${udn}?attr=Volume'
            wbTarget='/sendevent/av/render/control?type=http://id.webbrick.co.uk/events/av/render/control&amp;udn=${udn}&amp;action=volume&amp;volume='
            height="30"
            >
        </wb:volumeControl>

        <script type="text/javascript" >
            connect( window, "onload", partial(WbHideableBox_make, "botbox", "bottom", "", true) ); 
        </script>

    </div>

</html>
