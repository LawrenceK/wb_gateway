# $Id: TestWb6Commands.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Integration testing for WebBrick hardware unit
# See http://pyunit.sourceforge.net/pyunit.html
#
# NOTE: this is not strictly a unit test, in that it requires a WebBrick to be
# available at the specified IP address

import sys, time, logging
import unittest

sys.path.append("../..")

from WebBrickLibs             import WbDefs
from WebBrickLibs.Wb6Commands import Wb6Commands
from WebBrickLibs.Wb6Config   import Wb6Config
from WebBrickLibs.Wb6Status   import Wb6Status

from TestWbConfig             import TestWbConfig
from TestWb6Config            import TestWb6Config

def showWorking():
    sys.stdout.write(".")

def showWait():
    sys.stdout.write("w")

# TestWb6Config is based on unittest.TestCase, 
class TestWb6Commands(TestWb6Config):

    _wbAddress  = TestWbConfig.WbAddress
    _wbPassword = TestWbConfig.WbFactoryPw

    def verifyCmdStatus( self ):
        time.sleep(0.5)
        sts = Wb6Status( self._wbAddress )
        cmdSts = sts.getCmdStatus()
        if cmdSts == 6: # webbrick started.
            cmdSts = 0
        self.assertEqual( cmdSts, 0 )
        self.assertNotEqual( sts.getOperationalState(), 255 )

    def doLogin(self):
        self.wb.Login( self._wbPassword )
        # self.wb.Login( "installer" )
        return

    def doReboot(self):
        # takes a while.
        self.doLogin()
        self.wb.Send( "RB" )
        time.sleep(8.0)
        return

    def factoryReset(self):
        self.doLogin()
        # send factory reset, full reset, does reeboot as well.
        self.wb.Send( "FR1" )
        time.sleep(10.0) # takes a while.
        return
        
    def setUp(self):
        self.wb = Wb6Commands( self._wbAddress )
        self._log = logging.getLogger("TestWb6Commands")
        return

    def tearDown(self):
        return
        
    # Actual tests follow

    def testConfigureDigitalIn(self):
        self.doLogin()
        self.verifyCmdStatus()

        # send CD command
        # D1, Target A1, action On, sp 4, dw 2, udp 1, udpnode 100
        for cmd in range(WbDefs.AT_NONE, WbDefs.AT_SPARE):
            self._log.debug( "testConfigureDigitalIn cmd %u", cmd )
            sp = cmd % WbDefs.SPCOUNT       # Pick an arbitrary set point number
