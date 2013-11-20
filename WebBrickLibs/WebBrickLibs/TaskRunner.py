# $Id: TaskRunner.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# TaskRunner class definition
#

import sys
import string
import time
import logging, logging.config
from logging.config import fileConfig

from MiscLib.DomHelpers import *

CONFIG_FILE = "./TaskRunner.xml"
_log = logging.getLogger( "WebBrickLibs.TaskRunner" )

class TaskRunner:
    """
    This class creates and controls small tasks of work, a task is a separate class 
    that implements start, stop and configure.  The lists of tasks is currently 
    provided with an XML DOM configuration.
    
    The aim is that we can run lots of small simple tasks in a single process. 
    At task should keep running until told otherwise.
    """
    def __init__( self ):
        self._tasks = dict()

    # Helper to load a task.
    def importExtension( self, modulename, name ):
        try :
            # need to update to allow package name in config file
            _log.debug( 'attempting to load %s from %s' %(name, modulename) )
            newModule = __import__( modulename, globals(), locals(), [name] )
            _log.debug('loaded ' + modulename )
        except Exception, ex:
            _log.exception( ex )
            return None
        return getattr( newModule, name )()

    def configure( self, xmlDom ):
        """
        called with an XmlDom that contains the configuration for the task runner.
        It looks for its configuration in the provided Xml DOM and then creates the
        required python object using the provided module and class name.

        This new object is then configured as well, the task should not start being active
        until start is called.
        """
        myDom = getNamedElem( xmlDom, "TaskRunner" )
        logCfg = getAttrText( myDom, "logCfg" )
        if logCfg:
            fileConfig( logCfg )
        else:
            doDebug = getAttrText( myDom, "debug" )
            if doDebug == 'debug':
                logging.basicConfig(level=logging.DEBUG)
                _log.debug( 'debugging' )
            else:
                logging.basicConfig(level=logging.INFO)

        tasks = myDom.getElementsByTagName('Task')
        for task in tasks:
            # create and configure.
            moduleName = getAttrText( task, "module" )
            name = getAttrText( task, "name" )
            newTask = self.importExtension( moduleName, name )
            if newTask:
                newTask.configure( task )
                self._tasks[name] = newTask
                _log.info('loaded %s:%s' % (moduleName, name) )

    def start( self ):
        """
        call start on all configured tasks
        """
        for task in self._tasks:
            self._tasks[task].start()

    def stop( self ):
        """
        call stop on all configured tasks
        """
        for task in self._tasks:
            self._tasks[task].stop()

def main():
    runner = TaskRunner()
    args = sys.argv[1:]
    if args and args[0]:
        runner.configure( parseXmlFile( args[0] ) )
    else:
        runner.configure( parseXmlFile( CONFIG_FILE ) )
    runner.start( )

    try:
        print( "type exit or ^C and <Enter> to quit" )
        while sys.stdin.readline().find("exit") < 0 :
            print "type exit or ^C"
    except KeyboardInterrupt:
        pass
    print( "Shutdown in progress" )

    runner.stop()
    print( "Shutdown complete" )

if __name__ == "__main__":
    main()
