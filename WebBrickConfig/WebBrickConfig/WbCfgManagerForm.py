# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: WbCfgManagerForm.py 3138 2009-04-15 10:17:29Z philipp.schuster $

"""
Module to handle requests for WebBrick configuration resources
"""

import re
import sys
import time
import zipfile
import StringIO

import turbogears
import cherrypy

from WebBrickConfig   import WebBrickConfig
from WbConfigSettings import WbConfigSettings
from Discovery        import WbDiscoverFull, WbDiscoverCheck
import ConfigSet
import Config

from WebBrickLibs.WbAccess   import SendHTTPCmd, GetHTTPLines, WbAccessException
from WebBrickLibs.Wb6Config  import Wb6Config
from WebBrickLibs.Wb6Status  import Wb6Status, ERR_NotLoggedIn
from WebBrickLibs.WbUdpCommands    import sendUdpCommand

from MiscLib.DomHelpers import parseXmlString, escapeText, escapeTextForHtml
from MiscLib.NetUtils   import parseIpAdrs, parseNetAdrs, formatIpAdrs, \
                               mkBroadcastAddress, parseMacAdrs, getHostIpsAndMask
from MiscLib.Functions  import formatIntList, formatInt
from MiscLib.Logging    import Trace, Info, Warn, Error

# --------------------------------------------------
# WebBrick command invocation class
# --------------------------------------------------

