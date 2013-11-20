# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: ParameterSet.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
#  Lawrence Klyne
#
# NOTE as this is possibly configured through getDictFromXml, the values may be in dictionaries.
# This is likely to happen where multiple values are logically or'd. The code accepts the data either
# as an Xml attribute where there is one value and a list of elements otherwise. Elements NOW always
# create dictionaries.
#

"""
Module to handle matching structured parameter sets and other entities presented as 
nested dictionaries, and for extracting values from such entities.

One area this is used is for matching and processing events in event dispatching 
logic, where the events and event payloads are presented as dictionaries.  The matching
structures allow for matching of combinations of structures, and also for matching
based on ordering relations between values of basic data types such as integer, float,
etc.
"""


import re, logging

_log = logging.getLogger( "WebBrickLibs.ParameterSet" )

# some tests we need
# Note when testing test for int first and then float
testInt = re.compile( r'^\d+$' )
testFloat = re.compile( r'^\d+.\d*$' )

class ParameterBase:
    def __init__( self, key1, key2orValue, isKey ):
        self._key1 = key1
        self._key2orValue = key2orValue
        self._isKey = isKey

    def match( self, values ):
        return False

    def value1( self, values ):
        if values.has_key(self._key1):
            return values[self._key1]
        return None

    def value2( self, values ):
        if self._isKey:
            if values.has_key(self._key2orValue):
                return values[self._key2orValue]
            return None
        return self._key2orValue

    def __str__(self):
        return "%s - %s %s %s" % ( self.__class__.__name__, self._key1, self._isKey, self._key2orValue )

    def __repr__(self):
        return "%s - %s %s %s" % ( self.__class__.__name__, self._key1, self._isKey, self._key2orValue )

