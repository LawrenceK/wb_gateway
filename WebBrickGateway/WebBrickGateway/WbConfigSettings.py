# $Id: WbConfigSettings.py 2610 2008-08-11 20:04:17Z graham.klyne $

"""
WebBrick configuration settings module for WebBrickGateway

This module collects various options and settings that are used
by the WebBrick home gateway.  Initial default values are defined 
as class variables of class 'WbConfigSettings' when this module is 
initially loaded, but may be updated by other modules, e.g. from an 
external configuration file or a master configuration class.
"""

import logging

from WebBrickLibs.WbConfigBase import WbConfigBase

class WbConfigSettings(WbConfigBase):
    """
    This class collects WebBrick configuration settings and options for the
    WebBrick configiration application.
    """

    # Configuration sets directory: relative to python source code, or absolute
    #ConfDir = "resources/wbconf/"

    # Templates directory: relative to python source code, or absolute
    # (must end with "/templates/")
    #TemplateDir = "WebBrickGateway/templates/"

    # Networks available to this system
    #Networks = [ 
    #    # "193.123.216.64/26",    # Temporary for testing on GK system
    #    "10.0.0.0/8",
    #    "169.254.0.0/16",
    #    ]

    # Log all but trace output to console, everything to file
    ###LogConsoleLevel = logging.INFO
    ###LogFile         = "./WebBrickGateway.log"
    # LogFile         = "./log/WebBrickConfig.log"
    # LogFile         = "/Svn/Thirtover/HomeGateway/Trunk/WebBrickConfig/log/WebBrickConfig.log"
    ###LogFileLevel    = logging.DEBUG

# End: $Id: WbConfigSettings.py 2610 2008-08-11 20:04:17Z graham.klyne $