class WbCfgManagerForm(object):
    """
    Class to handle requests for WebBrick configuration management resources
    """

    def __init__(self, discover):
        self._discover = discover

    # Constants
    # ---------
    FrontPage = "/wbcnf/ConfigManager"

    # URI dispatching
    # ---------------

    @turbogears.expose()
    def index(self, *args):
        """
        Index page for configuration resources
        """
        requri = cherrypy.request.browserUrl
        raise cherrypy.HTTPRedirect(turbogears.url(self.FrontPage))
        ### raise cherrypy.HTTPError(404, "Unrecognized index URI: "+requri )
        return ""

    @turbogears.expose()
    def default(self, *args):
        """
        Analyze request URI and invoke the corresponding configuration resource
        """
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        requri  = cherrypy.request.browserUrl
        Trace("%s: %s"%(requri,str(args)), "WbCfgManagerForm.default")
        if len(args) > 0:
            # Configuration manager front page
            if args[0] == "ConfigManager": return self.ConfigFrontPage()

            # Information request callbacks
            if args[0] == "Networks": return self.wbNetworks()
            if args[0] == "Discover": return self.wbDiscover(args[1], args[2])
            if args[0] == "Config": 
                if len(args) == 1: 
                    return self.wbConfigSets()
                else:
                    return self.wbConfigSet(args[1])
            # Intermediate form responses
            if args[0] == "ConfigAction":    return self.wbConfigAction()
            if args[0] == "NewConfigSet":    return self.wbNewConfigSet()
            if args[0] == "DeleteConfigSet": return self.wbDeleteConfigSet()
            if args[0] == "DeleteConfig":    return self.wbDeleteConfig()
            if args[0] == "CopyConfig":      return self.wbCopyConfig()
            if args[0] == "MoveConfig":      return self.wbMoveConfig()
            if args[0] == "UploadConfig":    return self.wbUploadConfig()

        raise cherrypy.HTTPError(404, "Unrecognized URI: "+requri+", args[0] "+args[0] )
        # cherrypy.response.status = "204 WebBrick command accepted ("+wbaddr+","+wbchan+","+cmd+")"
        return ""

    @turbogears.expose()
    def continuation(self, *args):
        """
        Pseudo-continuation function.
        A web form that returns its values to /wbcnf/continuation can invoke
        a named function on this class, with specified parameters.
        
        Form parameters used:
        continuation    name of form parameter containing (a) the name of the method 
                        to invoke, followed by the names of the form parameters that
                        contain parameters to be passed to that method.
        <other>         (as named by 'params') parameters passed to the named method
        """
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        req          = cherrypy.request
        #Info("continuation params %s"%(str(req.paramMap)),"WbCfgManagerForm.continuation")
        continuation = req.paramMap["continuation"].split(',')
        method       = self.__getattribute__(continuation[0])
        params       = []
        for p in continuation[1:]: params.append(req.paramMap[p])
        #Info("method %s(%s)"%(method,str(params)),"WbCfgManagerForm.continuation")
        return method(*params)

    # Main configuration form display and submission processing
    # ---------------------------------------------------------

    @turbogears.expose(template="WebBrickConfig.templates.ConfigManager")
    def ConfigFrontPage(self):
        """
        Returns the configuration manager main page.
        """
        #TODO: provide for message to be displayed on form display
        #      (i.e. replace separate message displays)
        cherrypy.session.acquire_lock()
        result = {
            "Network"     : cherrypy.session.get("Network",""),
            "ConfigSet"   : cherrypy.session.get("ConfigSet",""),
            "Password"    : cherrypy.session.get("Password","") }
        cherrypy.session.release_lock()
        return result

    def getAction( self, paramMap ):
        # This is because IE is broken.
        # it returns the values for all buttons of the same name
        # whilst the spec is that it should only return the active button value
        if paramMap.has_key("WbNewCs"):
            return paramMap["WbNewCs"]
        if paramMap.has_key("WbDeleteCs"):
            return paramMap["WbDeleteCs"]
        if paramMap.has_key("WbLoad"):
            return paramMap["WbLoad"]
        if paramMap.has_key("WbSave"):
            return paramMap["WbSave"]
        if paramMap.has_key("WbSaveAll"):
            return paramMap["WbSaveAll"]
        if paramMap.has_key("WbNew"):
            return paramMap["WbNew"]
        if paramMap.has_key("WbShow"):
            return paramMap["WbShow"]
        if paramMap.has_key("WbEdit"):
            return paramMap["WbEdit"]
        if paramMap.has_key("WbDelete"):
            return paramMap["WbDelete"]
        if paramMap.has_key("WbDiscover"):
            return paramMap["WbDiscover"]
        if paramMap.has_key("WbRemove"):
            return paramMap["WbRemove"]
        if paramMap.has_key("WbAdd"):
            return paramMap["WbAdd"]
        if paramMap.has_key("WbIpUpdate"):
            return paramMap["WbIpUpdate"]
        if paramMap.has_key("WbCopy"):
            return paramMap["WbCopy"]
        if paramMap.has_key("WbMove"):
            return paramMap["WbMove"]
        if paramMap.has_key("WbUpload"):
            return paramMap["WbUpload"]
        if paramMap.has_key("WbDownload"):
            return paramMap["WbDownload"]
        return None

    @turbogears.expose()
    def wbConfigAction(self):
        """
        Process return from main configuration form
        """

        # Process submission        
        req    = cherrypy.request
        action = req.paramMap["action"]
        if isinstance( action, list ):
            # Internet explorer
            action = req.paramMap["buttonAction"]
        
        #action = self.getAction( req.paramMap )
        Trace("%s"%(req.paramMap), "wbConfigAction")

        # Save selections for session consistency
        cherrypy.session.acquire_lock()
        cherrypy.session["Network"]   = req.paramMap["WbIpNetworks"]
        cherrypy.session["ConfigSet"] = req.paramMap["WbConfigSets"]
        cherrypy.session["Password"]  = req.paramMap["WbPassword"]
        cherrypy.session.release_lock()

        # Force discovery of WebBricks on selected network
        if action == "WbDiscover":
            net = req.paramMap["WbIpNetworks"]
            self.WebBrickDiscover(net)
            return self.ConfigFrontPage()

        # Update IP address of WebBrick
        if action == "WbIpUpdate":
            Password   = req.paramMap["WbPassword"] or "password"
            NewIpAdrs  = req.paramMap["WbNewIpAdrs"]
            IpAddress  = req.paramMap["WbIpAddress"]
            MacAddress = req.paramMap["WbMacAddress"]
            NetAddress = req.paramMap["WbIpNetworks"]
            if NewIpAdrs == IpAddress:
                return self.wbConfigMessage(
                    "WebBrick IP address not changed (%s)"%(IpAddress))
            err = self.WebBrickUpdateIp(IpAddress, MacAddress, NetAddress, Password, NewIpAdrs)
            self.WebBrickFlushDiscovered()
            return err or self.wbConfigMessage(
                "Sent new IP address "+NewIpAdrs+
                " to WebBrick "+MacAddress+" at "+IpAddress,
                "(If the WebBrick IP address does not appear to be updated, "+
                "check that the correct WebBrick password is being used)")

        # Remove WebBrick from list of WebBricks
        if action == "WbRemoveWebBrick":
            wbn = req.paramMap.get("WbSelector","")
            err = self.WebBrickRemove(wbn)
            if err: return self.wbConfigError(err)
            return self.ConfigFrontPage()

        # Add WebBrick IP address to the list of WebBricks
        if action == "WbAddIpAddress":
            wbip = req.paramMap.get("WbNewIpAdrs","")
            err  = self.WebBrickAdd(wbip)
            return err or self.ConfigFrontPage()

        # Load/Save WebBrick configurations
        if action == "WbLoadConfig":
            if not req.paramMap.has_key("WbSelector"):
                return self.wbConfigError("No WebBrick selected for load")
            nodenum   = req.paramMap["WbSelector"]
            nodemac   = req.paramMap["WbMacAddress"]
            nodeip    = req.paramMap["WbIpAddress"]
            password  = req.paramMap["WbPassword"]
            configset = req.paramMap["WbConfigSets"]
            confignum = req.paramMap["WbConfigNode"]
            err = self.WebBrickLoad( nodenum, nodeip, nodemac, password, configset, confignum )
            return err or self.wbConfigMessage(
                "Loaded WebBrick configuration for node "+str(confignum),
                "If the WebBrick configuration does not appear to be updated, "+
                "check that the correct WebBrick password is being used")

        if action == "WbSaveConfig":
            if not req.paramMap.has_key("WbSelector"):
                return self.wbConfigError("No WebBrick selected for save")
            nodenum   = req.paramMap["WbSelector"]
            nodeip    = req.paramMap["WbIpAddress"]
            configset = req.paramMap["WbConfigSets"]
            err = self.WebBrickSave( nodenum, nodeip, configset, False )
            return err or self.wbConfigMessage(
                "Saved WebBrick configuration for node "+str(nodenum))

        if action == "WbSaveAllConfigs":
            def mkpair(s): return s.split(',',2)
            def ispair(p): return len(p) == 2            
            nodeliststr = req.paramMap["WbNodeList"]
            nodelist    = filter(ispair, map(mkpair, nodeliststr.split(';')))
            configset   = req.paramMap["WbConfigSets"]
            numnodes    = 0
            for (nodenum,nodeip) in nodelist:
                err = self.WebBrickSave( nodenum, nodeip, configset, False )
                if err: return err
                numnodes += 1
            if numnodes == 0:
                msg = "No WebBrick configurations saved"
            else:
                msg = "Saved configuration for "+str(numnodes)+" WebBrick"
                if numnodes > 1: msg += "s"
            return self.wbConfigMessage(msg)

        # Create/delete configuration set
        if action == "WbNewCs":
            return self.NewConfigSetForm("")

        if action == "WbDeleteCs":
            configset = req.paramMap["WbConfigSets"]
            if not ConfigSet.exists(configset):
                return self.wbConfigError(
                    "Configuration set does not exist: "+configset)
            return self.DeleteConfigSetForm(configset)

        if action == "WbDeleteConfig":
            configset  = req.paramMap["WbConfigSets"]
            confignode = req.paramMap["WbConfigNode"]
            configname = req.paramMap["WbConfigName"]
            if not Config.exists(configset, confignode):
                return self.wbConfigError(
                    "Configuration set %s/%s does not exist"%(configset,confignode))
            return self.DeleteConfigForm(configset, confignode, configname)

        # Configuration manipulation (New, Show, Edit, Delete)
        if action == "WbShowConfig":
            configset  = req.paramMap["WbConfigSets"]
            confignode = req.paramMap["WbConfigNode"]
            configname = req.paramMap["WbConfigName"]
            return self.ShowConfigForm(configset, confignode, configname)

