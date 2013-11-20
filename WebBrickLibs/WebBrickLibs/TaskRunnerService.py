import win32serviceutil, win32service
import pywintypes, win32con, winerror
import servicemanager

import thread
import time

from WebBrickLibs.TaskRunner import TaskRunner
from MiscLib.DomHelpers import parseXmlFile

def ApplyIgnoreError(fn, args):
    try:
        return apply(fn, args)
    except error: # Ignore win32api errors.
        return None

class TaskRunnerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TaskRunner"
    _svc_display_name_ = "Webbrick Gateway TaskRunner"
    _svc_description_ = "Acts as a host for python tasks."

    def __init__(self, args):
        self._svc_configFile_ = "TaskRunner.xml"
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.running = False
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        self.taskRunner.stop()

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
                TaskRunnerService._svc_name_,
                "TaskConfigurationFile",
                self._svc_configFile_ )

        # Create the active object.
        self.taskRunner = TaskRunner()
        self.taskRunner.configure( parseXmlFile( self._svc_configFile_ ) )
        self.taskRunner.start()
        self.running = True

        while self.running:
            # it is all on deamon threads
            time.sleep(1)   

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
                TaskRunnerService._svc_name_,
                "TaskConfigurationFile",
                val)
            fFoundConfigFile = 1
    if not fFoundConfigFile:
        print "Error: You forgot to pass in a path to your logging configuration file., use the '-c' option."
        raise ConfigFileNotFound

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(
        TaskRunnerService,
        customInstallOptions = "c:",
        customOptionHandler = customOptionHandler )
        
