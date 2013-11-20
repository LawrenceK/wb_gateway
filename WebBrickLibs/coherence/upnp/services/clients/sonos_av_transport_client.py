# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

from av_transport_client import AVTransportClient

class SonosAVTransportClient(AVTransportClient):

    # Sonos call
    def add_uri_to_queue(self, instance_id=0, next_uri='', next_uri_metadata='' ):
        action = self.service.get_action('AddURIToQueue')
        self.debug( "add_uri_to_queue %s", action )
        if action:  # optional
            return action.call( InstanceID=instance_id,
                            EnqueuedURI=next_uri,
                            EnqueuedURIMetaData=next_uri_metadata,
                            DesiredFirstTrackNumberEnqueued=0,
                            EnqueueAsNext=0
                            )
        else:
            for action in self.service.get_actions():
                self.debug( "action %s", action )
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG Action: AddURIToQueue
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: InstanceID, in, A_ARG_TYPE_InstanceID
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: EnqueuedURI, in, A_ARG_TYPE_URI
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: EnqueuedURIMetaData, in, A_ARG_TYPE_URIMetaData
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: DesiredFirstTrackNumberEnqueued, in, A_ARG_TYPE_TrackNumber
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: EnqueueAsNext, in, A_ARG_TYPE_EnqueueAsNext
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: FirstTrackNumberEnqueued, out, A_ARG_TYPE_TrackNumber
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: NumTracksAdded, out, A_ARG_TYPE_NumTracks
#2008-04-07 16:15:02,457 coherence.upnp.services.clients.av_transport_client DEBUG       Argument: NewQueueLength, out, A_ARG_TYPE_NumTracks

        return None

    def clear_queue(self, instance_id=0):
        action = self.service.get_action('RemoveAllTracksFromQueue')
        self.debug( "clear_queue %s", action )
        if action:  # optional
            return action.call( InstanceID=instance_id )
        else:
            for action in self.service.get_actions():
                self.debug( "action %s", action )

    def remove_from_queue(self, object_id, instance_id=0):
        # what id do I need
        action = self.service.get_action('RemoveTrackFromQueue')
        self.debug( "remove_from_queue %s, %s", action, object_id )
        if action:  # optional
            return action.call( InstanceID=instance_id,
                            ObjectId=object_id
                            )
        else:
            for action in self.service.get_actions():
                self.debug( "action %s", action )

    def link_to_group(self, coord_id, instance_id=0 ):
        return self._avt.set_av_transport_uri(instance_id, coord_id)

    def unlink_from_group(self, instance_id=0):
        
        action = self.service.get_action('BecomeCoordinatorOfStandaloneGroup')
        self.debug( "unlink_from_group %s", action )
        if action:  # optional
            return action.call( InstanceID=instance_id )
        else:
            for action in self.service.get_actions():
                self.debug( "action %s", action )

        return None
    
