# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#!/usr/bin/python
#!/usr/bin/python
# $Id: webbrick_util.py 3497 2010-02-01 13:55:26Z philipp.schuster $
# 
#  webbrick Utility
#
#--------+---------+---------+---------+---------+---------+---------+---------+
#
# Within this code all paths are specified in unix format and the platform will handle the changes.
# note the installer escapes back slashes! so we get \\ on the command line.

"""
A command line utility for miscellaneous operations.
"""

import sys
import logging
import pkg_resources

from os import getcwd, walk, mkdir, makedirs, environ
from os.path import join, split, abspath, exists
from shutil import copyfile

from configobj import ConfigObj
from optparse import OptionParser

# TODO make sure this gets to be python
# Breaks at times.
#sourceLocation = split(__file__)[0]

# the set of files and directories that make up a complate site
# these are all copied to the target directory
commonFiles = ['readme.txt']
# tuples for source and target directories, the later relative to target directory
#siteDirs = [ ('./samples1','./') ]


_log = None

# ------- --------- --------- --------- --------- ---------
# Main program driver
# ------- --------- --------- --------- --------- ---------

def main():
    """
    main program: parse command arguments and dispatch selected action(s).
    """
    # Parse command line
    parser = OptionParser(usage="%prog [options]",
                          version="%prog V0.1")
    parser.add_option("-n", "--new", 
                      action="store_true", dest="new", default=False,
                      help="Create a new Gateway configuration set in the current directory, includes a base set of templates.")
    parser.add_option("-k", "--key", 
                      action="store_true", dest="key", default=False,
                      help="Create a user key request file.")
    parser.add_option("-c", "--create", 
                      action="store_true", dest="create", default=False,
                      help="Create a new set of user interface templates.")
    parser.add_option("-d", "--directory", 
                      dest="directory", default="./",
                      help="Directory to create new site setup in")
    parser.add_option("-s", "--sample", 
                      dest="samplename", default="./sampleSite",
                      help="Directory to create new site setup in")
                      
#    parser.add_option("-s", "--service", 
#                      action="store", dest="service_cfg", default="",
#                      help="Set the webbrick gateway service to use an alternate configuration file.")
#    parser.add_option("-a", "--serviceauto", 
#                      action="store_true", dest="service_auto", default=False,
#                      help="Setup the webbrick gateway service to auto start.")
                      
    parser.add_option("-v", "--verbose", 
                      action="store_true", dest="verbose", default=False,
                      help="enable verbose level logging.")
    parser.add_option("--vv", "--very-verbose", 
                      action="store_true", dest="debug", default=False,
                      help="enable debug level logging.")
    (options, args) = parser.parse_args(sys.argv[1:])


    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    global _log
    _log = logging.getLogger( "WebBrickGateway.util" )

    sourceLocation = pkg_resources.resource_filename("WebBrickGateway", "../resources")
    sourceLocation = sourceLocation.replace("\\","/")
    sourceLocation = sourceLocation.replace("//","/")
    sourceLocation = abspath( sourceLocation )
    _log.debug( "sourceLocation %s" % (sourceLocation) )

    targetDir = options.directory.replace("\\","/")
    targetDir = targetDir.replace("//","/")
    targetDir = abspath( targetDir )
    _log.debug( "targetDir %s" % (targetDir) )
    
    _log.debug( "options %s" % options )

    # Now perform the required actions
    if options.new:
        # double back slash to single forward
        _log.warning( "Create new site in %s", targetDir )
        NewConfig(sourceLocation, targetDir, options.samplename)
    elif options.create:
        _log.warning( "Create new template set in %s", targetDir )
        CopyTemplates( targetDir )
    elif options.key:
        _log.warning( "Create key request" )
        CreateKeyRequest(sourceLocation)
    elif options.service_cfg:
        _log.warning( "Configure service/daemon" )
        pass
        # set gateway config file
    elif options.service_auto:
        _log.warning( "Configure service/daemon auto start" )
        SetAutoStart()
        # set gateway service startup
    else:
        # no command
        parser.print_help()


# ------- --------- --------- --------- --------- ---------
# Copy default template files from the egg install location
# to a new directory for editing.
# ------- --------- --------- --------- --------- ---------

def CopyTemplates( newLoc ):
    """
    
    """
    _log.debug( "Templates exported %s\n" % newLoc )
    _log.error( "Not Implemented" )

