# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

import logging
from twisted.internet import task, defer
from twisted.internet import reactor

import coherence.extern.louie as louie

from coherence.upnp.core.device import RootDevice

_log = logging.getLogger( "coherence.DeviceList" )

# this is a list of root devices!
class DeviceList(object):

    def __init__(self):
        self._devices = {}  # keyed by udn
#        self._devices = []
        louie.connect( self.create_device, 'Coherence.UPnP.SSDP.new_device', louie.Any)
        louie.connect( self.remove_device, 'Coherence.UPnP.SSDP.removed_device', louie.Any)
        louie.connect( self.add_device, 'Coherence.UPnP.RootDevice.detection_completed', louie.Any)

        #self.renew_service_subscription_loop = task.LoopingCall(self.check_devices)
        # what if the device under question gives less than 20 seconds as the timeout.
        #self.renew_service_subscription_loop.start(20.0, now=False)

        reactor.addSystemEventTrigger( 'before', 'shutdown', self.shutdown)

    def check_devices(self):
        """ iterate over devices and their embedded ones and renew subscriptions """
        for udn in self._devices:
            root_device = self._devices[udn]
            root_device.renew_service_subscriptions()

    def get_device_by_host(self, host):
        found = []
        for udn in self._devices:
            device = self._devices[udn]
            if device.get_host() == host:
                found.append(device)
        return found

    def get_device_with_usn(self, usn):
        found = None
        for ky in self._devices:
            if self._devices[ky].get_usn() == usn:
                found = self._devices[ky]
                break
        return found

    def get_device_with_id(self, device_id):
        # actually a udn.
        found = None
	if self._devices.has_key(device_id):
	    found = self._devices[device_id]

#        for device in self._devices:
#            id = device.get_id()
#            if device_id[:5] != 'uuid:':
#                id = id[5:]
#            if id == device_id:
#                found = device
#                break

	_log.debug("get_device_with_id %s (%s)", device_id, found )
        return found

    def get_nonlocal_devices(self):
        return [self._devices[d] for d in self._devices if self._devices[d].manifestation == 'remote']

    def create_device(self, device_type, infos):
        # the louie event is only triggerred for a root device.
        root = RootDevice(infos)
        # add_device will be called after rood detection completes

    def add_device(self, device):
	_log.debug("add_device %s (%s)", device.get_id(), device )
        self._devices[device.get_id()]= device

    def remove_device(self, device_type, infos):
        _log.info("removed device %s %s", infos['ST'], infos['USN'] )
        device = self.get_device_with_usn(infos['USN'])
        if device:
            del self._devices[device.get_id()]
            if infos['ST'] == 'upnp:rootdevice':
                louie.send('Coherence.UPnP.Device.removed', None, udn=device.get_id() )
            device.remove()

    def shutdown( self):
        """ send service unsubscribe messages """
        try:
            self.renew_service_subscription_loop.stop()
        except:
            pass
        l = []
        for ky in self._devices:
	    root_device = self._devices[ky]
            for device in root_device.get_devices():
                d = device.unsubscribe_service_subscriptions()
                l.append(d)
                d.addCallback(device.remove)
            d = root_device.unsubscribe_service_subscriptions()
            l.append(d)
            d.addCallback(root_device.remove)

        dl = defer.DeferredList(l)
        return dl
