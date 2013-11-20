import re
import sys
import string
import time
import logging

import turbogears
from turbogears import config
from turbogears import controllers, expose
import pkg_resources
pkg_resources.require("TurboGears")

import cherrypy

from MiscLib.DomHelpers import parseXmlFile, parseXmlString, getDictFromXml

from EventHandlers.EventRouterLoad import EventRouterLoader

from WebBrickLibs.WbConfigBase import WbConfigBase

from WebBrickConfig.Discovery import DiscoverHandler
from WebBrickConfig.WbCfgManagerForm import WbCfgManagerForm



import xml.etree.ElementTree as ET

import simplejson as json
from os import listdir

import Webbrick
#import LocalState
import EventState
import UserInterface
#import MediaAccess
###import PanelRenderer
import LocalData
import Schedule
import SendEvent
import ClientProfiles
import Media
from Utils import validateTemplateDirectory

# The common static base class is not working properly. or as intended
#from WebBrickGateway.WbConfigSettings import WbConfigSettings
from WebBrickConfig.WbConfigSettings import WbConfigSettings

#DESPATCH_CONFIG_FILE = "/EventDespatch"

# NEW (2009_08_01) WebBrick Gateway Config EGG Only to be loaded for Armour Dev for now
ARMOUR_DEV = False
if ARMOUR_DEV:
    from WebBrickGwConfig.WbGwCfgManager import WbGwCfgManager


# --------------------------------------------------
# Root controller
# --------------------------------------------------

_log = logging.getLogger( "WebBrickGateway.Root" )

def log_versions():
    from WebBrickLibs import __VERSION__ as libVersion
    from WebBrickRes import __VERSION__ as resVersion
    from WebBrickDoc import __VERSION__ as docVersion
    from WebBrickGateway import __VERSION__ as gwyVersion
    from WebBrickConfig import __VERSION__ as cfgVersion
    _log.info( "WebBrickLibs build nr %s", libVersion )
    _log.info( "WebBrickRes build nr %s", resVersion )
    _log.info( "WebBrickDoc build nr %s", docVersion )
    _log.info( "WebBrickGateway build nr %s", gwyVersion )
    _log.info( "WebBrickConfig build nr %s", cfgVersion )

def publish_versions(evt_router):
    from EventLib.Event import makeEvent  
    from EventLib.EventAgent import EventAgent

    from socket import gethostname
    
    from WebBrickLibs import __VERSION__ as libVersion
    from WebBrickRes import __VERSION__ as resVersion
    from WebBrickDoc import __VERSION__ as docVersion
    from WebBrickGateway import __VERSION__ as gwyVersion
    from WebBrickConfig import __VERSION__ as cfgVersion
    #
    #  Now publish these as events
    #
    
    sysName = gethostname()
    
    evt_router.publish( EventAgent(""), makeEvent( 'http://id.webbrick.co.uk/events/diagnostics/software/version', 'WebBrickLibs', { 'build':libVersion, 'name':sysName } ) )  
    evt_router.publish( EventAgent(""), makeEvent( 'http://id.webbrick.co.uk/events/diagnostics/software/version', 'WebBrickRes', { 'build':resVersion, 'name':sysName } ) )  
    evt_router.publish( EventAgent(""), makeEvent( 'http://id.webbrick.co.uk/events/diagnostics/software/version', 'WebBrickDoc', { 'build':docVersion, 'name':sysName } ) )  
    evt_router.publish( EventAgent(""), makeEvent( 'http://id.webbrick.co.uk/events/diagnostics/software/version', 'WebBrickGateway', { 'build':gwyVersion, 'name':sysName } ) )  
    evt_router.publish( EventAgent(""), makeEvent( 'http://id.webbrick.co.uk/events/diagnostics/software/version', 'WebBrickConfig', { 'build':cfgVersion, 'name':sysName } ) )  

    
