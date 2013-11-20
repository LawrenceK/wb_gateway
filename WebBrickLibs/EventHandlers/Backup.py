# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle UDP
#
#  Lawrence Klyne
#
# netifaces.ifaddresses( netifaces.interfaces()[0] )[netifaces.AF_LINK][0]['addr']
#
import logging
import httplib
import ftplib
import re
import base64
from tempfile import mkstemp
from glob import glob

from time import gmtime, time

import os
from os import fdopen, popen
from os import listdir, walk, remove
from os.path import join, abspath, isfile, getmtime, split
from zipfile import *

from StringIO import StringIO

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler

_log = None

class BackupFile:
    """
    Perform file backup.

    <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    """
    def __init__ (self, cfg):
        self._transportType = cfg['transport']
        self._nameTemplate = cfg['nameTemplate']
        self._directory = list()
        self._validfordays = list()
        
        if cfg.has_key('path'):
            self._directory = cfg['path']
        else: 
            self._directory = split(self._nameTemplate)[0]
            _log.debug( 'Backup directory not explicitly specified, using: %s' %(self._directory)  )
            
        if cfg.has_key('deleteAfterDays'):
            self._validfordays = int(cfg['deleteAfterDays'])
        else: 
            self._validfordays = 7
            _log.debug( 'deleteAfterDays not defined defaulted to 7 days' )
            
            
        _log.debug( 'nameTemplate %s' % (self._nameTemplate) )

    def getTransportType( self ): 
        return (self._transportType)
       
    def doSave( self, data, par ):
        # create filename
        fname = abspath(self._nameTemplate % par)
        fdir = os.path.split(fname)[0]    # access directory
        if not os.path.exists(fdir):
            # make it.
            os.makedirs(fdir)
        if os.path.isdir(fdir):
            _log.debug( 'save to %s' % (fname) )
            # save
            f = file( fname, 'wb' )
            f.write( data )
            f.close()
        else:
            _log.error( 'Unable to save to %s (cannot create directory or not a directory)' % (fname) )

            
    def doCleanUp(self):
        # check if backup directory contains archivedlog files with a timestamp older than self._validfordays adn removes them
        # due to the delete checks performed the maximum number of days logs can be kept is 30. 
        _log.debug( 'doCleanUp for: %s called' % self._directory )
        # get current time since epoch
        epoch = gmtime(0)
        ctime = time()
        
        
        for fn in os.listdir(self._directory):
            file = join(self._directory, fn)
            ftime = getmtime(file)
            temptime = gmtime(ctime - ftime)
            deltatime = list()
            for i in range(9):
                deltatime.append(temptime[i] - epoch[i])
            _log.debug( '%s is %s days old.' % (fn, deltatime[2]) )
            if deltatime[2] > self._validfordays:
                _log.debug( 'Removing file: %s' % fn )
                os.remove(file)
            elif deltatime[1] >  0:
                _log.debug( 'Removing file: %s' % fn )
                os.remove(file)
            elif deltatime[0] >  0:
                _log.debug( 'Removing file: %s' % fn )
                os.remove(file)
                
           
class BackupHttpS:
    """
    Perform SFTP transfer
        <destination transport="https" address="<template https URL>">
    """
    def __init__ (self, cfg):
        self._transportType = cfg['transport']
        self._targetAddress = cfg['address']
        self._nameTemplate = cfg['nameTemplate']
        self._authHdrs = {}
        self._password = None
        if cfg.has_key("username") and cfg.has_key("password"):
            self._authHdrs["Authorization"] = "Basic %s" % base64.b64encode( "%s:%s" % (cfg["username"],cfg["password"]) )

        _log.debug( '_targetAddress %s' % (self._targetAddress) )
        _log.debug( '_nameTemplate %s' % (self._nameTemplate) )

    def getTransportType( self ): 
        return (self._transportType)
        
    def doSave( self, data, par ):
        fname = self._nameTemplate % par
        # Create HTTPS connection
        # perform PUT.
        #TODO use dual keys so we need to identify as well as server?

        _log.debug( '_targetAddress %s - URL %s' % (self._targetAddress, fname) )
        conn = httplib.HTTPSConnection( self._targetAddress )
        # Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
        conn.request('PUT', fname, data, self._authHdrs )
        response = conn.getresponse()
#        if response.status == 401:
            # retry with authentication

        responseData = response.read()
        _log.debug( "%s:%s %s %s - %s" %( response.status, response.msg, response.reason, response.getheaders(), responseData ) )

