# $Id: TestBackup.py 3066 2009-02-17 14:34:37Z philipp.schuster $
#
# Unit testing for WebBrick library functions
# See http://pyunit.sourceforge.net/pyunit.html
#

import sys, logging, time
import unittest
import os
from os.path import isfile
from shutil import copyfile
import zipfile
from string import join

from MiscLib.DomHelpers  import *

from EventLib.Event import Event, makeEvent

from EventHandlers.BaseHandler import *
from EventHandlers.EventRouterLoad import EventRouterLoader

import EventHandlers.tests.TestEventLogger as TestEventLogger

import Events
from Utils import *

_log = logging.getLogger( "TestBackupHandler" )

# filenames of test data
testdata1 = "./work/file1.txt"
testdata2 = "./work/file2.txt"
testdata3 = "./work/file1_delete.txt"

workDir =  "./work"
sourceDir =  "./resources/testbackup"
outputDir =  "./TestOut"

# filenames for backups.
fname01 = "./TestOut/bu_20070203T040100.zip"
fname02 = "./TestOut/bu_20070203T040200.zip"
fname03 = "./TestOut/bu_20070203T040300.zip"
fname04 = "./TestOut/bu_20070203T040400.zip"
fname05 = "./TestOut/bu_20070203T040500.zip"
fname06 = "./TestOut/bu_20070203T040600.zip"
fname10 = "./TestOut/bu_20070203T041000.zip"

fname01sd = "./TestOut/20070203/bu_040100.zip"
fname02sd = "E:\\WebBrick SVN\\HomeGateway2\\Trunk\\WebBrickLibs\\EventHandlers\\tests\\TestOut\\20070203\\bu_040102.zip"

HttpSfname01 = "/o2m8/backup/bu_20070203T040100.zip"

Ftpfname01 = "/o2m8/backup/ftp_bu_20070203T040100.zip"

# a test with a single file
testConfigSingleFile = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name="minute">
                                <value>1</value>
                        </testEq>
        		    </params>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" 
                nameTemplate="./TestOut/%(year)04u%(month)02u%(date)02u/bu_%(hour)02u%(minute)02u00.zip"
                deleteAfterDays="7"
                path="./TestOut/20070203"/>

    </eventInterface>
</eventInterfaces>
"""

testConfigSingleFileCleanUp = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name="minute">
                                <value>1</value>
                        </testEq>
        		    </params>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>
        
        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name="minute">
                                <value>2</value>
                        </testEq>
        		    </params>
                    <!-- Check for changes to files in backup set -->
                    <cleanUp/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" 
                nameTemplate="./TestOut/%(year)04u%(month)02u%(date)02u/bu_%(hour)02u%(minute)02u00.zip"
                deleteAfterDays="7"
                path="E:\\WebBrick SVN\\HomeGateway2\\Trunk\\WebBrickLibs\\EventHandlers\\tests\\TestOut\\20070203\\"/>

    </eventInterface>
</eventInterfaces>
"""



# a test with a single file using the command line target
testConfigCommandLine = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <!-- Note the cmdTemplate needs to be local platform specific -->
        <destination transport="commandline" cmdTemplate="copy %(localname)s .\\TestOut\\bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

# a test with a single file
testConfigSingleFileDelete = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet deleteAfter="yes">
            <file path="./work/file1_delete.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMultipleFileChange = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files then do complete backup -->
                    <checkFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file?.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMixedChange = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <checkFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <file path="./work/file2.txt" />
            <directory path="./work/dir2" recursive='yes' />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMultipleFileDelta = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files then do complete backup -->
                    <checkDelta/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <file path="./work/file2.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMixedDelta = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <checkDelta/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <file path="./work/file2.txt" />
            <directory path="./work/dir2" recursive='yes' />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMultipleFile = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <file path="./work/file2.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMultipleFileCleanUp = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name="minute">
                                <value>1</value>
                                <value>2</value>
                                <value>3</value>
                        </testEq>
        		    </params>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>
        
        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name="minute">
                                <value>4</value>
                        </testEq>
        		    </params>
                    <!-- Check for changes to files in backup set -->
                    <cleanUp/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <file path="./work/file2.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination 
            transport="file" 
            nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""


