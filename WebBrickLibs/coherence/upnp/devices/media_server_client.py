# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

from coherence.upnp.services.clients import get_service_client

from coherence import log

import coherence.extern.louie as louie

class MediaServerClient(log.Loggable):
    logCategory = 'ms_client'

    def __init__(self, device):
        self.device = device
        self.device_type,self.version = device.get_device_type().split(':')[3:5]
        self.icons = device.icons
        self.scheduled_recording = None
        self.content_directory = None
        self.connection_manager = None
        self.av_transport = None

        self.detection_completed = False

        louie.connect(self.service_notified, signal='Coherence.UPnP.DeviceClient.Service.notified', sender=self.device)

        for service in self.device.get_services():
            if service.get_type() in ["urn:schemas-upnp-org:service:ContentDirectory:1",
                                      "urn:schemas-upnp-org:service:ContentDirectory:2"]:
                self.content_directory = get_service_client( service)
            if service.get_type() in ["urn:schemas-upnp-org:service:ConnectionManager:1",
                                      "urn:schemas-upnp-org:service:ConnectionManager:2"]:
                self.connection_manager = get_service_client( service)
            if service.get_type() in ["urn:schemas-upnp-org:service:AVTransport:1",
                                      "urn:schemas-upnp-org:service:AVTransport:2"]:
                self.av_transport = get_service_client( service)
            #if service.get_type()  in ["urn:schemas-upnp-org:service:ScheduledRecording:1",
            #                           "urn:schemas-upnp-org:service:ScheduledRecording:2"]:
            #    self.scheduled_recording = ScheduledRecordingClient( service)
        self.info("MediaServer %s" % (self.device.get_friendly_name()))
        if self.content_directory:
            self.info("ContentDirectory available")
        else:
            self.warning("ContentDirectory not available, device not implemented properly according to the UPnP specification")
            return
        if self.connection_manager:
            self.info("ConnectionManager available")
        else:
            self.warning("ConnectionManager not available, device not implemented properly according to the UPnP specification")
            return
        if self.av_transport:
            self.info("AVTransport (optional) available")
        if self.scheduled_recording:
            self.info("ScheduledRecording (optional) available")

        #d = self.content_directory.browse(0) # browse top level
        #d.addCallback( self.process_meta)

    def remove(self):
        self.info("removal of MediaServerClient started")
        if self.content_directory != None:
            self.content_directory.remove()
        if self.connection_manager != None:
            self.connection_manager.remove()
        if self.av_transport != None:
            self.av_transport.remove()
        if self.scheduled_recording != None:
            self.scheduled_recording.remove()
        #del self

    def service_notified(self, service):
        self.info("Service %s sent notification" % service);
        if self.detection_completed == True:
            return

        for cl in (self.content_directory,
                self.connection_manager,
                self.av_transport,
                self.scheduled_recording ):
	    if cl != None and cl.service.does_sends_events:
		if cl.service.last_time_updated is None:
                    self.info("detection not yet complete %s (%s)", self, cl.service);
                    return

        self.info("detection complete %s", self);
        self.detection_completed = True
        louie.send('Coherence.UPnP.DeviceClient.detection_completed', None,
                               client=self,udn=self.device.udn)

    def state_variable_change( self, variable, usn):
        self.info(variable.name, 'changed from', variable.old_value, 'to', variable.value)

    def print_results(self, results):
        self.info("results=", results)

    def process_meta( self, results):
        for k,v in results.iteritems():
            dfr = self.content_directory.browse(k, "BrowseMetadata")
            dfr.addCallback( self.print_results)