class BackupSftp:
    """
    Perform SFTP transfer
        <destination transport="sftp" address="backup.webbrick.co.uk">
    """
    def __init__ (self, cfg):
        self._transportType = cfg['transport']
        self._targetAddress = cfg['address']
        _log.debug( '_targetAddress %s' % (self._targetAddress) )

    def getTransportType( self ): 
        return (self._transportType)
        
    def doSave( self, data, par ):
        pass    

class BackupFtp:
    """
    Perform FTP transfer
        <destination transport="ftp" address="backup.webbrick.co.uk">
    """
    def __init__ (self, cfg):
        self._transportType = cfg['transport']
        self._targetAddress = cfg['address']
        self._nameTemplate = cfg['nameTemplate']
        self._username = cfg['username']
        self._password = cfg['password']
        # temporary setup to default to WebBrick FTP server, need to do this properly with DNS lookup.
        if self._targetAddress == "backup.webbrick.co.uk":
            self._targetAddress = "195.26.42.82"
            self._username = "webbrick.gateway"
            self._password = "gatewayupload"
        _log.debug( '_targetAddress %s', self._targetAddress)

    def getTransportType( self ): 
        return (self._transportType)   
        
    def doSave( self, data, par ):
        _log.debug( 'ftp doSave %s', self._targetAddress)
        fname = self._nameTemplate % par
        # parse into directory and local part
        (rem_path,rem_name) = split(fname)
        ftp = ftplib.FTP(self._targetAddress)
        ftp.login(self._username,self._password)
        # change directory
        ftp.cwd( rem_path )
        ftp.storbinary( "STOR %s" %(rem_name), StringIO(data) )
        ftp.quit()

class BackupCommandLine:
    """
    Perform command line
        <destination cmdTemplate="scp --user --password %(fromName)s %(toName)s">
    """
    def __init__ (self, cfg):
        self._transportType = cfg['transport']
        self._cmdTemplate = cfg['cmdTemplate']
        _log.debug( 'cmdTemplate %s', self._cmdTemplate)

    def getTransportType( self ): 
        return (self._transportType)        
 
    def doSave( self, data, par ):
        _log.debug( 'command line doSave %s', self._cmdTemplate)

        fd,fname = mkstemp()
        f = fdopen(fd, "w")
        _log.debug( 'save to %s' % (fname) )
        # save
        f.write( data )
        f.close()

        params = dict(par)
        params['localname'] = fname
        _log.debug( 'params %s', params)

        fullCmd = self._cmdTemplate % params
        _log.debug( 'full command %s', fullCmd)

        op = popen( fullCmd )
        if op:
            res = op.readlines()
            rcode = op.close()
            _log.debug( 'output %s %s', res, rcode)
        else:
            _log.error( 'error starting %s', fullCmd)
        # delete temporary file
        remove( fname )

class ActiveSaveSet:
    """
    A save in progress
    """
    def __init__ (self, absoluteNames, timeStamps ):
        self.saveAbsoluteFileNames = absoluteNames
        self._zipstr = StringIO()
        self._currentZip = ZipFile(self._zipstr, mode='w', compression=ZIP_DEFLATED)
        self._timeStamps = timeStamps
        self._count = 0

    def add(self, fnfull, fn, addAlways = True ):
        # return True if added
        if addAlways or not self._timeStamps.has_key(fnfull) or self._timeStamps[fnfull] <> getmtime(fnfull):

            self._timeStamps[fnfull] = getmtime(fnfull)

            if self.saveAbsoluteFileNames:
                _log.debug( 'add file "%s"' % (fnfull) )
                self._currentZip.write(fnfull)
            else:
                _log.debug( 'add file "%s" "%s"' % (fn, fnfull) )
                self._currentZip.write(fnfull,fn)
            self._count = self._count + 1
            return True
        return False

    def close(self):
        result = None
        self._currentZip.close()
        self._currentZip = None

        if self._count > 0:
            result = self._zipstr.getvalue()

        self._zipstr.close()
        self._zipstr = None

        return result
#        return (result,self._timeStamps)

#    def getTimestamps(self):
#        return self._timeStamps