testConfigMultipleFileAbsolute = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet absolutenames="yes" >
            <file path="./work/file1.txt" />
            <file path="./work/file2.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigSingleDirectory = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <directory path="./work" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMultipleDirectories = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <directory path="./work" />
            <directory path="./work/dir2" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigSingleDirectoryRecursive = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <directory path="./work" recursive='yes' />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigSingleDirectoryAbsolute = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet absolutenames="yes" >
            <directory path="./work" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigSingleDirectoryRecursiveAbsolute = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <params>
                        <testEq name="minute">
                            <value>1</value>
                        </testEq>
                    </params>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet absolutenames="yes" >
            <directory path="./work" recursive='yes' />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigMixed = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <file path="./work/file2.txt" />
            <directory path="./work/dir2" recursive='yes' />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="file" nameTemplate="./TestOut/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" />

    </eventInterface>
</eventInterfaces>
"""

testConfigFtp = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <file path="./work/file1.txt" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="ftp" 
            address="silent" 
            nameTemplate="./o2m8/backup/ftp_bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" 
            username="backup" password="backup" />

    </eventInterface>
</eventInterfaces>
"""

testConfigSingleDirectoryHttpS = """<?xml version="1.0" encoding="utf-8"?>
<eventInterfaces>
    <eventInterface module='EventHandlers.Backup' name='BackupHandler'>

        <eventtype type="">
            <eventsource source="time/minute" >
                <event>
                    <!-- Check for changes to files in backup set -->
                    <doFull/>
                </event>
            </eventsource>
        </eventtype>

        <!-- The steps we want -->
        <fileSet>
            <directory path="./work" />
            <exclude match=".*\.svn.*"/>
        </fileSet>

        <!-- Where to send backup -->
        <destination transport="https" 
            address="silent" 
            nameTemplate="/BACKUP/bu_%(year)04u%(month)02u%(date)02uT%(hour)02u%(minute)02u00.zip" 
            username="backup" password="backup"/>

    </eventInterface>
</eventInterfaces>
"""

