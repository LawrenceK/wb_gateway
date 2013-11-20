# $Id: Media.py 3138 2009-04-15 10:17:29Z philipp.schuster $

import sys, logging, string

from urlparse import urlparse, urljoin
from urllib import unquote, quote

import turbogears
import cherrypy
import ClientProfiles

from EventLib.Event         import Event
from EventLib.Status        import StatusVal
from EventLib.SyncDeferred  import makeDeferred

from EventLib.EventHandler  import EventHandler

from EventHandlers.BaseHandler import makeUri
from coherence.upnp.services.clients.caching_content_directory_client import UPNP_Container, UPNP_Item, UPNP_MediaServerList, device_name

from twisted.internet import reactor

import coherence.extern.louie as louie

_log = logging.getLogger( "WebBrickGateway.Media" )

# --------------------------------------------------
# Media interfaces
# --------------------------------------------------
class Media( object ):
    """
    Local class to handle queries for media details
    """
    def __init__(self):
        uri,logname = makeUri(self.__class__)
        super(Media,self).__init__(uri, self.doHandleEvent)
        # local ids are just indexes into these arrays.

        self._client_id = 0
        self._clients = {}  # UPNP clients

        self._servers = UPNP_MediaServerList()
        self.subcribeTimeout = 30

        # this needs to be early so we get to see the startup of the eventhandler.
        from coherence.base import Coherence
        self._coherence = Coherence()
        # subscribe to all events.
        louie.connect(self.new_server, 'Coherence.UPnP.ControlPoint.MediaServer.detected', louie.Any)
        louie.connect(self.new_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.detected', louie.Any)
        louie.connect(self.remove_server, 'Coherence.UPnP.ControlPoint.MediaServer.removed', louie.Any)
        louie.connect(self.remove_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.removed', louie.Any)

    def start( self, despatch ):
        pass

    def stop(self, despatch):
        louie.disconnect(self.new_server, 'Coherence.UPnP.ControlPoint.MediaServer.detected', louie.Any)
        louie.disconnect(self.new_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.detected', louie.Any)
        louie.disconnect(self.remove_server, 'Coherence.UPnP.ControlPoint.MediaServer.removed', louie.Any)
        louie.disconnect(self.remove_renderer, 'Coherence.UPnP.ControlPoint.MediaRenderer.removed', louie.Any)

    def doHandleEvent( self, handler, event ):
        et = event.getType()
        od = event.getPayload()

        return makeDeferred(StatusVal.OK)

    def new_renderer(self, client, udn ):
        # UPNP interface, the client is the local client to a UPNP renderer.
        # again container ids are just integers.

        for k in self._clients:
            if self._clients[k].device.get_id() == udn:
                _log.debug( "Update already exists %s", udn )
                #self._clients[k] = client
                return

        self._client_id = self._client_id + 1
        self._clients[self._client_id] = client
        _log.debug( "new_renderer %u id %s", self._client_id, udn )

    def remove_renderer(self, client, udn ):
        _log.debug( "remove_renderer id %s", udn )
        for k in self._clients:
            if self._clients[k].device.get_id() == udn:
                _log.debug( "removed renderer id %s", udn )
                del self._clients[k]
                break

    def new_server(self, client, udn ):
        # UPNP interface, the client is the local client to a UPNP server.
        # again container ids are just integers.
        _log.debug( "new_server udn %s", udn )
        self._servers.add_server( client, udn )

    def remove_server(self, client, udn ):
        _log.debug( "remove_server id %s", udn )
        self._servers.remove_server( client, udn )

    def log_result(self, result):
        for k in result:
            itm = result[k]
            if isinstance( itm, (list,tuple) ):
                for itm2 in itm:
                    _log.debug( "    item %s : %s", k, itm2 )
            elif isinstance( itm, (dict) ):
                _log.debug( "    item %s :", k )
                for key2 in itm:
                    itm2 = itm[key2]
                    _log.debug( "        item %s : %s", key2, itm2 )
            else:
                _log.debug( "item %s : %s", k, itm )

#
# list returns a container-id and a list of entries, the list may be returned as a dictionary for a template or XML
# 
    def generate_list(self, result, rid, id, offset, limit):
        #
        # if id is none then list the server sources.
        # else it a server-id:container-id.
        # 
        # Output is an update to the result dictionary
        # and the id of the container it is from.
        #
        _log.debug( "list id %s", id )
        result["rid"] = str(rid)    # in case browsing after select renderer
        if rid:
            rid = int(rid)
            result["name"] = device_name(self._clients[rid])
        else:
            result["name"] = ""

        srvc = None
        if id:
            srvc = self._servers.get_server(id)
            if srvc:
                ctr = srvc.get_container( id )

        elif rid and self._clients.has_key(rid):
            srvc = self._servers.default_server_for_renderer(device_name(self._clients[rid]))
            if srvc:
                id = srvc.get_top_level_container_id()
                ctr = srvc.get_container( id )

        result["title"] = "Browse"
        if srvc:
            _log.debug( "ctr %s", ctr )
            if ctr: 
                result["title"] = ctr.title()
#            result["title"] = "%s %s %s" % (ctr.artist(), ctr.album(), ctr.title())
            result["items"] = list()
            for ntry in srvc.enum_container(ctr, offset):
                result["items"].append( ntry )
                if len(result["items"]) >= limit:
                    break

            result["id"] = id   # container id
            result["offset"] = offset
            result["total"] = ctr.size()
            result["count"] = len(result["items"])
            result["limit"] = limit

            result["breadcrumb"] = srvc.get_breadcrumb_trail(ctr)

        else:
            result["items"] = self._servers.get_servers()

    def add_clients(self,result):
        result["clients"] = {}
        result["links"] = {}
        for k in self._clients:
            clnt = self._clients[k]
            if clnt:
                result["clients"][k] = device_name(clnt)
                result["links"][k] = {}
                for k2 in self._clients:
                    if k2 <> k and self._clients[k2]:
                        # This shows wheteher we should display Link/UnLink for this client pair.
                        result["links"][k][k2] = (True,True)

    # as a dictionary and as XML
    @turbogears.expose(template="WebBrickGateway.templates.mediaclient")
    def client(self,rid):
        rid = int(rid)
        if not self._clients.has_key(rid):
            return self.clients()   # no longer present.

        result = ClientProfiles.makeStandardResponse( cherrypy.request, "mediaclient" )

        result["rid"] = rid
        result["def_folder"] = ""   # blank
        result["sid"] = ""
        srvc = self._servers.default_server_for_renderer(device_name(self._clients[rid]))
        if srvc:
            result["sid"] = srvc._server_id
            result["def_folder"] = srvc.get_default_container_id()
        result["limit"] = 50

        # udn needed so client can pick up the correct event set.
        result["udn"] = self._clients[rid].device.get_id()
        result["name"] = device_name(self._clients[rid])
        result["hasTransport"] = True   # play,pause,position etc.
        result["hasRenderer"] = True    # volume
        result["showServers"] = True    # so can select tracks etc.
        self.add_clients( result )

        return result

# UPNP/media interface
#
    @turbogears.expose(template="WebBrickGateway.templates.showqueue")
    def showqueue(self, rid):
        rid = int(rid)
        id = None
        srvc = self._servers.default_server_for_renderer(device_name(self._clients[rid]))
        if srvc:
            id = srvc.get_default_container_id()

        result = ClientProfiles.makeStandardResponse( cherrypy.request, "showqueue" )
        self.generate_list(result, rid, id, 0, sys.maxint )

        self.log_result(result)

        return result

#
# list returns a container-id and a list of entries, the list may be returned as a dictionary for a template or XML
# 
    @turbogears.expose(template="WebBrickGateway.templates.mediabrowse")
    def list(self, rid, id, offset, limit):
        #
        # return a list of entries
        # if id is none then list the server sources.
        # else it a server-id:container-id.
        # 
        # Output is a list of items
        # and the id of the container it is from.
        #
	#TODO create breadcrumb trail
	# refresh containers. May be better to get UPNP classes to handle this trail
	#
        _log.debug( "list id %s", id )

        result = ClientProfiles.makeStandardResponse( cherrypy.request, "mediabrowse" )
        self.generate_list(result, rid, id, int(offset), int(limit) )

        self.log_result(result)

        return result

    @turbogears.expose(template="WebBrickGateway.templates.mediaclientlist")
    def clients(self):
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "mediaclientlist" )

        self.add_clients( result )

        return result

    def do_play(self, id, rid, queue_item):
        # if id None/blank then add complete container to be played.
        # locate server
        # locate current renderer
        # add to renderer play list.
        _log.debug( "play id %s, on %s", id, rid )
        if rid:
            rid = int(rid)
            srv = self._servers.get_server(id)
            if srv:
                itm = srv.get_item( id )
            _log.debug( "%s play %s", srv, itm )
            # get hold of the server and add to queue.
            self._coherence.ctrl.play_item( srv._client, self._clients[rid], itm, queue_item )

    @turbogears.expose()
    def clearqueue(self, rid ):
        # empty queue and return queue again
        rid = int(rid)
        _log.debug( "clearqueue rid %s", rid )
        if self._clients.has_key(rid):
            self._coherence.ctrl.clear_queue( self._clients[rid] )

        return self.client(rid)
        #return self.showqueue(rid)

    @turbogears.expose()
    def deletefromqueue(self, id, rid ):
        # delete entry and return new contents.
        rid = int(rid)
        srv = self._servers.get_server(id)
        if srv and self._clients.has_key(rid):
            itm = srv.get_item( id )
            if itm:
                _log.debug( "deletefromqueue itm %s", itm )
                reactor.callFromThread( self._clients[rid].av_transport.remove_from_queue, itm.id() )
        return self.showqueue(rid)

    @turbogears.expose(template="WebBrickGateway.templates.mediazonelink")
    def zonelink(self, rid ):
        rid = int(rid)
        if not self._clients.has_key(rid):
            return self.clients()   # no longer present.

        result = ClientProfiles.makeStandardResponse( cherrypy.request, "mediazonelink" )

        result["rid"] = rid

        # udn needed so client can pick up the correct event set.
        result["udn"] = self._clients[rid].device.get_id()
        result["name"] = device_name(self._clients[rid])

        result["clients"] = {}
        for k in self._clients:
            clnt = self._clients[k]
            if clnt and k <> rid:   # exclude self.
                result["clients"][k] = device_name(clnt)

        # create list of zones
        return result

    @turbogears.expose()
    def albumart(self, id, uri):
        # the id of the track
        #srv = self._servers.get_server(id)
        #if srv:
        #    itm = srv.get_item( id )
        #    # get album art uri.
        # DUMB proxy
        #unescape uri
        # parse
        parsed = urlparse( unquote(uri) )

        #r = DoHTTPRequest(wbaddr, "GET", wbUri)


    @turbogears.expose()
    def dozonelink(self, rid, target ):
        _log.debug( "dozonelink rid %s target %s", rid, target )
        if rid and target:
            rid = int(rid)
            target = int(target)
            if self._clients.has_key(rid) and self._clients.has_key(target):
                src_udn = "x-rincon:%s" % self._clients[rid].device.get_root_id()[5:]
                _log.debug( "dozonelink source %s", src_udn )
                reactor.callFromThread( self._clients[target].av_transport.set_av_transport_uri, 0, src_udn)

        return self.zonelink(rid)

    @turbogears.expose()
    def dozonelinkall(self, rid):
        rid = int(rid)
        for k in self._clients:
            if k <> rid:
                self.dozonelink(rid, k )

        return self.zonelink(rid)

    @turbogears.expose()
    def dozoneunlink(self, target ):
        _log.debug( "dozoneunlink rid %s", target )
        if target:
            target = int(target)
            if self._clients.has_key(target):
                _log.debug( "dozonelink target %s", target )
                reactor.callFromThread( self._clients[target].av_transport.unlink_from_group )

        return self.clients()

    @turbogears.expose()
    def dozoneunlinkall(self, rid=None):
        for k in self._clients:
            if k <> rid:
                self.dozoneunlink(k )
        if rid:
            return self.zonelink(rid)
        return self.clients()

    @turbogears.expose()
    def play(self, id, rid=None, clearQ=None):
        # if this is a single item then just play
        # else clear the queue and add then play
        self.do_play(id,rid,False)

        return ''   # success/failure?

    @turbogears.expose()
    def queue(self, id, rid=None, clearQ=None):
        self.do_play(id,rid,True)

        return ''   # success/failure?

    @turbogears.expose()
    def playqueue(self, rid):
        _log.debug( "playqueue on %s", rid )
        if rid:
            rid = int(rid)
            srv = self._servers.default_server_for_renderer(device_name(self._clients[rid]))
            cid = srv.get_default_container_id()
            ctr = srv.get_container(cid)

            # get hold of the server and add to queue.
            self._coherence.ctrl.play_item( srv._client, self._clients[rid], ctr, False )
        return self.client(rid)

    @turbogears.expose()
    def index(self,*args):
        return self.clients( '' )

# $Id: Media.py 3138 2009-04-15 10:17:29Z philipp.schuster $
