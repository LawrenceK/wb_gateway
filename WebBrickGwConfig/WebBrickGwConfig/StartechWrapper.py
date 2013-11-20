
import urllib
import time
import logging

#list of strings used when screen scraping the setup page
#chr 34 is a quotation mark
CTIP_STRING = """set("ctIP",""" + chr(34)
CTMASK_STRING = """set("ctMask",""" + chr(34)
CTGATEWAY_STRING = """set("ctGateway",""" + chr(34)
CTNETSPEED_STRING = """choose("ctNetSpeed",""" 
CTDHCP_STRING = """choose("ctDHCP","""
CTSIOPORT_STRING = """set("ctSioPort","""
CTSIOMODE_STRING = """choose("ctSioMode","""
CTDIOPORT_STRING = """set("ctDioPort","""
CTDIOMODE_STRING = """choose("ctDioMode","""
CTHOSTIP_STRING = """set("ctHostIP",""" + chr(34)
CTHOSTPORT_STRING = """set("ctHostPort","""
CTSIOBAUD_STRING = """choose("ctSioBaud","""
CTSIOPARITY_STRING = """choose("ctSioParity","""
CTSIOBITS_STRING = """choose("ctSioBits","""
CTSIOSTOPS_STRING = """choose("ctSioStops","""
CTSIOTYPE_STRING = """choose("ctSioType","""
CTAUTOCON_STRING = """choose("ctAutoCon","""
CTPKTMODE_STRING = """choose("ctPktMode","""
CTINACTIVE_STRING = """set("ctInactive","""
CTDEVICEID_STRING = """set("ctDeviceID","""
CTREPORTID_STRING = """choose("ctReportID","""
CTWEBPORT_STRING = """choose("ctWebPort","""
CTPASSWORD_STRING = """set("ctPassword",""" + chr(34)

