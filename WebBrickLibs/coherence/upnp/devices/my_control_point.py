# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>
import string, logging

from twisted.internet import task
from twisted.internet import reactor
from twisted.web import xmlrpc, client
from twisted.python import threadable

from coherence.upnp.core import service
from coherence.upnp.core.event import EventServer

from coherence.upnp.devices.media_server_client import MediaServerClient
from coherence.upnp.devices.media_renderer_client import MediaRendererClient
from coherence.upnp.devices.sonos_zoneplayer import SonosZonePlayerClient

from coherence.upnp.devices.control_point import ControlPoint

import coherence.extern.louie as louie

_log = logging.getLogger( "coherence.upnp.devices.my_control_point" )

def validateTwistedCall():
    if not threadable.isInIOThread():
        raise Exception("We are not in the event loop")

def choose_resource( server, renderer, item ):
    """
    Go through the itrem and make decision on the resource to use.
    """
    #protInf = self.connection_manager.service.get_state_variable("SinkProtocolInfo").split(',') # hopefully no escaped commas in the string
    # look in item to chose protocol, it is a comma separated string
    #item['resources']   # a dictionary of URI and protocol info
    _log.info( "choose_resource %s", item )
    if item.has_key('resources'):
        return item['resources'].items()[0] # key, protocol pair
    return (None,None)

class Connection(object):
    # a connection that is active or currently being created
    def __init__( self, server, renderer, itm ):
        self._server = server
        self._renderer = renderer
        # some defaults
        self._avt = renderer.av_transport
        self._avtid = 0

    def do_play( self, itm, queue_item ):
        _log.debug('do_play %s from %s on %s', itm, self._server, self._renderer )

        self._itm = itm # may become a list

        def got_error(result):
            _log.error('play %s', result )

        def play_done(param):
            # just so we see it.
            _log.debug('play_done %s', param )

        def start_play(param):
            # just so we see it.
            _log.debug('start_play %s', param )
            # look at current status
            # set 
            df = self._avt.play()
            if df:
                df.addCallback(play_done)
                df.addErrback(got_error)

        def unMute( result ):
            self._log.debug( 'unMute result %s', result )
            df = self._renderer.rendering_control.set_mute(desired_mute=0)
            if df and self._avt.service.get_state_variable("TransportState", self._avtid).value <> "PLAYING":
                df.addCallback(start_play)
            return df

        def set_uri(uri, mdata=''):
            # get the transport
            _log.debug('set_uri %s', uri )
            df = self._avt.set_av_transport_uri(self._avtid, uri, mdata)
            if df:
                cmute = self._renderer.rendering_control.service.get_state_variable("Mute")
                if cmute.value == '1':
                    df.addCallback(unMute)
                elif self._avt.service.get_state_variable("TransportState", self._avtid).value <> "PLAYING":
                    df.addCallback(start_play)
                else:
                    df.addCallback(play_done)

                df.addErrback(got_error)
            return df

        def start_queue(param):
            _log.debug('start_queue %s', param )
            queue_uri = "x-rincon-queue:%s#0" % (self._renderer.device.get_root_uuid())
            df = set_uri(queue_uri) # current queue
            return df

        def queue_uri(uri, mdata):
            # get the transport
# TODO add_uri_to_queue may not be valid , i.e. not SONOS
            _log.debug('queue_uri %s', uri )
            df = self._avt.add_uri_to_queue(self._avtid, uri, mdata)
            if df and self._avt.service.get_state_variable("TransportState", self._avtid).value != "PLAYING":
                df.addCallback(start_queue)
                df.addErrback(got_error)
            return df

        def add_uri():
            if itm['id'] == "Q:0":
                df = start_queue(None)
            else:

                mdata = itm.get('metadata', '' )
                if queue_item:
                    df = queue_uri(uri, itm['metadata'])
                else:
                    df = set_uri(uri, itm['metadata'])
            return df

        def server_connected( connection_id, avt_id, rcs_id ):
            # handle second connection
            _log.debug('server_connected %s avt_id %s rcs_id %s', connection_id, avt_id, rcs_id )
            if avt_id:
                self._avt = server.av_transport
                self._avtid = avt_id
                _log.debug('Have transport from Server %s %s', avt, avt_id )

            df = add_uri()

            return df

        def server_prepare( connection_id ):
            df = self._server.connection_manager.prepare_for_connection(prot, 
                        connection_id, 
                        self._avtid, "Output")
            # return {'ConnectionID': connection_id, 'AVTransportID': avt_id, 'RcsID': rcs_id}
            if df:
                df.addCallback( server_connected )
                df.addErrback(got_error)
            return df

        def renderer_connected( connection_id, avt_id, rcs_id ):
            # handle first connection
            _log.debug('renderer_connected %s avt_id %s rcs_id %s', connection_id, avt_id, rcs_id )
            if avt_id:
                _log.debug('Have transport from Renderer %s %s', renderer.av_transport, avt_id )
                self._avt = renderer.av_transport
                self._avtid = avt_id

            df = self.server_prepare(connection_id)
            if not df:
                _log.debug('MediaServer does not implement PrepareForConnection' )
                df = add_uri()
            return df

        def renderer_prepare():
            # first create renderer connection
            df = self._renderer.connection_manager.prepare_for_connection(prot, 
                            self._server.connection_manager.connection_manager_id(), 
                            -1, "Input")
            # return {'ConnectionID': connection_id, 'AVTransportID': avt_id, 'RcsID': rcs_id}
            if df:
                df.addCallback( renderer_connected )
                df.addErrback(got_error)
            return None

        uri,prot = choose_resource( self._server, self._renderer, self._itm )

        df = renderer_prepare()
        if df is None:
            _log.debug('MediaRenderer does not implement PrepareForConnection' )
            # not implemented on renderer
            df = server_prepare(self._renderer.connection_manager.connection_manager_id())
            if df is None:
                _log.debug('MediaServer does not implement PrepareForConnection' )
                # neither implement prepare
                # look for transport on renderer
                # else transport on server
                df = add_uri()

        return df

    def play_container( self, itm, queue_item ):
        # TODO slow this down.
        _log.debug('play_container %s', itm )

        def got_error(result):
            _log.error('play_container %s', result )

        def play_next_item( param, iter ):
            _log.debug('play_next_item %s %s', param, iter )
            df = None
            try :
                itm = iter.next()
                df = self.play_item( itm, queue_item )
                if df:
                    # df may be None, means no transport or unimplemented play command
                    df.addCallback( play_next_item, iter )
                    df.addErrback(got_error)
            except StopIteration:
                pass
            return df


        def enumerate_and_play( dummy ):
            _log.debug('enumerate_and_play %s', dummy )
            df = play_next_item(None, itm.enumItems())

            if hasattr(itm, "enumContainers"):
	        if df:
		    df.addCallback( play_next_item, itm.enumContainers() )
	        else:
		    # there where no items to play so straight to container.
		    df = play_next_item(None, itm.enumContainers())
            return df


        #enumerate container.
        # this returns deferred if we need to laod container first!
        df = itm.check_for_loaded()

        # TODO This is where I deadlock.
	if df:
	    df.addCallback( enumerate_and_play )
        else:
            df = enumerate_and_play( None )

        return df

    def play_item( self, itm, queue_item ):
        # itm is a UPNP_Item
        # itm._item access the attributes
        validateTwistedCall()

        if itm:
            if itm.id() == "Q:0":
                return self.do_play( itm._item, False )
            elif itm._item.has_key('resources'):
                return self.do_play( itm._item, queue_item )
            else:
                # handle container item?
                return self.play_container(itm, queue_item)