#################### more ############################


        # Configuration transfer options (Copy, Move, Upload, Download)
        if action == "WbCopyConfig":
            configsets = ConfigSet.listNames()
            configset  = req.paramMap["WbConfigSets"]
            confignode = req.paramMap["WbConfigNode"]
            configname = req.paramMap["WbConfigName"]
            return self.CopyConfigForm(configset, confignode, configname, configsets)

        if action == "WbMoveConfig":
            configsets = ConfigSet.listNames()
            if req.paramMap["WbConfigNode"] == "(None)":
                return self.wbConfigError("Move: a source node must be selected")
            configset  = req.paramMap["WbConfigSets"]
            confignode = req.paramMap["WbConfigNode"]
            configname = req.paramMap["WbConfigName"]
            return self.MoveConfigForm(configset, confignode, configname, configsets)

        if action == "WbUploadConfig":
            configset  = req.paramMap["WbConfigSets"]
            return self.UploadConfigForm(configset)

        if action == "WbDownloadConfig":
            configset  = req.paramMap["WbConfigSets"]
            confignode = req.paramMap["WbConfigNode"]
            return self.DownloadConfig(configset, confignode)

        # Default for now: dump form parameters
        paramlist = ""
        for k in req.paramMap.keys():
            paramlist += str(k)+": "+str(req.paramMap[k])+"\n"
        return ("<h1>Unrecognized option</h1>\n"+
            "<pre>"+paramlist+"</pre>"+
            """
            <p>
            <a href='"""+self.FrontPage+"""'>Return to main configuration manager page</a>
            </p>
            """)


    # Callback URI serving methods
    # ----------------------------

    @turbogears.expose()
    def wbNetworks(self):
        cherrypy.response.headerMap["Content-Type"]  = "application/xml"
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        networks = map( wrap("<Network>", "</Network>"), WbConfigSettings.Networks )
        return (
            """<?xml version="1.0" encoding="utf-8" ?>
            <Networks>
            """+
            "\n".join(networks)+
            """
            </Networks>
            """ )

    @turbogears.expose()
    def wbDiscover(self, netadrs, netmask):
        def mkWbAttrs(wb):
            if (wb["nodeNum"] != None) and (wb["nodeName"] != None):
                return (
                    "mac='%s' node='%03d' name='%s' adrs='%s' attn='%s'" %
                    (wb["macAdr"], wb["nodeNum"], wb["nodeName"],
                    wb["ipAdr"], wb["attention"]))
            else:
                return (
                    "mac='%s' node='' adrs='%s' attn='%s'" %
                    (wb["macAdr"], wb["ipAdr"], wb["attention"]))
        newnet = netadrs+"/"+netmask
        cherrypy.session.acquire_lock()
        oldnet = cherrypy.session.get("DiscoverNet","")
        wbs    = cherrypy.session.get("DiscoverWbs",[])
        cherrypy.session.release_lock()
        Info("New %s, old %s"%(newnet,oldnet), "WbCfgManagerForm.wbDiscover")
        if newnet != oldnet:
            wbs = self.WebBrickDiscover(newnet)
        cherrypy.response.headerMap["Content-Type"]  = "application/xml"
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        webbricks = map( 
            wrap("<WebBrick ", " />"), 
            map(mkWbAttrs,wbs) )
        return (
            """<?xml version="1.0" encoding="utf-8" ?>
            <WebBricks>
            """+
            "\n".join(webbricks)+
            """
            </WebBricks>
            """ )

    @turbogears.expose()
    def wbConfigSets(self):
        cherrypy.response.headerMap["Content-Type"]  = "application/xml"
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        configsets = map( wrap("<ConfigSet>", "</ConfigSet>"), ConfigSet.listNames() )
        return (
            """<?xml version="1.0" encoding="utf-8" ?>
            <ConfigSets>
            """+
            "\n".join(configsets)+
            """
            </ConfigSets>
            """ )

    @turbogears.expose()
    def wbConfigSet(self, configset):
        def mkConfig(n):
            cnfxml = Config.read(configset, n)
            try:
                wb6cnf = Wb6Config(cnfxml=cnfxml)
                return "<Config node='%s' name='%s' />" % (n, wb6cnf.getNodeName())
            except Exception, e:
                return "<Config node='%s' name='(Bad config file)' />"%(n)
        cherrypy.response.headerMap["Content-Type"]  = "application/xml"
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        configs = map(mkConfig, Config.listNodes(configset))
        return (
            """<?xml version="1.0" encoding="utf-8" ?>
            <Configs>
            """+
            "\n".join(configs)+
            """
            </Configs>
            """ )

    # Secondary form display functions
    # --------------------------------
    
    @turbogears.expose(template="WebBrickConfig.templates.NewConfigSet")
    def NewConfigSetForm(self, configsetname):
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        return { "ConfigSet" : configsetname }

    @turbogears.expose(template="WebBrickConfig.templates.DeleteConfigSet")
    def DeleteConfigSetForm(self, configsetname):
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        return { "ConfigSet" : configsetname }

    @turbogears.expose(template="WebBrickConfig.templates.DeleteConfig")
    def DeleteConfigForm(self, configsetname, confignode, configname):
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        return { "ConfigSet"  : configsetname,
                 "ConfigNode" : confignode, 
                 "ConfigName" : configname,
               }