class Root(controllers.RootController):

    def __init__( self ):
        self.eventloader = None
        self.homeTemplate = None
        
    def start(self):
        log_versions()
        # TODO         validateTemplateDirectory() on WebBrickGateway.templates
        persistFile = turbogears.config.get("client_profiles", None, False, "gateway" )

        ClientProfiles.load( persistFile )

        self.homeTemplate = turbogears.config.get("homepage", None, False, "gateway" )

        cfgStr = turbogears.config.get("templateDirectory", None, False, "gateway" )
        if cfgStr:
            _log.info( "additional template directory %s" % (cfgStr) )
            validateTemplateDirectory( cfgStr )

            #WbConfigSettings.addTemplateDir( cfgStr )
            sys.path.insert( 1, cfgStr )
            import kid
            _log.info( "Kid Paths %s"  % (str(kid.path.paths)) )
            ### tempdir = tempdir[:-(len(tempsuf)-1)]
            kid.path.insert( cfgStr )
            _log.info( "Kid Paths %s"  % (str(kid.path.paths)) )

        cfgStr = turbogears.config.get("network", None, False, "wbcfg" )
        if cfgStr:
            WbConfigBase.addNetwork( cfgStr )

        cfgStr = turbogears.config.get("webbrickDirectory", None, False, "wbcfg" )
        if cfgStr:
            WbConfigSettings.ConfDir = cfgStr
            _log.info( "updated webbrick configuration directory %s" % (cfgStr) )

        userDir = turbogears.config.get("despatchConfig", None, False, "gateway" )
        sysDir = turbogears.config.get("despatchConfigSystem", None, False, "gateway" )
        self.eventloader = EventRouterLoader()
        # system files first.

        self.eventloader.loadFromDirectories( [sysDir, userDir] )

        #print WbConfigSettings_hga.ConfDir
        #print WbConfigSettings.ConfDir
        
        ###self.panel = PanelRenderer.PanelRenderer()

        self.local       = LocalData.LocalData()
        self.userinterface = UserInterface.UserInterface()

        self.nameCache = Webbrick.WebbrickNodeNameCache()
        self.wbsts = Webbrick.WebbrickStatusCache( self.nameCache )
        self.wbcmd = Webbrick.WebbrickCommand( self.nameCache )
        self.eventstate = EventState.EventState( )
        self.discover = DiscoverHandler()
        self.media = Media.Media()

        # need to handle discovery better
        self.wbcnf = WbCfgManagerForm( self.discover )

        # THIS IS FOR ARMOUR gateway config and discovery only 
        if ARMOUR_DEV:
            self.wbgwcnf = WbGwCfgManager()
        
        self.schedule = Schedule.Schedule()
        self.sendevent = SendEvent.SendEventLocal(self.eventloader.getEventRouter())
        self.wbproxy = Webbrick.WebbrickProxy()

        self.eventstate.start(self.eventloader.getEventRouter())
        
        self.nameCache.start(self.eventloader.getEventRouter())
        self.wbsts.start(self.eventloader.getEventRouter())
        self.discover.start(self.eventloader.getEventRouter())
        self.schedule.start()
        self.media.start(self.eventloader.getEventRouter())
        
        # event handlers last
        if self.eventloader:
            self.eventloader.start()
        
        if not self.eventloader.getEventRouter():
            print "EVENT DESPATCH TASK NOT LOADED/FAILED CONFIGURE"

        _log.info( "Sys Paths %s"  % (sys.path) )

        # Now publish the versions
        router = self.eventloader.getEventRouter()
        publish_versions(router)
        
        
        import kid
        _log.info( "Kid Paths %s"  % (str(kid.path.paths)) )
        _log.warning( "**** System Configured ****" )

    def stop(self):
        """
        helper to shut down some class stuff.
        """
        self.schedule.stop()
        self.discover.stop(self.eventloader.getEventRouter())
        self.wbsts.stop( self.eventloader.getEventRouter() )
        self.nameCache.start( self.eventloader.getEventRouter() )
        self.eventloader.stop()
        self.media.stop(self.eventloader.getEventRouter())

    @turbogears.expose(template="WebBrickGateway.templates.welcome")
    def index(self):
        # look up in client profiles to get homePage.
        if self.homeTemplate:
            result = ClientProfiles.makeStandardResponse( cherrypy.request, self.homeTemplate )
        else:
            result = ClientProfiles.makeStandardResponse( cherrypy.request, "welcome" )
        result["now"] = time.ctime()
        return result

    @turbogears.expose(template="WebBrickGateway.templates.quiet")
    def quiet(self):
        result = ClientProfiles.makeStandardResponse( cherrypy.request )
        return result

    @turbogears.expose(template="WebBrickGateway.templates.listpanels")
    def panels(self):
        result = ClientProfiles.makeStandardResponse( cherrypy.request )

        def selectPanelName((_,nam)): 
            return nam[:-4]

        pattern = re.compile( r'^.+\.xml$' )
        c = CollectFiles("../resources/paneldef/",pattern,recursive=False)
        result['baseuri'] = turbogears.url("/")+"panel/"
        result['panels'] = map(selectPanelName,c)
        return result

    # Serve up media control panel
    @turbogears.expose(template="WebBrickGateway.templates.mediapanel")
    def mediapanel(self, **args):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "mediapanel" )
        # extract any parameters from the URL and add to the dictionary.
        for arg in args:
            result[arg] = args[arg]

        return result

    @turbogears.expose(template="WebBrickGateway.templates.welcome")
    def template(self, *args):
        """
        This function is used to return an arbitrary template used as
        a static page, but wrapped with the common header and footer
        elements.
        """
        # will set tg_template
        result = ClientProfiles.makeStandardResponse( cherrypy.request, string.join(args,'.') )
        if result.has_key("tg_format") and result["tg_format"] == "xml":
            #cherrypy.response.headers['Content-Type'] = "text/xml"
            cherrypy.response.headerMap['Content-Type'] = "text/xml"

        cherrypy.response.headers['Content-Type'] = "text/xml"
        cherrypy.response.headerMap['Content-Type'] = "text/xml"

        return result

    # obsolete, Andy:No actually turns out to be useful for serving files in pure XML format
    @turbogears.expose(template="WebBrickGateway.templates.welcome", format="xml", content_type="text/xml")
    def templatex(self, *args):
        """
        This function is used to return an arbitrary template used as
        a static page, but wrapped with the common header and footer
        elements.
        """
        # will set tg_template
        result = ClientProfiles.makeStandardResponse( cherrypy.request, string.join(args,'.') )

        result["tg_format"] = "xml"