class SaveSet:
    """
    Configuration of a save set

        <fileSet rootpath="" absolutenames="yes|no">
            <!-- if path does not start with then it is assumed to be relative to rootpath -->
            <file path="">
            <directory path="" recursive="yes|no">
            <exclude match="">
        </fileSet>
    """

    def addFile(self, cfgA):
        _log.debug( 'addFile %s' % (cfgA) )
        self._files.append( join( str(self.rootpath), str(cfgA['path']) ) )

    def addDir(self, cfgD):
        _log.debug( 'addDir %s' % (cfgD) )
        self._directories.append( (join( str(self.rootpath), str(cfgD['path'])), cfgD.has_key('recursive') and cfgD['recursive'] == 'yes' ) )

    def addExclude(self, cfgE):
        _log.debug( 'addExclude %s' % (cfgE) )
        # compile it
        if cfgE.has_key("match"):
            self._exclude.append( re.compile(cfgE["match"]) )

    def checkExclude(self, fname):
        # check the exclude fileset and identify whether excluded from the save set.
        for ex in self._exclude:
            # if match
            if ex.match(fname):
                return True
        return False

    def __init__ (self, cfg):

        self._currentZip = None
        self._timeStamps = dict()   # what we backed up last time
        self._files = list()
        self._directories = list()
        self._exclude = list()
        self._deleteAfter = False

        # first generic details
        if cfg.has_key('deleteAfter'):
            self._deleteAfter = cfg['deleteAfter'] == "yes"

        if cfg.has_key('rootpath'):
            self.rootpath = cfg['rootpath']
        else:
            self.rootpath = ''

#        self.basePath = path.abspath(self.basePath)

        self.saveAbsoluteFileNames = cfg.has_key('absolutenames') and cfg['absolutenames'] == 'yes'
            # convert self.basePath to absolute form

        # now component sets.
        if cfg.has_key('file'):
            # one or more distinct files
            if isinstance( cfg['file'], list ):
                for fn in cfg['file']:
                    self.addFile(fn)
            else:
                self.addFile(cfg['file'])

        
        if cfg.has_key('directory'):
            # one or more directories
            if isinstance( cfg['directory'], list ):
                for fn in cfg['directory']:
                    self.addDir(fn)
            else:
                self.addDir(cfg['directory'])
        
        if cfg.has_key('exclude'):
            # one or more excludes
            if isinstance( cfg['exclude'], list ):
                for fn in cfg['exclude']:
                    self.addExclude(fn)
            else:
                self.addExclude(cfg['exclude'])

        _log.debug( 'rootpath %s absolute %s' % (self.rootpath, self.saveAbsoluteFileNames) )
        _log.debug( 'files %s' % (self._files) )
        _log.debug( 'directories %s' % (self._directories) )

    def hasChanges(self):
        """
        see whether any changes since last backup.
        """
        _log.debug( 'hasChanges' )

        for fnf, fna in self.walkSaveSet() :
            if not self._timeStamps.has_key(fna):
                return True
            if self._timeStamps[fna] <> getmtime(fna):
                return True
        return False

    def walkSaveSet( self ):
        """
        Generator function to walk the save set
        """

        for fn in self._files:
            fnf = join(self.rootpath,fn)
            for sfn in glob(fnf):
                fna = abspath( sfn )
                if not self.checkExclude(fna):
                    yield sfn,fna    # yield the full path and the absolute path
                else:
                    _log.debug( 'Exclude %s', fna )

        for dr in self._directories:
            _log.debug( 'directories "%s" %s' % (dr[0], dr[1]) )
            # dr[0] is name and dr[1] is recursive flag
            if dr[1]:
                # recursive
                pfxLen = len(dr[0])
                if dr[0][-1] <> '/' and dr[0][-1] <> '\\':
                    pfxLen = pfxLen + 1 # because we will have an additional path separator

                for root, dirs, files in walk(dr[0]):
                    _log.debug( 'root %s sub dirs %s files %s' % (root, dirs, files) )
                    files.sort()
                    for fn in files:
                        fnf = join(root, fn)
                        fna = abspath(fnf)
                        if not self.checkExclude(fna):
                            # now loose the start point from fnf
                            fnf = fnf[pfxLen:]
                            yield fnf,fna
                        else:
                            _log.debug( 'Exclude %s', fna )
            else:
                files = listdir(dr[0])
                files.sort()
                for fn in files:
                    fnf = join(dr[0], fn)
                    fna = abspath(fnf)
                    if not self.checkExclude(fna):
                        _log.debug( 'file "%s"' % (fna) )
                        if isfile( fna ):
                            yield fn,fna
                    else:
                        _log.debug( 'Exclude %s', fna )

    def getSaveSet(self, allFiles = True):
        """
        get a save set for this 
        AllFiles is False for a Delta
        """
        deleteNames = list()
        zf = ActiveSaveSet(self.saveAbsoluteFileNames, self._timeStamps)

        for fnf, fna in self.walkSaveSet() :
            if zf.add(fna, fnf, allFiles) and self._deleteAfter:
                # delete once written
                deleteNames.append(fna)

#        result, self._timeStamps = zf.close()
        zipData = zf.close()

        # now clean up the unwanted files.
        for fna in deleteNames:
            remove(fna)

        return zipData