class ParameterLogical(ParameterBase):
    # A test that consists of a set of sub tests.
    def __init__( self ):
        ParameterBase.__init__( self, None, list(), None )
        self._keySet = set()   # All the keys used by this Logical

    def addTest( self, tst ):
        self._key2orValue.append( tst )

    def parse( self, tstConfig ):
        errCount = 0
        for key in tstConfig:
            if key != '':
                _log.debug( "newTest %s - %s" % ( key, tstConfig[key] ) )
                if key == 'testEq':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createTest( self.getEqTest, tst )
                    else:
                        self.createTest( self.getEqTest, tstConfig[key] )
                elif key == 'testNe':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createTest( self.getNeTest, tst )
                    else:
                        self.createTest( self.getNeTest, tstConfig[key] )
                elif key == 'testGt':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createTest( self.getGtTest, tst )
                    else:
                        self.createTest( self.getGtTest, tstConfig[key] )
                elif key == 'testGe':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createTest( self.getGeTest, tst )
                    else:
                        self.createTest( self.getGeTest, tstConfig[key] )
                elif key == 'testLt':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createTest( self.getLtTest, tst )
                    else:
                        self.createTest( self.getLtTest, tstConfig[key] )
                elif key == 'testLe':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createTest( self.getLeTest, tst )
                    else:
                        self.createTest( self.getLeTest, tstConfig[key] )
                elif key == 'testDiffGe':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createDiffTest( self.getDiffGeTest, tst )
                    else:
                        self.createDiffTest( self.getDiffGeTest, tstConfig[key] )
                elif key == 'testDiffLe':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createDiffTest( self.getDiffLeTest, tst )
                    else:
                        self.createDiffTest( self.getDiffLeTest, tstConfig[key] )
                elif key == 'testAbsDiffGe':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createDiffTest( self.getAbsDiffGeTest, tst )
                    else:
                        self.createDiffTest( self.getAbsDiffGeTest, tstConfig[key] )
                elif key == 'testAbsDiffLe':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createDiffTest( self.getAbsDiffLeTest, tst )
                    else:
                        self.createDiffTest( self.getAbsDiffLeTest, tstConfig[key] )
                elif key == 'testChanged':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createChangedTest( self.getChangedTest, tst )
                    else:
                        self.createChangedTest( self.getChangedTest, tstConfig[key] )
                elif key == 'testAnd':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createAndTest( tst )
                    else:
                        self.createAndTest( tstConfig[key] )
                elif key == 'testOr':
                    # content may be a list of tests.
                    if isinstance( tstConfig[key], list ):
                        for tst in tstConfig[key]:
                            self.createOrTest( tst )
                    else:
                        self.createOrTest( tstConfig[key] )
                else:
                    _log.error( "Unrecognised test %s - %s" % ( key, tstConfig[key] ) )
                    errCount = errCount + 1

        # is it enabled?
        if _log.isEnabledFor(logging.DEBUG ):
            _log.debug( "ParameterSet loaded, tests" )
            _log.debug( "%s" % ( self._key2orValue ) )  # we are a ParameterAndList
            _log.debug( "keys" )
            for key in self._keySet:
                _log.debug( "%s" % ( key ) )
        _log.debug( "ParameterLogical parse exit" )
        
    def getType( self, paramType, val, isKey ):
        # return 0 for string
        # 1 for int
        # 2 for float
        if paramType == 'int':
            return 1
        elif paramType == 'float':
            return 2
        elif paramType == 'string':
            return 0
        elif isKey or val is None:
            return 0
        elif testInt.match(val):
            return 1
        elif testFloat.match(val):
            return 2
        return 0

    def createTest( self, func, tst ):
        newTst = ParameterOrList()
        key = tst['name']
        paramType = ''
        if tst.has_key('type'):
            paramType = tst['type']

        if tst.has_key('value'):
            # has explicit values
            values = tst['value']
            if isinstance( values, list ):
                for val in values:
                    if isinstance( val, dict ):
                        val = val['']
                    pti = self.getType( paramType, val, False )
                    newTst.addTest( func(pti, key, val, False) )
            else:
                if isinstance( values, dict ):
                    values = values['']
                pti = self.getType( paramType, values, False )
                newTst.addTest( func(pti, key, values, False) )

        if tst.has_key('param2'):
            # has second names 
            param2 = tst['param2']
            if isinstance( param2, list ):
                for key2 in param2:
                    if isinstance( key2, dict ):
                        key2 = key2['']
                    pti = self.getType( paramType, key2, True )
                    newTst.addTest( func(pti, key, key2, True) )
                    self._keySet.add( key2 )
            else:
                if isinstance( param2, dict ):
                    param2 = param2['']
                pti = self.getType( paramType, param2, True )
                newTst.addTest( func(pti, key, param2, True) )
                self._keySet.add( param2 )

        self._keySet.add( key )
        self.addTest( newTst )

    def createChangedTest( self, func, tst ):
        newTst = ParameterOrList()
        key = tst['name']
        paramType = ''
        if tst.has_key('type'):
            paramType = tst['type']
        pti = self.getType( paramType, None, False )
        newTst.addTest( func(pti, key) )

        self._keySet.add( key )
        self.addTest( newTst )

    def createDiffTest( self, func, tst ):
        newTst = ParameterOrList()
        key = tst['name']
        diffValue = tst['diffValue']
        paramType = ''
        if tst.has_key('type'):
            paramType = tst['type']

        if tst.has_key('value'):
            # has explicit values
            values = tst['value']
            if isinstance( values, list ):
                for val in values:
                    if isinstance( val, dict ):
                        val = val['']
                    pti = self.getType( paramType, val, False )
                    newTst.addTest( func(pti, key, val, diffValue, False) )
            else:
                if isinstance( values, dict ):
                    values = values['']
                pti = self.getType( paramType, values, False )
                newTst.addTest( func(pti, key, values, diffValue, False) )

        if tst.has_key('param2'):
            # has second names 
            param2 = tst['param2']
            if isinstance( param2, list ):
                for key2 in param2:
                    if isinstance( key2, dict ):
                        key2 = key2['']
                    pti = self.getType( paramType, key2, True )
                    newTst.addTest( func(pti, key, key2, diffValue, True) )
                    self._keySet.add( key2 )
            else:
                if isinstance( param2, dict ):
                    param2 = param2['']
                pti = self.getType( paramType, param2, True )
                newTst.addTest( func(pti, key, param2, diffValue, True) )
                self._keySet.add( param2 )

        self._keySet.add( key )
        self.addTest( newTst )

    def createAndTest( self, tst ):
        newTst = ParameterAndList()
        newTst.parse(tst)
        for k in newTst._keySet:
            self._keySet.add( k )
        self.addTest( newTst )

    def createOrTest( self, tst ):
        newTst = ParameterOrList()
        newTst.parse(tst)
        for k in newTst._keySet:
            self._keySet.add( k )
        self.addTest( newTst )

    def getEqTest( self, pti, key, valOrKey, isKey ):
        if pti == 1:
            newTst = ParameterIntEq(key, valOrKey, isKey)
        elif pti == 2:
            newTst = ParameterFloatEq(key, valOrKey, isKey)
        else:
            newTst = ParameterStrEq(key, valOrKey, isKey)
        return newTst

    def getNeTest( self, pti, key, valOrKey, isKey ):
        if pti == 1:
            newTst = ParameterIntNe(key, valOrKey, isKey)
        elif pti == 2:
            newTst = ParameterFloatNe(key, valOrKey, isKey)
        else:
            newTst = ParameterStrNe(key, valOrKey, isKey)
        return newTst

    def getLtTest( self, pti, key, valOrKey, isKey ):
        if pti == 1:
            newTst = ParameterIntLt(key, valOrKey, isKey)
        elif pti == 2:
            newTst = ParameterFloatLt(key, valOrKey, isKey)
        else:
            newTst = ParameterStrLt(key, valOrKey, isKey)
        return newTst

    def getLeTest( self, pti, key, valOrKey, isKey ):
        if pti == 1:
            newTst = ParameterIntLtEq(key, valOrKey, isKey)
        elif pti == 2:
            newTst = ParameterFloatLtEq(key, valOrKey, isKey)
        else:
            newTst = ParameterStrLtEq(key, valOrKey, isKey)
        return newTst

    def getGtTest( self, pti, key, valOrKey, isKey ):
        if pti == 1:
            newTst = ParameterIntGt(key, valOrKey, isKey)
        elif pti == 2:
            newTst = ParameterFloatGt(key, valOrKey, isKey)
        else:
            newTst = ParameterStrGt(key, valOrKey, isKey)
        return newTst

    def getGeTest( self, pti, key, valOrKey, isKey ):
        if pti == 1:
            newTst = ParameterIntGtEq(key, valOrKey, isKey)
        elif pti == 2:
            newTst = ParameterFloatGtEq(key, valOrKey, isKey)
        else:
            newTst = ParameterStrGtEq(key, valOrKey, isKey)
        return newTst

    def getDiffGeTest( self, pti, key, valOrKey, diffValue, isKey ):
        if pti == 1:
            newTst = ParameterIntDiffGtEq(key, valOrKey, diffValue, isKey)
        elif pti == 2:
            newTst = ParameterFloatDiffGtEq(key, valOrKey, diffValue, isKey)
        else:
            newTst = ParameterFloatDiffGtEq(key, valOrKey, diffValue, isKey)
            pass
            # throw error
        return newTst

    def getDiffLeTest( self, pti, key, valOrKey, diffValue, isKey ):
        if pti == 1:
            newTst = ParameterIntDiffLtEq(key, valOrKey, diffValue, isKey)
        elif pti == 2:
            newTst = ParameterFloatDiffLtEq(key, valOrKey, diffValue, isKey)
        else:
            newTst = ParameterFloatDiffLtEq(key, valOrKey, diffValue, isKey)
            pass
            # throw error
        return newTst

    def getAbsDiffGeTest( self, pti, key, valOrKey, diffValue, isKey ):
        if pti == 1:
            newTst = ParameterIntDiffAbsGtEq(key, valOrKey, diffValue, isKey)
        elif pti == 2:
            newTst = ParameterFloatDiffAbsGtEq(key, valOrKey, diffValue, isKey)
        else:
            newTst = ParameterFloatDiffAbsGtEq(key, valOrKey, diffValue, isKey)
            pass
            # throw error
        return newTst

    def getAbsDiffLeTest( self, pti, key, valOrKey, diffValue, isKey ):
        if pti == 1:
            newTst = ParameterIntDiffAbsLtEq(key, valOrKey, diffValue, isKey)
        elif pti == 2:
            newTst = ParameterFloatDiffAbsLtEq(key, valOrKey, diffValue, isKey)
        else:
            newTst = ParameterFloatDiffAbsLtEq(key, valOrKey, diffValue, isKey)
            pass
            # throw error
        return newTst

    def getChangedTest( self, pti, key ):
        if pti == 1:
            newTst = ParameterIntChanged(key)
        elif pti == 2:
            newTst = ParameterFloatChanged(key)
        else:
            newTst = ParameterStrChanged(key)
        return newTst