def CopyDirectory( sourceDir, targetDir ):
    """
    Copy a set of files from one directory to another, create target if needed.
    """
    if not exists( targetDir):
        mkdir(targetDir)

    sourceDirLen = len(sourceDir)

    for root, dirs, files in walk(sourceDir):
        _log.debug( "walk: %s dirs %s files %s" % (root, dirs, files) )

        tgtRoot = join(targetDir, root[sourceDirLen+1:])  # we loose the original path to get the relative path
        _log.debug( "From: '%s' To: '%s'" % (root,tgtRoot) )

        # Create target directory?
        if not exists( tgtRoot):
            mkdir(tgtRoot)

        for name in files:
            fromName = abspath(join(root, name))
            toName = abspath(join( tgtRoot,name))
            if name[0] != '.' :
                if not exists( toName ):
                    _log.debug( "Copy: %s To: %s" % (fromName,toName) )
                    copyfile( fromName, toName )
                else:
                    _log.info( "Skipped: %s already exists" % (fromName) )
            else:
                _log.debug( "Skip: %s" % (fromName) )

        i = len(dirs)-1
        while i >= 0:
            _log.debug( "directory name %s (%i)" % (dirs[i], i) )
            if ( dirs[i][0] == '.' ):
                # remove as not to be copied.
                _log.debug( "directory name removed %s " % (dirs[i]) )
                del dirs[i]
            i = i - 1

def NewConfig( sourceLocation, targetLocation, samplename ):
    """
    Copy a complete set of sample files to a new directory, location.regedit

    """

    # Copy prof.cfg file
    # Copy templates & subs
    # Copy EventDespatch & subs
    # Copy MediaAccess.xml
    # Copy Readme.txt
    # Update .cfg file

    # Allow for multiple sample sets.
    sourcePath = abspath( join(sourceLocation,samplename) )
    _log.info( "Samples exporting from %s to %s\n" % ( sourcePath, targetLocation ) )
    if not exists(targetLocation):
        makedirs(targetLocation)

    CopyDirectory( abspath( join(sourceLocation, samplename) ), targetLocation )

    for fil in commonFiles:
        fromName = abspath( join(sourceLocation, fil ) )
        toName = abspath( join( targetLocation, fil ) )
        if not exists( toName ):
            _log.debug( "Copy: %s To: %s" % (fromName, toName) )
            copyfile( fromName, toName )
        else:
            _log.info( "Skipped: %s already exists" % (fromName) )

    # locate prod.cfg file and update userRootDirectory
    _log.info( "Update cfg file %s\n" % (targetLocation) )
    cfg = ConfigObj( join(targetLocation, "prod.cfg"), {'list_values':True, 'interpolation': False, 'unrepr': True} )
    # This needs to be unix formatted as configobj blows wobbler
    # and a quoted string.
    cfg['DEFAULT']['siteUserRootDirectory'] = targetLocation.replace( "\\", "/" )
    cfg.write()

    _log.info( "Samples exported %s\n" % (targetLocation) )

def SetAutoStart( newLoc ):
    """
    Set the Gateway to autostart on system boot and update the configuration file location.
    """
    _log.error( "Not Implemented" )
    if sys.platform == "win32":
        # need to add a service
        pass
    elif sys.platform == "linux2" or  sys.platform == "linux":
        # need to identify version of linux so as to locate init script location.
        pass

def CreateKeyPair( fileLoc ):
    # create a user key pair
    # self sign public key.

    COMPANY = "WebBrickSystems"
    PRODUCT = "WebBrick Gateway"
    INSTALLLOCKEY = "InstallLoc"
    pass

def InstallDir():
    # return directory path for app install.
    if sys.platform == "win32":
        # access registry
        import _winreg as wreg
        regPath = "Software\\%s\\%s" % (COMPANY,PRODUCT)
        regKey = None
        try:
            regKey = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, regPath)
        except:
            # no such key.
            regKey = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, regPath)
            iloc = join( environ["ProgramFiles"], COMPANY , PRODUCT )
            wreg.SetValue(regKey, INSTALLLOCKEY, wreg.REG_SZ, iloc )
        return wreg.QueryValue(regKey, INSTALLLOCKEY)

    elif sys.platform == "linux2" or  sys.platform == "linux":
        _log.error( "Not Implemented" )
        # look to see where we were installed.
        return "/opt/webbrick"
    return ""   # unknown platform

USER_DETAILS = ""
def CreateKeyRequest(sourceLocation):
    _log.error( "Not Implemented" )
    # copy template userdetails
    sourcePath = abspath( sourceLocation )
    destPath = InstallDir()
    fromName = join( sourcePath, USER_DETAILS )
    toName = join( destPath, USER_DETAILS )

    _log.debug( "Copy: %s To: %s" % (fromName,toName) )
    copyfile( fromName, toName )

    # update platform details

    # create user key

    # package
    # encrypt using webbricksystems key.

def HandleKeyResponse():
    # extract user countersigned signed key
    # verify user key
    # verify user enable data
    pass

# ------- --------- --------- --------- --------- ---------
# Invoke main program
# ------- --------- --------- --------- --------- ---------

if __name__ == "__main__":
    main()
