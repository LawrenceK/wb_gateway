# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle commands going to the system shell
#
#  Lawrence Klyne
#
#  Extended by Andy Harris to include string substitutions 26th Jan 2009
#
#
import logging, subprocess

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

_log = logging.getLogger( "EventHandlers.ShellAction" )

#
# WebBrick time event generator
#
class ShellAction( BaseHandler ):
    """
    Handle events targetting urls
    """

    def __init__ (self, localRouter):
        self._log = _log
        super(ShellAction,self).__init__(localRouter)

    def configureActions( self, cfgDict ):
        result = None
        if cfgDict.has_key("command"):
            if isinstance( cfgDict["command"], list ):
                result = cfgDict["command"]
            else:
                result = list()
                result.append(cfgDict["command"])
        return result

    def doActions( self, actions, inEvent ):
        if actions:
            for action in actions:
                try:
                    cmd = action['cmd']
                    param = action['params']
                    # has uri got any % symbols in it, attempt substitution
                    if inEvent.getPayload() and '%' in param:
                        # the params can contain string substitutions of the form %(key)s where
                        # the key is a key into other_data, the s is the string specifier.
                        # See String Formatting Operations in the python library ref.
                        param = param % inEvent.getPayload()

                    _log.info("shell command: %s param: %s" % (cmd, param) )
                    subprocess.Popen( param,shell=True )
                except Exception, ex:
                    _log.exception( ex )

