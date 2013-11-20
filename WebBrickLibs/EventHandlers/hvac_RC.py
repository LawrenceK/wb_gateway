

class RoomController():
    def __init__(self,cfgDict):
        """ inputDict is what we use to map analoginputs to offsets
            Should be formatted like so
                                    { (minimum,maximum) : offset , (minimum,maximum) : offset  } 
        """
        self.zonekey = cfgDict["roomcontroller"]["zonekey"]
        self.offsetMap = self.buildMap(cfgDict["roomcontroller"]["offsets"])
    
    def buildMap(self,cfgDict):
        offsetDict = {}
        for offset in cfgDict:
            #just check we have the required keys
            if offset.has_key("min"):
                if offset.has_key("max"):
                    if offset.has_key("offset"):
                        if offsetDict.has_key((int(offset["min"]) , int(offset["max"]))):
                            raise Exception("Duplicate offset range!")
                        else:
                            offsetDict[ (int(offset["min"]) , int(offset["max"])) ] = offset["offset"]                       
                    else:
                        log("RoomController : No offset specified")
                else:
                    log("RoomController : No maximum value specified")
            else:
                log("RoomController : No Minimum value specified")
        #created a rangedict from our dictionary of values
        rangeDict = RangedDictionary(offsetDict)
        return rangeDict

    def getOffset(self,value):
        #value must be of type int     
        return self.offsetMap[value]
        
        
class RangedDictionary():
        def __init__(self,rangeDict):
            "rangeDict is of the format { (min,max) : val } "
            if self.checkOverlap(rangeDict):
                self.rangeDict = rangeDict
            else:
                raise Exception("Overlap in ranges, invalid rangemap")
                
        
        def __getitem__(self, key):
            for rangeX in self.rangeDict:
                if key >= rangeX[0] and key <= rangeX[1]:
                    return self.rangeDict[rangeX]
            #throw keyerror exception here ?
            return None           
        def checkOverlap(self,rangedict):
            checkDict = {}
            for rangeX in rangedict:    
                for x in range(rangeX[0],rangeX[1]):
                    if checkDict.has_key(x):
                        return False
                    else:
                        checkDict[x] = 0
            return True
                    
