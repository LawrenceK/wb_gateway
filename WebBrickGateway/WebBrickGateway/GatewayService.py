# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

import win32serviceutil, win32service
import pywintypes, win32con, winerror
import servicemanager

import thread
import time

from os.path import normcase

from WebBrickGateway.main import start, stop
from MiscLib.DomHelpers import parseXmlFile

configKey = "ConfigurationFile"

def ApplyIgnoreError(fn, args):
    try:
        return apply(fn, args)
    except error: # Ignore win32api errors.
        return None

class GatewayService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WebBrick Gateway"
    _svc_display_name_ = "WebBrick Gateway"
    _svc_description_ = "WebBrick Gateway Service."

    def __init__(self, args):
        self._svc_configFile_ = None
        win32serviceutil.ServiceFramework.__init__(self, args)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        stop()

    def SvcDoRun(self):
        # Write an event log record - in debug mode we will also
        # see this message printed.
        servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
                )

        # attempt to retrieve comnfig file name
        self._svc_configFile_ = win32serviceutil.GetServiceCustomOption(
                GatewayService._svc_name_,
                configKey,
                self._svc_configFile_ )

        servicemanager.LogInfoMsg(
                "User configuration file %s"% (self._svc_configFile_)
                )

        start( self._svc_configFile_ )

        # Write another event log record.
        servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STOPPED,
                (self._svc_name_, "")
                )

def customOptionHandler(opts):
    #This is only called when the service is installed.
    fFoundConfigFile = 0
    for opt, val in opts:
        if opt == "-c":
            # This installs the location of the configuration file:
            win32serviceutil.SetServiceCustomOption(
                GatewayService._svc_name_,
                configKey,
                normcase(val.strip()) )
            fFoundConfigFile = 1
#    if not fFoundConfigFile:
#        print "Error: You forgot to pass in a path to your logging configuration file., use the '-c' option."
#        raise ConfigFileNotFound

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(
        GatewayService,
        customInstallOptions = "c:",
        customOptionHandler = customOptionHandler )
        
