


def main():
    streamUri =  GetStreamUrl("192.168.1.113")
    wrapper = ExterityWrapper("admin","labrador","192.168.1.200")
    wrapper.SetStreamUri(streamUri)

import httplib , base64 , urllib
from time import sleep
import socket
import binascii

def GetStreamUrl(address , retrys = 3):
    MCAST_GRP = '239.255.255.255' 
    MCAST_PORT = 9875
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    sock.bind(('', MCAST_PORT))
    host = socket.gethostbyname(socket.gethostname())
    print "Host: %s" % host
    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton('192.168.1.14'))
    #TODO Bind to an interface passed in on constructor, hardcoded for now
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MCAST_GRP) + socket.inet_aton('192.168.1.14'))
    timeoutlimit = 2
    timeouts = 0
    ip = ''
    retry = 0
    url = ''
    while ip != address:
        try:
            print "Waiting for Packet from %s...." %address
            data, addr = sock.recvfrom(1024)
            ip = addr[0]           
            start = data.find("m=")
            end = data[start+2:].find("\r\n")
            temp = data[start+2:][:end]
            #this should get us a message on the lines of "video 49408 udp 33" , which contains the port and video type information we need
            start = temp.find("video ")
            end = temp.find(" udp")
            port = temp[start+6:end]
            
            start = temp.find("udp ")
            videotype = temp[start+4:]
            
            start = data.find("c=IN IP4 ")
            end = data[start+9:].find("/255\r\n")
            streamip = data[start+9:][:end]
            url = "udp://%s:%s?format=%s" %(streamip,port,videotype)
                            
            print 'Received SAP from Ip = %s' %str(addr)
            retry +=1
        except socket.error, e:
            timeouts += 1
        finally:
            if timeouts > timeoutlimit:
                break
            if retry > retrys:
                break
    return url
class ExterityWrapper():
    def __init__(self,Username,Password,Address):
        self._addr = Address
        self._user = Username
        self._password = Password
        self._auth = 'Basic ' + base64.encodestring(self._user + ':' + self._password)
    
    def SetStreamUri(self,Uri):
        conn = httplib.HTTPConnection(self._addr)

        headers = {"Content-type": "application/x-www-form-urlencoded","Authorization": self._auth}

        cDict = {}
        cDict["Uri"] = Uri
        cDict["UseRawUri"] = "yes"
        ipParams = urllib.urlencode(cDict)

        conn.request("POST","/cgi-bin/channels.cgi?"+ipParams,None,headers)

        response = conn.getresponse()
        conn.close()
        print response.read()
        print "Connection gave %s with %s" % (response.status,response.reason)

        return response.status
                            
           
if __name__ == '__main__':
    main()            