class StartechWrapper:
    
    def __init__(self,IP,password):
        #TODO assert ip is a valid ip
        assert IP.find('/') == -1
        self.ip = IP
        self.password = password    
        self.html = ''
        self._settings = {}
     
    #a check to see if a startech device is there and our password is correct    
    def Present(self):
        params = urllib.urlencode({'ctPassword': self.password , 'ctLogin' : 'Login'})
        test = urllib.urlopen("http://%s/Setup.htm" %self.ip , params)
        self.html = test.read()
        assert self.html.find("<title>Setup</title>") != -1
        return True
        
    def GetSettings(self):
        self.__updateSettings()
        return self._settings
    
    def SetSettings(self,Settings):
        
        params = {}
        params["ctIP"] = Settings["IP"]
        params["ctMask"] = Settings["Mask"]
        params["ctGateway"] = Settings["Gateway"]
        params["ctNetSpeed"] = Settings["NetSpeed"]
        params["ctDHCP"] = Settings["DHCP"]
        params["ctSioPort"] = Settings["SioPort"]
        params["ctSioMode"] = Settings["SioMode"]
        params["ctDioPort"] = Settings["DioPort"]
        params["ctDioMode"] = Settings["DioMode"]
        params["ctHostPort"] = Settings["HostPort"]
        
        #Baud setting is an enumeration
        if Settings["SioBaud"] == '300':
            self._settings["SioBaud"] = '0'
        elif Settings["SioBaud"] == '600':
            self._settings["SioBaud"] = '1'
        elif Settings["SioBaud"] == '1200':
            self._settings["SioBaud"] = '2'
        elif Settings["SioBaud"] == '2400':
            self._settings["SioBaud"] = '3'
        elif Settings["SioBaud"] == '4800':
            self._settings["SioBaud"] = '4'
        elif Settings["SioBaud"] == '9600':
            self._settings["SioBaud"] = '5'
        elif Settings["SioBaud"] == '19200':
            self._settings["SioBaud"] = '6'
        elif Settings["SioBaud"] == '38400':
            self._settings["SioBaud"] = '7'
        elif Settings["SioBaud"] == '57600':
            self._settings["SioBaud"] = '8'
        elif Settings["SioBaud"] == '115200':
            self._settings["SioBaud"] = '9'
            
        params["ctSioParity"] = Settings["SioParity"]
        params["ctSioBits"] = Settings["SioBits"]
        params["ctSioStops"] = Settings["SioStops"]
        params["ctSioType"] = Settings["SioType"]
        params["ctAutoCon"] = Settings["AutoCon"]
        params["ctPktMode"] = Settings["PktMode"]
        params["ctInactive"] = Settings["Inactive"]
        params["ctDeviceID"] = Settings["DeviceID"]
        params["ctReportID"] = Settings["ReportID"]
        params["ctWebPort"] = Settings["WebPort"]
        params["ctPassword"] = Settings["Password"]
        
        #this parameter to tell the startech device we want to update the settings
        params["bSave"] = "Update"
        
        params = urllib.urlencode(params)
        url = urllib.urlopen("http://%s/Update.htm" %self.ip  , params)
        self.html = url.read()
        assert self.html.find("""<h3 align="center">Controller updated</h3>""") != -1
        #the device is rebooting at this point, incase we changed the ip or password we need to save those changes
        self.ip = Settings["IP"]
        self.password = Settings["Password"]
        #sleep so the device has time to reboot
        time.sleep(2)
        #grab settings from the device and ensure they are the same as the ones we sent it
        assert self.GetSettings() == Settings
        
    def __updateSettings(self):
        #this updates self._settings to be a dictionary representing the current device settings
        params = urllib.urlencode({'ctPassword': self.password , 'ctLogin' : 'Login'})
        test = urllib.urlopen("http://%s/Setup.htm" %self.ip , params)
        self.html = test.read()        
        
        self._settings["IP"] = self.__getSetting(self.html,CTIP_STRING,34)
        
        self._settings["Mask"] = self.__getSetting(self.html,CTMASK_STRING,34)
        
        self._settings["Gateway"] = self.__getSetting(self.html,CTGATEWAY_STRING,34)
        
        self._settings["NetSpeed"] = self.__getSetting(self.html,CTNETSPEED_STRING,41)
        
        self._settings["DHCP"] = self.__getSetting(self.html,CTDHCP_STRING,41)
        
        self._settings["SioPort"] = self.__getSetting(self.html,CTSIOPORT_STRING,41)
        
        self._settings["SioMode"] = self.__getSetting(self.html,CTSIOMODE_STRING,41)
        
        self._settings["DioPort"] = self.__getSetting(self.html,CTDIOPORT_STRING,41)
        
        self._settings["DioMode"] = self.__getSetting(self.html,CTDIOMODE_STRING,41)
        
        self._settings["HostIP"] = self.__getSetting(self.html,CTHOSTIP_STRING,34)
        
        self._settings["HostPort"] = self.__getSetting(self.html,CTHOSTPORT_STRING,41)   
        #baud is an enumeration so change it to something that means something
        baudenum = self.__getSetting(self.html,CTSIOBAUD_STRING,41)
        if baudenum == '0':
            self._settings["SioBaud"] = '300'
        elif baudenum == '1':
            self._settings["SioBaud"] = '600'
        elif baudenum == '2':
            self._settings["SioBaud"] = '1200'
        elif baudenum == '3':
            self._settings["SioBaud"] = '2400'
        elif baudenum == '4':
            self._settings["SioBaud"] = '4800'
        elif baudenum == '5':
            self._settings["SioBaud"] = '9600'
        elif baudenum == '6':
            self._settings["SioBaud"] = '19200'
        elif baudenum == '7':
            self._settings["SioBaud"] = '38400'
        elif baudenum == '8':
            self._settings["SioBaud"] = '57600'
        elif baudenum == '9':
            self._settings["SioBaud"] = '115200'
        else:
            self._settings["SioBaud"] = baudenum
            
        self._settings["SioParity"] = self.__getSetting(self.html,CTSIOPARITY_STRING,41)
        
        self._settings["SioBits"] = self.__getSetting(self.html,CTSIOBITS_STRING,41)
        
        self._settings["SioStops"] = self.__getSetting(self.html,CTSIOSTOPS_STRING,41)
        
        self._settings["SioType"] = self.__getSetting(self.html,CTSIOTYPE_STRING,41)
        
        self._settings["AutoCon"] = self.__getSetting(self.html,CTAUTOCON_STRING,41)
        
        self._settings["PktMode"] = self.__getSetting(self.html,CTPKTMODE_STRING,41)
        
        self._settings["Inactive"] = self.__getSetting(self.html,CTINACTIVE_STRING,41)
        
        self._settings["DeviceID"] = self.__getSetting(self.html,CTDEVICEID_STRING,41)
        
        self._settings["ReportID"] = self.__getSetting(self.html,CTREPORTID_STRING,41)
        
        self._settings["WebPort"] = self.__getSetting(self.html,CTWEBPORT_STRING,41)
        
        self._settings["Password"] = self.__getSetting(self.html,CTPASSWORD_STRING,34)
        
        return self._settings
    #searches through a string looking for the idstring, then returns upto the terminator, the terminator should be a decimal representation of the terminating character
    #this is to deal with non ascii characters and odd characters like quotation marks
    def __getSetting(self,html,idstring,terminator):
    
        index = html.find(idstring)            
        for x in range(index+len(idstring),len(html)):
            if ord(html[x]) == terminator:
                return self.html[index+len(idstring):x]
                    
        
              
       

