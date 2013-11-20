# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: WbCfg.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
#  WebBrick configuration utility.
#
#--------+---------+---------+---------+---------+---------+---------+---------+
#

"""
A command line utility for reading and writing Webbrick configurations.

Configurations are read as XML using a single HTTP GET operation directed 
to a WebBrick.

Configurations are written using a series of configuration commands, each
of which is submitted to a Webbrick by an HTTP operation.
"""

import sys
from optparse import OptionParser

# Do I really want to do this here?  
# Require PYTHONPATH to be set up appropriately instead?
# Note: doing this here should apply for the whole program:
# no need to do it in other modules.
sys.path.append("../../../../WebBrickLibs/src/main/python")

import WebBrickConfig
from WbAccess   import SendHTTPCmd, GetHTTPLines
from DomHelpers import parseXmlFile
from Logging    import Trace

# ------- --------- --------- --------- --------- ---------
# Main program driver
# ------- --------- --------- --------- --------- ---------

def WbCfg(sysargs):
    """
    WbCfg main program: parse command arguments and dispatch selected action(s).
    """
    # Parse command line
    parser = OptionParser(usage="%prog [options] <WbAdrs>",
                          version="%prog V0.1")
    parser.add_option("-d", "--display", 
                      action="store_true", dest="display", default=False,
                      help="Display WebBrick configuration (default)")
    parser.add_option("-s", "--save-config", 
                      action="store", type="string", dest="savefile",
                      help="Get current WebBrick configuration to specified file")
    parser.add_option("-u", "--update-config", 
                      action="store", type="string", dest="updatefile",
                      help="Update WebBrick configuration from details in specified file")
    parser.add_option("-p", "--password", 
                      action="store", type="string", dest="password", default="password",
                      help="Password for WebBrick configuration access (default: 'password')")
    parser.add_option("-t", "--trace",
                      action="store_true", dest="trace", default=False)
    (options, args) = parser.parse_args(sysargs)
    if len(args) != 1:
        parser.error("Incorrect number of arguments")
    # Now perform the required actions
    global traceflag
    traceflag = options.trace
    default  = True
    override = { "password" : options.password }
    if options.savefile:
        TraceVals("Save %s config to %s", args[0], options.savefile)
        SaveConfig(args[0], options.savefile )
        default = False
    if options.updatefile:
        TraceVals("Update %s config from %s", args[0], options.updatefile)
        UpdateConfig(args[0], options.updatefile, override)
        default = False
    if default or options.display:
        TraceVals("Display %s config", args[0], options.savefile)
        DisplayConfig(args[0])
    TraceVals("Finished")

# ------- --------- --------- --------- --------- ---------
# Update WebBrick configuration from supplied file
# ------- --------- --------- --------- --------- ---------

def UpdateConfig(adrs, filename, override):
    """
    Update configuration of specified WebBrick from specified file.
    """
    wbcfg = WebBrickConfig.WebBrickConfig()
    try:
        dom = parseXmlFile(filename)
    except IOError:
        print("Cannot read file %s" % filename)
        return None
    configcmds = wbcfg.makeConfigCommands(dom,override)
    for line in configcmds:
        if (line[0] != '#') :
            sys.stdout.write(".")
            SendHTTPCmd(adrs,line)
    print "\nWebbrick config updated\n"

# ------- --------- --------- --------- --------- ---------
# Save WebBrick configuration to supplied file
# ------- --------- --------- --------- --------- ---------

def SaveConfig(adrs, filename):
    """
    Save configuration of specified WebBrick to a specified file.
    """
    WriteConfig(adrs,filename=filename)
    print "Webbrick config saved\n"

# ------- --------- --------- --------- --------- ---------
# Display WebBrick configuration to stdout
# ------- --------- --------- --------- --------- ---------

def DisplayConfig(adrs):
    """
    Display configuration of specified WebBrick to stdout.
    """
    WriteConfig(adrs)

# ------- --------- --------- --------- --------- ---------
# Helper for Display and save config
# ------- --------- --------- --------- --------- ---------

def WriteConfig(adrs,filename=None,stream=sys.stdout):
    """
    Write configuration of specified WebBrick to named file or supplied stream.
    """
    config = GetHTTPLines(adrs,"/wbcfg.xml")
    if config:
        if filename:
            try:
                stream = open(filename,"w")
            except IOError:
                print("Cannot write file %s" % filename)
                return None
        stream.writelines(config)
        ##for line in config:
        ##    f.write(line)
        if filename:
            stream.close()
    return config

# ------- --------- --------- --------- --------- ---------
# Trace output helper
# ------- --------- --------- --------- --------- ---------

def TraceVals(msg,*args):
    if traceflag:
        Trace("WbCfg",msg % args)

# ------- --------- --------- --------- --------- ---------
# Invoke main program
# ------- --------- --------- --------- --------- ---------

if __name__ == "__main__":
    WbCfg(sys.argv[1:])
