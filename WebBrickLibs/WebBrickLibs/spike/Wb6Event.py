# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $id:$
#
#  Class to handle UDP
#
#  Lawrence Klyne
#
#
from WbEvent import WbEventOther

# accessor to UDP data from webbrick 6.
class Wb6Event(WbEventOther):
    """
    Creates an event from a UDP packet from a version 6 webbrick
    """
    def __init__ (self, adr, data):
        """
        data is the array of bytes fom the network.
        """
        WbEventOther.__init__ (self, u'http://id.webbrick.co.uk/events/webbrick/' + data[2:4], u'webbrick', dict() )

        self._other_data["ipAdr"] = str(adr[0])
        self._other_data["udpType"] = data[1]
        self._other_data["pktType"] = data[2:4]
        self._other_data["version"] = 6

        if ( self._other_data["pktType"] == "NN" ) or ( self._other_data["pktType"] == "AA" ):
            self._other_data["macAdr"] = "%02X:%02X:%02X:%02X:%02X:%02X" % (ord(data[4]), ord(data[5]),ord(data[6]),ord(data[7]),ord(data[8]),ord(data[9]) )
            self._source = u'webbrick/%s/%s' % (self._other_data["ipAdr"],self._other_data["pktType"])
        elif ( self._other_data["pktType"] == "RR" ):
            self._other_data["rtc"] = [ord(data[4]), ord(data[5]),ord(data[6]),ord(data[7]),ord(data[8]),ord(data[9]),ord(data[10]),ord(data[11]) ]
            self._source = u'webbrick/%s' % self._other_data["ipAdr"]
        else:
            self._other_data["fromNode"] = ord(data[7])

            if ( self._other_data["pktType"] == "SS" ):
                pass
            elif ( self._other_data["pktType"] == "ST" ):
                self._other_data["hour"] = ord(data[4])
                self._other_data["minute"] = ord(data[5])
                self._other_data["resetCode"] = ord(data[6])
                self._other_data["second"] = ord(data[8])
                self._other_data["day"] = ord(data[9])
                self._other_data["uptime"] = (ord(data[10]) * 256) + ord(data[11])
            elif ( self._other_data["pktType"] == "DB" ):
                self._other_data["uptime"] = (ord(data[5]) * 256) + ord(data[4])
                self._other_data["debug"] = "%x:%x:%x:%x:%x:%x" % data[6:11]
            elif ( self._other_data["pktType"] == "AO" ):
                self._other_data["srcChannel"] = ord(data[4])
                self._other_data["val"] = (ord(data[10]) * 256) + ord(data[11])
            elif ( self._other_data["pktType"] == "AI" ):
                self._other_data["srcChannel"] = ord(data[4])
                self._other_data["val"] = (ord(data[10]) * 256) + ord(data[11])
            elif ( self._other_data["pktType"][0] == "T" ):
                self._other_data["srcChannel"] = ord(data[4])
                self._other_data["tgtChannel"] = ord(data[5]) & 0x1F
                #self._other_data["val"] = (ord(data[10]) * 256) + ord(data[11])
                self._other_data["action"] = ord(data[6]) & 0xF
                self._other_data["dwell"] = ord(data[6]) >> 4
                self._other_data["setPoint"] = ord(data[9])
                if ( self._other_data["pktType"][1] == "D" ):
                    self._other_data["val"] = (ord(data[10]) * 256) + ord(data[11])
                elif ( self._other_data["pktType"][1] == "R" ):
                    self._other_data["toNode"] = ord(data[8])
            elif ( self._other_data["pktType"] == "DO" ):
                self._other_data["srcChannel"] = ord(data[4])
                action=ord(data[6]) & 0xF
                if action == 2:
                    self._other_data["state"] = 1
                else:
                    self._other_data["state"] = 0
            elif ( self._other_data["pktType"] == "IR" ):
                self._other_data["irAddress"] = ord(data[8])
                self._other_data["irChannel"] = ord(data[5])
            elif ( self._other_data["pktType"] == "CT" ):
                self._other_data["srcChannel"] = ord(data[4])
                tmp = (((ord(data[10]) & 0x0F) * 256) + ord(data[11]))
                if tmp > 2047:
                    tmp = tmp-4096  # negative
                self._other_data["val"] = tmp / 16.0
            else:
                # Unrecognised event type...
                self._other_data["srcChannel"] = ord(data[4])
                self._other_data["tgtType"] = ord(data[5]) >> 6
                self._other_data["tgtChannel"] = ord(data[5]) & 0x1F
                self._other_data["action"] = ord(data[6]) & 0xF
                self._other_data["dwell"] = ord(data[6]) >> 4
                self._other_data["toNode"] = ord(data[8])
                self._other_data["setPoint"] = ord(data[9])
                self._other_data["val"] = (ord(data[10]) * 256) + ord(data[11])

            if self._other_data.has_key("srcChannel"):
                self._source = u'webbrick/%i/%s/%i' % (self._other_data["fromNode"],self._other_data["pktType"],self._other_data["srcChannel"])
            elif self._other_data.has_key("irAddress"):
                self._source = u'webbrick/%i/%s/%i/%i' % (self._other_data["fromNode"],self._other_data["pktType"],self._other_data["irAddress"],self._other_data["irChannel"])
            else:
                self._source = u'webbrick/%i' % self._other_data["fromNode"]

