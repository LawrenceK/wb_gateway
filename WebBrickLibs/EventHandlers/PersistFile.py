# $Id: PersistFile.py 3735 2010-09-29 12:55:52Z tombushby $
#
#  Class to handle event actions that are implemented as an HTTP request.
#
#  Lawrence Klyne
#
#
import logging
from os.path import join, split, abspath, exists
from os import rename, remove

from shutil import copy

import threading
import time

from xml.sax.saxutils import escape, unescape

from MiscLib.DomHelpers          import *

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred
#from EventLib.EventSerializer import parseSubscribeData
from EventHandlers.BaseHandler import BaseHandler

_log = logging.getLogger( "EventHandlers.PersistFile" )

class PersistFile( BaseHandler ):
    """
    Handle events saving persistant configuration and distribute configuration.
    <eventInterface module='PersistFile' name='PersistFile' persistFile='./persist>
    </eventInterface>
    """

    def __init__ (self, localRouter):
        self._log = _log
        super(PersistFile,self).__init__(localRouter)
        self._isUpdate = False
        self._commit_delay = 0
        self._commit_time_since_original = 0
        self._commit_max_delay = 20
        self._commit_default_delay = 5
        self._subscribeTime = 30
        self._locked = threading.Lock()


    def configure( self, cfgDict ):
        """
        called with a dictionary that contains the configuration for self
        """
        _log.debug( 'configure' )
        # need persistFile
        if cfgDict.has_key('persistFile'):
            self._persistFile = cfgDict['persistFile']
            if not self._persistFile.lower().endswith( ".xml" ):
                # force extension
                self._persistFile = "%s.xml" % (self._persistFile)
            self._persistFile = abspath(self._persistFile)
            
            
            
            # if file does not exists then try to recover it from .bak file
            if not exists(self._persistFile):
                if exists(self._persistFile+'.bak'):
                    if exists(self._persistFile+'.restore'):
                        remove(self._persistFile+'.restore')
                    copy( self._persistFile+'.bak', self._persistFile+'.restore' )
                    rename(self._persistFile+'.restore', self._persistFile)
                    _log.debug('Persistant file recovered from - %s' % (self._persistFile+'.bak') )
                
                elif exists(self._persistFile+'.daily'):
                    if exists(self._persistFile+'.restore'):
                        remove(self._persistFile+'.restore')
                    copy( self._persistFile+'.daily', self._persistFile+'.restore' )
                    rename(self._persistFile+'.restore', self._persistFile)
                    _log.debug('Persistant file recovered from - %s' % (self._persistFile+'.daily') )
                    
            _log.debug( 'Persist file is %s', self._persistFile)
        else:
            _log.error('Configuration does not contain name of file to save persistant data to. %s' % (cfgDict) )

    def addEntry(self, ntry):
        if ntry.has_key( 'source' ) and ntry.has_key( 'value' ):
            if self._xRef.has_key(ntry['source']):
                # duplicate
                _log.error('Persist entry allready exists. %s' % (ntry) )
                # really need to clean up, suggests bug somewhere
            else:
                # locate values and generate od.
                od = dict()
                vals = ntry['value']
                if not isinstance( vals, list ):
                    # turn into list, easier later during update
                    ntry['value'] = list()
                    ntry['value'].append(vals)
                    vals = ntry['value']
                for v in vals:
                    od[v['name']] = v['']
                self._xRef[ntry['source']] = od
        else:
            _log.error('Persist entry missing name or value. %s' % (ntry) )

    def start(self):
        _log.debug( 'start' )
        self.__running = True

        self._xRef = dict()
        if exists(self._persistFile):
            # load persist file and build cross ref.
            self._persistData = getDictFromXmlFile( self._persistFile )
            # locate root entry
            if self._persistData.has_key( 'persist' ):
                if self._persistData['persist'].has_key( 'entry' ):
                    entry = self._persistData['persist']['entry']
                    if not isinstance( entry, list ):
                        # turn into list, easier later during update
                        self._persistData['persist']['entry'] = list()
                        self._persistData['persist']['entry'].append( entry )
                        entry = self._persistData['persist']['entry']
                    for ntry in entry:
                        self.addEntry(ntry)
            else:
                # error no root entry
                _log.error('Configuration data invalid no persist entry. %s' % (self._persistData) )
            
            for k in self._xRef:
                _log.debug( "Persist loaded %s - %s" % (k,self._xRef[k]) )
        else:
            _log.error( "No Persist data : %s", self._persistFile)
            self._persistData = {'persist':{}}

        # subscribe to subscribe events so we can see new subscriptions to get
