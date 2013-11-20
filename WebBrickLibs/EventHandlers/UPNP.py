#
#
import logging

from xml.sax.saxutils import escape, unescape

import threading, time
#from threading import Event

from urlparse import urlparse,urljoin

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

from MiscLib.DomHelpers       import *
from MiscLib.TimeUtils        import *

import coherence.extern.louie as louie

from coherence.upnp.core import DIDLLite

from coherence.base import Coherence
#
# This is so we can publish the dynamic updates to a UPNP service.
# TODO We need to do a periodic read of track position and publish.
#
class UPNP( BaseHandler ):
    """
    """
    def __init__ (self, localRouter):
        super(UPNP,self).__init__(localRouter)
        self._clients = {}

    def new_renderer(self, client, udn ):
        self._log.info( "new_renderer %s ", udn )
        self._clients[udn] = client
        name = client.device.get_friendly_name()
        self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/client", 
                "upnp/%s"%(name), { 'udn':udn, 'name': name } ) )

        # subscribe to changes.
        if client.rendering_control:
            louie.connect(self.render_service_update, 
                    'Coherence.UPnP.StateVariable.changed', 
                    client.rendering_control.service )

        if client.av_transport:
            louie.connect(self.transport_service_update, 
                    'Coherence.UPnP.StateVariable.changed', 
                    client.av_transport.service )

        if client.connection_manager:
            louie.connect(self.connection_manager_update, 
                    'Coherence.UPnP.StateVariable.changed', 
                    client.connection_manager.service )
        self.clear_renderer(udn)
        # get transport variables and ensure system knows them..
        for vname in ("CurrentTrackMetaData", "CurrentTrackDuration", 'TransportState'):
            self.transport_service_update(client.av_transport.service.get_state_variable(vname))
        # get renderer variables
        for vname in ("Volume","Mute"):
            self.render_service_update(client.rendering_control.service.get_state_variable(vname))
        

    def remove_renderer(self, client, udn ):
        if self._clients.has_key(udn):

            name = client.device.get_friendly_name()
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/client/delete", 
                    "upnp/%s"%(name), { 'udn':udn, 'name': name } ) )
            if client.rendering_control:
                louie.disconnect(self.render_service_update, 
                        'Coherence.UPnP.StateVariable.changed', 
                        client.rendering_control.service )

            if client.av_transport:
                louie.disconnect(self.transport_service_update, 
                        'Coherence.UPnP.StateVariable.changed', 
                        client.av_transport.service )

            if client.connection_manager:
                louie.disconnect(self.connection_manager_update, 
                        'Coherence.UPnP.StateVariable.changed', 
                        client.connection_manager.service )

            del self._clients[udn]
        self.clear_renderer(udn)

    def clear_renderer(self, udn ):
        self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/transport/state", 
                "av/transport/state/%s"%(udn), 
                { 'udn':udn, 'album':'', 'title':'', 'CurrentTrackDuration':'', 'albumarturi':'' } ) )

    def render_service_update(self, variable ):
        # locate udn and generate 
        # generate http://id.webbrick.co.uk/events/av/render/state
        self._log.info( "render_service_update %s ", variable )

        # generate http://id.webbrick.co.uk/events/av/render/state
        udn = variable.service.device.get_id()
        if variable.name != "LastChange":
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/render/state", 
                    "av/render/state/%s"%(udn), { 'udn':udn, variable.name:variable.value } ) )

    def send_metadata(self, srvc, udn, mdata, prefix ):
        # decode meta data, if not blank
        self._log.debug( "send_metadata %s %s '%s'", prefix, udn, mdata )
        # PS: We will need a more sophisticated check against this meta data !! Very large error logs
        if mdata and mdata != "NOT_IMPLEMENTED":
            try:
                elt = DIDLLite.DIDLElement.fromString(mdata)
                for itm in elt.getItems():
                    self._log.info( "send_metadata %s", itm )
                    for k in itm.__dict__:
                        self._log.info( "    %s %s", k, itm.__dict__[k] )
                    od = {'udn':udn, '%salbum'%(prefix):itm.album, '%stitle'%(prefix):itm.title }
                    if itm.albumArtURI:
                        # TODO is this correct for accessing album art?
                        # use urljoin.
                        od['%salbumarturi'%(prefix)] = urljoin( srvc.device.get_url_base(), itm.albumArtURI)
              	        # od['albumarturi'] = "%s%s" % ( variable.service.url_base, itm.albumArtURI)
                    else:
                        # should give a blank image URI
                        od['%salbumarturi'%(prefix)] = ''

                    self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/transport/state", 
                            "av/transport/state/%s"%(udn), od ) )
            except Exception, ex:
                self._log.exception(ex)

    def transport_service_update(self, variable ):
        # locate udn and generate 
        # generate http://id.webbrick.co.uk/events/av/transport/state
        # TODO if change of track and device does not support current position generate them.
        # TODO handle transport instances, for now assumes 0.
        self._log.info( "transport_service_update %s ", variable )
        udn = variable.service.device.get_id()
        if variable.name == "CurrentTrackMetaData":
            # do not use if this is an internet radio station.
            if not variable.service.get_state_variable("CurrentTrackURI").value.startswith("x-rincon-mp3radio:"):
                self.send_metadata( variable.service, udn, variable.value, "" )
            else:
                # all I want is aa station name
                self.send_metadata( variable.service, udn, variable.service.get_state_variable("AVTransportURIMetaData").value, "AVTransport" )
                pass
        elif variable.name == "NextTrackMetaData":
            self.send_metadata( variable.service, udn, variable.value, "Next" )
        elif variable.name == "EnqueuedTransportURIMetaData":
            self.send_metadata( variable.service, udn, variable.value, "Enqueued" )
        elif variable.name == "AVTransportURIMetaData":
            self.send_metadata( variable.service, udn, variable.value, "AVTransport" )
        elif variable.name == "TransportState" and variable.value == "STOPPED":
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/transport/state", 
                    "av/transport/state/%s"%(udn), { 'udn':udn, variable.name:variable.value,
                                 'album':'', 'title':'', 'albumarturi':'',
                                 'CurrentTrackDuration':'',
                                 'Nextalbum':'', 'Nexttitle':'', 'Nextalbumarturi':'',
                                 'Enqueuedalbum':'', 'Enqueuedtitle':'', 'Enqueuedalbumarturi':'',
                                 'AVTransportalbum':'', 'AVTransporttitle':'', 'AVTransportalbumarturi':''
                                 } ) )
        elif variable.name in ["RelativeTimePosition", "AbsoluteTimePosition", "CurrentTrackDuration"]:
            if variable.value != "NOT_IMPLEMENTED":
                self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/transport/state", 
                        "av/transport/state/%s"%(udn), { 'udn':udn, variable.name:parseTime(variable.value) } ) )
        elif variable.name != "LastChange":
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/transport/state", 
                    "av/transport/state/%s"%(udn), { 'udn':udn, variable.name:variable.value } ) )

    def connection_manager_update(self, variable ):
        # locate udn and generate 
        # generate http://id.webbrick.co.uk/events/av/connection/state
        self._log.info( "connection_manager_update %s ", variable )
        udn = variable.service.device.get_id()
        if variable.name != "LastChange":
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/connection/state", 
                    "av/connection/state/%s"%(udn), { 'udn':udn, variable.name:variable.value } ) )

    def new_server(self, client, udn ):
        self._log.info( "new_server %s ", udn )
        self._clients[udn] = client
        name = client.device.get_friendly_name()
        self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/server", 
                "upnp/%s"%(name), { 'udn':udn, 'name': name } ) )
        # generate http://id.webbrick.co.uk/events/av/render/state
        # generate http://id.webbrick.co.uk/events/av/transport/state
        # generate http://id.webbrick.co.uk/events/av/connection/state
        # subscribe to changes.

    def remove_server(self, client, udn ):
        if self._clients.has_key(udn):
            name = client.device.get_friendly_name()
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/server/delete", 
                    "upnp/%s"%(name), { 'udn':udn, 'name': name } ) )
            del self._clients[udn]

    def actionSuccess( self, data, action ):
        #self._log.debug("HTTP %s success targetUrl http://%s%s/n%s" % (action["cmd"],action["address"],action["uri"],data) )
        self._log.debug("UPNP success targetUrl http://%s/n%s" % (action,data) )

    def actionError( self, failure, action ):
        #self._log.error("HTTP %s error %s targetUrl http://%s%s" % (failure,action["cmd"],action["address"],action["uri"]) )
        self._log.error("UPNP error %s targetUrl http://%s" % (failure,action) )

    def configure( self, cfgDict ):
        self._upnpcfg = cfgDict

    def start(self):
        self._log.debug( 'start' )
        BaseHandler.start(self)
        self._upnpcfg['controlpoint'] = 'yes'   # force it

        self._coherence = Coherence()

        # ensure coherence calls to twisted are made on the reactor thread.
        # twisted is not thread safe.
        from twisted.internet import reactor
        reactor.callFromThread(self._coherence.setup, self._upnpcfg )
        #self._coherence.setup(self._upnpcfg)
        #self._coherence.start()


        # subscribe to media control events
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/render/control' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/transport/control' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/connection/control' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/second' )

        # coherence events
        louie.connect(self.new_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.detected', louie.Any)
        louie.connect(self.new_server, 'Coherence.UPnP.ControlPoint.MediaServer.detected', louie.Any)
        louie.connect(self.remove_server, 'Coherence.UPnP.ControlPoint.MediaServer.removed', louie.Any)
        louie.connect(self.remove_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.removed', louie.Any)

    def stop(self):
        self._log.debug( 'stop' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/render/control' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/transport/control' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/connection/control' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/second' )

        # coherence events
        louie.disconnect(self.new_server, 'Coherence.UPnP.ControlPoint.MediaServer.detected', louie.Any)
        louie.disconnect(self.new_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.detected', louie.Any)
        louie.disconnect(self.remove_server, 'Coherence.UPnP.ControlPoint.MediaServer.removed', louie.Any)
        louie.disconnect(self.remove_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.removed', louie.Any)

        BaseHandler.stop(self)

    def gotError( self, failure ):
        self._log.error( 'gotError control result %s', failure )

    def noError( self, result ):
        self._log.debug( 'noError control result %s', result )

    def handleTransportControl( self, inEvent ):
#        if inEvent.getSource() == "http://id.webbrick.co.uk/events/av/control" :
        od = inEvent.getPayload()
        if od.has_key("udn") and self._clients.has_key(od["udn"]):
            # get client.
            client = self._clients[od["udn"]]
            self._log.debug( 'handleTransportControl %s %s', client, od )
            # we need action and a renderer with an av transport
            if od.has_key("action"):
#            if od.has_key("action") and client.av_transport:
                df = None
                action = od["action"]
                if action == "play":
                    df = client.av_transport.play()
                elif action == "pause":
                    df = client.av_transport.pause()
                elif action == "stop":
                    df = client.av_transport.stop()
                elif action == "next":
                    df = client.av_transport.next()
                elif action == "prev":
                    df = client.av_transport.previous()
                if df:
                    df.addCallbacks(self.noError, self.gotError)
                    self.checkIfMuted( client, df )

    def unMute( self, result, client ):
        self._log.debug( 'unMute result %s %s', client, result )
        df = client.rendering_control.set_mute(desired_mute=0)
        return df

    def checkIfMuted( self, client, df ):
        cmute = client.rendering_control.service.get_state_variable("Mute")
        self._log.debug( 'checkIfMuted %s %s', client, cmute.value )
        if cmute.value == '1':
            df.addCallback(self.unMute, client)

    def handleRenderControl( self, inEvent ):
#        if inEvent.getSource() == "http://id.webbrick.co.uk/events/av/control" :

        od = inEvent.getPayload()
        if od.has_key("udn") and self._clients.has_key(od["udn"]):
            # get client.
            client = self._clients[od["udn"]]
            self._log.debug( 'handleRenderControl %s %s', client, od )
            action = "volume"
            df = None
            if od.has_key("action"):
                action = od["action"]

            if action == "volume" or od.has_key("volume"):
                volume = od["volume"]
                df = client.rendering_control.set_volume(desired_volume=volume)
                if df:
                    df.addCallbacks(self.noError, self.gotError)
                    self.checkIfMuted( client, df )

            elif action == "toggleMute":
                mute = 1
                if client.rendering_control.service.get_state_variable("Mute").value == '1':
                    mute = 0
                df = client.rendering_control.set_mute(desired_mute=mute)
                if df:
                    df.addCallbacks(self.noError, self.gotError)

    def handleConnectionControl( self, inEvent ):
#        if inEvent.getSource() == "http://id.webbrick.co.uk/events/av/control" :
        od = inEvent.getPayload()
        if od.has_key("udn") and self._clients.has_key(od["udn"]):
            # get client.
            client = self._clients[od["udn"]]
            self._log.debug( 'handleConnectionControl %s %s', client, od )
            if od.has_key("action"):
                action = od["action"]
                df = None
                if action == "play":
                    df = client.connection_manager.play()
                elif action == "pause":
                    df = client.connection_manager.pause()
                elif action == "stop":
                    df = client.connection_manager.stop()
                elif action == "next":
                    df = client.connection_manager.next()
                elif action == "prev":
                    df = client.connection_manager.previous()
                if df:
                    self.checkIfMuted( client, df )
                    df.addCallbacks(self.noError, self.gotError)

    def newPositionInfo( self, result, udn, srvc ):
    #def newPositionInfo( self, Track, TrackDuration, TrackMetaData, TrackURI, RelTime, AbsTime, RelCount, AbsCount ):
        self._log.debug( 'newPositionInfo %s', result )
        # 'AbsTime': 'NOT_IMPLEMENTED', 
        # 'Track': '1', 
        # 'TrackDuration': '0:00:00', 
        # 'TrackURI': 'x-rincon-mp3radio://mvy-mp3.andohs.net/ice96', 
        # 'AbsCount': '2147483647', 
        # 'TrackMetaData': '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/"><item id="-1" parentID="-1" restricted="true"><res protocolInfo="x-rincon-mp3radio:*:*:*">x-rincon-mp3radio://mvy-mp3.andohs.net/ice96</res><r:streamContent>BOB DYLAN - TANGLED UP IN BLUE</r:streamContent><dc:title>ice96</dc:title><upnp:class>object.item</upnp:class></item></DIDL-Lite>', 
        # 'RelCount': '2147483647', 
        # 'RelTime': '0:01:00'}
        self.send_metadata( srvc, udn, result['TrackMetaData'], "" )
        if result['TrackDuration'] == '0:00:00':
            pos = parseTime(result['RelTime'] )
            guess = 300
            while pos > guess:
                guess = guess + 300
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/transport/state", 
                    "av/transport/state/%s"%(udn), { 'udn':udn, 'CurrentTrackDuration':guess } ) )

    # TODO rework and use twisted callLater/repeat to call this.
    def getTransportPosition( self, inEvent ):
        # update perceived position
        # Every x seconds get position from UPNP device
        # use modulo arithmatic on length of clients, so we test one each time through.
        # but never more than each every 5 seconds
        curidx = len(self._clients)
        if curidx < 5:
            curidx = 5
        curidx = int(inEvent.getPayload()["second"]) % curidx
        for k in self._clients:
            client = self._clients[k]
            if client.av_transport:
                if client.av_transport.service.get_state_variable("TransportState").value == "PLAYING":
                    curTimeVar = client.av_transport.service.get_state_variable("RelativeTimePosition")
                    if curTimeVar and curTimeVar.value:
                        # update and publish
                        pos = parseTime(curTimeVar.value)
                        self._log.debug( 'RelativeTimePosition %s %s', curTimeVar.value, pos )
                        curTimeVar.value = formatTime( pos+1 )
                        self._log.debug( 'RelativeTimePosition %s %s', curTimeVar.value, pos )
                        self.transport_service_update(curTimeVar)
                    if curidx == 0:
                        df = client.av_transport.get_position_info()
                        df.addCallback(self.newPositionInfo, k, client.av_transport )
                        df.addErrback(self.gotError)
                    curidx = curidx - 1

    def doHandleEvent( self, handler, inEvent ):
        try:
            # we need to handle this on the recator thread as it will
            # very likely make network calls to a UPNP device that MUST
            # be processed on the reactor thread.
            # defer import to here so we can install alternate reactors.
            from twisted.internet import reactor
            if inEvent.getType() == "http://id.webbrick.co.uk/events/time/second" :
                reactor.callFromThread( self.getTransportPosition, inEvent )
            else:
                self._log.debug( 'doHandleEvent %s', inEvent )
                if inEvent.getType() == "http://id.webbrick.co.uk/events/av/render/control" :
                    reactor.callFromThread( self.handleRenderControl, inEvent )
                if inEvent.getType() == "http://id.webbrick.co.uk/events/av/transport/control" :
                    reactor.callFromThread( self.handleTransportControl, inEvent )
                if inEvent.getType() == "http://id.webbrick.co.uk/events/av/connection/control" :
                    reactor.callFromThread( self.handleConnectionControl, inEvent )
        except Exception, ex:
            self._log.exception(ex)

        return makeDeferred(StatusVal.OK)