############--############
    @turbogears.expose(template="WebBrickConfig.templates.EditConfig")
    def ShowConfigForm(self, configsetname, confignode, configname):
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        ### read config into local structure
        if not ConfigSet.exists(configsetname):
            return self.wbConfigError("Configuration set does not exist: "+configsetname)
        if not Config.exists(configsetname, confignode):
            return self.wbConfigError(
                "No configuration file for node (%s, %s)" % 
                (configset, confignode))
        cnfxml = Config.read(configsetname, confignode)
        if not cnfxml:
            return self.wbConfigError(
                "Cannot read configuration file for node (%s, %s)" % 
                (configsetname, confignode))
        wbcnf = Wb6Config(cnfxml=cnfxml)
        return { "WbCnf": wbcnf }
############--############

    @turbogears.expose(template="WebBrickConfig.templates.CopyConfig")
    def CopyConfigForm(self, configsetname, confignode, configname, configsets):
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        return { "ConfigSet"  : configsetname,
                 "ConfigNode" : confignode, 
                 "ConfigName" : configname, 
                 "ConfigSets" : configsets, 
               }

    @turbogears.expose(template="WebBrickConfig.templates.MoveConfig")
    def MoveConfigForm(self, configsetname, confignode, configname, configsets):
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        return { "ConfigSet"  : configsetname,
                 "ConfigNode" : confignode, 
                 "ConfigName" : configname, 
                 "ConfigSets" : configsets, 
               }

    @turbogears.expose(template="WebBrickConfig.templates.UploadConfig")
    def UploadConfigForm(self, configsetname):
        cherrypy.response.headerMap["Cache-Control"] = "no-cache"
        return { "ConfigSet"  : configsetname,
               }

