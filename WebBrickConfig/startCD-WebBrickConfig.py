# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#
#!/usr/bin/env python
#
# $Id: startCD-WebBrickConfig.py 2761 2008-09-19 14:28:53Z graham.klyne $
#

# Use version 2, not version 3 of CherryPy
import sys
import glob
from os.path import *
cpfile = glob.glob(sys.prefix+"\\Lib\\site-packages\\cherrypy-2.*")
sys.path.insert(1, cpfile[0])

# Now can import TurboGears, etc.
import pkg_resources
pkg_resources.require("TurboGears")

from turbogears import update_config, start_server, config
import cherrypy
cherrypy.lowercase_api = True
from os import getcwd
from os.path import join, dirname, exists
import sys
import logging

# Add application-specific MIME types for static serving
import mimetypes
mimetypes.types_map['.svg']   = 'image/svg+xml'
mimetypes.types_map['.xhtml'] = 'text/html'

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print "Usage: %s DIR"%(sys.argv[0])
        print ""
        print "where:"
        print "  DIR is the directory where webbrick configuration files are stored."
        print "      Create this directory with at least one empty subdirectory before"
        print "      running this program."
        print ""
        print "cwd = %s"%(getcwd())
        print ""
        sys.exit(1)

    cfgfil = join(getcwd(), "runCD.cfg")
    print "Config from runCD.cfg (%s)"%(cfgfil)
    sys.path.append( "../WebBrickLibs" )
    update_config(configfile=cfgfil, modulename="WebBrickConfig.config")

    # Set console logging details
    #
    # This is really naff -- both loggers and handlers have logging levels,
    # and both must be satisfied in order for a record to be logged.  So the
    # logging level of the logger (set by basicConfig) must the the lowest
    # of all the handlers that are invoked.  If a log level is not set in
    # basicConfig, then the root level defaults to WARNING.
    #
    # So use "basicConfig" to configure the most voluminous logging level,
    # and add handlers to deal with reduced logging levels.

    if config.get('server.environment') == "development":
        logfilemode = 'w'
    else:
        logfilemode = 'a'

    from WebBrickConfig.WbConfigSettings import WbConfigSettings

    logfile = config.get('server.log_file')
    if logfile != None:
        WbConfigSettings.__dict__["LogFile"] = logfile

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        dateftm="%H:%M:%S")

    import MiscLib.Logging as Logging
    Logging.Info(
        "Logging initialized (%s,%s,%i;%s)" % 
          (WbConfigSettings.LogFile,logfilemode,WbConfigSettings.LogFileLevel,config.get('server.environment')),
        __name__)

    # Add search directory for Kid templates, if specified
    if WbConfigSettings.__dict__.has_key("TemplateDir"):
        WbConfigSettings.addTemplateDir(WbConfigSettings.TemplateDir)

    # Try to flesh out available networks
    WbConfigSettings.Networks = WbConfigSettings.findNetworks(WbConfigSettings.Networks)

    # Set location for webbrick configuration files
    # TODO: pick up value from command line?
    WbConfigSettings.ConfDir = "E:/TEMP/wbconf/"
    if len(sys.argv) > 1:
        WbConfigSettings.ConfDir = join(getcwd(), sys.argv[1])

    from WebBrickConfig.controllers import Root

    # This is so all the start up code is not run in copy 1 which has a auto restart.
    cherrypy.root = Root()
    def startWbCnf(): cherrypy.root.start()
    def stopWbCnf(): cherrypy.root.stop()
    cherrypy.server.on_start_server_list.append( startWbCnf )
    cherrypy.server.on_stop_server_list.append( stopWbCnf )
    cherrypy.server.start()

# End.