class TestBackupHandler(unittest.TestCase):

    def clearDirectory(self, dname):
        for fn in os.listdir( dname ):
            fnf = "%s/%s" % (dname,fn)
            if isfile(fnf):
                _log.debug( "remove %s", fnf )
                os.remove( fnf )

    def setUp(self):
        _log.debug( "setup" )

        self.router = None
        self.loader = None

        ClearDirectory(workDir)
        ClearDirectory(outputDir)
        CopyDirectory(sourceDir, workDir)

        return

    def tearDown(self):

        if self.loader:
            self.loader.stop()  # all tasks
            self.loader = None
        self.router = None

        if isfile(testdata3):
            os.remove( testdata3 )

        return

    def waitForFile(self, fname, timeout=1.0 ):
        wait = timeout
        while wait > 0 and not isfile(fname):
            wait = wait - 0.1
            time.sleep(0.1)
            

    # Actual tests follow
    def testSingleFileLocal(self):
        """
        Initial single file backup
        """
        _log.debug( "\ntestSingleFileLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleFile) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01sd)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01sd ) )
        self.failUnless( zipfile.is_zipfile( fname01sd ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01sd, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 1 ) # one entry
        self.assertEqual( zfi[0].filename, "work/file1.txt" ) # one entry
        zf.close()

    def testSingleFileLocalCleanUp(self):
        """
        Initial single file backup
        """
        _log.debug( "\ntestSingleFileLocalCleanUp" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleFileCleanUp) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1)    # do initial backup
        self.waitForFile(fname01sd)
                
        # now verify file exists.
        self.failUnless( isfile( fname01sd ) )
        self.failUnless( zipfile.is_zipfile( fname01sd ) )
        # read zip info.

        now = time.time()
        
        # change the timestamp of the file to make it appear to be 6 days old  days old
        past6 = now - 3600*24*6
        os.utime(fname01sd, (past6, past6))
        # invoke cleanup
        self.router.publish( EventAgent("TestBackup"), Events.evtMinute2 )
        time.sleep(0.5)
        # verify file still exists.
        self.failUnless( isfile( fname01sd ) )
        
        # change the timestamp of the file to make it appear to be 6 days old  days old
        past8 = now - 3600*24*8
        os.utime(fname01sd, (past8, past8))
        # invoke cleanup
        self.router.publish( EventAgent("TestBackup"), Events.evtMinute2 )
        time.sleep(0.5)
        # verify file has been deleted
        self.failIf( isfile( fname01sd ) )
        
        self.loader.stop()  # all tasks
        self.loader = None

    def testSingleFileLocalDelete(self):
        """
        Initial single file backup
        """
        _log.debug( "\ntestSingleFileLocalDelete" )

        copyfile( testdata1, testdata3 )
        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleFileDelete) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 1 ) # one entry
        self.assertEqual( zfi[0].filename, "work/file1_delete.txt" )
        self.failIf( isfile( testdata3 ) )  # should be deleted
        zf.close()
    
    def testSingleDirectoryLocal(self):
        _log.debug( "\ntestSingleDirectoryLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleDirectory) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # two entrys
        self.assertEqual( zfi[0].filename, "file1.txt" )
        self.assertEqual( zfi[1].filename, "file2.txt" )
        zf.close()

    def testMultipleFilesLocal(self):
        _log.debug( "\ntestMultipleFilesLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMultipleFile) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # two entrys
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )
        zf.close()
        
        
    def testMultipleFilesLocalCleanUp(self):
        _log.debug( "\ntestMultipleFilesLocalCleanUp" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMultipleFileCleanUp) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do backup 1
        self.waitForFile(fname01)

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute2 )    # do backup 2
        self.waitForFile(fname02)

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute3 )    # do backup 3
        self.waitForFile(fname03)

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( isfile( fname02 ) )
        self.failUnless( isfile( fname03 ) )
       
        now = time.time()
        
        # change the timestamp of the file to make it appear to be 6 days old  days old
        past6 = now - 3600*24*6
        os.utime(fname02, (past6, past6))
        # invoke cleanup
        self.router.publish( EventAgent("TestBackup"), Events.evtMinute4 )
        time.sleep(0.5)
        # verify file still exists.
        self.failUnless( isfile( fname02 ) )
        
        # change the timestamp of the file to make it appear to be 6 days old  days old
        past8 = now - 3600*24*8
        os.utime(fname01, (past8, past8))
        os.utime(fname03, (past8, past8))
        # invoke cleanup
        self.router.publish( EventAgent("TestBackup"), Events.evtMinute4 )
        time.sleep(0.5)
        # verify file has been deleted
        self.failIf( isfile( fname01 ) )
        self.failUnless( isfile( fname02 ) )
        self.failIf( isfile( fname03 ) )
       
        self.loader.stop()  # all tasks
        self.loader = None

    def testMultipleDirectorysLocal(self):
        _log.debug( "\ntestMultipleDirectorysLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMultipleDirectories) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 4 )
        self.assertEqual( zfi[0].filename, "file1.txt" )
        self.assertEqual( zfi[1].filename, "file2.txt" )
        self.assertEqual( zfi[2].filename, "file1.1.txt" )
        self.assertEqual( zfi[3].filename, "file1.2.txt" )
        zf.close()

    def testSingleDirectoryRecursiveLocal(self):
        _log.debug( "\ntestSingleDirectoryRecursiveLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleDirectoryRecursive) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 4 )
        self.assertEqual( zfi[0].filename, "file1.txt" )
        self.assertEqual( zfi[1].filename, "file2.txt" )
        self.assertEqual( zfi[2].filename, "dir2/file1.1.txt" )
        self.assertEqual( zfi[3].filename, "dir2/file1.2.txt" )
        zf.close()

    def testMixedDataSetLocal(self):
        _log.debug( "\ntestMixedDataSetLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMixed) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 4 )
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )
        self.assertEqual( zfi[2].filename, "file1.1.txt" )
        self.assertEqual( zfi[3].filename, "file1.2.txt" )
        zf.close()

    def testSingleDirectoryAbsoluteLocal(self):
        _log.debug( "\ntestSingleDirectoryAbsoluteLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleDirectoryAbsolute) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()
        self.waitForFile(fname01)

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # two entrys
        self.failUnless( zfi[0].filename.endswith("/work/file1.txt") )
        self.failUnless( zfi[1].filename.endswith("/work/file2.txt") )
        zf.close()

    def testMultipleFilesAbsoluteLocal(self):
        _log.debug( "\ntestMultipleFilesAbsoluteLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMultipleFileAbsolute) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # two entrys
        self.failUnless( zfi[0].filename.endswith("/work/file1.txt") )
        self.failUnless( zfi[1].filename.endswith("/work/file2.txt") )
        zf.close()

    def testSingleDirectoryRecursiveAbsoluteLocal(self):
        _log.debug( "\ntestSingleDirectoryRecursiveAbsoluteLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleDirectoryRecursiveAbsolute) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 4 ) # two entrys
        self.failUnless( zfi[0].filename.endswith("/work/file1.txt") )
        self.failUnless( zfi[1].filename.endswith("/work/file2.txt") )
        self.failUnless( zfi[2].filename.endswith("/work/dir2/file1.1.txt") )
        self.failUnless( zfi[3].filename.endswith("/work/dir2/file1.2.txt") )
        zf.close()

    def testMultipleFileChangeLocal(self):
        """
        single file backup followed by no single file and then single file
        """
        _log.debug( "\ntestMultipleFileChangeLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMultipleFileChange) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # one entry
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute2 )    # no change should not create file
        time.sleep(0.1)
        self.failIf( exists( fname02 ) )    # should not exist

        file(testdata1, 'wb+').close()  # touch file
        time.sleep(0.1)
        zf.close()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute3 )    # no change should not create file
        self.waitForFile(fname03)
        # read zip info.
        zf = zipfile.ZipFile(fname03, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # one entry
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )

        self.loader.stop()  # all tasks
        self.loader = None
        zf.close()

    def testMixedDataSetChangeLocal(self):
        _log.debug( "\ntestMixedDataSetLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMixedChange) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 4 )
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )
        self.assertEqual( zfi[2].filename, "file1.1.txt" )
        self.assertEqual( zfi[3].filename, "file1.2.txt" )
        zf.close()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute2 )    # no change should not create file
        time.sleep(0.2)
        self.failIf( exists( fname02 ) )    # should not exist

        file(testdata2, 'wb+').close()  # touch file
        time.sleep(0.2)   # so clock rolls over

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute3 )    # no change should not create file
        self.waitForFile(fname03)
        # read zip info.
        self.failUnless( zipfile.is_zipfile( fname03 ) )
        zf = zipfile.ZipFile(fname03, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 4 )
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )
        self.assertEqual( zfi[2].filename, "file1.1.txt" )
        self.assertEqual( zfi[3].filename, "file1.2.txt" )
        zf.close()

        self.loader.stop()  # all tasks
        self.loader = None

    def testMultipleFileDeltaLocal(self):
        """
        single file backup followed by no single file and then single file
        """
        _log.debug( "\ntestMultipleFileDeltaLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMultipleFileDelta) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # one entry
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )
        zf.close()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute2 )    # no change should not create file
        time.sleep(0.2)
        self.failIf( exists( fname02 ) )    # should not exist

        file(testdata1, 'wb+').close()  # touch file
        time.sleep(0.2)

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute3 )    # no change should not create file
        self.waitForFile(fname03)
        # read zip info.
        zf = zipfile.ZipFile(fname03, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 1 ) # one entry
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        zf.close()

        self.loader.stop()  # all tasks
        self.loader = None

    def testMixedDataSetDeltaLocal(self):
        _log.debug( "\ntestMixedDataSetDeltaLocal" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigMixedDelta) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 4 )
        self.assertEqual( zfi[0].filename, "work/file1.txt" )
        self.assertEqual( zfi[1].filename, "work/file2.txt" )
        self.assertEqual( zfi[2].filename, "file1.1.txt" )
        self.assertEqual( zfi[3].filename, "file1.2.txt" )
        zf.close()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute2 )    # no change should not create file
        time.sleep(0.2)
        self.failIf( exists( fname02 ) )    # should not exist

        file(testdata2, 'wb+').close()  # touch file
        time.sleep(0.2)   # so clock rolls over

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute3 )    # no change should not create file
        self.waitForFile(fname03)
        # read zip info.
        self.failUnless( zipfile.is_zipfile( fname03 ) )
        zf = zipfile.ZipFile(fname03, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 1 ) # subversion control files get in the way.
        self.assertEqual( zfi[0].filename, "work/file2.txt" )
        zf.close()

        self.loader.stop()  # all tasks
        self.loader = None

    def testSingleDirectoryHttpS(self):
        _log.debug( "\ntestSingleDirectoryHttpS" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigSingleDirectoryHttpS) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(HttpSfname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( HttpSfname01 ) )
        self.failUnless( zipfile.is_zipfile( HttpSfname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(HttpSfname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # two entrys
        self.assertEqual( zfi[0].filename, "file1.txt" )
        self.assertEqual( zfi[1].filename, "file2.txt" )
        zf.close()

    def testSingleDirectoryFtp(self):
        _log.debug( "\ntestSingleDirectoryFtp" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigFtp) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(Ftpfname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( Ftpfname01 ) )
        self.failUnless( zipfile.is_zipfile( Ftpfname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(HttpSfname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 2 ) # two entrys
        self.assertEqual( zfi[0].filename, "file1.txt" )
        self.assertEqual( zfi[1].filename, "file2.txt" )
        zf.close()

    def testCommandLine(self):
        """
        Initial single file backup using command line disposal
        """
        _log.debug( "\ntestCommandLine" )

        self.loader = EventRouterLoader()
        self.loader.loadHandlers( getDictFromXmlString(testConfigCommandLine) )
        self.loader.start()  # all tasks
        self.router = self.loader.getEventRouter()

        self.router.publish( EventAgent("TestBackup"), Events.evtMinute1 )    # do initial backup
        self.waitForFile(fname01)

        self.loader.stop()  # all tasks
        self.loader = None

        # now verify file exists.
        self.failUnless( isfile( fname01 ) )
        self.failUnless( zipfile.is_zipfile( fname01 ) )
        # read zip info.
        zf = zipfile.ZipFile(fname01, 'r' ) # read only
        zfi = zf.infolist()
        self.assertEqual( len(zfi), 1 ) # one entry
        self.assertEqual( zfi[0].filename, "work/file1.txt" ) # one entry
        zf.close()

from MiscLib import TestUtils
def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testSingleFileLocal"
            , "testSingleFileLocalCleanUp"
            , "testSingleFileLocalDelete"
            , "testSingleDirectoryLocal"
            , "testSingleDirectoryRecursiveLocal"
            , "testMultipleFilesLocal"
            , "testMultipleFilesLocalCleanUp"
            , "testMultipleFilesAbsoluteLocal"
            , "testSingleDirectoryAbsoluteLocal"
            , "testSingleDirectoryRecursiveAbsoluteLocal"
            , "testMultipleDirectorysLocal"
            , "testMixedDataSetLocal"
            , "testMultipleFileChangeLocal"
            , "testMixedDataSetChangeLocal"
            , "testMultipleFileDeltaLocal"
            , "testMixedDataSetDeltaLocal"
            , "testCommandLine"
            ],
        "zzcomponent":
            [ "testComponents"
            ],
        "integration":
            [ "testSingleDirectoryHttpS"
             ,"testSingleDirectoryFtp"
            ],
        "zzpending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestBackupHandler, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestBackupHandler.log", getTestSuite, sys.argv)

