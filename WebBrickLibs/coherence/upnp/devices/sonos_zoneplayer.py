# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

from coherence.upnp.services.clients.connection_manager_client import ConnectionManagerClient
from coherence.upnp.services.clients.rendering_control_client import RenderingControlClient
from coherence.upnp.services.clients.av_transport_client import AVTransportClient
from coherence.upnp.services.clients.base_client import BaseClient
from coherence.upnp.services.clients.group_management_client import GroupManagementClient
from coherence.upnp.services.clients.zone_group_topology_client import ZoneGroupTopologyClient

import coherence.extern.louie as louie

from coherence import log

class ZonePlayers():
    def __init__(self):
        self._members = list()

    def find(self, member):
        # do we already have it.
        for mbr in self._members:
            if member.device.get_root_id() == mbr.device.get_root_id():
                return mbr
        return None

    def add(self, member):
        mbr = self.find(member)
        if mbr is None:
            self._members.append(member)

    def remove(self, member):
        mbr = self.find(member)
        if mbr is not None:
            self._members.remove(mbr)

class SonosZonePlayerClient(log.Loggable):

    def __init__(self, device):
        self.device = device
        self.device_type,self.version = device.get_device_type().split(':')[3:5]
        self.detection_completed = False
        self.standalone_group = True
        self.group_members = list()

#        self.icons = device.icons

        louie.connect(self.service_notified, signal='Coherence.UPnP.DeviceClient.Service.notified', sender=self.device)
	self.alarm_clock = None
	self.music_services = None
	self.audio_in = None
	self.device_properties = None
	self.system_properties = None
	self.zone_group_topology = None
	self.group_management = None

        for service in self.device.get_services():
            if service.get_type() in ["urn:schemas-upnp-org:service:AlarmClock:1",
                                      ]:
                self.alarm_clock = BaseClient( service)
            elif service.get_type() in ["urn:schemas-upnp-org:service:MusicServices:1",
					]:
                self.music_services = BaseClient( service)
            elif service.get_type() in ["urn:schemas-upnp-org:service:AudioIn:1",
					]:
                self.audio_in = BaseClient( service)
            elif service.get_type() in ["urn:schemas-upnp-org:service:DeviceProperties:1",
					]:
                self.device_properties = BaseClient( service)
            elif service.get_type() in ["urn:schemas-upnp-org:service:SystemProperties:1",
					]:
                self.system_properties = BaseClient( service)
            elif service.get_type() in ["urn:schemas-upnp-org:service:ZoneGroupTopology:1",
					]:
                self.zone_group_topology = ZoneGroupTopologyClient( service)
            elif service.get_type() in ["urn:schemas-upnp-org:service:GroupManagement:1",
					]:
                self.group_management = GroupManagementClient( service)

        self.info("%s", self.device.get_friendly_name())

    def remove(self):
        self.info("removal of SonosZonePlayer started")
	for cl in ( self.alarm_clock,
		    self.music_services,
		    self.audio_in,
		    self.device_properties,
		    self.system_properties,
		    self.zone_group_topology,
		    self.group_management):
	    if cl != None:
		cl.remove()

    def service_notified(self, service):
        self.info("Service %s sent notification" % service);
        if self.detection_completed == True:
            return

	# TODO this relies on every service sending an initial event set
	# I have seen this not happen
	for cl in ( self.alarm_clock,
		    self.music_services,
		    self.audio_in,
		    self.device_properties,
		    self.system_properties,
		    self.zone_group_topology,
		    self.group_management):
	    if cl != None and cl.service.does_sends_events:
		if cl.service.last_time_updated is None:
                    self.info("detection not yet complete %s (%s)", self, cl.service);
                    return

        self.info("detection complete %s", self);
        self.detection_completed = True
        louie.send('Coherence.UPnP.DeviceClient.detection_completed', None,
                               client=self, udn=self.device.get_id())

    def state_variable_change( self, variable):
        self.info('%s changed from %s to %s', variable.name, variable.old_value, variable.value)

    def get_zone_name( self):
	if self.device_properties:
	    return self.device_properties.service.get_state_variable("ZoneName").value
	return None
