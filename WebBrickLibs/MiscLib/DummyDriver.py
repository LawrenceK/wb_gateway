# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 


class DummyProtocolHandler():

    def Encode( self,Message ):
        message = Message + "success!"
        return message

    def Decode( self,Message ):
        message = "testmessage"
        return message
        
class DummyDriver():

    def GetCommand( self , Params ):
        return "turn lights on"        

    def GetEvent( self , Paramas ):
        #extract the useful information from the incomming message
        #create an event based on it
        events = []
        events.append({"source": "light1/on" , "type" : "lighting/update" , "payload":{"lightval" : "1"} } )
        return events