#
# WebBrick eggnunciate driver
#
class BackupHandler( BaseHandler ):
    """
    This handler generates zipped back up file sets and then 'saves' them some where.

    The configuration for this event handler is as follows

    <eventInterface module='EventHandlers.BackupHandler' name='BackupHandler`'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name="minute">
                            <value>1</value>
                        </testEq>
                    </params>
                    <!-- Check for changes to files in backup set -->
                    <checkBackup/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet rootpath="" absolutenames="yes|no" basename="">
            <!-- if path does not start with then it is assumed to be relative to rootpath -->
            <file path="">
            <directory path="" recursive="yes|no">
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="sftp" address="backup.webbrick.co.uk">
        </destination>

        <destination transport="ftp" address="backup.webbrick.co.uk">
        </destination>

        <destination transport="file" directory="/opt/webbrick/backup">
        </destination>

    </eventInterface>

    """

    def __init__ (self, localRouter):
        super(BackupHandler,self).__init__(localRouter)
        global _log
        _log = self._log

    def configureActions( self, eventDict ):
        result = list()
        if eventDict.has_key( 'checkFull' ):
            result.append( 'checkFull' )
        elif eventDict.has_key( 'checkDelta' ):
            result.append( 'checkDelta' )
        elif eventDict.has_key( 'doFull' ):
            result.append( 'doFull' )
        elif eventDict.has_key( 'cleanUp' ):
            result.append( 'cleanUp' )
        else:
            # not recognised
            pass
        return result

    def addDestination( self, cfgD ):
        if cfgD['transport'] == 'file':
            self._destinations.append(BackupFile(cfgD))
        elif cfgD['transport'] == 'https':
            self._destinations.append(BackupHttpS(cfgD))
        elif cfgD['transport'] == 'ftp':
            self._destinations.append(BackupFtp(cfgD))
        elif cfgD['transport'] == 'commandline':
            self._destinations.append(BackupCommandLine(cfgD))
#        elif cfgD['transport'] == 'sftp':
#            self._destinations.append(BackupSftp(cfgD))
        else:
            # unknown destination
            pass

    def configure( self, cfgDict ):
        super(BackupHandler,self).configure( cfgDict )

        self._fileSets = list()
        self._destinations = list()
        self._backupdirectories = list()

        if cfgDict.has_key("fileSet"):
            if isinstance( cfgDict["fileSet"], list ):
                for fs in cfgDict["fileSet"]:
                    self._fileSets.append(SaveSet(fs))
            else:
                self._fileSets.append(SaveSet(cfgDict["fileSet"]))
        else:
            _log.error( "No filesets defined for backup" )

        if cfgDict.has_key("destination"):
            if isinstance( cfgDict["destination"], list ):
                for ds in cfgDict["destination"]:
                    self.addDestination( ds )
            else:
                self.addDestination( cfgDict["destination"] )
        else:
            _log.error( "No destinations defined for backup" )
            
               

    def doFullBackup( self, inEvent ):
        # for each saveSet, generate zip
        for fs in self._fileSets:
            zp = fs.getSaveSet()
            if zp:
                for ds in self._destinations:
                    ds.doSave( zp, inEvent.getPayload() )

    def doFullDeltaBackup( self, inEvent ):
        # for each saveSet, generate complete zip if any changes to the backup.
        for fs in self._fileSets:
            if fs.hasChanges():
                zp = fs.getSaveSet()
                if zp:
                    for ds in self._destinations:
                        ds.doSave( zp, inEvent.getPayload() )

    def doDeltaBackup( self, inEvent ):
        # for each saveSet, generate zip of only changes to the backup
        for fs in self._fileSets:
            zp = fs.getSaveSet( False ) # delta
            if zp:
                for ds in self._destinations:
                    ds.doSave( zp, inEvent.getPayload() )
                    
    def doCleanUp( self, inEvent ):
        # for each local backup desitnation check that 
        # Note only supports local backups, i.e. transport = 'file'
        for ds in self._destinations:
            
            if ds.getTransportType() == 'file':
                ds.doCleanUp()

    def doActions( self, actions, inEvent ):

        _log.debug( 'doActions %s' % (actions) )
        for action in actions:
            try:
                if ( action == "doFull" ):
                    self.doFullBackup( inEvent )
                elif ( action == "checkFull" ):
                    self.doFullDeltaBackup( inEvent )
                elif ( action == "checkDelta" ):
                    self.doDeltaBackup( inEvent )
                elif ( action == "cleanUp" ):
                    self.doCleanUp( inEvent )
                    

            except Exception, ex:
                _log.exception( "doActions %s" % str(action) )