class ParameterOrList(ParameterLogical):
    def match( self, value ):
        result = False
        for tst in self._key2orValue:
            if tst.match( value ):
                result = True
        _log.debug( "ParameterOrList result %s tests %s values %s", result, self._key2orValue, value )
        return result

class ParameterAndList(ParameterLogical):
    def match( self, value ):
        result = len(self._key2orValue) > 0
        for tst in self._key2orValue:
            if not tst.match( value ):
                result = False
        _log.debug( "ParameterAndList result %s tests %s values %s", result, self._key2orValue, value )
        return result

class ParameterStrBase(ParameterBase):
    def __init__( self, key1, key2orValue, isKey=False ):
        ParameterBase.__init__( self, key1, key2orValue, isKey )

class ParameterStrChanged(ParameterStrBase):
    def __init__( self, key1 ):
        self._last = None
        ParameterStrBase.__init__( self, key1, None, False )
        
    def match( self, values ):
        v1 = self.value1(values)
        result = v1 is not None and (self._last is None or unicode(v1) != unicode(self._last) )
        _log.debug( "Changed: %s, '%s' '%s' ", result,v1, self._last)
        self._last = v1
        return result

class ParameterStrEq(ParameterStrBase):
    def match( self, values ):
        v1 = self.value1(values)
        v2 = self.value2(values)
        _log.debug( "Eq: '%s' '%s' ",v1,v2)
        return v1 is not None and v2 is not None and unicode(v1) == unicode(v2)

