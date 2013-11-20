# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: DumpCommands.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# I'm not sure what this is, but it appears to be a quick-and-dirty utility to dump 
# out Webbrick commands for a configuration file named on the command line, with
# no provision for specifying an initial dictionary of default values.
# -- #g
#

import sys

sys.path.append("..")
sys.path.append("../../../../WebBrickLibs/src/main/python")

from DomHelpers import parseXmlFile
from WebBrickConfig import WebBrickConfig

if __name__ == "__main__":
    cfg = WebBrickConfig()
    for cmd in cfg.makeConfigCommands( parseXmlFile( sys.argv[1] ), dict() ):
        print cmd
