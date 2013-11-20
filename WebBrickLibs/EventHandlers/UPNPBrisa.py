# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: UPNPBrisa.py 3199 2009-06-15 15:21:25Z philipp.schuster $
#
# Class to interface with Brisa UPnP framework
#
# Philipp Schuster
#

import logging, threading


from brisa.core.reactors import install_default_reactor
reactor = install_default_reactor()


from brisa.upnp.control_point.control_point_webbrick import ControlPointWB

from MiscLib.DomHelpers         import getDictFromXmlString
from urlparse import urlparse,urljoin

from EventLib.Event             import Event
from EventLib.Status            import StatusVal
from EventLib.SyncDeferred      import makeDeferred

from EventHandlers.BaseHandler  import BaseHandler

from MiscLib.DomHelpers         import *
from MiscLib.TimeUtils          import *

   
#
# This is so we can publish the dynamic updates to a UPNP service.
#
class UPNPBrisa( BaseHandler, threading.Thread ):
    """
        Class to provide a UPnP controlpoint based on Brisa framework
        Features: 
            -
             
        TODO:
            -     
    """   
    
    CDS_namespace = 'urn:schemas-upnp-org:service:ContentDirectory:1'
    AVT_namespace = 'urn:schemas-upnp-org:service:AVTransport:1'
    DMS_type = 'urn:schemas-upnp-org:device:MediaServer:'
    DMR_type = 'urn:schemas-upnp-org:device:MediaRenderer:'     
    
    def __init__ (self, localRouter):
        BaseHandler.__init__(self, localRouter)
        self._devicesFound = {}
        self._devicesIncluded = {}
        self._renderers = {}
        self._includeList = None
        self._excludeList = None
        self._controlpoint = None
        threading.Thread.__init__(self)
        self.setDaemon( True )

    def configure( self, cfgDict ):
        self._upnpcfg = cfgDict
        # Process excludedevice
        if self._upnpcfg.has_key('excludedevice') and self._upnpcfg['excludedevice'].has_key('modelName'):
            excs = self._upnpcfg['excludedevice']['modelName']
            self._excludeList = list()
            if isinstance( excs, list ):
                for ntry in excs:
                    self._log.debug("excludedevice %s", ntry)
                    self._excludeList.append( ntry[''].lower() )
            else:
                self._log.debug("exclude %s", excs)
                self._excludeList.append( excs[''].lower() )
        # Process includedevice    
        if self._upnpcfg.has_key('includedevice') and self._upnpcfg['includedevice'].has_key('modelName'):
            incs = self._upnpcfg['includedevice']['modelName']
            self._includeList = list()
            if isinstance( incs, list ):
                for ntry in incs:
                    self._log.debug("include %s", ntry)
                    self._includeList.append( ntry[''].lower() )
            else:
                self._log.debug("includedevice %s", incs)
                self._includeList.append( incs[''].lower() )

    def start(self):
        self._log.debug( 'starting' )
        
        BaseHandler.start(self)
        
        self._upnpcfg['controlpoint'] = 'yes'   # force it
        
        self._controlpoint = ControlPointWB()
        
        # subscribe to gateway events that are of interest
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/runtime' )
        
        # subscribe to media control events
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/upnp/debug' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/transport/control' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/av/connection/control' )

        # subscribe to brisa events events
        self._controlpoint.subscribe('new_device_event', self.on_new_device)
        self._controlpoint.subscribe('removed_device_event', self.on_removed_device)
        
        # start the control point
        self._controlpoint.start()
        
        # TODO: Does this have to be doen here or can we do this in the stop function?
        reactor.add_after_stop_func(self._controlpoint.destroy)
        
        # start seperate thread for brisa reactor
        threading.Thread.start(self)
        
         
        
    def stop(self):
        self._log.debug( 'stop' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/upnp/debug' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/transport/control' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/av/connection/control' )
        
        # unsubscribe from brisa events events
        self._controlpoint.unsubscribe('new_device_event', self.on_new_device)
        self._controlpoint.unsubscribe('removed_device_event', self.on_removed_device)
        
        # stop the control point
        # TODO: Atm done in start by adding after_stop_func to raector
        # self._controlpoint.stop()

        BaseHandler.stop(self)
        print "about to stop"
        reactor.main_quit()
        
    def run(self):
        """
            Called on new thread, when the Tread is started
            Lets Brisa Reactor run on seperate thread
            NOTE: Need to avoid race conditions in the rest of the design! 
        """
        self._log.debug( 'Enter run on Brisa Reactor Thread' )
        reactor.main()
    
    def doHandleEvent( self, handler, inEvent ):
        try: 
            self._log.debug( 'doHandleEvent %s', inEvent )
            if inEvent.getType() == 'http://id.webbrick.co.uk/events/upnp/debug':
                self.doHandleUpnpDebug( inEvent )

            elif inEvent.getType() == "http://id.webbrick.co.uk/events/av/transport/control" :
                self.doHandleAVTransport( inEvent )
                
            elif inEvent.getType() == "http://id.webbrick.co.uk/events/av/connection/control" :
                self.doHandleZone( inEvent )
            
            elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/runtime" :
                self.doHandleRuntime( inEvent )
            
            else:
                # unexpected 
                self._log.error( "Not expecting this event %s", inEvent.getType() )
        except Exception, ex: 
            self._log.exception(ex)

        return makeDeferred(StatusVal.OK)
    
    def doHandleUpnpDebug(self, inEvent):
        src = inEvent.getSource().split("/")
        if src[1] == "search":
            self._log.info( "Start search for new UPnP devices" )
            self._controlpoint.start_search(600, 'upnp:rootdevice')
            
        
        elif src[1] == "stop":
            self._log.info( "Stop search for new UPnP devices" )
            self._controlpoint.stop_search()
            
        elif src[1] == "list":
            n = 0
            if src[2] == "all":
                self._log.info( "List all discovered UPnP devices" )
                for device in self._devicesFound.values():
                    self._log.info( "Device %d:" % n)
                    self._log.info( "udn: %s", device.udn)
                    self._log.info( "friendly_name: %s", device.friendly_name)
                    self._log.info( "type: %s", device.device_type)
                    n += 1
            elif src[2] == "included":
                self._log.info( "List included discovered UPnP devices" )
                for device in self._devicesIncluded.values():
                    self._log.info( "Device %d:" % n)
                    self._log.info( "udn: %s", device.udn)
                    self._log.info( "friendly_name: %s", device.friendly_name)
                    self._log.info( "type: %s", device.device_type)
                    n += 1
                    
        elif src[1] == "play":
            self._log.info( "Stop search for new UPnP devices" )
            self._controlpoint.stop_search()

    def doHandleRuntime( self, inEvent ):
        od = inEvent.getPayload()
        #TODO: Probably more reasonable to start this search later
        if int(od["elapsed"]) == 10:
            self._log.info( "Start search for new UPnP devices" )
            self._controlpoint.start_search(600, 'upnp:rootdevice')
            
        
    

    def doHandleAVTransport(self, inEvent):
        src = inEvent.getSource()
        if src == "av/transport/control":
            payload = inEvent.getPayload()
            if payload.has_key("udn") and payload.has_key("action"):
                udn = payload["udn"]
                if payload["action"] == "play":
                    try:
                        self._controlpoint.set_current_renderer(self.get_device(udn))
                        self._controlpoint.av_play()
                        self._log.info("Sent play")
                    except Exception, ex:
                        self._log.exception( ex )
                        
                elif payload["action"] == "stop":
                    try:
                        self._controlpoint.set_current_renderer(self.get_device(udn))
                        self._controlpoint.av_stop()
                        self._log.info("Sent stop")
                    except Exception, ex:
                        self._log.exception( ex )
                                
                elif payload["action"] == "pause":
                    try:
                        self._controlpoint.set_current_renderer(self.get_device(udn))
                        self._controlpoint.av_pause()
                        self._log.info("Sent pause")
                    except Exception, ex:
                        self._log.exception( ex )
                        
                elif payload["action"] == "next":
                    try:
                        self._controlpoint.set_current_renderer(self.get_device(udn))
                        self._controlpoint.av_next()
                        self._log.info("Sent next")
                    except Exception, ex:
                        self._log.exception( ex )
                        
                elif payload["action"] == "previous":
                    try:
                        self._controlpoint.set_current_renderer(self.get_device(udn))
                        self._controlpoint.av_previous()
                        self._log.info("Sent previous")
                    except Exception, ex:
                        self._log.exception( ex )
                
                elif payload["action"] == "shuffle":
                    try:
                        self._controlpoint.set_current_renderer(self.get_device(udn))
                        self._controlpoint.av_playmode("SHUFFLE_NOREPEAT")
                        self._log.info("Sent shuffle_norepeat")
                    except Exception, ex:
                        self._log.exception( ex )
                        
                elif payload["action"] == "repeat":
                    try:
                        self._controlpoint.set_current_renderer(self.get_device(udn))
                        self._controlpoint.av_playmode("REPEAT_ALL")
                        self._log.info("Sent repeat_all")
                    except Exception, ex:
                        self._log.exception( ex )   
                        
            else:
                self._log.error("Payload not correct - payload: %s" % payload)
    
    def get_device(self, udn, search_nested=True, search_all=False):
        """
            Function to return device from inclused devices
            
        """
        result = None
                 
        if search_all:
            devices = self._devicesFound
        else: 
            devices = self._devicesIncluded
            
        if devices.has_key(udn):
            # found the device (is root device)
            result = devices[udn]
            
        elif search_nested:
            #Lets try and search nested devices 
            for dev in devices.values():
                if dev.devices:
                    for embedded_dev in dev.devices.values():
                        if embedded_dev.udn == udn:
                            result = embedded_dev
                    
                
        return result
        
    def on_new_device(self, dev):
        """
            Callback, is triggered when a new device is found.
            We keep a record of all devices we find, but operate
            on a limited number of devices stored in a seperate dict. 
        """
        self._log.info( 'Found new device: %s', dev.udn )
        print "NEW DEVICE %s" %dev.udn
        self.process_new_device(dev)

    def on_removed_device(self, udn):
        """ 
            Callback, is triggered when a device leaves the network.
        """
        self._log.info( 'Device Gone: %s', udn )
        self.remove_device(udn)
          
           
    def process_new_device(self, dev ):
        """
            This function processes any new devices that are found in as 
            followed:
            1. Add all root devices to the devices found dict.
            2. Add all root devices that are identified as included to 
               the devicesIncluded dict
            3. Find included (including none root) MediaRenders and call 
               process_process_new_renderer
        """
        self._log.debug( 'Processing new device: %s', dev.udn)
        
        self._devicesFound[dev.udn] = dev
        
        if self.check_include(dev.model_name.lower()):
            self._log.debug( 'Including new device: %s', dev.udn )
            self._devicesIncluded[dev.udn] = dev
            self.sendNumberOfDevices(len(self._devicesIncluded))
            self.sendDevicesDiscoveryInfo(len(self._devicesIncluded), dev.udn, dev.model_name.lower())
            
            self._log.debug( "New Device's Type is: %s", dev.device_type )
            if dev.device_type == "urn:schemas-upnp-org:device:MediaRenderer:1":
                self.process_new_renderer(dev)
                self.sendRendererDiscoveryInfo(len(self._devicesIncluded), 1, dev.udn)
            
            
            if dev.devices:
                self._log.debug( 'Processing embedded devices of: %s', dev.udn )
                i = 1
                for embedded_dev in dev.devices.values():
                    self._log.debug( "Embedded Device's Type is: %s", embedded_dev.device_type )
                    if embedded_dev.device_type == "urn:schemas-upnp-org:device:MediaRenderer:1":
                        self.sendRendererDiscoveryInfo(len(self._devicesIncluded), i, embedded_dev.udn)
                        self.process_new_renderer(embedded_dev)
                        i = i + 1
                
    def remove_device(self, udn ):
        if self._devicesFound.has_key(udn):
            self._log.info( 'Removing Device: %s', udn )
            del self._devicesFound[udn]
        if self._devicesIncluded.has_key(udn):
            self._log.info( 'Removing Device from INCLUDED devices: %s', udn )
            del self._devicesIncluded[udn]
    
    def check_include (self, model_name):
        self._log.debug( 'Check whether to include: %s', model_name )
        include = False
        if self._includeList:
            for ntry in self._includeList:
                self._log.debug( 'check_include - is include entry: %s  in model_name: %s' % (ntry, model_name) )
                if ntry in model_name:
                    include = True
        return include    
    
    
    def sendNumberOfDevices(self, count):
        self.sendEvent( Event("http://id.webbrick.co.uk/events/upnp/system",
            "upnp/device/count",
            {'val': count} ) )
            
    def sendDevicesDiscoveryInfo(self, device_number, udn, model):
        self.sendEvent( Event("http://id.webbrick.co.uk/events/upnp/system",
            "upnp/device/%s" %device_number,
            {'udn': udn,
             'model': model} ) )
   
    def sendRendererDiscoveryInfo(self, device_number, renderer_number, udn):
        self.sendEvent( Event("http://id.webbrick.co.uk/events/upnp/system",
            "upnp/device/%s/%s" %(device_number,renderer_number),
            {'udn': udn} ) )
    
    def process_new_renderer(self, dev ):
        name = dev.friendly_name
        udn = dev.udn
        self._log.debug( 'Processing new render: %s', name )
        
        self._renderers[udn] = dev
        
        self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/client", 
                "upnp/%s"%(udn), { 'udn':udn, 'name': name } ) )

        # subscribe to changes.
        
        avt = dev.get_service_by_type(self.AVT_namespace)
        if avt:
            avt.event_subscribe(self._controlpoint.event_host,
                                    lambda c,s,t: self._avt_event_subscribe_callback(udn,c,s,t), 
                                    None,
                                    True, 
                                    lambda c,s,t: self._avt_event_renew_callback(udn,c,s,t))
            avt.subscribe_for_variable("LastChange",
                                           lambda n,v: self._avt_event_callback(udn,n,v) )
        
       #     louie.connect(self.render_service_update, 
       #             'Coherence.UPnP.StateVariable.changed', 
       #             client.rendering_control.service )

       # if client.av_transport:
       #     louie.connect(self.transport_service_update, 
       #             'Coherence.UPnP.StateVariable.changed', 
       #             client.av_transport.service )

        #if client.connection_manager:
        #    louie.connect(self.connection_manager_update, 
        #            'Coherence.UPnP.StateVariable.changed', 
        #            client.connection_manager.service )
        
        #self.clear_renderer(udn)
        
        # get transport variables and ensure system knows them..
        #for vname in ("CurrentTrackMetaData", "CurrentTrackDuration", 'TransportState'):
        #    self.transport_service_update(client.av_transport.service.get_state_variable(vname))
        # get renderer variables
        #for vname in ("Volume","Mute"):
        #    self.render_service_update(client.rendering_control.service.get_state_variable(vname))
    
    
    def _avt_event_subscribe_callback(self, udn, cargo, subscription_id, timeout):
        self._log.debug( 'Subscribed to Events of AVT Service on: %s    Subs-ID: %s    Timeout: %s' %(udn, str(subscription_id[5:]), str(timeout)) )
        
    def _avt_event_renew_callback(self, udn, cargo, subscription_id, timeout):
        self._log.debug( 'Renewed Event Subscription for AVT Service on: %s    Subs-ID: %s    Timeout: %s' %(udn, str(subscription_id[5:]), str(timeout)) )
                         
    def _event_unsubscribe_callback(self, cargo, old_subscription_id):
        print
        print "Event unsubscribe done!"
        print 'Old subscription ID: ' + str(old_subscription_id[5:])

    def _avt_event_callback(self, udn, name, value):
        self._log.debug( '%s update for device: %s' %(name,udn) )
        # TODO: Process event 
        
        if name == "LastChange":
            try:  
                last_change = getDictFromXmlString(str(value))
            except:
                print "no valid xml"
            try:
                last_change["Event"]["InstanceID"]["CurrentTrackMetaData"]["val"] = getDictFromXmlString(last_change["Event"]["InstanceID"]["CurrentTrackMetaData"]["val"])
            except:
                print "no valid xml 2"
            #try: 
            #    last_change["Event"]["InstanceID"]["r:NextTrackMetaData"]["val"] = getDictFromXmlString(last_change["Event"]["InstanceID"]["r:NextTrackMetaData"]["val"])
            #except:
            #    print "no valid xml 3"
            try: 
                title = last_change["Event"]["InstanceID"]["CurrentTrackMetaData"]["val"]["DIDL-Lite"]["item"]["dc:title"][""]
            except:
                print "no title"
                title = ""
                
            try: 
                artist = last_change["Event"]["InstanceID"]["CurrentTrackMetaData"]["val"]["DIDL-Lite"]["item"]["dc:creator"][""]
            except:
                print "no artist"
                artist = ""
                
            try: 
                album = last_change["Event"]["InstanceID"]["CurrentTrackMetaData"]["val"]["DIDL-Lite"]["item"]["upnp:album"][""]
            except:
                print "no album"
                album = ""
                
            try: 
                current_track = last_change["Event"]["InstanceID"]["CurrentTrack"]["val"]
            except:
                print "no current track"
                current_track = ""
                
            try: 
                no_of_tracks = last_change["Event"]["InstanceID"]["NumberOfTracks"]["val"]
            except:
                print "no number of tracks"
                no_of_tracks = ""
                
            try: 
                current_track_duration = last_change["Event"]["InstanceID"]["CurrentTrackDuration"]["val"]
            except:
                print "no duration"
                current_track_duration = ""
            try: 
                transport_state = last_change["Event"]["InstanceID"]["TransportState"]["val"]
            except:
                print "no transport state"
                transport_state = ""
            try: 
                current_play_mode = last_change["Event"]["InstanceID"]["CurrentPlayMode"]["val"]
            except:
                print "no playmode"
                current_play_mode = ""
                
            if transport_state == "PLAYING":
                playing = 1
                paused = 0
                stopped = 0
            elif transport_state == "PAUSED_PLAYBACK":
                playing = 0
                paused = 1
                stopped = 0
            elif transport_state == "STOPPED":
                playing = 0
                paused = 0
                stopped = 1
            else:
                print "no valid tarnsport state"
                playing = 0
                paused = 0
                stopped = 0
            
            if current_play_mode == "NORMAL":
                repeat = 0
                shuffle = 0
            elif current_play_mode == "REPEAT_ALL":
                repeat = 1
                shuffle = 0
            elif current_play_mode == "SHUFFLE_NOREPEAT":
                repeat = 0
                shuffle = 1
            elif current_play_mode == "SHUFFLE":
                repeat = 1
                shuffle = 1
            else:
                print "no valid playmode"
                repeat = 0
                shuffle = 0
                
            
                
            self.sendEvent( Event( "http://id.webbrick.co.uk/events/av/transport/state", 
                "av/transport/state/%s" %(udn), 
                { 'udn':udn, 
                  'artist':artist,
                  'album':album, 
                  'title':title, 
                  'albumarturi':"",
                  'CurrentTrack':current_track,
                  'NumberOfTracks':no_of_tracks,
                  'CurrentTrackDuration':current_track_duration,
                  'TransportState':transport_state,
                  'playing':playing,
                  'stopped':stopped,
                  'paused':paused,
                  'shuffle':shuffle,
                  'repeat':repeat,
                 } ) )
        
                           
    def clear_renderer(self, udn ):
        pass

    def render_service_update(self, variable ):
        pass
        
    def send_metadata(self, srvc, udn, mdata, prefix ):
        pass
        
    def transport_service_update(self, variable ):
        pass
       
    def connection_manager_update(self, variable ):
        pass
       
    def new_server(self, client, udn ):
        pass
        
    def remove_server(self, client, udn ):
        pass
        
    def actionSuccess( self, data, action ):
        pass
        
    def actionError( self, failure, action ):
        pass

    def gotError( self, failure ):
        pass

    def noError( self, result ):
        pass
        
    def handleTransportControl( self, inEvent ):      
        pass

    def unMute( self, result, client ):
        pass
       
    def checkIfMuted( self, client, df ):
        pass
       
    def handleRenderControl( self, inEvent ):
        pass

    def handleConnectionControl( self, inEvent ):
        pass

    def newPositionInfo( self, result, udn, srvc ):
        pass
 
    def getTransportPosition( self, inEvent ):
        pass

    
     

