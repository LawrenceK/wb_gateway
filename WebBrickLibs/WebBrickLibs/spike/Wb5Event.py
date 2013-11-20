# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
from WbEvent import WbEventOther

# accessor to UDP data from webbrick 5
class Wb5Event(WbEventOther):
    """
    Creates an event from a UDP packet received from a version 5 webbrick
    """
    def __init__ (self, adr, data):

        WbEventOther.__init__ (self, u'http://id.webbrick.co.uk/events/webbrick/', u'webbrick', dict() )

        self._other_data["ipAdr"] = str(adr[0])
        self._other_data["udpType"] = "G"
        self._other_data["pktType"] = "??"
        self._other_data["version"] = 5

        if ( data[0] == "R" ):
            self._other_data["pktType"] = "TD"
            self._other_data["udpType"] = "R"
            self._other_data["toNode"] = ord(data[1])
            self._other_data["tgtChannel"] = ord(data[3])
            if ( data[2] == "D" ):
                self._other_data["tgtType"] = 0
            else:
                # analogue
                self._other_data["tgtType"] = 2
                self._other_data["setPoint"] = ord(data[5])
        elif ( data[0:2] == "NN" ):
            self._other_data["pktType"] = "NN"
            # thats it
        elif ( data[0:2] == "LT" ):
            self._other_data["udpType"] = "A"
            self._other_data["pktType"] = "Tt"
            self._other_data["fromNode"] = ord(data[2])
            self._other_data["val"] = ord(data[3]) * 16   # into 1/16ths to match DS18B20/Wb6
            # high or low? use temperature and limits to decide.
            if ( ord(data[3]) > ord(data[6]) ) :
                self._other_data["pktType"] = "TT"
        elif ( data[0:2] == "LA" ):
            self._other_data["udpType"] = "A"
            self._other_data["pktType"] = "Ta"
            self._other_data["fromNode"] = ord(data[3])
            if ( ord(data[2]) == "H" ) :
                self._other_data["pktType"] = "TA"
            self._other_data["val"] = ord(data[4]) + ( ord(data[5]) << 8)
        elif ( data[0:2] == "DI" ):
            self._other_data["pktType"] = "TD"
            self._other_data["fromNode"] = ord(data[2])
            self._other_data["srcChannel"] = ord(data[3])
            # UDPString[4] = operand ;  // Ignore
        elif ( data[0:2] == "LI" ):
            # digital in generated alarm packet
            self._other_data["udpType"] = "A"
            self._other_data["pktType"] = "TD"
            self._other_data["fromNode"] = ord(data[2])
            self._other_data["srcChannel"] = ord(data[3])
        elif ( data[0:2] == "St" ):
            self._other_data["pktType"] = "SS"
            self._other_data["fromNode"] = ord(data[5])
        else:
            self._other_data["pktType"] = data[0:2]

        self._type = u'http://id.webbrick.co.uk/events/webbrick/%s' % self._other_data["pktType"] 
        if self._other_data.has_key("fromNode"):
            if self._other_data.has_key("srcChannel"):
                self._source = u'webbrick/%i/%s/%i' % (self._other_data["fromNode"],self._other_data["pktType"],self._other_data["srcChannel"])
            else:
                self._source = u'webbrick/%i' % self._other_data["fromNode"]
        else:
            self._source = u'webbrick/%s' % self._other_data["ipAdr"]


#
# WebBrick UDP event packets
#
