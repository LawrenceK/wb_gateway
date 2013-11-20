# $Id: TestParameterSet.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# Unit testing for parameter matching code.
# See http://pyunit.sourceforge.net/pyunit.html
#
import logging
import sys
import string
import unittest

sys.path.append("../..")

from MiscLib.DomHelpers import *

from WebBrickLibs.ParameterSet import *

class TestParameterSet(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestParameterSet" )
        self._log.debug( "setUp" )

    def tearDown(self):
        self._log.debug( "tearDown" )

    # Actual tests follow
    def testString(self):
        self._log.debug( "\ntestString" )

        val0 = {'val0':'1String', 'val':'0String'}
        val1 = {'val0':'1String', 'val':'1String'}
        val2 = {'val0':'1String', 'val':'2String'}

        testStr = ParameterStrEq('val', "1String")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterStrNe('val', "1String")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterStrLtEq('val', "1String")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterStrLt('val', "1String")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterStrGtEq('val', "1String")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterStrGt('val', "1String")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterStrEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterStrNe('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterStrLtEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterStrLt('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterStrGtEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterStrGt('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

    def testStringBlank(self):
        # Not None but an empty string.
        self._log.debug( "\ntestStringBlank" )

        val0 = {'val':''}
        val1 = {'val':'notBlank'}

        testStr = ParameterStrEq('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )

        testStr = ParameterStrNe('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )

        testStr = ParameterStrLtEq('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )

        testStr = ParameterStrLt('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )

        testStr = ParameterStrGtEq('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )

        testStr = ParameterStrGt('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )

        testStr = ParameterStrEq('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrNe('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )

        testStr = ParameterStrLtEq('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )

        testStr = ParameterStrLt('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )

        testStr = ParameterStrGtEq('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrGt('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

    def testStringMissing(self):
        # Missing
        self._log.debug( "\ntestStringBlank" )

        val0 = {}

        testStr = ParameterStrEq('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrNe('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrLtEq('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrLt('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrGtEq('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrGt('val', "")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrEq('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrNe('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrLtEq('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrLt('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrGtEq('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )

        testStr = ParameterStrGt('val', "notBlank")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )


    def testInteger(self):
        self._log.debug( "\ntestInteger" )

        val0 = {'val0':'1', 'val':'0'}
        val1 = {'val0':'1', 'val':'1'}
        val2 = {'val0':'1', 'val':'2'}

        testStr = ParameterIntEq('val', "1")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterIntNe('val', "1")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterIntLtEq('val', "1")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterIntLt('val', "1")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterIntGtEq('val', "1")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterIntGt('val', "1")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterIntEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterIntNe('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterIntLtEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterIntLt('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterIntGtEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterIntGt('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

    def testIntegerDiff(self):
        self._log.debug( "\ntestIntegerDiff" )

        val0 = {'val0':'1', 'val':'0'}
        val1 = {'val0':'1', 'val':'1'}
        val2 = {'val0':'1', 'val':'2'}
        val3 = {'val0':'1', 'val':'3'}

        testStr = ParameterIntDiffGtEq('val', "1", 1)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), True )

        testStr = ParameterIntDiffLtEq('val', "1", 1)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), False )

    def testIntegerDiffAbs(self):
        self._log.debug( "\ntestIntegerDiffAbs" )

        val0 = {'val0':'1', 'val':'0'}
        val1 = {'val0':'1', 'val':'1'}
        val2 = {'val0':'1', 'val':'2'}
        val3 = {'val0':'1', 'val':'3'}

        testStr = ParameterIntDiffAbsGtEq('val', "1", 1)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), True )

        testStr = ParameterIntDiffAbsLtEq('val', "1", 1)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), False )

    def testFloatDiff(self):
        self._log.debug( "\ntestFloatDiff" )

        val0 = {'val0':'1.5', 'val':'0.5'}
        val1 = {'val0':'1.5', 'val':'1.5'}
        val2 = {'val0':'1.5', 'val':'2.5'}
        val3 = {'val0':'1.5', 'val':'3.5'}

        testStr = ParameterFloatDiffGtEq('val', "1.5", 1.0)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), True )

        testStr = ParameterFloatDiffLtEq('val', "1.5", 1.0)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), False )

    def testFloatDiffAbs(self):
        self._log.debug( "\ntestFloatDiffAbs" )

        val0 = {'val0':'1.5', 'val':'0.5'}
        val1 = {'val0':'1.5', 'val':'1.5'}
        val2 = {'val0':'1.5', 'val':'2.5'}
        val3 = {'val0':'1.5', 'val':'3.5'}

        testStr = ParameterFloatDiffAbsGtEq('val', "1.5", 1.0)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), True )

        testStr = ParameterFloatDiffAbsLtEq('val', "1.5", 1.0)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )
        self.assertEqual( testStr.match(val3), False )

    def testFloat(self):
        self._log.debug( "\ntestFloat" )

        val0 = {'val0':'1.5', 'val':'0.5'}
        val1 = {'val0':'1.5', 'val':'1.5'}
        val2 = {'val0':'1.5', 'val':'2.5'}

        testStr = ParameterFloatEq('val', "1.5")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterFloatNe('val', "1.5")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterFloatLtEq('val', "1.5")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterFloatLt('val', "1.5")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterFloatGtEq('val', "1.5")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterFloatGt('val', "1.5")
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterFloatEq('val', 'val0', True )
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterFloatNe('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterFloatLtEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterFloatLt('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), False )

        testStr = ParameterFloatGtEq('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )
        self.assertEqual( testStr.match(val2), True )

        testStr = ParameterFloatGt('val', 'val0', True)
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), False )
        self.assertEqual( testStr.match(val2), True )
    
    def testSetEq(self):
        self._log.debug( "\ntestSetEq" )

        testSet = ParameterSet( { 'testEq': { 'type':'int', 'name': 'key1', 'value':'1'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0 } ), False )
        self.assertEqual( testSet.match( {'key1': 1 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2 } ),  False )

        testSet = ParameterSet( { 'testEq': {'type':'float', 'name': 'key1', 'value':'1.5' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2.5 } ),  False )

        testSet = ParameterSet( { 'testEq': { 'type':'string', 'name': 'key1', 'value':'1String'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  False )

    def testSetInt(self):
        self._log.debug( "\ntestSetInt" )

        testSet = ParameterSet( { 'testEq': {'name': 'key1', 'value':'1' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0 } ), False )
        self.assertEqual( testSet.match( {'key1': 1 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2 } ),  False )

        testSet = ParameterSet( { 'testLe': {'name': 'key1', 'value':'1' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0 } ),  True )
        self.assertEqual( testSet.match( {'key1': 1 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2 } ),  False )

        testSet = ParameterSet( { 'testLt': {'name': 'key1', 'value':'1' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0 } ),  True )
        self.assertEqual( testSet.match( {'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key1': 2 } ),  False )

        testSet = ParameterSet( { 'testGe': {'name': 'key1', 'value':'1' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2 } ),  True )

        testSet = ParameterSet( { 'testGt': {'name': 'key1', 'value':'1' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key1': 2 } ),  True )
    
    def testSetInt2(self):
        self._log.debug( "\ntestSetInt2" )

        testSet = ParameterSet( { 'testEq': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 0 } ), False )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 1 } ),  True )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 2 } ),  False )

        testSet = ParameterSet( { 'testNe': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 0 } ), True )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 2 } ),  True )

        testSet = ParameterSet( { 'testLe': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 0 } ),  True )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 1 } ),  True )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 2 } ),  False )

        testSet = ParameterSet( { 'testLt': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 0 } ),  True )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 2 } ),  False )

        testSet = ParameterSet( { 'testGe': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 1 } ),  True )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 2 } ),  True )

        testSet = ParameterSet( { 'testGt': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1': 2 } ),  True )

    def testSetInt3(self):
        self._log.debug( "\ntestSetInt3" )

        testSet = ParameterSet( { 'testLe': { 'name': 'key1', 'value':'8'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': -4 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12 } ),  False )

        testSet = ParameterSet( { 'testLt': { 'name': 'key1', 'value':'8'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12 } ),  False )

        testSet = ParameterSet( { 'testGe': { 'name': 'key1', 'value':'8'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12 } ),  True )

        testSet = ParameterSet( { 'testGt': { 'name': 'key1', 'value':'8'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12 } ),  True )

        testSet = ParameterSet( { 'testLe': { 'name': 'key1', 'value':'15'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 15 } ),  True )
        self.assertEqual( testSet.match( {'key1': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': -4 } ),  True )
        self.assertEqual( testSet.match( {'key1': 18 } ),  False )

        testSet = ParameterSet( { 'testLt': { 'name': 'key1', 'value':'15'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 15 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': -4 } ),  True )
        self.assertEqual( testSet.match( {'key1': 18 } ),  False )

        testSet = ParameterSet( { 'testGe': { 'name': 'key1', 'value':'15'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 15 } ),  True )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 18 } ),  True )

        testSet = ParameterSet( { 'testGt': { 'name': 'key1', 'value':'15'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 15 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 18 } ),  True )

    def testSetInt4(self):
        self._log.debug( "\ntestSetInt4" )

        testSet = ParameterSet( { 'testDiffGe': { 'name': 'key1', 'value':'8', 'diffValue':'1'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12 } ),  True )

        testSet = ParameterSet( { 'testDiffLe': { 'name': 'key1', 'value':'8', 'diffValue':'1'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': -4 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12 } ),  False )

        testSet = ParameterSet( { 'testAbsDiffGe': { 'name': 'key1', 'value':'8', 'diffValue':'1'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12 } ),  True )

        testSet = ParameterSet( { 'testAbsDiffLe': { 'name': 'key1', 'value':'8', 'diffValue':'1'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12 } ),  False )

    def testSetFloat(self):
        self._log.debug( "\ntestSetFloat" )

        testSet = ParameterSet( { 'testEq': {'name': 'key1', 'value':'1.5' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2.5 } ),  False )

        testSet = ParameterSet( { 'testLe': {'name': 'key1', 'value':'1.5' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2.5 } ),  False )

        testSet = ParameterSet( { 'testLt': {'name': 'key1', 'value':'1.5' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 2.5 } ),  False )

        testSet = ParameterSet( { 'testGe': {'name': 'key1', 'value':'1.5' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 2.5 } ),  True )

        testSet = ParameterSet( { 'testGt': {'name': 'key1', 'value':'1.5' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 2.5 } ),  True )

    def testSetFloat2(self):
        self._log.debug( "\ntestSetFloat2" )

        testSet = ParameterSet( { 'testEq': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 2.5 } ),  False )

        testSet = ParameterSet( { 'testNe': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 0.5 } ),  True )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 2.5 } ),  True )

        testSet = ParameterSet( { 'testLe': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 0.5 } ),  True )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 2.5 } ),  False )

        testSet = ParameterSet( { 'testLt': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 0.5 } ),  True )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 2.5 } ),  False )

        testSet = ParameterSet( { 'testGe': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 2.5 } ),  True )

        testSet = ParameterSet( { 'testGt': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1': 2.5 } ),  True )

    def testSetFloat3(self):
        self._log.debug( "\ntestSetFloat3" )

        testSet = ParameterSet( { 'testLe': { 'name': 'key1', 'value':'1.5'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': -0.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12.5 } ),  False )

        testSet = ParameterSet( { 'testLt': { 'name': 'key1', 'value':'1.5'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': -0.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12.5 } ),  False )

        testSet = ParameterSet( { 'testGe': { 'name': 'key1', 'value':'1.5'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': -0.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12.5 } ),  True )

        testSet = ParameterSet( { 'testGt': { 'name': 'key1', 'value':'1.5'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': -0.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12.5 } ),  True )

    def testSetFloat4(self):
        self._log.debug( "\ntestSetFloat4" )

        testSet = ParameterSet( { 'testDiffGe': { 'name': 'key1', 'value':'1.5', 'diffValue':'1.0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': -3.0 } ),  False )
        self.assertEqual( testSet.match( {'key1': 3.0 } ),  True )

        testSet = ParameterSet( { 'testDiffLe': { 'name': 'key1', 'value':'1.5', 'diffValue':'1.0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': -3.0 } ),  True )
        self.assertEqual( testSet.match( {'key1': 3.0 } ),  False )

        testSet = ParameterSet( { 'testAbsDiffGe': { 'name': 'key1', 'value':'1.5', 'diffValue':'1.0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key1': -3.0 } ),  True )
        self.assertEqual( testSet.match( {'key1': 3.0 } ),  True )

        testSet = ParameterSet( { 'testAbsDiffLe': { 'name': 'key1', 'value':'1.5', 'diffValue':'1.0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 1.5 } ),  True )
        self.assertEqual( testSet.match( {'key1': -3.0 } ),  False )
        self.assertEqual( testSet.match( {'key1': 3.0 } ),  False )

    def testSetString2(self):
        self._log.debug( "\ntestSetString2" )

        testSet = ParameterSet( { 'testEq': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '2String' } ),  False )

        testSet = ParameterSet( { 'testNe': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '0String' } ),  True )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '2String' } ),  True )

        testSet = ParameterSet( { 'testLe': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '0String' } ),  True )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '2String' } ),  False )

        testSet = ParameterSet( { 'testLt': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '0String' } ),  True )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '2String' } ),  False )

        testSet = ParameterSet( { 'testGe': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '2String' } ),  True )

        testSet = ParameterSet( { 'testGt': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1': '2String' } ),  True )

    def testMissingStringValues(self):
        self._log.debug( "\ntestMissingStringValues" )

        testSet = ParameterSet( { 'testEq': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '2String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '2String' } ),  False )

        testSet = ParameterSet( { 'testNe': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '2String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '2String' } ),  False )

        testSet = ParameterSet( { 'testLe': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '2String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '2String' } ),  False )

        testSet = ParameterSet( { 'testLt': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '2String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '2String' } ),  False )

        testSet = ParameterSet( { 'testGe': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '2String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '2String' } ),  False )

        testSet = ParameterSet( { 'testGt': {'name': 'key1', 'param2':'key0' } } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0x':'1String', 'key1': '2String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key0':'1String', 'key1x': '2String' } ),  False )
    
    def testMissingIntValues(self):
        self._log.debug( "\ntestMissingIntValues" )

        testSet = ParameterSet( { 'testEq': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 0 } ), False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 2 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 0 } ), False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 2 } ),  False )

        testSet = ParameterSet( { 'testNe': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 0 } ), False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 2 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 0 } ), False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 2 } ),  False )

        testSet = ParameterSet( { 'testLe': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 2 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 2 } ),  False )

        testSet = ParameterSet( { 'testLt': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 2 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 2 } ),  False )

        testSet = ParameterSet( { 'testGe': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 2 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 2 } ),  False )

        testSet = ParameterSet( { 'testGt': { 'type':'int', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0x':1, 'key1': 2 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 0 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 1 } ),  False )
        self.assertEqual( testSet.match( {'key0':1, 'key1x': 2 } ),  False )

    def testMissingFloatValues(self):
        self._log.debug( "\ntestMissingFloatValues" )

        testSet = ParameterSet( { 'testEq': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 2.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 2.5 } ),  False )

        testSet = ParameterSet( { 'testNe': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 2.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 2.5 } ),  False )

        testSet = ParameterSet( { 'testLe': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 2.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 2.5 } ),  False )

        testSet = ParameterSet( { 'testLt': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 2.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 2.5 } ),  False )

        testSet = ParameterSet( { 'testGe': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 2.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 2.5 } ),  False )

        testSet = ParameterSet( { 'testGt': { 'type':'float', 'name': 'key1', 'param2':'key0'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0x': 1.5, 'key1': 2.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 0.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 1.5 } ),  False )
        self.assertEqual( testSet.match( {'key0': 1.5, 'key1x': 2.5 } ),  False )

    def testSetString(self):
        self._log.debug( "testSetString" )

        testSet = ParameterSet( { 'testEq': { 'type':'string', 'name': 'key1', 'value':'1String'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  False )

        testSet = ParameterSet( { 'testLe': { 'type':'string', 'name': 'key1', 'value':'1String'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': '0String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  False )

        testSet = ParameterSet( { 'testLt': { 'type':'string', 'name': 'key1', 'value':'1String'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': '0String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  False )

        testSet = ParameterSet( { 'testGe': { 'type':'string', 'name': 'key1', 'value':'1String'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  True )

        testSet = ParameterSet( { 'testGt': { 'type':'string', 'name': 'key1', 'value':'1String'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  True )

    def testSetAnd(self):
        # Loaded from XML
        self._log.debug( "\ntestSetAnd" )

        testCfgXml = """<root><testGt type='int' name='key1' param2='ki' />
                    <testGt name='key4' param2='ks4' />
                    </root>
                    """

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root

        testCfgRef = { 'testGt': [ { 'name': 'key1', 'param2':'ki'},
                                { 'name': 'key4', 'param2':'ks4'} ]
            }

        test1 = { 'key1': 2,
            'key4': '5String',
            'ki':1,
            'ks4':'4String',
            }

        test2 = { 'key1': 1,
            'key4': '5String',
            'ki':1,
            'ks4':'4String',
            }

        test3 = { 'key1': 2,
            'key4': '4String',
            'ki':1,
            'ks4':'4String',
            }

        test4 = { 'key1': 1,
            'key4': '4String',
            'ki':1,
            'ks4':'4String',
            }

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), False )
        self.assertEqual( testSet.match( test3 ), False )
        self.assertEqual( testSet.match( test4 ), False )

    def testSetOr(self):
        # Loaded from XML
        self._log.debug( "\ntestSetOr" )

        testCfgXml = """<root>
<testGt name='key2'><param2>ks1</param2><param2>ks2</param2></testGt>
</root>
"""

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root

        testCfgRef = { 'testGt': [ { 'name': 'key2', 'param2':['ks1','ks2'] },
                                ]
            }

        test1 = { 
            'key2': '2String',
            'ks1':'1String',
            'ks2':'2String'
            }

        test2 = { 
            'key2': '2String',
            'ks1':'2String',
            'ks2':'1String'
            }

        test3 = { 
            'key2': '2String',
            'ks1':'1String',
            'ks2':'1String'
            }

        test4 = { 
            'key2': '2String',
            'ks1':'2String',
            'ks2':'2String'
            }

        self._log.debug( "testCfg %s" % (testCfg) )
        self._log.debug( "testCfgRef %s" % (testCfgRef) )

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), True )
        self.assertEqual( testSet.match( test3 ), True )
        self.assertEqual( testSet.match( test4 ), False )

    def testList(self):
        self._log.debug( "\ntestList" )

        testSet = ParameterSet( { 'testEq': {'name': 'key1', 'value':['1String', '2String' ] } } )
        self._log.debug( testSet )

        self.assertEqual( testSet.match( {'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  True )

    def testList2(self):
        self._log.debug( "\ntestList2" )

        testCfg = { 
            'testEq':
                { 'name': 'key1', 'value': ['1String', '2String'] },
            }

        testSet = ParameterSet( testCfg )
        self._log.debug( "testCfg %s" % testCfg )
        self._log.debug( "testSet %s" % testSet )

        self.assertEqual( testSet.match( {'key1': '0String' } ),  False )
        self.assertEqual( testSet.match( {'key1': '1String' } ),  True )
        self.assertEqual( testSet.match( {'key1': '2String' } ),  True )

    def testSetMixed(self):
        self._log.debug( "\ntestSetMixed" )

        testCfg = {'testGt': {'name': 'key1', 'value':'1' },
            'testGe': {'name': 'key2', 'value':'1String' },
            'testLt': {'name': 'key3', 'value':'1.5' },
             }

        test1 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4
            }

        test2 = { 'key1': 1,
            'key2': '2String',
            'key3': 1.4
            }

        test3 = { 'key1': 2,
            'key2': '0String',
            'key3': 1.4
            }

        test4 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.6
            }


        testSet = ParameterSet( testCfg )
        self._log.debug( testCfg )
        self._log.debug( testSet )

        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), False )
        self.assertEqual( testSet.match( test3 ), False )
        self.assertEqual( testSet.match( test4 ), False )

    def testSetMixed2(self):
        self._log.debug( "\n\testSetMixed2" )

        testCfg = { 'testGt': { 'name': 'key1', 'value':'1'},
                    'testGe': { 'name': 'key2', 'value':'1String'},
                    'testLt': { 'name': 'key3', 'value':'1.5'}
            }

        test1 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4
            }

        test2 = { 'key1': 1,
            'key2': '2String',
            'key3': 1.4
            }

        test3 = { 'key1': 2,
            'key2': '0String',
            'key3': 1.4
            }

        test4 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.6
            }

        testSet = ParameterSet( testCfg )
        self._log.debug( testCfg )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), False )
        self.assertEqual( testSet.match( test3 ), False )
        self.assertEqual( testSet.match( test4 ), False )

    def testSetMixed3(self):
        self._log.debug( "\n\testSetMixed3" )

        # multiple > tests with multiple values for one key.
        testCfg = { 'testGt': [ { 'name': 'key1', 'value':'1'},
                                { 'name': 'key2', 'value':['1String','2String'] },
                                { 'name': 'key4', 'value':'4String'} ],
                    'testLt': { 'name': 'key3', 'value':'1.5'}
            }

        test1 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            }

        test2 = { 'key1': 1,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            }

        test3 = { 'key1': 2,
            'key2': '0String',
            'key3': 1.4,
            'key4': '5String',
            }

        test4 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.6,
            'key4': '5String',
            }

        test5 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            }

        self._log.debug( testCfg )
        testSet = ParameterSet( testCfg )
        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), False )
        self.assertEqual( testSet.match( test3 ), False )
        self.assertEqual( testSet.match( test4 ), False )
        self.assertEqual( testSet.match( test5 ), True )

    def testSetMixed4(self):
        # Loaded from XML
        self._log.debug( "\ntestSetMixed4" )

        testCfgXml = """<root><testGt name='key1' value='1' />
                    <testGt name='key2'><value>1String</value><value>2String</value></testGt>
                    <testGt name='key4' value='4String' />
                    <testLt name='key3' value='1.5' />
                    </root>
                    """

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root

        testCfgRef = { 'testGt': [ { 'name': 'key1', 'value':'1'},
                                { 'name': 'key2', 'value':['1String','2String'] },
                                { 'name': 'key4', 'value':'4String'} ],
                    'testLt': { 'name': 'key3', 'value':'1.5'}
            }

        test1 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            }

        test2 = { 'key1': 1,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            }

        test3 = { 'key1': 2,
            'key2': '0String',
            'key3': 1.4,
            'key4': '5String',
            }

        test4 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.6,
            'key4': '5String',
            }

        test5 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            }

        self._log.debug( "testCfg %s" % (testCfg) )
        self._log.debug( "testCfgRef %s" % (testCfgRef) )

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), False )
        self.assertEqual( testSet.match( test3 ), False )
        self.assertEqual( testSet.match( test4 ), False )
        self.assertEqual( testSet.match( test5 ), True )

    def testSetMixed5(self):
        # Loaded from XML
        self._log.debug( "\ntestSetMixed5" )

        testCfgXml = """<root><testGt type='int' name='key1' param2='ki' />
                    <testGt name='key2'><param2>ks1</param2><param2>ks2</param2></testGt>
                    <testGt name='key4' param2='ks4' />
                    <testLt type='float' name='key3' param2='kf' />
                    </root>
                    """

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root

        testCfgRef = { 'testGt': [ { 'name': 'key1', 'param2':'ki'},
                                { 'name': 'key2', 'param2':['ks1','ks2'] },
                                { 'name': 'key4', 'param2':'ks4'} ],
                    'testLt': { 'name': 'key3', 'param2':'kf'}
            }

        test1 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            'ki':1,
            'ks1':'1String',
            'ks2':'2String',
            'ks4':'4String',
            'kf':1.5,
            }

        test2 = { 'key1': 1,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            'ki':1,
            'ks1':'1String',
            'ks2':'2String',
            'ks4':'4String',
            'kf':1.5,
            }

        test3 = { 'key1': 2,
            'key2': '0String',
            'key3': 1.4,
            'key4': '5String',
            'ki':1,
            'ks1':'1String',
            'ks2':'2String',
            'ks4':'4String',
            'kf':1.5,
            }

        test4 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.6,
            'key4': '5String',
            'ki':1,
            'ks1':'1String',
            'ks2':'2String',
            'ks4':'4String',
            'kf':1.5,
            }

        test5 = { 'key1': 2,
            'key2': '2String',
            'key3': 1.4,
            'key4': '5String',
            'ki':1,
            'ks1':'1String',
            'ks2':'2String',
            'ks4':'4String',
            'kf':1.5,
            }

        self._log.debug( "testCfg %s" % (testCfg) )
        self._log.debug( "testCfgRef %s" % (testCfgRef) )

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), False )
        self.assertEqual( testSet.match( test3 ), False )
        self.assertEqual( testSet.match( test4 ), False )
        self.assertEqual( testSet.match( test5 ), True )

    def testTimeStr(self):
        # Loaded from XML
        self._log.debug( "\ntestTimeStr" )

        testCfgXml = """<root>
            <testGe name='timestr' value='06:30:00'/>
            <testLt name='timestr' value='10:00:00'/>
                    </root>
                    """

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root


        test1 = { 'timestr': '04:33:33'
            }

        test2 = {  'timestr': '06:30:30'
            }

        test3 = {  'timestr': '07:33:00'
            }

        test4 = {  'timestr': '09:59:00'
            }

        test5 = {  'timestr': '10:00:00'
            }

        test6 = {  'timestr': '12:00:00'
            }


        self._log.debug( "testCfg %s" % (testCfg) )

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), False )
        self.assertEqual( testSet.match( test2 ), True )
        self.assertEqual( testSet.match( test3 ), True )
        self.assertEqual( testSet.match( test4 ), True )
        self.assertEqual( testSet.match( test5 ), False )
        self.assertEqual( testSet.match( test6 ), False )

    def testExplicitAnd(self):
        self._log.debug( "\ntestExplicitAnd" )

        testCfgXml = """<root>
                            <testAnd>
                    <testGe name='val1' value='1'/>
                    <testGe name='val2' value='2'/>
                            </testAnd>
                    </root>
                    """

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root


        test1 = { 'val1': 1,
                    'val2': 2
            }

        self._log.debug( "testCfg %s" % (testCfg) )

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )

    def testExplicitOr(self):
        self._log.debug( "\ntestExplicitOr" )

        testCfgXml = """<root>
                            <testOr>
                    <testGe name='val1' value='1'/>
                    <testGe name='val2' value='2'/>
                            </testOr>
                    </root>
                    """

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root


        test1 = { 'val1': 1,
                    'val2': 1
            }

        self._log.debug( "testCfg %s" % (testCfg) )

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )

    def testSetNamedCompare(self):
        # compare using named values for both sides.
        # Loaded from XML
        self._log.debug( "\ntestSetNamedCompare" )

        testCfgXml = """<root>
<testGt name='key1' param2='key2' />
<testGt name='key3' param2='key4' />
</root>
"""

        testCfg = getDictFromXmlString(testCfgXml)
        testCfg = testCfg['root'] # loose root

        testCfgRef = { 'testGt': [ { 'name': 'key1', 'param2': 'key2'},
                                { 'name': 'key3', 'param2': 'key4'}],
            }

        test1 = { 'key1': 2,
            'key2': '2String'
            }

        test1 = { 
            'key3': 'bstring',
            'key4': 'astring',
            }

        self._log.debug( "testCfg %s" % (testCfg) )
        self._log.debug( "testCfgRef %s" % (testCfgRef) )

        testSet = ParameterSet( testCfg )

        self._log.debug( testSet )
        self.assertEqual( testSet.match( test1 ), True )
        self.assertEqual( testSet.match( test2 ), False )

    def testChanged(self):
        self._log.debug( "\ntestChanged" )

        val0 = {'val':'0String', 'vali':0, 'valf':0.5}
        val1 = {'val':'1String', 'vali':1, 'valf':1.5}

        testStr = ParameterStrChanged('val')
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )

        testStr = ParameterIntChanged('vali')
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )

        testStr = ParameterFloatChanged('valf')
        self._log.debug( testStr )
        self.assertEqual( testStr.match(val0), True )
        self.assertEqual( testStr.match(val0), False )
        self.assertEqual( testStr.match(val1), True )
    
    def testSetChanged(self):
        self._log.debug( "\ntestSetChanged" )
        
        val0 = {'val':'0String', 'vali':0, 'valf':0.5}
        val1 = {'val':'1String', 'vali':1, 'valf':1.5}

        testSet = ParameterSet( { 'testChanged': { 'type':'int', 'name': 'vali'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match(val0), True )
        self.assertEqual( testSet.match(val0), False )
        self.assertEqual( testSet.match(val1), True )

        testSet = ParameterSet( { 'testChanged': { 'type':'float', 'name': 'valf'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match(val0), True )
        self.assertEqual( testSet.match(val0), False )
        self.assertEqual( testSet.match(val1), True )

        testSet = ParameterSet( { 'testChanged': { 'type':'string', 'name': 'val'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match(val0), True )
        self.assertEqual( testSet.match(val0), False )
        self.assertEqual( testSet.match(val1), True )

        # test when type defaults to string.
        testSet = ParameterSet( { 'testChanged': { 'name': 'val'} } )
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match(val0), True )
        self.assertEqual( testSet.match(val0), False )
        self.assertEqual( testSet.match(val1), True )

    def testExplicitOr(self):
        self._log.debug( "\ntestExplicitOr" )

        testSet = ParameterSet( { 'testOr': 
                    {
                    'testLe': { 'name': 'key1', 'value':'8'},
                    'testLt': { 'name': 'key2', 'value':'4'}
                    }
                }
            )
        
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': -4 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12 } ),  False )
        self.assertEqual( testSet.match( {'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key2': -4 } ),  True )
        self.assertEqual( testSet.match( {'key2': 12 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8, 'key2': 8 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12, 'key2': 3 } ),  True )
        self.assertEqual( testSet.match( {'key1': 12, 'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8, 'key2': 3 } ),  True )

    def testExplicitAnd(self):
        self._log.debug( "\ntestExplicitAnd" )

        testSet = ParameterSet( { 'testAnd': 
                    {
                    'testLe': { 'name': 'key1', 'value':'8'},
                    'testLt': { 'name': 'key2', 'value':'4'}
                    }
                }
            )
        
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12 } ),  False )
        self.assertEqual( testSet.match( {'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key2': -4 } ),  False )
        self.assertEqual( testSet.match( {'key2': 12 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8, 'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12, 'key2': 3 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12, 'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8, 'key2': 3 } ),  True )

    def testImplicitAnd(self):
        self._log.debug( "\ntestExplicitAnd" )

        testSet = ParameterSet( 
                    {
                    'testLe': { 'name': 'key1', 'value':'8'},
                    'testLt': { 'name': 'key2', 'value':'4'}
                    }
            )
        
        self._log.debug( "testSet %s" % (testSet) )
        self.assertEqual( testSet.match( {'key1': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': -4 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12 } ),  False )
        self.assertEqual( testSet.match( {'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key2': -4 } ),  False )
        self.assertEqual( testSet.match( {'key2': 12 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8, 'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12, 'key2': 3 } ),  False )
        self.assertEqual( testSet.match( {'key1': 12, 'key2': 8 } ),  False )
        self.assertEqual( testSet.match( {'key1': 8, 'key2': 3 } ),  True )

    # Sentinel/placeholder tests

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "No pending test"

    def testDummy(self):
        self._log.debug( "\ntestDummy" )

# Assemble test suite

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
            [ "testUnits"
            , "testString"
            , "testStringBlank"
            , "testStringMissing"
            , "testInteger"
            , "testIntegerDiff"
            , "testIntegerDiffAbs"
            , "testFloat"
            , "testFloatDiff"
            , "testFloatDiffAbs"
            , "testSetEq"
            , "testSetAnd"
            , "testSetOr"
            , "testSetInt"
            , "testSetInt2"
            , "testSetInt3"
            , "testSetInt4"
            , "testSetFloat"
            , "testSetFloat2"
            , "testSetFloat3"
            , "testSetFloat4"
            , "testSetString"
            , "testSetString2"
            , "testSetMixed"
            , "testSetMixed2"
            , "testSetMixed3"
            , "testSetMixed4"
            , "testSetMixed5"
            , "testMissingStringValues"
            , "testMissingIntValues"
            , "testMissingFloatValues"
            , "testList"
            , "testList2"
            , "testTimeStr"
            , "testChanged"
            , "testSetChanged"
            , "testExplicitOr"
            , "testExplicitAnd"
            , "testImplicitAnd"
            ],
        "component":
            [ "testComponents"
            ],
        "integration":
            [ "testIntegration"
            ],
        "pending":
            [ "testPending"
            ]
        }
    return TestUtils.getTestSuite(TestParameterSet, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestParameterSet.log", getTestSuite, sys.argv)