#            if ( cmd == WbDefs.AT_DWELL ) or ( cmd == WbDefs.AT_DWELLCAN ):
            if ( cmd in (WbDefs.AT_DWELLALWAYS,WbDefs.AT_DWELLCAN,WbDefs.AT_DWELLON,WbDefs.AT_DWELLOFF ) ):
                showWorking()
                dwell = cmd % WbDefs.DWELLCOUNT     # Pick an arbitrary dwell number
                idStr = ( "ConfigDigIn, 1, WbDefs.TT_ANALOGUE, 1, cmd:" + str(cmd) + 
                          " sp:"+ str(sp) +" dw:"+str(dwell) + ",1,100")
                # Assemble and send command to WebBrick
                self.wb.ConfigDigIn(1, WbDefs.TT_ANALOGUE, 1, cmd, sp, dwell, 1, 100)
                self.verifyCmdStatus()
                # read all the configuration and verify entries.
                cfg = Wb6Config( self._wbAddress )
                for idx in range( 0, WbDefs.DICOUNT ):
                    if ( idx != 1):
                        self.verifyDiConfiguration(idx, cfg)
                    else:
                        di = cfg.getDigInTrigger(idx)
                        self.assertEqual( di["name"], "Sw-"+str(idx))
                        #self.assertEqual(di["action"], WbDefs.ActionStrs[cmd])
                        if not di["action"] in [WbDefs.ActionStrs[cmd], WbDefs.ActionStrs65[cmd]]:
                            print ">>> cmd ", cmd, ", ", [WbDefs.ActionStrs[cmd], WbDefs.ActionStrs65[cmd]]
                            print ">>> action ", di["action"]                        
                        assert(di["action"] in [WbDefs.ActionStrs[cmd], WbDefs.ActionStrs65[cmd]])
                        self.assertEqual(di["actionNr"], cmd)
                        self.assertEqual(di["pairChn"], 1)
                        self.assertEqual(di["options"], 2)
                        self.assertEqual(di["dwell"], dwell)
                        self.assertEqual(di["typeNr"], 2)
                        self.assertEqual(di["type"], "Analogue")
                        self.assertEqual(di["setPoint"], sp)
                        self.assertEqual(di["UDPRem"], "General")
                        self.assertEqual(di["UDPRemNr"], 1)
                        self.assertEqual(di["RemNode"], 100)
            else:
                showWorking()
                dwell = 0
                idStr = "ConfigDigIn, 1, WbDefs.TT_ANALOGUE, 1, cmd:" + str(cmd) + " sp:"+ str(sp) +" dw:"+str(dwell) + ",1,100"
                self.wb.ConfigDigIn( 1,WbDefs.TT_ANALOGUE,1,cmd,sp,dwell,1,100 )
                self.verifyCmdStatus()
                # read all the configuration and verify entries.
                cfg = Wb6Config( self._wbAddress )
                for idx in range( 0, WbDefs.DICOUNT ):
                    if ( idx != 1):
                        self.verifyDiConfiguration(idx, cfg)
                    else:
                        di = cfg.getDigInTrigger(idx)
                        self.assertEqual( di["name"], "Sw-"+str(idx))
                        self.assertEqual( di["actionNr"], cmd)
                        self.assertEqual( di["action"], WbDefs.ActionStrs[cmd])
                        self.assertEqual( di["pairChn"], 1)
                        self.assertEqual( di["options"], 2)
                        self.assertEqual( di["dwell"], dwell)
                        self.assertEqual( di["typeNr"], 2)
                        self.assertEqual( di["type"], "Analogue")
                        self.assertEqual( di["setPoint"], sp)
                        self.assertEqual( di["UDPRem"], "General")
                        self.assertEqual( di["UDPRemNr"], 1)
                        self.assertEqual( di["RemNode"], 100)
        
    def testConfigureAnIn(self):
        self.doLogin()
        # send CI command
        # CI<chn>;<L|H><val>;<ADS><tgtChn>;<sp>;<actionType>;<dwell>;<udpType>;<associatedValue>:
        self.wb.ConfigAnIn( 1, "L", 17, WbDefs.TT_ANALOGUE, 2, 
                WbDefs.AT_ON, WbDefs.SP_4, WbDefs.DW_0, WbDefs.UDPT_GENERAL, 99 )
        self.verifyCmdStatus()
        self.wb.ConfigAnIn( 1, "H", 87, WbDefs.TT_DIGITAL, 2, 
                WbDefs.AT_DWELLCAN, WbDefs.SP_0, WbDefs.DW_2, WbDefs.UDPT_GENERAL, 99 )
        self.verifyCmdStatus()

        idStr = "ConfigAnIn, 1"
        # read all the configuration and verify entries.
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.AICOUNT ):
            if ( idx != 1):
                self.verifyAiConfiguration(idx, cfg)
            else:
                ai = cfg.getAnalogueTriggerLow(idx)
                self.assertEqual( ai["name"], "AnIn-"+str(idx) )
                self.assertEqual( ai["threshold"], 17 )
                self.assertEqual( ai["actionNr"], 2 )
                self.assertEqual( ai["action"], "On" )
                self.assertEqual( ai["pairChn"], 2 )
                self.assertEqual( ai["dwell"], 0 )
                self.assertEqual( ai["typeNr"], 2 )
                self.assertEqual( ai["type"], "Analogue" )
                self.assertEqual( ai["setPoint"], 4 )
                self.assertEqual( ai["UDPRem"], "General" )
                self.assertEqual( ai["UDPRemNr"], 1 )
                self.assertEqual( ai["RemNode"], 99 )
        
                ai = cfg.getAnalogueTriggerHigh(idx)
                self.assertEqual( ai["name"], "AnIn-"+str(idx) )
                self.assertEqual( ai["threshold"], 87 )
                self.assertEqual( ai["actionNr"], 6 )
                self.assertEqual( ai["action"], "Dwell-can" )
                self.assertEqual( ai["pairChn"], 2 )
                self.assertEqual( ai["dwell"], 2 )
                self.assertEqual( ai["typeNr"], 0 )
                self.assertEqual( ai["type"], "Digital" )
                self.assertEqual( ai["setPoint"], 0 )
                self.assertEqual( ai["UDPRem"], "General" )
                self.assertEqual( ai["UDPRemNr"], 1 )
                self.assertEqual( ai["RemNode"], 99 )
        return

    def testConfigureAnThreshold(self):
        self.doLogin()
        # send CD command
        # D1, Target A1, action On, sp 4, dw 2, udp 1, udpnode 100
        self.wb.ConfigAnThreshold( 1, "L", 5 )
        self.verifyCmdStatus()
        self.wb.ConfigAnThreshold( 1, "H", 99 )
        self.verifyCmdStatus()

        # read all the configuration and verify entries.
        cfg = Wb6Config( self._wbAddress )
        sts = Wb6Status( self._wbAddress )
        for idx in range(0, WbDefs.AICOUNT ):
            # self.verifyAiConfiguration(idx, cfg)
            if ( idx == 1 ):
                self.assertEqual( sts.getAnInLowThresh(1), 5 )
                self.assertEqual( sts.getAnInHighThresh(1), 99 )
            else:
                self.assertEqual( sts.getAnInLowThresh(idx), 0 )
                self.assertEqual( sts.getAnInHighThresh(idx), 100 )
        return

    def testConfigureTempThreshold(self):
        self.doLogin()
        self.wb.ConfigTempThreshold( 1, "L", -10.5 )
        self.verifyCmdStatus()
        self.wb.ConfigTempThreshold( 1, "H", 57.5 )
        self.verifyCmdStatus()

        idStr = "ConfigTemp, 1"
        # read all the configuration and verify entries.
        cfg = Wb6Config( self._wbAddress )
        sts = Wb6Status( self._wbAddress )
        for idx in range(0, WbDefs.TEMPCOUNT ):
            # self.verifyTempConfiguration(idx, cfg)
            if ( idx == 1 ):
                self.assertEqual( sts.getTempHighThresh(1), 57.5 )
                self.assertEqual( sts.getTempLowThresh(1), -10.5 )
            else:
                self.assertEqual( sts.getTempHighThresh(idx), 100 )
                self.assertEqual( sts.getTempLowThresh(idx), -50 )
        return

    def testConfigureTemp(self):
        self.doLogin()
        # send CD command
        self.wb.ConfigTemp( 1, "L", -14.5, WbDefs.TT_ANALOGUE, 2, 
                WbDefs.AT_ON, WbDefs.SP_4, WbDefs.DW_2, WbDefs.UDPT_GENERAL, 99 )
        self.verifyCmdStatus()
        self.wb.ConfigTemp( 1, "H", 62.5, WbDefs.TT_DIGITAL, 2, 
                WbDefs.AT_DWELLCAN, WbDefs.SP_0, WbDefs.DW_2, WbDefs.UDPT_GENERAL, 99 )
        self.verifyCmdStatus()

        idStr = "ConfigTemp, 1"
        # read all the configuration and verify entries.
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.TEMPCOUNT ):
            if ( idx != 1):
                self.verifyTempConfiguration(idx, cfg)
            else:
                ti = cfg.getTempTriggerLow(idx)
                self.assertEqual( ti["name"], "Temp-"+str(idx) )
                self.assertEqual( ti["threshold"], -14.5 )
                self.assertEqual( ti["actionNr"], 2 )
                self.assertEqual( ti["action"], "On" )
                self.assertEqual( ti["pairChn"], 2 )
                self.assertEqual( ti["dwell"], 0 )
                self.assertEqual( ti["typeNr"], 2 )
                self.assertEqual( ti["type"], "Analogue" )
                self.assertEqual( ti["setPoint"], 4 )
                self.assertEqual( ti["UDPRem"], "General" )
                self.assertEqual( ti["UDPRemNr"], 1 )
                self.assertEqual( ti["RemNode"], 99 )
        
                ti = cfg.getTempTriggerHigh(idx)
                self.assertEqual( ti["name"], "Temp-"+str(idx) )
                self.assertEqual( ti["threshold"], 62.5 )
                self.assertEqual( ti["actionNr"], 6 )
                self.assertEqual( ti["action"], "Dwell-can" )
                self.assertEqual( ti["pairChn"], 2 )
                self.assertEqual( ti["dwell"], 2 )
                self.assertEqual( ti["typeNr"], 0 )
                self.assertEqual( ti["type"], "Digital" )
                self.assertEqual( ti["setPoint"], 0 )
                self.assertEqual( ti["UDPRem"], "General" )
                self.assertEqual( ti["UDPRemNr"], 1 )
                self.assertEqual( ti["RemNode"], 99 )
        return

    def doSetTime( self, d, h, m ):
        self.doLogin()
        self.wb.SetTime( d, h, m )
        time.sleep(5.0) # the schdule catch up could take a few seconds so lets make sure we wait to see whats happened
        self.verifyCmdStatus()
        sts = Wb6Status( self._wbAddress )
        ts = sts.getTime()
        tstr = "%02u:%02u:" % (h,m)
        assert (ts >= "%s00" % tstr ) and (ts <= "%s59" % tstr), "%s expected %s" % (ts,tstr)
        self.assertEqual( sts.getDay(), d)

    def testSetClock(self):
        self.doSetTime( 1, 1, 1 )
        self.verifyCmdStatus()
        sts = Wb6Status( self._wbAddress )
        ts = sts.getTime()
        assert (ts >= "01:01:00") and (ts <= "01:01:59"), ts
        self.assertEqual( sts.getDay(), 1)

    def testScheduledEvent(self):
        self.doSetTime( 1, 1, 1 )
        # Create a scheduled event
        self.wb.ConfigScheduled(  1, "1", 1, 2, WbDefs.TT_DIGITAL, 3, WbDefs.AT_TOGGLE, WbDefs.SP_0, WbDefs.DW_0, WbDefs.UDPT_GENERAL, 98 )
        self.verifyCmdStatus()
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.SCHEDCOUNT ):
            if ( idx == 1 ):
                sc = cfg.getScheduledEvent(idx)
                self.assertEqual( sc["days"], 2 )
                self.assertEqual( sc["hours"], 1 )
                self.assertEqual( sc["mins"], 2 )
                self.assertEqual( sc["actionNr"], 4 )
                self.assertEqual( sc["action"], "Toggle" )
                self.assertEqual( sc["pairChn"], 3 )
                self.assertEqual( sc["dwell"], 0 )
                self.assertEqual( sc["typeNr"], 0 )
                self.assertEqual( sc["type"], "Digital" )
                self.assertEqual( sc["setPoint"], 0 )
                self.assertEqual( sc["UDPRemNr"], 1 )
                self.assertEqual( sc["UDPRem"], "General" )
                self.assertEqual( sc["RemNode"], 98 )
            else:
                self.verifyScheduleConfiguration(idx, cfg)

        sts = Wb6Status( self._wbAddress )
        cur = sts.getDigOut(3);
        # wait for it to run?
        while ( sts.getTime() < "01:02:00" ):
            time.sleep(1.0)
            showWait()
            sts = Wb6Status( self._wbAddress )
        # ensure it has a chance to run
        time.sleep(1.0)
        sts = Wb6Status( self._wbAddress )
        assert (cur <> sts.getDigOut(3)),str(sts.getDigOut(3))    # did it toggle

    def testScheduledRestart(self):
        self.factoryReset() # from known state
        self.doSetTime( 1, 1, 0 ) # before scheduled event
        # Create a scheduled event
        self.wb.ConfigScheduled(  2, "1", 1, 2, WbDefs.TT_DIGITAL, 3, WbDefs.AT_TOGGLE, WbDefs.SP_0, WbDefs.DW_0, WbDefs.UDPT_GENERAL, 98 )
        self.verifyCmdStatus()

        # reboot, let system settle and then move clock forward
        self.doReboot()
        self.doSetTime( 1, 1, 3 ) # after scheduled event
        # now see what has happened
        sts = Wb6Status( self._wbAddress )
        assert sts.getDigOut(3), sts.getTime() + " " + str(sts.getDigOut(3))

    def testaScene(self):
        # configure a scene and verify it
        self.factoryReset()
        self.doLogin()
        self.wb.ConfigScene( 1, ["N","F","I","N","F","I","N","F"], [("S",1),"I",("S",2),"I"] )
        self.verifyCmdStatus()
        cfg = Wb6Config( self._wbAddress )
        for idx in range(0, WbDefs.SCENECOUNT ):
            if idx == 1 :
                sc = cfg.getScene(idx)
                self.assertEqual( sc["Digital0"], "On")
                self.assertEqual( sc["Digital1"], "Off")
                self.assertEqual( sc["Digital2"], "Ignore")
                self.assertEqual( sc["Digital3"], "On")
                self.assertEqual( sc["Digital4"], "Off")
                self.assertEqual( sc["Digital5"], "Ignore")
                self.assertEqual( sc["Digital6"], "On")
                self.assertEqual( sc["Digital7"], "Off")
                self.assertEqual( sc["Analogue0"], "SetPoint1")
                self.assertEqual( sc["Analogue1"], "Ignore")
                self.assertEqual( sc["Analogue2"], "SetPoint2")
                self.assertEqual( sc["Analogue3"], "Ignore")
            else:
                self.verifySceneConfiguration(idx, cfg)

    # did the scene set the outputs as expected.
    def verifySceneAction(self):
        time.sleep(1.0)
        sts = Wb6Status( self._wbAddress )
        # verify digital output state
        self.assertEqual( sts.getDigOut(0), True )
        self.assertEqual( sts.getDigOut(1), False )
        self.assertEqual( sts.getDigOut(2), False )     # not touched

        self.assertEqual( sts.getDigOut(3), True )
        self.assertEqual( sts.getDigOut(4), False )
        self.assertEqual( sts.getDigOut(5), False )     # not touched
        self.assertEqual( sts.getDigOut(6), True )
        self.assertEqual( sts.getDigOut(7), False )

        # verify analogue output state
        an = sts.getAnOut(0)
        assert  an == 14 , "Analogue 0 not at expected level " + str(an)
        an = sts.getAnOut(1)
        assert  an == 0 , "Analogue 1 not at expected level " + str(an)
        an = sts.getAnOut(2)
        assert  an == 28 , "Analogue 2 not at expected level " + str(an)
        an = sts.getAnOut(3)
        assert  an == 0 , "Analogue 3 not at expected level " + str(an)

    def testaSceneAndSet(self):
        # configure a scene and verify it
        self.testaScene()
        # Then set scene and verify outputs
        self.wb.SetScene( 1 )
        self.verifyCmdStatus()
        # let it process and update Siteplayer
        self.verifySceneAction()

    def testaSceneAndTrigger(self):
        # configure a scene and verify it
        self.testaScene()
        # configure a digital input to trigger a scene.
        self.wb.ConfigDigIn( 1,WbDefs.TT_SCENE, 1, WbDefs.AT_TOGGLE, WbDefs.SP_0, WbDefs.DW_0, WbDefs.UDPT_GENERAL, 100 )
        self.verifyCmdStatus()
        # Then trigger scene and verify outputs
        self.wb.DigTrigger(1)
        # let it process and update Siteplayer
        self.verifyCmdStatus()
        self.verifySceneAction()

    def testaTrigger(self):
        # make sure output off
        self.wb.DigOff(1)

        self.verifyCmdStatus()
        sts = Wb6Status( self._wbAddress )
        # verify digital output state
        self.assertEqual( sts.getDigOut(1), False )

        # configure a digital input to trigger a scene.
        self.wb.SendTrigger( WbDefs.TT_ANALOGUE, 1, WbDefs.AT_DWELL, WbDefs.SP_7, WbDefs.DW_3, WbDefs.UDPT_GENERAL, 100 )
        self.wb.SendTrigger( WbDefs.TT_DIGITAL, 1, WbDefs.AT_ON, WbDefs.SP_0, WbDefs.DW_0, WbDefs.UDPT_GENERAL, 100 )
        self.verifyCmdStatus()

        sts = Wb6Status( self._wbAddress )
        # verify digital output state
        self.assertEqual( sts.getDigOut(1), True )

    def testNameNode(self):
        self.doLogin()
        self.wb.Send( "NNTest1234" )
        self.verifyCmdStatus()
        
        self.wb.Send( "SN1" )
        self.verifyCmdStatus()
        cfg = Wb6Config( self._wbAddress )
        self.assertEqual( cfg.getNodeNumber(), 1 )

    # Sentinel/placeholder tests

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "Pending test"