#        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/subscribe', '' )
        self._localRouter.watch( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/config/get' )

        # subscribe to set so we can update persist data
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/runtime' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/config/set' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/minute' )
        self._localRouter.subscribe( self._subscribeTime, self, 'http://id.webbrick.co.uk/events/time/second', 'time/second' )

    def stop(self):
        _log.debug( 'stop' )
        self.__running = False
        self._localRouter.endWatch( self, 'http://id.webbrick.co.uk/events/config/get' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/config/set', '' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/runtime', '' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/minute' )
        self._localRouter.unsubscribe( self, 'http://id.webbrick.co.uk/events/time/second', 'time/second' )

    def commitCountdown( self ):
        # commits are now based on a timer or "countdown".
        # this means that a timer is reset on every new persist event, and when
        # it reaches 0, the persist events are all written to disk
        if (self._commit_delay > 0):
            _log.debug('Commit countdown executing; commit delay:%s ' % self._commit_delay)
            self._commit_delay = self._commit_delay - 1
            
            # ++ causes syntax issues, annoying python
            self._commit_time_since_original = self._commit_time_since_original + 1
        
            if self._commit_delay == 0 or self._commit_time_since_original >= self._commit_max_delay:
                
                # if after 20 seconds changing are still happening, write anyway
                if self._commit_time_since_original >= self._commit_max_delay:
                    _log.error("Persist data rate high, please consider refusing your usage")
                
                # reset original counter
                self._commit_time_since_original = 0
                self._commit_delay = 0
                
                # now commit change
                _log.debug("Committing persistent change to disk")
                self.commitChange()

    def commitChange( self ):
        # write persist to Xml file.
        while not self._locked.acquire():
            _log.info( "Already writing persisted data " )
            time.sleep(0.5)  
        xmlDom = getXmlDomFromDict( self._persistData )
        _log.debug( "Xml %s" % (getElemPrettyXml(xmlDom)) )
        saveXmlToFilePretty( self._persistFile , xmlDom )
        self._locked.release()

    def doDailyBackup( self ):
        # creates DailyBackup of the persisted data file
        while not self._locked.acquire():
            _log.info( "Already writing persisted data " )
            time.sleep(0.5)  
        xmlDom = getXmlDomFromDict( self._persistData )
        _log.debug( "Xml %s" % (getElemPrettyXml(xmlDom)) )
        saveXmlToFilePretty( self._persistFile+'.daily', xmlDom )
        self._locked.release()    
        
    def handleSet( self, inEvent ):

        es = inEvent.getSource()
        if not self._xRef.has_key( es ):
            # create new.
            od = dict()
            self._xRef[es] = od
        od = self._xRef[es]

        # locate entry in persist
        vals = None
        if self._persistData['persist'].has_key('entry'):
            entries = self._persistData['persist']['entry']
            for ntry in entries:
                if ntry['source'] == es:
                    vals = ntry['value']
        else:
            self._persistData['persist']['entry'] = list()
            entries = self._persistData['persist']['entry']

        if vals == None:
            # create new persist entry
            vals = list()
            entries.append( {'source':es, 'value' : vals } )

        for k in inEvent.getPayload():
            nv = inEvent.getPayload()[k]
                        
            if not od.has_key(k) or od[k] != nv:
                _log.debug("The commit delay has been reset to: %s" % self._commit_default_delay)
                self._commit_delay = self._commit_default_delay
                # self._isUpdate = self._isUpdate or not od.has_key(k) or od[k] != nv
            od[k] = nv
            fnd = False
            for v in vals:
                if v['name'] == k:
                    v[''] = nv
                    fnd = True
            if not fnd:
                vals.append( { 'name':k, '':nv} )

        # Replaced by commitCountdown
        # TODO may leave for a short while before writing.
        #        if self._isUpdate:
        #            self.commitChange()        
        
        # let everyone know
        self.sendEvent( Event( "http://id.webbrick.co.uk/events/config/get", 
            es, dict(self._xRef[es]) ) )    # copy other data as we may update

    def doPublish( self, es ):
        """ send data for the subscribed event source """
        if es == "" or es == None:
            # wildcard subscribe send all persist data
            for k in self._xRef:
                self.sendEvent( Event( "http://id.webbrick.co.uk/events/config/get", 
                    k, dict(self._xRef[k]) ) )
        else:
            # locate and send correct data
            if self._xRef.has_key(es):
                # send event
                self.sendEvent( Event( "http://id.webbrick.co.uk/events/config/get", 
                    es, dict(self._xRef[es]) ) )

    def handleSubscribe( self, inEvent ):
        """ If to one of our events resend relevant data """
        sd = inEvent.getPayload()
#        sd = parseSubscribeData( inEvent.getPayload() )

        _log.debug( 'handleSubscribe %s' % ( sd ) )

        """
        When subscriptions are received they could be wild carded by providing blank eventType or eventSource
        so we need to check for these
        """
        if sd and (sd[0] > 0):
            et = sd[1]
            es = sd[2]
            if (et == "http://id.webbrick.co.uk/events/config/get") or (et == "") or (et == None):
                self.doPublish(es)

    def doHandleEvent( self, handler, inEvent ):
        # handle commit using self._commit_delay
        if inEvent.getType() == "http://id.webbrick.co.uk/events/time/minute" :
            # Chose 19.05 since at this time most heating will be on, hence if gateway fals over and uses 24hr backup heatign will be on! 
            if int(inEvent.getPayload()["hour"]) == 19 and int(inEvent.getPayload()["minute"]) == 5:
                self.doDailyBackup()
    
        elif inEvent.getType() == "http://id.webbrick.co.uk/events/config/set" :
            self.handleSet( inEvent )

        elif inEvent.getType() == "http://id.webbrick.co.uk/events/subscribe" :
            self.handleSubscribe( inEvent )

        elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/second":
            self.commitCountdown()

        elif inEvent.getType() == "http://id.webbrick.co.uk/events/time/runtime" :
            if int(inEvent.getPayload()["elapsed"]) == 5:
                self.doPublish("")  # publish all the data.

        return makeDeferred(StatusVal.OK)

# End.       
# $Id: PersistFile.py 3735 2010-09-29 12:55:52Z tombushby $
