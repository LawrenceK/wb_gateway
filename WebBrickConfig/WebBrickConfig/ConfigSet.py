# $Id: ConfigSet.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
WebBrick configuration set manipulation
"""

import string
import os
import os.path

from WbConfigSettings import WbConfigSettings
# import WbConfigSettings

def validName(configsetname):
    """
    Tests if the supplied name is valid for a configuration set name
    """
    for c in configsetname:
        if not c in string.letters+string.digits+"$_-":
            return False
    return configsetname != ""

def listNames():
    def isConfigSet(f):
        # Names not containing '.':
        return f.find('.') < 0
    names = os.listdir(WbConfigSettings.ConfDir)
    return filter(isConfigSet, names)

def configsetPath(configsetname):
    """
    Returns the path name corresponding to a supplied configuration set name.
    """
    cnfdir = WbConfigSettings.ConfDir
    return os.path.normpath(os.path.join(cnfdir, configsetname))

def exists(configsetname):
    """
    Test for the existence of the names configuration set.
    """
    cnfset = configsetPath(configsetname)
    return os.path.exists(cnfset) and os.path.isdir(cnfset)

def create(configsetname):
    """
    Create a new configuration set with the supplied name.
    """
    cnfset = configsetPath(configsetname)
    os.mkdir(cnfset)
    return None

def delete(configsetname):
    """
    Delete the named configuration set.
    """
    cnfset = configsetPath(configsetname)
    files  = os.listdir(cnfset)
    for f in files: os.remove(os.path.join(cnfset, f))
    os.rmdir(cnfset)
    return None

# End: $Id: ConfigSet.py 2612 2008-08-11 20:08:49Z graham.klyne $
