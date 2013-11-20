
import urllib
import time

class SitePlayer:
    
    def __init__(self,IP,username,password):
        assert IP.find('/') == -1
        self.address = "http://%s:%s@%s" %(username,password,IP)     
        self.username = username
        self.password = password    
      
    def SitePlayerAvailable(self):
        try:
            test = urllib.urlopen(self.address)
            t = test.read()
            assert t.find("SitePlayer Telnet Setup") != -1
            return True
        except Exception , e :
            return False
            
            
    def GetName(self):
        servicesUrl = urllib.urlopen(self.address+'/services.html')
        servicesHtml = servicesUrl.read()
        nameIndex = servicesHtml.find("""("Device Name:","device",""")
        for x in range(nameIndex+26,len(servicesHtml)):
            if ord(servicesHtml[x]) == 34:
                return servicesHtml[nameIndex+26:x]
        return ''       
    def SetName(self,newName):
        assert type(newName) == str
        params = urllib.urlencode({'device':newName,'change':"Change Device Name"})
        url = urllib.urlopen(self.address + "/device.cgi?%s" %params)
        response = url.read()
        assert response.find("Restarting. Please wait") != -1
    def SetDHCPOn(self):
        params = urllib.urlencode({'dhcp':'ON','reset':"Set DHCP Configuration"})
        url = urllib.urlopen(self.address + "/dhcp.cgi?%s" %params)
        response = url.read()
        assert response.find("Restarting. Please wait") != -1    
        
    def SetIp(self,newIP):
        assert type(newIP) == str
        ipStrings = newIP.split('.')
        assert len(ipStrings) == 4
        params = urllib.urlencode({'dhcp':'OFF','reset':"Set DHCP Configuration"})
        url = urllib.urlopen(self.address + "/dhcp.cgi?%s" %params)
        response = url.read()
        assert response.find("Restarting. Please wait") != -1    
        time.sleep(2)
        
        params = urllib.urlencode({'F1IP1':ipStrings[0],'F1IP2':ipStrings[1],'F1IP3':ipStrings[2],'F1IP4':ipStrings[3],'set':'Set Fixed IPs'})
        url = urllib.urlopen(self.address + "/staticip.cgi?%s" %params)
        response = url.read()
        assert response.find("Restarting. Please wait") != -1    
        self.address = "http://%s:%s@%s" %(self.username,self.password,newIP) 