class ParameterStrNe(ParameterStrBase):
    def match( self, values ):
        v1 = self.value1(values)
        v2 = self.value2(values)
        _log.debug( "Ne: '%s' '%s' ",v1,v2)
        return v1 is not None and v2 is not None and unicode(v1) != unicode(v2)

class ParameterStrLt(ParameterStrBase):
    def match( self, values ):
        v1 = self.value1(values)
        v2 = self.value2(values)
        _log.debug( "Lt: '%s' '%s' ",v1,v2)
        return v1 is not None and v2 is not None and unicode(v1) < unicode(v2)

class ParameterStrLtEq(ParameterStrBase):
    def match( self, values ):
        v1 = self.value1(values)
        v2 = self.value2(values)
        _log.debug( "LtEq: '%s' '%s' ",v1,v2)
        return v1 is not None and v2 is not None and unicode(v1) <= unicode(v2)

class ParameterStrGt(ParameterStrBase):
    def match( self, values ):
        v1 = self.value1(values)
        v2 = self.value2(values)
        _log.debug( "Gt: '%s' '%s' ",v1,v2)
        return v1 is not None and v2 is not None and unicode(v1) > unicode(v2)

class ParameterStrGtEq(ParameterStrBase):
    def match( self, values ):
        v1 = self.value1(values)
        v2 = self.value2(values)
        _log.debug( "GtEq: '%s' '%s' ",v1,v2)
        return v1 is not None and v2 is not None and unicode(v1) >= unicode(v2)
    
class ParameterIntBase(ParameterBase):
    def __init__( self, key1, key2orValue, isKey=False ):
        ParameterBase.__init__( self, key1, key2orValue, isKey )

class ParameterIntChanged(ParameterIntBase):
    def __init__( self, key1 ):
        self._last = None
        ParameterIntBase.__init__( self, key1, None, False )
        
    def match( self, values ):
        try:
            v1 = int(self.value1(values))
        except TypeError:
            v1 = None
        except ValueError:
            v1 = None
        result = v1 is not None and (self._last is None or v1 != self._last )
        _log.debug( "Changed: %s, '%s' '%s' ", result,v1, self._last)
        self._last = v1
        return result