# Assemble test suite
from MiscLib import TestUtils
def getTestSuite(select="unit", testargs=[]):
    """
    Get test suite

    select  is one of the following:
            "unit"        return suite of unit tests only
            "component"   return suite of component tests
            "integration" return suite of integration tests
            "all"         return suite of unit and component tests
            "pending"     return suite of pending tests
            name          a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testUnits"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            , "factoryReset"
            , "testNameNode"
            , "testConfigureDigitalIn"
            , "testConfigureAnIn"           # This pair interact a little
            , "testConfigureAnThreshold"    # This will fail on older firmware
            , "testConfigureTemp"           # This pair interact a little    
            , "testConfigureTempThreshold"  # This will fail on older firmware
            , "testSetClock"
            , "testScheduledEvent"
            , "testScheduledRestart"
            , "testaScene"
            , "testaSceneAndSet"
            , "testaSceneAndTrigger"
            , "testaTrigger"
            , "factoryReset"                # 2nd time
            ],
        "pending":
            [ "testPending"
            ]
        }
    for (argname,argval) in testargs:
        if argval: setattr(TestWb6Commands, argname, argval)
    return TestUtils.getTestSuite(TestWb6Commands, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    _wbAddress  = TestWbConfig.WbAddress
    _wbPassword = TestWbConfig.WbFactoryPw
    testargs = [ ("-a", "--address",  "ADR", "_wbAddress",  "IP address of WebBrick") 
               , ("-p", "--password", "PWD", "_wbPassword", "Password to access WebBrick")
               ]
    TestUtils.runTests("TestWb6Commands.log", getTestSuite, sys.argv, testargs)

# End.