### How can I write a generic template+dictionary expose function?
#    @turbogears.expose()
#    def ExposeForm(template, **kwargs ):
#        kwargs["..."] = template
#        return kwargs

    # Secondary form submission handling
    # ----------------------------------

    def wbNewConfigSet(self):
        """
        Process return from new configuration set form
        """
        req = cherrypy.request
        if "Confirm" in req.paramMap.keys():
            configset = req.paramMap["WbConfigSet"]
            if not ConfigSet.validName(configset):
                return self.wbConfigError("Invalid configuration set name: '"+configset+"'")
            if ConfigSet.exists(configset):
                return self.wbConfigError("Configuration set already exists: "+configset)
            ConfigSet.create(configset)        
        return self.ConfigFrontPage()

    def wbDeleteConfigSet(self):
        """
        Process return from delete configuration set confirmation form
        """
        req = cherrypy.request
        if "Confirm" in req.paramMap.keys():
            configset = req.paramMap["WbConfigSet"]
            if not ConfigSet.exists(configset):
                return self.wbConfigError("Configuration set does not exist: "+configset)
            ConfigSet.delete(configset)
        return self.ConfigFrontPage()

    def wbDeleteConfig(self):
        """
        Process return from delete WebBrick configuration confirmation form
        """
        req = cherrypy.request
        if "Confirm" in req.paramMap.keys():
            configset  = req.paramMap["WbConfigSet"]
            confignode = req.paramMap["WbConfigNode"]
            err = Config.delete(configset,confignode)
            if err: return self.wbConfigError(err)
        return self.ConfigFrontPage()

    def wbCopyConfig(self):
        """
        Process return from copy configuration form
        
        Sample request parameter map dictionaries:
        {'Cancel': ''}
        {'Confirm': '', 'NodeOrSet': 'Set', 
         'ConfigSet': 'Example-1', 
         'ToConfigSet': 'Example-2'}
        {'Confirm': '', 'NodeOrSet': 'Node', 
         'ConfigSet': 'Example-1', 'ConfigNode': '011', 'ConfigName': 'Example1-011', 
         'ToConfigSet': 'Example-2', 'ToConfigNode': '022'}
        """
        req = cherrypy.request
        Trace( str(req.paramMap), "WbCfgManagerForm.wbCopyConfig")
        if req.paramMap.has_key("Cancel"):
            return self.ConfigFrontPage()
        frset = req.paramMap["ConfigSet"] 
        toset = req.paramMap["ToConfigSet"]
        if req.paramMap["NodeOrSet"] == "Set":
            return self.CopyConfigSet(frset, toset)
        frnode = req.paramMap["ConfigNode"] 
        tonode = req.paramMap["ToConfigNode"]
        return self.CopyConfig(frset, frnode, toset, tonode)

    def wbMoveConfig(self):
        """
        Process return from move/rename configuration form
        
        Sample request parameter map dictionaries:
        {'Cancel': ''}
        {'Confirm': '',
         'ConfigSet': 'Example-1', 'ConfigNode': '011', 'ConfigName': 'Example1-011', 
         'ToConfigSet': 'Example-2', 'ToConfigNode': '022'}
        """
        req = cherrypy.request
        Trace( str(req.paramMap), "WbCfgManagerForm.wbMoveConfig")
        if req.paramMap.has_key("Cancel"):
            return self.ConfigFrontPage()
        frset = req.paramMap["ConfigSet"] 
        toset = req.paramMap["ToConfigSet"]
        frnode = req.paramMap["ConfigNode"] 
        tonode = req.paramMap["ToConfigNode"]
        return self.MoveConfig(frset, frnode, toset, tonode)

    # def wbUploadConfig(self, ConfigSet=None, ConfigFile=None):
    def wbUploadConfig(self):
        """
        Process return from move/rename configuration form
        
        Sample request parameter map dictionaries:
        {'Cancel': ''}
        {'Confirm': '',
         'ConfigSet': 'Example-1',
         'ConfigFile': (data),
         }
        """
        req = cherrypy.request
        Trace( str(req.paramMap), "WbCfgManagerForm.wbUploadConfig")
        if req.paramMap.has_key("Cancel"):
            return self.ConfigFrontPage()
        toset   = req.paramMap["ConfigSet"] 
        datastr = req.paramMap["ConfigFile"].file
        # toset   = ConfigSet
        # datastr = ConfigFile.file
        return self.UploadConfig(toset, datastr)

    # WebBrick discovery function
    # ---------------------------

    def WebBrickDiscover(self, net):
        wbs = WbDiscoverFull(self._discover, net)
