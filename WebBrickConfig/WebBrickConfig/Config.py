# $Id: Config.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
WebBrick configuration manipulation.
"""

import string
import os
import os.path

from WbConfigSettings import WbConfigSettings
import ConfigSet

from MiscLib.DomHelpers       import parseXmlString, getNamedNode, replaceChildrenText, getElemPrettyXml
from MiscLib.Functions        import formatInt

def listNodes(configsetname):
    """
    Return list of node numbers in stored configuration set
    """
    def isConfig(f):    return len(f) == 2 and f[1] == "xml"
    def nodeNum(f):     return f[0]
    def splitName(f):   return f.split('.', 2)
    cnfset = ConfigSet.configsetPath(configsetname)
    nodes  = map(splitName, os.listdir(cnfset))
    return map(nodeNum, filter(isConfig, nodes))

def configPath(configsetname, node):
    """
    Returns the path name corresponding to a specified configuration.
    """
    if not ConfigSet.exists(configsetname): return None
    return os.path.join(ConfigSet.configsetPath(configsetname), node+".xml")

def exists(configsetname, node):
    """
    Test for the existence of the specified node in the named configuration set.
    Returns None or the path name of the file
    """
    config = configPath(configsetname, node)
    if config and os.path.exists(config): return config
    return None

def create(configsetname, node, cnfxml):
    """
    Create new configuration file with supplied XML content
    Return None if create succeeds, otherwise a string describing the reason 
    for failure.
    """
    node   = formatInt("%03d")(int(node))
    config = configPath(configsetname, node)
    if not config:  
        return ( 
            "Create config: config path name problem (%s, %s) - missing directory or bad name?" % 
            (configsetname, node) )
    if os.path.exists(config):
        return ( 
            "Create config: file already exists (%s, %s)" % 
            (configsetname, node) )
    f = open(config, mode="w")
    f.write(cnfxml)
    f.close()
    return None

def read(configsetname, node):
    """
    Read configuration file, returning its content as an XML string,
    or None if the configuration cannot be read.
    """
    config = configPath(configsetname, node)
    cnfxml = None
    if config and os.path.exists(config):
        f = open(config, mode="r")
        cnfxml = f.read()
        f.close()
    return cnfxml

def write(configsetname, node, cnfxml):
    """
    Write configuration file with content supplied as an XML string.
    Return None for success, or a string containing error information.
    """
    config = configPath(configsetname, node)
    if config and os.path.exists(config):
        return "Output file already exists: "+config
    f = open(config, mode="w")
    f.write(cnfxml)
    f.close()
    return None

def delete(configsetname, node):
    """
    Delete the specified configuration.
    Return None if the delete succeeds, otherwise a string describing 
    the reason for failure.
    """
    config = configPath(configsetname, node)
    if not config:  
        return ( 
            "Delete config: config path name problem (%s/%s) - missing directory or bad name?" % 
            (configsetname, node) )
    if not os.path.exists(config): 
        return ( 
            "Delete config: file does not exist (%s/%s)" % 
            (configsetname, node) )
    os.remove(config)
    return None

def backup(configsetname, node):
    """
    Move specified configuration to a backup copy.
    Return None if the rename succeeds, otherwise a string describing 
    the reason for failure.
    """
    config = configPath(configsetname, node)
    if not config:  
        return ( 
            "Backup config: config path name problem (%s, %s) - missing directory or bad name?" % 
            (configsetname, node) )
    if not os.path.exists(config): 
        return ( 
            "Backup config: file does not exist (%s, %s)" % 
            (configsetname, node) )
    cnfbak = config+".bak"
    if os.path.exists(cnfbak): os.remove(cnfbak)
    os.rename(config, cnfbak)
    return None

def copy(configsetname, node, tgtconfigsetname, tgtnode):
    """
    Copy specified configuration, updating the node number containmed in its body    
    """
    cnfxml = read(configsetname, node)
    if node == tgtnode:
        newxml = cnfxml
    else:
        cnfdom = parseXmlString(cnfxml)
        wbroot = cnfdom.documentElement
        wbsn   = getNamedNode(wbroot, "SN")
        if not wbsn:
            return "Config file has no <SN> element (node number)"
        replaceChildrenText(wbsn, tgtnode)
        newxml = getElemPrettyXml(cnfdom)
        # newxml = cnfdom.toprettyxml(indent="  ",newl="\n")
    return write(tgtconfigsetname, tgtnode, newxml)

def move(configsetname, node, tgtconfigsetname, tgtnode):
    """
    Move specified configuration, updating the node number contained in its body    
    """
    err = copy(configsetname, node, tgtconfigsetname, tgtnode)
    if err: return err
    err = delete(configsetname, node)
    return err

# End: $Id: Config.py 2612 2008-08-11 20:08:49Z graham.klyne $