#        result["tg_template"] = 'WebBrickGateway.templates.'+string.join(args,'.')

        cherrypy.response.headerMap['Refresh'] = "30"

        return result
   
    @turbogears.expose(format="manifest", content_type="text/cache-manifest")
    def manifest(self, *args):
        """
        This function is used to return an arbitrary template used as
        a static page, but wrapped with the common header and footer
        elements.
        """
        # get the path where the manifest is stored and serve it as the correct content type
        _log.debug("Requesting manifest for: " + args[0] + "skin")
        manifestpath = pkg_resources.resource_filename("WebBrickRes", "../resources/skins/") + args[0] + "/static/manifest/" + args[0] + ".manifest"
        result = file(manifestpath).read()

        return result
      
    # Serves dataset from siteLogRoot and graph_prop.xml from /static/css
    # as combined Json for use with OpenFlashChart
    # TODO: Move data processing out of controllers
    @turbogears.expose()
    def jsondata(self, logfile = None, propfile = None):
        """
        """
        result = ""
        
        # for debugging only
        # logPath = "/home/webbrick"
        # propPath = "/home/webbrick"
        
        # get the location of log files
        logPath = turbogears.config.get ('siteLogRoot', None, False, 'DEFAULT')
        
        # get the location of css files
        staticRoot = str(turbogears.config.get("static_filter.root", None, False, "global" ))
        staticCss = str(turbogears.config.get("static_filter.dir", None, False, "/static/css" ))
        if staticCss[0] != "/":
            propPath = staticRoot + staticCss
        else:
            propPath = staticCss
        
        
        if logfile and propfile:
            
        
            # does the log folder exist
            if logPath:
                
                # try to read the log file
                try:
                    
                    processeddata = {}
                    
                    xmldatastring = "<entrys>" + "".join(file(logPath + "/" + logfile).readlines()) + "</entrys>"
                    xmldatablob = parseXmlString(xmldatastring)
                    datadict = getDictFromXml(xmldatablob, typecast=True)
                    for item in datadict["entrys"][0]:
                        processeddata[item] = []
                        for entry in datadict["entrys"]:
                            processeddata[item].append(entry[item][0])
                            
                    result = str(processeddata)
                except:
                    _log.error( "log file: %s does not exist on Path: %s" %(logfile, logPath) )    
                
            if propPath:
                
                # try to read the prop file
                try:
                    xmlpropstring = "".join(file(propPath + "/" + propfile).readlines())
                    xmlpropblob = parseXmlString(xmlpropstring)
                    propdict = getDictFromXml(xmlpropblob, typecast=True)
                    propdict = propdict['graphprop']
                    #result = json.dumps(propdict)
                    #result = str(propdict)
                except:
                    _log.error( "log file: %s does not exist on Path: %s" %(propfile, propPath) )
           
            if processeddata and propdict: 
                try:
                    propdict["datasets"] = []
                    for item in processeddata:
                        if item != "time" and item != "date":
                            propdict["datasets"].append({"text": item.replace(".", " "), "values":processeddata.get(item)})
                        elif item == "time":
                            propdict["x_axis"]["labels"]["times"] = processeddata.get(item)
                        elif item == "date":                    
                            propdict["x_axis"]["labels"]["dates"] = processeddata.get(item)
                except:
                    _log.error( "Could not add data to chart" )
                result = json.dumps(propdict)
                
        else:
            _log.error( "Not enough arguments passed to allow processing" )
         
        return result
    
    # Serves dataset from siteLogRoot and graph_prop.xml from /static/css
    # as combined Json for use with OpenFlashChart
    # TODO: Move data processing out of controllers
    @turbogears.expose()
    def jsonfiles(self, filterstr = None):
        """
        """
        result = ""
        
        # get the location of log files
        logPath = turbogears.config.get ('siteLogRoot', None, False, 'DEFAULT')

        filenames = []
        if logPath:
            if filterstr:
                _log.debug( "Filter Filenames using: %s" %(filterstr))
                for filename in listdir(logPath):
                    if filterstr in filename:
                        filenames.append(filename)
            else:
                _log.debug( "No filter string provided - return all filenames")
                for filename in listdir(logPath):
                    filenames.append(filename)
            
            resultdict = {"options":filenames}
            result = json.dumps(resultdict)
        else: 
            _log.error( "No valid siteRootLog" )
        return result                     
        
    
       
    @turbogears.expose()
    def redirect(self,*args):
        """ 
        generalised redirect, so Gateway can manage locations of cameras etc.
        The URLs returned may be changed dependant on whether client on local network or not
        """
        cfgStr = turbogears.config.get(args[0], None, False, "redirect" )
        if cfgStr:
            raise cherrypy.HTTPRedirect(cfgStr)
        return self.index()

    #@turbogears.expose()
    def default(self,*args):
        return self.panels()

