# $Id: testutils.py 2612 2008-08-11 20:08:49Z graham.klyne $
"""
Test upnp.core.utils
"""
import sys
import string
import unittest
import logging

from coherence.upnp.core.utils import *

# This data is joined using CRLF pairs.
testChunkedData = ['200',
'<?xml version="1.0" ?> ',
'<root xmlns="urn:schemas-upnp-org:device-1-0">',
'	<specVersion>',
'		<major>1</major> ',
'		<minor>0</minor> ',
'	</specVersion>',
'	<device>',
'		<deviceType>urn:schemas-upnp-org:device:MediaRenderer:1</deviceType> ',
'		<friendlyName>DMA201</friendlyName> ',
'		<manufacturer>   </manufacturer> ',
'		<manufacturerURL>   </manufacturerURL> ',
'		<modelDescription>DMA201</modelDescription> ',
'		<modelName>DMA</modelName> ',
'		<modelNumber>201</modelNumber> ',
'		<modelURL>   </modelURL> ',
'		<serialNumber>0',
'200',
'00000000001</serialNumber> ',
'		<UDN>uuid:BE1C49F2-572D-3617-8F4C-BB1DEC3954FD</UDN> ',
'		<UPC /> ',
'		<serviceList>',
'			<service>',
'				<serviceType>urn:schemas-upnp-org:service:ConnectionManager:1</serviceType>',
'				<serviceId>urn:upnp-org:serviceId:ConnectionManager</serviceId>',
'				<controlURL>http://10.63.1.113:4444/CMSControl</controlURL>',
'				<eventSubURL>http://10.63.1.113:4445/CMSEvent</eventSubURL>',
'				<SCPDURL>/upnpdev.cgi?file=/ConnectionManager.xml</SCPDURL>',
'			</service>',
'			<service>',
'				<serv',
'223',
'iceType>urn:schemas-upnp-org:service:AVTransport:1</serviceType>',
'				<serviceId>urn:upnp-org:serviceId:AVTransport</serviceId>',
'				<controlURL>http://10.63.1.113:4444/AVTControl</controlURL>',
'				<eventSubURL>http://10.63.1.113:4445/AVTEvent</eventSubURL>',
'				<SCPDURL>/upnpdev.cgi?file=/AVTransport.xml</SCPDURL>',
'			</service>',
'			<service>',
'				<serviceType>urn:schemas-upnp-org:service:RenderingControl:1</serviceType>',
'				<serviceId>urn:upnp-org:serviceId:RenderingControl</serviceId>',
'				<controlURL>http://10.63.1.113:4444/RCSControl</',
'c4',
'controlURL>',
'				<eventSubURL>http://10.63.1.113:4445/RCSEvent</eventSubURL>',
'				<SCPDURL>/upnpdev.cgi?file=/RenderingControl.xml</SCPDURL>',
'			</service>',
'		</serviceList>',
'	</device>',
'</root>'
'',
'0',
'']

testChunkedDataResult = ['<?xml version="1.0" ?> ',
'<root xmlns="urn:schemas-upnp-org:device-1-0">',
'	<specVersion>',
'		<major>1</major> ',
'		<minor>0</minor> ',
'	</specVersion>',
'	<device>',
'		<deviceType>urn:schemas-upnp-org:device:MediaRenderer:1</deviceType> ',
'		<friendlyName>DMA201</friendlyName> ',
'		<manufacturer>   </manufacturer> ',
'		<manufacturerURL>   </manufacturerURL> ',
'		<modelDescription>DMA201</modelDescription> ',
'		<modelName>DMA</modelName> ',
'		<modelNumber>201</modelNumber> ',
'		<modelURL>   </modelURL> ',
'		<serialNumber>000000000001</serialNumber> ',
'		<UDN>uuid:BE1C49F2-572D-3617-8F4C-BB1DEC3954FD</UDN> ',
'		<UPC /> ',
'		<serviceList>',
'			<service>',
'				<serviceType>urn:schemas-upnp-org:service:ConnectionManager:1</serviceType>',
'				<serviceId>urn:upnp-org:serviceId:ConnectionManager</serviceId>',
'				<controlURL>http://10.63.1.113:4444/CMSControl</controlURL>',
'				<eventSubURL>http://10.63.1.113:4445/CMSEvent</eventSubURL>',
'				<SCPDURL>/upnpdev.cgi?file=/ConnectionManager.xml</SCPDURL>',
'			</service>',
'			<service>',
'				<serviceType>urn:schemas-upnp-org:service:AVTransport:1</serviceType>',
'				<serviceId>urn:upnp-org:serviceId:AVTransport</serviceId>',
'				<controlURL>http://10.63.1.113:4444/AVTControl</controlURL>',
'				<eventSubURL>http://10.63.1.113:4445/AVTEvent</eventSubURL>',
'				<SCPDURL>/upnpdev.cgi?file=/AVTransport.xml</SCPDURL>',
'			</service>',
'			<service>',
'				<serviceType>urn:schemas-upnp-org:service:RenderingControl:1</serviceType>',
'				<serviceId>urn:upnp-org:serviceId:RenderingControl</serviceId>',
'				<controlURL>http://10.63.1.113:4444/RCSControl</controlURL>',
'				<eventSubURL>http://10.63.1.113:4445/RCSEvent</eventSubURL>',
'				<SCPDURL>/upnpdev.cgi?file=/RenderingControl.xml</SCPDURL>',
'			</service>',
'		</serviceList>',
'	</device>',
'</root>',
''
]

class TestUpnpUtils(unittest.TestCase):

    def setUp(self):
        self._log = logging.getLogger( "TestUpnpUtils" )
        return

    def tearDown(self):
        return

    def testChunked(self):
        testData = string.join( testChunkedData, '\r\n' )
        self._log.debug( testData )
        newData = de_chunk_payload(testData)
        self._log.debug( newData )
        # see whether we can parse the result
        self.assertEqual(newData, string.join( testChunkedDataResult, '\r\n' ))

def getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestUpnpUtils("testChunked"))
    return suite

# Run unit tests directly from command line
if __name__ == "__main__":

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)
        tests = TestUpnpUtils( sys.argv[1] )
    else:
        logging.basicConfig(level=logging.ERROR)
        tests = getTestSuite()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)

# $Id: testutils.py 2612 2008-08-11 20:08:49Z graham.klyne $
