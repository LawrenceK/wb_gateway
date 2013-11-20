# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

#import string
import socket
#import os, sys
#import traceback
import logging

from twisted.internet import defer, reactor
from twisted.web import server, resource

from coherence import __version__

from coherence.upnp.core.utils import get_ip_address, get_host_address

from coherence.upnp.core.utils import Site

_log = logging.getLogger( "coherence.WebServer" )

class SimpleRoot(resource.Resource):
    addSlash = True

    def __init__(self, ws):
        resource.Resource.__init__(self)
        self.ws = ws

    def getChild(self, name, request):
        _log.info('SimpleRoot getChild %s, %s', name, request)
        try:
            return self.ws.children[name]
        except:
            return self

    def listchilds(self, uri):
        _log.info('listchilds %s', uri)
        if uri[-1] != '/':
            uri += '/'
        cl = ''
        for c in self.ws.children:
            device = self.ws.get_device_with_id(c)
            if device != None:
                _,_,_,device_type,version = device.get_device_type().split(':')
                cl +=  '<li><a href=%s%s>%s:%s %s</a></li>' % (
                                        uri,c,
                                        device_type.encode('utf-8'), version.encode('utf-8'),
                                        device.get_friendly_name().encode('utf-8'))

        for c in self.ws.children:
                cl += '<li><a href=%s%s>%s</a></li>' % (uri,c,c)
        return cl

    def render(self,request):
        return """<html><head><title>Coherence</title></head><body>
<a href="http://coherence.beebits.net">Coherence</a> - a Python UPnP A/V framework for the Digital Living<p>Hosting:<ul>%s</ul></p></body></html>""" % self.listchilds(request.uri)

class WebServer(object):

    def __init__(self, config, deviceList):
#        self.web_server = WebServer( config.get('web-ui',None), int(config.get('serverport', 0)), self)

        ui = config.get('web-ui',None)
        self._deviceList = deviceList
        self.children = {}
        self.web_server_port = int(config.get('serverport', 0))

        network_if = config.get('interface')
	self.hostname = None
        if network_if:
            self.hostname = get_ip_address(network_if)
	    if self.hostname is None:
		# invalid interface
                _log.error("Invalid interface name %s", network_if)

	if self.hostname is None:
            try:
                self.hostname = socket.gethostbyname(socket.gethostname())
            except socket.gaierror:
                _log.error("hostname can't be resolved, maybe a system misconfiguration?")
                self.hostname = '127.0.0.1'

        if self.hostname == '127.0.0.1':
            """ use interface detection via routing table as last resort """
            self.hostname = get_host_address()

        _log.info('running on host: %s' % self.hostname)
        if self.hostname == '127.0.0.1':
            _log.error('detection of own ip failed, using 127.0.0.1 as own address, functionality will be limited')

        try:
            if ui != 'yes':
                """ use this to jump out here if we do not want
                    the web ui """
                raise ImportError

            from nevow import __version_info__, __version__
            if __version_info__ <(0,9,17):
                _log.warning( "Nevow version %s too old, disabling WebUI" % __version__)
                raise ImportError

            from nevow import appserver, inevow
            from coherence.web.ui import Web, IWeb, WebUI
            from twisted.python.components import registerAdapter

            def ResourceFactory( original):
                return WebUI( IWeb, original)

            registerAdapter(ResourceFactory, Web, inevow.IResource)

            self.web_root_resource = Web(coherence)
            self.site = appserver.NevowSite( self.web_root_resource)
        except ImportError:
            self.site = Site(SimpleRoot(self))

        port = reactor.listenTCP( self.web_server_port, self.site)
        self.web_server_port = port._realPortNumber

        # XXX: is this the right way to do it?
        self.urlbase = 'http://%s:%d/' % (self.hostname, self.web_server_port )
        _log.info( "WebServer at %s ready" % (self.urlbase) )

    def port():
        return self.web_server_port

    def urlbase():
        return self.urlbase

    def add_web_resource(self, name, render):
        # Add a new resource to our webserver
        # render is the class that haandles rendering for this resource
        # name is the relative name for the resource
        # returns the full URL for the resource
        _log.info( "add_web_resource %s (%s)" %(name, render) )
        self.children[name] = render
        return "%s%s" %(self.urlbase, name)

    def remove_web_resource(self, name):
        # XXX implement me
        _log.info( "remove_web_resource %s", name)