#        wbs = WbDiscoverFull(net)
        cherrypy.session.acquire_lock()
        cherrypy.session["DiscoverWbs"] = wbs
        cherrypy.session["DiscoverNet"] = net
        cherrypy.session.release_lock()
        return wbs

    def WebBrickFlushDiscovered(self):
        cherrypy.session.acquire_lock()
        cherrypy.session["DiscoverNet"] = ""
        cherrypy.session.release_lock()
        return

    def WebBrickRemove(self, wbn):
        if not wbn:
            return "Remove WebBrick: none selected"
        cherrypy.session.acquire_lock()
        wbs = cherrypy.session.get("DiscoverWbs",[])
        for wb in wbs:
            if wbn and wb["nodeNum"] == int(wbn):
                wbs.remove(wb)
                cherrypy.session["DiscoverWbs"] = wbs
                break
        cherrypy.session.release_lock()
        return None

    def WebBrickAdd(self, wbip):
        if not wbip or wbip == "(None)":
            return "Add WebBrick: no IP address specified"
        err = None
        cherrypy.session.acquire_lock()
        wbs = cherrypy.session.get("DiscoverWbs",[])
        new = True
        for wb in wbs:
            new = new and wb["ipAdr"] != wbip
        if new:
            try:
                wb = WbDiscoverCheck(wbip)
                if wb:
                    wbs.append(wb)
                    cherrypy.session["DiscoverWbs"] = wbs
                else:
                    err = self.wbConfigError(
                        "No WebBrick found with IP address %s"%(wbip))
            except Exception, e:
                err = self.wbConfigError(
                    "Error accessing WebBrick at %s"%(wbip),
                    escapeTextForHtml(str(e)))
        cherrypy.session.release_lock()
        return err

    def WebBrickUpdateIp(self, IpAddress, MacAddress, NetAddress, Password, NewIpAdrs):
        if IpAddress == "(None)": return "No WebBrick selected"
        if NewIpAdrs == "(None)": return "No IP address specified"
        bcadrs   = formatIpAdrs(mkBroadcastAddress(*parseNetAdrs(NetAddress)))
        macbytes = parseMacAdrs(MacAddress)
        ipbytes  = parseIpAdrs(NewIpAdrs)
        err      = login(bcadrs, Password)
        err      = err or setIp(bcadrs, macbytes, ipbytes)
        return err

    # WebBrick load/save functions
    # ----------------------------

    def WebBrickLoad(self, nodenum, nodeip, nodemac, password, configset, confignum):
        """
        Load configuration to a specified WebBrick from the given
        configuration file.

        Returns None if the operation is completed successfully, otherwise
        returns a page to be displayed describing the reason for non-completion.
        """
        if not ConfigSet.exists(configset):
            return self.wbConfigError("Configuration set does not exist: "+configset)
        if not Config.exists(configset, confignum):
            return self.wbConfigError(
                "No configuration file for node (%s, %s)" % 
                (configset, str(confignum)))
        cnfxml = Config.read(configset, confignum)
        if not cnfxml:
            return self.wbConfigError(
                "Cannot read configuration file for node (%s, %s)" % 
                (configset, str(confignum)))
        return self.UpdateConfig(nodeip, cnfxml, {'password': password})

    def WebBrickSave(self, nodenum, nodeip, configset, confirmed):
        """
        Save configuration for the specified WebBrick into the given
        configuration set directory.
        
        Returns None if the operation is completed successfully, otherwise
        returns a page to be displayed describing the reason for non-completion.
        """
        if not ConfigSet.exists(configset):
            return self.wbConfigError("Configuration set does not exist: "+configset)
        if Config.exists(configset, nodenum):
            if not bool(confirmed):
                return self.wbConfirmQuery(
                    "Overwrite existing configuration for node "+str(nodenum)+"?",
                    "WebBrickSaveAndContinue", nodenum, nodeip, configset, "True" )
            Config.backup(configset, nodenum)
        wb     = Wb6Config(nodeip)
        cnfxml = wb.getConfigXml()
        if not cnfxml:
            return self.wbConfigError(
                "Cannot get configuration from WebBrick (%s, %s)")
        return Config.create(configset, nodenum, cnfxml)

    def WebBrickSaveAndContinue(self, nodenum, nodeip, configset, confirmed):
            err = self.WebBrickSave( nodenum, nodeip, configset, confirmed)
            return err or self.wbConfigMessage(
                "Saved WebBrick configuration for node "+str(nodenum))

    def UpdateConfig(self, adrs, cnfxml, override):
        """
        Update configuration of specified WebBrick from specified file.

        Returns None if the operation is completed successfully, otherwise
        returns a page to be displayed describing the reason for non-completion.

        'adrs' is the IP address of the WebBrick top be updated.

        'cnfxml' is the text of the WebBrick XML configuration file to be uploaded.

        'override' is a dictionary of values that can be used to override values
        in the supplied DOM when generating the configuration commands; e.g.
            "password" - overrides password used with "LG" command
            "IP"       - overrides IP addresss set with "IA" command
        """
        #TODO: may need to add logic to allow rejection of commands/command forms
        #      not supported by older WebBricks?
        try:
            wbcfg = WebBrickConfig()
            dom   = parseXmlString(cnfxml)
            configcmds = wbcfg.makeConfigCommands(dom, override)
            # configcmds.append("RU")
            # Reboot WebBrick to work around RU command bug in some WebBrick firmware versions
            # TODO: 
            #   Consider: should the RU command be withdrawn?  
            #   How many buggy webbricks are in the wild?
            configcmds.append("RB")
            errs = ""
            for line in configcmds:
                if line[0] != '#':
                    SendHTTPCmd(adrs,line)
                    err = Wb6Status(adrs).getCmdStatus()
                    msg = None
                    if err == ERR_NotLoggedIn:
                        msg = "Incorrect WebBrick password ("+line+")"
                        err = 0
                    if err:
                        errs += "WebBrick command error: "+str(err)+",  ("+line+")\n"
                    if msg:
                        Warn(msg, "WbCfgManagerForm.UpdateConfig")
                        raise WbAccessException(msg)
        except Exception, e:
            return self.wbConfigError(
                "Failed to update WebBrick at %s" % (adrs), 
                escapeTextForHtml(str(e)))
        if errs:
            return self.wbConfigError(
                "Failure(s) updating WebBrick at %s" % (adrs), 
                escapeTextForHtml(errs))
        self.WebBrickFlushDiscovered()
        return None

    def CopyConfigSet(self, frset, toset):
        """
        Copy configuration set on gateway server
        """
        if frset == toset:
            return self.wbConfigError("Cannot copy configuration set to itself")
        if not ConfigSet.exists(toset):
            return self.wbConfigError("Target configuration set does not exist")
            # ConfigSet.create(toset)
        if Config.listNodes(toset):
            return self.wbConfigError(
                "Copy: target configuration set already contains node configuration data"+
                " - select a new or empty configuration set")
        nodes = Config.listNodes(frset)
        for n in nodes:
            err = Config.copy(frset,n,toset,n)
            if err:
                return self.wbConfigError(err)
        return self.wbConfigMessage(
            "Copied WebBrick configuration set %s to %s" % (frset, toset))

    NodeNumRegex = re.compile(r'\d*$')

    def CopyConfig(self, frset, frnode, toset, tonode):
        """
        Copy node configuration on gateway server
        """
        if frset == toset and frnode == tonode:
            return self.wbConfigError("Cannot copy node configuration to itself")
        # Check target node, and ensure it is a 3-digit string
        if not WebBrickCfgEdit.NodeNumRegex.match(tonode):
            return self.wbConfigError(
                "Invalid target node %s (must be a number)"%(tonode))
        n = int(tonode)
        if n <= 0 or n > 255:
            return self.wbConfigError(
                "Invalid target node %n (must be in range 1-255)"%(n))
        tonode = formatInt("%03d")(n)
        if Config.exists(toset, tonode):
            return self.wbConfigError(
                "Invalid target node %s/%s already exists"%(toset,tonode))
        # Now copy
        err = Config.copy(frset, frnode, toset, tonode)
        if err: 
            return self.wbConfigError(err)
        return self.wbConfigMessage(
            "Copied WebBrick configuration %s/%s to %s/%s" % 
            (frset, frnode, toset, tonode))

    def MoveConfig(self, frset, frnode, toset, tonode):
        """
        Move/rename node configuration on gateway server
        """
        if frset == toset and frnode == tonode:
            return self.wbConfigError("Cannot move node configuration to itself")

        # Check target node, and ensure it is a 3-digit string
        if not WebBrickCfgEdit.NodeNumRegex.match(tonode):
            return self.wbConfigError(
                "Invalid target node %s (must be a number)"%(tonode))
        n = int(tonode)
        if n <= 0 or n > 255:
            return self.wbConfigError(
                "Invalid target node %n (must be in range 1-255)"%(n))
        tonode = formatInt("%03d")(n)
        if Config.exists(toset, tonode):
            return self.wbConfigError(
                "Invalid target node %s/%s already exists"%(toset,tonode))
        # Now copy
        err = Config.move(frset, frnode, toset, tonode)
        if err: 
            return self.wbConfigError(err)
        return self.wbConfigMessage(
            "Moved WebBrick configuration %s/%s to %s/%s" % 
            (frset, frnode, toset, tonode))

    def UploadConfig(self, toset, datastr):
        """
        Upload configuration set or single configuration file to the
        specified copnfiguration set.
        
        'toset'   is the target configuration set
        
        'datastr' is a file-like object containing the data to be uploaded.
                  If this appears to be a ZIP file, it is presumed to contain 
                  configuration set, one file per WebBrick.
        """
        try:
            # ZIP file - upload configuration set
            datazip = zipfile.ZipFile(datastr)
            datastr = None
        except zipfile.BadZipfile, e:
            # Non-ZIP file - upload single configuration
            datastr.seek(0)
            datazip = None
        if datazip:
            if Config.listNodes(toset):
                return self.wbConfigError(
                    "Copy: target configuration set already contains node configuration data"+
                    " - select a new or empty configuration set")
            uploads = ""
            for f in datazip.namelist():
                Trace( "Zip entry %s"%(f), "WbCfgManagerForm.UploadConfigData")
                # Filter out hidden files and empty directories (e.g. .svn/):
                if f[0] != '.' and f[-1] != '/':
                    (tonode,err) = self.UploadConfigData(toset, datazip.read(f))
                    if err:
                        return self.wbConfigError(
                            err+"<br/>Configuration upload abandoned"+uploads)
                    uploads += ("...uploaded file %s as node %s<br/>"%(f,tonode))
            return self.wbConfigMessage(
                "Uploaded WebBrick configuration set %s"%(toset), uploads)
        else:
            Trace( "Upload file", "WbCfgManagerForm.UploadConfigData")
            (tonode,err) = self.UploadConfigData(toset, datastr.read())
            if err:
                return self.wbConfigError(err)
            return self.wbConfigMessage(
                "Uploaded WebBrick configuration %s/%s " % (toset, tonode))

    def UploadConfigData(self, toset, data):
        """
        Save configuration for a single WebBrick
        
        'toset'   is the target configuration set
        
        'data'    is a the WebBrick configuration data to be saved.
        """
        Trace( "%s"%(toset), "WbCfgManagerForm.UploadConfigData")
        if not data:
            return (toset, "Empty configuration data supplied")
        wbcfg  = Wb6Config(cnfxml=data)
        tonode = formatInt("%03d")(wbcfg.getNodeNumber())
        return (tonode,Config.write(toset, tonode, wbcfg.getConfigXml()))

    def DownloadConfig(self, frset, frnode):
        """
        Upload configuration set or single configuration file to the
        specified configuration set.
        
        'frset'   is the configuration set from whioch data is downloaded
        
        'frnode'  is the node whose configuration is to be downloaded as a
                  simple XML file, or "(None)" is the entire configuration set 
                  is to be downloaded as a ZIP file.
        """
        if frnode == "(None)":
            frnodes = Config.listNodes(frset)
            zipstr  = StringIO.StringIO()
            zipfil  = zipfile.ZipFile(zipstr, mode='w')
            for n in frnodes:
                dattim = time.localtime()[0:6]
                zipinf = zipfile.ZipInfo(filename=n+".xml", date_time=dattim)
                zipfil.writestr(zipinf, Config.read(frset, n))
            zipfil.close()
            cherrypy.response.headerMap.update(
                {"Content-Type":        "application/octet-stream",
                 "Content-disposition": "attachment; filename=%s.zip"%frset})
            result = zipstr.getvalue()
            zipstr.close()
            return result
        else:
            data = Config.read(frset, frnode)
            cherrypy.response.headerMap.update(
                {"Content-Type":        "application/xml",
                 "Content-disposition": "attachment; filename=%s.xml"%frnode})
            return data


    # Generic error, message and query forms
    # --------------------------------------

    def wbConfigError(self, msg, detail=""):
        """
        Report an error condition, 
        after which return to the main configuration screen
        """
        if detail:
            detail = "<p>"+detail+"</p>"
        return (
            """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
              <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
              <title>WebBrick Configuration Error</title>
            </head>
            <body>
            <h1>Configuration error</h1>
            <h2>"""+msg+"""</h2>"""+detail+"""
            <form name="ConfigError" action='"""+self.FrontPage+"""' method="get">
              <button>Continue</button>
            </form>
            </body>
            </html>
            """)

    def wbConfigMessage(self, msg, detail=""):
        """
        Display a message to the user,
        after which return to the main configuration screen
        """
        if detail:
            detail = "<p>"+detail+"</p>"
        return (
            """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
              <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
              <title>WebBrick Configuration</title>
            </head>
            <body>
            <h1>WebBrick Configuration</h1>
            <h2>"""+msg+"""</h2>"""+detail+"""
            <form name="ConfigError" action='"""+self.FrontPage+"""' method="get">
              <button>Continue</button>
            </form>
            </body>
            </html>
            """)

    def wbConfirmQuery(self, msg, method, *args):
        """
        Display a confirmation query to the user.
        If the user cancels the queried operation, return to the main 
        configuration screen, otherwise invoke the named continuation
        method with parameters supplied as additional arguments to this
        function.
        """
        continuation = method
        paramlist    = ""
        i            = 0
        for pval in args:
            pname = "p" + str(i)
            continuation += "," + pname
            paramlist    += "<input type='hidden' name='"+pname+"' value='"+pval+"' />\n"
            i += 1
        return (
            """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
              <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
              <title>Confirm WebBrick Configuration Action</title>
            </head>
            <body>
            <h1>Confirm WebBrick Configuration Action</h1>
            <h2>"""+msg+"""</h2>
            <form name="ConfirmQuery" action="/wbcnf/continuation" method="get">
              <button name="continuation" value='"""+continuation+"""'>OK</button>
              <button name="continuation" value="ConfigFrontPage">Cancel</button>
              """+paramlist+"""
            </form>
            </body>
            </html>
            """)


# Helper functions
# ----------------

def wrap(s1,s2): 
    """
    Return a function that wraps a supplied string in a supplied prefix and suffix.
    This is used for constructing XML elements from a list of values.
    """
    return (lambda t: s1+t+s2)

def login(tgtadrs, password):
    if not sendUdpCommand(tgtadrs, ':LG;'+password+':'):
        return "Failed to send login to WebBrick"
    return None

def setIp(tgtadrs, macbytes, ipbytes):
    cmd  = (':SA;'+
        formatIntList(macbytes,sep=";")+";"+
        formatIntList(ipbytes,sep=";")+":")
    if not sendUdpCommand(tgtadrs, cmd):
        return "Failed to send new address to WebBrick"
    return None

# End: $Id: WbCfgManagerForm.py 3138 2009-04-15 10:17:29Z philipp.schuster $
