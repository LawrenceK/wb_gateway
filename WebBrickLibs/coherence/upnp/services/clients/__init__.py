
from coherence.upnp.services.clients.connection_manager_client import ConnectionManagerClient
from coherence.upnp.services.clients.caching_content_directory_client import CachingContentDirectoryClient
from coherence.upnp.services.clients.content_directory_client import ContentDirectoryClient
from coherence.upnp.services.clients.av_transport_client import AVTransportClient
from coherence.upnp.services.clients.rendering_control_client import RenderingControlClient
from coherence.upnp.services.clients.sonos_av_transport_client import SonosAVTransportClient

def get_service_client(service):
    # passed off so we can override in derived classes.
    if service.get_type() in ["urn:schemas-upnp-org:service:ContentDirectory:1",
                              "urn:schemas-upnp-org:service:ContentDirectory:2"]:
        if service.device and service.device.model_name.find( 'ZonePlayer') >= 0:
            return CachingContentDirectoryClient( service)
        else:
            return ContentDirectoryClient( service)

    if service.get_type() in ["urn:schemas-upnp-org:service:ConnectionManager:1",
                              "urn:schemas-upnp-org:service:ConnectionManager:2"]:
        return ConnectionManagerClient( service)

    if service.get_type() in ["urn:schemas-upnp-org:service:RenderingControl:1",
                              "urn:schemas-upnp-org:service:RenderingControl:2"]:
        return RenderingControlClient( service)

    if service.get_type() in ["urn:schemas-upnp-org:service:ConnectionManager:1",
                              "urn:schemas-upnp-org:service:ConnectionManager:2"]:
        return ConnectionManagerClient( service)

    if service.get_type() in ["urn:schemas-upnp-org:service:AVTransport:1",
                              "urn:schemas-upnp-org:service:AVTransport:2"]:
        if service.device and service.device.model_name.find( 'ZonePlayer') >= 0:
            return SonosAVTransportClient( service)
        else:
            return AVTransportClient( service)

    return BaseClient( service)