class ParameterIntEq(ParameterIntBase):
    def match( self, values ):
        #_log.debug( "'%s' : '%s'" % ( value, self._match ) )
        # can have issues where value is empty as int('') is an error
        try:
            return int(self.value1(values)) == int(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntNe(ParameterIntBase):
    def match( self, values ):
        #_log.debug( "'%s' : '%s'" % ( value, self._match ) )
        # can have issues where value is empty as int('') is an error
        try:
            return int(self.value1(values)) != int(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntLt(ParameterIntBase):
    def match( self, values ):
        try:
            return int(self.value1(values)) < int(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntLtEq(ParameterIntBase):
    def match( self, values ):
        try:
            return int(self.value1(values)) <= int(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntGt(ParameterIntBase):
    def match( self, values ):
        try:
            return int(self.value1(values)) > int(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntGtEq(ParameterIntBase):
    def match( self, values ):
        try:
            return int(self.value1(values)) >= int(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False
    
class ParameterIntDiffBase(ParameterIntBase):
    # Test the difference between key1 and key2 
    def __init__( self, key1, key2orValue, diffValue, isKey=False ):
        ParameterIntBase.__init__( self, key1, key2orValue, isKey )
        self._diffValue = int(diffValue)

    def diffValue(self,values):
        return int(self.value1(values)) - int(self.value2(values))

class ParameterIntDiffGtEq(ParameterIntDiffBase):
    def match( self, values ):
        try:
            return self.diffValue(values) >= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntDiffLtEq(ParameterIntDiffBase):
    def match( self, values ):
        try:
            return self.diffValue(values) <= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntDiffAbsGtEq(ParameterIntDiffBase):
    def match( self, values ):
        try:
            return abs(self.diffValue(values)) >= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterIntDiffAbsLtEq(ParameterIntDiffBase):
    def match( self, values ):
        try:
            return abs(self.diffValue(values)) <= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatBase(ParameterBase):
    def __init__( self, key1, key2orValue, isKey=False ):
        ParameterBase.__init__( self, key1, key2orValue, isKey )

class ParameterFloatChanged(ParameterFloatBase):
    def __init__( self, key1 ):
        self._last = None
        ParameterFloatBase.__init__( self, key1, None, False )
        
    def match( self, values ):
        try:
            v1 = float(self.value1(values))
        except TypeError:
            v1 = None
        except ValueError:
            v1 = None
        result = v1 is not None and (self._last is None or v1 != self._last )
        _log.debug( "Changed: %s, '%s' '%s' ", result,v1, self._last)
        self._last = v1
        return result

class ParameterFloatEq(ParameterFloatBase):
    def match( self, values ):
        try:
            return float(self.value1(values)) == float(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatNe(ParameterFloatBase):
    def match( self, values ):
        try:
            return float(self.value1(values)) != float(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatLt(ParameterFloatBase):
    def match( self, values ):
        try:
            return float(self.value1(values)) < float(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatLtEq(ParameterFloatBase):
    def match( self, values ):
        try:
            return float(self.value1(values)) <= float(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatGt(ParameterFloatBase):
    def match( self, values ):
        try:
            return float(self.value1(values)) > float(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatGtEq(ParameterFloatBase):
    def match( self, values ):
        try:
            return float(self.value1(values)) >= float(self.value2(values))
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatDiffBase(ParameterFloatBase):
    # Test the difference between key1 and key2 
    def __init__( self, key1, key2orValue, diffValue, isKey=False ):
        ParameterFloatBase.__init__( self, key1, key2orValue, isKey )
        self._diffValue = float(diffValue)

    def diffValue(self,values):
        return float(self.value1(values)) - float(self.value2(values))

class ParameterFloatDiffGtEq(ParameterFloatDiffBase):
    def match( self, values ):
        try:
            return self.diffValue(values) >= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatDiffLtEq(ParameterFloatDiffBase):
    def match( self, values ):
        try:
            return self.diffValue(values) <= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatDiffAbsGtEq(ParameterFloatDiffBase):
    def match( self, values ):
        try:
            return abs(self.diffValue(values)) >= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterFloatDiffAbsLtEq(ParameterFloatDiffBase):
    def match( self, values ):
        try:
            return abs(self.diffValue(values)) <= self._diffValue
        except TypeError:
            return False
        except ValueError:
            return False

class ParameterSet(ParameterAndList):
    def __init__( self, tstConfig ):
        ParameterAndList.__init__( self)
        errCount = self.parse(tstConfig)
        if errCount > 0:
            # TODO throw an error exception.
            pass

    def uses( self, name ):
        """ quick check on whether a change means we should be scanned TODO """
        return name in self._keySet

    def match( self, allValues ):
        """ allValues is a complete dictionary of name value pairs """

        return ParameterAndList.match( self, allValues)

    def keys(self):
        return self._keySet

# End.
