# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

from coherence import log

from coherence.upnp.services.clients.base_client import BaseClient

from MiscLib.DomHelpers import getDictFromXmlString

#2008-07-21 15:50:53,546 coherence.upnp.core.service INFO updated var ZoneGroupState - 
#   <ZoneGroups><ZoneGroup Coordinator="RINCON_000E5813306001400" ID="RINCON_000E5813306001400:6"><ZoneGroupMember UUID="RINCON_000E5813306001400" Location="http://193.123.195.200:1400/xml/zone_player.xml" ZoneName="Library" Icon="x-rincon-roomicon:library" SoftwareVersion="8.6-46171" BootSeq="5"/></ZoneGroup><ZoneGroup Coordinator="RINCON_000E581339C201400" ID="RINCON_000E581339C201400:8"><ZoneGroupMember UUID="RINCON_000E581339C201400" Location="http://193.123.195.220:1400/xml/zone_player.xml" ZoneName="Living Room" Icon="x-rincon-roomicon:living" SoftwareVersion="8.6-46171" BootSeq="73"/></ZoneGroup></ZoneGroups> 
#2008-07-21 15:50:53,546 coherence.upnp.core.service INFO updated var AlarmRunSequence - RINCON_000E581339C201400:73:0 
#2008-07-21 15:50:53,546 coherence.upnp.core.service INFO updated var AvailableSoftwareUpdate - <UpdateItem xmlns="urn:schemas-rinconnetworks-com:update-1-0" Type="Software" Version="8.6-46171" UpdateURL="http://update.sonos.com/firmware/Gold/Greenday-v2.5/^8.6-46171" DownloadSize="0"/> 
#2008-07-21 15:50:53,546 coherence.upnp.core.service INFO updated var ThirdPartyMediaServers - <MediaServers><Service UDN="SA_RINCON8_" Md="724856835,GB" Password="00-0E-58-13-39-C2:1" TrialDays="0"/></MediaServers> 

# we should really only need one of these.
# or the data should be global.
class ZoneGroupTopologyClient(BaseClient):
    #  Base for any client to a UPNP service

    def __init__(self, service):
        super(ZoneGroupTopologyClient,self).__init__(service)

        self.subscribe_for_variable("ZoneGroupState", self.zonegroup_update)
# or instead of subscribe
#	    return self.device_properties.service.get_state_variable("ZoneName").value

    def zonegroup_update(self, variable):
        if variable.name == "ZoneGroupState" and variable.value:
            # variable.value is an XML fragment
            zgs = getDictFromXmlString(variable.value)
            self.debug("ZoneGroupState %s", zgs )

            # two separated zones
            #{u'ZoneGroups': 
            #    [
            #        {u'Coordinator': u'RINCON_000E581339C201400', 
            #            u'ZoneGroupMember': {u'UUID': u'RINCON_000E581339C201400', u'SoftwareVersion': u'8.6-46171', u'Location': u'http://193.123.195.220:1400/xml/zone_player.xml', u'BootSeq': u'74', u'ZoneName': u'Living Room', u'Icon': u'x-rincon-roomicon:living'}, 
            #            u'ID': u'RINCON_000E581339C201400:8'
            #        }, 
            #        {u'Coordinator': u'RINCON_000E5813306001400', 
            #            u'ZoneGroupMember': {u'UUID': u'RINCON_000E5813306001400', u'SoftwareVersion': u'8.6-46171', u'Location': u'http://193.123.195.200:1400/xml/zone_player.xml', u'BootSeq': u'6', u'ZoneName': u'Library', u'Icon': u'x-rincon-roomicon:library'}, 
            #            u'ID': u'RINCON_000E5813306001400:8'}
            #    ]
            #}

            # two zones in one zone group
            #{u'ZoneGroups': 
            #    [
            #        {u'Coordinator': u'RINCON_000E5813306001400', 
            #            u'ZoneGroupMember': 
            #                [
            #                    {u'UUID': u'RINCON_000E5813306001400', u'SoftwareVersion': u'8.6-46171', u'Location': u'http://193.123.195.200:1400/xml/zone_player.xml', u'BootSeq': u'6', u'ZoneName': u'Library', u'Icon': u'x-rincon-roomicon:library'}, 
            #                    {u'UUID': u'RINCON_000E581339C201400', u'SoftwareVersion': u'8.6-46171', u'Location': u'http://193.123.195.220:1400/xml/zone_player.xml', u'BootSeq': u'74', u'ZoneName': u'Living Room', u'Icon': u'x-rincon-roomicon:living'}
            #                ], 
            #            u'ID': u'RINCON_000E5813306001400:8'
            #        }
            #    ]
            #}