# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

from twisted.internet import task, defer
from twisted.internet import reactor

import coherence.extern.louie as louie

from coherence import __version__

from coherence.upnp.core.ssdp import SSDPServer
from coherence.upnp.core.msearch import MSearch

from coherence.upnp.devices.control_point import ControlPoint
from coherence.upnp.devices.my_control_point import MyControlPoint
from coherence.WebServer import WebServer
from coherence.DeviceList import DeviceList

from coherence import log

global single_coherence
single_coherence = None

# to make sure a single coherence object in the application.
# but allow multiple configurations.
# in case called without configuration in one case.
def Coherence(config=None):
    global single_coherence
    if not single_coherence:
        single_coherence = CoherenceObject(config)

    if config:
        single_coherence.configure(config)
        if config.get('start', 'no') == 'yes':
	    single_coherence.start()

    return single_coherence

class Plugins(log.Loggable):
    logCategory = 'plugins'
    _instance_ = None  # Singleton

    _valids = ("coherence.plugins.backend.media_server",
               "coherence.plugins.backend.media_renderer",
               "coherence.plugins.backend.binary_light",
               "coherence.plugins.backend.dimmable_light")

    _plugins = {}

    def __new__(cls, *args, **kwargs):
        obj = getattr(cls, '_instance_', None)
        if obj is not None:
            return obj
        else:
            obj = super(Plugins, cls).__new__(cls, *args, **kwargs)
            cls._instance_ = obj
            obj._collect(*args, **kwargs)
            return obj

    def __repr__(self):
        return str(self._plugins)

    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, key):
        return self._plugins.__getitem__(key)

    def get(self, key,default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        self._plugins.__setitem__(key,value)

    def set(self, key,value):
        return self.__getitem__(key,value)

    def keys(self):
        return self._plugins.keys()

    def _collect(self, ids=_valids):
        if not isinstance(ids, (list,tuple)):
            ids = (ids)
        try:
            import pkg_resources
            for id in ids:
                for entrypoint in pkg_resources.iter_entry_points(id):
                    try:
                        self._plugins[entrypoint.name] = entrypoint.load()
                    except ImportError, msg:
                        self.warning("Can't load plugin %s (%s), maybe missing dependencies..." % (entrypoint.name,msg))
                        self.info(traceback.format_exc())
        except ImportError:
            self.info("plugin reception activated, no pkg_resources")
            from coherence.extern.simple_plugin import Reception
            reception = Reception(os.path.join(os.path.dirname(__file__),'backends'), log=self.warning)
            self.info(reception.guestlist())
            for cls in reception.guestlist():
                self._plugins[cls.__name__.split('.')[-1]] = cls
        except Exception, msg:
            self.warning(msg)

class CoherenceObject(log.Loggable):

    def __init__(self, config={}):
        self.info("Create CoherenceObject")
        self._deviceList = DeviceList()

        plugin = louie.TwistedDispatchPlugin()
        louie.install_plugin(plugin)

        self.available_plugins = None
        self.installed_plugins = None
        self.web_server = None
        self.ctrl = None

    def clear(self):
        """ we do need this to survive multiple calls
            to Coherence during trial tests
        """
        global single_coherence
        single_coherence = None

    def get_devices(self):
        return self._deviceList._devices.values()

    def get_device_with_id(self, device_id):
        return self._deviceList.get_device_with_id(device_id)

    def configure(self, config):
        self.info("Configure CoherenceObject %s", config)

        if not self.web_server and config.has_key("webserver"):
            self.web_server = WebServer( config["webserver"], self._deviceList)

        plugins = config.get('plugins',None)
        if plugins:
            self.info("Configure plugins %s", plugins)
            for plugin,arguments in plugins.items():
                self.info("Configure plugin %s %s", plugin, arguments )
                try:
                    if not isinstance(arguments, dict):
                        arguments = {}
                    # ensure keye are strings and not unicode strings. Grrr
                    for k in arguments:
                        d = arguments[k]
                        del arguments[k]
                        arguments[str(k)] = d
                    #arguments = {'medialocation': u'C:\\Music', 'mediadb': u'C:\\Music\\MediaStore.db', 'name': u'Coherence MediaStore'}
                    self.info("Configure plugin %s %s", plugin, arguments )
                    self.add_plugin(plugin, **arguments)
                except Exception, msg:
                    self.exception("Can't enable plugin, %s: %s!" % (plugin, msg))

        if self.ctrl is None and config.get('controlpoint', 'no') == 'yes':
            self.ctrl = MyControlPoint(config, self.web_server, self._deviceList)

    def start(self):
        self.warning("Coherence UPnP framework version %s starting..." % __version__)
        self.ssdp_server = SSDPServer()
        self.msearch = MSearch(self.ssdp_server)

    def stop(self):
        pass

    def add_plugin(self, plugin, **kwargs):
        self.info("adding plugin %s", plugin)
        self.available_plugins = Plugins()

        def get_installed_plugins(ids):
            if self.installed_plugins is None:
                self.installed_plugins = {}
                import pkg_resources
                if not isinstance(ids, (list,tuple)):
                    ids = (ids)
                for id in ids:
                    for entrypoint in pkg_resources.iter_entry_points(id):
                        try:
                            self.installed_plugins[entrypoint.name] = entrypoint.load()
                        except ImportError, msg:
                            self.exception("Can't load plugin %s (%s), maybe missing dependencies..." % (entrypoint.name,msg))

        get_installed_plugins(("coherence.plugins.backend.media_server",
                               "coherence.plugins.backend.media_renderer"))
        try:
            plugin_class = self.installed_plugins.get(plugin,None)
            if plugin_class == None:
                raise KeyError
            for device in plugin_class.implements:
                try:
                    device_class=globals().get(device,None)
                    if device_class == None:
                        raise KeyError
                    self.critical("Activating %s plugin as %s..." % (plugin, device))
                    device_class(self, plugin_class, **kwargs)
                except KeyError:
                    self.critical("Can't enable %s plugin, sub-system %s not found!" % (plugin, device))
                except Exception, msg:
                    self.exception("Can't enable %s plugin for sub-system %s, %s!" % (plugin, device, msg))
        except KeyError:
            self.critical("Can't enable %s plugin, not found!" % plugin)
        except Exception, msg:
            self.exception("Can't enable %s plugin, %s!" % (plugin, msg))