class MyControlPoint(ControlPoint):

    def __init__(self, config, webserver, deviceList):
	self.info("Create MyControlPoint")
        ControlPoint.__init__( self, webserver, deviceList )
#        super(ControlPoint,self).__init__( ws, deviceList )

        self._connections=[] # track them
	self._excludeList = None
	self._includeList = None
	# for now just on model name
	if config.has_key('excludedevice') and config['excludedevice'].has_key('modelName'):
	    self._excludeList = list()
	    excs = config['excludedevice']['modelName']
	    if isinstance( excs, list ):
		for ntry in excs:
		    self.debug("excludedevice %s", ntry)
		    self._excludeList.append( ntry[''].lower() )
	    else:
		self.debug("exclude %s", excs)
		self._excludeList.append( excs[''].lower() )

	if config.has_key('includedevice') and config['includedevice'].has_key('modelName'):
	    self._includeList = list()
	    incs = config['includedevice']['modelName']
	    if isinstance( incs, list ):
		for ntry in incs:
		    self.debug("include %s", ntry)
		    self._includeList.append( ntry[''].lower() )
	    else:
		self.debug("includedevice %s", incs)
		self._includeList.append( incs[''].lower() )

    def is_visible_device( self, device ):
	# Look and see whether we are hiding this device from the local application.
	# used to hide UPNP servers that do not yet work with Gateway
	m_name = device.model_name.lower()
	self.debug("is_visible_device %s", m_name)
	if self._includeList:
	    for k in self._includeList:
		self.debug("is_visible_device includedevice %s", k)
		if m_name.find(k) >= 0:
		    return True
	if self._excludeList:
	    for k in self._excludeList:
		self.debug("is_visible_device excludedevice %s", k)
		if m_name.find(k) >= 0:
		    return False
	return True

    def notify_device( self, client, device, isComplete=False ):
	if self.is_visible_device( device ):
	    ControlPoint.notify_device( self, client, device, isComplete )
	else:
	    self.info("Hiding %s from application", device)

    def play_item( self, server, renderer, item, queue_item ):
        """
        server is a MediaServer object
        renderer is a MediaRenderer object
        itemuri is a dictionary of attributes for the item as returned from browse
        """
	self.info("play_item %s", item)
        if not queue_item and not item._item.has_key('resources')and not item.id() == "Q:0":
            queue_item = True   # override
            self.clear_queue(renderer)

        # TODO see whether we already have a connection to the server/renderer pair.
        connection = Connection( server, renderer, item )
        self._connections.append( connection )
        reactor.callFromThread( connection.play_item, item, queue_item )
#        return connection.play_item( item, queue_item )

    def clear_queue( self, renderer ):
        reactor.callFromThread( renderer.av_transport.clear_queue )

    def check_device( self, device):
        self.info("found device %s of type %s",device.get_friendly_name(), device.get_device_type())
        short_type = device.get_device_type().split(':')[3]
        if short_type == "ZonePlayer":
                self.info("identified ZonePlayer %s", device.get_friendly_name())
                client = SonosZonePlayerClient(device)
                device.set_client(client)
# event sent in self.completed
                louie.send('Coherence.UPnP.ControlPoint.ZonePlayer.detected', None,
                                   client=client,udn=device.get_id())

        ControlPoint.check_device( self, device )
#	super(ControlPoint,self).check_device( device )
	    
