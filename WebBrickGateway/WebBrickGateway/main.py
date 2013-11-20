# $Id: main.py 2923 2008-11-05 13:48:51Z lawrence.klyne $
#

import pkg_resources
pkg_resources.require("TurboGears")

from turbogears import update_config, start_server
from turbogears.startup import SimpleWSGIServer
import cherrypy
import turbogears.config
import cherrypy.config
cherrypy.lowercase_api = True

from os.path import abspath, exists, isabs
import sys
import logging
import socket,errno

# Add application-specific MIME types for static serving
import mimetypes
mimetypes.types_map['.svg']='image/svg+xml'
mimetypes.types_map['.xhtml']='text/html'

#from MiscLib.TwistedLogObserver import TwistedLogObserver
#_tlog = TwistedLogObserver()

# This is so can catch EINTR without hacking cherrypy.
from cherrypy._cpwsgiserver import CherryPyWSGIServer

class myWSGIServer(SimpleWSGIServer):
#class myWSGIServer(CherryPyWSGIServer):
    def tick(self):
        try:
            CherryPyWSGIServer.tick(self)
        except socket.error, x:
            if x[0] == errno.EINTR or x[0] == errno.EAGAIN:
                return
            raise

def start( param = None ):

    # First look on the command line for a desired config file,
    # if it's not on the command line, then
    # look for setup.py in this directory. If it's not there, this script is
    # probably installed
    cfgfil = None
    if param:
        pkg_resources.require("WebBrickLibs")
        pkg_resources.require("WebBrickConfig")
        # windows service seems to get this wrong
        #if isabs(param):
        cfgfil = param
        #else:
        #    cfgfil = abspath(param)
        #print "Config from commandd line %s"%(cfgfil)
    elif exists(abspath("setup.py")):
        cfgfil = abspath("dev.cfg")
        print "Config from dev.cfg (%s)"%(cfgfil)
        #update_config(configfile="dev.cfg", modulename="WebBrickConfig.config")
        # In development environment, add WebBrickLibs to python path
        # (In production, we assume its been installed and added via setup)
        # for develop do "setup.py develop"
        #sys.path.append( "../WebBrickLibs" )
        #sys.path.append( "../WebBrickConfig" )
    else:
        pkg_resources.require("WebBrickLibs")
        pkg_resources.require("WebBrickConfig")
        cfgfil = abspath("prod.cfg")
        print "Config from prod.cfg (%s)"%(cfgfil)
    # first programatically set static_filter.root

    # set default first, handles dev/prod better
    cherrypy.config.configs["global"]["static_filter.root"] = pkg_resources.resource_filename("WebBrickRes", "../resources/static")
    update_config(configfile=cfgfil, modulename="WebBrickGateway.config")
    
    # handle nested configuration files
    if cherrypy.config.configs.has_key("config_files"):
        for k in cherrypy.config.configs["config_files"]:

            cfgfil = cherrypy.config.configs["config_files"][k]
            if exists(cfgfil):
                configdict = turbogears.config.config_obj(cfgfil).dict()
                cherrypy.config.update(configdict)
            else:
                print "No such configuration file %s" %(cfgfil)

    _log = logging.getLogger('WebBrickGateway')
            
    try :
        # Now the path is set up, we can import library stuff we use here
        from MiscLib.Logging  import infoLogDataStructure
        from WebBrickGateway.WbConfigSettings import WbConfigSettings 

        # Add search directory for Kid templates, if specified
        if WbConfigSettings.__dict__.has_key("TemplateDir"):
            WbConfigSettings.addTemplateDir(WbConfigSettings.TemplateDir)

        # Try to flesh out available networks
        #WbConfigSettings.Networks = WbConfigSettings.findNetworks(WbConfigSettings.Networks)

        # Log combined configuration for diagnostics
        if param:
            _log.info( "Configuration Param %s"%(param) )
        if cfgfil:
            _log.info( "Config file %s"%(cfgfil) )
        infoLogDataStructure( _log, cherrypy.config.configs )
        #print cherrypy.config.configs

        # Now start the server
        from WebBrickGateway.controllers import Root

        # TurboGears way:
        # start_server(Root())

        # Our way:
        # This is so all the start up code is not run in copy 1 which has a auto restart.
        cherrypy.root = Root()
        def startGateway(): cherrypy.root.start()
        def stopGateway(): cherrypy.root.stop()
        cherrypy.server.on_start_server_list.append( startGateway )
        cherrypy.server.on_stop_server_list.append( stopGateway )
        cherrypy.server.start(server=myWSGIServer())    # so can catch EINTR on Linux
    except Exception, ex :
        _log = logging.getLogger('WebBrickGateway')
        _log.exception(ex)
        
#   cherrypy.server.start( True )   # init_only
#   _tlog.start()

#   from twisted.internet import reactor
#   reactor.run()

def stop():
    # instruct cherrypy to shutdown clean
    try:
        cherrypy.server.stop()
    except:
        # On win64 the service barfsin trying to log the shutdown. I suspect log files closed early.
        pass
#   _tlog.stop()

# End. $Id: main.py 2923 2008-11-05 13:48:51Z lawrence.klyne $
