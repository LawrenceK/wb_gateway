# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: WbConfigBase.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
Base class for application configuration settings module.

An application configuration module collects various options and settings 
that are used by WebBrick application server code.  Configuration items are
defined as class variables of a subclass, assigned initial default values 
when the class is loaded, but may be updated by other modules, e.g. from 
an external configuration file or a master configuration class.

This base class module contains helper methods that may be used when setting
application configuration and environment values.
"""

import logging
import sys

from MiscLib.NetUtils import getHostIpsAndMask

_log = logging.getLogger("WebBrickLibs.WbConfigBase")

class WbConfigException(Exception):
    """
    Exception value for reporting configuration problems.
    """

    def __init__(self, cfgopt=None, cfgval=None, cfgerr=None):
        """
        Initialize a configuration exception
        cfgopt is the name of description of the configuration option, if known
        cfgval is the value given for the configuration option, if known
        cfgerr is a description of the configuration error
        """
        self.cfgopt = cfgopt
        self.cfgval = cfgval
        self.cfgerr = cfgerr
        return

    def __str__(self):
        s = "Configuration error"
        if self.cfgopt: s += " for %s"%(self.cfgopt)
        if self.cfgval: s += ": value '%s': "%(self.cfgval)
        if self.cfgerr:
            s += self.cfgerr
        else:
            s += "(unspecified error)"
        return s


class WbConfigBase:
    """
    This class contains helper methods that may be used when setting
    application configuration and environment values.
    
    It also contains some general default values that may be used by 
    application configuratyion code.
    """

    # Templates directory: relative to python source code, or absolute
    # (must end with "/templates/")
    TemplateDir = "./templates/"

    # Configuration sets directory: relative to python source code, or absolute
    ConfDir = "resources/wbconf/"

    # Default networks available (class A and class B non-routed)
    Networks = [ 
        "10.0.0.0/8",
        "169.254.0.0/16",
        ]

    # Default log all but trace output to console, everything to file
    ###LogConsoleLevel = logging.INFO
    ###LogFileLevel    = logging.DEBUG

    # Method to attempt discovery of connected networks.
    # Accepts initial list of networks, and returns a possibly augmented list.
    # Networks are represented as a string like this "10.0.0.0/8".
    @staticmethod
    def findNetworks(nets):
        for ip in getHostIpsAndMask():
            _log.debug( "findNetworks %s " % ip )
            if not ip in nets: 
                _log.debug( "added %s " % ip )
                nets.append(ip)
        return nets

    # Method to add a network to the list of connected networks.
    # Networks are represented as a string like this "10.0.0.0/8".
    @staticmethod
    def addNetwork(ip):
        _log.debug( "addNetwork %s " % ip )
        if not ip in WbConfigBase.Networks: 
            _log.debug( "added %s " % ip )
            WbConfigBase.Networks.append(ip)

    # Method to extend search path for python modules
    # (Turbogears/CherryPy may also require to be notified of this change).
    @staticmethod
    def addPythonPath(newpath):
        if newpath not in sys.path:
            sys.path.append(newpath)
        return

    # Method to add an additional directory in which to look for TurboGears 
    # template files, assuming that they are referenced as "templates.<templatename>"
    # in @turbogears.expose(...) web page function decorators.
    #
    # This means that the final segment of the template directory path 
    # must be "templates/".
    @staticmethod
    def addTemplateDir(tempdir):
        tempsuf = "/templates/"
        if not tempdir.endswith(tempsuf):
            err = WbConfigException(
                cfgopt="Template directory", cfgval=tempdir, 
                cfgerr="directory must end with '%s'"%tempsuf) 
            WbConfigBase.configError(err)
        else:
            # As far as I can tell, Kid is designed to use the python import mechanism, 
            # hence python path, for locating templates.
            # The only documented alternative I can find is to explicitly create a 
            # Kid Template object with a specified file name.
            # Hence I prefer to not depend on changing Kid's internal structures.
            tempdir = tempdir[:-(len(tempsuf)-1)]
            if tempdir not in sys.path:
                sys.path.append(tempdir)
        # Another version:
        #if False:
        #    import kid
        #    ### tempdir = tempdir[:-(len(tempsuf)-1)]
        #    kid.path.insert(tempdir)
        return

    # Function called when a configuration error is detected
    @staticmethod
    def configError(err):
        _log.warning(str(err))
        raise err

    #TODO: utility methods for checking configuration parameters; e.g.
    #   fileExists
    #   fileIsWritable
    #   dirIsWritable
    #   matchRegex
    #   (etc...)
    #
    # (cf. telephone discussion with Lawrence, 7-Nov-2006)

# Flesh out networks on class load.
WbConfigBase.Networks = WbConfigBase.findNetworks(WbConfigBase.Networks)

# End: $Id: WbConfigBase.py 2612 2008-08-11 20:08:49Z graham.klyne $
