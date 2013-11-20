The differences between coherence 0.54 and us.


I have split the root coherence object up.
Tempted to have the device module maintain list of root devices.

.\__init__.py	different (D:\o2m8\coherence_trunk\Coherence-0.5.4\coherence is more recent)
.\base.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)
.\coherence.conf	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence
.\devicelist.py	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence
.\main.py	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence
.\webserver.py	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence

This hooks all coherence logging to python logging, replaces normal module

.\log.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

Have parse_xml exceptions pass up stack. Lose print statements.

.\extern\et.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

Deleted obsolete
.\extern\logger.py	only in D:\o2m8\coherence_trunk\Coherence-0.5.4\coherence
.\extern\log\log.py	only in D:\o2m8\coherence_trunk\Coherence-0.5.4\coherence

Logging fixes.
.\upnp\core\action.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

Handle embedded devices
.\upnp\core\device.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

Add video and music containers, and default to item, container if not known
.\upnp\core\didllite.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

Need work to get closer to baseline, takes a webserver instead of coherence main object.
.\upnp\core\event.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

rename subscribe to known_services.
.\upnp\core\service.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

use logging and not print, try to fix up nero.
.\upnp\core\soap_proxy.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

loose callbacks
.\upnp\core\ssdp.py	different (D:\o2m8\coherence_trunk\Coherence-0.5.4\coherence is more recent)

rework use netiface package
.\upnp\core\utils.py	different (D:\o2m8\coherence_trunk\Coherence-0.5.4\coherence is more recent)

logging tweaks
.\upnp\core\variable.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

rework
.\upnp\devices\control_point.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

hook sonos av client and use of udn
.\upnp\devices\media_renderer_client.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)
use of udn
.\upnp\devices\media_server_client.py	different (D:\o2m8\coherence_trunk\Coherence-0.5.4\coherence is more recent)
use if logging, handle optional actions
.\upnp\services\clients\av_transport_client.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)
handle optional actions
.\upnp\services\clients\connection_manager_client.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)
lose print statements.
.\upnp\services\clients\content_directory_client.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)
minimal
.\upnp\services\clients\rendering_control_client.py	different (D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence is more recent)

These I am adding to extend coherence.
.\upnp\devices\my_control_point.py	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence
.\upnp\devices\sonos_zoneplayer.py	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence
.\upnp\services\clients\base_client.py	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence
.\upnp\services\clients\sonos_av_transport_client.py	only in D:\o2m8\svn\HomeGateway2\Trunk\WebBrickLibs\coherence
